"""Recompute the sampling table from a saved run and my hand labels. Drafted in a Claude chat 2026-10-29."""
import json, sys, glob, collections
run = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob("experiment/runs/sampling_*"))[-1]
v = json.load(open(f"{run}/summary.json"))["verdicts"]
labels = {str(l["id"]): l["label"] for l in json.load(open("experiment/labels_dev.json"))}
agree = total = unanimous = 0
print(f"run: {run}\n{'id':<12}{'label':<14}{'verdicts':<52}{'counts':<26}agree")
for pid, vs in v.items():
    c = collections.Counter(vs); a = sum(x == labels[pid] for x in vs)
    agree += a; total += len(vs); unanimous += len(c) == 1
    print(f"{pid:<12}{labels[pid]:<14}{','.join(x[0] for x in vs):<52}{str(dict(c)):<26}{a}/{len(vs)}")
print(f"\nagreement with my labels: {agree}/{total} = {agree/total:.0%}; unanimous postings: {unanimous}/{len(v)}")
