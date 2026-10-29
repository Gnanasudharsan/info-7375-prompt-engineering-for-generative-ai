"""Offline tests for experiment/run_judge.py with a mocked client. Every model
reply below is CONSTRUCTED; none is real Claude output. No test calls the API."""
import builtins
import hashlib
import importlib.util
import io
import json
import pathlib
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("run_judge", ROOT / "experiment" / "run_judge.py")
run_judge = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run_judge)

PROMPT = ROOT / "prompts" / "judge_baseline.md"
DEV = json.loads((ROOT / "experiment" / "postings_dev.json").read_text(encoding="utf-8"))
DEV_IDS = [p["id"] for p in DEV]


def text_response(text, stop_reason="end_turn"):
    return SimpleNamespace(stop_reason=stop_reason, model="mock-model",
                           content=[SimpleNamespace(type="text", text=text)])


def valid_reply(pid, verdict):
    return json.dumps({"id": pid, "verdict": verdict, "reasoning": "constructed test reply",
                       "resume_fields_cited": ["target_roles"],
                       "posting_fields_cited": ["title"]})


class ScriptedClient:
    """Answers from script(posting_id, call_number_for_that_posting) -> text."""

    def __init__(self, script):
        self.script = script
        self.calls = []
        self.per_posting = {}
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        pid = json.loads(kwargs["messages"][0]["content"])["posting"]["id"]
        n = self.per_posting.get(pid, 0)
        self.per_posting[pid] = n + 1
        return text_response(self.script(pid, n))


def always_relevant(pid, n):
    return valid_reply(pid, "RELEVANT")


def run(tmp_path, *extra, client=None, name="out"):
    client = client or ScriptedClient(always_relevant)
    out = tmp_path / name
    code = run_judge.main(["--split", "dev", "--prompt", str(PROMPT), "--out", str(out), *extra],
                          client=client)
    return code, out, client


def test_every_call_is_a_fresh_single_message_request(tmp_path):
    ids = f"{DEV_IDS[0]},{DEV_IDS[1]}"
    _, _, client = run(tmp_path, "--ids", ids, "--repeats", "3")
    assert len(client.calls) == 6
    for call in client.calls:
        assert set(call) == {"model", "max_tokens", "system", "messages"}
        assert len(call["messages"]) == 1 and call["messages"][0]["role"] == "user"
        assert set(json.loads(call["messages"][0]["content"])) == {"posting", "resume"}
        assert call["system"] == PROMPT.read_text(encoding="utf-8")
    # No message list is shared or grown across calls.
    assert len({id(c["messages"]) for c in client.calls}) == 6


def test_retry_is_also_fresh_and_raw_text_of_each_attempt_is_saved(tmp_path):
    pid = DEV_IDS[0]
    client = ScriptedClient(lambda p, n: "not json" if n == 0 else valid_reply(p, "NOT_RELEVANT"))
    _, out, _ = run(tmp_path, "--ids", str(pid), client=client)
    assert len(client.calls) == 2
    assert all(len(c["messages"]) == 1 for c in client.calls)
    saved = json.loads((out / f"{pid}_r01.json").read_text())
    assert [a["raw_text"] for a in saved["attempts"]] == ["not json", valid_reply(pid, "NOT_RELEVANT")]
    assert saved["parsed"]["verdict"] == "NOT_RELEVANT"
    assert saved["validator"]["status"] == "ok" and len(saved["validator"]["failed_attempts"]) == 1


def test_summary_lists_verdicts_per_posting_across_repeats(tmp_path):
    a, b, c = DEV_IDS[:3]

    def script(pid, n):
        if pid == a:
            return valid_reply(pid, "RELEVANT")
        if pid == b:  # alternates by repeat: calls 0, 1, 2 are repeats 1, 2, 3
            return valid_reply(pid, "RELEVANT" if n % 2 == 0 else "NOT_RELEVANT")
        return "never valid"  # c: two failures per repeat -> judgment_unavailable

    _, out, client = run(tmp_path, "--ids", f"{a},{b},{c}", "--repeats", "3",
                         client=ScriptedClient(script))
    summary = json.loads((out / "summary.json").read_text())
    assert summary["verdicts"] == {
        str(a): ["RELEVANT"] * 3,
        str(b): ["RELEVANT", "NOT_RELEVANT", "RELEVANT"],
        str(c): ["judgment_unavailable"] * 3,
    }
    assert summary["repeats"] == 3 and summary["split"] == "dev"
    assert summary["prompt_sha256"] == hashlib.sha256(PROMPT.read_bytes()).hexdigest()
    assert client.per_posting[c] == 6  # 1 retry per repeat, never a third attempt


def test_one_file_per_call_with_required_fields(tmp_path):
    pid = DEV_IDS[0]
    _, out, _ = run(tmp_path, "--ids", str(pid), "--repeats", "2")
    assert sorted(p.name for p in out.iterdir()) == [f"{pid}_r01.json", f"{pid}_r02.json",
                                                     "summary.json"]
    saved = json.loads((out / f"{pid}_r02.json").read_text())
    assert saved["posting_id"] == pid and saved["repeat"] == 2
    assert saved["timestamp_utc"].endswith("+00:00")
    assert saved["model"] == run_judge.claude_judge.DEFAULT_MODEL
    assert saved["prompt_file"] == str(PROMPT)
    assert saved["prompt_sha256"] == hashlib.sha256(PROMPT.read_bytes()).hexdigest()
    assert saved["attempts"][0]["raw_text"] == valid_reply(pid, "RELEVANT")
    assert saved["validator"] == {"status": "ok", "failed_attempts": []}


def test_judgment_unavailable_is_recorded_as_such(tmp_path):
    pid = DEV_IDS[0]
    client = ScriptedClient(lambda p, n: "Here is my verdict: RELEVANT")
    _, out, _ = run(tmp_path, "--ids", str(pid), client=client)
    saved = json.loads((out / f"{pid}_r01.json").read_text())
    assert saved["parsed"] == "judgment_unavailable"
    assert saved["validator"]["status"] == "judgment_unavailable"
    assert len(saved["attempts"]) == 2 and len(saved["validator"]["failed_attempts"]) == 2


def test_refuses_existing_out_folder_before_any_call(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    (out / "keep.txt").write_text("earlier result")
    client = ScriptedClient(always_relevant)
    with pytest.raises(FileExistsError):
        run(tmp_path, client=client)
    assert client.calls == []
    assert [p.name for p in out.iterdir()] == ["keep.txt"]
    assert (out / "keep.txt").read_text() == "earlier result"


def test_second_run_into_same_out_is_refused(tmp_path):
    run(tmp_path, "--ids", str(DEV_IDS[0]))
    with pytest.raises(FileExistsError):
        run(tmp_path, "--ids", str(DEV_IDS[0]))


def is_labels_file(path) -> bool:
    name = Path(str(path)).name
    return name.startswith("labels_") and name.endswith(".json")


def test_never_opens_the_labels_files(tmp_path, monkeypatch):
    opened = []

    def spy(original):
        def wrapper(file, *args, **kwargs):
            opened.append(str(file))
            if is_labels_file(file):
                raise AssertionError(f"runner opened a labels file: {file}")
            return original(file, *args, **kwargs)
        return wrapper

    def spy_method(original):
        def wrapper(self, *args, **kwargs):
            opened.append(str(self))
            if is_labels_file(self):
                raise AssertionError(f"runner opened a labels file: {self}")
            return original(self, *args, **kwargs)
        return wrapper

    monkeypatch.setattr(builtins, "open", spy(builtins.open))
    monkeypatch.setattr(io, "open", spy(io.open))
    for method in ("open", "read_text", "read_bytes"):
        monkeypatch.setattr(pathlib.Path, method, spy_method(getattr(pathlib.Path, method)))

    run(tmp_path, "--repeats", "2")
    assert any(name.endswith("postings_dev.json") for name in opened)  # the spy is working
    assert not [name for name in opened if is_labels_file(name)]


def test_unknown_id_is_refused_before_any_call(tmp_path):
    client = ScriptedClient(always_relevant)
    with pytest.raises(SystemExit, match="not in dev"):
        run(tmp_path, "--ids", "123", client=client)
    assert client.calls == [] and not (tmp_path / "out").exists()


def test_heldout_ids_are_not_in_dev(tmp_path):
    heldout = json.loads((ROOT / "experiment" / "postings_heldout.json").read_text())
    with pytest.raises(SystemExit):
        run(tmp_path, "--ids", str(heldout[0]["id"]))
