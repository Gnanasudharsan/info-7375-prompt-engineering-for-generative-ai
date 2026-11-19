# Job-Search Agent 3 — The Filter, the Tool, and the Score

This project builds on the JS2 collection and judge loop copied at `9ef84715`. It adds a versioned filter, hand audit, evidence-checked shortlist, and a read-only archived score tool. For NEU students, the university portal provides Claude Code access. Public readers need their own Claude Code account. The Python replay and tests run offline and need no account keys.

## Toolchain and commands

Verified with Python 3.15.2, the pinned dependencies in `requirements.txt`, and Claude Code 2.1.328 for the live tool demo. The server and evaluation code use Python's standard library.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python scripts/check_labels.py
.venv/bin/python scripts/review_claims.py --status
.venv/bin/python scripts/evaluate_js3.py --allow-partial-claims
```

Run the evaluation without `--allow-partial-claims` to require all 75 confirmed rows. Use `python3 scripts/review_claims.py --batch` for human review of the Codex classifications.

Replay into a scratch directory to protect the archived outputs.

```sh
replay_dir=$(mktemp -d)
ln -s "$PWD/runs/20261119T162945Z/raw" "$replay_dir/raw"
PYTHONPATH=. .venv/bin/python scripts/run_filter.py "$replay_dir"
for change in C1 C2 C3 C4 C1,C4; do
  PYTHONPATH=. .venv/bin/python scripts/run_filter.py "$replay_dir" --changes "$change"
done
```

To start the offline MCP stdio server, run `python3 -m jobwatch.mcp_score` from this directory. For a live Claude Code run, from the same directory use a fresh transcript path.

```sh
mcp_config='{"mcpServers":{"js3-score":{"command":"python3","args":["-m","jobwatch.mcp_score","--transcript","evidence/mcp_reproduction.jsonl"]}}}'
claude -p --tools '' --strict-mcp-config --mcp-config "$mcp_config" \
  --allowedTools mcp__js3-score__lookup_score --setting-sources '' --no-session-persistence \
  --output-format stream-json --verbose \
  'Use lookup_score for board greenhouse:anthropic and id 5198255008. Report the archived decision and score.'
```

## Evidence and submission status

| Requirement | File and status |
|---|---|
| Versioned filter, evidence rules, wrong versions | [FILTER.md](FILTER.md), [filter code](jobwatch/filter.py), [tests](tests) |
| Reject audit, close calls, keeps, false friend and uncertainty | [Audit report](audit/AUDIT.md) and the two hand-verdict CSVs in [audit](audit) |
| Evidence-grounded shortlist | [Original proposals](shortlist/shortlist_v1_1.json), [human labels](shortlist/claim_labels.csv), and [44 Codex classifications](shortlist/CODEX_REVIEW.md). Human approval remains open for 44 claims. |
| Tool server, real transcript and both server evaluations | [MCP.md](MCP.md), with links to the captures. Student trust decisions remain open. |
| One change at a time and held-out evaluation | [SCORE.md](SCORE.md). Independent development comparisons complete. Fresh, hand-labeled held-out evaluation remains open. |
| Driver's seat and sign-off | [SIGN_OFF.md](SIGN_OFF.md). Student signature remains open. |
| Provenance and Frictional | [SOURCES.md](SOURCES.md), [FRICTIONAL.md](FRICTIONAL.md) |
| GitHub and Canvas | Draft package prepared for review. Final posted commit and matching submission remain open. |

The v1.1 filter kept the Post-Training Model Evaluations posting with a score of 5. The student's review marked the role claim insufficient against the original excerpt. The [Codex review report](shortlist/CODEX_REVIEW.md) records the additional duties visible in the full posting and preserves the student's verdict. This is an example of why a keyword score alone cannot support a claim.

The course-wide validator was also run. Its output reported broken links and non-Python implementations elsewhere in the course repository. The JS3 test output and exact replay checks are retained in [evidence](evidence).

Also from the same Codex session (files dated 16:03 ET), found untracked later the same day and moved here unchanged:
README.md, SCORE.md and SIGN_OFF.md (drafts of my README, score report and sign-off), and an edit to my FILTER.md changelog
(saved as FILTER_md_codex_edit.diff and reverted). I write my own versions; these are not used.
