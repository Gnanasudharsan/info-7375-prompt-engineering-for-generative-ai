"""Draw the reject-audit sample from a filter run and write a BLIND label sheet.
Groups: R = 30 random rejects (seed 7375); C = every close call (score 4-6); K = up to 10 random kept (seed 7376).
The sheet shuffles all items (seed 7377) and hides the filter decision and score."""
import csv, gzip, html, json, random, re, sys
from pathlib import Path
from jobwatch.loop import _parse_jobs
from jobwatch.normalize import normalize

run = Path(sys.argv[1])
rows = [json.loads(l) for l in (run / "filter_v1.jsonl").read_text().splitlines()]
boards = {b["id"]: b for b in json.loads(Path("boards.json").read_text())}
postings = {}
for f in sorted((run / "raw").glob("*.body.gz")):
    board_id = next((b for b in boards if f.name.startswith(b.replace(":", "_") + ".")), None)
    if not board_id:
        continue
    jobs, _ = _parse_jobs(boards[board_id]["ats"], gzip.decompress(f.read_bytes()))
    for j in jobs or []:
        p = normalize(boards[board_id]["ats"], j)
        postings[(board_id, str(p["id"]))] = p

def text(s):
    s = html.unescape(html.unescape(s or ""))
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

rejects = [r for r in rows if r["decision"] == "reject"]
kept = [r for r in rows if r["decision"] == "keep"]
groups = {}
for r in random.Random(7375).sample(rejects, 30):
    groups.setdefault((r["board"], str(r["id"])), []).append("R")
for r in rows:
    if r["score"] is not None and 4 <= r["score"] <= 6:
        groups.setdefault((r["board"], str(r["id"])), []).append("C")
for r in random.Random(7376).sample(kept, min(10, len(kept))):
    groups.setdefault((r["board"], str(r["id"])), []).append("K")

items = list(groups.items())
random.Random(7377).shuffle(items)
by_key = {(r["board"], str(r["id"])): r for r in rows}
out = Path("audit"); out.mkdir(exist_ok=True)
sample = [{"n": n, "board": k[0], "id": k[1], "groups": g,
           "filter_decision": by_key[k]["decision"], "filter_score": by_key[k]["score"],
           "rejected_by": by_key[k]["rejected_by"]} for n, (k, g) in enumerate(items, 1)]
(out / "sample_v1.json").write_text(json.dumps(sample, indent=1))
with open(out / "label_sheet_v1.md", "w") as fh:
    fh.write(f"# Blind label sheet — {len(items)} postings from run {run.name}\n"
             "Filter decisions are hidden. Label in audit/hand_verdicts_v1.csv.\n\n")
    for n, (k, _) in enumerate(items, 1):
        p = postings.get(k, {})
        fh.write(f"## #{n} — {k[0]} — {p.get('title')}\n- location: {p.get('location')}\n"
                 f"- link: {p.get('absolute_url')}\n\n> {text(p.get('content'))[:2000]}\n\n")
with open(out / "hand_verdicts_v1.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["n", "board", "id", "title", "my_verdict", "my_reason"])
    for n, (k, _) in enumerate(items, 1):
        w.writerow([n, k[0], k[1], postings.get(k, {}).get("title"), "", ""])
print(f"{len(items)} items: R={sum('R' in g for _, g in items)} C={sum('C' in g for _, g in items)} K={sum('K' in g for _, g in items)}")
