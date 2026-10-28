#!/usr/bin/env python3
"""eval_first_rows.py — dataset side of the first evaluation rows (Co-op Sponsor Check).

For each company, ask MY recipe's own matcher (imported, not re-implemented) what the
80 Days to Stay CSV says, using the name a student would type. Also list every CSV
name that merely CONTAINS the typed word — an audit for the human, never a match.

Usage: python3 eval_first_rows.py <path-to-the-reallocation-engine checkout>
"""
import csv, json, os, sys

REPO = os.path.abspath(sys.argv[1])
RECIPE = os.path.join(REPO, "scripts/contrib/2026fa/arundhatik26-coop-sponsor-swe-15-1252")
sys.path.insert(0, RECIPE)
import coop_sponsor_check as c  # noqa: E402

COMPANIES = ["PayPal", "Visa", "Goldman Sachs", "Mastercard", "BlackRock", "LSEG"]
RULES = {"proven_min_approvals": 100, "p_proven": 0.9, "p_likely": 0.6, "p_sponsors_not_software": 0.3}

csv_path = os.path.join(REPO, c.SPONSOR_CSV)
idx = c.load_sponsor_index(csv_path)
names = []
with open(csv_path, encoding="utf-8", newline="") as f:
    names = [r["company_name"] for r in csv.DictReader(f)]

out = []
for co in COMPANIES:
    ev = c.resolve_company({"company": co}, idx, RULES)
    word = co.split()[0].upper()
    contains = sorted({n for n in names if word in n.upper()})
    row = {"company": co, "status": ev["status"],
           "csv_rows": ev.get("rows", []),
           "total_approvals": (ev.get("total_approvals") or {}).get("value"),
           "software_titles": (ev.get("software_titles") or {}).get("value"),
           "tier": (ev.get("tier") or {}).get("value"),
           "audit_names_containing_word": contains[:12], "audit_count": len(contains)}
    out.append(row)
print(json.dumps({"csv": c.SPONSOR_CSV, "csv_sha256": c.sha256(csv_path), "rows": out}, indent=2))
