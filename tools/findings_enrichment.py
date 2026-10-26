"""Optional sourced README extracts and Google Cloud translations for Findings.

No generative summaries. Never use Google credentials on the public website.
Translations are cached inside the committed snapshot and only refreshed when
the English source text changes.
"""
from __future__ import annotations

import base64
import html
import json
import os
import re
import urllib.parse
import urllib.request

API_ROOT = "https://api.github.com/repos/"
TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"
README_LIMIT_PER_FEED = 10
TRANSLATE_LIMIT = 53000


def clean_text(source: str, limit: int = 1400) -> str:
    value = html.unescape(str(source or ""))
    # Strip embeds and fenced source code before selecting descriptive paragraphs.
    value = re.sub(r"<(script|style)\b[^>]*>[\s\S]*?</\1>", " ", value, flags=re.I)
    value = re.sub(r"(?ms)^\s*\x60{3}.*?^\s*\x60{3}\s*$", " ", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"(?m)^\s*(?:#|>|[*-]\s|\|).*?$", " ", value)
    value = re.sub(r"(?:\x60|[*_]{1,3})", "", value)
    paragraphs = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", value)]
    informative = [p for p in paragraphs if len(p) >= 75
                   and not re.match(r"(install|usage|contribute|requirements|license)\b", p, re.I)]
    return " ".join(informative[:3])[:limit]


def repository_name(record: dict) -> str | None:
    match = re.fullmatch(r"([A-Za-z0-9-]+)/([A-Za-z0-9_.-]+)", str(record.get("title") or ""))
    url = str(record.get("url") or "")
    if not match or url.rstrip("/") != "https://github.com/" + match.group(0):
        return None
    return match.group(0)


def load_readme(record: dict, token: str | None = None) -> str:
    repo = repository_name(record)
    if not repo:
        return ""
    request = urllib.request.Request(
        API_ROOT + repo + "/readme",
        headers={"Accept": "application/vnd.github+json",
                 "User-Agent": "OpenResearchAssets-Findings/1.0",
                 **({"Authorization": "Bearer " + token} if token else {})},
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or payload.get("encoding") != "base64":
        return ""
    decoded = base64.b64decode(str(payload.get("content") or ""), validate=False)
    if len(decoded) > 320_000:
        return ""
    return clean_text(decoded.decode("utf-8", errors="replace"))


def enrich_readmes(feeds: dict, old_feeds: dict) -> int:
    token = os.getenv("GITHUB_TOKEN")
    count = 0
    for kind in ("github", "skills", "workflows"):
        feed = feeds.get(kind, {})
        if feed.get("status") != "ok":
            continue
        old_lookup = {x.get("url"): x for x in old_feeds.get(kind, {}).get("items", [])
                      if isinstance(x, dict)}
        for entry in feed.get("items", [])[:README_LIMIT_PER_FEED]:
            previous = old_lookup.get(entry.get("url"), {})
            # Stable README source notes: fetch once if already useful. Avoid
            # 30 repeated API requests every six hours unless content was absent.
            if previous.get("detail") and previous.get("summary_source") == "repository README":
                entry["detail"] = previous["detail"]
                entry["summary_source"] = "repository README"
                count += 1
                continue
            try:
                excerpt = load_readme(entry, token)
                if len(excerpt) > 90:
                    entry["detail"] = excerpt
                    entry["summary_source"] = "repository README"
                    count += 1
            except Exception as exc:
                print(f"README unavailable for {entry.get('title')}: {type(exc).__name__}")
    return count


def google_translate(texts: list[str], api_key: str) -> list[str]:
    # Official Google Cloud Translation Basic v2, POST + batch; key is NEVER
    # printed or placed in browser content. Set secret in repository Actions.
    body = json.dumps({"q": texts, "target": "zh-CN", "format": "text"},
                      ensure_ascii=False).encode("utf-8")
    url = TRANSLATE_URL + "?" + urllib.parse.urlencode({"key": api_key})
    request = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json",
                                 "User-Agent": "OpenResearchAssets-Findings/1.0"},
        method="POST")
    with urllib.request.urlopen(request, timeout=25) as response:
        result = json.load(response)
    translated = result["data"]["translations"]
    if len(translated) != len(texts):
        raise ValueError("Google Translation returned a partial response")
    return [html.unescape(x["translatedText"]) for x in translated]


def add_translations(feeds: dict, old_feeds: dict, key: str | None = None) -> tuple[str, int]:
    """Reuse identical translations and translate only missing fields up to budget.

    Google Translate is opt-in to avoid a billable API call every six hours.
    """
    key = key or os.getenv("GOOGLE_TRANSLATE_API_KEY", "")
    # Spread the fixed-cost envelope across content families; otherwise 100
    # paper abstracts would permanently starve project/workflow translations.
    remaining_by_feed = {"papers": 30000, "github": 8000,
                         "skills": 7500, "workflows": 7500}
    queue: list[tuple[dict, str, str]] = []
    reused = 0
    for kind in ("papers", "github", "skills", "workflows"):
        feed = feeds.get(kind, {})
        if feed.get("status") != "ok":
            continue
        old_lookup = {x.get("url"): x for x in old_feeds.get(kind, {}).get("items", [])
                      if isinstance(x, dict)}
        max_records = 100 if kind == "papers" else 14
        for entry in feed.get("items", [])[:max_records]:
            previous = old_lookup.get(entry.get("url"), {})
            for field in (("title", "detail") if kind == "papers"
                          else ("subtitle", "detail")):
                raw = entry.get(field)
                if not isinstance(raw, str) or len(raw.strip()) < 15:
                    continue
                dest = field + "_zh"
                if previous.get(field) == raw and previous.get(dest):
                    entry[dest] = previous[dest]
                    reused += 1
                elif key and remaining_by_feed[kind] >= len(raw):
                    queue.append((entry, dest, raw))
                    remaining_by_feed[kind] -= len(raw)
    def copy_abstract_preview():
        # Abstract details begin with the same passage as the shorter preview.
        # Reuse one paid translation instead of billing for overlapping text.
        for entry in feeds.get("papers", {}).get("items", []):
            if entry.get("detail_zh"):
                entry["subtitle_zh"] = entry["detail_zh"][:650]

    if not key:
        copy_abstract_preview()
        return ("cached" if reused else "not_configured"), reused
    translated_count = 0
    # Avoid partial translations for individual batches on remote errors.
    for start in range(0, len(queue), 12):
        batch = queue[start:start + 12]
        try:
            translations = google_translate([x[2] for x in batch], key)
            for (record, field, _), text in zip(batch, translations):
                record[field] = text[:3000]
                translated_count += 1
        except Exception as exc:
            # Never log the request URI or auth parameters.
            print(f"Google Translation failed for a batch: {type(exc).__name__}")
            break
    copy_abstract_preview()
    return ("translated" if translated_count else "cached" if reused else "unavailable",
            translated_count + reused)
