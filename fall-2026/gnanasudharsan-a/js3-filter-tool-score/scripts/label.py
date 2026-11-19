"""Blind, resumable labeling: shows each posting from audit/label_sheet_v2.md and records MY verdict.
r = RELEVANT, n = NOT_RELEVANT, c = CANNOT_TELL, s = skip for now, q = save and quit."""
import csv, re
from pathlib import Path
sheet = Path("audit/label_sheet_v2.md").read_text()
blocks = {int(m.group(1)): m.group(0) for m in re.finditer(r"## #(\d+) .*?(?=\n## #|\Z)", sheet, re.S)}
path = Path("audit/hand_verdicts_v2.csv")
rows = list(csv.DictReader(path.open()))
codes = {"r": "RELEVANT", "n": "NOT_RELEVANT", "c": "CANNOT_TELL"}
def save():
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
todo = [r for r in rows if not r["my_verdict"]]
print(f"{len(todo)} left to label")
for row in todo:
    print("\n" + "=" * 100 + "\n" + blocks[int(row["n"])][:3000])
    while True:
        a = input("\n[r]elevant / [n]ot relevant / [c]annot tell / [s]kip / [q]uit > ").strip().lower()
        if a in ("q", "s") or a in codes:
            break
    if a == "q":
        break
    if a == "s":
        continue
    row["my_verdict"] = codes[a]
    row["my_reason"] = input("reason (your words) > ").strip()
    save()
save()
print(f"saved; {sum(1 for r in rows if not r['my_verdict'])} left")
