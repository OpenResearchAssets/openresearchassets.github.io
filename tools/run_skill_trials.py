#!/usr/bin/env python3
"""Runnable source-guided Skill trials, not automatic model/agent skill invocation."""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import argparse, csv, hashlib, json, subprocess, sys, time, traceback
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_UPSTREAM_COMMIT = "49f948faa9258a0c61caceaf225e179651397431"

def write_json(p, obj):
    p.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

def compute_metrics(source):
    content = source.read_bytes()
    entries = json.loads(content)["entries"]
    return {
        "source": "catalog/index.json",
        "source_sha256": hashlib.sha256(content).hexdigest(),
        "entry_count": len(entries),
        "kind_counts": dict(sorted(Counter(e["kind"] for e in entries).items())),
        "track_counts": dict(sorted(Counter(e.get("curation", {}).get("track") or "untracked" for e in entries).items())),
        "topic_counts": dict(sorted(Counter(t for e in entries for t in e["topics"]).items())),
    }

def make_notebook(helper, out):
    if not helper.is_file():
        raise FileNotFoundError("Official pinned Notebook Skill scaffold missing")
    path = out / "catalog-coverage.ipynb"
    subprocess.run([sys.executable, str(helper), "--kind", "experiment",
                    "--title", "Research catalog coverage", "--out", str(path), "--force"],
                   check=True, capture_output=True, text=True)
    notebook = json.loads(path.read_text(encoding="utf-8"))
    notebook["cells"] = notebook["cells"][:1]  # preserve upstream template and title
    def cell(kind, content):
        item = {"cell_type": kind, "metadata": {}, "source": content.strip().splitlines(keepends=True)}
        if kind == "code":
            item.update({"execution_count": None, "outputs": []})
        notebook["cells"].append(item)
    cell("markdown", """
## Objective / 科研资产分类核验

Use the actual public catalog rather than fabricated experiment data.
Compute record kinds (mutually exclusive), curation tracks (mutually exclusive)
and topics (overlapping). Compare against a separate Python implementation.
""")
    cell("code", """
from pathlib import Path
from collections import Counter
import json, hashlib
source = Path("catalog/index.json")
raw = source.read_bytes()
entries = json.loads(raw)["entries"]
assert entries and len({e["id"] for e in entries}) == len(entries)
print("Records:", len(entries), "SHA256:", hashlib.sha256(raw).hexdigest()[:16])
""")
    cell("markdown", "## Compute categories and record provenance / 计算类型与来源摘要")
    cell("code", """
kind = Counter(e["kind"] for e in entries)
track = Counter(e.get("curation", {}).get("track") or "untracked" for e in entries)
topic = Counter(t for e in entries for t in e["topics"])
metrics = {
    "source": "catalog/index.json",
    "source_sha256": hashlib.sha256(raw).hexdigest(),
    "entry_count": len(entries),
    "kind_counts": dict(sorted(kind.items())),
    "track_counts": dict(sorted(track.items())),
    "topic_counts": dict(sorted(topic.items())),
}
assert sum(kind.values()) == len(entries)
assert sum(track.values()) == len(entries)
print("Kinds:", metrics["kind_counts"])
print("Top topics:", topic.most_common(5))
""")
    cell("markdown", "## Verify a reproducible output / 保存可复核结果")
    cell("code", """
output = Path("experiments/skill-trials/_output")
output.mkdir(parents=True, exist_ok=True)
(output / "notebook-metrics.json").write_text(
    json.dumps(metrics, indent=2, sort_keys=True, ensure_ascii=False) + "\\n", encoding="utf-8")
print("Saved notebook summary", metrics["entry_count"])
""")
    write_json(path, notebook)
    import nbformat
    from nbclient import NotebookClient
    notebook = nbformat.read(path, as_version=4)
    start = time.perf_counter()
    executed = NotebookClient(notebook, timeout=120, kernel_name="python3",
                              resources={"metadata": {"path": str(ROOT)}}).execute()
    duration = round((time.perf_counter() - start) * 1000, 1)
    nbformat.write(executed, out / "catalog-coverage-executed.ipynb")
    code_cells = [c for c in executed.cells if c.cell_type == "code"]
    assert code_cells and all(c.execution_count is not None for c in code_cells)
    assert not any(x.output_type == "error" for c in code_cells for x in c.outputs)
    return {"elapsed_ms": duration, "executed_code_cells": len(code_cells),
            "upstream_scaffold_helper_actually_invoked": True}

def make_figure(metrics, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    start = time.perf_counter()
    counts = metrics["kind_counts"]
    labels = list(counts)
    values = list(counts.values())
    fig, ax = plt.subplots(figsize=(11, 5.8), layout="constrained")
    bars = ax.bar(range(len(labels)), values, color="#52748b", width=0.66)
    ax.set_title("Research asset coverage by record type", loc="left", fontsize=17, pad=20)
    ax.set_ylabel("Catalog records (count)")
    ax.set_xlabel("Asset kind · mutually exclusive")
    ax.set_ylim(bottom=0, top=max(values) * 1.24)
    ax.set_xticks(range(len(labels)), labels, rotation=16, ha="right")
    ax.bar_label(bars, padding=4, fontsize=12)
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.16)
    fig.text(0.02, 0.015, "Source: catalog/index.json | counts, not quality scores or model effectiveness",
             fontsize=9, color="#455567")
    fig.savefig(out / "asset-kind-coverage.svg")
    fig.savefig(out / "asset-kind-coverage.png", dpi=150)
    plt.close(fig)
    with (out / "asset-kind-data.csv").open("w", newline="", encoding="utf-8") as f:
        csvw = csv.writer(f)
        csvw.writerow(["kind", "record_count", "source_sha256"])
        csvw.writerows((k, counts[k], metrics["source_sha256"]) for k in labels)
    return {"elapsed_ms": round((time.perf_counter() - start) * 1000, 1),
            "output": ["asset-kind-coverage.svg", "asset-kind-coverage.png", "asset-kind-data.csv"]}

def make_robot_figure(source, out):
    """Redraw *author-reported* RoboRender task results, not robot replication."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    start = time.perf_counter()
    with source.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    cols = ("simulation_success_pct", "simulation_dr_success_pct", "roborender_success_pct")
    assert len(rows) == 8 and len({r["task_id"] for r in rows}) == 8
    assert all(r["provenance"] == "author-reported" and
               r["independent_replication"] == "no" and
               int(r["rollouts_per_method"]) == 10 for r in rows)
    samples = [[int(r[k]) for k in cols] for r in rows]
    assert all(all(0 <= x <= 100 and x % 10 == 0 for x in sample) for sample in samples)
    averages = [sum(s[i] for s in samples) / len(samples) for i in range(3)]
    # Published as rounded means 10/20/71%; arithmetic mean is 71.25%.
    assert averages == [10, 20, 71.25], f"Unexpected source table: {averages}"
    from matplotlib import ticker
    fig, ax = plt.subplots(figsize=(13, 6.8), layout="constrained")
    xs = list(range(len(rows)))
    colors = ["#91a1ad", "#5c85a0", "#d78b51"]
    names = ["Sim", "Sim + DR", "RoboRender"]
    for idx in range(3):
        pos = [x + (idx - 1) * 0.23 for x in xs]
        ax.bar(pos, [sample[idx] for sample in samples], width=0.21, color=colors[idx],
               label=names[idx], zorder=3)
    ax.set_xticks(xs, [r["task"] for r in rows], rotation=25, ha="right", fontsize=9)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
    ax.set_ylabel("Success rate per task (%) · 10 rollouts per method")
    ax.set_title("RoboRender · author-reported real-robot task results", loc="left", pad=16, fontsize=16)
    ax.grid(axis="y", alpha=.18, zorder=0)
    ax.legend(ncols=3, frameon=False, loc="upper left")
    fig.text(.01, .015,
             "Source: examples/roborender-results.csv · authors' public table; NOT independent replication. No fabricated error bars.",
             fontsize=9, color="#495765")
    svg = out / "roborender-author-reported.svg"
    fig.savefig(svg)
    fig.savefig(out / "roborender-author-reported.png", dpi=150)
    plt.close(fig)
    raw = source.read_bytes()
    summary = {
        "source": "examples/roborender-results.csv",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "source_kind": "authors_reported_not_independently_reproduced",
        "task_count": len(rows),
        "rollouts_per_task_per_method": 10,
        "arithmetic_mean_percent": dict(zip(names, averages)),
        "display_mean_percent_rounded": {"Sim": 10, "Sim + DR": 20, "RoboRender": 71},
        "artifact": "roborender-author-reported.svg"
    }
    write_json(out / "roborender-provenance-check.json", summary)
    return {"elapsed_ms": round((time.perf_counter() - start) * 1000, 1),
            "task_count": len(rows), "mean_success_percent": summary["arithmetic_mean_percent"],
            "source_sha256": summary["source_sha256"],
            "independent_robot_replication": False}


def verify_robot_figure(source, out):
    data = json.loads((out / "roborender-provenance-check.json").read_text(encoding="utf-8"))
    svg = (out / "roborender-author-reported.svg").read_text(encoding="utf-8")
    root = ElementTree.fromstring(svg)
    with source.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {
        "paper_source_sha_matches": hashlib.sha256(source.read_bytes()).hexdigest() == data["source_sha256"],
        "paper_means_match_raw_author_table": (
            len(rows) == 8 and
            all(r["provenance"] == "author-reported" and r["independent_replication"] == "no" for r in rows) and
            [sum(int(r[col]) for r in rows) / 8 for col in
             ("simulation_success_pct", "simulation_dr_success_pct", "roborender_success_pct")] == [10, 20, 71.25]),
        "paper_svg_is_vector_and_discloses_provenance": (
            not any(node.tag.rsplit("}", 1)[-1] == "image" for node in root.iter())
            and "NOT independent replication" in svg
            and "No fabricated error bars" in svg)
    }


def verify(metrics, out):
    copied = json.loads((out / "notebook-metrics.json").read_text(encoding="utf-8"))
    with (out / "asset-kind-data.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    svg = (out / "asset-kind-coverage.svg").read_text(encoding="utf-8")
    xml = ElementTree.fromstring(svg)
    def verified_rows(candidate):
        return (
            {r["kind"]: int(r["record_count"]) for r in candidate} == metrics["kind_counts"]
            and all(r["source_sha256"] == metrics["source_sha256"] for r in candidate)
        )
    # Mutate a real copy of the same CSV rows, then assert the actual validator rejects it.
    corrupted = [dict(r) for r in rows]
    corrupted[0]["record_count"] = str(int(corrupted[0]["record_count"]) + 1)
    return {
        "notebook_matches_independent_python": copied == metrics,
        "kind_counts_exhaust_all_records": sum(metrics["kind_counts"].values()) == metrics["entry_count"],
        "track_counts_exhaust_all_records": sum(metrics["track_counts"].values()) == metrics["entry_count"],
        "figure_data_matches_source": verified_rows(rows),
        "svg_has_no_embedded_raster_images": not any(el.tag.rsplit("}", 1)[-1] == "image" for el in xml.iter()),
        "svg_describes_source": all(s in svg for s in ("Research asset coverage", "catalog/index.json", "count")),
        "negative_control_detects_tampered_count": (
            verified_rows(rows) and not verified_rows(corrupted)),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--helper", type=Path, required=True,
                        help="Path to pinned upstream official new_notebook.py; no substituted helper")
    parser.add_argument("--out", type=Path, default=ROOT / "experiments/skill-trials/_output")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    result = {
        "schema_version": 1, "status": "failed",
        "source": "catalog/index.json",
        "notebook_helper_upstream_commit": NOTEBOOK_UPSTREAM_COMMIT,
        "execution_mode": "operator-written source-guided scripts; real upstream notebook scaffold",
        "native_agent_skill_invocation": False,
        "controlled_no_skill_baseline": False,
        "model_token_usage": None,
        "model_token_note": "No metered model API was used; token count is unavailable.",
        "checks": {}, "errors": []
    }
    try:
        metrics = compute_metrics(ROOT / "catalog/index.json")
        result["source_sha256"] = metrics["source_sha256"]
        result["entry_count"] = metrics["entry_count"]
        write_json(out / "source-metrics.json", metrics)
        result["notebook"] = make_notebook(args.helper, out)
        result["figure"] = make_figure(metrics, out)
        robot_source = ROOT / "examples/roborender-results.csv"
        result["paper_figure"] = make_robot_figure(robot_source, out)
        result["checks"] = {**verify(metrics, out), **verify_robot_figure(robot_source, out)}
        assert all(result["checks"].values()), "One or more objective evidence checks failed"
        result["status"] = "passed"
    except Exception as error:
        result["errors"].append({"type": type(error).__name__, "message": str(error),
                                  "traceback": traceback.format_exc(limit=6)})
    finally:
        write_json(out / "trial-results.json", result)
        print("ORA_SKILL_TRIAL_RESULT:" + json.dumps(result, ensure_ascii=False, sort_keys=True))
    if result["status"] != "passed":
        sys.exit(1)

if __name__ == "__main__":
    main()
