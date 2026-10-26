"""Chinese punctuation normalization for translated Findings prose.

Preserve technical syntax including decimals, versions, URLs, filenames and code.
Only normalize Chinese-language fields; never mutate source-language data.
"""
from __future__ import annotations

import re

_HAN = re.compile(r"[\u3400-\u9fff]")
_URL = re.compile(r'https?://[^\s<>\u3000"“”\u3400-\u9fff，。；！？]+', re.IGNORECASE)
_CODE = re.compile(chr(96) + r"[^" + chr(96) + r"\n]+" + chr(96))


def normalize_zh_typography(value: str) -> str:
    if not isinstance(value, str) or not _HAN.search(value):
        return value
    protected = [False] * len(value)
    for expression in (_CODE, _URL):
        for m in expression.finditer(value):
            end = m.end()
            if expression is _URL:
                while end > m.start() and value[end - 1] in ".,;!":
                    end -= 1
            for pos in range(m.start(), end):
                protected[pos] = True
    result: list[str] = []
    for i, char in enumerate(value):
        if protected[i] or char not in ".,;:!?":
            result.append(char)
            continue
        prev = value[i - 1] if i else ""
        nxt = value[i + 1] if i + 1 < len(value) else ""
        if char == ".":
            # Decimal/version separators, filenames and dotted identifiers.
            if prev.isascii() and prev.isalnum() and nxt.isascii() and nxt.isalnum():
                result.append(char)
            elif nxt.isascii() and nxt.isalpha() and (prev in "/\\" or prev == chr(96)):
                result.append(char)
            else:
                result.append("。")
        elif char == ",":
            result.append("," if prev.isdecimal() and nxt.isdecimal() else "，")
        elif char == ":":
            result.append(":" if (prev.isdigit() and nxt.isdigit()) or nxt in "/\\" else "：")
        else:
            result.append({";": "；", "?": "？", "!": "！"}[char])
    normalized = "".join(result)
    normalized = re.sub(r"\s+([，。；：！？])", r"\1", normalized)
    normalized = re.sub(r"([，。；：！？])\s+(?=[\u3400-\u9fff])", r"\1", normalized)
    return normalized


def normalize_translated_feeds(feeds: dict) -> int:
    changed = 0
    for feed in feeds.values():
        for record in feed.get("items", []):
            for field in ("title_zh", "subtitle_zh", "detail_zh"):
                if record.get(field):
                    updated = normalize_zh_typography(record[field])
                    if updated != record[field]:
                        record[field] = updated
                        changed += 1
    return changed
