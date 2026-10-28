"""How many sponsored titles does the 80 Days CSV list per company? (run from the-reallocation-engine root)"""
import ast, collections, csv
F = "data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv"
rows = sponsors = 0
counts = collections.Counter()
with open(F, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows += 1
        try:
            approvals = float(r["Total Approvals"])
        except ValueError:
            approvals = 0.0
        t = r["top_job_titles_sponsored"].strip()
        n = len(ast.literal_eval(t)) if t.startswith("[") else 0
        if approvals > 0:
            sponsors += 1
            counts[n] += 1
print(f"rows: {rows}; companies with Total Approvals > 0: {sponsors}")
print("titles listed per sponsoring company:", dict(sorted(counts.items())))
print(f"exactly one title: {counts[1]} of {sponsors} ({counts[1] / sponsors:.1%}); five or fewer: "
      f"{sum(v for k, v in counts.items() if k <= 5)} of {sponsors}")
