"""Prompt-contract validation for Assignment 01: a controlled prompt experiment.

Validates model-shaped responses against an explicit output contract:
JSON object with exactly the keys "answer" and "sources", a non-empty
string answer, and a non-empty list of source IDs drawn from the supplied
evidence set.

Starting point: lessons/02-prompt-contracts-and-evaluation/code/main.py in
nikbearbrown/info-7375-prompt-engineering-for-generative-ai (read 2026-10-10).
Deliberate differences from the reference:
  - validate() returns (ok, reason) instead of a bare bool, so every failure
    names its cause (json / schema / type / empty / source). is_valid()
    preserves the boolean interface.
  - pass_rate() returns (rate, failures) with per-response reasons, so the
    experiment can report *which* contract clause failed, not just a number.
  - render() fills a contract template with a question and evidence map;
    pure string templating, no model call.

What this establishes: format validity only. A response can pass every
check here while stating a falsehood, as long as the falsehood is well
formed and cites a real source ID. That boundary is the point of the
experiment, not a bug in it.
"""
import json

REQUIRED_KEYS = ("answer", "sources")


def validate(text, source_ids):
    """Check a response against the output contract.

    Returns (True, "ok") or (False, reason) where reason is one of:
    not-json, not-object, schema (wrong key set), type (wrong field type),
    empty (blank answer or empty sources), source (unknown source ID).
    """
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        return False, "not-json"
    if not isinstance(data, dict):
        return False, "not-object"
    if set(data.keys()) != set(REQUIRED_KEYS):
        return False, "schema: keys must be exactly %s" % (list(REQUIRED_KEYS),)
    if not isinstance(data["answer"], str):
        return False, "type: answer must be a string"
    if not data["answer"].strip():
        return False, "empty: answer must be non-blank"
    if not isinstance(data["sources"], list):
        return False, "type: sources must be a list"
    if not data["sources"]:
        return False, "empty: sources must be non-empty"
    for s in data["sources"]:
        if not isinstance(s, str) or s not in source_ids:
            return False, "source: unknown source id %r" % (s,)
    return True, "ok"


def is_valid(text, source_ids):
    """Boolean interface matching the lesson reference."""
    ok, _ = validate(text, source_ids)
    return ok


def pass_rate(responses, source_ids):
    """Format-pass rate plus a per-response failure breakdown.

    Returns (rate, failures) where failures is a list of
    {"index": i, "reason": reason} for each failing response.
    Raises ValueError on an empty experiment (a pass rate over nothing
    is undefined, not zero).
    """
    if not responses:
        raise ValueError("an empty experiment has no pass rate")
    failures = []
    passed = 0
    for i, r in enumerate(responses):
        ok, reason = validate(r, source_ids)
        if ok:
            passed += 1
        else:
            failures.append({"index": i, "reason": reason})
    return passed / len(responses), failures


def render(template, question, evidence):
    """Fill a prompt-contract template. Pure templating; no model is called."""
    lines = ["Evidence (source_id: text):"]
    for sid, text in evidence.items():
        lines.append("- %s: %s" % (sid, text))
    evidence_block = "\n".join(lines)
    return template.replace("{{QUESTION}}", question).replace(
        "{{EVIDENCE}}", evidence_block)
