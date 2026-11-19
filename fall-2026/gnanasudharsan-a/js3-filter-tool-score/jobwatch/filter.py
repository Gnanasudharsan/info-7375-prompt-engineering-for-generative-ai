"""FILTER.md v1.0 as code: Stage A hard rejects, abstention, Stage B score, threshold.

evaluate(posting) -> {"decision": "keep" | "reject" | "cannot_tell",
                      "rejected_by": [rule ids], "score": int | None,
                      "components": {"B1": int, "B2": [words], "B3": [skills]},
                      "matched": {rule_id: matched text}}

Every word list and number is in FILTER_V1 below, so a version change is one visible diff.
Matching is case-insensitive and on whole words: no letter or digit directly before or after
a phrase, and any whitespace run between its words. HTML is unescaped and tags are stripped
before matching. Deterministic and offline.
"""
import html
import re

FILTER_V1 = {
    "version": "1.0",
    # Stage A — hard rejects
    "A1_title_seniority": ["senior", "sr", "staff", "principal", "lead", "manager",
                           "director", "head", "vp", "distinguished"],
    "A2_remote_words": ["remote"],
    "A2_us_words": ["united states", "usa", "us", "u.s.", "u.s.a."],
    "A2_us_states": {
        "al": "alabama", "ak": "alaska", "az": "arizona", "ar": "arkansas", "ca": "california",
        "co": "colorado", "ct": "connecticut", "de": "delaware", "fl": "florida", "ga": "georgia",
        "hi": "hawaii", "id": "idaho", "il": "illinois", "in": "indiana", "ia": "iowa",
        "ks": "kansas", "ky": "kentucky", "la": "louisiana", "me": "maine", "md": "maryland",
        "ma": "massachusetts", "mi": "michigan", "mn": "minnesota", "ms": "mississippi",
        "mo": "missouri", "mt": "montana", "ne": "nebraska", "nv": "nevada",
        "nh": "new hampshire", "nj": "new jersey", "nm": "new mexico", "ny": "new york",
        "nc": "north carolina", "nd": "north dakota", "oh": "ohio", "ok": "oklahoma",
        "or": "oregon", "pa": "pennsylvania", "ri": "rhode island", "sc": "south carolina",
        "sd": "south dakota", "tn": "tennessee", "tx": "texas", "ut": "utah", "vt": "vermont",
        "va": "virginia", "wa": "washington", "wv": "west virginia", "wi": "wisconsin",
        "wy": "wyoming", "dc": "district of columbia", "d.c.": "district of columbia",
    },
    "A2_location_separators": r"[|;]",
    "A3_sponsorship_phrases": ["unable to sponsor", "not able to sponsor", "no visa sponsorship",
                               "without sponsorship now or in the future",
                               "u.s. citizenship required", "must be a u.s. citizen"],
    "A4_min_years": 3,
    "A4_years_pattern": r"(?<![a-z0-9])(\d+)\s*\+\s*years?(?![a-z0-9])",
    "A5_phd_required_pattern": (r"(?<![a-z0-9])(?:ph\.?\s?d\.?)(?:\s+degree)?\s+(?:is\s+)?required"
                                r"|(?<![a-z0-9])requires?\s+an?\s+ph\.?\s?d(?![a-z0-9])"),
    "A6_clearance_phrases": ["security clearance", "ts/sci", "secret clearance",
                             "clearance required"],
    "A7_unpaid_words": ["unpaid", "volunteer"],
    # Stage B — score
    "B1_title_phrases": ["machine learning", "ml engineer", "ai engineer", "applied ai", "nlp",
                         "llm", "research engineer"],
    "B1_points": 3,
    "B2_topic_words": ["pytorch", "transformers", "hugging face", "natural language", "nlp", "llm",
                       "large language model", "embeddings", "retrieval", "rag", "fine-tuning",
                       "inference", "mlops", "evaluation"],
    "B2_max": 5,
    "B3_skills": ["python", "pytorch", "sql", "transformers", "sentence-transformers", "fastapi",
                  "mlflow", "postgresql", "aws"],
    "B3_max": 4,
    "keep_threshold": 5,
}

STAGE_A = ("A1", "A2", "A3", "A4", "A5", "A6", "A7")

_TAG = re.compile(r"<[^>]+>")
_WHITESPACE = re.compile(r"\s+")
_PATTERNS = {}


def to_text(value) -> str:
    """Unescape entities, strip tags, unescape again (escaped HTML can carry escaped
    entities), collapse whitespace, lowercase. None and non-strings become ""."""
    if not isinstance(value, str):
        return ""
    text = _TAG.sub(" ", html.unescape(value))
    text = _TAG.sub(" ", html.unescape(text))
    return _WHITESPACE.sub(" ", text).strip().lower()


def _pattern(phrase: str) -> re.Pattern:
    if phrase not in _PATTERNS:
        words = [re.escape(w) for w in phrase.lower().split()]
        _PATTERNS[phrase] = re.compile(r"(?<![a-z0-9])" + r"\s+".join(words) + r"(?![a-z0-9])")
    return _PATTERNS[phrase]


def find(phrase: str, text: str):
    """The matched text of a whole-word phrase, or None."""
    match = _pattern(phrase).search(text)
    return match.group(0) if match else None


def _first(phrases, text):
    for phrase in phrases:
        found = find(phrase, text)
        if found:
            return found
    return None


def _location_name(location):
    """Normalized postings carry {"name": str}; plain strings are accepted too.
    Missing, empty or whitespace-only is None (never a default)."""
    if isinstance(location, dict):
        location = location.get("name")
    return location.strip() if isinstance(location, str) and location.strip() else None


def _us_or_remote_part(location_name: str):
    """The first location part that is remote or in the US, else None."""
    states = FILTER_V1["A2_us_states"]
    for part in re.split(FILTER_V1["A2_location_separators"], location_name):
        cleaned = to_text(part)
        if not cleaned:
            continue
        if _first(FILTER_V1["A2_remote_words"], cleaned) or _first(FILTER_V1["A2_us_words"], cleaned):
            return part.strip()
        last = cleaned.rsplit(",", 1)[-1].strip() if "," in cleaned else None
        if last and (last in states or last in states.values()):
            return part.strip()
    return None


def _stage_a(title: str, text: str, location_name):
    fired = {}
    found = _first(FILTER_V1["A1_title_seniority"], title)
    if found:
        fired["A1"] = found
    if location_name is not None and _us_or_remote_part(location_name) is None:
        fired["A2"] = location_name
    found = _first(FILTER_V1["A3_sponsorship_phrases"], text)
    if found:
        fired["A3"] = found
    for match in re.finditer(FILTER_V1["A4_years_pattern"], text):
        if int(match.group(1)) >= FILTER_V1["A4_min_years"]:
            fired["A4"] = match.group(0)
            break
    match = re.search(FILTER_V1["A5_phd_required_pattern"], text)
    if match:
        fired["A5"] = match.group(0)
    found = _first(FILTER_V1["A6_clearance_phrases"], text)
    if found:
        fired["A6"] = found
    found = _first(FILTER_V1["A7_unpaid_words"], text)
    if found:
        fired["A7"] = found
    return fired


def _distinct(words, text):
    return [w for w in words if find(w, text)]


def evaluate(posting: dict) -> dict:
    title = to_text(posting.get("title"))
    content = to_text(posting.get("content"))
    location_name = _location_name(posting.get("location"))
    # "Text" rules (A3-A7) read title and content; A1/B1 read the title; B2/B3 the content.
    text = f"{title} {content}".strip()

    b1_found = _first(FILTER_V1["B1_title_phrases"], title)
    components = {
        "B1": FILTER_V1["B1_points"] if b1_found else 0,
        "B2": _distinct(FILTER_V1["B2_topic_words"], content),
        "B3": _distinct(FILTER_V1["B3_skills"], content),
    }
    matched = _stage_a(title, text, location_name)
    if b1_found:
        matched["B1"] = b1_found
    rejected_by = [rule for rule in STAGE_A if rule in matched]

    def result(decision, score=None):
        return {"decision": decision, "rejected_by": rejected_by, "score": score,
                "components": components, "matched": matched}

    if rejected_by:
        return result("reject")
    if location_name is None or not content:
        return result("cannot_tell")
    score = (components["B1"]
             + min(len(components["B2"]), FILTER_V1["B2_max"])
             + min(len(components["B3"]), FILTER_V1["B3_max"]))
    return result("keep" if score >= FILTER_V1["keep_threshold"] else "reject", score)
