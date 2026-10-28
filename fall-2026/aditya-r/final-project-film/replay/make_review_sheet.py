"""Build the review sheet for one replay run.

Usage: python3 make_review_sheet.py runs/<run_id>   -> writes runs/<run_id>/REVIEW-SHEET.md
Reads daythread.sqlite, flags.json (automated), claude_provisional.json (Claude's reading) and,
if present, aditya_review.json (Aditya's judgments). Without aditya_review.json, Aditya's column
is left blank. '—' means Aditya did not individually review that cell.
"""
import json
import sqlite3
import sys
from pathlib import Path

DETAILS = ["D2 timing", "D3 place/cause", "D4 effects", "D5 nothing broken", "D6 daughter"]


def quote(text):
    return "\n".join("> " + line for line in text.strip().splitlines())


def load(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def main():
    run_dir = Path(sys.argv[1])
    db = sqlite3.connect(run_dir / "daythread.sqlite")
    flags = json.loads((run_dir / "flags.json").read_text())
    prov = load(run_dir / "claude_provisional.json", {"summaries": {}, "openings": {}})
    adi = load(run_dir / "aditya_review.json", None)
    blank = "—" if adi else ""
    adi = adi or {"summaries": {}, "openings": {}}

    lines = [
        f"# Review sheet — replay run `{run_dir.name}`",
        "",
        "Synthetic fixture; Peg Hollis is fictional. Simulated dates: day 1 = 2026-11-02, day 2 = 2026-11-03.",
        "Criteria: `../../PRE-RUN.md` §4. Three separate columns per item:",
        "",
        "- **Auto**: keyword pre-flag (`flags.py`). A rough aid, often wrong on nuance.",
        "- **Claude (provisional)**: Claude's reading, written before Aditya's review. Not human review.",
        "- **Aditya**: Aditya's judgment. Only this column is human review.",
        "",
        "Scores: C1 Yes / Ambiguous / No · details Kept / Omitted / Softened / Changed · "
        "C4 Explicit / Mention only / Ambiguous-generic / None · C3 = invented or unsupported details.",
        "",
    ]
    if "provenance" in adi:
        lines += ["## Aditya's review", "", adi["provenance"], ""]
        lines += [f"- **{k}** {v}" for k, v in {**adi["aggregate"], **adi["rules"]}.items()]
        lines.append("")
    summaries = db.execute("SELECT id, setting, trial, text FROM summaries ORDER BY setting DESC, trial").fetchall()
    for sid, setting, trial, text in summaries:
        key = f"{setting}-{trial}"
        f = flags["summaries"].get(key, {})
        p = prov["summaries"].get(key, {})
        a = adi["summaries"].get(key, {})
        rows = ["C1"] + DETAILS + ["C3"] + (["Format"] if setting == "constrained" else [])
        names = {"C1": "C1 fall preserved", "C3": "C3 invented/unsupported", "Format": "Format (one sentence)"}
        lines += ["---", "", f"## {setting.capitalize()} summary, trial {trial}", "", quote(text), "",
                  "| Criterion | Auto | Claude (provisional) | Aditya |", "|---|---|---|---|"]
        for r in rows:
            auto = f.get("auto_C1", "") if r == "C1" else ""
            lines.append(f"| {names.get(r, r)} | {auto} | {p.get(r, '')} | {a.get(r, blank)} |")
        lines += ["", f"Auto keyword hits: `{json.dumps(f.get('hits', {}))}`"]
        if p.get("note"):
            lines.append(f"Claude's note: {p['note']}")
        lines.append("")
        for cond in ("A", "B"):
            row = db.execute("SELECT text FROM openings WHERE summary_id=? AND condition=?", (sid, cond)).fetchone()
            okey = f"{key}-{cond}"
            fo, po, ao = flags["openings"].get(okey, {}), prov["openings"].get(okey, {}), adi["openings"].get(okey, {})
            label = "A: summary only" if cond == "A" else "B: summary + raw transcript"
            lines += [f"### Day-two opening {label}", ""]
            if row is None:
                lines += ["*No output (call failed; see run.log).*", ""]
                continue
            lines += [quote(row[0]), "",
                      "| Criterion | Auto | Claude (provisional) | Aditya |", "|---|---|---|---|",
                      f"| C4 follow-up | {fo.get('auto_C4', '')} | {po.get('C4', '')} | {ao.get('C4', blank)} |",
                      f"| C3 invented/unsupported | | {po.get('C3', '')} | {ao.get('C3', blank)} |", ""]
            if po.get("note"):
                lines += [f"Claude's note: {po['note']}", ""]
    (run_dir / "REVIEW-SHEET.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {run_dir / 'REVIEW-SHEET.md'}")


if __name__ == "__main__":
    main()
