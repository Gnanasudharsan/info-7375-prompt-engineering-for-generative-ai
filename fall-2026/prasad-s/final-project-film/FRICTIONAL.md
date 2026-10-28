## 10/08/2026 — Choosing the final project and checking for existing work
What I tried: In a planning session with Claude (claude.ai), I compared project
ideas and chose one: a demo that tests whether the text shown to a person
approving an AI agent's payment matches the signed terms. I read Google's AP2
announcement post and the v0.2 specification main page, and I found and opened
the Razorpay-buildathon repository's README myself.
What happened: My working title was "Mandate Mirror". A name-collision search
during planning found products called "Mandate" and "MandatePay" but missed a
repository with the exact name, which I found. Its README describes a payment
firewall that checks requests against a mandate and cumulative spend, not a
check on the text shown to the person (README only; I did not read the code).
My first draft of the alternatives also included a Stripe entry that blended two
different protocols and made claims I had not checked against Stripe's own
docs, so it was dropped.
What I did instead, or decided: I kept the project, renamed it "GistGap" (picked
from a shortlist), and narrowed my claims. I read only the AP2 main spec page.
It requires a non-agentic Trusted Surface, so the problem may be smaller than I
first thought. I recorded that as the main risk in the brief. A single
exact-string search for "GistGap" during planning found no match; I have not
yet searched GitHub or domain names myself.
What I'd check next time: Search GitHub for an exact name myself before adopting
it, open candidate repositories instead of relying on summaries, and confirm
each claim against the primary source before writing it down.

## 10/08/2026 — Git blocked by the Xcode license
What I tried: I asked Claude Code to create the project folder skeleton and
check my git settings.
What happened: Every git command failed with "You have not agreed to the Xcode
license agreements." The tool stopped without changing anything and said it
needed my password.
What I did instead, or decided: I ran "sudo xcodebuild -license" in Terminal
and typed "agree." Git then worked and the setup finished.
What I'd check next time: If git fails with a license message, accept the
license first. Stopping instead of working around the error was the right
behavior.

## 10/08/2026 — Placeholder email set as my git email
What I tried: I set my git commit email to my GitHub no-reply address.
What happened: The command I was given contained a placeholder address, and I
ran it unchanged, so my global git email became the placeholder. I was told to
get my real no-reply address from GitHub Settings, then ran the same
placeholder command a second time. Checking the setting showed the placeholder
again, my real no-reply address was looked up with the gh tool, and I set it.
Nothing was committed with the placeholder.
What I did instead, or decided: I set the real address globally, replacing my
previous global email for all repositories, and confirmed it with
"git config user.email".
What I'd check next time: Replace placeholders before running any copied
command, read the whole message before running it, and check "git config
user.email" before the first commit.

## 10/09/2026 — Prediction before the first full render
Written before running audio generation, ./art run, or any gate on the real
film.
What I know going in: the 2-beat test reel passed every gate on its first run.
The real film has 14 beats and 13 new drawn scenes that I have only seen as
low-resolution stills, not at 4K. The narration is 474 words.
What I expect: every gate (pre-flight, contrast, layout, visual QC, type check,
final verification, master check) passes on the first try, so no gate fails
first. I expect the final film to run over 3:00, and I expect 3 to 5
fix-and-re-render rounds.
Why: the topic is fairly complex, so I expect to need 3 to 5 iterations to get
the pictures and the narration right.

## 10/09/2026 — Toolkit friction before the first build
What I tried: Smoke-tested the Brutalist toolkit and read its docs before
building.
What happened: The toolkit's own smoke test failed because its fixture's slug
(_smoke) breaks the toolkit's slug rule. The show-tell reference example could
not be built because its scenes.py is not shipped. No check is called "render
integrity"; the closest are ./art final's verification and master_check.py,
whose duration test is skipped because clock_check.py is missing. The docs
disagree about whether the Kokoro model ships with the toolkit. My Mac's
system Python (3.9.6) is too old, so the toolkit's .venv has to come first on
PATH. After I updated the toolkit, show-tell appeared with defaults (a persona
voice and a spoken credit outro) that conflict with the assignment's
no-persona rule.
What I did instead, or decided: Wrote my own scenes.py and sheet, used the
af_bella voice with no persona or outro, treated ./art final, master_check.py
and an ffprobe duration check together as my render-integrity check, and kept
strict gates with no overrides.
What I'd check next time: Run the full documented build on a tiny reel early,
and read which checks get skipped.

## 10/10/2026 — Build problems, in the order they happened
What I tried: Built the film from the beat sheet with strict gates and no
overrides.
What happened: Gate A failed first, on B05: the scene places a dot relative to
a label's width, and Gate A's stand-in for Manim overestimates text width.
After I edited scenes (labels, B06, B12), ./art run silently reused the old
clips, because it only renders a scene whose clip is missing. Watching the
review cut, I saw B14's title leave the tail of the "p" unfilled; Gate V had
reported no problems. At ./art final, Gate T (which only runs at final) failed
B11, reading the large dark base as overlapping text. The build also wrote
absolute local paths into build-state.json (29) and the receipt (29), and one
into MASTERCHECK.md.
What I did instead, or decided: Gave the B05 dot a fixed position; moved old
clips into _superseded/ before each rebuild; redrew B14 as a drawn scene;
scaled B11's base together with its box (tested in a scratch copy first);
untracked build-state.json and committed redacted copies of the receipt and
master check with my home path replaced by <home>.
What I'd check next time: Move old clips aside after every scene edit, watch
the whole cut myself because gates miss visual problems, and run the final's
checks earlier.

## 10/11/2026 — Outcome against my 10/09 prediction
What I predicted: Every gate passes on the first try (so none fails first), a
final film over 3:00, and 3 to 5 fix-and-re-render rounds.
What happened: Gate A failed first and Gate T failed later, so the first
prediction was wrong. The narration measured 175.23 s and the master 175.458 s
(2:55.5), under 3:00, so the second was wrong. I count four fix rounds (Gate A
on B05; the label, B06 and B12 edits with the stale-clip problem; B14; Gate T
on B11), inside my 3 to 5. The final master passed Gate T and the master check;
I checked its duration with ffprobe because the check's own duration test was
skipped.
What I'd do differently: Expect the visual gates to need most of the rounds.
The narration pace came out at about 2.7 words per second.

## 10/11/2026 — Running the final before FACTCHECK verdicts
What happened: The header of my FACTCHECK.md says the final should wait until
every row reads PASS, CORRECTED or EXEMPT, but the toolkit's Gate F only checks
that the file exists, so the final ran with every row still PENDING. I set the
verdicts afterwards, on 10/11, after reading the table.
What I did: All 33 rows read APPROVED after I read the table; APPROVED is my own
word, not one of the toolkit's verdicts (PASS, CORRECTED, EXEMPT). No row
required changing the film. I recorded the order in a note under the table.
What I'd check next time: Do the fact-check before the final, not after.

## 10/11/2026 — Push: rebase changed commit hashes and committer dates
What happened: Before pushing I ran git pull --rebase, because origin/main had
moved. That replayed my 13 commits for this assignment onto the newer main, so
each has a new hash and a committer date of the day it was replayed. Their
order, messages, content and author dates are unchanged. The four Assignment 1
hashes shown in the film (B12) were already on origin/main and did not change.
What I did: Updated stale commit-hash citations in my files in a new commit, and
kept a local backup branch of the pre-rebase history until after submission.
What I'd check next time: Merge instead of rebasing when the checkpoint dates
are part of the evidence.
