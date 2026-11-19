"""Filter tests for FILTER.md v1.0 (rules A1-A7, B1-B3, threshold 5, abstention, wrong versions W1-W5).
Written by me before jobwatch/filter.py existed; expected to FAIL on first run (no module)."""
import pytest
from jobwatch.filter import evaluate

GOOD = ("<p>Build LLM retrieval and evaluation pipelines in Python and PyTorch with "
        "Hugging Face transformers, served with FastAPI on AWS.</p>")


def P(title="Machine Learning Engineer", location="San Francisco, CA", content=GOOD):
    return {"title": title, "location": location, "content": content, "departments": None}


def test_good_posting_is_kept():
    r = evaluate(P())
    assert r["decision"] == "keep" and r["score"] >= 5


# --- Stage A hard rejects --------------------------------------------------------

@pytest.mark.parametrize("title", ["Senior Machine Learning Engineer", "Sr. ML Engineer",
                                   "Staff AI Engineer", "ML Engineering Manager", "Tech Lead, NLP"])
def test_A1_seniority_title_rejects(title):
    r = evaluate(P(title=title))
    assert r["decision"] == "reject" and "A1" in r["rejected_by"]


def test_A2_non_us_location_rejects():
    r = evaluate(P(location="London, UK"))
    assert r["decision"] == "reject" and "A2" in r["rejected_by"]


@pytest.mark.parametrize("loc", ["San Francisco, California", "New York, NY", "Remote", "Remote - US",
                                 "Boston, MA | Remote"])
def test_A2_us_or_remote_passes_including_ashby_city_state(loc):
    """'San Francisco, California' is the Ashby format the JS1 rule missed."""
    assert "A2" not in evaluate(P(location=loc))["rejected_by"]


@pytest.mark.parametrize("text", ["We are unable to sponsor visas for this role.",
                                  "No visa sponsorship is available.",
                                  "U.S. citizenship required.",
                                  "Candidates must be a U.S. citizen."])
def test_A3_sponsorship_or_citizenship_disclaimer_rejects(text):
    r = evaluate(P(content=GOOD + f"<p>{text}</p>"))
    assert r["decision"] == "reject" and "A3" in r["rejected_by"]


def test_A3_silence_or_offer_does_not_reject():
    assert "A3" not in evaluate(P(content=GOOD + "<p>We sponsor visas.</p>"))["rejected_by"]


@pytest.mark.parametrize("text,rejects", [("5+ years of experience in ML", True),
                                          ("3+ years of industry experience", True),
                                          ("1-3 years of experience", False),
                                          ("2+ years of experience", False)])
def test_A4_years_rule_and_wrong_version_W4(text, rejects):
    r = evaluate(P(content=GOOD + f"<p>{text}</p>"))
    assert ("A4" in r["rejected_by"]) is rejects


@pytest.mark.parametrize("text,rejects", [("A PhD is required.", True), ("PhD preferred.", False)])
def test_A5_phd_required_only(text, rejects):
    assert ("A5" in evaluate(P(content=GOOD + f"<p>{text}</p>"))["rejected_by"]) is rejects


def test_A6_clearance_rejects():
    r = evaluate(P(content=GOOD + "<p>Active TS/SCI security clearance required.</p>"))
    assert r["decision"] == "reject" and "A6" in r["rejected_by"]


def test_A7_unpaid_rejects():
    r = evaluate(P(content=GOOD + "<p>This is an unpaid volunteer position.</p>"))
    assert r["decision"] == "reject" and "A7" in r["rejected_by"]


# --- Stage B score and threshold ----------------------------------------------------

def test_score_components_and_threshold():
    r = evaluate(P(content="<p>We use Python and SQL.</p>"))   # B1 3 + B2 0 + B3 2 = 5
    assert r["score"] == 5 and r["decision"] == "keep"
    r = evaluate(P(content="<p>We use Python.</p>"))           # 3 + 0 + 1 = 4
    assert r["score"] == 4 and r["decision"] == "reject" and r["rejected_by"] == []


def test_html_escaped_content_is_read():
    """Greenhouse sends HTML-escaped content."""
    r = evaluate(P(content="&lt;p&gt;PyTorch and Python&lt;/p&gt;"))
    assert "pytorch" in r["components"]["B3"] and "python" in r["components"]["B3"]


# --- Abstention -------------------------------------------------------------------

@pytest.mark.parametrize("posting", [P(location=None), P(content=None), P(content="   ")],
                         ids=["no-location", "no-content", "blank-content"])
def test_missing_fields_give_cannot_tell_not_a_guess_W3(posting):
    r = evaluate(posting)
    assert r["decision"] == "cannot_tell" and r["score"] is None


def test_hard_reject_still_wins_over_missing_location():
    assert evaluate(P(title="Senior ML Engineer", location=None))["decision"] == "reject"


# --- Wrong versions -----------------------------------------------------------------

def test_W1_whole_words_not_substrings():
    r = evaluate(P(title="HTML Engineer", content="<p>Email templates, xml feeds, leading brands, maintain sites.</p>"))
    assert r["components"]["B1"] == 0          # "ml engineer" must not match inside "html engineer"
    assert "A1" not in r["rejected_by"]         # "leading" is not "lead"
    assert r["decision"] == "reject"


def test_W2_repetition_cannot_beat_the_caps():
    r = evaluate(P(content="<p>" + "python " * 30 + "</p>"))
    assert r["components"]["B3"] == ["python"] and r["score"] == 4


def test_W5_title_alone_is_not_enough():
    r = evaluate(P(content="<p>Own the sales pipeline and close enterprise deals.</p>"))
    assert r["score"] == 3 and r["decision"] == "reject"
