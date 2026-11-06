# Boundary tests — permission policy (GATE §6)
Predictions written 2026-11-06, before any policy code existed.
Interface under test: jobwatch/policy.py
- check_url(url, method="GET")        -> returns normally if allowed, raises PolicyViolation if not
- check_path(path, mode)              -> mode is "read" or "write"
- check_delete(path, approved=False)  -> deleting/resetting state/ needs approved=True (the --i-approve flag)

| # | case | input | predicted | catches GATE wrong version |
|---|---|---|---|---|
| B1 | allowed host, GET | GET https://api.lever.co/v0/postings/spotify?mode=json | ALLOW | baseline |
| B2 | host suffix trick | GET https://api.lever.co.evil.com/v0/postings/x | REFUSE | #3 |
| B3 | host prefix trick | GET https://evilapi.lever.co/v0/postings/x | REFUSE | #3 |
| B4 | off-list host | GET https://example.com/jobs | REFUSE | - |
| B5 | plain HTTP to allowed host | GET http://api.lever.co/v0/postings/spotify | REFUSE | - |
| B6 | write method to allowed host | POST https://boards-api.greenhouse.io/v1/boards/anthropic/jobs | REFUSE | - (never POST) |
| B7 | write inside runs/ | write runs/2026-11-06T1800Z/trace.jsonl | ALLOW | baseline |
| B8 | .. escape | write runs/../persona/ananya-rao.resume.json | REFUSE | #2 |
| B9 | prefix trick folder | write runs-evil/trace.jsonl | REFUSE | #1 |
| B10 | symlink escape | write runs/link/x.json where runs/link -> /tmp | REFUSE | #2 |
| B11 | absolute path outside | write /tmp/x.json | REFUSE | - |
| B12 | read vs write: read allowed | read persona/ananya-rao.resume.json | ALLOW | baseline |
| B13 | read vs write: same file, write | write persona/ananya-rao.resume.json | REFUSE | #10 |
| B14 | delete state without approval | delete state/seen_ids.json, approved=False | REFUSE | approval rule |
| B15 | delete state with approval | delete state/seen_ids.json, approved=True | ALLOW | approval rule |
| B16 | read outside allowed reads | read ../js1-contract-and-watch/CONTRACT.md | REFUSE | - |

Results column will be filled from the actual pytest output, not edited by hand.
