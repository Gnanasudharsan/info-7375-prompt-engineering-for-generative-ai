"""Probe @modelcontextprotocol/server-filesystem@2.4.0 with a from-scratch stdlib MCP client.
Allowed dir = a fresh temp folder. Never calls a write tool. Logs every line both ways to transcripts/."""
import json, os, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

PKG = "@modelcontextprotocol/server-filesystem@2.4.0"
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%MZ")
log = open(f"transcripts/filesystem_probe_{ts}.jsonl", "x")
root = Path(tempfile.mkdtemp(prefix="fsprobe-")).resolve()
outside = Path(tempfile.mkdtemp(prefix="fsoutside-")).resolve()
(root / "inside.txt").write_text("hello from inside the allowed folder\n")
(outside / "secret.txt").write_text("this file is OUTSIDE the allowed folder\n")
os.symlink(outside / "secret.txt", root / "link_to_outside.txt")

p = subprocess.Popen(["npx", "-y", PKG, str(root)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=open(f"transcripts/filesystem_probe_{ts}.stderr.txt", "w"), text=True, bufsize=1)
def note(direction, line):
    log.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "direction": direction, "line": line}) + "\n"); log.flush()
def send(msg):
    line = json.dumps(msg); note("client_to_server", line); p.stdin.write(line + "\n"); p.stdin.flush()
def wait(i, timeout=60):
    end = time.time() + timeout
    while time.time() < end:
        line = p.stdout.readline()
        if not line: break
        note("server_to_client", line.rstrip("\n"))
        m = json.loads(line)
        if m.get("id") == i: return m
    raise SystemExit(f"no reply for id {i}")
n = 0
def req(method, params=None):
    global n; n += 1
    send({"jsonrpc": "2.0", "id": n, "method": method, **({"params": params} if params is not None else {})}); return wait(n)
def call(name, args):
    r = req("tools/call", {"name": name, "arguments": args})["result"]
    return {"isError": r.get("isError", False), "text": " ".join(c.get("text", "") for c in r.get("content", []))[:200]}

init = req("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "gnanasudharsan-probe", "version": "1"}})
print("server:", init["result"].get("serverInfo"), "| protocol:", init["result"].get("protocolVersion"))
send({"jsonrpc": "2.0", "method": "notifications/initialized"})
tools = req("tools/list")["result"]["tools"]
print(f"\n{len(tools)} tools declared:")
for t in tools:
    print(f"  {t['name']:<28} annotations={t.get('annotations')}")
names = {t["name"] for t in tools}
read = "read_text_file" if "read_text_file" in names else "read_file"
print("\nallowed:", call("list_allowed_directories", {}))
print("inside :", call(read, {"path": str(root / "inside.txt")}))
print("outside:", call(read, {"path": str(outside / "secret.txt")}))
print("dotdot :", call(read, {"path": str(root) + "/../" + outside.name + "/secret.txt"}))
print("symlink:", call(read, {"path": str(root / "link_to_outside.txt")}))
p.stdin.close(); p.terminate()
print(f"\ntranscript: transcripts/filesystem_probe_{ts}.jsonl")
