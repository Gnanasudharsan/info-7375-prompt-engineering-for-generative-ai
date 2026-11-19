"""Held-out set for the score experiments: postings NEVER labeled before (not in audit v1/v2), drawn before labeling.
Strata: all unlabeled v1.1 keeps; 12 near-misses (seed 9101); 13 random rejects (seed 9102). Sheet is blind and shuffled (seed 9103)."""
import csv, gzip, html, json, random, re
from pathlib import Path
from jobwatch.loop import _parse_jobs
from jobwatch.normalize import normalize
run = Path("runs/20261119T162945Z")
v11 = [json.loads(l) for l in open(run / "filter_v1_C1_C4.jsonl")]
seen = set()
for v in ("v1", "v2"):
    seen |= {(x["board"], x["id"]) for x in json.load(open(f"audit/sample_{v}.json"))}
key = lambda r: (r["board"], str(r["id"]))
fresh = [r for r in v11 if key(r) not in seen]
keeps = [r for r in fresh if r["decision"] == "keep"]
near = [r for r in fresh if r["decision"] == "reject" and (r["components"]["B1"] > 0 or (r["score"] is not None and r["score"] >= 3))]
rest = [r for r in fresh if r["decision"] == "reject" and r not in near]
pick = [("keep", r) for r in keeps] + [("near", r) for r in random.Random(9101).sample(near, min(12, len(near)))] + \
       [("random", r) for r in random.Random(9102).sample(rest, 13)]
random.Random(9103).shuffle(pick)
boards = {b["id"]: b for b in json.loads(Path("boards.json").read_text())}
post = {}
for f in (run / "raw").glob("*.body.gz"):
    bid = next((b for b in boards if f.name.startswith(b.replace(":", "_") + ".")), None)
    if bid:
        jobs, _ = _parse_jobs(boards[bid]["ats"], gzip.decompress(f.read_bytes()))
        for j in jobs or []:
            p = normalize(boards[bid]["ats"], j); post[(bid, str(p["id"]))] = p
text = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(html.unescape(s or "")))).strip()
out = Path("heldout"); out.mkdir(exist_ok=True)
(out / "sample.json").write_text(json.dumps([{"n": n, "stratum": s, "board": r["board"], "id": str(r["id"])} for n, (s, r) in enumerate(pick, 1)], indent=1))
with open(out / "label_sheet.md", "w") as fh:
    fh.write(f"# Held-out blind label sheet — {len(pick)} postings never labeled before (filter decision and stratum hidden)\n\n")
    for n, (_, r) in enumerate(pick, 1):
        p = post[key(r)]
        fh.write(f"## #{n} — {r['board']} — {p.get('title')}\n- location: {p.get('location')}\n- link: {p.get('absolute_url')}\n\n> {text(p.get('content'))[:2000]}\n\n")
with open(out / "hand_verdicts.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["n", "board", "id", "title", "my_verdict", "my_reason"])
    for n, (_, r) in enumerate(pick, 1):
        w.writerow([n, r["board"], r["id"], post[key(r)].get("title"), "", ""])
print(f"{len(pick)} held-out postings: keep {len(keeps)}, near {min(12, len(near))} (of {len(near)}), random 13; none previously labeled")
