# Action-surface comparison — Job-Search Agent 1 (Chapter 3)
Same task three ways on posting 4613568008 with prompts/judge_baseline.md, 2026-10-29. Evidence files are in `experiment/action_surface/`.

| | Mode 1: paste into chat | Mode 2: Claude reads a file | Mode 3: agent fetches + writes state |
|---|---|---|---|
| Can read | Only what I pasted into the conversation (prompt, posting, persona). | Anything my user account can read, via raw Bash. It used this to list its temp folder and read posting_task.txt. Started in the project folder, it could have read `labels_*.json`. | Anything my user account can read, via raw Bash, plus the internet via `curl`. |
| Can write | Nothing on my machine; I saved the reply by hand. | Anything my user account can write, via Bash. It wrote nothing (folder unchanged: `mode2_folder_check.txt`). | Anything my user account can write, via Bash. It wrote files in a scratchpad outside the sandbox and a `state.json` with its own schema inside it. |
| Can send | The pasted text to Claude.ai; nothing else. | The file's contents to the model; it ran no network commands. | Network requests via `curl` (it fetched the Greenhouse board), plus everything it read, to the model. |
| Authority needed | Minimal: only my Claude login. | Auto mode with raw Bash, the same as Mode 3, even though the task needed only one file read. | Auto mode with raw Bash and internet access; every step approved by the auto-mode classifier, not by me. |
| What could go wrong | Pasting the wrong text (my clipboard was overwritten twice while preparing this), and no automatic record of the call. | Reading private files such as my labels if not started in an isolated folder; with Bash it could also have run other commands without asking. | Contacting hosts off my allow-list (nothing enforced it), writing outside the sandbox, inventing an incompatible state format, mishandling the data (e.g. double-escaped HTML), and not keeping raw evidence. |
| What actually happened | Valid JSON reply on the first try. | One Bash command, `cat …/posting_task.txt; ls -la …`, approved by the auto-mode classifier with no prompt to me. | Bash only, auto-approved: `curl` from `boards-api.greenhouse.io` only (by its own choice), wrote `dl/jobs.json`, `dl/fetched_at.txt`, `extract.py` and `ids.json` to a scratchpad outside the sandbox, unescaped HTML once on double-escaped content, then wrote `state.json` in the sandbox. The raw download was not kept in my evidence. |
| Verdict / validator | RELEVANT, passes my validator. | RELEVANT, passes my validator. | NOT_RELEVANT, passes my validator. |
| Evidence | `mode1_input.txt`, `mode1_reply_2026-10-29.json`, `mode1_validation.txt`, `mode1_notes.md` | `mode2_reply_2026-10-29.json`, `mode2_validation.txt`, `mode2_folder_check.txt`, `mode2_tool_summary.txt`, `mode2_notes.md` | `mode3_reply_2026-10-29.json`, `mode3_validation.txt`, `mode3_tool_log.txt`, `mode3_folder_check.txt`, `mode3_agent_state.json`, `mode3_notes.md` |

## Least autonomy that suffices

The optimal architectural choice is a hybrid design: keep data ingestion, allow-listing, string cleaning (such as handling double-escapes), and state tracking strictly inside deterministic Python code that I test and control, while restricting the LLM judge to text-only evaluation (`--tools ""` inside an isolated, empty temporary working directory).

This approach provides Mode 1's limited authority in an automated pipeline, avoiding the risks demonstrated by Mode 3 — unconstrained Bash access, files written outside the sandbox, an improvised state schema, single-unescaped content, and no preserved raw evidence.

Modes 2 and 3 also show that in Claude Code the authority comes from the tool settings, not the task: a one-file read ran with the same auto-approved raw shell as the full fetch-and-write agent. My watch already uses the hybrid design: Amendment 2's safeguards (no tools, empty temp folder, no session persistence), used in run 2 (`b04c897`), with `num_turns 1` and a temp working folder verified in the smoke test (`96de51f`). Even this design sends the fictional persona and the posting text to Anthropic.

## Limits

This comparison cannot attribute verdict differences to the operating mode: it used one posting with one call per mode, and posting `4613568008` split 3–2 across earlier evaluations. Modes 2 and 3 ran with auto mode on; under default, user-prompted permissions their behavior (and the approvals required) would differ, and I did not test that. Each tool call appears twice in the local session logs, which I believe is a logging artifact rather than a second run, but I did not verify it.
