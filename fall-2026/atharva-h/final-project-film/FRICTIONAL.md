# FRICTIONAL — Final Project Pitch Film

Dated entries, written as the work happened. Times are local (America/New_York).

## 2026-10-07 — Read the assignment
Read the brief. The film is due before Reallocation Engine Part 2. I worked to a deadline of the night of 2026-10-14, so the suggested five-day shape got compressed into about three working days.

## 2026-10-12 — Choosing a topic
Looked at six candidate projects: extending my Reallocation job checker, a plain-English-to-SQL helper, an H-1B sponsor dataset, a number-claim checker, tested metric definitions, and a data-quality agent. Picked the **plain-English-to-SQL helper with an honest evaluation log**. It is the clearest signal for a Data Analyst role, and it lines up with the course's evaluation and verification themes.

## 2026-10-13 — Dataset and brief
- I wanted data that actually helps someone looking for a job. Chose the U.S. Department of Labor's LCA (H-1B) disclosure data and opened the OFLC Performance Data page myself.
- Chose **FY2025** over FY2026. FY2025 is a complete year and won't change. The FY2026 Q3 file is partial, and the page says it can still be revised.
- Decided this is a pure pitch: no first run before filming. So the film's "exists today" is just the brief and the chosen data source.
- First draft of PROJECT-BRIEF.md cited my earlier projects as evidence. I asked for them to be removed, since the film is about this project only. Then I added back one line to the brief (not the film): my earlier work includes a SQL and Power BI data-modelling project and a crime-data analysis in Snowflake. I left out the percentage improvements, because I can't show proof of them in this submission.
- Alternatives: I have used ChatGPT and Vanna.ai, but I haven't run a structured comparison for this project. So the brief and film describe my reading of each tool and say plainly that it isn't a tested comparison. The claim is that SponsorSQL will make accuracy measurable, not that it will be more accurate.

## 2026-10-13 — Brutalist checkout predates show-tell
My `brutalist.art` checkout is commit `ba2d0e0` (2026-09-07). The show-tell skill was added upstream later. Updating the checkout would have changed toolkit files that still hold uncommitted work from my earlier reels, so I didn't update. I built on the existing **ai-explainer** chassis and kept to the show-tell idea where it fits: one drawing per body beat, labels only, the voice explains. A `git fetch` updated only git's remote-tracking refs, not any working files.

## 2026-10-14 — Narrating as myself
The toolkit's defaults are the instructor's persona ("Liam, in for Bear"), and its title-outro component hardcodes the instructor's handle. The assignment forbids both. What I did:
- The script is first person ("I'm Atharva"). The voice is the free local Kokoro `am_onyx` voice. The film says aloud in B00, and again in B12, that the voice is synthetic.
- The composer beats use `folderLabel: "@Atharva"` and my own greeting.
- The outro is a Manim scene in my reel folder, not `ClaudeTitleOutro`, so no toolkit file had to change.

## 2026-10-14 — Checking the data claims
- Read `LCA_Record_Layout_FY2025_Q4.pdf` to confirm the column names the film shows: EMPLOYER_NAME, JOB_TITLE, WORKSITE_CITY, WAGE_RATE_OF_PAY_FROM, TRADE_NAME_DBA. No PDF tools were installed, so the text was pulled out with Python's standard library (zlib).
- **Caught a bad example in my own brief.** The risk section used "Amazon.com Services LLC" vs "Amazon Web Services Inc" as two spellings of one company. Those are actually two different legal entities, so the example was wrong. I replaced it with a constructed company ("EXAMPLE DATA LLC" and its variants), labelled CONSTRUCTED on screen, and cited the real `TRADE_NAME_DBA` field.

## 2026-10-14 — Keeping the toolkit untouched
Before building, I recorded a snapshot of every toolkit file's git status and timestamp. During the build:
- `remotion_scenes.py` appended three rows about this reel to a shared, git-ignored index, `runtime/remotion/_bench/consumers.json`. I removed those rows so the file's content is back to what it was. (Its timestamp did change.)
- Ran the toolkit with `PYTHONDONTWRITEBYTECODE=1` so no `.pyc` files were written into it.

## 2026-10-14 — Gates
- **GATE A failed:** three scenes used `np` without importing numpy. Fixed the import.
- **GATE B failed on B02:** the "?" sat on the spreadsheet's edge line, and the title and source caption were outside the safe area. Narrowed the sheet and moved both lines inside.
- **Duration is not gated** by this toolkit. Kokoro measured the narration at 197.0 s (3 min 17 s), and I checked the 2–4 minute limit by hand.
- **GATE B failed on B07:** the strike-through lines ran across their own labels, and the tray's top edge cut through the cards. Replaced the strikes with an ✕ beside each card and lowered the cards.
- **GATE B also caught** B04's "failure log" label off the right edge, B08's CONSTRUCTED label off the left edge, and B09's heading touching its chip stack. All fixed with a small helper that keeps labels inside the safe area.
- **GATE V failed: 2 BLOCKER, 12 MAJOR.** B03's tag was off the left edge, B02 and B07 were low-contrast (pale fills), and most body beats were under the 55% canvas-fill floor. This checkout has no "sparse by design" waiver, so I didn't switch the gate off (`ART_STRICT=0`). I redesigned the layouts instead: bigger pipeline boxes, a persistent PROPOSED tag, dashed outlines for steps not yet drawn, darker cell bars, unfilled trays, a larger title and credits, and a larger font on the hesitant writer.
- **Found by looking at frames, not by any gate:** B03's check mark and B02's "?" only started drawing in the last half-second, so they never visibly landed. B03's check mark was also tiny and sat on the word "check". B05's dot sat on the README border. B08's highlight box stayed put when its rows moved. Fixed each, then re-checked the frames.
- **Final run (run-10): every gate passed, GATE V 0 BLOCKER / 0 MAJOR.** Exported the master with `./art final --height 1080 --out` into my reel folder, so nothing was written to the toolkit's `renders/`. Runtime 197.3 s.
- Two advisory warnings remain, and both are deliberate. (1) "graphic carries 10/13 beats": this is a one-drawing-per-beat film. (2) "OUTRO LAW wants ClaudeTitleOutro": that component hardcodes the instructor's handle.
- **Not verified:** I couldn't machine-check the pronunciation of "Sponsor S Q L", "H one B" and similar spellings, because no speech-recognition model is installed and I didn't download one. These need a listen before submitting.
- **Pronunciation checked by ear (2026-10-14):** I watched the film and the pronunciation is right.

## 2026-10-14 — Pauses: considered, not done
I wanted a 1-second pause after every sentence. There are 64 sentences, so that would add about 64 s and push the film to about 4:21, over the 4-minute limit. A 0.5-second pause (about 3:49) would fit, but it means regenerating all the audio and re-rendering every beat, roughly 30–45 minutes, and there wasn't enough time before the deadline. I submitted the film as it is.
- **Toolkit check at the end:** git status matches the pre-build snapshot exactly. The only file whose timestamp changed was `consumers.json`; its content was restored and its timestamp reset. No other project folder was edited. A copy of the beat sheet was added at `beat-sheets/sponsorsql/`, as a new file only.

## 2026-10-24 — Revision: latest data, credits, ChatGPT test
- **Data switched to the latest release.** The newest LCA file on the DOL page is FY2026 Q3 (determinations October 1, 2025 to June 30, 2026); Q4 isn't published yet. I downloaded `LCA_Disclosure_Data_FY2026_Q3.xlsx` (251,850,891 bytes, SHA-256 `f8ca8448…bd28b3`). It's kept out of the repository because it's over GitHub's 100 MB limit.
- **Checked the real columns.** Read the file's header row (98 columns) with Python's standard library. EMPLOYER_NAME, JOB_TITLE, WORKSITE_CITY, WAGE_RATE_OF_PAY_FROM and TRADE_NAME_DBA are all there, so B02 and B08 now cite the FY2026 Q3 file instead of the FY2025 layout.
- **Found personal contact columns.** The file includes employer contacts, attorneys and preparers, with names and emails. The scope now says the load step will drop them, and B07 has a new card, "contact columns dropped".
- **Q3 can still change.** The DOL says some Q3 records may be revised, so the answer key will be tied to this exact file by its checksum.
- **Credits corrected.** B00 now says "The script was written with Claude, and reviewed by me." The B12 narration and on-screen credit say the same.
- **Ran one question through ChatGPT** (GPT-6, high mode), with the FY2026 Q3 record layout attached: certified H-1B Data Analyst cases with a Boston worksite.
  - First reply: a DuckDB query and 15 assumptions, including that only the first worksite on each filing is checked. It hadn't run the query.
  - Follow-up, asking it to run the query: it reported 40. That's its own query under the same assumptions, so the number is unchecked, and it is not my answer key.
  - Both replies are saved word for word in `evals/chatgpt-test-2026-10-24.md`.
  - B04 is rebuilt around this test, and Vanna.ai is marked "not tested yet".
- **B10 updated.** It now lists three things that exist (brief, data file, ChatGPT test) and says nothing is loaded or built yet.
- **Re-render.** Regenerated audio for B00, B04, B07, B10 and B12, and re-rendered B00, B02, B04, B06, B07, B10 and B12. Runtime went from 197.3 s to 210.8 s (3:31), still under 4 minutes. Every gate passed, with GATE V at 0 BLOCKER and 0 MAJOR.
- **Found by looking at frames, not by any gate:** in B04, "its own run · unchecked" overlapped the page edge, and in B10 the "nothing loaded" caption ran into the divider. Fixed both and re-checked.
- **Toolkit untouched.** As before, the renderer added rows about this film to the shared `consumers.json`. I removed them and reset the timestamp, and the toolkit's file list and git status match the pre-render snapshot exactly.
