# SOURCES — Job-Search Agent 2

## Starting materials
- My JS1 code (js1-contract-and-watch, final e0d0e7e): jobwatch/ (rule, persona, claude_judge, validator, watch, fetcher), tests, prompts, persona. Copied at d76a1a6.
- Fictional persona Ananya Rao from the-reallocation-engine examples (via JS1).
- Public board endpoints: Greenhouse boards-api, Ashby posting-api, Lever v0 postings.
- Not used: Lectern, the Reallocation Engine ATS providers or greenhouse-watch skill.

## What I wrote or decided
Board probe and choice of boards; GATE.md decisions (seconds rule added, values accepted) and Amendment 1; boundary-test predictions; gate_config.json and boards.json; every live and seeded run and its prediction; all FRICTIONAL entries; the review decision.

## What Claude contributed
- **Claude chat (claude.ai):** drafted GATE.md structure and proposed values, BOUNDARY_TESTS.md, the test code in tests/test_policy_boundary.py, test_loop.py and test_review_empty_board.py, scripts/seeded_run.py, check_run.py and wrong_versions.py, the recomputation snippets, REVIEW_PACKET.md, FINISHED_WRONG_ANSWER.md and README drafts. It also drafted the test_L6 setup bug, which I accepted without catching.
- **Claude Code 2.1.319, session 7096e7f8 (2026-11-06, default permission mode):** wrote jobwatch/policy.py, loop.py, transport.py, normalize.py; listed 29 choices GATE.md did not decide (evidence/claude_code_choices_2026-11-06.txt); diagnosed the test_L6 setup bug without editing tests/.
- **Claude Code, session 7a088b59:** the review patch (Amendment 1) in jobwatch/loop.py, +26 −2.
- Removed from the JS1 copy: tests/test_run_judge.py and the run_judge part of tests/test_claude_cli_backend.py (they test experiment/run_judge.py, which is not in JS2; a720410).
Session transcripts stay on my machine; only Claude Code's final build reply is committed, with its timestamp.
