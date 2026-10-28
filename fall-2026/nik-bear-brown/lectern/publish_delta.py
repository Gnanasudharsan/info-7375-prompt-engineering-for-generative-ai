#!/usr/bin/env python3
"""publish_delta.py — after a collection run, publish only what changed since the last published run.

    python3 publish_delta.py                       # dry run on the newest run: print the delta, write nothing
    python3 publish_delta.py --run runs/2026-10-18 # a specific run folder
    python3 publish_delta.py --write               # write delta-<date>.{md,json,csv}; the state does not move yet
    python3 publish_delta.py --commit              # --write, update published-state.json, commit ONLY those files (no push)
    python3 publish_delta.py --push                # --commit, then push. Only on Professor Bear's word.
    python3 publish_delta.py --post                # also post the new listings to the public Discord channel
    python3 publish_delta.py --post-only           # post the new listings of the latest run's delta, nothing else

Why: a run reads thousands of postings and keeps a few dozen. The full files (all-jobs, jobs-of-interest,
raw/) stay on this machine; what goes to GitHub is the small difference from the last published state:
  new      kept today, not in the published state
  changed  in both, but title, place, department, link, matched words or ad text differ
  gone     in the published state, not kept today — said WHY (off the board, now rejected by the filter,
           or the source was unavailable today so nothing can be said)

Design: the published state is one small file (published-state.json): per candidate, the fields above and
a hash of the ad text, never the ad text. Candidates are keys `<provider>:<source_id>`. Everything is
review material, "candidates for human review, not classifications". Stdlib only.

Nothing is committed unless --commit or --push is given. Only the files this script writes are added;
the full snapshots are refused by name even if asked for. Each push also needs a row in the folder's
FRICTIONAL.md "GitHub pushes" table; the script prints the row and does not edit the log.
"""
import argparse, csv, datetime as dt, hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_NAME = "published-state.json"
FIELDS = ("title", "url", "location_text", "department")
NEVER_COMMIT = re.compile(r"(^|/)(all-jobs-|jobs-of-interest-|quality-report-)|(^|/)raw(/|$)|monitor\.db")


def sha(s):
    return hashlib.sha256((s or "").encode("utf-8")).hexdigest()[:16]


def key_of(r):
    return f"{r['source']}:{r['source_id']}"


def norm_matched(m):
    """Drop empty entries so a rule added to the filter (a new key that is None on old records) is not
    reported as a change to every posting. A real change to what matched still shows."""
    if not isinstance(m, dict):
        return m
    return {k: v for k, v in m.items() if v not in (None, [], {}, False)}


def slim(r):
    out = {k: r.get(k) for k in ("company", "source", "source_id", *FIELDS, "date_posted")}
    out["matched"] = norm_matched(r.get("matched"))
    out["text_sha"] = sha(r.get("text")) if r.get("text") is not None else None
    return out


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def find(run_dir, prefix):
    names = sorted(n for n in os.listdir(run_dir) if n.startswith(prefix) and n.endswith(".json"))
    return os.path.join(run_dir, names[-1]) if names else None


def load_run(run_dir):
    kept_path, all_path = find(run_dir, "jobs-of-interest-"), find(run_dir, "all-jobs-")
    if not kept_path:
        raise SystemExit(f"no jobs-of-interest-*.json in {run_dir}")
    kept = load_json(kept_path)
    allj = load_json(all_path) if all_path else {"records": [], "sources": []}
    m = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(kept_path))
    return {
        "date": m.group(1) if m else os.path.basename(run_dir),
        "kept": {key_of(r): slim(r) for r in kept["records"]},
        "all": {key_of(r): r for r in allj["records"]},
        "sources": {s["company"]: s for s in (allj.get("sources") or kept.get("sources") or [])},
        "files": {os.path.basename(p): file_sha(p) for p in (kept_path, all_path) if p},
        "kw_version": allj.get("keywords_version") or kept.get("keywords_version"),
    }


def file_sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fingerprint(s):
    return sha(json.dumps({k: s.get(k) for k in (*FIELDS, "matched", "text_sha")}, sort_keys=True, default=str))


def baseline_from_runs(runs_dir, before):
    """No state file yet: treat every earlier run's kept set as already published."""
    cands, used = {}, []
    for name in sorted(os.listdir(runs_dir)):
        p = os.path.join(runs_dir, name)
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", name) and name < before and os.path.isdir(p) and find(p, "jobs-of-interest-"):
            r = load_run(p)
            for k, v in r["kept"].items():
                cands[k] = {**v, "fp": fingerprint(v), "published": name}
            used.append(f"{name} (filter {r['kw_version']})")
    return cands, used


def diff(state_c, run):
    new, changed, gone = [], [], []
    for k, s in run["kept"].items():
        if k not in state_c:
            new.append(s)
        else:
            old = state_c[k]
            if fingerprint(s) != old.get("fp"):
                what = []
                for f in (*FIELDS, "matched", "text_sha"):
                    if s.get(f) != old.get(f):
                        what.append({"field": "ad text" if f == "text_sha" else f,
                                     "before": None if f == "text_sha" else old.get(f),
                                     "after": None if f == "text_sha" else s.get(f)})
                changed.append({**s, "changes": what})
    for k, old in state_c.items():
        if k in run["kept"]:
            continue
        src = run["sources"].get(old["company"])
        if src is None:
            why = "company not watched in this run"
        elif src.get("status") != "ok":
            why = f"unknown: source {src.get('status')} today ({src.get('reason', 'no reason given')})"
        elif k in run["all"]:
            why = "still on the board, no longer kept by the filter: " + str(run["all"][k].get("reject_reason"))
        else:
            why = "no longer on the board"
        gone.append({**old, "why": why})
    return new, changed, gone


def write_outputs(run_dir, run, base_desc, new, changed, gone, unavailable, first_time, filter_note=""):
    d = run["date"]
    meta = {"tool": "publish_delta", "run_date": d, "baseline": base_desc, "generated_at":
            dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "counts": {"new": len(new), "changed": len(changed), "gone": len(gone), "kept_today": len(run["kept"])},
            "source_files_sha256": run["files"], "unavailable_sources": unavailable, "first_time_companies": first_time, "filter_note": filter_note,
            "note": "Candidates for human review, not classifications."}
    paths = {}
    paths["json"] = os.path.join(run_dir, f"delta-{d}.json")
    with open(paths["json"], "w", encoding="utf-8") as f:
        json.dump({**meta, "new": new, "changed": changed, "gone": gone}, f, indent=2, ensure_ascii=False)
        f.write("\n")
    paths["csv"] = os.path.join(run_dir, f"delta-{d}.csv")
    with open(paths["csv"], "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["change", "company", "title", "location", "department", "url", "matched", "detail"])
        for kind, rows in (("new", new), ("changed", changed), ("gone", gone)):
            for r in rows:
                detail = ("; ".join(c["field"] for c in r["changes"]) if kind == "changed"
                          else r.get("why", "") if kind == "gone" else "")
                w.writerow([kind, r.get("company"), r.get("title"), r.get("location_text"), r.get("department"),
                            r.get("url"), json.dumps(r.get("matched"), ensure_ascii=False), detail])
    paths["md"] = os.path.join(run_dir, f"delta-{d}.md")
    with open(paths["md"], "w", encoding="utf-8") as f:
        f.write(render_md(meta, run, new, changed, gone))
    return paths


def matched_text(m):
    """Matched words as `group: word, word`, then why it was kept. Lectern's own record, shown unedited."""
    if not isinstance(m, dict):
        return str(m or "")
    parts = []
    for g, v in m.items():
        if isinstance(v, dict):                      # e.g. connector: {title: [...], institution: [...]}
            v = [w for x in v.values() if isinstance(x, list) for w in x]
        if isinstance(v, list) and v:
            parts.append(f"{g}: {', '.join(v)}")
    if m.get("kept_because"):
        parts.append(f"({m['kept_because']})")
    return "; ".join(parts)


def render_md(meta, run, new, changed, gone):
    c, d = meta["counts"], meta["run_date"]
    by_co = {}
    for r in new:
        by_co.setdefault(r["company"], []).append(r)
    L = [f"# Delta {d}: what changed since the last published run\n",
         "## Executive summary\n",
         f"**What this is.** The difference between the postings Lectern kept on {d} and the postings already published ({meta['baseline']}). Only the difference is published; the full run stays on the machine that made it.\n",
         f"**What changed.** **{c['new']} new**, **{c['changed']} changed**, **{c['gone']} gone**, out of {c['kept_today']} kept today.\n"]
    if meta["unavailable_sources"]:
        L.append("**What could not be read today.** " + "; ".join(meta["unavailable_sources"]) +
                 ". Postings from these sources cannot be called gone or unchanged; they are marked unknown.\n")
    if meta["first_time_companies"]:
        L.append("**Not fresh, just not watched before.** " + ", ".join(meta["first_time_companies"]) +
                 " had nothing in the published state, so every kept posting from them shows as new. That says the company was added to the watch list, not that the postings were posted recently.\n")
    if meta.get("filter_note"):
        L.append("**The filter changed.** " + meta["filter_note"] + "\n")
    L.append("**How to read it.** Every row is a candidate for human review, not a classification. A keyword match is a guess; the matched words are listed so each one can be checked.\n")
    L.append("---\n")
    if new:
        L.append(f"## New ({len(new)})\n")
        for co in sorted(by_co):
            L.append(f"### {co} ({len(by_co[co])})\n")
            L.append("| Title | Location | Matched | Link |\n|---|---|---|---|")
            for r in sorted(by_co[co], key=lambda x: x["title"] or ""):
                ms = matched_text(r.get("matched"))
                L.append(f"| {r['title']} | {r.get('location_text') or ''} | {ms} | [link]({r['url']}) |")
            L.append("")
    if changed:
        L.append(f"## Changed ({len(changed)})\n")
        L.append("| Company | Title | What changed |\n|---|---|---|")
        for r in changed:
            L.append(f"| {r['company']} | {r['title']} | {', '.join(x['field'] for x in r['changes'])} |")
        L.append("")
    if gone:
        L.append(f"## Gone ({len(gone)})\n")
        L.append("| Company | Title | Why it is not in today's set |\n|---|---|---|")
        for r in gone:
            L.append(f"| {r['company']} | {r['title']} | {r['why']} |")
        L.append("")
    L.append("## Provenance\n")
    for n, h in meta["source_files_sha256"].items():
        L.append(f"- `{n}` sha256 `{h}` (kept on the machine that ran the collection, not published)")
    return "\n".join(L) + "\n"


def write_state(runs_dir, run, state_c):
    path = os.path.join(runs_dir, STATE_NAME)
    cands = dict(state_c)
    for k, v in run["kept"].items():
        cands[k] = {**v, "fp": fingerprint(v), "published": cands.get(k, {}).get("published", run["date"]),
                    "last_published": run["date"]}
    for k in [k for k in cands if k not in run["kept"] and run["sources"].get(cands[k]["company"], {}).get("status") == "ok"]:
        del cands[k]          # gone, and the source was readable: drop it. Unavailable sources keep their rows.
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"schema": 1, "as_of": run["date"], "kw_version": run["kw_version"], "candidates": cands}, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    return path


def watched_companies():
    """Companies on the current watch list (a company removed from sources.json is never posted)."""
    cfg = load_json(os.path.join(HERE, "sources.json"))
    return {b["company"] for s in cfg["sources"] for b in s["boards"]}


def post_new_listings(new, first_time, runs, date, send):
    try:
        import notify
    except ImportError:
        raise SystemExit("posting to Discord is done from the master folder (info-7375-computational-skepticism-for-ai), which has notify.py")
    return notify.post_new(new, watched_companies(), set(first_time), os.path.join(runs, "posted-to-discord.json"),
                           f"run {date}", send)


def git(args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", default=os.path.join(HERE, "runs"))
    ap.add_argument("--run", help="a run folder (default: the newest dated folder under --runs)")
    ap.add_argument("--write", action="store_true", help="write the delta files and update the published state")
    ap.add_argument("--commit", action="store_true", help="--write, then commit only those files; no push")
    ap.add_argument("--push", action="store_true", help="--commit, then push. Only on Professor Bear's word.")
    ap.add_argument("--post", action="store_true", help="after writing, post the new listings to the public Discord channel (standing rule, 2026-10-19)")
    ap.add_argument("--post-only", action="store_true", help="post the new listings in the latest run's existing delta file; write and commit nothing")
    a = ap.parse_args(argv)
    a.write = a.write or a.commit or a.push
    a.commit = a.commit or a.push

    runs = os.path.abspath(a.runs)
    if a.run:
        run_dir = os.path.abspath(a.run)
    else:
        dated = sorted(n for n in os.listdir(runs) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", n)
                       and find(os.path.join(runs, n), "jobs-of-interest-"))
        if not dated:
            raise SystemExit(f"no dated run folder with jobs-of-interest-*.json under {runs}")
        run_dir = os.path.join(runs, dated[-1])
    if a.post_only:
        d = os.path.basename(run_dir)
        dj = load_json(os.path.join(run_dir, f"delta-{d}.json"))
        post_new_listings(dj["new"], dj.get("first_time_companies", []), runs, d, send=True)
        return 0
    run = load_run(run_dir)

    state_path = os.path.join(runs, STATE_NAME)
    if os.path.exists(state_path):
        st = load_json(state_path)
        state_c, base_desc = st["candidates"], f"published state as of {st['as_of']} (filter {st.get('kw_version')})"
        if st["as_of"] >= run["date"]:
            raise SystemExit(f"published state is as of {st['as_of']}, not older than this run ({run['date']}); nothing to do")
    else:
        state_c, used = baseline_from_runs(runs, run["date"])
        base_desc = ("earlier runs treated as already published: " + ", ".join(used)) if used else "no earlier run: everything is new"

    new, changed, gone = diff(state_c, run)
    import re as _re
    base_versions = set(_re.findall(r"filter ([\w.]+)\)", base_desc)) - {"None"}
    filter_note = (f"The filter changed between the published runs ({', '.join(sorted(base_versions))}) and this one "
                   f"({run['kw_version']}). A 'matched' change can come from the filter, not from the posting."
                   if base_versions and run["kw_version"] not in base_versions else "")
    unavailable = [f"{co} ({s['status']}: {s.get('reason', '')})" for co, s in run["sources"].items() if s.get("status") != "ok"]
    print(f"run {run['date']}  kept {len(run['kept'])}  vs {base_desc}")
    print(f"  new {len(new)} · changed {len(changed)} · gone {len(gone)}")
    for u in unavailable:
        print(f"  UNAVAILABLE today: {u}")
    base_cos = {v["company"] for v in state_c.values()}
    first_time = sorted({r["company"] for r in new if r["company"] not in base_cos})
    if first_time:
        print("  first time in the published state (new because unwatched before, not because fresh): " + ", ".join(first_time))
    why = {}
    for r in gone:
        why[r["why"]] = why.get(r["why"], 0) + 1
    for w, n in sorted(why.items(), key=lambda x: -x[1]):
        print(f"  gone {n}: {w}")
    cos = {}
    for r in new:
        cos[r["company"]] = cos.get(r["company"], 0) + 1
    if cos:
        print("  new by company: " + ", ".join(f"{co} {n}" for co, n in sorted(cos.items(), key=lambda x: -x[1])))
    if not a.write:
        print("dry run: nothing written. Add --write to write the delta files (the published state moves only with --commit).")
        return 0

    paths = write_outputs(run_dir, run, base_desc, new, changed, gone, unavailable, first_time, filter_note)
    if a.post:
        post_new_listings(new, first_time, runs, run["date"], send=True)
    if a.commit:      # the state means "what is published": it moves only when the delta is committed
        paths["state"] = write_state(runs, run, state_c)
    for p in paths.values():
        print("  wrote", os.path.relpath(p, HERE))
    if not a.commit:
        return 0

    for ext in ("md", "json"):        # the churn report is small and is published with the delta, if today's run has one
        c = os.path.join(run_dir, f"churn-{run['date']}.{ext}")
        if os.path.exists(c):
            paths[f"churn_{ext}"] = c
    rel = [os.path.relpath(p, HERE) for p in paths.values()]
    bad = [r for r in rel if NEVER_COMMIT.search(r)]
    if bad:
        raise SystemExit(f"refusing to commit full snapshots: {bad}")
    top = git(["rev-parse", "--show-toplevel"], HERE)
    subject = f"data(lectern): delta {run['date']}: +{len(new)} new, ~{len(changed)} changed, -{len(gone)} gone"
    git(["add", "--", *[os.path.join(HERE, r) for r in rel]], top)
    git(["commit", "-m", subject, "--", *[os.path.join(HERE, r) for r in rel]], top)
    print("committed:", subject)
    print("Log row for FRICTIONAL.md's GitHub pushes table (add it yourself; this script does not edit the log):")
    print(f"| {dt.date.today().isoformat()} | {subject} |")
    if a.push:
        print(git(["push"], top) or "pushed")
    else:
        print("not pushed. Add --push (or run git push) only on Professor Bear's word.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
