"""Exit 1 (and block the commit) unless every row has a valid verdict and a reason."""
import csv, sys
from collections import Counter
rows = list(csv.DictReader(open(__import__("sys").argv[1] if len(__import__("sys").argv) > 1 else "audit/hand_verdicts_v2.csv")))
bad = [r["n"] for r in rows if r["my_verdict"] not in ("RELEVANT", "NOT_RELEVANT", "CANNOT_TELL") or not r["my_reason"].strip()]
print(len(rows), Counter(r["my_verdict"] for r in rows), "unlabeled:", bad)
sys.exit(1 if bad else 0)
