#!/usr/bin/env python3
"""Build a sourced, static Findings snapshot. No content is invented on failure.

Runs in GitHub Actions (scheduled) and keeps the last successful source-specific
data if one upstream becomes unavailable. The editorial catalog is untouched.
"""
from __future__ import annotations

import datetime as dt
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "findings.json"
UTC = dt.timezone.utc
REPO_PATH = re.compile(r"^/([A-Za-z0-9-]+)/([A-Za-z0-9_.-]+)/?$")
GH_SOURCE = "https://github.com/trending?since=weekly"
HF_SOURCE = "https://huggingface.co/papers/trending"
SKILL_SOURCE = "https://skills.sh/trending"
WORKFLOW_SOURCE = "https://github.com/search?q=research+workflow&type=repositories"
MAX_RESULTS = 14
MAX_LENGTH = 520


def now() -> str:
    return dt.datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def plain(value: object, max_len: int = MAX_LENGTH) -> str:
    text = html.unescape(str(value if value is not None else ""))
    return " ".join(text.split())[:max_len]


def valid_url(value: object, host: str | None = None) -> str:
    try:
        url = urllib.parse.urlsplit(str(value))
        if url.scheme != "https" or not url.hostname:
            return ""
        if host and url.hostname != host:
            return ""
        return urllib.parse.urlunsplit((url.scheme, url.netloc, url.path, url.query, ""))
    except (TypeError, ValueError):
        return ""


def request_bytes(url: str, *, accept: str = "application/json") -> bytes:
    headers = {"User-Agent": "OpenResearchAssets-Findings/1.0 (public source monitor)",
               "Accept": accept}
    if urllib.parse.urlsplit(url).hostname == "api.github.com" and os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=22) as response:
        return response.read(2_000_000)


def request_json(url: str) -> object:
    return json.loads(request_bytes(url))


def item(**values: object) -> dict:
    record = {key: value for key, value in values.items() if value is not None}
    for key in ("title", "subtitle", "author", "badge"):
        if key in record:
            record[key] = plain(record[key], 210 if key == "title" else MAX_LENGTH)
    url = valid_url(record.get("url", ""))
    if not url or not record.get("title"):
        raise ValueError("Incomplete sourced item")
    record["url"] = url
    if "value" in record and (not isinstance(record["value"], int) or record["value"] < 0):
        record.pop("value")
    return record


def fetch_papers() -> tuple[list[dict], str, str]:
    # Official huggingface_hub interface; no API-token or HTML scraping needed.
    from huggingface_hub import HfApi
    api = HfApi(token=False)
    papers = list(api.list_daily_papers(sort="trending", limit=MAX_RESULTS, token=False))
    entries = []
    for paper in papers:
        pid = plain(getattr(paper, "id", ""), 80)
        if not re.fullmatch(r"\d{4}\.\d{4,5}(?:v\d+)?", pid):
            continue
        date = getattr(paper, "published_at", None)
        date_str = date.isoformat() if isinstance(date, (dt.datetime, dt.date)) else None
        entries.append(item(title=getattr(paper, "title", ""),
                            url="https://huggingface.co/papers/" + pid,
                            subtitle=getattr(paper, "summary", ""),
                            author=pid, value=getattr(paper, "upvotes", None),
                            badge=date_str or "", metric="upvotes"))
    if not entries:
        raise ValueError("Hugging Face did not return valid trending papers")
    return entries, "Hugging Face Papers", "HF 社区投票 · 官方 trending 排序"


class TrendingHTMLParser(HTMLParser):
    """Read repository identities and visible copy from GitHub's public weekly Trending page."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = None
        self.in_h2 = False
        self.in_p = False
        self.records: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        a = dict(attrs)
        if tag == "article" and "Box-row" in a.get("class", ""):
            self.active = {"href": "", "pieces": [], "description": [], "period": []}
        if self.active is None:
            return
        if tag == "h2":
            self.in_h2 = True
        elif tag == "p" and not self.active["description"]:
            self.in_p = True
        elif tag == "a" and self.in_h2:
            path = urllib.parse.urlsplit(a.get("href", "")).path
            if REPO_PATH.fullmatch(path):
                self.active["href"] = path

    def handle_data(self, data: str) -> None:
        if self.active is None:
            return
        val = plain(data)
        if not val:
            return
        self.active["pieces"].append(val)
        if self.in_p:
            self.active["description"].append(val)

    def handle_endtag(self, tag: str) -> None:
        if self.active is None:
            return
        if tag == "h2":
            self.in_h2 = False
        elif tag == "p":
            self.in_p = False
        elif tag == "article":
            if self.active["href"]:
                self.records.append(self.active)
            self.active = None
            self.in_p = False
            self.in_h2 = False


def parse_github_trending(body: str) -> list[dict]:
    parser = TrendingHTMLParser()
    parser.feed(body)
    entries = []
    seen = set()
    for record in parser.records:
        path = record["href"]
        if path in seen:
            continue
        seen.add(path)
        title = path.strip("/")
        visible = " ".join(record["pieces"])
        match = re.search(r"([\d,]+)\s+stars?\s+this\s+week", visible, re.I)
        gain = int(match.group(1).replace(",", "")) if match else None
        entries.append(item(title=title, url="https://github.com" + path,
                            subtitle=" ".join(record["description"])[:MAX_LENGTH],
                            badge="GitHub Trending · weekly",
                            value=gain, metric="stars gained this week" if gain is not None else "position"))
        if len(entries) >= MAX_RESULTS:
            break
    return entries


def fetch_github_trending() -> tuple[list[dict], str, str]:
    body = request_bytes(GH_SOURCE, accept="text/html").decode("utf-8", errors="replace")
    entries = parse_github_trending(body)
    if not entries:
        raise ValueError("GitHub Trending page did not expose recognizable repository cards")
    return entries, "GitHub Trending", "官方 weekly Trending 排名；可见时显示本周新增 Stars"


def github_search(query: str, per_page: int = 18) -> list[dict]:
    params = urllib.parse.urlencode({
        "q": query, "sort": "stars", "order": "desc", "per_page": per_page
    })
    data = request_json("https://api.github.com/search/repositories?" + params)
    if not isinstance(data, dict):
        raise ValueError("GitHub search returned non-object")
    return data.get("items", []) if isinstance(data.get("items"), list) else []


def repo_records(repos: list[dict], *, badge: str, limit: int = MAX_RESULTS) -> list[dict]:
    entries: list[dict] = []
    seen: set[str] = set()
    for repo in repos:
        identity = repo.get("full_name", "")
        url = valid_url(repo.get("html_url"), "github.com")
        if not re.fullmatch(r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+", identity) or not url or identity in seen:
            continue
        seen.add(identity)
        entries.append(item(title=identity, url=url,
                            subtitle=repo.get("description", ""),
                            badge=badge, author=repo.get("language") or "",
                            value=repo.get("stargazers_count"), metric="total stars"))
        if len(entries) >= limit:
            break
    return entries


def new_repos(queries: list[str], days: int = 60) -> list[dict]:
    since = (dt.datetime.now(UTC) - dt.timedelta(days=days)).date().isoformat()
    combined: dict[str, dict] = {}
    for term in queries:
        for entry in github_search(term + " created:>=" + since):
            identity = entry.get("full_name")
            if isinstance(identity, str):
                combined[identity] = entry
    return sorted(combined.values(), key=lambda x: x.get("stargazers_count") or 0, reverse=True)


def fetch_skills() -> tuple[list[dict], str, str]:
    # Skills.sh documents this API, but some hosts require a Vercel OIDC token.
    # Anonymous rejection is expected; never impersonate an authorized client.
    try:
        data = request_json("https://skills.sh/api/v1/skills?view=trending&per_page=20")
        values = data.get("data", []) if isinstance(data, dict) else []
        results = []
        for row in values:
            if not isinstance(row, dict):
                continue
            target = valid_url(row.get("url"), "skills.sh")
            if not target:
                continue
            results.append(item(title=row.get("name") or row.get("slug"),
                                subtitle=row.get("source", ""), url=target,
                                author=row.get("source"), badge="Skills.sh · trending",
                                value=row.get("installs"), metric="total installs"))
            if len(results) >= MAX_RESULTS:
                break
        if results:
            return results, "Skills.sh", "官方 Trending 排名 · 累计安装量"
    except (urllib.error.URLError, ValueError, TimeoutError, OSError):
        pass
    # Clearly named fallback, NOT falsely described as a Skills.sh ranking.
    results = repo_records(new_repos(["topic:agent-skills", "topic:claude-skills"], 60),
                           badge="GitHub · 新创建 Skills 仓库")
    if not results:
        raise ValueError("Neither Skills.sh nor GitHub skills discovery was available")
    return results, "GitHub Search", "近 60 天创建的 Skills 仓库，按累计 Stars 排序（非增长榜）"


def fetch_workflows() -> tuple[list[dict], str, str]:
    results = repo_records(new_repos([
        "topic:agent-workflow", "topic:research-workflow",
        "workflow automation in:name,description"
    ], 60), badge="GitHub · 新创建工作流")
    if not results:
        raise ValueError("GitHub workflow discovery returned no new repositories")
    return results, "GitHub Search", "近 60 天创建的工作流项目，按累计 Stars 排序（非 Trending 官方榜）"


def fallback_feed(name: str, url: str, previous: dict | None) -> dict:
    if isinstance(previous, dict) and previous.get("items") and previous.get("fetched_at"):
        return {**previous, "status": "stale"}
    return {"source": name, "url": url, "fetched_at": None,
            "status": "unavailable", "metric_note": "", "items": []}


def build(existing: dict | None = None) -> dict:
    existing = existing if isinstance(existing, dict) else {}
    old_feeds = existing.get("feeds") if isinstance(existing.get("feeds"), dict) else {}
    settings = {
        "papers": (fetch_papers, "Hugging Face Papers", HF_SOURCE),
        "github": (fetch_github_trending, "GitHub Trending", GH_SOURCE),
        "skills": (fetch_skills, "Skills.sh / GitHub Search", SKILL_SOURCE),
        "workflows": (fetch_workflows, "GitHub Search", WORKFLOW_SOURCE)
    }
    feeds = {}
    for key, (fetcher, source, link) in settings.items():
        try:
            entries, name, note = fetcher()
            if not entries:
                raise ValueError("No valid source entries")
            feeds[key] = {"source": name, "url": link, "fetched_at": now(),
                          "status": "ok", "metric_note": note,
                          "items": entries[:MAX_RESULTS]}
            print(f"{key}: {len(entries)} verified-source items ({name})")
        except Exception as error:
            feeds[key] = fallback_feed(source, link, old_feeds.get(key))
            print(f"{key}: source unavailable ({type(error).__name__}: {str(error)[:160]})", file=sys.stderr)
    return {"schema_version": "1", "generated_at": now(), "feeds": feeds}


def main() -> int:
    previous = {}
    if OUTPUT.is_file():
        try:
            previous = json.loads(OUTPUT.read_text("utf-8"))
        except (OSError, ValueError):
            pass
    result = build(previous)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    successful = sum(bool(f["items"]) and f["status"] == "ok" for f in result["feeds"].values())
    print(f"Findings snapshot: {successful}/4 sources refreshed")
    return 0  # Source failures do not fabricate results or erase previous good snapshots.


if __name__ == "__main__":
    raise SystemExit(main())
