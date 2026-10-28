# Beat draft — for Yudan to approve before rendering

Each beat = one drawn picture + 1–3 word labels + the narration below (read by a synthetic Kokoro voice, first person, as Yudan).
Target ≈ 3 minutes (~470 words). **Every sentence must be one you agree with and can defend.** Mark anything to change.

Labels on screen in [brackets]. `CONSTRUCTED` = on-screen tag for a drawing that is a sketch, not a screenshot.

---

**B00 — Opening**
Picture: a quill writes a title on a page.
> Hi, I'm Yudan Zhou, an Information Systems master's student. This is the pitch for my final project, a portfolio piece for data analyst roles. The voice you hear is a synthetic voice reading my script.

**B01 — What it is**
Picture: job postings ride a conveyor into three trays [apply] [consider] [skip], and a fourth tray off to the side [no record].
> In one sentence: it is a job-search triage tool for international students. It sorts job postings into apply, consider, or skip, using public funding and visa-sponsorship records. And when there is no record, it says so, instead of calling it a no. When it is done, it will be a repository: a recipe you can audit, a Python tool, tests, and an evaluation log.

**B02 — The problem, in the data**
Picture: three bars shrink one after another; counter shows the numbers. [record · run 2026-10-02]
> Here is why it matters. In the public dataset I worked with, twenty-seven thousand, eight hundred seventy-four companies have a funding date. Only one thousand, five hundred thirty-two of them have any H-1B approval on record. And only one hundred thirty-one of those raised money in the last two years. Funded and sponsoring barely overlap.

**B03 — A blank is not a no**
Picture: a huge stack of blank cards next to five small cards marked 0. [blank] [0]
> The bigger trap is the blank. Twenty-eight thousand, eight hundred twelve rows have no approval number at all. Only five say zero. So a blank almost never means "does not sponsor". It means nobody matched a record.

**B04 — What I compared it to**  ⚠️ *WAITING ON YOUR OWN LOOK AT h1bdata.info / myvisajobs — will be written from what you report, with the date.*
Picture: a search box, then the tool beside it.
> (draft after your observation)

**B05 — What it does with a blank**
Picture: a blank card rides the conveyor, is lifted off, and lands in the [network] tray with a question bubble.
> So my tool does one thing differently. It labels the blank, keeps that company out of the ranking, and moves it to my networking list, with a question to ask a real person. It does not save lookup time. It stops a student from throwing away most of the market because a search came back empty.

**B06 — Who opens it, first sixty seconds**
Picture: a laptop; one command runs; a shortlist appears with small tags on each number [record] [your-input].
> The reader I am pitching to is a hiring manager for a data analyst role. In the first sixty seconds, they clone the repository, run one command, and see a shortlist where every number carries a tag. "Record" means it came from a data file. "Your input" means I chose it.

**B07 — What it proves**
Picture: a magnifier passes over the tags; a check appears beside a test list. [source grounding] [verification]
> What it shows about me is source grounding and verification. A test suite already checks those labels, not just the arithmetic. On October twelfth, a teaching assistant reviewing the recipe wrote: "you never turn a blank into a no." The same review took points off for two things, and fixing them is my first step.

**B08 — Exists today vs. will exist**
Picture: two shelves. Left [exists] fills with items; right [will] has dashed outlines.
> Here is the honest split. Today, a recipe, a Python prototype, and eleven tests exist. I ran it on October second, and it was reviewed on October twelfth. Still to come: the corrected status, a written reason for every assumption, a sensitivity check, a test set with known answers, and an honest failure analysis.

**B09 — In, out, first**
Picture: a gate that only opens for records; a [first] flag on the two review fixes.
> One thing it will deliberately never do: say a company does not sponsor, except the five whose record shows a zero. The first thing I will make run is the two fixes from the review: set the recipe's status back to draft, and replace my placeholder numbers with values that each have a written reason. You will know it ran when the tests pass and no number in the report says "placeholder".

**B10 — What could sink it**
Picture: a balance: one hand-typed number on one side outweighs a tall stack of records on the other. [assumption] [records]
> The risk is that numbers I choose can outweigh the records I look up. In my own run, one company had five hundred sixty-four approvals, and still scored zero, because of one hand-entered demo value in the input file. Even this pitch's first draft had four statements that did not match my own files, caught by an AI review against the records. So I will add a sensitivity check that moves each assumption and counts how many decisions flip.

**B11 — Why this project**
Picture: two piles [have] and [learning].
> Why this project? It is a mix. What I already have is the domain: I am the person it is built for, and the judgment calls in the recipe are mine. The code was written with an AI assistant under my direction. What is new for me is writing and testing code myself, building a test set with known answers, and sensitivity analysis.

**B12 — Close**
Picture: the title page again, signed.
> This is is-funded-sponsor-triage. I'm Yudan Zhou. Thanks for watching.

---

## Decisions for you

1. **Voice:** pick one Kokoro voice — `af_heart` (warm, American female), `af_sarah`, `bf_emma` (British female), or `am_michael` (American male). Not `am_onyx` (that's the instructor's "Liam" persona).
2. **Any sentence you disagree with?** Change it in your own words — the film reads exactly what is here.
3. **B04:** send me what you saw on the alternative site(s) and the date.
