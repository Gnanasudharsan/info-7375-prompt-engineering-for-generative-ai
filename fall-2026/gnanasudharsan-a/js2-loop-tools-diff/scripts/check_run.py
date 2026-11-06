"""Independent check of a run's report. Does NOT import jobwatch.
Usage: python scripts/check_run.py <run_dir> <prior_state.json> [recount_board recount_url]"""
import json, sys, urllib.request
from pathlib import Path

ALLOWED = ("https://boards-api.greenhouse.io/", "https://api.ashbyhq.com/", "https://api.lever.co/")


def main(run_dir, prior_path, recount_board=None, recount_url=None):
    report = json.loads((Path(run_dir) / "report.json").read_text())
    prior = json.loads(Path(prior_path).read_text())
    problems = []
    print(f"run {Path(run_dir).name}: the agent reports exit={report['exit']}")
    for board, r in report["boards"].items():
        if r["status"] != "ok":
            continue
        before, after = len(prior.get(board, [])), r["count"]
        new, removed = len(r["new"] or []), len(r["removed"] or [])
        flag = ""
        if before > 0 and after == 0:
            flag = "EMPTY-AFTER-NONEMPTY"
        elif before > 0 and removed > before / 2:
            flag = "LOST-MORE-THAN-HALF"
        elif board in prior and before == 0 and new > 0:
            flag = "ALL-NEW-AFTER-EMPTY-STATE"
        print(f"  {board}: prior {before} -> reported {after}, new {new}, removed {removed} {flag}")
        if flag:
            problems.append(f"{board}: {flag}")
    if recount_url:
        assert recount_url.startswith(ALLOWED), "recount host not on the allow-list"
        req = urllib.request.Request(recount_url, headers={
            "Accept": "application/json",
            "User-Agent": "jobwatch-js2-check/1.0 (INFO 7375 course project, independent check)"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                d = json.load(resp)
        except Exception as exc:  # a failed recount is reported, never turned into a number
            print(f"  direct recount of {recount_board}: UNAVAILABLE ({type(exc).__name__}: {exc})")
        else:
            n = len(d if isinstance(d, list) else d["jobs"])
            rep = report["boards"][recount_board]["count"]
            print(f"  direct recount of {recount_board}: {n} postings vs reported {rep}")
            if n != rep:
                problems.append(f"{recount_board}: direct recount {n} != reported {rep}")
    print("VERDICT:", "WRONG ANSWER CAUGHT -> " + "; ".join(problems) if problems else "no problem found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
