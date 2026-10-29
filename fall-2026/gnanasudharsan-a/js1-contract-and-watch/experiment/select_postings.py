"""Select 20 postings for blind hand labeling and split them into dev and held-out.

Offline: reads one saved board response and judges it with the current rule.
The output files carry no rule verdict, so the labels can be written blind.
Refuses to overwrite earlier output, so the selection is made once.

Usage: .venv/bin/python experiment/select_postings.py
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from jobwatch.persona import DEFAULT_PERSONA, load_persona  # noqa: E402
from jobwatch.rule import _phrase_pattern, html_to_text, judge_posting  # noqa: E402

RAW_FILE = ROOT / "data" / "raw" / "anthropic_20261028T192103Z.json"
OUT_DIR = ROOT / "experiment"
SEED = 7375
TOTAL = 20
DEV_SIZE = 10
# "engineer" is a substring test (it also matches "engineering"); the others
# are whole-word/phrase tests, so "ai" does not match inside "maintain".
ENGINEER_WORD = "engineer"
FIELD_WORDS = ("ai", "ml", "machine learning", "research", "nlp")


def title_matches(title: str) -> bool:
    lowered = (title or "").lower()
    return ENGINEER_WORD in lowered and any(
        _phrase_pattern(word).search(lowered) for word in FIELD_WORDS)


def blind_record(job: dict) -> dict:
    return {
        "id": job["id"],
        "title": job.get("title"),
        "location.name": (job.get("location") or {}).get("name"),
        "content": html_to_text(job.get("content")),
    }


def write_new(path: Path, text: str) -> None:
    with open(path, "x", encoding="utf-8") as f:
        f.write(text)


def main() -> None:
    jobs = json.loads(RAW_FILE.read_bytes())["jobs"]
    persona = load_persona(DEFAULT_PERSONA)
    verdicts = {job["id"]: judge_posting(job, persona)["verdict"] for job in jobs}

    relevant = sorted((j for j in jobs if verdicts[j["id"]] == "RELEVANT"),
                      key=lambda j: j["id"])
    not_relevant = [j for j in jobs if verdicts[j["id"]] == "NOT_RELEVANT"]
    # Sorted by id so the sample depends only on the seed, not on board order.
    title_pool = sorted((j for j in not_relevant if title_matches(j.get("title"))),
                        key=lambda j: j["id"])

    need = TOTAL - len(relevant)
    if need < 0 or need > len(title_pool):
        sys.exit(f"cannot make {TOTAL}: {len(relevant)} RELEVANT, "
                 f"{len(title_pool)} in the title pool")
    added = random.Random(SEED).sample(title_pool, need)

    chosen = relevant + added
    random.Random(SEED).shuffle(chosen)
    dev, heldout = chosen[:DEV_SIZE], chosen[DEV_SIZE:]

    for name, part in (("postings_dev.json", dev), ("postings_heldout.json", heldout)):
        write_new(OUT_DIR / name,
                  json.dumps([blind_record(j) for j in part], indent=2,
                             ensure_ascii=False) + "\n")

    # The log lists ids per split only, not which pool each came from, so
    # reading it before labeling does not reveal the rule's verdicts.
    log = [
        f"raw_file: {RAW_FILE.relative_to(ROOT)}",
        f"seed: {SEED} (random.Random({SEED}).sample for the added postings; "
        f"a fresh random.Random({SEED}).shuffle for the split)",
        f"title filter: '{ENGINEER_WORD}' as substring AND whole word/phrase any of "
        + ", ".join(f"'{w}'" for w in FIELD_WORDS),
        f"total postings: {len(jobs)}",
        f"rule RELEVANT pool: {len(relevant)} (all taken)",
        f"rule NOT_RELEVANT pool: {len(not_relevant)}",
        f"NOT_RELEVANT title-filter pool: {len(title_pool)} (sampled {need})",
        f"chosen: {len(chosen)}",
        f"dev ids ({len(dev)}): " + ", ".join(str(j["id"]) for j in dev),
        f"heldout ids ({len(heldout)}): " + ", ".join(str(j["id"]) for j in heldout),
    ]
    write_new(OUT_DIR / "selection_log.txt", "\n".join(log) + "\n")


if __name__ == "__main__":
    main()
