"""Offline tests for Step 2 (the watch). Fixtures under tests/fixtures/ are constructed."""
import copy
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from jobwatch import fetcher
from jobwatch.__main__ import main
from jobwatch.persona import PersonaRefused, load_persona, validate_persona
from jobwatch.watch import run_watch

FIXTURES = Path(__file__).parent / "fixtures"
BASE = FIXTURES / "board_base.json"
PLUS_ONE = FIXTURES / "board_plus_one.json"
T0 = datetime(2026, 10, 28, 12, 0, 0, tzinfo=timezone.utc)
T1 = T0 + timedelta(hours=1)


class RecordingSession:
    """Stands in for requests.Session; records calls and returns a canned body."""

    def __init__(self, body=b""):
        self.calls = []
        self.body = body

    def get(self, url, **kwargs):
        self.calls.append(url)
        session = self

        class Response:
            content = session.body

            def raise_for_status(self):
                pass

        return Response()


def valid_persona():
    return json.loads((FIXTURES / "persona_valid.json").read_text())


# --- allow-list -------------------------------------------------------------

@pytest.mark.parametrize("url", [
    "https://example.com/v1/boards/anthropic/jobs",
    "https://boards-api.greenhouse.io.evil.example/v1/boards/anthropic/jobs",
    "https://api.greenhouse.io/v1/boards/anthropic/jobs",
])
def test_non_allow_listed_host_raises_and_sends_nothing(url):
    session = RecordingSession()
    with pytest.raises(ValueError):
        fetcher.fetch(url, session=session)
    assert session.calls == []


def test_allow_listed_host_is_requested_once():
    session = RecordingSession(body=b'{"jobs": []}')
    assert fetcher.fetch(fetcher.BOARD_URL, session=session) == b'{"jobs": []}'
    assert session.calls == [fetcher.BOARD_URL]


# --- persona ----------------------------------------------------------------

def test_real_persona_file_loads():
    resume = load_persona(Path(__file__).parent.parent / "persona" / "ananya-rao.resume.json")
    assert resume["target_roles"] == [
        "Machine Learning Engineer", "AI Engineer", "Applied NLP Engineer", "ML Engineer",
        "Research Engineer"]  # CONTRACT.md Amendment 1


@pytest.mark.parametrize("email", ["ananya.rao@gmail.com", "someone@example.com.evil.org"])
def test_real_looking_email_is_refused(email):
    resume = valid_persona()
    resume["personal"]["email"] = email
    with pytest.raises(PersonaRefused, match="example.com"):
        validate_persona(resume)


@pytest.mark.parametrize("phone", ["(617) 253-0171", "617-555", "(555) 253-0171"])
def test_non_555_phone_is_refused(phone):
    resume = valid_persona()
    resume["personal"]["phone"] = phone
    with pytest.raises(PersonaRefused, match="555"):
        validate_persona(resume)


@pytest.mark.parametrize("path", [
    ("personal", "name"),
    ("skills", "languages"),
    ("skills", "ml_nlp"),
    ("skills", "backend_automation"),
    ("skills", "database_cloud"),
    ("skills", "familiar_with_not_shipped"),
    ("target_roles",),
    ("willing_to_relocate_us",),
    ("needs_sponsorship",),
])
def test_missing_required_field_is_refused(path):
    resume = copy.deepcopy(valid_persona())
    parent = resume
    for key in path[:-1]:
        parent = parent[key]
    del parent[path[-1]]
    with pytest.raises(PersonaRefused, match="schema"):
        validate_persona(resume)


# --- watch ------------------------------------------------------------------

def test_first_run_reports_zero_new_and_writes_state(tmp_path):
    session = RecordingSession(body=BASE.read_bytes())
    report = run_watch(tmp_path, T0, session=session)
    assert report["run_type"] == "baseline"
    assert report["new_count"] == 0 and report["new_postings"] == []
    assert report["total_postings"] == 2
    state = json.loads((tmp_path / "state" / "seen_ids.json").read_text())
    assert state == {"seen_ids": [1001, 1002], "last_run_utc": "2026-10-28T12:00:00Z"}


def test_live_run_saves_raw_body_unmodified(tmp_path):
    body = BASE.read_bytes()
    run_watch(tmp_path, T0, session=RecordingSession(body=body))
    raw = tmp_path / "data" / "raw" / "anthropic_20261028T120000Z.json"
    assert raw.read_bytes() == body


def test_second_run_with_one_added_id_reports_exactly_that_id(tmp_path):
    run_watch(tmp_path, T0, session=RecordingSession(body=BASE.read_bytes()))
    report = run_watch(tmp_path, T1, session=RecordingSession(body=PLUS_ONE.read_bytes()))
    assert report["run_type"] == "live"
    assert report["new_count"] == 1
    assert report["new_postings"] == [{"id": 1003, "title": "Fixture Posting C"}]
    state = json.loads((tmp_path / "state" / "seen_ids.json").read_text())
    assert state["seen_ids"] == [1001, 1002, 1003]
    assert state["last_run_utc"] == "2026-10-28T13:00:00Z"


def test_second_run_with_no_changes_reports_zero_new(tmp_path):
    run_watch(tmp_path, T0, session=RecordingSession(body=BASE.read_bytes()))
    report = run_watch(tmp_path, T1, session=RecordingSession(body=BASE.read_bytes()))
    assert report["run_type"] == "live"
    assert report["new_count"] == 0 and report["new_postings"] == []


def test_run_report_file_matches_contract_fields(tmp_path):
    run_watch(tmp_path, T0, session=RecordingSession(body=BASE.read_bytes()))
    report = json.loads((tmp_path / "data" / "runs" / "20261028T120000Z.json").read_text())
    assert set(report) == {"run_type", "label", "baseline", "run_time_utc", "raw_file",
                           "total_postings", "new_count", "new_postings",
                           "claude_enabled", "results"}
    assert report["raw_file"].endswith("anthropic_20261028T120000Z.json")


def test_seeded_run_is_labeled_seeded_in_report_and_output(tmp_path, capsys, monkeypatch):
    run_watch(tmp_path, T0, from_file=BASE)

    def no_network(*args, **kwargs):
        raise AssertionError("seeded run must not fetch")

    monkeypatch.setattr(fetcher, "fetch", no_network)
    assert main(["watch", "--from-file", str(PLUS_ONE), "--root", str(tmp_path),
                 "--no-claude"]) == 0
    out = capsys.readouterr().out
    assert all(line.startswith("SEEDED ") for line in out.strip().splitlines())
    assert "SEEDED NEW 1003 Fixture Posting C" in out

    reports = sorted((tmp_path / "data" / "runs").glob("*.json"))
    latest = json.loads(reports[-1].read_text())
    assert latest["run_type"] == "seeded" and latest["label"] == "SEEDED"
    assert latest["raw_file"] == str(PLUS_ONE)
    assert latest["new_postings"] == [{"id": 1003, "title": "Fixture Posting C"}]
    # A seeded run reads the given file; it does not write a new raw file.
    assert not (tmp_path / "data" / "raw").exists()


def test_seeded_run_without_root_leaves_project_state_untouched(tmp_path, monkeypatch, capsys):
    import jobwatch.__main__ as cli

    monkeypatch.setattr(cli, "PROJECT_ROOT", tmp_path)
    state_path = tmp_path / "state" / "seen_ids.json"
    state_path.parent.mkdir()
    original = b'{"seen_ids": [1001], "last_run_utc": "2026-10-27T00:00:00Z"}\n'
    state_path.write_bytes(original)
    mtime = state_path.stat().st_mtime_ns

    assert main(["watch", "--from-file", str(PLUS_ONE), "--no-claude"]) == 0
    out = capsys.readouterr().out

    assert state_path.read_bytes() == original
    assert state_path.stat().st_mtime_ns == mtime
    assert not (tmp_path / "data").exists()
    # Had it read the project state (id 1001 seen), it would have reported new ids.
    assert "baseline=True" in out and "new=0" in out
    assert (tmp_path / "seeded" / "state" / "seen_ids.json").exists()
    assert len(list((tmp_path / "seeded" / "data" / "runs").glob("*.json"))) == 1


def test_seeded_run_refuses_project_folder_as_root(tmp_path, monkeypatch):
    import jobwatch.__main__ as cli

    monkeypatch.setattr(cli, "PROJECT_ROOT", tmp_path)
    with pytest.raises(SystemExit):
        main(["watch", "--from-file", str(PLUS_ONE), "--root", str(tmp_path),
              "--no-claude"])
    assert not (tmp_path / "state").exists() and not (tmp_path / "data").exists()


def test_seeded_first_run_is_still_a_baseline(tmp_path):
    report = run_watch(tmp_path, T0, from_file=PLUS_ONE)
    assert report["run_type"] == "seeded" and report["label"] == "SEEDED"
    assert report["baseline"] is True and report["new_count"] == 0
