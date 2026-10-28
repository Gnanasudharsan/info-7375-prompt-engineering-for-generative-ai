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