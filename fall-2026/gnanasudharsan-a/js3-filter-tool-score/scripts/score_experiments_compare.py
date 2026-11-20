"""Compare the Claude runs on my held-out labels: false keeps per run, and flips between runs (control = identical baseline twice)."""
import csv, glob, json
from collections import Counter
mine = {int(r["n"]): r["my_verdict"] for r in csv.DictReader(open("heldout/hand_verdicts.csv"))}
def load(tag):
    out = {}
    for f in glob.glob(f"evidence/score_claude/{tag}/*.json"):
        rec = json.load(open(f)); n = int(f.split("/")[-1][:2])
        o = rec.get("output") if isinstance(rec.get("output"), dict) else {}
        out[n] = o.get("verdict") or f"FAILED({rec.get('status')})"
    return out
runs = {t: load(t) for t in ("baseline", "baseline_repeat", "revision")}
judged = sorted(n for n in mine if all(not str(runs[t].get(n)).startswith("FAILED") for t in runs))
print(f"judged in all three runs: {len(judged)} of {len(mine)} (the rest: judgment_unavailable)")
for t, v in runs.items():
    c = Counter((v.get(n), mine[n]) for n in judged)
    print(f"{t:<16} RELEVANT on my NOT_RELEVANT (false keep) {c[('RELEVANT','NOT_RELEVANT')]:>2} | RELEVANT on my CANNOT_TELL {c[('RELEVANT','CANNOT_TELL')]:>2} | NOT_RELEVANT agreeing with me {c[('NOT_RELEVANT','NOT_RELEVANT')]:>2}")
for a, b, label in (("baseline", "baseline_repeat", "CONTROL (identical prompt, two fresh runs)"), ("baseline", "revision", "PROMPT change (baseline -> revision)")):
    flips = [(n, runs[a][n], runs[b][n], mine[n]) for n in judged if runs[a][n] != runs[b][n]]
    print(f"\n{label}: {len(flips)} of {len(judged)} verdicts differ")
    for n, x, y, m in flips:
        print(f"   #{n:<3} {x} -> {y}   (me: {m})")
