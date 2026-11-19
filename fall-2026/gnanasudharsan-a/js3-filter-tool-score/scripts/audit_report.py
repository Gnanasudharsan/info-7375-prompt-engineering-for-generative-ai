"""Write audit/AUDIT.md from my blind hand verdicts (v1, v2), the samples and filter_v1.jsonl. All numbers computed here."""
import csv, json, re
from math import comb
from pathlib import Path

def cp(k, n, a=0.05):
    cdf = lambda p, x: sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(x + 1))
    def solve(f):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2; lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    return (0.0 if k == 0 else solve(lambda p: 1 - cdf(p, k - 1) < a / 2)), (1.0 if k == n else solve(lambda p: cdf(p, k) > a / 2))
iv = lambda k, n: "{:.1%} to {:.1%}".format(*cp(k, n))

filt = {(r["board"], str(r["id"])): r for r in map(json.loads, open("runs/20261119T162945Z/filter_v1.jsonl"))}
def load(v):
    s = {x["n"]: x for x in json.load(open(f"audit/sample_{v}.json"))}
    h = {int(r["n"]): r for r in csv.DictReader(open(f"audit/hand_verdicts_{v}.csv"))}
    return s, h
s1, h1 = load("v1"); s2, h2 = load("v2")
final = lambda r: r.get("corrected_after_unblind") or r["my_verdict"]

R1 = [n for n in s1 if "R" in s1[n]["groups"]]; R2 = list(s2)
fr_blind = sum(h1[n]["my_verdict"] == "RELEVANT" for n in R1) + sum(h2[n]["my_verdict"] == "RELEVANT" for n in R2)
fr_corr = sum(final(h1[n]) == "RELEVANT" for n in R1) + sum(final(h2[n]) == "RELEVANT" for n in R2)
ct_r = sum(final(h1[n]) == "CANNOT_TELL" for n in R1) + sum(final(h2[n]) == "CANNOT_TELL" for n in R2)
K = [n for n in s1 if "K" in s1[n]["groups"]]; C = [n for n in s1 if "C" in s1[n]["groups"]]
kv = {v: sum(final(h1[n]) == v for n in K) for v in ("RELEVANT", "NOT_RELEVANT", "CANNOT_TELL")}
cv = {v: sum(final(h1[n]) == v for n in C) for v in ("RELEVANT", "NOT_RELEVANT", "CANNOT_TELL")}
total = len(filt); rej = sum(r["decision"] == "reject" for r in filt.values()); kept = sum(r["decision"] == "keep" for r in filt.values())

level_words = re.compile(r"\b(senior|sr|staff|principal|lead|manager|junior|new grad|entry|intern|associate)\b", re.I)
ct_k = [n for n in K if final(h1[n]) == "CANNOT_TELL"]
no_level = [n for n in ct_k if "A4" not in filt[(s1[n]["board"], s1[n]["id"])]["matched"]
            and not level_words.search(filt[(s1[n]["board"], s1[n]["id"])]["title"] or "")]

def row(s, h, n):
    f = filt[(s[n]["board"], s[n]["id"])]
    c = h[n].get("corrected_after_unblind")
    mine = h[n]["my_verdict"] + (f" -> {c} (after unblinding)" if c else "")
    return f"| {s[n]['board']} | {f['title'][:55]} | {f['decision']} | {f['score']} | {','.join(f['rejected_by']) or '-'} | {mine} | {h[n]['my_reason'][:90]} |"

out = f"""# AUDIT.md — reject audit of filter v1.0 (FILTER.md 1.0, run 20261119T162945Z)
All numbers below are computed by scripts/audit_report.py from my blind hand verdicts. Nothing here is a measured rate for all postings.

## What was audited
- Corpus: {total} postings (anthropic, notion, spotify; the 404 board is absent, not zero). Filter v1.0 kept {kept}, rejected {rej}.
- My labels: blind (filter decision hidden), by audit/LABELING_RULE.md (the persona, not FILTER.md). Two samples:
  v1 = 30 random rejects (seed 7375) + {len(C)} close calls (score 4-6) + {len(K)} random kept (seed 7376); v2 = 30 more random rejects (seed 7378), excluding v1.

## 1. Random rejects (60 = v1 30 + v2 30)
- Postings I would call RELEVANT that the filter rejected: **{fr_blind}/60 blind**, **{fr_corr}/60 after my consistency correction** (v2 #27, recorded in FRICTIONAL). Could not tell: {ct_r}/60.
- Exact 95% interval for the false-reject rate **among random rejects**: blind {iv(fr_blind, 60)}; corrected {iv(fr_corr, 60)}.
- **What this sample can honestly show:** with 0 or 1 errors in 60, a false-reject rate of up to roughly {cp(fr_blind,60)[1]:.0%} among rejects (about {round(cp(fr_blind,60)[1]*rej)} of the {rej} rejects) is still consistent with what I saw.
  It does **not** show the filter misses nothing, and it says little about rare relevant postings: most random rejects are plainly off-target (sales, legal, PM), so a random sample mostly tests the easy cases.

## 2. Kept postings ({len(K)} random of {kept})
- My verdicts: RELEVANT {kv['RELEVANT']}, NOT_RELEVANT {kv['NOT_RELEVANT']}, CANNOT_TELL {kv['CANNOT_TELL']}.
- Wrong keeps (I said NOT_RELEVANT): {kv['NOT_RELEVANT']}/{len(K)}, exact 95% interval {iv(kv['NOT_RELEVANT'], len(K))} — too wide to rank the filter's precision.
- **Why so many CANNOT_TELL — tested, not assumed:** of my {len(ct_k)} CANNOT_TELL kept postings, **{len(no_level)}** state no "N+ years" (A4 did not fire) and have no level word in the title.
  The filter never asked for a level signal: FILTER.md abstention rule (c) ("level insufficient and no title level signal") was not implemented (Claude Code choice #11).

## 3. Close calls ({len(C)}, score 4-6)
- My verdicts: RELEVANT {cv['RELEVANT']}, NOT_RELEVANT {cv['NOT_RELEVANT']}, CANNOT_TELL {cv['CANNOT_TELL']}. This is where my judgment and the threshold disagree most.

## 4. False friend (a word that matched for the wrong reason)
- **A6 "security clearance"** on v1 #3, Product Manager, Public Sector. Filter matched: `{json.dumps(filt[(s1[3]['board'], s1[3]['id'])]['matched'])}`.
  The posting says some portfolios require eligibility for a US security clearance, **though most do not**: the phrase matched, but the role does not require a clearance.
  Harmless here only because A1 and A4 also fired.
- Contrast, v2 #9 (Staff+ Software Engineer, Public Sector): A6 matched for the **right** reason ("Active federal security clearance (Secret or above)").

## 5. A miss found by the audit
- **A3** did not fire on v2 #9, although the text says "This position requires verification of U.S. citizenship". The A3 phrase list ("U.S. citizenship required", "must be a U.S. citizen") is too literal.

## 6. My predictions vs. what I found (audit/PREDICTIONS.md, written before labeling)
- Predicted ~5 wrong random rejects of 30: found {sum(h1[n]['my_verdict']=='RELEVANT' for n in R1)} in v1 and {sum(h2[n]['my_verdict']=='RELEVANT' for n in R2)} in v2 (blind).
- Predicted ~2 wrong keeps of 10: found {kv['NOT_RELEVANT']}, plus {kv['CANNOT_TELL']} I could not decide.
- Predicted Notion/Spotify kept 0 was a blind spot: not supported — every Notion/Spotify posting in my random samples was a correct reject by my labels.

## Rule changes after measuring
See FILTER.md changelog (v1.1): every rule added, cut, or rejected, with the numbers that motivated it.

## Every audited posting
### v1 random rejects
| board | title | filter | score | rejected_by | me | my reason |
|---|---|---|---|---|---|---|
""" + "\n".join(row(s1, h1, n) for n in sorted(R1)) + """
### v2 random rejects
| board | title | filter | score | rejected_by | me | my reason |
|---|---|---|---|---|---|---|
""" + "\n".join(row(s2, h2, n) for n in sorted(R2)) + """
### Close calls and kept
| board | title | filter | score | rejected_by | me | my reason |
|---|---|---|---|---|---|---|
""" + "\n".join(row(s1, h1, n) for n in sorted(set(C) | set(K))) + "\n"
Path("audit/AUDIT.md").write_text(out); print(out.split("## Every audited posting")[0])
