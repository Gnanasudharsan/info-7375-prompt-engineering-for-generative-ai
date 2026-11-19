"""Build the v1.1 shortlist: 5 claims per kept posting, each with a proposed label and the quoted span (FILTER.md 'Shortlist claim rules')."""
import csv, gzip, html, json, re
from pathlib import Path
from jobwatch.loop import _parse_jobs
from jobwatch.normalize import normalize

run = Path("runs/20261119T162945Z")
kept = [r for r in map(json.loads, open(run / "filter_v1_C1_C4.jsonl")) if r["decision"] == "keep"]
boards = {b["id"]: b for b in json.loads(Path("boards.json").read_text())}
post = {}
for f in (run / "raw").glob("*.body.gz"):
    bid = next((b for b in boards if f.name.startswith(b.replace(":", "_") + ".")), None)
    if bid:
        jobs, _ = _parse_jobs(boards[bid]["ats"], gzip.decompress(f.read_bytes()))
        for j in jobs or []:
            p = normalize(boards[bid]["ats"], j); post[(bid, str(p["id"]))] = p
clean = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(html.unescape(s or "")))).strip()
sents = lambda t: [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]
first = lambda ss, rx: next((s for s in ss if re.search(rx, s, re.I)), None)
BUILD = r"\b(build|building|design|designing|implement|implementing|train|training|develop|developing|deploy|deploying)\b"
ML = r"\b(model|models|ml|machine learning|llms?|language models?|rl|reinforcement learning|training|inference|evaluations?)\b"
LEVEL = r"\b(new grads?|new graduates?|entry-level|early career|junior)\b"
SENIOR = r"\b(senior|sr|staff|principal|lead|manager|director|head|vp|distinguished)\b"
YEARS = r"\b([3-9]|\d{2,})\s*\+\s*years?\b"
DEFER = r"years of experience required will correlate with the internal job level"
SPONSOR = r"\b(we (do )?sponsor visas|visa sponsorship (is )?available|will sponsor)\b"
SKILLS = ["python", "pytorch", "sql", "transformers", "sentence-transformers", "fastapi", "mlflow", "postgresql", "aws"]
US_STATE = r",\s*(AL|AK|AZ|AR|CA|CO|CT|DE|DC|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b|united states"

rows = []
for r in kept:
    k = (r["board"], str(r["id"])); p = post[k]; text = clean(p.get("content")); ss = sents(text)
    title = p.get("title") or ""; loc = (p.get("location") or {}).get("name") if isinstance(p.get("location"), dict) else p.get("location")
    def add(claim, label, span):
        rows.append({"board": k[0], "id": k[1], "title": title.strip(), "claim": claim, "proposed": label, "span": (span or "")[:400]})
    s = next((x for x in ss if re.search(BUILD, x, re.I) and re.search(ML, x, re.I)), None)
    add("role: hands-on ML/AI engineering", "SUPPORTED" if s else "INSUFFICIENT", s)
    if re.search(SENIOR, title, re.I): add("level: realistic for a new grad", "CONTRADICTED", "title: " + title)
    elif first(ss, YEARS): add("level: realistic for a new grad", "CONTRADICTED", first(ss, YEARS))
    elif first(ss, LEVEL): add("level: realistic for a new grad", "SUPPORTED", first(ss, LEVEL))
    else: add("level: realistic for a new grad", "INSUFFICIENT", first(ss, DEFER) or "no level statement")
    parts = [x.strip() for x in re.split(r"[|;]", loc or "") if x.strip()]
    if not parts: add("location: US-based or remote-US", "INSUFFICIENT", "no location")
    elif any(re.search(US_STATE, x, re.I) for x in parts): add("location: US-based or remote-US", "SUPPORTED", "location: " + loc)
    elif all(not re.search(r"\bremote\b", x, re.I) for x in parts): add("location: US-based or remote-US", "CONTRADICTED", "location: " + loc)
    else: add("location: US-based or remote-US", "INSUFFICIENT", "location: " + loc)
    if r["matched"].get("A3"): add("sponsorship: does not rule out sponsorship", "CONTRADICTED", r["matched"]["A3"])
    else:
        s = first(ss, SPONSOR); add("sponsorship: does not rule out sponsorship", "SUPPORTED" if s else "INSUFFICIENT", s or "text is silent on sponsorship")
    found = [w for w in SKILLS if re.search(rf"(?<![a-z0-9-]){re.escape(w)}(?![a-z0-9-])", text, re.I)]
    add("skills: asks for skills she has shipped", "SUPPORTED" if len(found) >= 2 else "INSUFFICIENT",
        f"found: {', '.join(found) or 'none'} | " + (first(ss, rf"\b{found[0]}\b") or "") if found else "found: none")
out = Path("shortlist"); out.mkdir(exist_ok=True)
(out / "shortlist_v1_1.json").write_text(json.dumps(rows, indent=1))
with open(out / "claim_labels.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]) + ["my_label", "my_note"]); w.writeheader()
    for x in rows: w.writerow({**x, "my_label": "", "my_note": ""})
from collections import Counter
print(len(kept), "postings,", len(rows), "claims; proposed:", Counter((x["claim"].split(":")[0], x["proposed"]) for x in rows))
