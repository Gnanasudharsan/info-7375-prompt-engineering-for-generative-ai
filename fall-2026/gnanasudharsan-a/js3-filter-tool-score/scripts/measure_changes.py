"""Measure each v1.1 change alone against v1.0: corpus counts, every flipped posting, and agreement with my hand labels.
Reads only runs/<id>/filter_v1*.jsonl and audit/hand_verdicts_v1.csv / _v2.csv + samples. Also runs the C5 check."""
import csv, json, re
from collections import Counter
from pathlib import Path
run = Path("runs/20261119T162945Z")
load = lambda f: {(r["board"], str(r["id"])): r for r in map(json.loads, open(run / f))}
base = load("filter_v1.jsonl")
labels = {}
for v in ("v1", "v2"):
    s = {x["n"]: x for x in json.load(open(f"audit/sample_{v}.json"))}
    for r in csv.DictReader(open(f"audit/hand_verdicts_{v}.csv")):
        x = s[int(r["n"])]
        labels[(x["board"], x["id"])] = r.get("corrected_after_unblind") or r["my_verdict"]

def agree(res):
    c = Counter()
    for k, mine in labels.items():
        c[(res[k]["decision"], mine)] += 1
    return c

def show(name, res):
    d = Counter(r["decision"] for r in res.values())
    a = agree(res)
    print(f"\n=== {name}: keep {d['keep']} | reject {d['reject']} | cannot_tell {d['cannot_tell']}  "
          f"(A3 fired {sum('A3' in r['rejected_by'] for r in res.values())}, A6 fired {sum('A6' in r['rejected_by'] for r in res.values())})")
    print(f"    on my {len(labels)} labels: kept&RELEVANT {a[('keep','RELEVANT')]} | kept&NOT_RELEVANT {a[('keep','NOT_RELEVANT')]} | kept&CANNOT_TELL {a[('keep','CANNOT_TELL')]} | "
          f"rejected&RELEVANT {a[('reject','RELEVANT')]} | cannot_tell&CANNOT_TELL {a[('cannot_tell','CANNOT_TELL')]} | cannot_tell&RELEVANT {a[('cannot_tell','RELEVANT')]} | cannot_tell&NOT_RELEVANT {a[('cannot_tell','NOT_RELEVANT')]}")

show("v1.0 baseline", base)
for c in ("C1", "C2", "C3", "C4"):
    res = load(f"filter_v1_{c}.jsonl")
    show(c + " alone", res)
    flips = [(k, base[k]["decision"], res[k]["decision"]) for k in base if base[k]["decision"] != res[k]["decision"]]
    print(f"    {len(flips)} postings changed decision:")
    for k, b, n in flips:
        mine = labels.get(k, "-")
        print(f"      {b:>11} -> {n:<11} me={mine:<13} {k[0]:<22} {base[k]['title'][:60]}")
    if c in ("C1", "C2"):
        rule = "A3" if c == "C1" else "A6"
        gained = [k for k in base if rule in res[k]["rejected_by"] and rule not in base[k]["rejected_by"]]
        lost = [k for k in base if rule in base[k]["rejected_by"] and rule not in res[k]["rejected_by"]]
        print(f"    {rule} now fires on {len(gained)} more and {len(lost)} fewer postings (even where another rule already rejects):")
        for k in gained + lost:
            print(f"      {'+' if k in gained else '-'}{rule}  me={labels.get(k,'-'):<13} {base[k]['title'][:60]}  | was matched: {base[k]['matched'].get(rule)}  now: {res[k]['matched'].get(rule)}")

nonus = re.compile(r"\b(london|dublin|tokyo|singapore|paris|berlin|munich|zurich|amsterdam|stockholm|toronto|vancouver|sydney|seoul|bangalore|bengaluru|india|japan|korea|uk|united kingdom|ireland|germany|france|canada|australia|emea|apac|europe|latam|brazil|mexico)\b", re.I)
us = re.compile(r"\b(united states|usa|us|u\.s\.)\b|,\s*[A-Z]{2}\b", re.I)
c5 = [k for k, r in base.items() if "A2" not in r["rejected_by"] and r["location"] and re.search(r"\bremote\b", r["location"], re.I)
      and nonus.search(r["location"]) and not us.search(r["location"])]
print(f"\n=== C5 check: {len(c5)} postings pass A2 through 'remote' while naming a non-US place and no US place")
for k in c5:
    print(f"      {base[k]['decision']:<11} me={labels.get(k,'-'):<13} {base[k]['title'][:50]:<50} | {base[k]['location']}")
