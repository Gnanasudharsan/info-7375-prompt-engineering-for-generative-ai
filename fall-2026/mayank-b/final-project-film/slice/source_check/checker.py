"""Source Check, first slice: the deterministic checker.

Claude's job (not built yet) is to turn a bot's answer into claims that follow
CLAIM_FIELDS. This module decides PASS or HOLD with plain code: it never asks a
model whether an answer is right. Anything it cannot verify is a HOLD.
"""
import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import List, Optional

PASS, HOLD = "PASS", "HOLD"

# The prompt contract: every claim must carry exactly these fields.
CLAIM_FIELDS = {"topic", "relation", "amount", "unit", "anchor"}
RELATIONS = {"before", "after", "within"}


@dataclass
class Decision:
    verdict: str
    reasons: List[str] = field(default_factory=list)
    policy_version: Optional[str] = None
    policy_lines: List[str] = field(default_factory=list)


def load_policies(path):
    return json.loads(Path(path).read_text())


def current_version(policies, topic, today):
    """The version in effect on `today` (ISO date): the newest one already effective, or None.
    A version dated in the future is ignored until its date arrives."""
    versions = [p for p in policies if p["topic"] == topic and p["effective"] <= today]
    return max(versions, key=lambda p: p["effective"]) if versions else None


def _condition(rule):
    return (rule["relation"], rule["amount"], rule["unit"], rule["anchor"])


def _say(c):
    relation, amount, unit, anchor = c
    if relation == "within":
        return f"within {amount} {unit} of {anchor}"
    return f"{amount} {unit} {relation} {anchor}" if amount else f"{relation} {anchor}"


def check_claim(claim, policies, today):
    """Return (ok, reason, policy) for one claim, judged against the policy in effect on `today`."""
    missing = CLAIM_FIELDS - set(claim)
    extra = set(claim) - CLAIM_FIELDS
    if missing or extra or claim.get("relation") not in RELATIONS:
        return False, (f"claim breaks the contract (missing {sorted(missing)}, extra {sorted(extra)}, "
                       f"relation {claim.get('relation')!r})"), None

    policy = current_version(policies, claim["topic"], today)
    if policy is None:
        if any(p["topic"] == claim["topic"] for p in policies):
            return False, f"no version of the '{claim['topic']}' policy is in effect yet", None
        return False, f"no policy covers '{claim['topic']}'", None

    said = _condition(claim)
    if said == _condition(policy):
        return True, "matches the current policy", policy

    others = [p for p in policies if p["topic"] == claim["topic"] and p is not policy]
    if any(said == _condition(p) for p in others if p["effective"] < policy["effective"]):
        return False, f"matches an outdated version, not {policy['version']}", policy
    if any(said == _condition(p) for p in others if p["effective"] > today):
        return False, f"matches a version not in effect yet, not {policy['version']}", policy

    return False, f"answer says '{_say(said)}', policy says '{_say(_condition(policy))}'", policy


def check_answer(claims, policies, today=None):
    """PASS only if the answer has claims and every claim matches the policy in effect on `today`
    (an ISO date string; defaults to the real date)."""
    today = today or date.today().isoformat()
    if not claims:
        return Decision(HOLD, ["no claims extracted, so nothing to verify"])
    reasons, lines, versions = [], [], []
    ok_all = True
    for claim in claims:
        ok, reason, policy = check_claim(claim, policies, today)
        ok_all = ok_all and ok
        if not ok:
            reasons.append(reason)
        if policy:
            lines.append(f"{policy['version']}: {policy['line']}")
            versions.append(policy["version"])
    return Decision(PASS if ok_all else HOLD, reasons, ", ".join(sorted(set(versions))) or None, lines)
