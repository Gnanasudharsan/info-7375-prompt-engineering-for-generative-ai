# Claude runs, 2026-10-21

- **Model:** Claude Opus 5.5 (`claude-opus-5-5`), run as three separate Claude Code subagents
  in one session on 2026-10-21. No API key; no tools; each saw only `prompt.txt`.
- **Blind:** the prompt holds the schema and the eight questions. It does not contain the gold
  SQL, the variants, or any result.
- **Raw output:** `run1_raw.json`, `run2_raw.json`, `run3_raw.json` are each subagent's full
  reply, saved unedited.
- **Scored by:** `python3 ../../score_claude_runs.py` (offline; executes each query read-only and
  compares rows with the gold answer).
