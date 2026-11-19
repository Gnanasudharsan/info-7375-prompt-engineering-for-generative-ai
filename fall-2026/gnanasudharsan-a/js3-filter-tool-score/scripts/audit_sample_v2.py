"""Fresh BLIND random sample of 30 rejects (seed 7378), excluding the 50 items already seen in v1."""
import csv, gzip, html, json, random, re
from pathlib import Path
from jobwatch.loop import _parse_jobs
from jobwatch.normalize import normalize
run = Path("runs/20261119T162945Z")
rows = [json.loads(l) for l in (run / "filter_v1.jsonl").read_text().splitlines()]
seen = {(s["board"], s["id"]) for s in json.loads(Path("audit/sample_v1.json").read_text())}
boards = {b["id"]: b for b in json.loads(Path("boards.json").read_text())}
postings = {}
for f in (run / "raw").glob("*.body.gz"):
    bid = next((b for b in boards if f.name.startswith(b.replace(":", "_") + ".")), None)
    if bid:
        jobs, _ = _parse_jobs(boards[bid]["ats"], gzip.decompress(f.read_bytes()))
        for j in jobs or []:
            p = normalize(boards[bid]["ats"], j); postings[(bid, str(p["id"]))] = p
text = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(html.unescape(s or "")))).strip()
pool = [r for r in rows if r["decision"] == "reject" and (r["board"], str(r["id"])) not in seen]
pick = random.Random(7378).sample(pool, 30)
Path("audit/sample_v2.json").write_text(json.dumps([{"n": n, "board": r["board"], "id": str(r["id"]),
    "filter_decision": r["decision"], "filter_score": r["score"], "rejected_by": r["rejected_by"]}
    for n, r in enumerate(pick, 1)], indent=1))
with open("audit/label_sheet_v2.md", "w") as fh:
    fh.write("# Blind label sheet v2 — 30 random rejects not seen before (filter decision hidden)\n\n")
    for n, r in enumerate(pick, 1):
        p = postings[(r["board"], str(r["id"]))]
        fh.write(f"## #{n} — {r['board']} — {p.get('title')}\n- location: {p.get('location')}\n- link: {p.get('absolute_url')}\n\n> {text(p.get('content'))[:2000]}\n\n")
with open("audit/hand_verdicts_v2.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["n", "board", "id", "title", "my_verdict", "my_reason"])
    for n, r in enumerate(pick, 1):
        w.writerow([n, r["board"], r["id"], postings[(r["board"], str(r["id"]))].get("title"), "", ""])
print(f"{len(pick)} fresh rejects drawn from a pool of {len(pool)}")
