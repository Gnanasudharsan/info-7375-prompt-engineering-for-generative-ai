## Shortlist review assistance

On 2026-11-19, Codex read the archived Greenhouse descriptions for the nine postings with pending claims and recorded 44 Codex-generated classifications in `shortlist/claim_suggestions.json`. It used the fictional Ananya Rao résumé, the evidence rules in `FILTER.md`, and the original board snapshot at the path recorded in the JSON. For skills, Codex checked overlap with documented skills and project work. Where a generic skill match left a central requirement unclear, Codex used INSUFFICIENT. Codex implemented the batch reviewer and verified that each quoted excerpt appears in the snapshot.

Run `python3 scripts/review_claims.py --batch` from the project directory. Each screen covers the pending claims for one posting. Press `v` for its full archived description, enter a claim number to edit a label, and press `a` to explicitly approve and save the displayed batch. Press `n` to skip a posting or `q` to leave and resume later. A suggestion that changes the original proposal carries its attributed Codex rationale into the review CSV only when explicitly approved. Student-written notes are entered through the edit action.

## Filter, scoring and tool evidence

- JS2 code copied at `9ef84715`. The prior Claude Code filter contributions are recorded in `evidence/claude_code_filter_build_choices_2026-11-19.txt` and `evidence/claude_code_v11_build_choices_2026-11-19.txt`. Student audit verdicts and post-unblind corrections are in the original audit CSVs.
- The archived Greenhouse, Ashby and Lever board responses for run `20261119T162945Z` supply the filter inputs. `boards.json` records the endpoints and `runs/20261119T162945Z/report.md` records collection scope and the excluded failing board.
- Codex wrote the standard-library MCP lookup, ran the Claude Code demo, evaluated the external reference server, and prepared the score report, reproducibility checks, and draft sign-off for student review.
- MCP wire design follows the published 2025-11-25 [stdio transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) and [tool messages](https://modelcontextprotocol.io/specification/2025-11-25/server/tools). External server version and pinned sources are in [MCP.md](MCP.md). Sources checked 2026-11-19.

- **Codex (OpenAI), 2026-11-19:** reviewed 44 shortlist claims and wrote suggested labels, quotes and reasons (shortlist/CODEX_REVIEW.md, shortlist/claim_suggestions.json). Kept as a separate, disclosed second opinion (codex_* columns); every final claim label is mine.
