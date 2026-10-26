"""Apply reviewed Chinese lead-ins only when source records are unchanged.

These are translations of public data, not Curated membership or new source
claims. No saved text may silently override a changed upstream description.
"""
from __future__ import annotations
import json
from pathlib import Path

OVERRIDES = Path(__file__).resolve().parents[1] / "data" / "findings_editorial_zh.json"


def apply_editorial_chinese(feeds: dict, path: Path = OVERRIDES) -> int:
    if not path.is_file():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    rules = {row["url"]: row for row in data.get("overrides", [])
             if isinstance(row, dict) and row.get("url")}
    updated = 0
    for feed in feeds.values():
        for entry in feed.get("items", []):
            override = rules.get(entry.get("url"))
            if not override:
                continue
            if entry.get("title") != override.get("source_title") or (
                entry.get("subtitle") != override.get("source_subtitle")
            ):
                continue
            for field in ("title_zh", "subtitle_zh"):
                if override.get(field):
                    entry[field] = override[field]
            entry["zh_intro_reviewed"] = True
            updated += 1
    return updated
