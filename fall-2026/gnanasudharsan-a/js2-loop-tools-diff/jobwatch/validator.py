"""Strict validator for the Claude judge's reply. CONTRACT.md "Out" and "Refuses".

Accepts only a bare JSON object with exactly the five contract keys. Anything
else raises ValidationFailed; the caller retries once, then records
judgment_unavailable.

Field paths use dots; list elements are addressed without an index
(departments.name means the name of any department).
"""
import json

REQUIRED_KEYS = frozenset({"id", "verdict", "reasoning",
                           "resume_fields_cited", "posting_fields_cited"})
VERDICTS = ("RELEVANT", "NOT_RELEVANT")

# From CONTRACT.md "In" (the required résumé fields) plus the persona's other
# content sections. Contact details and skills.agent_note are not citable.
RESUME_FIELD_PATHS = frozenset({
    "personal.name",
    "personal.location",
    "education",
    "experience",
    "projects",
    "skills.languages",
    "skills.ml_nlp",
    "skills.backend_automation",
    "skills.database_cloud",
    "skills.familiar_with_not_shipped",
    "target_roles",
    "willing_to_relocate_us",
    "needs_sponsorship",
})

# Fields present on real postings from boards-api.greenhouse.io/v1/boards/anthropic/jobs
# (checked against data/raw/anthropic_20261028T192103Z.json) that carry evidence.
POSTING_FIELD_PATHS = frozenset({
    "title",
    "location.name",
    "content",
    "departments.name",
    "offices.name",
    "offices.location",
    "metadata.value",
    "updated_at",
    "first_published",
})


class ValidationFailed(ValueError):
    """The reply is not an acceptable Claude verdict."""


def _check_citations(output: dict, key: str, known: frozenset) -> None:
    cited = output[key]
    if not isinstance(cited, list):
        raise ValidationFailed(f"{key} is not an array")
    if not cited:
        raise ValidationFailed(f"{key} is empty")
    unknown = [c for c in cited if not isinstance(c, str) or c not in known]
    if unknown:
        raise ValidationFailed(f"{key} has unknown field path(s): {unknown!r}")


def validate(text: str, expected_id: int) -> dict:
    """Return the parsed verdict, or raise ValidationFailed naming the reason."""
    try:
        output = json.loads(text)
    except (json.JSONDecodeError, TypeError) as exc:
        if isinstance(text, str) and "{" in text:
            raise ValidationFailed(f"text around the JSON object or broken JSON: {exc}") from exc
        raise ValidationFailed(f"not JSON: {exc}") from exc
    if not isinstance(output, dict):
        raise ValidationFailed(f"not a JSON object: {type(output).__name__}")

    keys = set(output)
    if keys != REQUIRED_KEYS:
        missing, extra = sorted(REQUIRED_KEYS - keys), sorted(keys - REQUIRED_KEYS)
        raise ValidationFailed(f"wrong keys: missing {missing}, extra {extra}")

    if output["verdict"] not in VERDICTS or not isinstance(output["verdict"], str):
        raise ValidationFailed(f"verdict must be RELEVANT or NOT_RELEVANT, got {output['verdict']!r}")
    # bool is an int subclass; True must not pass for id 1.
    if (isinstance(output["id"], bool) or not isinstance(output["id"], int)
            or output["id"] != expected_id):
        raise ValidationFailed(f"id {output['id']!r} does not match posting id {expected_id!r}")
    if not isinstance(output["reasoning"], str):
        raise ValidationFailed("reasoning is not a string")

    _check_citations(output, "resume_fields_cited", RESUME_FIELD_PATHS)
    _check_citations(output, "posting_fields_cited", POSTING_FIELD_PATHS)
    return output
