#!/usr/bin/env python3
"""Bounded, paired Skill-context A/B. This is NOT autonomous Agent Skill execution."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import time
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"experiments/skill-ab"
SYSTEM=(
 "You are an assistant performing a constrained research reasoning task. "
 "Use only the supplied evidence, not imagined sources. Reply in valid JSON, "
 'exactly {"selected":["OPTION_ID",...],"reason":"short explanation"}. '
 "Only select offered option IDs, each at most once. There may be multiple correct answers."
)
def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode("utf-8")).hexdigest()
def user_prompt(task):
    return "Task: "+task["id"]+" / "+task["title"]+"\nScenario:\n"+task["context"]+"\n"+task["question"]+"\nOptions:\n"+"\n".join(k+": "+v for k,v in task["options"].items())+"\nReturn selected IDs and a brief reason in JSON."
def make_messages(task,protos,arm):
    s=SYSTEM
    if arm=="skill":
        s+="\n\n--- SOURCE-GUIDED SKILL ---\n"+protos[task["domain"]]["text"]+"\n--- END SKILL ---"
    return [{"role":"system","content":s},{"role":"user","content":user_prompt(task)}]
def schedule(tasks,seed):
    pairs=[]
    for task in tasks:
        arms=["no_skill","skill"]
        rng=random.Random(str(seed)+task["id"])
        rng.shuffle(arms)
        pairs.extend({"task_id":task["id"],"arm":arm} for arm in arms)
    return pairs
def validate_data(data,labels):
    tasks=data["tasks"]
    assert len(tasks)==6 and len(labels)==6
    assert len({t["id"] for t in tasks})==6
    assert set(labels)==set(t["id"] for t in tasks)
    assert len({t["domain"] for t in tasks})==3
    for t in tasks:
        assert t["domain"] in data["skill_protocols"]
        assert not {"gold","correct","selected"}.intersection(t)
        assert len(t["options"])>=6 and labels[t["id"]]
        assert set(labels[t["id"]]).issubset(t["options"])
    for proto in data["skill_protocols"].values():
        assert proto["sha"] and proto["upstream"] and proto["text"]
def parse_response(content,choices):
    try:
        obj=json.loads(content)
        ids=obj["selected"]
        if not isinstance(ids,list) or not all(isinstance(v,str) for v in ids):
            return None,"selected must be a string list"
        if len(ids)!=len(set(ids)) or not set(ids).issubset(choices):
            return None,"repeated or invalid IDs"
        if not isinstance(obj.get("reason"),str):
            return None,"missing reason"
        return ids,None
    except (ValueError,KeyError,TypeError):
        return None,"invalid JSON/schema"
def score(pred,gold):
    if pred is None:
        return {"f1":0.0,"precision":0.0,"recall":0.0,"exact":False}
    a,b=set(pred),set(gold)
    p=len(a&b)/len(a) if a else 0.0
    r=len(a&b)/len(b) if b else 0.0
    return {"f1":round(2*p*r/(p+r),6) if p+r else 0.0,
            "precision":round(p,6),"recall":round(r,6),"exact":a==b}
def request(base,key,model,messages,max_tokens,timeout):
    if not base.startswith("https://"):
        raise ValueError("Model API base must use HTTPS")
    body={"model":model,"messages":messages,"temperature":0,"max_tokens":max_tokens}
    req=urllib.request.Request(base.rstrip("/")+"/chat/completions",
      data=json.dumps(body).encode("utf-8"),method="POST",
      headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
    start=time.perf_counter()
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            result=json.loads(r.read(2_000_000))
    except urllib.error.HTTPError as e:
        # Never log request headers, credentials or potentially sensitive provider replies.
        raise RuntimeError("Model provider HTTP "+str(e.code)) from None
    elapsed=round((time.perf_counter()-start)*1000,1)
    choice=result["choices"][0]
    usage=result.get("usage") or {}
    return {"content":choice["message"].get("content") or "",
            "elapsed_ms":elapsed,"actual_model":result.get("model"),
            "finish_reason":choice.get("finish_reason"),
            "input_tokens":usage.get("prompt_tokens"),
            "output_tokens":usage.get("completion_tokens")}
def stats(records,tasks):
    arms={}
    for arm in ("no_skill","skill"):
        rs=[r for r in records if r["arm"]==arm]
        arms[arm]={"count":len(rs),
          "macro_f1":round(sum(r["score"]["f1"] for r in rs)/len(rs),6) if rs else None,
          "exact_match_count":sum(r["score"]["exact"] for r in rs),
          "input_tokens":sum(r["input_tokens"] for r in rs) if rs and all(isinstance(r["input_tokens"],int) for r in rs) else None,
          "output_tokens":sum(r["output_tokens"] for r in rs) if rs and all(isinstance(r["output_tokens"],int) for r in rs) else None,
          "wall_ms":round(sum(r["elapsed_ms"] for r in rs),1)}
    paired=[]
    for t in tasks:
        pair={r["arm"]:r for r in records if r["task_id"]==t["id"]}
        if len(pair)==2:
            paired.append({"task_id":t["id"],"domain":t["domain"],
              "no_skill_f1":pair["no_skill"]["score"]["f1"],
              "skill_f1":pair["skill"]["score"]["f1"],
              "delta_f1":round(pair["skill"]["score"]["f1"]-pair["no_skill"]["score"]["f1"],6)})
    return {"arms":arms,"paired":paired,"paired_count":len(paired),
      "mean_delta_f1":round(sum(x["delta_f1"] for x in paired)/len(paired),6) if paired else None,
      "qualification":"six-item descriptive pilot; no significance or native agent tool use"}
def main(args):
    data=load(DATA/"tasks.json")
    gold=load(DATA/"gold.json")
    labels={g["id"]:g["selected"] for g in gold["gold"]}
    validate_data(data,labels)
    planned=schedule(data["tasks"],args.seed)
    assert len(planned)==12
    for i in range(0,12,2):
        assert planned[i]["task_id"]==planned[i+1]["task_id"]
        assert {planned[i]["arm"],planned[i+1]["arm"]}=={"no_skill","skill"}
    if args.dry_run:
        print("AB_PREFLIGHT:"+json.dumps({"task_count":6,"calls":12,"schedule":planned,
            "dataset_sha256":digest(data),"gold_sha256":digest(gold)},ensure_ascii=False))
        return 0
    if not os.environ.get("AB_API_KEY"):
        print("AB_NOT_RUN: AB_API_KEY is not configured; no inference performed.")
        return 2
    if args.max_calls<12:
        raise ValueError("Required 12 calls exceed explicit budget")
    items={t["id"]:t for t in data["tasks"]}
    report={"status":"incomplete","model_requested":args.model,"provider_base":args.api_base,
      "dataset_sha256":digest(data),"gold_sha256":digest(gold),"seed":args.seed,
      "method":"six-paired-single-turn-skill-context-ab",
      "native_agent_skill_invocation":False,"max_tokens":args.max_tokens,"temperature":0,
      "records":[],"errors":[]}
    for index,job in enumerate(planned):
        task=items[job["task_id"]]
        messages=make_messages(task,data["skill_protocols"],job["arm"])
        try:
            result=request(args.api_base,os.environ["AB_API_KEY"],args.model,
                           messages,args.max_tokens,args.timeout)
            selected,error=parse_response(result["content"],task["options"])
            record={"task_id":task["id"],"domain":task["domain"],"arm":job["arm"],
              "presentation_index":index,"prompt_sha256":digest(messages),
              "selected":selected,"parse_error":error,"reason_raw":result["content"],
              "score":score(selected,labels[task["id"]]),
              "elapsed_ms":result["elapsed_ms"],"input_tokens":result["input_tokens"],
              "output_tokens":result["output_tokens"],"actual_model":result["actual_model"],
              "finish_reason":result["finish_reason"]}
            report["records"].append(record)
            if result["actual_model"]:
                existing=report.setdefault("model_reported",result["actual_model"])
                if existing!=result["actual_model"]:
                    raise RuntimeError("provider changed the model between arms")
        except Exception as exc:
            report["errors"].append({"index":index,"task_id":task["id"],
                "arm":job["arm"],"type":type(exc).__name__,"reason":str(exc)[:200]})
            break
    report["summary"]=stats(report["records"],data["tasks"])
    report["status"]="completed" if len(report["records"])==12 and not report["errors"] else "incomplete"
    out=Path(args.out)
    out.mkdir(parents=True,exist_ok=True)
    (out/"ab-results.json").write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("AB_RESULT:"+json.dumps({"status":report["status"],"paired":report["summary"]["paired_count"],
       "delta_f1":report["summary"]["mean_delta_f1"],"errors":report["errors"]},ensure_ascii=False))
    return 0 if report["status"]=="completed" else 1
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--dry-run",action="store_true")
    parser.add_argument("--model",default="gpt-4.1-mini")
    parser.add_argument("--api-base",default="https://api.openai.com/v1")
    parser.add_argument("--max-tokens",type=int,default=550)
    parser.add_argument("--max-calls",type=int,default=12)
    parser.add_argument("--timeout",type=int,default=75)
    parser.add_argument("--seed",type=int,default=20261026)
    parser.add_argument("--out",default=str(DATA/"_output"))
    sys.exit(main(parser.parse_args()))
