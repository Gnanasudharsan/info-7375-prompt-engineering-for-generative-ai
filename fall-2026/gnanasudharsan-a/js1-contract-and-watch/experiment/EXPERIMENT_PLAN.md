# Prompt experiment plan — written 2026-10-29 before any experiment call
- Backend claude_cli, model claude-opus-5-5, 1 fresh call per posting per prompt.
- Ground truth: my hand labels in experiment/labels_dev.json and labels_heldout.json (commit 4d5278c).
- Step 1: baseline prompt (prompts/judge_baseline.md, commit 7cfc8e5) on all 10 dev postings.
- Step 2: choose exactly ONE change, based only on the dev results, and write prompts/judge_revision.md = baseline + that one change. Commit it before running.
- Step 3: revision on the same 10 dev postings.
- Step 4: only then run baseline and revision on the 10 held-out postings, which I will not look at before this step.
- Metric: pass rate = calls whose verdict matches my label, out of calls made (judgment_unavailable counts as a miss).
- Known limit before starting: the sampling run showed the same prompt can split 3-1 on one posting, so a 1-2 posting difference between prompts may be noise.
