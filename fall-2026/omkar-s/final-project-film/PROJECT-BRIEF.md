# PROJECT-BRIEF — BiteCheck
**Omkar Salian · INFO 7375 Fall 2026 · v2, 2026-10-22** · Target role: new-grad Software / AI Engineer · Stack: TypeScript, Express, Node's test runner, Claude Code, GitHub Actions

**Who:** I'm Omkar Salian, a software engineering master's student at Northeastern, building this alone with Claude Code as my coding assistant.
**Simple version:** you only know a smoke alarm works if you blow smoke at it. Tests are software's alarms. BiteCheck is the smoke: it breaks one rule on purpose and checks which tests go off.

**1. What is it?** A Claude Code workflow that writes API tests for my InstaLoan loan demo (Express + TypeScript, synthetic data) and checks that each test **fails when a business rule is broken on purpose**. When done: a public GitHub repo with a test-writing prompt contract, a planted-bug list ("mutants"), a runner, a one-page report and an evaluation log.
**How it works:** (1) I write numbered rules and mutants, each a copy of the code with one rule broken. (2) Claude Code writes TypeScript tests, each naming its rule. (3) The runner runs every test on the real API (all must pass) and on each mutant (one must fail). A surviving mutant is a gap. A test failing on correct code is Claude's mistake and goes in a dated log.

**2. Why care?** It tells an engineer reviewing AI-written API tests which ones would catch a broken business rule. *Postbot* and *Schemathesis* (docs read 2026-10-12) write test scripts and check APIs against schemas, not business rules. *StrykerJS*, which I ran with Claude Code on 2026-10-13 (`evidence/stryker/`), made 92 mutants, but **none changed the ₹15,000 limit**. BiteCheck adds one-rule-at-a-time business mutants tied to rule IDs.

**3. Who opens it?** A hiring manager screening a new-grad SWE or AI engineer. In 60 seconds: run `npm run bitecheck` and read one page showing what passed, which mutants were caught or survived, and Claude's wrong tests.

**4. What does it prove?** Prompt contracts (each test cites a rule), source grounding (no rule, no test), a bounded agent loop (Claude edits tests, never the API, with fixed tries) and evaluation (mutation score plus mistake log). Evidence: repo, CI runs, log. It is measured on one API, not every API.

**5. In / out / first.** *In:* one API, ~20 mutants, runner, report, log. *Out:* not a general tool, and it never fixes app code. *First (done 2026-10-22):* my income mutant (15,000 → 1,500) in GitHub Actions. The run passed on the real rule and killed both mutants (`evidence/ci/`).

**6. What could sink it?** I write the mutants, so I could make them too easy. I'll commit the list before Claude writes tests, include boundary cases, and report every survivor.

**7. Why this project?** A mix. *Have (private):* API testing and CI gates at my last job. *Have (public):* a Claude workflow with run logs ([nikbearbrown/the-reallocation-engine#37](https://github.com/nikbearbrown/the-reallocation-engine/pull/37)). *New:* mutation testing and evaluation design.

**Exists today (2026-10-22)**
- InstaLoan API (local, private), run 2026-10-12 with Claude Code: ₹14,999 rejected, ₹15,000 offered, early payout refused, HTTP 409 (`evidence/los_smoke_test.txt`)
- StrykerJS run on its rules, 2026-10-13: 92 mutants, none on the 15,000 limit (`evidence/stryker/`)
- Income-rule unit tests (4) and a mutant checker written by Claude Code (2026-10-21), plus two mutants: Claude's `<`→`<=` and mine, 15,000 → 1,500 (2026-10-22). GitHub Actions ran them in my private repo on 2026-10-22: all passed, 2 killed (`evidence/ci/`)
- This brief, the beat sheet and the film

**Will exist**
- The prompt contract, rules file and full mutant list (committed first)
- Claude-written API tests, the runner, the report, the log
- The public repository
