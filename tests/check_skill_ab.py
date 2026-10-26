#!/usr/bin/env python3
"""Free offline checks: arm equality, gold isolation, scoring, and balanced order."""
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("run_skill_ab",ROOT/"tools/run_skill_ab.py")
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)
d=json.loads((ROOT/"experiments/skill-ab/tasks.json").read_text(encoding="utf-8"))
g={x["id"]:x["selected"] for x in json.loads((ROOT/"experiments/skill-ab/gold.json").read_text(encoding="utf-8"))["gold"]}
m.validate_data(d,g)
pairs=m.schedule(d["tasks"],20261026)
assert len(pairs)==12
assert sum(pairs[i]["arm"]=="skill" for i in range(0,12,2))==3
assert sum(pairs[i]["arm"]=="no_skill" for i in range(0,12,2))==3
for i in range(0,12,2):
    assert pairs[i]["task_id"]==pairs[i+1]["task_id"]
    assert {x["arm"] for x in pairs[i:i+2]}=={"skill","no_skill"}
for t in d["tasks"]:
    a=m.make_messages(t,d["skill_protocols"],"no_skill")
    b=m.make_messages(t,d["skill_protocols"],"skill")
    assert a[1]==b[1]
    assert len(a)==len(b)==2
    assert "SOURCE-GUIDED SKILL" not in a[0]["content"]
    assert "SOURCE-GUIDED SKILL" in b[0]["content"]
    p,err=m.parse_response(json.dumps({"selected":g[t["id"]],"reason":"ok"}),t["options"])
    assert err is None and m.score(p,g[t["id"]])["exact"]
    assert m.parse_response('{"selected":["INVALID"],"reason":"x"}',t["options"])[0] is None
    assert m.score(None,g[t["id"]])["f1"]==0
    assert m.parse_response('{"selected":["A","A"],"reason":"x"}',t["options"])[0] is None
print("PASS: six gold-isolated tasks, twelve paired arms, scoring and JSON validation")
