# SHOTLIST — SponsorScout

One picture per beat, one idea per beat (revision of 2026-10-14, after Akshit's notes). All
drawings are Manim scenes in `scenes.py`. **Every body beat carries a corner tag**:
`constructed drawing` plus `ran <date>` or `proposed`, so a drawing is never mistaken for a
screenshot and ran is never confused with proposed. The title beat shows the legend
(solid dot = ran, dashed ring = proposed).

**How every scene moves:** a staggered entrance; each reveal starts on its spoken word
(`mp3/words.json`, from `align.py`); a fade to the stage at the end, which gives a smooth dip
between beats. Nothing is drawn below y = −2.5, where the captions sit.

**Cast (same objects all film):** kraft **crate** = one company · **dark block** = a machine
(SponsorScout, the engine scorer, the resolver) · **trays** = verdicts · **gates/walls** = checks
· **sheets** = records and reports. Depth is correct: a crate passes *between* a gate's back
and front posts, and sits *inside* a tray, between its back and front walls.

| Beat | Answers | Picture | Corner tag |
|---|---|---|---|
| BOPEN | name, author | SponsorScout writes on beside its mark (a crate under a scout's lens); byline; legend ran / proposed | — (title) |
| BIDEA | the question | "Which companies should I apply to?" → "apply to?" greys out with a cross beside it → "network with?" | — (title) |
| B00 | Q1 what is it | company → SponsorScout block → fan of 4 arrows → apply / network / check by hand / skip, each on its word; a record slip | proposed |
| B01 | Q1 artifact | Repository box; Python · Claude Code · public data; recipe, prototype, tests, eval log, report fly out on their words | proposed |
| B02 | how it works | Moving conveyor, 3 depth-correct gates; lamps pulse; sponsored? (H-1B) · funded? (Form D) · open today? (job board) | ran 2026-10-03 |
| B03 | Q2 alt 1 | Engine scorer path (grey, dashed) → 0 → skip, vs SponsorScout path (solid) → network list | ran 2026-10-03 |
| B04 | Q2 alt 2 | MyVisaJobs panel with past-count bars; crate → network route crossed out ("no network step") | looked 2026-10-07 |
| B05 | Q3 reader | Briefcase: data analyst / data engineer / hiring manager; 60 s clock; command → report → source record | proposed |
| B06 | exists | Four trays; the real run-2 counts 2 · 1 · 107 · 13 on their words; 16 boards, 123 sponsors; job seeker fictional | real counts · run-2 · 2026-10-03 |
| B07 | Q4 verification | Zoox crate lands in apply; scan + flag; moved to excluded; test pill; 25 / 25 tests pass · Oct 12 | ran 2026-10-03 & 10-12 |
| B08 | Q4 grounding | Report rows marked record (●) / my input (○); a wall stops an unconfirmed crate before the scorer | ran 2026-10-03 |
| B09 | Q4 loop + eval | Loop with two human-gate squares; token stops; my sign-off; dashed empty eval log (proposed) | gates ran · eval proposed |
| B10 | Q5 out | Apply / email / contact slide to a wall, crossed out; you decide; no résumé | proposed |
| B11 | Q5 first | Board resolver; the real 16 / 123; a bar that never grows (no invented progress); dashed up-arrow | 16/123 real · resolver proposed |
| B12 | Q6 risk | Vault (no public board?) blocks a crate → check by hand; Greenhouse, Lever, Ashby; no scraping; coverage as a number | proposed |
| B13 | Q6 unknown | recent funding → hiring?; a 14-day calendar fills; an empty "?" result box | proposed |
| B14 | Q7 why | 100+ applications → a short list; stack: prototype code: Claude Code (grey) · the rules: mine · gate sign-offs: mine · new: evaluation, resolving boards (dashed) | constructed drawing |
| BOUT | outro | `PitchOutro`: SponsorScout · a pitch by Akshit Verma · INFO 7375 · Final Project Pitch | — |

## Changed from the show-tell defaults, and why

| Default | Changed to | Reason |
|---|---|---|
| "Hallo. This is Liam, in for Bear." | "SponsorScout. A final project pitch by Akshit Verma." | Assignment: narrate as yourself, no instructor persona. "By" means the voice never claims to be Akshit |
| Kokoro `am_onyx` (Liam) | `am_michael` (Akshit's choice, 2026-10-14) | Same. The synthetic voice is disclosed in README.md and SOURCES.md, not on screen (Akshit's choice) |
| Hesitant-writer cold open (Remotion) | `BOPEN_Title` + `BIDEA_Question` (Manim) | Akshit: open on the project's name; one visual style for the whole film |
| `@NikBearBrown` outro (`ClaudeTitleOutro`) | `PitchOutro`, credited to Akshit Verma | No instructor credit line. `bookend_check.py` checks the outro handle against `channel_title` ("Akshit Verma") |
| BDEFS terms card | Terms defined inline | Keeps the film inside 2–4 min (show-tell law 3) |
| BHTF Your Turn (Claude.ai composer) | Exempt | A pitch has no viewer task, and a Claude-styled composer would suggest a Claude exchange that didn't happen |
| Professor Bear portrait for people | No people drawn (a briefcase for the reader) | The portrait is the instructor's likeness |
| One to three labels per beat | Up to seven short labels | Akshit: the visuals should explain the content, not only illustrate it |
