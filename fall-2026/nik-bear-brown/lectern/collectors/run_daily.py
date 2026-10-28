#!/usr/bin/env python3
"""run_daily.py — daily run: collect the big four, feed the shared monitor.

Usage:
    python3 -m collectors.run_daily [--db monitor.db] [--only google] [--text-out DIR]

Each collector returns (jobs, reported_total). Descriptions are fetched
only for job IDs not already in the database. Ends with one health line
per source:

    google  fetched=3345  reported=3345  new=12  closed=9  trusted=yes
"""
import argparse
import json
import os
import sys
import traceback
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collectors import amazon, google, microsoft, monitor

COLLECTORS = {
    "google": google,
    "amazon": amazon,
    "microsoft": microsoft,
}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "monitor.db"))
    ap.add_argument("--only", choices=list(COLLECTORS),
                    help="run one collector")
    ap.add_argument("--text-out", metavar="DIR",
                    help="keep every posting's ad text in DIR/<company>.jsonl, written as each is read "
                         "(the monitor keeps only a hash). Resumable: ids already in the file are not fetched "
                         "again, so a run that dies keeps what it read. Local data, not for committing.")
    a = ap.parse_args(argv)
    if a.text_out:
        os.makedirs(a.text_out, exist_ok=True)

    db = monitor.open_db(a.db)
    targets = [a.only] if a.only else list(COLLECTORS)
    for name in targets:
        mod = COLLECTORS[name]
        try:
            jobs, reported = mod.collect()
        except Exception as e:
            print(f"{name:10} COLLECT FAILED: {type(e).__name__}: {e}")
            traceback.print_exc()
            continue
        # descriptions only for new IDs, plus, with --text-out, any id whose text is not saved yet
        text_path = os.path.join(a.text_out, f"{name}.jsonl") if a.text_out else None
        saved = set()
        if text_path and os.path.exists(text_path):
            with open(text_path, encoding="utf-8") as f:
                saved = {json.loads(line)["job_id"] for line in f if line.strip()}
        for j in jobs:
            known = db.execute(
                "SELECT 1 FROM jobs WHERE company=? AND job_id=?",
                (name, j["job_id"])).fetchone()
            need_text = text_path is not None and j["job_id"] not in saved
            desc = None
            if not known or need_text:
                try:
                    desc = mod.fetch_description(j)
                except Exception as e:
                    print(f"  {name}: detail fetch failed for {j['job_id']}: {e}")
            if need_text and desc:
                with open(text_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"company": name, "job_id": j["job_id"], "title": j.get("title"),
                                        "locations": j.get("locations"), "url": j.get("url"),
                                        "posted_at": j.get("posted_at"), "description": desc,
                                        "read_at": datetime.now(timezone.utc).isoformat(timespec="seconds")},
                                       ensure_ascii=False) + "\n")
                saved.add(j["job_id"])
            j["description"] = desc if not known else None
        trusted, new_n, closed_n = monitor.record_run(db, name, jobs, reported)
        print(f"{name:10} fetched={len(jobs):,}  reported={reported}  "
              f"new={new_n}  closed={closed_n}  "
              f"trusted={'yes' if trusted else 'NO (incomplete)'}")
    db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
