"""Review shortlist claims in the terminal. Use --batch for Codex suggestions."""

import argparse
import csv
import gzip
import html
import io
import json
import os
import re
import tempfile
from itertools import groupby
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABELS = ROOT / "shortlist/claim_labels.csv"
SUGGESTIONS = ROOT / "shortlist/claim_suggestions.json"
CODES = {"s": "SUPPORTED", "c": "CONTRADICTED", "i": "INSUFFICIENT"}


def key(row):
    return row["board"], row["id"], row["claim"]


def pending(row):
    return not (row["my_label"] or row["my_note"])


def read_labels():
    original = LABELS.read_bytes()
    reader = csv.DictReader(io.StringIO(original.decode("utf-8"), newline=""))
    return original, reader.fieldnames, list(reader)


def save(original, fields, rows):
    """Publish a complete CSV and catch edits made while a batch was open."""
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="", dir=LABELS.parent, delete=False
    ) as out:
        temporary = Path(out.name)
        try:
            writer = csv.DictWriter(out, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
            out.close()
            if LABELS.read_bytes() != original:
                raise SystemExit("The CSV changed during review. Restart to load the current labels.")
            temporary.chmod(LABELS.stat().st_mode & 0o777)
            os.replace(temporary, LABELS)
            return LABELS.read_bytes()
        finally:
            temporary.unlink(missing_ok=True)


def load_suggestions():
    data = json.loads(SUGGESTIONS.read_text(encoding="utf-8"))
    with gzip.open(ROOT / data["source"], "rt", encoding="utf-8") as archive:
        jobs = json.load(archive)["jobs"]
    by_id = {}
    for job in jobs:
        content = html.unescape(html.unescape(job.get("content") or ""))
        content = re.sub(r"</(?:p|li|h[1-6]|div)>|<br\s*/?>", "\n", content)
        content = re.sub(r"<[^>]+>", "", content)
        by_id[str(job["id"])] = {
            "description": "\n".join(line.strip() for line in content.splitlines() if line.strip()),
            "location": job["location"]["name"],
        }
    suggestions = {}
    for item in data["suggestions"]:
        ref = key(item)
        if ref in suggestions or item["label"] not in CODES.values():
            raise SystemExit(f"Duplicate or invalid suggestion for {ref}")
        source = by_id[item["id"]][item["field"]]
        if not item["quote"] or " ".join(item["quote"].split()) not in " ".join(source.split()):
            raise SystemExit(f"Could not verify source quote for {ref}")
        suggestions[ref] = item
    return suggestions, by_id


def choose_label(row):
    while True:
        choice = input("Label [s]upported / [c]ontradicted / [i]nsufficient / [q] cancel > ").strip().lower()
        if choice == "q":
            return None
        if choice in CODES:
            label = CODES[choice]
            note = input("Your note > ").strip()
            while label != row["proposed"] and not note:
                note = input("Give your reason for changing the original label > ").strip()
            return label, note


def review_batch(group, suggestions, source):
    decisions = {}
    while True:
        for number, row in enumerate(group, 1):
            item = suggestions[key(row)]
            label, note = decisions.get(number, (item["label"], ""))
            status = "Your edit" if number in decisions else "Codex suggestion"
            print(f"\n{number}. {row['claim']}  (original proposal: {row['proposed']})")
            print(f"   {status}: {label}")
            print(f"   {item['field']}: {item['quote']}")
            print(f"   Codex reason: {item['reason']}")
            if note:
                print(f"   Your note: {note}")
        print("\nApproving also endorses the displayed Codex reason for any unedited suggestion "
              "that changes the original proposal.")
        command = input(
            f"[a] approve / [1–{len(group)}] edit / [v] full posting / [n] skip / [q] quit > "
        ).strip().lower()
        if command in {"n", "q"}:
            return command
        if command == "v":
            print(f"\nLocation: {source['location']}\n\n{source['description']}")
        if command in {str(n) for n in range(1, len(group) + 1)}:
            number = int(command)
            decision = choose_label(group[number - 1])
            if decision:
                decisions[number] = decision
        if command == "a":
            for number, row in enumerate(group, 1):
                if number in decisions:
                    row["my_label"], row["my_note"] = decisions[number]
                else:
                    row["my_label"] = suggestions[key(row)]["label"]
                    if row["my_label"] != row["proposed"]:
                        row["my_note"] = "Approved Codex rationale: " + suggestions[key(row)]["reason"]
            return "a"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--batch", action="store_true", help="review and approve one posting at a time")
    modes.add_argument("--status", action="store_true", help="print review counts and verify suggestion quotes")
    args = parser.parse_args()
    original, fields, rows = read_labels()
    todo = [row for row in rows if pending(row)]
    reviewed = sum(bool(row["my_label"]) for row in rows)
    print(f"{reviewed} labeled of {len(rows)} claims. {len(todo)} available for review.")
    if reviewed + len(todo) != len(rows):
        print("Rows with existing notes and no label need manual attention.")
    if args.batch or args.status:
        suggestions, jobs = load_suggestions()
        missing = [key(row) for row in todo if key(row) not in suggestions]
        if missing:
            raise SystemExit(f"Missing batch suggestions: {missing}")
        if args.status:
            print(f"Verified source quotes for {len(suggestions)} stored Codex suggestions.")
            return

    try:
        for (board, identifier), group in groupby(todo, key=lambda row: (row["board"], row["id"])):
            group = list(group)
            print(f"\n{group[0]['title']} ({board} {identifier})")
            if args.batch:
                command = review_batch(group, suggestions, jobs[identifier])
                if command == "q":
                    break
                if command == "a":
                    original = save(original, fields, rows)
                    print(f"Saved {len(group)} approved labels.")
                continue
            for row in group:
                print(f"\n{row['claim']}\nProposed: {row['proposed']}\nSpan: {row['span']}")
                decision = choose_label(row)
                if decision is None:
                    return
                row["my_label"], row["my_note"] = decision
                original = save(original, fields, rows)
    except (EOFError, KeyboardInterrupt):
        print("\nReview stopped. Only previously saved decisions were recorded.")
    finally:
        print(f"{sum(pending(row) for row in rows)} claims available for review.")


if __name__ == "__main__":
    main()
