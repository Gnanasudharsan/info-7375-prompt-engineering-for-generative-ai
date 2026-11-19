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

# FILTER.md "v1.1 — proposed changes": each switch is off unless named in evaluate(changes=...).
FILTER_V1_1 = {
    "version": "1.1",
    "switches": ("C1", "C2", "C3", "C4"),
    # C1 — A3 also rejects these citizenship phrases, and "US" without dots
    # (the no-dot form is applied to the v1.0 citizenship phrases too).
    "C1_citizenship_phrases": ["verification of u.s. citizenship", "u.s. citizens only",
                               "requires u.s. citizenship",
                               "verification of us citizenship", "us citizens only",
                               "requires us citizenship",
                               "us citizenship required", "must be a us citizen"],
    # C2 — A6 fires only for a clearance phrase with no negation within the window
    # (characters of cleaned text, on either side of the phrase).
    "C2_negations": ["not", "no", "do not", "most do not"],
    "C2_window_chars": 120,
    # C3 — a would-be keep becomes cannot_tell without a title level word or a numeric
    # experience statement. Anthropic's deferral sentence is removed before searching.
    "C3_title_level_words": ["senior", "sr", "staff", "principal", "lead", "manager", "director",
                             "head", "vp", "distinguished", "junior", "jr", "entry level",
                             "entry-level", "new grad", "new graduate", "graduate", "intern",
                             "internship", "associate", "early career", "i", "ii", "iii"],
    # Explicit level phrases in the text count as a level statement, like a numeric one.
    "C3_text_level_phrases": ["new grad", "new grads", "new graduate", "new graduates",
                              "entry-level", "early career", "junior"],
    "C3_numeric_experience_pattern": (r"(?<![a-z0-9])\d+\s*(?:\+|(?:-|–|—|to)\s*\d+\s*\+?)?\s*"
                                      r"(?:years?|yrs?)(?![a-z0-9])"),
    "C3_deferral_pattern": (r"years of experience required will correlate with the internal "
                            r"job level requirements for the position\.?"),
    # C4 — keep requires B1 > 0.
    "C4_min_b1": 1,
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


def _negated(text: str, start: int, end: int) -> bool:
    window = FILTER_V1_1["C2_window_chars"]
    before, after = text[max(0, start - window):start], text[end:end + window]
    return any(find(word, before) or find(word, after) for word in FILTER_V1_1["C2_negations"])


def _clearance_c2(text: str):
    """C2: the first clearance phrase occurrence (list order, then position) with no
    negation within the window; None if every occurrence is negated."""
    for phrase in FILTER_V1["A6_clearance_phrases"]:
        for match in _pattern(phrase).finditer(text):
            if not _negated(text, match.start(), match.end()):
                return match.group(0)
    return None


def _has_level_signal(title: str, text: str) -> bool:
    """C3: a level word in the title, or a level statement in the text other than the
    deferral sentence: a numeric experience statement or an explicit level phrase."""
    if _first(FILTER_V1_1["C3_title_level_words"], title):
        return True
    without_deferral = re.sub(FILTER_V1_1["C3_deferral_pattern"], " ", text)
    if re.search(FILTER_V1_1["C3_numeric_experience_pattern"], without_deferral):
        return True
    return _first(FILTER_V1_1["C3_text_level_phrases"], without_deferral) is not None


def _stage_a(title: str, text: str, location_name, changes=frozenset()):
    fired = {}
    found = _first(FILTER_V1["A1_title_seniority"], title)
    if found:
        fired["A1"] = found
    if location_name is not None and _us_or_remote_part(location_name) is None:
        fired["A2"] = location_name
    found = _first(FILTER_V1["A3_sponsorship_phrases"], text)
    if not found and "C1" in changes:
        found = _first(FILTER_V1_1["C1_citizenship_phrases"], text)
    if found:
        fired["A3"] = found
    for match in re.finditer(FILTER_V1["A4_years_pattern"], text):
        if int(match.group(1)) >= FILTER_V1["A4_min_years"]:
            fired["A4"] = match.group(0)
            break
    match = re.search(FILTER_V1["A5_phd_required_pattern"], text)
    if match:
        fired["A5"] = match.group(0)
    found = (_clearance_c2(text) if "C2" in changes
             else _first(FILTER_V1["A6_clearance_phrases"], text))
    if found:
        fired["A6"] = found
    found = _first(FILTER_V1["A7_unpaid_words"], text)
    if found:
        fired["A7"] = found
    return fired


def _distinct(words, text):
    return [w for w in words if find(w, text)]


def _check_changes(changes) -> frozenset:
    changes = frozenset(changes or ())
    unknown = changes - set(FILTER_V1_1["switches"])
    if unknown:
        raise ValueError(f"unknown v1.1 switch(es): {sorted(unknown)}; "
                         f"allowed {list(FILTER_V1_1['switches'])}")
    return changes


def evaluate(posting: dict, changes=frozenset()) -> dict:
    changes = _check_changes(changes)
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
    matched = _stage_a(title, text, location_name, changes)
    if b1_found:
        matched["B1"] = b1_found
    rejected_by = [rule for rule in STAGE_A if rule in matched]

    def result(decision, score=None):
        return {"decision": decision, "rejected_by": rejected_by, "score": score,
                "components": components, "matched": matched, "changes": sorted(changes)}

    if rejected_by:
        return result("reject")
    if location_name is None or not content:
        return result("cannot_tell")
    score = (components["B1"]
             + min(len(components["B2"]), FILTER_V1["B2_max"])
             + min(len(components["B3"]), FILTER_V1["B3_max"]))
    if score < FILTER_V1["keep_threshold"]:
        return result("reject", score)
    if "C4" in changes and components["B1"] < FILTER_V1_1["C4_min_b1"]:
        return result("reject", score)
    if "C3" in changes and not _has_level_signal(title, text):
        return result("cannot_tell", score)
    return result("keep", score)
