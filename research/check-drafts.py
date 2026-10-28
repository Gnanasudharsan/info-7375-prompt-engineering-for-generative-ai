"""Read-only checks for the optional book; not editorial or factual approval."""
import argparse
import ast
import json
from pathlib import Path
import re
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--require-full", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    weeks = json.loads((root / "course.json").read_text())["weeks"]
    rows, failures, pending = [], [], []
    found = sorted((root / "chapters").glob("[0-9][0-9]-*.md"))
    by_number = {}
    for p in found:
        by_number.setdefault(int(p.name[:2]), []).append(p)
    weeks_numbers = {w["week"] for w in weeks}
    for number, paths in by_number.items():
        if number not in weeks_numbers or len(paths) > 1:
            failures.append("Unexpected chapter filenames: " + repr(sorted(x.name for x in paths)))
    for week in weeks:
        matches = by_number.get(week["week"], [])
        if not matches:
            pending.append("%02d-*.md" % week["week"])
            continue
        chapter = matches[0]
        body = chapter.read_text()
        words = len(body.split())
        if not 5000 <= words <= 9000:
            failures.append(f"{chapter.name}: {words} words outside approved range")
        if not body.startswith(f"# Chapter {week['week']} — "):
            failures.append(f"{chapter.name}: title/number mismatch")
        for heading in ("## What you will be able to do", "## Assessments — ungraded practice",
                        "### Warm-up", "### Application", "### Synthesis", "### Challenge"):
            if heading not in body:
                failures.append(f"{chapter.name}: missing {heading}")
        if "[FIGURE:" not in body:
            failures.append(f"{chapter.name}: no figure-needs marker")
        if f"../{week['path']}/docs/en.md" not in body:
            failures.append(f"{chapter.name}: missing paired lesson link")
        if f"../{week['path']}/quiz.json" not in body:
            failures.append(f"{chapter.name}: missing existing knowledge check")
        for i, snippet in enumerate(re.findall(r"```python\n(.*?)```", body, re.S)):
            try:
                ast.parse(snippet)
            except SyntaxError as error:
                failures.append(f"{chapter.name}: Python block {i}: {error}")
        for target in re.findall(r"\]\(([^)]+)\)", body):
            if "://" in target or target.startswith("#"):
                continue
            path_part = target.split("#")[0]
            if path_part and not (chapter.parent / path_part).exists():
                failures.append(f"{chapter.name}: broken local link {target}")
        if "## Irreducibly Human" in body and not all(x in body for x in ("**AI should**", "**Human should**")):
            failures.append(f"{chapter.name}: missing explicit responsibility split")
        sidecar = Path(str(chapter) + ".verified.json")
        if not sidecar.exists():
            failures.append(f"{chapter.name}: missing review sidecar")
        rows.append({"chapter": chapter.name, "whitespace_words": words})
    if args.require_full and pending:
        failures.append(f"Full draft incomplete: {len(pending)} chapters missing")
    print(json.dumps({"scope": "structural checks only; not prose, source, or human approval",
                      "chapters": rows, "total_whitespace_words": sum(r['whitespace_words'] for r in rows),
                      "pending": pending, "full_draft_exists": not pending,
                      "failures": failures}, indent=2))
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
