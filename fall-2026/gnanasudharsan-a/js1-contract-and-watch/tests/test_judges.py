"""Offline tests for Step 3: validator, Claude judge (mocked client), rule
justification, and the wiring into the watch. All postings and model replies
below are CONSTRUCTED; none is real Claude output. No test calls the API."""
import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import anthropic
import httpx2
import pytest

from jobwatch import claude_judge, validator
from jobwatch.__main__ import main
from jobwatch.rule import judge_posting
from jobwatch.watch import run_watch

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).parent / "fixtures"
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
VALID = {
    "id": POSTING_ID,
    "verdict": "RELEVANT",
    "reasoning": "constructed test reply",
    "resume_fields_cited": ["skills.ml_nlp", "target_roles"],
    "posting_fields_cited": ["title", "content"],
}


def reply(**changes):
    out = dict(VALID)
    for key, value in changes.items():
        if value is KeyError:
            del out[key]
        else:
            out[key] = value
    return json.dumps(out)


# --- validator: one test per rejection reason, plus the valid case ---------

def test_valid_reply_is_accepted():
    assert validator.validate(json.dumps(VALID), POSTING_ID) == VALID


def test_rejects_non_json():
    with pytest.raises(validator.ValidationFailed, match="not JSON"):
        validator.validate("RELEVANT, because the title matches.", POSTING_ID)


@pytest.mark.parametrize("text", [
    "Here is my verdict: " + json.dumps(VALID),
    "```json\n" + json.dumps(VALID) + "\n```",
    json.dumps(VALID) + "\nHope this helps.",
])
def test_rejects_text_around_json(text):
    with pytest.raises(validator.ValidationFailed, match="text around"):
        validator.validate(text, POSTING_ID)


def test_rejects_extra_key():
    with pytest.raises(validator.ValidationFailed, match="extra \\['confidence'\\]"):
        validator.validate(reply(confidence=0.9), POSTING_ID)


def test_rejects_missing_key():
    with pytest.raises(validator.ValidationFailed, match="missing \\['reasoning'\\]"):
        validator.validate(reply(reasoning=KeyError), POSTING_ID)


@pytest.mark.parametrize("verdict", ["relevant", "MAYBE", "RELEVANT ", None, ["RELEVANT"]])
def test_rejects_verdict_not_exact(verdict):
    with pytest.raises(validator.ValidationFailed, match="verdict"):
        validator.validate(reply(verdict=verdict), POSTING_ID)


@pytest.mark.parametrize("bad_id", [POSTING_ID + 1, str(POSTING_ID), True, None])
def test_rejects_id_not_matching_posting(bad_id):
    with pytest.raises(validator.ValidationFailed, match="does not match posting id"):
        validator.validate(reply(id=bad_id), POSTING_ID)


@pytest.mark.parametrize("key", ["resume_fields_cited", "posting_fields_cited"])
def test_rejects_empty_citation_array(key):
    with pytest.raises(validator.ValidationFailed, match=f"{key} is empty"):
        validator.validate(reply(**{key: []}), POSTING_ID)


@pytest.mark.parametrize("key,path", [
    ("resume_fields_cited", "skills.kubernetes"),
    ("resume_fields_cited", "personal.email"),
    ("posting_fields_cited", "salary"),
    ("posting_fields_cited", "Title"),
])
def test_rejects_unknown_cited_field(key, path):
    with pytest.raises(validator.ValidationFailed, match="unknown field path"):
        validator.validate(reply(**{key: ["title" if key.startswith("posting") else "target_roles", path]}),
                           POSTING_ID)


# --- Claude judge with a mocked client --------------------------------------

def text_response(text, stop_reason="end_turn"):
    return SimpleNamespace(stop_reason=stop_reason,
                           content=[SimpleNamespace(type="text", text=text)])


class MockClient:
    """Stands in for anthropic.Anthropic; replays canned replies or raises."""

    def __init__(self, *replies):
        self.replies = list(replies)
        self.calls = []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        item = self.replies.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def judge_once(client, model="test-model"):
    return claude_judge.judge_with_claude(POSTING, PERSONA, client, "PROMPT TEXT", model)


def test_valid_reply_first_try_is_ok_and_labeled():
    client = MockClient(text_response(json.dumps(VALID)))
    record = judge_once(client)
    assert record["status"] == "ok" and record["output"] == VALID
    assert record["label"] == "judgment (model output, not fact)"
    assert record["failed_attempts"] == [] and len(client.calls) == 1


def test_request_carries_prompt_file_text_and_data_only():
    client = MockClient(text_response(json.dumps(VALID)))
    judge_once(client)
    call = client.calls[0]
    assert call["system"] == "PROMPT TEXT" and call["model"] == "test-model"
    sent = json.loads(call["messages"][0]["content"])
    assert set(sent) == {"posting", "resume"}
    assert sent["posting"]["id"] == POSTING_ID
    # content is double-unescaped and tag-stripped before it is sent
    assert sent["posting"]["content"] == "Build with Python, PyTorch and AWS."
    assert sent["resume"] == PERSONA


def test_one_retry_after_invalid_reply():
    client = MockClient(text_response("not json"), text_response(json.dumps(VALID)))
    record = judge_once(client)
    assert record["status"] == "ok" and len(client.calls) == 2
    assert len(record["failed_attempts"]) == 1


def test_two_invalid_replies_give_judgment_unavailable_without_third_call():
    client = MockClient(text_response(reply(id=1)), text_response(reply(verdict="maybe")),
                        text_response(json.dumps(VALID)))
    record = judge_once(client)
    assert record["status"] == "judgment_unavailable" and record["output"] is None
    assert len(client.calls) == 2 and len(record["failed_attempts"]) == 2


def test_api_errors_give_judgment_unavailable_not_a_crash():
    request = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")
    client = MockClient(anthropic.APIConnectionError(request=request),
                        anthropic.APIConnectionError(request=request))
    record = judge_once(client)
    assert record["status"] == "judgment_unavailable"
    assert all(e.startswith("api: APIConnectionError") for e in record["failed_attempts"])


def test_refusal_stop_reason_counts_as_failed_attempt():
    client = MockClient(text_response("", stop_reason="refusal"),
                        text_response(json.dumps(VALID)))
    record = judge_once(client)
    assert record["status"] == "ok" and "refusal" in record["failed_attempts"][0]


def test_model_comes_from_jobwatch_model_env(monkeypatch, tmp_path):
    monkeypatch.setenv("JOBWATCH_MODEL", "env-model")
    prompt = tmp_path / "p.md"
    prompt.write_text("FROM FILE")
    client = MockClient(text_response(json.dumps(VALID)))
    claude_judge.make_judge(prompt, client=client)(POSTING, PERSONA)
    assert client.calls[0]["model"] == "env-model"
    assert client.calls[0]["system"] == "FROM FILE"


def test_missing_api_key_refuses_to_build_client():
    with pytest.raises(claude_judge.ClaudeJudgeUnavailable, match="ANTHROPIC_API_KEY"):
        claude_judge.make_client()


def test_missing_prompt_file_refuses(tmp_path):
    with pytest.raises(claude_judge.ClaudeJudgeUnavailable, match="prompt file"):
        claude_judge.make_judge(tmp_path / "absent.md", client=MockClient())


# --- rule justification -----------------------------------------------------

def test_relevant_justification_cites_every_contract_item():
    j = judge_posting(POSTING, PERSONA)["justification"]
    assert j["title"]["matches"][0]["matched_phrase"] == "machine learning engineer"
    assert j["location"]["matched_part"] == "San Francisco, CA"
    assert j["sponsorship"]["negative_phrase_found"] is False
    assert {(m["skill"], m["resume_path"]) for m in j["skills"]["matched"]} == {
        ("Python", "skills.languages"), ("PyTorch", "skills.ml_nlp"),
        ("AWS", "skills.database_cloud")}
    assert j["failed_conditions"] == []


def test_not_relevant_names_each_failed_condition():
    p = copy.deepcopy(POSTING)
    p["title"] = "Senior Account Executive"
    p["location"] = {"name": "Zurich, CH"}
    result = judge_posting(p, PERSONA)
    assert result["verdict"] == "NOT_RELEVANT"
    assert result["justification"]["failed_conditions"] == ["title", "seniority", "location"]
    assert "failed: title, seniority, location" in result["justification"]["summary"]


def test_entity_coded_skill_is_found_after_double_unescape():
    # CONTRACT.md "What a failure looks like": entity codes must not hide "PyTorch".
    p = copy.deepcopy(POSTING)
    p["content"] = "&amp;lt;b&amp;gt;PyTorch&amp;lt;/b&amp;gt; Python AWS"
    assert judge_posting(p, PERSONA)["verdict"] == "RELEVANT"


@pytest.mark.parametrize("name,verdict", [
    ("Remote-Friendly (Travel Required) | San Francisco, CA", "RELEVANT"),
    ("London, UK; Washington, DC", "RELEVANT"),
    ("New York City, NY; Dublin, IE", "RELEVANT"),
    ("Dublin, IE | Zurich, CH", "NOT_RELEVANT"),
])
def test_location_parts(name, verdict):
    p = copy.deepcopy(POSTING)
    p["location"] = {"name": name}
    assert judge_posting(p, PERSONA)["verdict"] == verdict


def test_skill_mentioned_many_times_counts_once():
    p = copy.deepcopy(POSTING)
    p["content"] = "Python python PYTHON and PyTorch"
    skills = judge_posting(p, PERSONA)["justification"]["skills"]
    assert skills["distinct_count"] == 2 and not skills["passed"]


# --- wiring into the watch --------------------------------------------------

T0 = datetime(2026, 10, 28, 12, 0, 0, tzinfo=timezone.utc)
CONTRACT_FIELDS = {"id", "title", "location", "department", "updated_at",
                   "rule_verdict", "claude_verdict", "justification"}


def test_new_posting_record_has_contract_fields_and_both_labels(tmp_path):
    run_watch(tmp_path, T0, from_file=FIXTURES / "board_base.json")
    client = MockClient(text_response(reply(id=1003)))
    report = run_watch(tmp_path, T0.replace(hour=13), from_file=FIXTURES / "board_plus_one.json",
                       persona=PERSONA, claude_judge=lambda job, persona:
                       claude_judge.judge_with_claude(job, persona, client, "P", "m"))
    [record] = report["results"]
    assert set(record) == CONTRACT_FIELDS
    assert record["rule_verdict"] == {"verdict": "NOT_RELEVANT", "label": "record (recomputable)"}
    assert record["claude_verdict"]["label"] == "judgment (model output, not fact)"
    assert record["claude_verdict"]["output"]["id"] == 1003
    saved = json.loads(Path(report["report_file"]).read_text())
    assert saved["results"] == report["results"]


def test_no_claude_run_records_not_run_and_keeps_rule_verdict(tmp_path):
    run_watch(tmp_path, T0, from_file=FIXTURES / "board_base.json")
    report = run_watch(tmp_path, T0.replace(hour=13), from_file=FIXTURES / "board_plus_one.json",
                       persona=PERSONA, claude_judge=None)
    [record] = report["results"]
    assert report["claude_enabled"] is False
    assert record["claude_verdict"]["status"] == "not_run"
    assert record["rule_verdict"]["verdict"] in ("RELEVANT", "NOT_RELEVANT")


def test_cli_without_key_and_without_no_claude_stops_before_writing(tmp_path, capsys):
    prompt = tmp_path / "p.md"
    prompt.write_text("P")
    with pytest.raises(SystemExit):
        main(["watch", "--from-file", str(FIXTURES / "board_plus_one.json"),
              "--root", str(tmp_path / "r"), "--prompt", str(prompt)])
    assert "ANTHROPIC_API_KEY" in capsys.readouterr().err
    assert not (tmp_path / "r").exists()
