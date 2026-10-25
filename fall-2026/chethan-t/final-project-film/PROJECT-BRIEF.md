# PROJECT-BRIEF — API Impact

**Author:** Chethan Gowda (MS Information Systems, Northeastern) · **Target role:** AI Software Development Engineer · **Date:** 2026-10-14

**Status:** a plan. None of the tool is built yet, so every description of it below is in "will."

**1. What is it?**
Before a backend change merges, API Impact will find the frontend lines it breaks and open a draft fix pull request in each affected frontend repo, linked back to the backend PR. When it's done, it will be a public GitHub repository containing:
- a Python CLI on PyPI
- a GitHub Action (with a GitHub App for PR access to the frontend repos)
- an evaluation report on GitHub Pages

**2. Why would anyone care?**
It helps a backend engineer who is about to rename a field that other teams' frontends read. Tools like oasdiff and Optic already compare two OpenAPI versions and flag breaking changes in CI. On 2026-10-25 I ran oasdiff myself: I forked RealWorld and renamed `Profile.username` to `handle` ([commit 85c2a15](https://github.com/chethangowda-git/fork-realworld/commit/85c2a15ddf56ee41c224e7073776c97e7ad0cd2e)). It flagged 12 breaking changes across 12 endpoints, reported `username` as removed rather than renamed, and named no frontend files (see `evidence/`). I haven't used Optic; I know it only from its docs. They tell you the spec broke. They don't find the frontend lines that depend on it, and they don't fix them. Search-and-replace isn't a substitute. A plain search of the public Angular RealWorld frontend for `username` returns 171 matches in 23 files, and 124 of them are in tests. That search was run by Claude Code in my session on 2026-10-13. API Impact will trace the data from the API call to the property read, edit only those lines, and prove each edit with the frontend's own checks.

**3. Who opens it, and what do they do in the first 60 seconds?**
- **Hiring manager or engineer reviewing my portfolio:** opens the README. The first link is the eval report. Next to it is a real draft fix PR generated on the test bed.
- **End user, a backend developer:** sees the linked draft PRs appear in the frontend repos.
- **Frontend reviewer:** reads the diff and its passing checks, then decides whether to merge.

**4. What does it prove about me?**
If it works, it will be evidence for four skills, each backed by the eval report and the test suite:
- **Source grounding:** every edit is tied to a real `file:line`.
- **Verification:** every cited line is re-checked, and every fix must pass the frontend's type check and tests before a PR opens.
- **Prompt contracts:** Claude handles only what static analysis can't settle, with a fixed output format.
- **Evaluation:** catch rate, false alarms, citation accuracy and fixes passing tests. The baselines are plain search and "regenerate types + run tsc."

It will not show agent loops. This is a gated pipeline, and I won't claim otherwise.

**5. In, out, first.**
- **In:** renamed or retyped fields in OpenAPI specs, TypeScript frontends, and the repos listed in the config.
- **Out:** it will never merge its own fixes. It won't guess at deleted fields; it will flag those lines instead. GraphQL and non-OpenAPI APIs are out for v1.
- **First:** one planted rename in a RealWorld fork. The CLI finds the exact `file:line`, then opens one draft fix PR. Someone will know it ran because CI passes on that PR, and a pytest asserts the found location.

**6. What could sink it?**
A fix that compiles but is wrong, such as editing a `username` that actually came from a different endpoint.
- **What I'll do:** only confirmed lines get edited, every fix must pass the frontend's own tsc and tests, and PRs open as drafts that a person merges.
- **Underneath that:** tracing may not hold up on real Angular code (RxJS chains, generated clients). If it doesn't, I'll narrow v1 to one client pattern and say so in the report.

**7. Why this project?**
A mix, mostly learning.
- **Already have:** Angular and TypeScript, so I know the code on the receiving end of these breaks. Evidence: [ms_node_project](https://github.com/chethangowda-git/ms_node_project), a task app I built with an Angular frontend and a Node.js/SQL Server backend (pushed to GitHub 2026-01-03). It didn't involve the breaking-change problem itself.
- **New to me:** tree-sitter, oasdiff, writing GitHub Actions and Apps, Claude API structured output, and evaluating an AI that edits code.

**Exists today**
- This plan (PROJECT-BRIEF.md)
- The pitch video, its beat sheet and build files (this folder)
- One real measurement shown in the video: the `username` search on angular-realworld-example-app @ dd99ed2 (2026-10-13)
- One oasdiff run on a planted rename in my RealWorld fork, commit 85c2a15 (2026-10-25), with its output in `evidence/`

**Will exist**
- The detector: the CLI and the GitHub Action
- Draft fix PRs in frontend repos, merged only by a person
- The forked RealWorld test bed with about 20 planted breaking changes
- The eval report on GitHub Pages, with real numbers, good or bad
