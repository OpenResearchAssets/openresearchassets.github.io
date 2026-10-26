"""Dependency-light coordinator for Argos offline English to Chinese translation.

Install argostranslate in the GitHub Actions job, not in the public website.
Use a persistent model cache and per-run time budget. Model translations are
machine-generated, never editorial summaries. Preserve English for verification.
"""
from __future__ import annotations

import os
import re
import time

ARGOS_LIMIT_SECONDS = int(os.getenv("ARGOS_TRANSLATION_SECONDS", "780"))
PER_SOURCE_LIMIT = {
    "papers": 100,
    "github": 14,
    "skills": 14,
    "workflows": 14,
}


def is_chinese(text: str) -> bool:
    # A bilingual README with one Chinese label is still predominantly English.
    # Count visible language content rather than treating one Han character as
    # proof that the full paragraph is translated.
    han = len(re.findall(r"[\u3400-\u9fff]", text or ""))
    latin = len(re.findall(r"[A-Za-z]", text or ""))
    return han >= 2 and han / max(1, han + latin) >= 0.32


def load_translator(source: str = "en", target: str = "zh"):
    import argostranslate.package as package
    import argostranslate.translate as translate

    def installed_pair():
        languages = translate.get_installed_languages()
        from_lang = next((x for x in languages if x.code == source), None)
        to_lang = next((x for x in languages if x.code == target), None)
        return from_lang.get_translation(to_lang) if from_lang and to_lang else None

    found = installed_pair()
    if found:
        return found
    package.update_package_index()
    pair = next((x for x in package.get_available_packages()
                 if x.from_code == source and x.to_code == target), None)
    if pair is None:
        raise RuntimeError(f"Argos {source}->{target} package not available")
    package.install_from_path(pair.download())
    result = installed_pair()
    if result is None:
        raise RuntimeError("Argos language model installation did not complete")
    return result


def add_offline_translations(feeds: dict, previous_feeds: dict,
                             translator=None, seconds: int | None = None) -> tuple[str, int]:
    """Translate visible-first content; reuse source-exact cached text.

    Working set is ordered first by first-screen position across all four feeds,
    then by the next visible batch, then remaining papers. In-progress work is
    published in the snapshot after each successful run; subsequent refreshes
    continue from previously cached fields.
    """
    start = time.monotonic()
    old = {}
    for key in PER_SOURCE_LIMIT:
        old[key] = {
            item.get("url"): item
            for item in previous_feeds.get(key, {}).get("items", [])
            if isinstance(item, dict)
        }
    tasks: list[tuple[dict, str, str]] = []
    reverse_tasks: list[tuple[dict, str, str]] = []
    reused = 0
    for index in range(100):
        for feed_name, limit in PER_SOURCE_LIMIT.items():
            if index >= limit:
                continue
            feed = feeds.get(feed_name, {})
            if feed.get("status") != "ok":
                continue
            items = feed.get("items", [])
            if index >= len(items):
                continue
            current = items[index]
            prior = old[feed_name].get(current.get("url"), {})
            fields = ("title", "detail") if feed_name == "papers" else ("subtitle", "detail")
            for field in fields:
                original = current.get(field)
                dest = field + "_zh"
                if not isinstance(original, str) or len(original.strip()) < 14:
                    continue
                if is_chinese(original):
                    current[dest] = original
                    english_field = field + "_en"
                    if prior.get(field) == original and prior.get(english_field):
                        current[english_field] = prior[english_field]
                        reused += 1
                    elif not current.get(english_field):
                        reverse_tasks.append((current, english_field, original))
                    continue
                if prior.get(field) == original and is_chinese(prior.get(dest, "")):
                    current[dest] = prior[dest]
                    reused += 1
                elif is_chinese(current.get(dest, "")):
                    continue
                else:
                    tasks.append((current, dest, original))
    if not tasks and not reverse_tasks:
        _propagate_preview(feeds)
        return ("cached" if reused else "not_configured"), reused
    try:
        engine = translator or load_translator()
    except Exception as exc:
        print(f"Argos translation unavailable: {type(exc).__name__}: {str(exc)[:110]}")
        _propagate_preview(feeds)
        return ("cached" if reused else "unavailable"), reused

    processed = 0
    deadline = seconds if seconds is not None else ARGOS_LIMIT_SECONDS
    for entry, target, source in tasks:
        if time.monotonic() - start > deadline:
            print(f"Argos time budget reached after {processed} new fields; remaining cached next run")
            break
        try:
            converted = engine.translate(source).strip()
            if is_chinese(converted) and len(converted) >= 4:
                entry[target] = converted[:8500]
                processed += 1
        except Exception as exc:
            print(f"Argos item error: {type(exc).__name__}: {str(exc)[:100]}")
    if reverse_tasks and time.monotonic()-start<deadline:
        try:
            reverse_engine = load_translator("zh", "en")
            for entry, target, source in reverse_tasks:
                if time.monotonic()-start > deadline:
                    break
                result = reverse_engine.translate(source).strip()
                latin = len(re.findall(r"[A-Za-z]", result))
                if latin >= 12 and not is_chinese(result):
                    entry[target] = result[:8500]
                    processed += 1
        except Exception as exc:
            print(f"Reverse translation unavailable: {type(exc).__name__}: {str(exc)[:110]}")
    _propagate_preview(feeds)
    return ("offline_argos" if processed else "cached" if reused else "unavailable",
            processed + reused)


def _propagate_preview(feeds: dict) -> None:
    for paper in feeds.get("papers", {}).get("items", []):
        translated = paper.get("detail_zh", "")
        if translated and is_chinese(translated):
            paper["subtitle_zh"] = translated[:850]
