#!/usr/bin/env python3
"""Generate derived AI search files from the canonical catalog/index.json.

Run python3 tools/sync_catalog.py (or --check).
Do not edit manifest.json or entry fragments manually.
"""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / "catalog/index.json").read_text(encoding="utf-8"))
entries = catalog["entries"]
assert len({e["id"] for e in entries}) == len(entries), "duplicate asset ID"

manifest = {
    "schema_version": catalog["schema_version"],
    "catalog_source": "catalog/index.json",
    "generated_on": catalog["generated_on"],
    "instructions": {
        "zh": "先匹配此轻量目录，再沿 entry 路径只读取最相关条目。第三方图片默认不可复制，只有单条 rights 明确授权才可复用。",
        "en": "Select from this lightweight manifest, then fetch only relevant entry JSON files. External visuals are not licensed for copying by default; inspect each entry's rights."
    },
    "facets": catalog["facets"],
    "entries": [{
        "id": e["id"], "title": e["title"], "kind": e["kind"],
        "stages": e["stages"], "domains": e["domains"], "topics": e["topics"], "tasks": e["tasks"],
        "keywords": e["keywords"]["zh"] + e["keywords"]["en"],
        "description_zh": e["description"]["zh"],
        "entry": "catalog/entries/" + e["id"] + ".json"
    } for e in entries]
}
dump = lambda obj: json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
outputs = {root / "catalog/manifest.json": dump(manifest)}
for entry in entries:
    outputs[root / "catalog/entries" / (entry["id"] + ".json")] = dump(entry)
entry_folder = root / "catalog/entries"
old = set(entry_folder.glob("*.json"))
extra = old - set(outputs)
if "--check" in sys.argv:
    stale = [str(p.relative_to(root)) for p,c in outputs.items()
             if not p.is_file() or p.read_text(encoding="utf-8") != c]
    if stale or extra:
        print("STALE:", stale + sorted(str(p.relative_to(root)) for p in extra))
        raise SystemExit(1)
    print("PASS: derived catalog", len(entries), "entries")
else:
    entry_folder.mkdir(parents=True, exist_ok=True)
    for p,content in outputs.items():
        p.write_text(content, encoding="utf-8")
    for p in extra:
        p.unlink()
    print("Generated", len(entries), "entry files and manifest")
