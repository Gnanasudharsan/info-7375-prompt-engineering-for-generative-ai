"""Claude-judge experiments on my held-out labels. Usage: score_experiments_claude.py <prompt.md> <tag> [limit]
Each call is a fresh `claude -p` process (JS1 claude_cli backend). Saves every raw result under evidence/score_claude/<tag>/."""
import csv, gzip, json, os, sys
from pathlib import Path
os.environ.setdefault("JOBWATCH_BACKEND", "claude_cli")
from jobwatch.claude_judge import make_judge
from jobwatch.persona import DEFAULT_PERSONA, load_persona
from jobwatch.loop import _parse_jobs
from jobwatch.normalize import normalize
prompt, tag = Path(sys.argv[1]), sys.argv[2]
limit = int(sys.argv[3]) if len(sys.argv) > 3 else None
run = Path("runs/20261119T162945Z"); boards = {b["id"]: b for b in json.loads(Path("boards.json").read_text())}
post = {}
for f in (run / "raw").glob("*.body.gz"):
    bid = next((b for b in boards if f.name.startswith(b.replace(":", "_") + ".")), None)
    if bid:
        jobs, _ = _parse_jobs(boards[bid]["ats"], gzip.decompress(f.read_bytes()))
        for j in jobs or []:
            p = normalize(boards[bid]["ats"], j)
            if str(p["id"]).isdigit(): p["id"] = int(p["id"])
            post[(bid, str(p["id"]))] = p
items = json.load(open("heldout/sample.json"))[:limit]
judge = make_judge(prompt); persona = load_persona(DEFAULT_PERSONA)
out = Path(f"evidence/score_claude/{tag}"); out.mkdir(parents=True, exist_ok=True)
for x in items:
    if any((out).glob(f"{x['n']:02d}_*.json")):
        continue  # already judged in this tag: resume, never re-ask
    rec = judge(post[(x["board"], x["id"])], persona)
    (out / f"{x['n']:02d}_{x['board'].replace(':','_')}_{x['id']}.json").write_text(json.dumps(rec, indent=1, default=str))
    v = (rec.get("output") or {}).get("verdict") if isinstance(rec.get("output"), dict) else None
    print(f"#{x['n']:<3} {x['board']:<22} status={rec.get('status')} verdict={v}")
