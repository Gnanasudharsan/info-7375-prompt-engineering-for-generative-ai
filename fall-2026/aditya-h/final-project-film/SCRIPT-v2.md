# ProductLens AI: pitch film script v2 (for Aditya's approval)

**Story:** one running example, a PM at an online shoe store deciding on a one-page checkout, carried through the whole film.
**Language:** plain; every term is explained the first time it's used.
**Format:** show-tell, the same pipeline that passed every gate: one drawing per beat, 1–3 word labels, the voice explains.
**Honesty:** past tense only for what exists. Drawings of the unbuilt product are tagged `constructed`; your real run is tagged
`real run · Oct 25 · by Aditya`.
Your input is in: real run Oct 25 (B05–B06) and your pivot reason (B15).

| # | Narration (spoken) | Picture | Answers |
|---|---|---|---|
| BIDEA | Hi, I'm Aditya Hasija. Product managers ask one question all the time: should we build this feature? I think a better question is: what should we test first? | Typewriter: "Should we build this feature?" is corrected to "What should we test first?" | hook |
| B00 | Say you're a product manager at an online shoe store, and your team wants a one-page checkout. | A shopping cart; a 4-step checkout folds into 1 page | example |
| B01 | Before you build it, you need to know what customers want, what other stores do, and what could go wrong. That research takes days, and a good-sounding idea isn't always a good decision. | Three question cards: customers · competitors · risks | Q2 why care |
| B02 | That's the job of my project, ProductLens AI. You type in the feature and the goal, say, more completed purchases, and attach a few public articles. It will give back a one-page decision brief. | Idea card + articles go in; one brief page comes out | Q1 what is it |
| B03 | The brief will list the biggest risks, the numbers to watch, like checkout completion, and the first experiment to run. Every claim in it will be marked: backed by a source, or an assumption. | Brief page with sections; "sourced" / "assumption" tags land | Q1 |
| B04 | Inside, three AI agents will each take one angle: the market, the customers, and the risks. A fourth agent, the checker, compares their work to the sources and can send one back to fix it, once. | Three dark blocks → review desk; one page goes back once | Q1/Q4 |
| B05 | Can't a chatbot already do this? I tested it myself. On October 25th, I gave ChatGPT the shoe-store idea plus a made-up claim: Baymard, a checkout research firm, says one-page checkouts always convert better. Their research says it depends. | **Your real ChatGPT screenshot** (cropped, date visible), your prompt with the planted line underlined | Q2 real alternative |
| B06 | It caught my made-up claim right away, and the advice was solid. But only one paragraph had a source, and it rarely said which points were facts and which were guesses. | Your screenshot scrolls; one source chip circled; unlabelled rows marked with "?" | Q2 the gap |
| B07 | That's the gap I'm aiming at. Tools like DimeADozen and ValidatorAI already score whole startup ideas. ProductLens is for one feature in a product that already exists, with every claim labelled and checked. | Big "startup idea" box vs one small "feature" card | Q2 difference |
| B08 | When it's done, it will be a GitHub repository with the app, a set of made-up test ideas, and a score sheet. | Parcel opens: app window, test cards, score sheet | Q1 artifact |
| B09 | If you're hiring for an AI product role, you'd open it and, within a minute, see one sample brief and how often the checker caught planted mistakes, misses included. | README → sample brief → score sheet on a desk | Q3 who opens |
| B10 | It should show that I can write clear instructions an AI has to follow, check its answers against sources, and measure how well it works. It won't show I'm a machine learning engineer. | Instruction page + a gate the answer must fit | Q4 what it proves |
| B11 | The first step is small: one agent, one feature idea, run from the command line. You'll know it worked when it saves a log where every quoted source checks out. | One parcel → one agent → log page with a check | Q5 first |
| B12 | It won't plug into company data, run real A/B tests, or say go or no-go. It suggests the test; people decide. | A "go / no-go" stamp blocked at a gate | Q5 out |
| B13 | The biggest risk is a checker that agrees with everything, since it's the same AI grading its own team. | A stamp approving a cracked page | Q6 risk |
| B14 | So I'll hide mistakes in ten test ideas and count how many it catches. If it misses too many, those checks move into plain code. | Test samples in; tally grows; a code block docks | Q6 fix |
| B15 | I changed this from my first pitch, a pre-mortem tool for startup ideas, because it was too close to an AI wrapper. I wanted something built for product managers, with real everyday use. | Last pitch's crate turns into the feature card | change log |
| B16 | Why this project? It's a mix. I've spent years in product roles writing requirements and doing research, and my WorkShip, SkillPort and Touchline projects are on GitHub. Building and testing AI agents is the new part. | Filled "have" shelf; outlined "new" shelf | Q7 why |
| B17 | Today, ProductLens is a plan: the idea, a written outline, and my chatbot test. Everything else I'll build with Claude Code in the next two weeks. | Small "exists" tray; dashed "will build" slots | exists vs will |
| BOUT | ProductLens AI. Aditya Hasija. | Title + name | outro |

## What changed from your draft, and why
- **Kept** your name, problem framing, checkout example, agents + checker, first milestone, "out" list, "convincing ≠ correct" risk
  idea, and the skills-plus-learning reason.
- **Added** a real test you run yourself (B05–B06), which fixes both −0.5 deductions. Also added the hiring-manager reader (Q3),
  how you'd know the first step ran (Q5), "won't prove" (Q4), a specific, measurable risk (Q6), evidence for existing skills
  (Q7), and an explicit exists / will-build split.
- **Removed** "Validate faster" (an unproven speed claim), "not just a one-time opinion" (unverified claim about competitors), and
  on-screen slogans (show-tell keeps text to labels; the voice says it).
- **Running length:** ~545 words with placeholders, about 3:40. The limit is 4:00.
