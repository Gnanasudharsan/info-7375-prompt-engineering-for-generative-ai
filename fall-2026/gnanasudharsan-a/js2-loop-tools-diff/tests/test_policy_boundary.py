"""Boundary tests for GATE §6, cases B1-B16 from BOUNDARY_TESTS.md.
Written by me before jobwatch/policy.py existed. Expected to FAIL on first run.
A refusal must be PolicyViolation specifically, so a crash is never mistaken for a refusal."""
import pytest
from jobwatch.policy import Policy, PolicyViolation


@pytest.fixture
def root(tmp_path):
    r = tmp_path / "project"
    for d in ["runs", "state", "persona", "prompts"]:
        (r / d).mkdir(parents=True)
    (r / "persona" / "ananya-rao.resume.json").write_text("{}")
    (r / "state" / "seen_ids.json").write_text("[]")
    (r / "runs-evil").mkdir()                      # B9: sibling folder sharing the "runs" prefix
    outside = tmp_path / "outside"
    outside.mkdir()
    (r / "runs" / "link").symlink_to(outside, target_is_directory=True)   # B10
    js1 = tmp_path / "js1-contract-and-watch"
    js1.mkdir()
    (js1 / "CONTRACT.md").write_text("x")          # B16 target, outside root
    return r


@pytest.fixture
def policy(root):
    return Policy(root)


URL_CASES = [
    ("B1",  "GET",  "https://api.lever.co/v0/postings/spotify?mode=json",          "ALLOW"),
    ("B2",  "GET",  "https://api.lever.co.evil.com/v0/postings/x",                  "REFUSE"),
    ("B3",  "GET",  "https://evilapi.lever.co/v0/postings/x",                       "REFUSE"),
    ("B4",  "GET",  "https://example.com/jobs",                                     "REFUSE"),
    ("B5",  "GET",  "http://api.lever.co/v0/postings/spotify",                      "REFUSE"),
    ("B6",  "POST", "https://boards-api.greenhouse.io/v1/boards/anthropic/jobs",    "REFUSE"),
]

PATH_CASES = [
    ("B7",  "write", "runs/2026-11-06T1800Z/trace.jsonl",          "ALLOW"),
    ("B8",  "write", "runs/../persona/ananya-rao.resume.json",     "REFUSE"),
    ("B9",  "write", "runs-evil/trace.jsonl",                      "REFUSE"),
    ("B10", "write", "runs/link/x.json",                           "REFUSE"),
    ("B11", "write", "/tmp/x.json",                                "REFUSE"),
    ("B12", "read",  "persona/ananya-rao.resume.json",             "ALLOW"),
    ("B13", "write", "persona/ananya-rao.resume.json",             "REFUSE"),
    ("B16", "read",  "../js1-contract-and-watch/CONTRACT.md",      "REFUSE"),
]


@pytest.mark.parametrize("case,method,url,expected", URL_CASES, ids=[c[0] for c in URL_CASES])
def test_url_boundary(policy, case, method, url, expected):
    if expected == "ALLOW":
        policy.check_url(url, method=method)
    else:
        with pytest.raises(PolicyViolation):
            policy.check_url(url, method=method)


@pytest.mark.parametrize("case,mode,path,expected", PATH_CASES, ids=[c[0] for c in PATH_CASES])
def test_path_boundary(policy, case, mode, path, expected):
    if expected == "ALLOW":
        policy.check_path(path, mode)
    else:
        with pytest.raises(PolicyViolation):
            policy.check_path(path, mode)


def test_B14_delete_state_without_approval_refused(policy):
    with pytest.raises(PolicyViolation):
        policy.check_delete("state/seen_ids.json", approved=False)


def test_B15_delete_state_with_approval_allowed(policy):
    policy.check_delete("state/seen_ids.json", approved=True)
