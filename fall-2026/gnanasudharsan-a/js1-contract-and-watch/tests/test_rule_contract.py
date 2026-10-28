"""Rule tests derived from CONTRACT.md, written 2026-10-28 BEFORE any rule code existed.
Cases and expected verdicts: from my CONTRACT.md. File drafted with help from a Claude chat.
All postings below are CONSTRUCTED (not real board data)."""
import copy
import json
from pathlib import Path

from jobwatch.rule import judge_posting

ROOT = Path(__file__).resolve().parent.parent
PERSONA = json.loads((ROOT / "persona" / "ananya-rao.resume.json").read_text())

POSITIVE_BOILERPLATE = (
    "Visa sponsorship: We do sponsor visas! However, we aren't able to "
    "successfully sponsor visas for every role and every candidate"
)
NEGATIVE_FELLOWS = "We are not currently able to sponsor visas for fellows"

# Satisfies all five conditions: target-role phrase, no seniority word,
# US location, no negative sponsorship phrase, 3 distinct shipped skills
# (python, pytorch, aws).
CONTROL = {
    "id": 9000001,
    "title": "Machine Learning Engineer, Applied NLP",
    "location": {"name": "San Francisco, CA"},
    "content": POSITIVE_BOILERPLATE
    + " You will build retrieval systems in Python and PyTorch and deploy them on AWS.",
    "departments": [{"name": "Engineering"}],
    "updated_at": "2026-10-28T00:00:00-04:00",
}


def judge(p):
    return judge_posting(p, PERSONA)


def test_control_posting_is_relevant():
    # Guards against an implementation that always says NOT_RELEVANT.
    assert judge(CONTROL)["verdict"] == "RELEVANT"


def test_control_justification_is_not_empty():
    # Contract "Out": the rule verdict's justification must cite fields.
    assert judge(CONTROL)["justification"]


def test_rejects_senior_titles():
    # Wrong version 1 (CONTRACT.md): lax_seniority_matcher
    p = copy.deepcopy(CONTROL)
    p["title"] = "Senior AI Engineer"
    assert judge(p)["verdict"] == "NOT_RELEVANT"


def test_respects_negative_sponsorship_boilerplate():
    # Wrong version 2 (CONTRACT.md): ignoring_sponsorship_trap, BOTH phrases present
    p = copy.deepcopy(CONTROL)
    p["content"] = CONTROL["content"] + " " + NEGATIVE_FELLOWS
    assert judge(p)["verdict"] == "NOT_RELEVANT"


def test_irish_location_is_not_us():
    # Condition 3 trap: ", ie" looks like a 2-letter state code
    p = copy.deepcopy(CONTROL)
    p["location"] = {"name": "Dublin, IE"}
    assert judge(p)["verdict"] == "NOT_RELEVANT"


def test_not_shipped_skills_do_not_count():
    # Condition 5: Kubernetes and Ray are familiar_with_not_shipped; only 1 shipped skill left
    p = copy.deepcopy(CONTROL)
    p["content"] = POSITIVE_BOILERPLATE + " You will run Python services on Kubernetes and Ray."
    assert judge(p)["verdict"] == "NOT_RELEVANT"


def test_ai_in_sales_title_is_not_a_role_match():
    # Condition 1 trap: "AI" in a non-engineering title
    p = copy.deepcopy(CONTROL)
    p["title"] = "Account Executive, AI Native"
    assert judge(p)["verdict"] == "NOT_RELEVANT"
