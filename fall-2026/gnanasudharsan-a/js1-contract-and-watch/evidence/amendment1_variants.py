# Offline analysis script used to produce evidence/amendment1_variant_counts_2026-10-28.txt; written by Claude Code on 2026-10-28; reads data/raw/anthropic_20261028T192103Z.json and persona/ananya-rao.resume.json, imports jobwatch.rule and jobwatch.persona, makes no network calls and writes no files.
import json, sys
from pathlib import Path
sys.path.insert(0, ".")
from jobwatch import rule
from jobwatch.persona import load_persona

SRC = "data/raw/anthropic_20261028T192103Z.json"
print("Claude Code output, 2026-10-28, offline analysis on data/raw/anthropic_20261028T192103Z.json, no code changed.")
print()
print("Method: jobwatch.rule.judge_posting (committed code at b1f1e45) run on every posting;")
print("a posting passes a variant if every non-skills condition passes and distinct shipped-skill")
print("count >= the variant threshold. Variants C/D add 'research engineer' to an in-memory copy of")
print("persona target_roles only; no file on disk was modified.")
print()
persona = load_persona(Path("persona/ananya-rao.resume.json"))
jobs = json.load(open(SRC))["jobs"]
print("postings:", len(jobs))
print("shipped skills:", [s for s, _ in rule.shipped_skills(persona)])
variants = [("current rule", 3, False, "threshold 3, current target_roles"),
            ("A", 1, False, "threshold 1, current target_roles"),
            ("B", 2, False, "threshold 2, current target_roles"),
            ("C", 1, True, "threshold 1, + 'research engineer'"),
            ("D", 2, True, "threshold 2, + 'research engineer'")]
results = []
for name, thr, extra, desc in variants:
    p = dict(persona)
    if extra:
        p["target_roles"] = list(persona["target_roles"]) + ["research engineer"]
    hits = []
    for j in jobs:
        r = rule.judge_posting(j, p)
        jj = r["justification"]
        failed = [k for k in jj["failed_conditions"] if k != "skills"]
        if not failed and jj["skills"]["distinct_count"] >= thr:
            hits.append((j["id"], j["title"], jj["skills"]["distinct_count"],
                         [m["skill"] for m in jj["skills"]["matched"]],
                         (j.get("location") or {}).get("name")))
    results.append((name, desc, hits))
print()
print("== Count table")
print(f"{'variant':<14}| {'definition':<38}| passing")
print("-" * 64)
for name, desc, hits in results:
    print(f"{name:<14}| {desc:<38}| {len(hits)}")
for name, desc, hits in results:
    print(f"\n== {name} ({desc}): {len(hits)}")
    if not hits:
        print("  (no passing postings)")
    for h in hits:
        print(f"  {h[0]} | {h[1]} | skills={h[2]}: {', '.join(h[3])} | {h[4]}")
