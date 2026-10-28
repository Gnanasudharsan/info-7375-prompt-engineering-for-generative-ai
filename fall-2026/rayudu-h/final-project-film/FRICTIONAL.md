# FRICTIONAL: honest build log (Electricity Supplier Check pitch film)

**How this log was written.** I asked Claude (Claude Code, Opus 5.5) to draft it on 2026-10-14. It's built from two sources, both from the same day:
- the raw command log, `FRICTIONAL-NOTES.md` (times from `date`);
- my own messages in the session, quoted where they matter.

Nothing here is invented. Where a time wasn't captured, the entry says so. Lines marked **Confirm:** state what I understood; I checked each one against what I actually think.

**Reviewed and approved by Hemanth Rayudu on:** ______Oct 14 2026______ *(I fill this in. Until I do, this log isn't approved.)*

## Inputs I provided

| Input | What it is | Used? |
|---|---|---|
| `PROJECT-BRIEF.md` | My answers to the seven questions; the source of truth for every claim in the film | Yes (corrected once, then condensed to one page; see the first and fifth entries) |
| `03.30.2026_CES Report.pdf` | Massachusetts Attorney General, 2026 competitive supply report (46 pages) | Yes: $738.7 million (p. 2) and the 10–30% / 51.45% finding (p. 4) |
| `meco_basic_service.pdf` | National Grid, Summary of Basic Service Rates, M.D.P.U. No. 1-26-H, effective Aug 1, 2026 | Yes: the residential rates printed on the B01 bill |
| `5.1.26_massachusetts_electric_company_summary_of_rates_tariff_basic_service-(2).pdf` | An older National Grid tariff, M.D.P.U. No. 1-26-F | No. I chose 1-26-H because my brief cites rates effective 8/1/26 |
| The Brutalist toolkit, `../brutalist.art` | The video toolkit, already installed (I first said it was at `../`) | Yes, updated to GitHub `519fcbb` at my request |
| My prompts in the session | My instructions, answers and decisions | Quoted in full in `BUILD-PROMPT.md`, section 4 |

---

## 2026-10-14: checking my brief against the sources (about 15:15–15:24)

**I tried / expected:** I asked Claude to:
- find my two statistics ($738.7 million; suppliers 10–30% above basic service causing more than half of losses) in the Attorney General's report, with exact pages;
- confirm the tariff's effective date and residential rows;
- check my download dates against the files.

My instruction was "If a claim doesn't match its source, stop and tell me." **Confirm:** I expected my wording to hold up, but I wanted it checked, not assumed.

**What happened:**
- **"over $738.7 million":** the report (`03.30.2026_CES Report.pdf`), p. 2, Table ES-1, says customers "paid $738.7 million more than if they stayed on basic service". My brief said "**over** $738.7 million". The "over" came from the AG's press-release headline ("lost over 738 million"), which rounds the figure. Claude stopped, as I'd asked.
- **10–30% figure:** p. 4 says "51.45 percent of customer losses". My "more than half" was correct.
- **Two tariff PDFs:** my folder had two, `5.1.26_…` (M.D.P.U. 1-26-F) and `meco_basic_service.pdf` (1-26-H, effective Aug 1, 2026).
- **Download dates:** I'd never filled them in (the brief said "[downloaded on: add date]"). The files' dates were copy times, so the real download dates couldn't be recovered.

**What I did:**
- **Tariff and dates:** I answered "yes use ../brutalist.art, meco_basic_service.pdf, today's date". So the tariff source is 1-26-H, and the brief records 2026-10-14 as the download date. That's the date I chose, not a verified download date.
- **The figure:** I answered "yes make it 738.7 million" (brief edited at 15:23:45).

**What Claude or another person contributed:** Claude:
- extracted the PDF text and found the page numbers;
- flagged the "over" mismatch and the second tariff file;
- edited the brief only after I approved.

I approved all three changes. **Confirm:** I didn't open pages 2 and 4 myself; I relied on the quoted text and page numbers in FACTCHECK.md.

**What I understand now / still do not understand:**
- **Confirm:** a rounded press-release number isn't the same claim as the report's exact figure, so I should quote the source document, not the headline.
- **Still open:** this tariff sheet doesn't split residential rates by load zone; only the industrial rows are. I still don't know whether bills print a load zone at all, which is the open question in my brief.

**Evidence and next step:**
- `youtube/electricity-supplier-check-pitch/FACTCHECK.md` rows 1–4
- `FRICTIONAL-NOTES.md`, 15:15:25–15:23:45
- **Next step:** check a real bill against the tariff sheet for the load zone.

---

## 2026-10-14: the toolkit wasn't where I said, then wouldn't start (about 15:13–16:10)

**I tried / expected:** I wrote "The Brutalist toolkit is already installed in the parent folder (../). Confirm that ../art and ../HOW-TO.md exist. If they don't, stop and tell me." I expected it at `../`, and I told Claude not to reinstall or clone anything.

**What happened:**
- **Location:** `../art` and `../HOW-TO.md` didn't exist. The toolkit was in `../brutalist.art/`.
- **"Blocked" features (15:23:50):** `./setup` reported audio, captions and Manim as blocked. The cause was plain `python3`, a rye shim without the packages, while the packages were in the toolkit's `.venv`. With `.venv` active, all 7 features were ready (15:30:59). This is the same trap my week-1 log records ("`./art` shells out to plain `python3`"), and I hit it again.
- **Stale copy:** the local copy was commit `ba2d0e0` (2026-09-07) and had no **show-tell** skill. GitHub's `519fcbb` (2026-10-12) has it, and the assignment calls show-tell "the right format for a pitch".
- **Update (16:07:05):** my two local edits were stashed, the toolkit fast-forwarded to `519fcbb`, and the edits restored with no conflicts.
- **Setup after the update (16:07:24–16:09:54):** `./setup --install` installed manim 0.20.1, then **exited 1** on the toolkit's own "no ElevenLabs" guard, which matched files in GitHub's own example reels. Claude ran the readiness checks by hand instead; all passed, and a Kokoro test phrase measured −21.8 dB.

**What I did:**
- Confirmed `../brutalist.art` as the toolkit root.
- When asked whether to update, I answered "yes update to current github version". That reversed my earlier "do not reinstall or clone" instruction. **Confirm:** I chose it because the assignment expects the current repo.

**What Claude or another person contributed:** Claude:
- found the venv cause;
- backed up my local edits before the update;
- ran the update and the manual checks;
- edited no toolkit source files.

**Confirm:** I accepted this.

**What I understand now / still do not understand:**
- **Confirm:** a stale checkout isn't neutral. My copy was missing the one skill the assignment names.
- **Confirm:** I need to activate the venv in every terminal; I hadn't carried that over from week 1.
- **Still open:** whether the setup exit 1 is a toolkit bug I should report to the course.

**Evidence and next step:**
- `FRICTIONAL-NOTES.md`, 15:23:50–16:10:18
- toolkit `git log`: `ba2d0e0` → `519fcbb`
- **Next step:** decide whether to report the setup guard.

---

## 2026-10-14: the first draft broke the assignment, and I caught it (about 15:35–15:59)

**I tried / expected:** I gave Claude my beat order and rules, and asked it to draft the beat sheet with the ai-explainer skill, then "STOP and show me every beat's narration in a table".

**What happened:**
- **Draft v1:** it put lists and columns on screen and trimmed the narration to fit. Claude asked me five questions about it. To three of them I answered:
  - "I did not understand this" (the sample-bill question);
  - "explain more" (the formula);
  - "idk do what ever is correct for our scenaria" (Remotion vs Manim).

  I also added a point of my own: "did you read the @Final_Project_Pitch_Film_Assignment.pdf ?"
- **What the re-check found:** v1 did the opposite of the assignment's pitch format, "one simple drawn picture per beat, minimal on-screen text, narration carrying the explanation". It also left these out of the narration:
  - the "saves a household the work of…" sentence that Q2 asks for;
  - the course skills (Q4);
  - my full target role;
  - my stack;
  - when I got the AG data.
- **README:** the toolkit README, which the assignment names, hadn't been read.

**What I did:**
- Asked whether the PDF had been read, which led to the redraft (v2, 15:59).
- On the questions I didn't understand, asked for explanations rather than guessing.
- Left the Remotion-vs-Manim choice to Claude. It chose Manim scenes kept in my reel folder, because that needs no edits to the shared toolkit.
- After reading v2, answered "the narration looks good".

**What Claude or another person contributed:**
- Claude wrote v1 and v2, admitted the v1 mismatch, found the show-tell skill on GitHub, and rewrote the narration so the voice carries every idea.
- I rejected v1 and approved v2 **without rewriting any of it in my own words**. When later offered "Narration in my words", I didn't choose it. So the narration is Claude's draft from my brief, approved by me.

**What I understand now / still do not understand:**
- **Confirm:** a toolkit skill's default rules can contradict the assignment, and the assignment wins.
- **Confirm:** I couldn't follow the sample-bill question as first asked; the plain explanation (what to print on a made-up bill) made it answerable.

**Evidence and next step:**
- `youtube/electricity-supplier-check-pitch/PEDAGOGY.md`, section "What changed from v1, and why"
- `FRICTIONAL-NOTES.md`, 15:52:53–15:59:13

---

## 2026-10-14: honesty rules, and where the toolkit pushed back (throughout)

**I tried / expected:** my standing rules for the film:
- I narrate in first person;
- no instructor persona, name, channel chip or credit line;
- Kokoro `am_onyx` voice;
- only claims from my brief;
- past tense only for what exists;
- CONSTRUCTED labels on mock-ups;
- never my real bill;
- no Claude response shown;
- free pipeline only.

**What happened:**
- **Persona and branding:** the toolkit puts "Liam, in for Bear" and an `@NikBearBrown` handle or logo into scenes and the outro by default. These were turned off for my reel only, and the toolkit's bookend check now **fails** on the missing `@NikBearBrown` outro. That failure is a direct result of my rule, and it's recorded in CHECKS-REPORT.md.
- **The bill:** I asked that "in that bill print the meco_basic or any of the bills from the web". Claude:
  - didn't use a web bill (someone's private data, or a utility's branding);
  - in the first master, put the real rates **beside** the drawn bill, arguing that printing them on it would claim real bills show them.
- **Formula:** for the formula on the mock report, I chose "keep option a", a grey placeholder. Claude's reason for offering it: my brief never states the formula.
- **Voice fixes after the speech-to-text check:**
  - "pytest" is written "py-test" (the voice said "PIE-dist");
  - "isn't instant" became "it is not instant" (heard as "is an instant").

**What I did:**
- Answered "its ok for past tense" (for real past events like my overpayment) and "name is fine" (my name on the title card).
- After watching the first master, chose to have the tariff rates printed **on** the bill after all. The bill stays tagged CONSTRUCTED, with the tariff caption.

**What Claude or another person contributed:** Claude:
- found where the toolkit inserts the persona and handle, and disabled them per reel;
- proposed the "beside the bill" layout, which I later overrode;
- made the voice respellings.

I chose the placeholder formula. **Confirm:** I accept the voice respellings.

**What I understand now / still do not understand:**
- **Confirm:** honesty rules can clash with a toolkit's defaults, and the clash should be logged, not hidden; that's why the bookend failure stays in the report.
- **Still open:** should the tool compare a bill against the **fixed** basic service price ($0.17185/kWh) or the **monthly variable** one ($0.16074 in August)? My brief doesn't decide this.

**Evidence and next step:**
- `beat_sheet.json`, `metadata.decisions` and `metadata.overrides`
- `CHECKS-REPORT.md`, BOOKEND row
- `SOURCES.md`, section "What Claude contributed"
- **Next step:** decide fixed vs variable before writing the calculator.

---

## 2026-10-14: gates, visual checks, and the one-page brief (about 16:24–19:29)

**I tried / expected:** render with the toolkit's gates on, look at every frame at 2 fps, then make the brief fit the assignment's "one page… ending with two lists". I answered "Yes fix the brief's layout".

**What happened:**
- **Gate B (16:28):** failed B03, "label on a curve/line: `$`". Fixed.
- **Run 1 (16:29–16:59):** Gate V failed the title card for underfill (8% of the safe area against a 55% minimum). A written sparse-by-design waiver was added, the same mechanism the drawn beats use.
- **2 fps review:** found about 8 s with no motion in B05 and about 7 s in B03, plus beats opening on an empty stage (B06, B11, B12). All fixed and re-rendered.
- **Run 2:** clean.
- **First master (17:10):** GATE T PASS 13/13; MASTER and LOUDNESS PASS.
- **The brief:** cut from 989 to 620 words over many passes, keeping every claim; it still runs 4 lines onto page 2 in Arial 11 pt. Later I added the tool itself ("Electricity Supplier Check itself…") to the top of the Will exist list, because the list named only the parts; that brought it to 649 words. The Sources section moved to SOURCES.md. Some squeezed phrasings changed meaning slightly ("traceable to a tariff") and were put back.

**What I did:**
- Approved the layout fix.
- **Confirm:** I accept about 650 words rather than cutting more content.
- The full original is kept in `_archive/PROJECT-BRIEF.before-layout.md`.

**What Claude or another person contributed:** Claude:
- wrote all the scene code (`scene_body.py`);
- ran every gate and the frame review, and fixed what they found;
- condensed the brief.

**Confirm:** I accept the condensed brief.

**What I understand now / still do not understand:**
- **Confirm:** "one page" depends on the font; at about 650 words it fits in some layouts and not others.
- **Still open:** whether a grader will count the brief as one page.

**Evidence and next step:**
- `CHECKS-REPORT.md`, `_qc/REPORT.md`, `TYPECHECK.md`, `MASTERCHECK.md`, `LOUDNESS.md`
- `FRICTIONAL-NOTES.md`, 16:24:54–19:29:13

---

## 2026-10-14: revisions after watching the first master (about 19:38–19:53)

**I tried / expected:** I said "I still want to improve things a little bit more" and picked three changes from a list:
- redraw B08's skills visual;
- a bigger title card, with my name said correctly;
- the tariff rates printed on the bill.

I didn't pick "narration in my words".

**What happened:**
- **My name:** the first voice said it "HEM-anth RAY-oo-doo" (heard as "Hemant Ray Udu"). Claude made four sample pronunciations and asked me to pick one; instead I typed how I say it, "Hey- Month Ra- You- do". B00's voice script now spells it "Hey-month Rah-you-doo", and the re-voiced take was heard as "hey month raw you do" (19:41:52). On screen it stays "Hemanth Rayudu".
- **Title card:** rebuilt as a drawn card. The old `FormACard` auto-sized the title small; it's now 80 pt.
- **The bill:** now prints "Supplier · competitive supplier", "Basic service, fixed · $0.17185 / kWh" and "Basic service, Aug 2026 · $0.16074 / kWh".
- **B08:** the five grey blocks became five objects, one per skill.
- **Checks:** Gates A, W and B passed; run 3 was clean; GATE T passed 13/13.
- **Second master (19:53):** 3:32, sha256 `c66583e099dd35ec7c34ab223d722378260f9e1334ab031df41e2bd92248211f`; MASTER and LOUDNESS PASS.

**What I did:** chose the three changes and gave my own pronunciation.

**What Claude or another person contributed:** Claude wrote the new scenes, re-voiced B00, re-ran every gate and re-exported. **Confirm:** I accept the result. I also asked Claude to draft this log from the session record instead of writing it from scratch myself.

**What I understand now / still do not understand:**
- **Confirm:** a TTS voice needs a respelling to say a Telugu name; the spelling on screen and the spelling for the voice can differ.

**Evidence and next step:**
- `_qc/recheck_B00.png`, `_qc/recheck_B01.png`, `_qc/recheck_B08.png`
- `beat_sheet.json`, `metadata.decisions` (`name_pronunciation`, `title_card`, `b08_skills`, `sample_bill`)
- **Next step:** zip and push. Final GitHub commit: ____________ *(add after pushing)*

---

## 2026-10-14: the visuals didn't fit electricity, and two things in my pitch didn't add up (evening; first captured time 22:14:35, master 22:40)

**I tried / expected:** I watched the second master and read this log, and found three problems:
- **The tool was missing from my brief:** I asked, "In will exist section of project-brief.md there should be the product and the tool itself right?"
- **The visuals:** I wrote, "I feel like the images are not relevant. I see alot of cardboard boxes and I dont know why. Also the video says this is a drawing and not mine, which should not be mentioned at all… could you replace them with transformer images because it is relevant to eletricity".
- **The logic:** I asked, "Why would AI Engineer see the eval report from thte tool, Are we giving him access to the code and how would he determine if the data is from cod eor not. and Where are we using claude codee in the project?"

**What happened:**
- **The brief:** its "Will exist" list named only the parts. "Electricity Supplier Check itself: a Python repository with the agent…" was added as the first item.
- **The eval-report answer:** the hiring manager doesn't use the tool. They open the project's public GitHub repository. The verifier compares every number in Claude's explanation with the numbers the Python calculator produced, and the evaluation report shows that per test bill. They can rerun the tests.
- **The Claude Code answer:** it has two possible roles, building the project and being how the agent calls Claude at runtime. My brief rules out paid API calls, so the runtime role means anyone running the tool needs Claude Code access.
- **My four choices** (a multiple-choice question):
  - Claude Code for build and runtime;
  - rewrite B05;
  - an electricity cast;
  - remove both spoken disclaimers.
- **Brief first (before 22:14:35; time not captured):** the brief got the Claude Code role, the GitHub repository check, and "For now it is a portfolio demo: whoever runs it needs Claude Code access."
- **Re-voice (22:14:35):** B01 and B04 lost "This bill is a drawing, not mine" and "That screen is a constructed mock-up". B05 and B07 were reworded. The on-screen CONSTRUCTED tags stay, because the assignment requires them.
- **Visuals:** ten scenes were redrawn with:
  - a pole-mounted transformer as the tool;
  - a coin stack;
  - an offers board;
  - a GitHub folder;
  - a crossed-out contract;
  - plain panels instead of boxes.
- **Gate V (22:25):** failed B03 and B05 for low contrast (0.27 and 0.22 against 0.30), from the folder's pale fill. Fixed, then clean.
- **2 fps re-read:** found long holds in B03 and B05; fixed.
- **Third master (22:40):** 3:38, sha256 `c1dffb5c60fc91ffcdf0ee584b1c2b2d1d936ef6cc4681799e885beb4c3de72c`; GATE T 13/13, MASTER and LOUDNESS PASS.

**What I did:**
- Raised all three problems.
- Chose the four options.
- Asked for transformer images specifically. Claude used the transformer as the tool and plain panels where a box was only a container, and I chose that option.

**What Claude or another person contributed:**
- Claude answered the two questions.
- It drafted the new brief sentences and the B05 and B07 wording (I picked them in the multiple-choice question).
- It redrew the scenes and re-ran every gate.
- **Confirm:** I accept the result.

**What I understand now / still do not understand:**
- **Confirm:** an evaluation report only proves something if a reviewer can open the repository and rerun it; the hiring manager reviews the code and the report, not the tool.
- **Confirm:** with no paid API calls, Claude Code in headless mode is how the agent will call Claude, and that limits who can run it.
- **Still open:** how a household would use the tool without their own Claude Code access. For now it's a portfolio demo.

**Evidence and next step:**
- `_qc/recheck_cast_A.png`–`_qc/recheck_cast_E.png`
- `CHECKS-REPORT.md` (Gate V row)
- `PROJECT-BRIEF.md` (Stack header, section 3, section 5)
- `beat_sheet.json` `metadata.decisions` (`claude_code_role`, `visual_cast`, `spoken_disclaimers`)

---

## Summary of contributions

| Who | What |
|---|---|
| Me | Wrote PROJECT-BRIEF.md and the project idea. Set the rules and beat order. Caught that draft v1 broke the assignment. Chose the tariff file, download date, toolkit update, formula placeholder, bill layout, title card change, B08 redraw, and my name's pronunciation. Approved the narration as drafted. Pointed out that the tool itself was missing from my Will exist list. Questioned the cardboard visuals, why a hiring manager would see the eval report, and where Claude Code is used. Then chose the electricity cast, the B05 rewrite, Claude Code at build and runtime, and removing the spoken disclaimers. |
| Claude (Claude Code) | Checked the brief against the PDFs; drafted all narration; wrote all scene code and paperwork; ran the toolkit, gates and visual checks and fixed what they found; condensed the brief; drafted this log at my request. |
| No one else | No classmates, TAs or other people helped on this assignment. *(Confirm.)* |
