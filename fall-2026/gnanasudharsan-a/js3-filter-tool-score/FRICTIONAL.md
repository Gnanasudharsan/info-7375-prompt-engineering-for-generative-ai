# FRICTIONAL — Job-Search Agent 3

## 2026-11-19 ~11:05–11:20 ET — Started the JS3 folder twice
I copied the JS2 code into js3-filter-tool-score at 9ef84715 (baseline: evidence/js2_baseline_in_js3_2026-11-19T1604Z.txt), then ran the copy again from a fresh chat. The second copy (e4b5939e) re-copied identical files; its only real additions were GATE.md and empty FILTER/FRICTIONAL/SOURCES files. Its message calls it the "starting point"; the real starting point is 9ef84715. Corrected here, not rewritten.
Checked: git log, the file contents, and git ls-files before continuing.

## 2026-11-19 ~11:45 ET — FILTER.md: dropped "research engineer", then restored it
I removed "research engineer" from B1 in 48c39853 without checking her résumé; resume.json target_roles lists "Research Engineer". Restored before any filter code existed, with the source named in the reason. profile.yml (primary/secondary roles) and resume.json (target_roles) disagree slightly; I treat resume.json as the fuller list.
