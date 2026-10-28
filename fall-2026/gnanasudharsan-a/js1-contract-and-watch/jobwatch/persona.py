"""Load the résumé and refuse anything that is not the fictional persona shape.

CONTRACT.md "In": the résumé must pass a schema check before anything runs,
and the loader refuses any résumé whose email does not end in @example.com
or whose phone is not a 555 number.
"""
import json
import re
from pathlib import Path

import jsonschema

_STRING_LIST = {"type": "array", "items": {"type": "string"}}

RESUME_SCHEMA = {
    "type": "object",
    "required": [
        "personal",
        "skills",
        "target_roles",
        "willing_to_relocate_us",
        "needs_sponsorship",
    ],
    "properties": {
        "personal": {
            "type": "object",
            # email and phone are required so the refusal check always has input.
            "required": ["name", "email", "phone"],
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "email": {"type": "string"},
                "phone": {"type": "string"},
            },
        },
        "skills": {
            "type": "object",
            "required": [
                "languages",
                "ml_nlp",
                "backend_automation",
                "database_cloud",
                "familiar_with_not_shipped",
            ],
            "properties": {
                "languages": _STRING_LIST,
                "ml_nlp": _STRING_LIST,
                "backend_automation": _STRING_LIST,
                "database_cloud": _STRING_LIST,
                "familiar_with_not_shipped": _STRING_LIST,
            },
        },
        "target_roles": {**_STRING_LIST, "minItems": 1},
        "willing_to_relocate_us": {"type": "boolean"},
        "needs_sponsorship": {"type": "boolean"},
    },
}


class PersonaRefused(ValueError):
    """The résumé failed the schema check or looks like real personal data."""


def _is_555_number(phone: str) -> bool:
    # A NANP number whose exchange (digits 4-6, after an optional leading 1) is 555.
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return len(digits) == 10 and digits[3:6] == "555"


def validate_persona(resume: dict) -> dict:
    try:
        jsonschema.validate(resume, RESUME_SCHEMA)
    except jsonschema.ValidationError as exc:
        raise PersonaRefused(f"résumé failed schema check: {exc.message}") from exc

    email = resume["personal"]["email"].strip().lower()
    if not email.endswith("@example.com"):
        raise PersonaRefused("refusing résumé: email does not end in @example.com")
    if not _is_555_number(resume["personal"]["phone"]):
        raise PersonaRefused("refusing résumé: phone is not a 555 number")
    return resume


def load_persona(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return validate_persona(json.load(f))
