import json
from io import StringIO

from jobwatch.mcp_score import VERSION, ScoreServer, load_scores, serve


def test_lookup_protocol_and_read_only_boundary():
    def request(method, identifier=None, params=None):
        message = {"jsonrpc": "2.0", "method": method}
        if identifier is not None:
            message["id"] = identifier
        if params is not None:
            message["params"] = params
        return json.dumps(message) + "\n"

    board, posting = "greenhouse:anthropic", "5198255008"

    def call(identifier, name, arguments):
        return request("tools/call", identifier, {"name": name, "arguments": arguments})

    messages = [
        request("tools/list", 1),
        request("initialize", 2, {"protocolVersion": VERSION}),
        request("notifications/initialized"),
        request("tools/list", 3),
        call(4, "lookup_score", {"board": board, "id": posting}),
        call(5, "lookup_score", {"board": board, "id": "missing"}),
        call(6, "lookup_score", {"board": board, "id": posting, "path": "unused"}),
        call(7, "write_file", {"board": board, "id": posting}),
        "{\n",
    ]
    stdout = StringIO()
    serve(ScoreServer(load_scores()), StringIO("".join(messages)), stdout)
    replies = list(map(json.loads, stdout.getvalue().splitlines()))
    assert len(replies) == 8
    assert replies[0]["error"]["code"] == -32002
    assert replies[1]["result"]["protocolVersion"] == VERSION
    assert [tool["name"] for tool in replies[2]["result"]["tools"]] == ["lookup_score"]
    assert json.loads(replies[3]["result"]["content"][0]["text"]) == load_scores()[board, posting]
    assert replies[4]["result"]["isError"]
    assert [reply["error"]["code"] for reply in replies[5:]] == [-32602, -32602, -32700]
