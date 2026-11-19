"""Tests for mcp/server.py against mcp/TOOL_SPEC.md, written before the server exists (expected to fail)."""
import json, subprocess, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "mcp" / "server.py"

def session(messages):
    p = subprocess.run([sys.executable, str(SERVER)], input="\n".join(json.dumps(m) if isinstance(m, dict) else m for m in messages) + "\n",
                       capture_output=True, text=True, cwd=ROOT, timeout=20)
    return [json.loads(l) for l in p.stdout.splitlines() if l.strip()]

INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "0"}}}
NOTE = {"jsonrpc": "2.0", "method": "notifications/initialized"}

def call(i, args):
    return {"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": "score_posting", "arguments": args}}

def kept_id():
    for line in open(ROOT / "runs/20261119T162945Z/filter_v1_C1_C4.jsonl"):
        r = json.loads(line)
        if r["decision"] == "keep":
            return r["board"], str(r["id"])

def test_initialize_and_no_reply_to_notification():
    out = session([INIT, NOTE])
    assert len(out) == 1 and out[0]["id"] == 1
    assert out[0]["result"]["protocolVersion"] == "2025-06-18" and "tools" in out[0]["result"]["capabilities"]

def test_tools_list_declares_one_read_only_tool():
    out = session([INIT, NOTE, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}])
    tools = out[1]["result"]["tools"]
    assert [t["name"] for t in tools] == ["score_posting"]
    ann = tools[0]["annotations"]
    assert ann["readOnlyHint"] is True and ann["destructiveHint"] is False and ann["openWorldHint"] is False

def test_call_returns_filter_result_and_claims_for_a_shortlisted_posting():
    board, pid = kept_id()
    out = session([INIT, NOTE, call(3, {"board": board, "id": pid})])
    res = out[1]["result"]; assert not res.get("isError")
    body = json.loads(res["content"][0]["text"])
    assert body["decision"] == "keep" and len(body["claims"]) == 5

@pytest.mark.parametrize("args", [{"board": "greenhouse:anthropic", "id": "../../etc/passwd"},
                                  {"board": "greenhouse:anthropic", "id": "000000"},
                                  {"board": "evil:board", "id": "1"}])
def test_bad_input_is_a_tool_error_not_a_crash(args):
    out = session([INIT, NOTE, call(4, args)])
    assert out[1]["result"]["isError"] is True

def test_unknown_method_and_bad_json():
    out = session([INIT, NOTE, {"jsonrpc": "2.0", "id": 5, "method": "files/write"}, "{not json"])
    assert out[1]["error"]["code"] == -32601
    assert out[2]["error"]["code"] == -32700

def test_writes_only_its_transcript(tmp_path):
    before = {p for p in ROOT.rglob("*") if ".venv" not in p.parts and "transcripts" not in p.parts and ".pytest_cache" not in p.parts and "__pycache__" not in p.parts}
    board, pid = kept_id(); session([INIT, NOTE, call(6, {"board": board, "id": pid})])
    after = {p for p in ROOT.rglob("*") if ".venv" not in p.parts and "transcripts" not in p.parts and ".pytest_cache" not in p.parts and "__pycache__" not in p.parts}
    assert after == before

def test_transcript_records_both_directions():
    board, pid = kept_id(); session([INIT, NOTE, call(7, {"board": board, "id": pid})])
    newest = max((ROOT / "transcripts").glob("server-*.jsonl"), key=lambda p: p.stat().st_mtime)
    dirs = [json.loads(l)["direction"] for l in newest.read_text().splitlines()]
    assert "in" in dirs and "out" in dirs
