"""Tests for the FILTER.md v1.1 switches C1-C4, written before the code; each switch alone, v1.0 behavior unchanged when off."""
import pytest
from jobwatch.filter import evaluate
from tests.test_filter import P, GOOD

DEFER = "<p>Minimum years of experience: Years of experience required will correlate with the internal job level requirements for the position.</p>"
FALSE_FRIEND = "<p>Some portfolios require eligibility for a US security clearance, though most do not.</p>"
REAL_CLEARANCE = "<p>Experience deploying software on government networks Active federal security clearance (Secret or above) This position requires verification of U.S. citizenship due to citizenship-based legal restrictions.</p>"


def test_switches_off_is_v1_0():
    assert evaluate(P()) == evaluate(P(), changes=frozenset())


# C1 — widen A3
@pytest.mark.parametrize("text", ["This position requires verification of U.S. citizenship.",
                                  "Open to U.S. citizens only.", "This role requires US citizenship."])
def test_C1_citizenship_wording_rejects_only_with_switch(text):
    post = P(content=GOOD + f"<p>{text}</p>")
    assert "A3" not in evaluate(post)["rejected_by"]
    r = evaluate(post, changes={"C1"})
    assert r["decision"] == "reject" and "A3" in r["rejected_by"]


# C2 — narrow A6
def test_C2_negated_clearance_no_longer_fires():
    post = P(content=GOOD + FALSE_FRIEND)
    assert "A6" in evaluate(post)["rejected_by"]
    assert "A6" not in evaluate(post, changes={"C2"})["rejected_by"]


def test_C2_real_clearance_still_fires():
    assert "A6" in evaluate(P(content=GOOD + REAL_CLEARANCE), changes={"C2"})["rejected_by"]


# C3 — abstain when the only experience statement is the deferral
def test_C3_deferral_only_keep_becomes_cannot_tell():
    post = P(title="Research Engineer, Pretraining", content=GOOD + DEFER)
    assert evaluate(post)["decision"] == "keep"
    r = evaluate(post, changes={"C3"})
    assert r["decision"] == "cannot_tell"


@pytest.mark.parametrize("extra", ["<p>1-2 years of experience is fine.</p>", "<p>New grads welcome.</p>"])
def test_C3_a_real_level_statement_still_keeps(extra):
    assert evaluate(P(content=GOOD + DEFER + extra), changes={"C3"})["decision"] == "keep"


def test_C3_does_not_touch_rejects():
    assert evaluate(P(title="Senior ML Engineer", content=GOOD + DEFER), changes={"C3"})["decision"] == "reject"


# C4 — require a B1 title role phrase
def test_C4_content_only_keep_is_rejected():
    post = P(title="Research Scientist, Discovery")
    assert evaluate(post)["decision"] == "keep"
    r = evaluate(post, changes={"C4"})
    assert r["decision"] == "reject" and r["components"]["B1"] == 0


def test_C4_title_role_still_keeps():
    assert evaluate(P(), changes={"C4"})["decision"] == "keep"
