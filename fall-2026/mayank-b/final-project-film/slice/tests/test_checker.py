import json
from pathlib import Path

import pytest

from source_check.checker import HOLD, PASS, check_answer, load_policies

DATA = Path(__file__).resolve().parents[1] / "data"
POLICIES = load_policies(DATA / "policies.json")
CASES = json.loads((DATA / "cases.json").read_text())


TODAY = "2026-10-25"  # pinned so the tests give the same answer on any day


def run(name, today=TODAY):
    return check_answer(CASES[name]["claims"], POLICIES, today)


def test_air_canada_shape_holds():
    d = run("air_canada_shape")
    assert d.verdict == HOLD
    assert "answer says 'after travel', policy says 'before travel'" in d.reasons[0]
    assert d.policy_lines == ["BRV-2026-03: Bereavement fares must be requested before travel. "
                              "They cannot be claimed after the trip."]


def test_within_90_days_vs_90_days_after_holds():
    d = run("within_vs_after")
    assert d.verdict == HOLD
    assert "policy says 'within 90 days of purchase'" in d.reasons[0]


def test_within_24h_of_booking_vs_24h_before_departure_holds():
    d = run("booking_vs_departure")
    assert d.verdict == HOLD
    assert "policy says 'within 24 hours of booking'" in d.reasons[0]


def test_matching_answer_passes_and_logs_version():
    d = run("matching_refund")
    assert d.verdict == PASS
    assert d.policy_version == "RFD-2026-01"


def test_outdated_version_holds():
    d = run("outdated_refund")
    assert d.verdict == HOLD
    assert "outdated version" in d.reasons[0]


def test_no_source_holds():
    assert run("no_source").verdict == HOLD


def test_broken_contract_holds():
    assert "breaks the contract" in run("broken_contract").reasons[0]


def test_no_claims_holds():
    assert check_answer([], POLICIES, TODAY).verdict == HOLD


def test_extra_field_breaks_the_contract():
    d = run("extra_field")
    assert d.verdict == HOLD
    assert "extra ['fee_waived']" in d.reasons[0]


def test_future_policy_is_ignored_until_its_date():
    assert run("matching_refund").verdict == PASS  # 90 days is still the rule today
    d = run("future_policy")  # 60 days only starts in March 2027
    assert d.verdict == HOLD
    assert "not in effect yet" in d.reasons[0]


def test_future_policy_applies_once_effective():
    later = "2027-04-01"
    assert run("future_policy", later).verdict == PASS
    assert run("future_policy", later).policy_version == "RFD-2027-03"
    assert "outdated version" in run("matching_refund", later).reasons[0]


def test_topic_with_only_a_future_version_holds():
    only_future = [dict(POLICIES[2], topic="pet fee")]
    d = check_answer(CASES["no_source"]["claims"], only_future, TODAY)
    assert d.verdict == HOLD
    assert "in effect yet" in d.reasons[0]


@pytest.mark.parametrize("name", sorted(k for k in CASES if not k.startswith("_")))
def test_every_case_matches_its_label(name):
    assert run(name).verdict == CASES[name]["expect"]
