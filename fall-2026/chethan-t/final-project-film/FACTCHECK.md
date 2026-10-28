# FACTCHECK — API Impact, the pitch

Every factual claim the film makes, where it comes from, and its status. Checked 2026-10-13; re-checked 2026-10-25 after the TA-requested narration edits (B01, B03, B06, B08, B09, B11, B12).

| Beat | Claim | Source / how checked | Status |
|---|---|---|---|
| B00 | Target role and status ("Planned — design and evaluation plan") | Chethan's own statements, 2026-10-13 | Self-reported, accurate |
| B01 | The street-renaming comparison | An analogy, not a factual claim. Every tool behavior in it is "will" | Analogy |
| B03 | oasdiff compares two OpenAPI versions and flags breaking changes. It runs in CI, and there is a GitHub Action | Public docs and listings for oasdiff (github.com/oasdiff/oasdiff, formerly Tufin/oasdiff) | Supported |
| B03 | oasdiff flags the break but doesn't find the frontend lines | Chethan ran oasdiff 1.34.1 on 2026-10-25 against a planted `Profile.username` → `handle` rename (fork commit 85c2a15). 12 errors, all `response-required-property-removed`; output names API paths and response fields only, no frontend files. See `evidence/` | Real run |
| B03 | Optic diffs OpenAPI versions, flags breaking changes in CI and adds changelogs to PRs | Public Optic repo, docs and blog posts (github.com/opticdev/optic) | Supported |
| B03 | Neither tool finds the frontend lines or opens fix PRs in consumer repos | Neither project describes scanning or editing consumer repos. This is a claim that the feature is absent, based on their own descriptions. For oasdiff this is now confirmed by Chethan's own run (row above). Optic he knows only from its docs, so the narration says "tools like," not "I looked at" | Supported (oasdiff: confirmed by run; Optic: soft) |
| B04 | "A plain search… returns" (not "I ran"): 171 whole-word matches for `username` in 23 files. 124 of them are in `*.spec.ts` | Ran `grep -rnw --include=*.ts --include=*.html username src` on gothinkster/angular-realworld-example-app @ dd99ed2 (commit dated 2026-05-13), cloned 2026-10-13 | Real run |
| B04 | The four sample lines (auth.component.html:21, profile.routes.ts:9, user.service.ts:17, profile.component.html:17) | Copied from that grep output. The comment line is shortened with "…" | Real |
| B05 | The call chain profile.service.ts:19–20 → profile.component.ts:54–55 → profile.component.html:11,17 | Line numbers checked with `grep -n` at dd99ed2. The type argument on line 19 is shortened to `<…>`, and line 20's `(data: { profile: Profile })` to `(data)` | Real, lightly shortened |
| B07 | Cited lines follow-button.component.ts:34 and profile.component.html:15 | Real lines at dd99ed2. The FIX PR / LIST ONLY / DROPPED verdicts are constructed, because the verifier doesn't exist | Lines real, verdicts constructed and labelled |
| B08 | The draft fix PR (diff, tsc ✓ / tests ✓, "waiting for human review") | Constructed mock-up of planned v1 output, labelled on screen. The diff line is the real profile.component.html:17 | Constructed |
| B09 | About 20 planted changes, three metrics, two baselines | From the project plan. No results exist, and every cell reads "no result yet" | Planned |
| B12 | Angular / TypeScript background | Public repo github.com/chethangowda-git/ms_node_project (Angular frontend with 5 components, Node.js backend; Chethan's own commits, pushed 2026-01-03). The 2026-10-14 cut said "none of that work is public yet," which was out of date (the repo was already on GitHub). Re-recorded 2026-10-25 as "some of that work is on my GitHub"; the on-screen tag now reads "Experience · on GitHub" | Public evidence |

## Corrections made while scripting
- Specmatic was dropped from the comparison. Claude hadn't checked it, and the assignment asks only for alternatives "you actually looked at."
- "The tool finds N real reads" was never claimed. Only the grep counts are numbers, and those are real.
- The tool is never described in past tense.
