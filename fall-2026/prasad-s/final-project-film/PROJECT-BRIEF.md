# PROJECT-BRIEF — GistGap
Subtitle: What you see is what you sign, for AI agent payments.
(The subtitle echoes an established security idea; AP2's announcement uses
a close phrase, "what you see is what you pay for.")

1. What is it?
GistGap will be a web demo that tests whether the plain-English text shown
to a person approving an AI agent's payment matches the signed terms (a
"mandate") they are agreeing to. When done it will exist as a public GitHub
repository with a static demo page, a synthetic test set, and a results
table.

2. Why would anyone care?
For a product manager or engineer who owns the approval screen of an
agent-payment feature, GistGap will make it possible to test, before launch
and with synthetic data, whether the approval text leaves out or changes a
spending cap, amount, expiry, or recurrence.
Alternatives I looked at:
(a) Google's Agent Payments Protocol (AP2): the v0.2 specification main page
and Google's announcement post of September 16, 2025. The spec requires
verifiers to check closed mandates against the constraints in open ones, and
requires a non-agentic Trusted Surface to get the user's informed consent
before a mandate is signed. It says the shopping agent assembles the mandate
content and leaves out of scope how it does so. On the page I read, I found
no rule or test that the text shown to the user matches the signed fields. I
did not read the spec's other pages.
(b) The Razorpay-buildathon repository named "Mandate Mirror". Its README
describes a firewall that checks each payment request against a mandate and
the spend already used, and says its buyer agent explains blocks to the user
in plain language. In the README I found no mention of a check on that text;
I did not read the code.
AP2 states the goal, and the repository enforces the mandate. GistGap will
test, with constructed examples, whether the text a person is shown,
including any summary an agent writes for them, matches the signed fields.

3. Who opens it, and what do they do?
Target role: a product manager working on AI agent products. Reader: a hiring
manager or an engineer. In the first sixty seconds they will click three
constructed examples (clean, hidden cap, changed amount) and read the
results table.

4. What does it prove about me?
Skills: prompt contracts (a fixed summary format for Claude), verification
(field-by-field checks), evaluation (a planted-error test set with caught,
missed, and falsely flagged counts), and source grounding (each claim in a
summary traced to a mandate field). Evidence that will back it: the test
set, the results table, dated Claude outputs, and predictions committed
before each run. A reviewer could fairly conclude I can design and measure
a verification check. They could not conclude it works on real payments.
Existing evidence: I have built and submitted one Brutalist film with a
committed checkpoint trail (Assignment 1, fall-2026/prasad-s/week-01-video/).

5. What is in, what is out, what comes first?
In: five fields (amount, merchant, spending cap, expiry date, one-time versus
recurring). Out: signature verification, real payments, protocol compliance,
and checking whether the mandate the agent assembles matches what the user
originally asked for (AP2 leaves how the agent assembles it out of scope).
All mandates and summaries will be constructed, inspired by public AP2
material, with no real payment data.
First to run: the generator plus checker on 10 constructed mandates, 3 with
planted errors. It ran if it flags exactly those 3 and none of the other 7.
I will commit my prediction before running it.

6. What could sink it?
The problem may be smaller than I claim. AP2 requires the surface that shows
the mandate to be non-agentic, so a correct implementation may never show
AI-written text, and I have not examined any implementation. If so, GistGap
narrows to two uses: checking text produced outside that surface (such as a
summary an agent writes for the user), and letting builders test their own
display against the signed fields. A second risk is brittle text matching:
the checker may miss paraphrases such as "five hundred" versus "$500" or
flag correct summaries, so I will test paraphrases on purpose and report
caught, missed, and falsely flagged counts as they come out.

7. Why this project?
A mix, mainly learning. Payments and agent-payment protocols are new to me,
and I have limited background in fintech. I want to learn fintech and break
into fintech product management. Already have: making and committing a
Brutalist film with a checkpoint trail (Assignment 1 in this repository) and
a habit of checking and measuring outputs instead of trusting them.

EXISTS TODAY: this brief; the beat sheet and scene code; the rendered pitch
film (2:55) with its gate reports; the Brutalist toolkit (third-party, used in
Assignment 1 and this film).
WILL EXIST: the generator, the checker, the test set, the demo page, and the
results table.
