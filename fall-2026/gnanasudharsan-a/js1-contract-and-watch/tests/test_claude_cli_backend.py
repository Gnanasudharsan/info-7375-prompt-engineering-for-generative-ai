"""Offline tests for the claude_cli backend with a mocked subprocess. Every CLI
envelope and model reply below is CONSTRUCTED; none is real Claude output.
No test starts a real claude process (conftest.py refuses subprocess.run)."""
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

from jobwatch import claude_judge, validator

ROOT = Path(__file__).resolve().parent.parent
PERSONA = json.loads((ROOT / "persona" / "ananya-rao.resume.json").read_text())
POSTING_ID = 9000001
POSTING = {
    "id": POSTING_ID,
    "title": "Machine Learning Engineer, Applied NLP",
    "location": {"name": "San Francisco, CA"},
    "content": "&lt;p&gt;Build with Python, PyTorch and AWS.&lt;/p&gt;",
    "departments": [{"name": "Engineering"}],
    "updated_at": "2026-10-28T00:00:00-04:00",
}
VALID = json.dumps({"id": POSTING_ID, "verdict": "RELEVANT", "reasoning": "constructed test reply",
                    "resume_fields_cited": ["target_roles"], "posting_fields_cited": ["title"]})
SESSION_FLAGS = {"-c", "--continue", "-r", "--resume", "--fork-session", "--from-pr",
                 "--teleport", "--bg", "--background"}


def envelope(result, is_error=False, subtype="success", session_id="constructed-session",
             model="constructed-model"):
    return json.dumps({"type": "result", "subtype": subtype, "is_error": is_error,
                       "result": result, "session_id": session_id, "num_turns": 1,
                       "modelUsage": {model: {"inputTokens": 1, "outputTokens": 1}}})


class FakeRun:
    """Stands in for subprocess.run: records each call, replays stdout items in order.
    An item may be a string (stdout, exit 0), a (stdout, returncode) pair, or an exception."""

    def __init__(self, *items):
        self.items = list(items)
        self.calls = []

    def __call__(self, argv, **kwargs):
        cwd = Path(kwargs["cwd"])
        self.calls.append({"argv": list(argv), "cwd_contents": sorted(cwd.iterdir()), **kwargs})
        item = self.items.pop(0)
        if isinstance(item, Exception):
            raise item
        stdout, code = item if isinstance(item, tuple) else (item, 0)
        return subprocess.CompletedProcess(argv, code, stdout=stdout, stderr="")


def flag_value(argv, flag):
    return argv[argv.index(flag) + 1]


def judge(fake, model="test-model", prompt="PROMPT TEXT"):
    runner = claude_judge.ClaudeCliRunner("claude", run=fake)
    record = claude_judge.judge_with_claude(POSTING, PERSONA, runner, prompt, model)
    return record, runner


def test_each_attempt_is_a_fresh_process_with_its_own_session_and_directory():
    fake = FakeRun(envelope("not json"), envelope(VALID))
    record, runner = judge(fake)
    judge(FakeRun(envelope(VALID)))
    assert record["status"] == "ok" and record["backend"] == "claude_cli"
    assert len(fake.calls) == 2  # the retry started a second process
    for call in fake.calls:
        assert call["argv"][0] == "claude" and "-p" in call["argv"]
        assert not SESSION_FLAGS & set(call["argv"])
        assert call["argv"].count("--session-id") == 1
        assert "--no-session-persistence" in call["argv"]
    session_ids = [flag_value(c["argv"], "--session-id") for c in fake.calls]
    assert len(set(session_ids)) == 2
    assert len({c["cwd"] for c in fake.calls}) == 2


def test_working_directory_is_a_new_empty_temp_dir_never_the_project():
    fake = FakeRun(envelope(VALID))
    judge(fake)
    [call] = fake.calls
    cwd = Path(call["cwd"]).resolve()
    assert cwd != ROOT.resolve() and ROOT.resolve() not in cwd.parents
    assert cwd != Path.cwd().resolve() and Path.cwd().resolve() not in cwd.parents
    assert call["cwd_contents"] == []  # empty when the process started


@pytest.mark.parametrize("inside", ["", "jobwatch", "experiment/runs"])
def test_project_folder_or_a_subfolder_is_refused_as_workdir(inside):
    with pytest.raises(claude_judge.ClaudeCliError, match="refusing"):
        claude_judge.check_workdir(ROOT / inside)


def test_project_workdir_counts_as_failed_attempt_and_no_process_starts(monkeypatch):
    monkeypatch.setattr(claude_judge.tempfile, "mkdtemp", lambda prefix: str(ROOT))
    fake = FakeRun(envelope(VALID), envelope(VALID))
    record, _ = judge(fake)
    assert fake.calls == []
    assert record["status"] == "judgment_unavailable"
    assert all(e.startswith("cli: refusing") for e in record["failed_attempts"])


def test_all_tools_are_disabled_and_none_are_allowed():
    fake = FakeRun(envelope(VALID))
    judge(fake)
    argv = fake.calls[0]["argv"]
    assert flag_value(argv, "--tools") == ""
    assert "--strict-mcp-config" in argv and "--mcp-config" not in argv
    assert "--safe-mode" in argv and "--disable-slash-commands" in argv
    assert flag_value(argv, "--permission-prompts") == "none"
    for loosening in ("--allowedTools", "--allowed-tools", "--add-dir", "--dangerously-skip-permissions",
                      "--allow-dangerously-skip-permissions", "--chrome"):
        assert loosening not in argv


def test_model_from_jobwatch_model_and_prompt_file_as_system_prompt(monkeypatch, tmp_path):
    monkeypatch.setenv("JOBWATCH_MODEL", "env-model")
    monkeypatch.setenv("JOBWATCH_BACKEND", "claude_cli")
    prompt = tmp_path / "p.md"
    prompt.write_text("FROM FILE\nsecond line")
    fake = FakeRun(envelope(VALID))
    runner = claude_judge.ClaudeCliRunner("claude", run=fake)
    record = claude_judge.make_judge(prompt, client=runner)(POSTING, PERSONA)
    argv = fake.calls[0]["argv"]
    assert flag_value(argv, "--model") == "env-model" and record["model"] == "env-model"
    assert flag_value(argv, "--system-prompt") == "FROM FILE\nsecond line"
    # The user turn is data only, on stdin, not a positional argument.
    sent = json.loads(fake.calls[0]["input"])
    assert set(sent) == {"posting", "resume"} and sent["posting"]["id"] == POSTING_ID
    assert fake.calls[0]["input"] not in argv


def test_raw_result_text_reaches_the_validator_unchanged(monkeypatch):
    seen = []
    real_validate = validator.validate
    monkeypatch.setattr(validator, "validate", lambda text, pid: seen.append(text) or real_validate(text, pid))
    padded = "\n" + VALID + "  "
    fenced = "```json\n" + VALID + "\n```"
    record, _ = judge(FakeRun(envelope(fenced), envelope(padded)))
    assert seen == [fenced, padded]  # no strip, no fence removal, no repair before validating
    assert record["status"] == "ok" and record["failed_attempts"][0].startswith("validator:")


def test_invalid_output_gets_one_retry_then_judgment_unavailable():
    fake = FakeRun(envelope("Here is my verdict: RELEVANT"), envelope("{}"), envelope(VALID))
    record, runner = judge(fake)
    assert len(fake.calls) == 2 and len(fake.items) == 1  # never a third process
    assert record["status"] == "judgment_unavailable" and record["output"] is None
    assert all(e.startswith("validator:") for e in record["failed_attempts"])
    assert len(runner.attempts) == 2


@pytest.mark.parametrize("bad", [
    ("not an envelope", 0),
    (envelope(VALID), 1),
    (envelope("", is_error=True, subtype="error_during_execution"), 0),
    (json.dumps({"type": "result", "is_error": False}), 0),
    subprocess.TimeoutExpired(cmd="claude", timeout=600),
    FileNotFoundError("claude"),
])
def test_cli_failures_count_as_failed_attempts_not_crashes(bad):
    record, _ = judge(FakeRun(bad, bad if not isinstance(bad, Exception) else bad))
    assert record["status"] == "judgment_unavailable"
    assert len(record["failed_attempts"]) == 2
    assert all(e.startswith("cli:") for e in record["failed_attempts"])


def test_attempt_record_has_flags_without_prompt_text_and_reported_ids():
    fake = FakeRun(envelope(VALID, session_id="sess-123", model="claude-x"))
    _, runner = judge(fake, prompt="SECRET-LOOKING PROMPT BODY")
    [attempt] = runner.attempts
    assert attempt["backend"] == "claude_cli"
    assert "SECRET-LOOKING PROMPT BODY" not in json.dumps(attempt["command"])
    assert flag_value(attempt["command"], "--system-prompt") == "<prompt file text>"
    assert attempt["command"][1:] != fake.calls[0]["argv"][1:]  # only the prompt differs
    assert attempt["reported_session_id"] == "sess-123"
    assert attempt["requested_session_id"] == flag_value(fake.calls[0]["argv"], "--session-id")
    assert attempt["reported_models"] == ["claude-x"]
    assert attempt["raw_text"] == VALID and attempt["returncode"] == 0


def test_backend_env_default_invalid_and_missing_executable(monkeypatch):
    assert claude_judge.backend_name() == "api"
    monkeypatch.setenv("JOBWATCH_BACKEND", "openai")
    with pytest.raises(claude_judge.ClaudeJudgeUnavailable, match="JOBWATCH_BACKEND"):
        claude_judge.backend_name()
    monkeypatch.setenv("JOBWATCH_BACKEND", "claude_cli")
    monkeypatch.setattr(claude_judge.shutil, "which", lambda name: None)
    with pytest.raises(claude_judge.ClaudeJudgeUnavailable, match="claude executable"):
        claude_judge.make_backend_client()
    # claude_cli needs no ANTHROPIC_API_KEY (conftest removed it)
    monkeypatch.setattr(claude_judge.shutil, "which", lambda name: "/usr/local/bin/claude")
    assert isinstance(claude_judge.make_backend_client(), claude_judge.ClaudeCliRunner)


# --- experiment/run_judge.py with the claude_cli backend ---------------------

_spec = importlib.util.spec_from_file_location("run_judge", ROOT / "experiment" / "run_judge.py")
run_judge = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run_judge)
PROMPT = ROOT / "prompts" / "judge_baseline.md"
DEV_IDS = [p["id"] for p in json.loads((ROOT / "experiment" / "postings_dev.json").read_text())]


def valid_for(pid):
    return json.dumps({"id": pid, "verdict": "NOT_RELEVANT", "reasoning": "constructed test reply",
                       "resume_fields_cited": ["target_roles"], "posting_fields_cited": ["title"]})


def test_run_judge_saves_cli_attempts_per_call(monkeypatch, tmp_path):
    monkeypatch.setenv("JOBWATCH_BACKEND", "claude_cli")
    a, b = DEV_IDS[:2]
    fake = FakeRun(envelope("bad", session_id="s1"), envelope(valid_for(a), session_id="s2"),
                   envelope(valid_for(b), session_id="s3"))
    out = tmp_path / "out"
    run_judge.main(["--split", "dev", "--prompt", str(PROMPT), "--ids", f"{a},{b}", "--out", str(out)],
                   client=claude_judge.ClaudeCliRunner("claude", run=fake))
    first = json.loads((out / f"{a}_r01.json").read_text())
    second = json.loads((out / f"{b}_r01.json").read_text())
    assert first["backend"] == second["backend"] == "claude_cli"
    assert [x["reported_session_id"] for x in first["attempts"]] == ["s1", "s2"]
    assert [x["reported_session_id"] for x in second["attempts"]] == ["s3"]
    assert [x["raw_text"] for x in first["attempts"]] == ["bad", valid_for(a)]
    assert first["parsed"]["verdict"] == "NOT_RELEVANT"
    assert PROMPT.read_text() not in json.dumps(first["attempts"])
    summary = json.loads((out / "summary.json").read_text())
    assert summary["backend"] == "claude_cli"
    assert summary["verdicts"] == {str(a): ["NOT_RELEVANT"], str(b): ["NOT_RELEVANT"]}


def test_run_judge_refuses_client_that_does_not_match_backend(monkeypatch, tmp_path):
    monkeypatch.setenv("JOBWATCH_BACKEND", "claude_cli")
    with pytest.raises(SystemExit, match="does not match"):
        run_judge.main(["--split", "dev", "--prompt", str(PROMPT), "--out", str(tmp_path / "o")],
                       client=object())
    assert not (tmp_path / "o").exists()
