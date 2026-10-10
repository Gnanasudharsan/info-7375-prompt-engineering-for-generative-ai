# Alternatives test — NotebookLM and ChatGPT

**What I tested.** I gave two existing tools the same six documents and the
same four questions. I wanted to see whether each tool could:

- find the current decision,
- notice that an earlier decision had been reversed,
- name who approved the change,
- refuse to answer a question the documents don't answer.

Q4 asks for a migration budget, and no document gives one.

**The test pack is synthetic.** `test-pack/` holds six documents about a
fictional company, "Northwind Logistics", plus `questions.txt`. Claude Code
generated them on 2026-10-09 from a spec I wrote. They contain no real
company, people or data, and every file is labelled `SYNTHETIC`.

**Answer key.** The answer key was drafted by Claude (claude.ai chat, 2026-10-09) from the six docs before any tool was asked Q1–Q4, and checked by me against the docs. The NotebookLM auto-summary appeared on upload, before the key existed.

**Tools and dates.**

| Tool | Tried | How |
|---|---|---|
| NotebookLM | 2026-10-09 | Run 1: all four questions in one message. Run 2: one question at a time. I also checked its auto-generated summary. |
| ChatGPT | 2026-10-09 | One run, one question at a time, all 6 docs attached, no extra instructions. |

**Screenshots.** Everything in `screenshots/` is an unedited capture taken
on 2026-10-10. There is no screenshot of NotebookLM run 1; I copied that
answer text into `alt-notes.md` on 2026-10-09.

**Files**

- `alt-notes.md`: answer key, a grade for each question, and findings for
  each tool.
- `test-pack/`: the 6 synthetic documents and `questions.txt`.
- `screenshots/`:
  - `2026-10-10_notebooklm_summary.png`
  - `2026-10-10_notebooklm_run2_q1–q4.png`
  - `2026-10-10_chatgpt_q1–q4.png`
