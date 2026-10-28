# SCRIPT-DRAFT — Co-op Sponsor Check (pitch film)

> **Superseded 2026-10-12.** Kept as the first draft. The final narration is `beat_sheet.json`
> (B05 became B05/B05A from a real USCIS hub search; B11 became B11/B11A from my own choices).

Draft narration, one beat per idea, for review before it becomes `beat_sheet.json`.
Voice: Kokoro `bf_emma` (free, local, British English) — my choice, 2026-10-12. The persona is removed: my name replaces "Liam, in for Bear"; no instructor outro or portraits.
Tense rule: past tense = exists and shown in `evidence/`; everything else = "will".
Beats marked **[YOU]** wait on my own text in PROJECT-BRIEF §2 and §7.

| Beat | Picture (one drawing) | On-screen label | Narration |
|---|---|---|---|
| BIDEA | hesitant writer types "Will this company sponsor me", corrects to "Has this company sponsored software jobs" | — | Hello. I'm Arundhati Kandelkar, and you're hearing a synthetic voice reading my script. This is a pitch, not a finished build. The question I started with was "will this company sponsor me?" The question a tool can actually answer is narrower: has this company sponsored software jobs before? |
| BDEFS | terms card | sponsorship record · co-op · unknown | Three terms. A sponsorship record is a public government record of an employer filing for a work visa. A co-op is a paid work term during my degree. And unknown means the data is silent, which is not the same as no. |
| B00 | a company box arrives on a desk next to a spreadsheet page | company | The tool will take a list of companies and the job I want, which is software or full-stack development. |
| B01 | the box opens: three parts — a record page, a calendar, a check | record · dates · check | For each company it will answer three things: is there a record of sponsoring software titles, does the co-op fit before my graduation date, and is the posting still live. |
| B02 | a box rides to a gate marked "not in data"; the gate shows "?" not "0" | unknown, not 0 | This part already exists. I built it as a recipe in the Reallocation Engine, pushed on October third. When a company is missing from the data, it says unknown and tells you to ask a person. It never prints zero. |
| B03 | three bank boxes fall through a gap in the spreadsheet | SEC list | Building it, I found its biggest limit. JPMorgan Chase, Goldman Sachs and Morgan Stanley were not in the dataset at all. The dataset's own notes say it starts from a list of funded companies filed with the S E C, so the large banks were never in it. |
| B04 | test tray: 17 small checks light up | 17 tests | Seventeen tests passed when I built it, and again when I re-ran them on October tenth. They cover six failure cases, including a fake posting and two company names that might be the same firm. |
| B05 | [YOU] the alternatives — two windows side by side, one searched by hand | [YOU] | [YOU — after you open the USCIS Data Hub and one other tool: what each does, and the one thing mine does that they don't] |
| B06 | a second data page slides under the first, filling the gap | second source | What will exist: a second public data source to fill that gap, so a missing bank becomes a real answer or an honest unknown. |
| B07 | 25 boxes in a grid; each gets a tick or a cross from a hand check | 25 checked | And an evaluation. I will check twenty-five real companies by hand against public records and compare each one to the tool's answer. The first thing I will make run is that comparison. You'll know it ran when the table of matches and mismatches is committed, with its date. |
| B08 | two labels on one box: "BNY Mellon" / "Bank of New York Mellon"; a human-check stamp | same company? | The risk that could sink it is names. "B N Y Mellon" and "The Bank of New York Mellon" may be one employer or two. A wrong match turns a sponsor into unknown, or borrows another company's record. So the tool will not guess. It will show the candidates to a person, and I will report how many of the twenty-five needed one. |
| B09 | a stop sign beside a scales icon | not legal advice | One thing it will deliberately not do: give immigration advice, or predict whether anyone gets a visa. It reports history, with every answer labelled as a record, a judgment, or your own input. |
| B10 | a hiring manager's screen: README, one command, the report | 60 seconds | Who opens it? A hiring manager or engineer hiring software developers. In the first minute they will run one command and see a report that says unknown where the data is silent, next to a table of where the tool was right and wrong. |
| B11 | [YOU] | [YOU] | [YOU — why this project: what is new to me, what I already know, and the evidence for it] |
| BHTF | composer: "Your turn" | — | Your turn. Pick one company you would apply to. Look it up in the public U S C I S H-1B Employer Data Hub, and write down whether it is there under one name or several. |
| BOUT | title card, no instructor credit | Co-op Sponsor Check | Co-op Sponsor Check. A pitch by Arundhati Kandelkar. |

## Honesty audit to run on the final script (every beat, bookends included)

- B02, B04: dates and counts must match `evidence/recipe-rerun-2026-10-10.txt` and the `03784b0` commit date.
- B03: the SEC claim must quote what the dataset README actually says; no stronger.
- B05: only what I wrote after looking at the alternatives myself.
- B06–B10: all "will", nothing implying it already runs.
- BIDEA/BOUT: synthetic voice disclosed; no instructor name, persona or credit line.
- Any drawing of a screen or report not yet built gets an on-screen "constructed" label.
