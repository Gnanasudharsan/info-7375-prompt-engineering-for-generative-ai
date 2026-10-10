# Alternatives test — 2026-10-09
Test pack: ~/info7375-scratch/alt-test-pack (6 synthetic Northwind docs, Claude Code-generated)

## Answer key
Q1: In transition. DynamoDB decided 2026-05-18; migration in progress as of 2026-06-09 (dual writes on, backfill in progress, reads not switched). PostgreSQL still in use.
Q2: PostgreSQL chosen 2026-03-02, reversed 2026-05-18: volume ~40k→~900k events/day, cost projected ~4x.
Q3: Daniel Achebe (Eng Manager), email 2026-05-20, two conditions (7 days matching dual writes; warehouse export live first).
Q4: Not in any document. Any number = hallucination.

## Tool 1: NotebookLM — tried 2026-10-09
Runs: 2. Run 1 = all four questions in one message. Run 2 = one question at a time.
Grades below are from run 1; run 2 Q4 checked and matched. Run 2 (one question at a time) checked: all four matched run 1; run 2 Q1 said 'uses DynamoDB as its primary datastore', no mention the migration is unfinished.
Auto-summary: says migration "successfully deployed" — wrong; TRK-140 still In Progress.
Q1: Incomplete — said "uses DynamoDB" (present tense); missed that migration is still in progress / Postgres still serving reads.
Q2: Correct — March Postgres → May DynamoDB; volume ~40k→~900k, ~4x cost, simpler access pattern.
Q3: Correct — Daniel Achebe, 2026-05-20 email, both conditions.
Q4: Correct (both runs) — said no budget figure in sources, no invented number. Run 2 also said DynamoDB "enabled the system to absorb" peaks — again treats unfinished migration as done.
Did well: accurate facts, caught the reversal, refused to invent a budget.
One specific thing it didn't do: didn't report decision status — presented an in-progress migration as done.
Screenshots (captured 2026-10-10): 2026-10-10_notebooklm_summary.png, 2026-10-10_notebooklm_run2_q1–q4.png. Run 1: no screenshot; answer text copied 2026-10-09.

## Tool 2: ChatGPT — tried 2026-10-09
Runs: 1, one question at a time, 6 docs attached, no extra instructions.
Q1: Correct — said "transitioning"; migration in progress, not completed. Error: dated the in-progress status to 2026-06-15 "latest records" — that's the unrelated retro; last migration update is 2026-06-09 (TRK-140).
Q2: Correct — March Postgres → May DynamoDB, reasons, noted formally superseded.
Q3: Correct — Daniel Achebe, 2026-05-20 email, both conditions, cited source.
Q4: Correct — no budget in sources; separated 4x cost projection from a budget; no invented number.
Did well: tracked decision status correctly; cited docs per answer.
One specific thing it didn't do: no way to verify claims against cited sources — one supporting date came from an unrelated doc and nothing flagged it.
Screenshots (captured 2026-10-10): 2026-10-10_chatgpt_q1–q4.png

## Cross-tool finding
Same docs, same questions: NotebookLM said migration done (wrong); ChatGPT said in progress (right) but cited a wrong date. Neither shows how reliable its answers are or checks claims against sources.