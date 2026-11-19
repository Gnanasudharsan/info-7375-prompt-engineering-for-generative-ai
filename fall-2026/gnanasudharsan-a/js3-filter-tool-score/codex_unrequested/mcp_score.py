"""Read-only MCP stdio server for the archived v1.1 scores."""

import argparse
import json
import sys
from contextlib import nullcontext
from pathlib import Path

SCORES = Path(__file__).resolve().parents[1] / "runs/20261119T162945Z/filter_v1_C1_C4.jsonl"
VERSION = "2025-11-25"
TOOL = {
    "name": "lookup_score",
    "description": "Look up a deterministic v1.1 filter decision in the archived JS3 corpus.",
    "inputSchema": {
        "type": "object",
        "properties": {"board": {"type": "string"}, "id": {"type": "string"}},
        "required": ["board", "id"],
        "additionalProperties": False,
    },
    "annotations": {"readOnlyHint": True, "openWorldHint": False},
}


def load_scores():
    with SCORES.open(encoding="utf-8") as source:
        rows = map(json.loads, source)
        return {(row["board"], row["id"]): row for row in rows}


class ScoreServer:
    def __init__(self, scores):
        self.scores = scores
        self.state = "new"

    def reply(self, request):
        identifier = request.get("id")
        method = request.get("method")
        if request.get("jsonrpc") != "2.0" or not isinstance(method, str):
            return self.error(identifier, -32600, "Invalid request")
        if "id" not in request:
            if method == "notifications/initialized" and self.state == "initializing":
                self.state = "ready"
            return None
        if method == "initialize" and self.state == "new":
            self.state = "initializing"
            result = {
                "protocolVersion": VERSION,
                "serverInfo": {"name": "js3-score", "version": "1.0.0"},
                "capabilities": {"tools": {}},
            }
        elif method == "ping":
            result = {}
        elif self.state != "ready":
            return self.error(identifier, -32002, "Server is not initialized")
        elif method == "tools/list":
            result = {"tools": [TOOL]}
        elif method == "tools/call":
            result = self.call(request.get("params"))
            if result is None:
                return self.error(identifier, -32602, "Expected lookup_score with board and id strings")
        else:
            return self.error(identifier, -32601, "Method not found")
        return {"jsonrpc": "2.0", "id": identifier, "result": result}

    @staticmethod
    def error(identifier, code, message):
        return {"jsonrpc": "2.0", "id": identifier, "error": {"code": code, "message": message}}

    def call(self, params):
        if not isinstance(params, dict) or params.get("name") != TOOL["name"]:
            return None
        args = params.get("arguments")
        if (
            not isinstance(args, dict)
            or set(args) != {"board", "id"}
            or not all(isinstance(value, str) for value in args.values())
        ):
            return None
        score = self.scores.get((args["board"], args["id"]))
        if score is None:
            return {"isError": True, "content": [{"type": "text", "text": "No archived score for that board and id."}]}
        return {"content": [{"type": "text", "text": json.dumps(score, ensure_ascii=False)}]}


def serve(server, source, sink, transcript=None):
    def record(direction, line):
        if transcript:
            print(json.dumps({"direction": direction, "line": line}), file=transcript, flush=True)

    for line in source:
        record("client_to_server", line.rstrip("\r\n"))
        try:
            request = json.loads(line)
        except ValueError:
            response = server.error(None, -32700, "Parse error")
        else:
            response = (
                server.reply(request) if isinstance(request, dict)
                else server.error(None, -32600, "Invalid request")
            )
        if response is not None:
            wire = json.dumps(response, ensure_ascii=False)
            print(wire, file=sink, flush=True)
            record("server_to_client", wire)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transcript", type=Path, help="capture both directions to a new local JSONL file")
    args = parser.parse_args()
    with (args.transcript.open("x", encoding="utf-8") if args.transcript else nullcontext()) as log:
        serve(ScoreServer(load_scores()), sys.stdin, sys.stdout, log)


if __name__ == "__main__":
    main()
