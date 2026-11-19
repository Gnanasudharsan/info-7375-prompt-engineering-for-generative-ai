"""jobwatch-score: a read-only MCP tool server, built from mcp/TOOL_SPEC.md.

Standard library only. JSON-RPC 2.0 over stdio, one JSON object per line
(no Content-Length framing). One tool, score_posting, which looks a posting up
in two fixed files. It writes nothing except its own transcript.
"""
import csv
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# The only two files the tool ever reads. Fixed here; never built from client input.
FILTER_PATH = ROOT / "runs" / "20261119T162945Z" / "filter_v1_C1_C4.jsonl"
LABELS_PATH = ROOT / "shortlist" / "claim_labels.csv"
TRANSCRIPT_DIR = ROOT / "transcripts"

SERVER_INFO = {"name": "jobwatch-score", "version": "1.0.0"}
SUPPORTED_VERSIONS = ("2024-11-05", "2025-03-26", "2025-06-18")
DEFAULT_VERSION = "2025-06-18"
BOARDS = ("greenhouse:anthropic", "ashby:notion", "lever:spotify")
ID_RE = re.compile(r"^[A-Za-z0-9-]{1,64}$")
OUTPUT_FIELDS = ("decision", "score", "rejected_by", "matched", "components")

TOOL = {
    "name": "score_posting",
    "description": (
        "Look up one job posting's filter result (decision, score, rejected_by, matched, "
        "components) from the fixed filter run, plus its five claim labels if it is on the shortlist. "
        "Read-only; reads two fixed local files."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "board": {"type": "string", "enum": list(BOARDS)},
            "id": {"type": "string", "pattern": ID_RE.pattern},
        },
        "required": ["board", "id"],
        "additionalProperties": False,
    },
    "annotations": {
        "readOnlyHint": True,
        "openWorldHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
    },
}


class Transcript:
    """Appends one JSON line per message, both directions, to transcripts/server-<UTC>.jsonl."""

    def __init__(self):
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        TRANSCRIPT_DIR.mkdir(exist_ok=True)
        self.path = TRANSCRIPT_DIR / f"server-{stamp}.jsonl"
        self._fh = open(self.path, "x", encoding="utf-8")

    def log(self, direction, message):
        ts = datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
        self._fh.write(json.dumps({"ts": ts, "direction": direction, "message": message}) + "\n")
        self._fh.flush()

    def close(self):
        self._fh.close()


def error(id_, code, message):
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


def result(id_, value):
    return {"jsonrpc": "2.0", "id": id_, "result": value}


def tool_error(message):
    return {"content": [{"type": "text", "text": message}], "isError": True}


def score_posting(args):
    board, pid = args.get("board"), args.get("id")
    if not isinstance(board, str) or board not in BOARDS:
        return tool_error(f"unknown board: {board!r}; expected one of {', '.join(BOARDS)}")
    if not isinstance(pid, str) or not ID_RE.match(pid):
        return tool_error("bad id: must be 1-64 characters, letters, digits or hyphens only")

    record = None
    with open(FILTER_PATH, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("board") == board and str(r.get("id")) == pid:
                record = r
                break
    if record is None:
        return tool_error(f"unknown id: no posting {pid} on {board} in the filter run")

    body = {"board": board, "id": pid}
    body.update({k: record.get(k) for k in OUTPUT_FIELDS})

    with open(LABELS_PATH, encoding="utf-8", newline="") as fh:
        claims = [{"claim": row["claim"], "label": row["my_label"]}
                  for row in csv.DictReader(fh)
                  if row["board"] == board and row["id"] == pid]
    if claims:
        body["claims"] = claims

    return {"content": [{"type": "text", "text": json.dumps(body)}], "isError": False}


def handle(msg):
    """Return a response dict, or None when no reply is due (notifications)."""
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or not isinstance(msg.get("method"), str):
        rid = msg.get("id") if isinstance(msg, dict) else None
        return error(rid, -32600, "invalid request")

    is_notification = "id" not in msg
    rid, method, params = msg.get("id"), msg["method"], msg.get("params")

    if is_notification:
        return None  # notifications/initialized and any other notification: never answered

    if params is not None and not isinstance(params, dict):
        return error(rid, -32602, "params must be an object")
    params = params or {}

    if method == "initialize":
        requested = params.get("protocolVersion")
        version = requested if requested in SUPPORTED_VERSIONS else DEFAULT_VERSION
        return result(rid, {"protocolVersion": version, "capabilities": {"tools": {}}, "serverInfo": SERVER_INFO})

    if method == "tools/list":
        return result(rid, {"tools": [TOOL]})

    if method == "tools/call":
        name, args = params.get("name"), params.get("arguments", {})
        if name != TOOL["name"]:
            return error(rid, -32602, f"unknown tool: {name!r}")
        if not isinstance(args, dict):
            return error(rid, -32602, "arguments must be an object")
        try:
            return result(rid, score_posting(args))
        except Exception as exc:  # file missing/corrupt: a tool failure, not a crash
            return result(rid, tool_error(f"tool failed: {type(exc).__name__}"))

    return error(rid, -32601, f"method not found: {method}")


def main():
    stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
    stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")
    transcript = Transcript()
    try:
        for raw in stdin:
            line = raw.rstrip("\r\n")
            if not line.strip():
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                transcript.log("in", line)
                response = error(None, -32700, "parse error")
            else:
                transcript.log("in", msg)
                try:
                    response = handle(msg)
                except Exception as exc:
                    rid = msg.get("id") if isinstance(msg, dict) else None
                    response = error(rid, -32603, f"internal error: {type(exc).__name__}")
            if response is not None:
                transcript.log("out", response)
                stdout.write(json.dumps(response) + "\n")
                stdout.flush()
    finally:
        transcript.close()


if __name__ == "__main__":
    main()
