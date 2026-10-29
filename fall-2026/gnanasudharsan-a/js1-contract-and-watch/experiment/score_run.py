"""Score a saved run against my hand labels. Usage: score_run.py <run_dir> <dev|heldout>. Drafted in a Claude chat 2026-10-29."""
import json, sys
run, split = sys.argv[1], sys.argv[2]
v = json.load(open(f"{run}/summary.json"))["verdicts"]
labels = {str(l["id"]): l for l in json.load(open(f"experiment/labels_{split}.json"))}
ok = n = 0
print(f"run: {run} | split: {split}\n{'id':<12}{'my label':<14}{'claude':<16}match  title")
for pid, vs in v.items():
    for x in vs:
        m = x == labels[pid]["label"]; ok += m; n += 1
        print(f"{pid:<12}{labels[pid]['label']:<14}{x:<16}{'yes' if m else 'NO':<7}{labels[pid]['title'].strip()[:45]}")
print(f"\npass rate: {ok}/{n} = {ok/n:.0%}")
