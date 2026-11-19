"""Unblind audit v2: my blind hand verdicts on 30 fresh random rejects vs. the filter."""
import csv, json
from math import comb
from pathlib import Path
sample = {s["n"]: s for s in json.loads(Path("audit/sample_v2.json").read_text())}
mine = {int(r["n"]): r for r in csv.DictReader(open("audit/hand_verdicts_v2.csv"))}
def cp(k, n, a=0.05):
    cdf = lambda p, x: sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(x + 1))
    def solve(f):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2; lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    return (0.0 if k == 0 else solve(lambda p: 1 - cdf(p, k - 1) < a / 2)), (1.0 if k == n else solve(lambda p: cdf(p, k) > a / 2))
for n in sorted(sample):
    s, m = sample[n], mine[n]
    flag = "  <== FALSE REJECT" if m["my_verdict"] == "RELEVANT" else ("  <== I could not tell" if m["my_verdict"] == "CANNOT_TELL" else "")
    print(f"#{n:<3} {s['board']:<22} score={str(s['filter_score']):<5} rejected_by={','.join(s['rejected_by']) or '-':<12} me={m['my_verdict']:<13} {m['title'][:50]}{flag}\n      my reason: {m['my_reason']}")
k = sum(m["my_verdict"] == "RELEVANT" for m in mine.values()); n = len(mine)
lo, hi = cp(k, n)
print(f"\nFalse rejects: {k}/{n}; could not tell: {sum(m['my_verdict']=='CANNOT_TELL' for m in mine.values())}/{n}; exact 95% interval for the false-reject rate among random rejects: {lo:.1%} to {hi:.1%}")
