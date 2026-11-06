"""The rule judge. Implements CONTRACT.md "The rule" and its "Out" justification.

Deterministic: the same posting and persona always give the same record,
so the verdict is labeled "record (recomputable)".
"""
import html
import re

RULE_LABEL = "record (recomputable)"

# Lists fixed by CONTRACT.md "The rule"; everything else is read from the persona.
SENIORITY_WORDS = ("senior", "lead", "staff", "principal", "manager", "director",
                   "vp", "head", "distinguished")
US_STATE_CODES = (
    "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga", "hi", "id", "il", "in",
    "ia", "ks", "ky", "la", "me", "md", "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv",
    "nh", "nj", "nm", "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn",
    "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy",
)
US_SUFFIXES = tuple(f", {code}" for code in ("dc",) + US_STATE_CODES)
REMOTE_PREFIXES = ("remote-friendly", "remote")
NEGATIVE_SPONSORSHIP = "not currently able to sponsor"
MIN_SKILLS = 2  # CONTRACT.md Amendment 1 (was 3)
# skills.* keys that never count as shipped skills (CONTRACT.md condition 5).
IGNORED_SKILL_KEYS = ("familiar_with_not_shipped", "agent_note")

_TAG = re.compile(r"<[^>]+>")
_WHITESPACE = re.compile(r"\s+")


def html_to_text(content: str) -> str:
    """Unescape HTML entities twice, then strip tags. Case is preserved."""
    text = html.unescape(html.unescape(content or ""))
    text = _TAG.sub(" ", text)
    return _WHITESPACE.sub(" ", text).strip()


def clean_content(content: str) -> str:
    return html_to_text(content).lower()


def clean_title(title: str) -> str:
    return (title or "").strip().lower()


def _phrase_pattern(phrase: str) -> re.Pattern:
    # Whole-word/phrase match: no letter or digit directly before or after,
    # and any whitespace run between the words of a phrase.
    words = [re.escape(word) for word in phrase.lower().split()]
    return re.compile(r"(?<![a-z0-9])" + r"\s+".join(words) + r"(?![a-z0-9])")


def _find(phrase: str, text: str):
    match = _phrase_pattern(phrase).search(text)
    return match.group(0) if match else None


def _check_title(title: str, persona: dict) -> dict:
    matches = []
    for role in persona["target_roles"]:
        found = _find(role, title)
        if found:
            matches.append({"target_role": role, "matched_phrase": found})
    return {"field": "title", "passed": bool(matches), "matches": matches}


def _check_seniority(title: str) -> dict:
    found = [word for word in SENIORITY_WORDS if _find(word, title)]
    return {"field": "title", "passed": not found, "excluded_words_found": found}


def _check_location(location_name: str) -> dict:
    for part in re.split(r"[|;]", location_name or ""):
        cleaned = part.strip().lower()
        if "united states" in cleaned:
            rule = 'contains "united states"'
        elif cleaned.endswith(US_SUFFIXES):
            rule = f'ends with "{cleaned[cleaned.rfind(","):]}"'
        elif cleaned.startswith(REMOTE_PREFIXES):
            rule = f'starts with "{next(p for p in REMOTE_PREFIXES if cleaned.startswith(p))}"'
        else:
            continue
        return {"field": "location.name", "passed": True,
                "matched_part": part.strip(), "matched_by": rule}
    return {"field": "location.name", "passed": False, "matched_part": None,
            "matched_by": None, "value": location_name}


def _check_sponsorship(content: str) -> dict:
    found = _find(NEGATIVE_SPONSORSHIP, content) is not None
    result = (f'negative phrase "{NEGATIVE_SPONSORSHIP}" found' if found
              else f'negative phrase "{NEGATIVE_SPONSORSHIP}" not found')
    return {"field": "content", "passed": not found,
            "negative_phrase_found": found, "result": result}


def shipped_skills(persona: dict):
    """(skill, résumé path) pairs for every shipped skill in the persona."""
    for key, values in persona["skills"].items():
        if key in IGNORED_SKILL_KEYS or not isinstance(values, list):
            continue
        for skill in values:
            yield skill, f"skills.{key}"


def _check_skills(content: str, persona: dict) -> dict:
    matched, seen = [], set()
    for skill, path in shipped_skills(persona):
        if skill.lower() in seen:
            continue
        if _find(skill, content):
            seen.add(skill.lower())
            matched.append({"skill": skill, "resume_path": path})
    return {"field": "content", "passed": len(matched) >= MIN_SKILLS,
            "matched": matched, "distinct_count": len(matched), "required": MIN_SKILLS}


def _summary(checks: dict, failed: list) -> str:
    title, location, skills = checks["title"], checks["location"], checks["skills"]
    parts = [
        "title: " + (", ".join(f'"{m["matched_phrase"]}"' for m in title["matches"])
                     or "no target role matched"),
        "seniority: " + (", ".join(checks["seniority"]["excluded_words_found"])
                         or "no excluded word"),
        "location.name: " + (f'"{location["matched_part"]}" ({location["matched_by"]})'
                             if location["passed"] else "no US or remote part"),
        "content sponsorship: " + checks["sponsorship"]["result"],
        f"skills ({skills['distinct_count']}/{skills['required']}): "
        + (", ".join(f'{m["skill"]} [{m["resume_path"]}]' for m in skills["matched"])
           or "none"),
    ]
    if failed:
        parts.append("failed: " + ", ".join(failed))
    return "; ".join(parts)


def judge_posting(posting: dict, persona: dict) -> dict:
    title = clean_title(posting.get("title"))
    content = clean_content(posting.get("content"))
    location_name = (posting.get("location") or {}).get("name") or ""

    checks = {
        "title": _check_title(title, persona),
        "seniority": _check_seniority(title),
        "location": _check_location(location_name),
        "sponsorship": _check_sponsorship(content),
        "skills": _check_skills(content, persona),
    }
    failed = [name for name, check in checks.items() if not check["passed"]]
    justification = {**checks, "failed_conditions": failed,
                     "summary": _summary(checks, failed)}
    return {
        "verdict": "NOT_RELEVANT" if failed else "RELEVANT",
        "label": RULE_LABEL,
        "justification": justification,
    }
