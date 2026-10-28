"""Automated keyword pre-flags for one replay run. A preliminary aid only, not a score.

Usage: python3 flags.py runs/<run_id>     -> writes runs/<run_id>/flags.json
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

PATTERNS = {
    "fall_clear": r"\bfell\b|\bfall(s|en|ing)?\b|\btumbl(e|ed|es)\b",
    "fall_ambiguous": r"\bslip(ped|s)?\b|\bstumbl(e|ed|es)\b|\btrip(ped|s)?\b|\bincident\b|\bmishap\b",
    "effects": r"\bhip\b|\bsore(ness)?\b|\bstairs\b|getting around|\bmobility\b|\bpain\b",
    "timing": r"last night|previous (night|evening)|the night before|\bevening\b",
    "place_cause": r"\bkitchen\b|\bkettle\b",
    "nothing_broken": r"nothing.{0,12}broken|not broken|no (serious |major )?injur|uninjur|unhurt|no harm",
    "daughter": r"\bdaughter\b",
}
INCIDENT_TERMS = r"fell|fall|tumbl|slip|stumbl|trip|hip|sore|stairs|getting around|mobility|kitchen|kettle"


def scan(text):
    hits = {name: sorted({m.group(0).lower() for m in re.finditer(p, text, re.I)})
            for name, p in PATTERNS.items()}
    return {name: found for name, found in hits.items() if found}


def auto_c1(hits):
    if "fall_clear" in hits:
        return "yes?"
    if "fall_ambiguous" in hits:
        return "ambiguous?"
    return "no?"


def auto_c4(text):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    questions = [s for s in sentences if s.endswith("?")]
    tied = [s for s in questions if re.search(INCIDENT_TERMS, s, re.I)]
    if tied:
        return "explicit?", tied
    if re.search(INCIDENT_TERMS, text, re.I):
        return "mention-only?", []
    return "generic/none?", []


def main():
    run_dir = Path(sys.argv[1])
    db = sqlite3.connect(run_dir / "daythread.sqlite")
    out = {"note": "Keyword pre-flags only. '?' marks a machine guess for human review.",
           "summaries": {}, "openings": {}}
    for setting, trial, text in db.execute("SELECT setting, trial, text FROM summaries ORDER BY trial, setting"):
        hits = scan(text)
        out["summaries"][f"{setting}-{trial}"] = {"auto_C1": auto_c1(hits), "hits": hits}
    for setting, trial, cond, text in db.execute(
            "SELECT setting, trial, condition, text FROM openings ORDER BY trial, setting, condition"):
        c4, tied = auto_c4(text)
        out["openings"][f"{setting}-{trial}-{cond}"] = {"auto_C4": c4, "incident_questions": tied,
                                                        "hits": scan(text)}
    (run_dir / "flags.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote {run_dir / 'flags.json'}")


if __name__ == "__main__":
    main()
