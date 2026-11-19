"""Evaluate archived filter outputs and confirmed shortlist labels offline."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/20261119T162945Z"
VARIANTS = {
    "v1.0": "",
    "C1": "_C1",
    "C2": "_C2",
    "C3′ (revised C3)": "_C3",
    "C4": "_C4",
}
DECISIONS = ("keep", "reject", "cannot_tell")
VERDICTS = ("RELEVANT", "NOT_RELEVANT", "CANNOT_TELL")
CLAIM_LABELS = {"SUPPORTED", "CONTRADICTED", "INSUFFICIENT"}


def index(rows, *fields):
    result = {}
    for row in rows:
        key = tuple(str(row[field]) for field in fields)
        if key in result:
            raise ValueError(f"Duplicate key {key}")
        result[key] = row
    return result


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def audit_labels(version):
    sample = json.loads((ROOT / f"audit/sample_{version}.json").read_text(encoding="utf-8"))
    expected = index(sample, "n", "board", "id")
    rows = csv_rows(ROOT / f"audit/hand_verdicts_{version}.csv")
    if index(rows, "n", "board", "id").keys() != expected.keys():
        raise ValueError(f"Audit sample and verdict IDs differ for {version}")
    labels = {}
    for key, row in index(rows, "board", "id").items():
        original = row["my_verdict"]
        correction = row.get("corrected_after_unblind")
        if original not in VERDICTS or not row["my_reason"].strip():
            raise ValueError(f"Missing confirmed verdict or reason for {key}")
        if correction and (correction not in VERDICTS or not row["correction_reason"].strip()):
            raise ValueError(f"Invalid correction for {key}")
        labels[key] = (original, correction or original)
    return labels


def filter_metrics():
    first, second = audit_labels("v1"), audit_labels("v2")
    if first.keys() & second.keys():
        raise ValueError("The hand-labeled samples overlap")
    labels = first | second
    print(f"## Filter comparisons on {len(labels)} hand-audited development postings\n")
    print("| Variant | Corpus keep / reject / abstain | Decision flips | A3 / A6 fired | "
          "Labeled keep (R / N / U) | Labeled reject (R / N / U) | Labeled abstain (R / N / U) | "
          "Exact matches corrected / blind |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for name, suffix in VARIANTS.items():
        with (RUN / f"filter_v1{suffix}.jsonl").open(encoding="utf-8") as source:
            rows = index(map(json.loads, source), "board", "id")
        if not suffix:
            baseline = rows
        if rows.keys() != baseline.keys() or not labels.keys() <= rows.keys():
            raise ValueError(f"Inconsistent corpus for {name}")
        counts = Counter(row["decision"] for row in rows.values())
        flips = sum(row["decision"] != baseline[key]["decision"] for key, row in rows.items())
        filters = Counter(rule for row in rows.values() for rule in row["rejected_by"])
        actual = Counter((rows[key]["decision"], verdicts[1]) for key, verdicts in labels.items())
        exact = [sum(VERDICTS[DECISIONS.index(rows[key]["decision"])] == verdict[version]
                     for key, verdict in labels.items()) for version in (1, 0)]
        cells = [" / ".join(str(counts[d]) for d in DECISIONS), str(flips), f"{filters['A3']} / {filters['A6']}"]
        cells.extend(" / ".join(str(actual[d, v]) for v in VERDICTS) for d in DECISIONS)
        cells.append(" / ".join(f"{n}/{len(labels)}" for n in exact))
        print("| " + " | ".join([name, *cells]) + " |")


def claim_metrics():
    keys = ("board", "id", "claim")
    proposed = index(json.loads((ROOT / "shortlist/shortlist_v1_1.json").read_text(encoding="utf-8")), *keys)
    reviewed = index(csv_rows(ROOT / "shortlist/claim_labels.csv"), *keys)
    if len(proposed) != 75 or proposed.keys() != reviewed.keys():
        raise ValueError("Expected 75 matching unique shortlist claim keys")
    print("\n## Shortlist label verification\n")
    labels = Counter()
    changes = 0
    for key, row in reviewed.items():
        if any(row[field] != proposed[key][field] for field in ("title", "proposed", "span")):
            raise ValueError(f"Original shortlist evidence changed for {key}")
        label = row["my_label"]
        if not label:
            continue
        if label not in CLAIM_LABELS or (label != row["proposed"] and not row["my_note"].strip()):
            raise ValueError(f"Invalid label or missing change rationale for {key}")
        labels[label] += 1
        changes += label != row["proposed"]
    confirmed = labels.total()
    print(f"{confirmed}/75 confirmed labels in the workspace CSV. {75 - confirmed} outstanding.")
    print("Confirmed counts: " + ", ".join(f"{label} {labels[label]}" for label in sorted(CLAIM_LABELS)) + ".")
    print(f"Confirmed changes from original proposals: {changes}/{confirmed}.")
    print("Source of truth: my_label in claim_labels.csv, with no suggestion-file fallback.")
    return confirmed == 75


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-partial-claims", action="store_true", help="report confirmed rows while showing the outstanding count")
    args = parser.parse_args()
    filter_metrics()
    done = claim_metrics()
    return 0 if done or args.allow_partial_claims else 1


if __name__ == "__main__":
    raise SystemExit(main())
