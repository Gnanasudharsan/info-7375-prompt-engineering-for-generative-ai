#!/usr/bin/env python3
"""check-awards.py: does an institution hold ACTIVE federal research money on a topic?

An ingest script (SNICKERDOODLE P2: only ingest scripts touch the network). It asks two public award databases,
NIH RePORTER and the NSF Award Search, for awards at named institutions whose text matches a topic, and applies
three testable gates to every award it finds. It never writes a person's name into its tracked outputs.

  python3 scripts/funding/check-awards.py --orgs "NORTHEASTERN UNIVERSITY" "BROAD INSTITUTE, INC." \
      --terms "single cell" --window-start 2027-01-01 --out-json out.json --out-md out.md

Gates (each award gets all of them; a failed gate is recorded, never dropped):
  G1 active   the award ends at least --min-months-left months after --window-start
  G2 type     the award can pay for work by someone who is not its named trainee: research-project activity codes
              (R01, R21, R35, U01, P01 ...) pass; fellowship, career and training codes (F31, F32, K99, T32 ...) are
              marked trainee-only, because they fund one named person's training
  G3 org      a control query with no topic must find awards at that organisation name; if it finds none, the NAME is
              wrong, and a zero from a wrong name is not evidence of no funding
Privacy: --redact-ids replaces award numbers in the written outputs with a stable stand-in (activity code plus six hex
characters), for folders that may not carry grant tracking numbers. --private-file PATH (with --with-pi) writes the real
award numbers and the principal investigators' names to a file whose path contains a "private" directory, and nowhere else:
who holds an award is a local, human step, never a tracked one.
Amounts: NIH gives the amount of ONE fiscal year ('annual'); NSF gives an estimated total over the award ('total').
They are never added together.
"""
import argparse, datetime as dt, hashlib, json, os, re, sys, urllib.error, urllib.parse, urllib.request

REPORTER = "https://api.reporter.nih.gov/v2/projects/search"
NSF = "https://api.nsf.gov/services/v1/awards.json"
UA = "reallocation-engine-mode-build/0.1 (course project; public award data only)"
RESEARCH = {"R01", "R03", "R15", "R21", "R33", "R34", "R35", "R37", "R56", "R61", "R00", "RF1", "RM1", "DP1", "DP2", "DP5",
            "P01", "P20", "P30", "P50", "PM1", "U01", "U19", "U24", "U2C", "UG3", "UH3", "UM1", "OT2", "R43", "R44"}
TRAINEE = {"F30", "F31", "F32", "F33", "K01", "K08", "K12", "K23", "K24", "K25", "K99", "T32", "T34", "T35", "T90", "TL1", "D43", "R25"}
NIH_FIELDS = ["ProjectNum", "AwardAmount", "ProjectStartDate", "ProjectEndDate", "Organization", "ProjectTitle", "FiscalYear", "AgencyIcAdmin"]
PI_FIELD = "PrincipalInvestigators"   # requested ONLY with --with-pi, and written ONLY to --private-file
PI_KEY = "principal_investigators"      # the key the API answers with


def http_json(url, body=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **({"Content-Type": "application/json"} if body is not None else {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def activity_code(project_num):
    m = re.match(r"^\d?([A-Z]\d{2}|[A-Z]{2}\d)", project_num or "")
    return m.group(1) if m else None


def months_between(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month) + (b.day - a.day) / 30.0


def gates(end_date, code, window_start, min_months):
    months_left = round(months_between(window_start, end_date), 1) if end_date else None
    g1 = bool(end_date) and months_left >= min_months
    if code in RESEARCH:
        g2 = "research-project"
    elif code in TRAINEE:
        g2 = "trainee-only"
    else:
        g2 = "unclassified"                      # an unknown code is neither passed nor failed: a person decides
    return {"G1_active": g1, "months_left_at_window_start": months_left, "G2_type": g2}


def parse_date(s):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s or "")
    return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def nih_query(org, term, fy, fetch, limit=500, first_page_only=False, with_pi=False):
    crit = {"org_names": [org], "fiscal_years": [fy]}
    if term:
        crit["advanced_text_search"] = {"operator": "and", "search_field": "all", "search_text": term}
    fields = NIH_FIELDS + ([PI_FIELD] if with_pi else [])
    rows, offset, total = [], 0, 0
    while True:
        r = fetch(REPORTER, {"criteria": crit, "include_fields": fields, "limit": limit, "offset": offset})
        total = r.get("meta", {}).get("total", 0)
        rows += r.get("results", [])
        offset += limit
        if first_page_only or offset >= total or not r.get("results"):
            break
    return total, rows


NSF_PAGE = 25          # the Award Search returns 25 awards a page unless told otherwise; a query that stops at 25 is cut off
NSF_MAX_PAGES = 40


def nsf_query(org, term, window_start, fetch):
    """All awards for one awardee and phrase, page by page. Returns (awards, truncated)."""
    rows, truncated = [], False
    for page in range(NSF_MAX_PAGES):
        params = {"awardeeName": org, "keyword": f'"{term}"', "expDateStart": window_start.strftime("%m/%d/%Y"), "rpp": NSF_PAGE, "offset": page * NSF_PAGE + 1,
                  "printFields": "id,title,startDate,expDate,estimatedTotalAmt,fundsObligatedAmt,awardeeName,fundProgramName"}
        got = fetch(NSF + "?" + urllib.parse.urlencode(params), None).get("response", {}).get("award") or []
        rows += got
        if len(got) < NSF_PAGE:
            break
    else:
        truncated = True                   # hit the page cap while pages were still full: say so, never report it as complete
    return rows, truncated


def run(orgs, terms, fy, window_start, min_months, fetch=http_json, sources=("nih", "nsf"), log=lambda *a: None, with_pi=False, sidecar=None):
    awards, queries, orgs_status = {}, [], {}
    for org in orgs:
        if "nih" in sources:
            ctl, _ = nih_query(org, None, fy, fetch, limit=1, first_page_only=True)          # G3: does this organisation name exist in the database?
            orgs_status[org] = {"nih_control_total": ctl, "name_matched": ctl > 0}
            queries.append({"source": "nih_reporter", "org": org, "term": None, "fiscal_year": fy, "reported_total": ctl, "purpose": "control (G3)"})
            if ctl == 0:
                log(f"  {org}: NAME NOT MATCHED in NIH RePORTER (control query found nothing); no topic query run")
                continue
            for term in terms:
                total, rows = nih_query(org, term, fy, fetch, with_pi=with_pi)
                names = sorted({x["organization"]["org_name"] for x in rows})
                orgs_status[org]["returned_org_names"] = sorted(set(orgs_status[org].get("returned_org_names", [])) | set(names))
                if len(orgs_status[org]["returned_org_names"]) > 1:
                    log(f"  {org}: the database matched {len(orgs_status[org]['returned_org_names'])} different organisation names; a partial name matches loosely")
                queries.append({"source": "nih_reporter", "org": org, "term": term, "fiscal_year": fy, "reported_total": total, "fetched": len(rows)})
                for x in rows:
                    num = x["project_num"]
                    end, code = parse_date(x.get("project_end_date")), activity_code(num)
                    key = ("nih", num)
                    a = awards.setdefault(key, {"source": "nih_reporter", "award_id": num, "query_org": org, "org": x["organization"]["org_name"], "title": x.get("project_title"),
                                                "activity_code": code, "ic": (x.get("agency_ic_admin") or {}).get("abbreviation"), "fiscal_year": x.get("fiscal_year"),
                                                "amount": x.get("award_amount"), "amount_kind": "annual (one fiscal year)", "start": (x.get("project_start_date") or "")[:10] or None,
                                                "end": (x.get("project_end_date") or "")[:10] or None, "terms_matched": []})
                    a["terms_matched"].append(term)
                    a.update(gates(end, code, window_start, min_months))
                    if sidecar is not None and x.get(PI_KEY):
                        sidecar[num] = {"org": a["org"], "principal_investigators": [p.get("full_name") for p in x[PI_KEY]]}
        if "nsf" in sources:
            for term in terms:
                try:
                    rows, truncated = nsf_query(org, term, window_start, fetch)
                except urllib.error.URLError as e:
                    raise SystemExit(f"NSF Award Search failed ({e}); refusing to report a zero")
                # The NSF search matches awardee names loosely (a query for one university returns many). Keep only awards whose
                # awardee name is the same name, ignoring case and punctuation, and count what was dropped so it stays visible.
                kept = [x for x in rows if norm_name(x.get("awardeeName")) == norm_name(org)]
                queries.append({"source": "nsf_award_search", "org": org, "term": term, "window_start": str(window_start), "fetched": len(rows), "kept_exact_awardee_name": len(kept),
                                "dropped_other_awardees": len(rows) - len(kept), "truncated": truncated,
                                "note": "no control query exists for NSF: a zero here may be a name the NSF spells differently"})
                rows = kept
                for x in rows:
                    end = None
                    m = re.match(r"(\d\d)/(\d\d)/(\d{4})", x.get("expDate") or "")
                    if m:
                        end = dt.date(int(m.group(3)), int(m.group(1)), int(m.group(2)))
                    prog = (x.get("fundProgramName") or "")
                    a = awards.setdefault(("nsf", x["id"]), {"source": "nsf_award_search", "award_id": x["id"], "query_org": org, "org": x.get("awardeeName"), "title": x.get("title"), "activity_code": None,
                                                              "ic": prog or None, "fiscal_year": None, "amount": int(x["estimatedTotalAmt"]) if str(x.get("estimatedTotalAmt", "")).isdigit() else None,
                                                              "amount_kind": "total (estimated, whole award)", "start": x.get("startDate"), "end": end.isoformat() if end else None, "terms_matched": []})
                    a["terms_matched"].append(term)
                    g = gates(end, None, window_start, min_months)
                    g["G2_type"] = "trainee-only" if re.search(r"fellowship|traineeship|training", prog, re.I) else "research-project"
                    a.update(g)
    return list(awards.values()), queries, orgs_status


def norm_name(x):
    return re.sub(r"[^a-z0-9 ]", "", (x or "").casefold()).strip()


def pseudo_id(award_id, code):
    return f"redacted-{code or 'NSF'}-{hashlib.sha1(award_id.encode()).hexdigest()[:6]}"


def redact(awards):
    out = []
    for a in awards:
        b = dict(a)
        b["award_id"] = pseudo_id(a["award_id"], a.get("activity_code"))
        out.append(b)
    return out


def private_path_ok(path):
    return "private" in os.path.normpath(os.path.abspath(path)).split(os.sep)


def summarise(awards, orgs):
    out = {}
    for org in orgs:
        mine = [a for a in awards if a.get("query_org") == org]
        res = [a for a in mine if a.get("G1_active") and a.get("G2_type") == "research-project"]
        nih = [a for a in res if a["source"] == "nih_reporter"]
        out[org] = {"found": len(mine), "pass_G1_and_G2": len(res), "trainee_only": sum(1 for a in mine if a.get("G2_type") == "trainee-only"),
                    "ended_before_window_plus_margin": sum(1 for a in mine if not a.get("G1_active")),
                    "nih_annual_amount_of_passing_awards": sum(a["amount"] or 0 for a in nih)}
    return out


def render_md(report):
    c = report["config"]
    L = ["# Funded-research award check", "",
         "## Executive summary", "",
         f"This report asks two public federal award databases which of {len(c['orgs'])} Boston-area institutions hold active research money on the topic \"{', '.join(c['terms'])}\". "
         "It exists because a lab's own web page never says whether the lab can pay anyone; the money is on record elsewhere. "
         f"For work starting {c['window_start']}, it found {report['totals']['found']} awards, of which {report['totals']['pass']} are research-project awards still running at least {c['min_months_left']} months into the window. "
         "A zero for an institution means either no money or a misspelled name; the table says which. "
         "This is a list of funded projects, not of labs that want a collaborator: whose project each one is, and whether they would talk, is the next, human step.", "",
         "## What the numbers mean", "",
         "- NIH amounts are one fiscal year's award; NSF amounts are an estimated total over the whole award. They are never added together.",
         "- *Trainee-only* awards (fellowships, career and training grants) pay one named person's training; they are not a source of pay for anyone else.",
         "- No person's name is in this report. Looking up who holds an award is a separate, local step.", "",
         "## By institution", "",
         "| Institution | Name matched in NIH | Awards found | Research awards running into the window | Trainee-only | Ended or ending too soon | NIH annual $ of the passing awards |", "|---|---|---|---|---|---|---|"]
    for org, s in report["by_org"].items():
        nm = report["orgs_status"].get(org, {})
        matched = "yes" if nm.get("name_matched") else ("NO: the name is wrong, not the funding" if nm else "n/a")
        L.append(f"| {org} | {matched} | {s['found']} | {s['pass_G1_and_G2']} | {s['trainee_only']} | {s['ended_before_window_plus_margin']} | {s['nih_annual_amount_of_passing_awards']:,} |")
    multi = {o: st["returned_org_names"] for o, st in report["orgs_status"].items() if len(st.get("returned_org_names", [])) > 1}
    if multi:
        L += ["", "**The name matched more than one organisation:** " + "; ".join(f"{o} returned {len(n)} names ({', '.join(n)})" for o, n in multi.items()) + ". A partial name is accepted loosely; use the exact name."]
    L += ["", "## Provenance", ""]
    for q in report["queries"]:
        tot = f"reported total {q['reported_total']}" if "reported_total" in q else "no total reported by this source"
        L.append(f"- {q['source']} · {q['org']} · {q.get('term') or '(control, no topic)'} · {tot} · fetched {q.get('fetched', 'only the total was read')}" + (f" · kept {q['kept_exact_awardee_name']} under the same awardee name, dropped {q['dropped_other_awardees']} other awardees" if "kept_exact_awardee_name" in q else "") + (" · **TRUNCATED, results incomplete**" if q.get("truncated") else ""))
    L += ["", f"Retrieved {report['retrieved_at']}. Window start {c['window_start']}; minimum months left {c['min_months_left']}."]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orgs", nargs="+", required=True, help="exact organisation names as NIH RePORTER spells them (upper case)")
    ap.add_argument("--terms", nargs="+", required=True)
    ap.add_argument("--fy", type=int, default=dt.date.today().year, help="NIH fiscal year to read (default: this year)")
    ap.add_argument("--window-start", required=True, help="YYYY-MM-DD: when the work would start")
    ap.add_argument("--min-months-left", type=int, default=6)
    ap.add_argument("--sources", nargs="+", default=["nih", "nsf"], choices=["nih", "nsf"])
    ap.add_argument("--out-json", required=True); ap.add_argument("--out-md", required=True)
    ap.add_argument("--redact-ids", action="store_true", help="replace award numbers in the written outputs with stable stand-ins")
    ap.add_argument("--with-pi", action="store_true", help="also fetch principal investigators; needs --private-file")
    ap.add_argument("--private-file", help="where real award numbers and investigators go; the path must contain a 'private' directory")
    a = ap.parse_args(argv)
    ws = parse_date(a.window_start) or sys.exit("--window-start must be YYYY-MM-DD")
    if a.with_pi and not a.private_file:
        print("STOP: --with-pi needs --private-file, so that no person's name can reach a tracked file.", file=sys.stderr)
        return 2
    if a.private_file and not private_path_ok(a.private_file):
        print(f"STOP: {a.private_file} is not under a 'private' directory; refusing to write award numbers or names there.", file=sys.stderr)
        return 2
    sidecar = {} if a.private_file else None
    try:
        awards, queries, orgs_status = run(a.orgs, a.terms, a.fy, ws, a.min_months_left, sources=tuple(a.sources), log=lambda m: print(m, file=sys.stderr), with_pi=a.with_pi, sidecar=sidecar)
    except urllib.error.URLError as e:
        print(f"STOP: a database could not be reached ({e}). Refusing to report an empty result.", file=sys.stderr)
        return 2
    by_org = summarise(awards, a.orgs)
    if sidecar is not None:
        full = {pseudo_id(x["award_id"], x.get("activity_code")): {"award_id": x["award_id"], **sidecar.get(x["award_id"], {"org": x["org"]})} for x in awards}
        os.makedirs(os.path.dirname(os.path.abspath(a.private_file)), exist_ok=True)
        with open(a.private_file, "w", encoding="utf-8") as f:
            json.dump(full, f, indent=2, ensure_ascii=False); f.write("\n")
    report = {"tool": "check-awards", "tool_version": "0.1.0", "retrieved_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
              "config": {"orgs": a.orgs, "terms": a.terms, "fy": a.fy, "window_start": a.window_start, "min_months_left": a.min_months_left, "sources": a.sources},
              "orgs_status": orgs_status, "queries": queries, "by_org": by_org,
              "totals": {"found": len(awards), "pass": sum(s["pass_G1_and_G2"] for s in by_org.values())},
              "awards": sorted(redact(awards) if a.redact_ids else awards, key=lambda x: (x["org"] or "", x["award_id"])),
              "labels": {"award_fields": "record (from the database)", "gates": "script-output", "interpretation": "not produced here: a person decides which awards matter"}}
    with open(a.out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False); f.write("\n")
    with open(a.out_md, "w", encoding="utf-8") as f:
        f.write(render_md(report))
    print(f"found {report['totals']['found']} awards; {report['totals']['pass']} research-project awards running into the window; wrote {a.out_json} and {a.out_md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
