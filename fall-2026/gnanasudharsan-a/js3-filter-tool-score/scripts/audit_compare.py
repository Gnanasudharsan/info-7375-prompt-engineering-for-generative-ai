"""Unblind audit v1: my hand verdicts vs. the filter, per group, with exact (Clopper-Pearson) 95% intervals."""
import csv, json
from math import comb
from pathlib import Path

sample = {s["n"]: s for s in json.loads(Path("audit/sample_v1.json").read_text())}
mine = {int(r["n"]): r for r in csv.DictReader(open("audit/hand_verdicts_v1.csv"))}

def cp(k, n, a=0.05):
    """Exact two-sided interval for k successes in n, by bisection on the binomial CDF."""
    cdf = lambda p, x: sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(x + 1))
    def solve(f):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    low = 0.0 if k == 0 else solve(lambda p: 1 - cdf(p, k - 1) < a / 2)
    high = 1.0 if k == n else solve(lambda p: cdf(p, k) > a / 2)
    return low, high

def row(n):
    s, m = sample[n], mine[n]
    return f"#{n:<3} {s['board']:<22} filter={s['filter_decision']:<11} score={str(s['filter_score']):<5} rejected_by={','.join(s['rejected_by']) or '-':<12} me={m['my_verdict']:<13} {m['title'][:45]:<45} | {m['my_reason'][:80]}"

for g, name, wrong in [("R", "30 random rejects", "RELEVANT"), ("K", "kept sample", "NOT_RELEVANT"), ("C", "close calls (score 4-6)", None)]:
    ns = sorted(n for n, s in sample.items() if g in s["groups"])
    print(f"\n=== {g}: {name} ({len(ns)}) ===")
    for n in ns:
        print(row(n))
    if wrong:
        k = sum(mine[n]["my_verdict"] == wrong for n in ns)
        ct = sum(mine[n]["my_verdict"] == "CANNOT_TELL" for n in ns)
        lo, hi = cp(k, len(ns))
        print(f"--> filter wrong (I said {wrong}): {k}/{len(ns)}; I could not tell: {ct}/{len(ns)}; "
              f"exact 95% interval for this group's error rate: {lo:.1%} to {hi:.1%}")
