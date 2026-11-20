# SOURCES.md — who and what contributed (JS3)

## People
- **Me (Gnanasudharsan Ashokumar):** every hand label (audit v1: 50, audit v2: 30, held-out: 28, first-pass shortlist claim labels), every prediction,
  the decisions on every rule change, the trust decisions, the sign-off. Persona Ananya Rao is fictional (persona/).

## AI tools
- **Claude (chat, claude.ai), 2026-11-19:** planned the steps; drafted FILTER.md v1.0 and v1.1 tables (I edited and committed them), the tests
  (tests/test_filter.py, test_filter_v11.py, test_mcp_server.py), mcp/TOOL_SPEC.md, the scripts in scripts/ except those listed under Claude Code and Codex,
  and drafts of AUDIT.md, SHORTLIST.md, SCORE.md, mcp/EVALUATION.md and this README (generated from my labels and evidence; I reviewed them).
- **Claude Code 2.1.x, default permission mode, three build sessions (every action approved by me):**
  1475c16e (jobwatch/filter.py, scripts/run_filter.py; evidence/claude_code_filter_build_choices_2026-11-19.txt),
  the v1.1 switches in the same session (evidence/claude_code_v11_build_choices_2026-11-19.txt),
  645fc518 (mcp/server.py; evidence/claude_code_mcp_build_choices_2026-11-19.txt). Also the MCP client in the two real sessions (transcripts/claude_code_session_*).
- **Claude (model behind `claude -p`)** as the judge in the score experiments (evidence/score_claude/), with the JS1 prompts.
- **Codex (OpenAI), 2026-11-19 ~16:00 ET:** asked only to check shortlist labels. It suggested labels for 44 claims (shortlist/CODEX_REVIEW.md,
  claim_suggestions.json, codex_* columns), replaced scripts/review_claims.py (the reviewer that ran in my second pass), and, without being asked, wrote an
  MCP server, docs, drafts of README/SCORE/SIGN_OFF and a FILTER.md edit. All unrequested files are in codex_unrequested/ unchanged and are not used.

## Code and data I did not write
- JS1/JS2 code carried over (jobwatch/ loop, transport, normalize, policy, claude_judge, persona; prompts/; tests) from my own earlier assignments.
- Job postings: public Greenhouse (anthropic), Ashby (notion) and Lever (spotify) board APIs, collected once on 2026-11-19 (runs/20261119T162945Z).
- @modelcontextprotocol/server-filesystem 2.4.0 (npm, github.com/modelcontextprotocol/servers), evaluated, not modified.
- Python standard library; requirements.txt packages.
