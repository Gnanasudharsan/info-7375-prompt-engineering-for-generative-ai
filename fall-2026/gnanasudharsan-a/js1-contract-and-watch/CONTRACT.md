# CONTRACT — Job-Search Agent 1
Author: Gnanasudharsan Ashokumar · Written 2026-10-28, before any implementation.

## In
- Board: Greenhouse public JSON API, host `boards-api.greenhouse.io`, token `anthropic`,
  endpoint `/v1/boards/anthropic/jobs?content=true`
- Résumé: `persona/ananya-rao.resume.json` (fictional persona from the-reallocation-engine,
  extended by me with labeled additions: `target_roles` ["Machine Learning Engineer", "AI Engineer", "Applied NLP Engineer", "ML Engineer"], `willing_to_relocate_us: true`, and `needs_sponsorship: true`)
- The résumé must pass a schema check before anything runs: must contain `personal.name`, `skills.languages`, `skills.ml_nlp`, `skills.backend_automation`, `skills.database_cloud`, `skills.familiar_with_not_shipped`, plus the added fields `target_roles`, `willing_to_relocate_us`, and `needs_sponsorship`. Also includes a testable refusal check: refuses to load any résumé whose email does not end in `@example.com` or whose phone is not a 555 number.
- Also needs: `state/seen_ids.json`, `data/raw/`, hardcoded host allow-list checking against `boards-api.greenhouse.io`, and `ANTHROPIC_API_KEY` exclusively loaded for the Claude judge.

## Out
For each posting whose `id` is not in the state file:
- Fields in each result record: `id`, `title`, `location`, `department`, `updated_at`, `rule_verdict`, `claude_verdict`, `justification`
- Rule verdict: RELEVANT / NOT_RELEVANT — labeled "record (recomputable)" with justification explicitly citing: the matched phrase from `title`, the matched part of `location.name`, the sponsorship check result from `content`, and each matched skill with its exact résumé path (e.g., `skills.ml_nlp`).
- Claude verdict: JSON object containing `id` (must match the posting id to prevent pairing mix-ups), `verdict: "RELEVANT" | "NOT_RELEVANT"`, `reasoning: string`, `resume_fields_cited: array`, and `posting_fields_cited: array` (each citation array must be non-empty and drawn from known schema/posting field paths) — labeled "judgment (model output, not fact)"
- First run: Baseline run reporting 0 new postings and initializing `seen_ids.json`

## Refuses
- Host allow-list rule: Any URL or request targeting a host other than `boards-api.greenhouse.io` triggers an immediate `ValueError` and halts execution.
- Real résumé: Refuses to load any résumé whose email does not end in `@example.com` or whose phone is not a 555 number, keeping real personal data entirely off-screen and excluded from repository tracking via `.gitignore` rules covering `private/` and local credential files.
- Model judgment as fact: Enforced in the output schema and prompt instructions by separating the deterministic rule verdict from the probabilistic Claude verdict, rendering both with distinct labels.
- Apply / email / message / log in: The agent strictly lacks any execution or network capabilities for submitting forms, sending emails, logging in, or interacting with application portals.
- Claude output that fails the validator: Any response failing the strict JSON schema validation, missing matching pairing ids, or containing empty citations triggers 1 retry, then is logged as `judgment_unavailable` (the rule verdict still stands without crashing the run loop).

## The rule
Text cleaning and matching: Title and content are both trimmed and lowercased; all title, seniority, and skill matches are case-insensitive whole-word or phrase matches. Content undergoes double unescaping of HTML entities and HTML tag stripping prior to matching.
A posting is RELEVANT if and only if ALL of these hold:
1. Title: Contains whole-word or phrase matches for any of Ananya's target roles (`machine learning engineer`, `ai engineer`, `applied nlp engineer`, `ml engineer`).
2. Seniority: Does not contain exclusion whole words in the title: `senior`, `lead`, `staff`, `principal`, `manager`, `director`, `vp`, `head`, `distinguished`.
3. Location: RELEVANT on location if any part (split by `|` or `;`) matches either: (a) containing `"united states"` or ending with `, dc` or any of the 50 US state postal codes (`, al`, `, ak`, `, az`, `, ar`, `, ca`, `, co`, `, ct`, `, de`, `, fl`, `, ga`, `, hi`, `, id`, `, il`, `, in`, `, ia`, `, ks`, `, ky`, `, la`, `, me`, `, md`, `, ma`, `, mi`, `, mn`, `, ms`, `, mo`, `, mt`, `, ne`, `, nv`, `, nh`, `, nj`, `, nm`, `, ny`, `, nc`, `, nd`, `, oh`, `, ok`, `, or`, `, pa`, `, ri`, `, sc`, `, sd`, `, tn`, `, tx`, `, ut`, `, vt`, `, va`, `, wa`, `, wv`, `, wi`, `, wy`), explicitly excluding international codes like `, ie` and `, ch`; or (b) starting with `remote-friendly` or `remote`.
4. Sponsorship: Does not contain the negative phrase `"not currently able to sponsor"` in the content body, overriding positive sponsor boilerplate.
5. Skills: Matches at least 3 distinct core shipped skills from `skills` using exact string matches: `"python"`, `"pytorch"`, `"sql"`, `"hugging face transformers"`, `"sentence-transformers"`, `"fastapi"`, `"mlflow"`, `"postgresql"`, `"aws"` (matched case-insensitively). Mentioning a skill multiple times counts as 1 distinct match; `familiar_with_not_shipped` items like `"kubernetes"` and `"ray"` plus `agent_note` are strictly ignored.
Otherwise NOT_RELEVANT.

## Wrong versions (my tests must catch these)
1. `lax_seniority_matcher` — caught by test `test_rejects_senior_titles` using input title `"Senior AI Engineer"` with expected verdict `NOT_RELEVANT`.
2. `ignoring_sponsorship_trap` — caught by test `test_respects_negative_sponsorship_boilerplate` using posting content containing both positive sponsorship boilerplate and the negative phrase `"not currently able to sponsor visas for fellows"` with expected verdict `NOT_RELEVANT`.

## What a failure looks like
2026-10-28: A failure would be if an HTML entity unescaping bug caused description text to retain entity codes, preventing regex skill extraction from recognizing exact skill strings like `"PyTorch"`.

## Amendment 1 — 2026-10-28 (after the first offline run on real data)
Where this amendment conflicts with the sections above (conditions 1 and 5, and the allow-list in In and Refuses), this amendment governs.

Reason: The initial rule execution on real Greenhouse board data (commit b1f1e45) yielded 0 relevant postings. Analysis of the per-condition breakdown showed two binding constraints: strict title matching limited matches to 10 postings (all titled "Applied AI Engineer"), and the requirement of at least 3 shipped skills yielded 0 overlapping postings because none of the title matches contained 3 or more shipped skills.

Evidence: Testing variant hypothetical rule sets yielded: Variant A (threshold 1) = 2 matches; Variant B (threshold 2) = 0 matches; Variant C (threshold 1 + "research engineer") = 21 matches; Variant D (threshold 2 + "research engineer") = 7 matches (computed offline by Claude Code from data/raw/anthropic_20261028T192103Z.json; output saved in `evidence/amendment1_variant_counts_2026-10-28.txt`). Variant D was selected because a skill threshold of 2 maintains rigorous filtering (avoiding single-keyword false positives) while "research engineer" unlocks Anthropic's actual core ML/AI role nomenclature, yielding a healthy sample size of 7 relevant jobs without breaking existing test coverage.

Changes:
1. Skills threshold: Lowered from 3 to 2 distinct shipped skills.
2. Title phrases / target_roles: Added `"research engineer"` to Ananya's target title phrases and `target_roles` in her persona, labeled as a persona extension reflecting Anthropic's primary ML engineering nomenclature.
3. Allow-list: Expanded to two allowed hosts with stated purposes: `boards-api.greenhouse.io` (for public job board data fetching) and `api.anthropic.com` (for executing the Claude judge model).
4. Known limits: 
   - The `"Remote"` location prefix passes remote postings regardless of country code or region if no specific domestic restriction is parsed.
   - Anthropic “Research Engineer” roles may expect research depth beyond a new-grad profile; the rule doesn’t check this.

Tests changed: No test in tests/test_rule_contract.py was changed; all original tests still pass at threshold 2. Added test_amendment1_research_engineer_title_is_a_role_match and test_amendment1_two_skills_is_enough before implementation. Implementing the amendment broke two of Claude Code's own tests, which were updated: test_skill_mentioned_many_times_counts_once (now uses one repeated skill, so it tests dedup independent of the threshold) and test_real_persona_file_loads (expected target_roles now includes "Research Engineer").