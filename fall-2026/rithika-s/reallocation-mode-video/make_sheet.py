#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for rithika-reallocation-mode-video (show-tell).

INFO 7375 mode video for the Reallocation Engine, by Rithika Sankar Rajeswari. Eight beats,
one drawn Manim scene each, on one cast: Sasha's identity card, the GATE row (G1 → G2 → Level
→ G3 → G4), the three exits (HELD / CLOSED / OVER-LEVEL), and terminal-style text cards that
carry real output verbatim. Bella narrates in the first person, as Rithika.

`script_text` is Rithika's script, VERBATIM (2026-10-21). `narration_text` is what Kokoro voices:
identical except for the audio-only respellings in PRONUNCIATION (on-screen text keeps the
standard spelling). Beat 8 is the outro (BOUT), drawn in Manim, as in the final-project film.

Audio: generate_audio_kokoro.py <reel> --speed 1.04, then pad each beat's mp3 with the silent
tail in TAIL_S (natural pauses between beats, to land the runtime in 3:45–3:55) and write the
measured durations back. Re-running this file rewrites beat_sheet.json from scratch and DROPS
measured audio fields; re-voice and re-pad afterwards.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "rithika-reallocation-mode-video"
TITLE = "A Mode for the Reallocation Engine"
VOICE = "af_bella"
SPEED = 1.04          # the course's speed limit for this video: max 1.04x
WPS = 2.86            # af_bella at 1.0, measured 2026-10-10 (final-project film)

# audio-only respellings, applied in order to script_text → narration_text
PRONUNCIATION = [
    ("H-1B", "H one B"),
    ("F-1", "F one"),
    ("OPT", "O P T"),
    ("G1", "G one"), ("G2", "G two"), ("G3", "G three"), ("G4", "G four"),
    ("API", "A P I"),
    ("TODOs", "to-dooz"),
    ("DRAFT", "draft"),
    # added after the whisper check (2026-10-21): heard "Risica", "in-stack art", "airbim"/"Airbent", "repose", "to DOS"
    ("Rithika", "Ritika"),          # soft dental t; Rithika to confirm
    ("Instacart", "Instuh cart"),
    ("Airbnb", "Air B N B"),
    ("repo's", "ree-poh's"),
]
NARRATION_ONLY = {}


def spoken(text, bid=None):
    for a, b in PRONUNCIATION:
        text = text.replace(a, b)
    for a, b in NARRATION_ONLY.get(bid, []):
        text = text.replace(a, b)
    return text


SPARSE = ("show-tell style: one drawn scene on a cream stage per beat, the voice carries the explanation. "
          "The negative space is the style, so only underfill and clustered are waived; edge-bleed, empty-frame "
          "and contrast still apply.")


def beat(bid, script, cls, image, show, constructed=False, sparse=True):
    b = {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
         "script_text": script, "narration_text": spoken(script, bid),
         "estimated_duration_s": round(len(script.split()) / WPS / SPEED, 1),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                  "manim": {"class": cls}, "motion_claim": image}}
    if constructed:
        b["constructed"] = True
        b["constructed_note"] = "Sasha Jones is a fictional persona; the card carries an on-screen 'fictional persona' label."
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}
    return b


B = [
 beat("B01",
  "Hi, I'm Rithika. This is my mode for the Reallocation Engine. It's built for Sasha Jones, a fictional F-1 master's student in data science. She graduates in December 2026, her OPT work permit should start in January 2027, and she's applying for entry-level Data Scientist roles that sponsor an H-1B. Like most students, she finds them on aggregator sites.",
  "B01_Persona",
  "Sasha's identity card slides in, labelled 'fictional persona'; its five fields fill in on the words (F-1, MS Data Science, grad Dec 2026, OPT Jan 2027, SOC 15-2051); three aggregator listing cards fan out behind it.",
  [{"at": 0.2, "event": "identity card + 'fictional persona'"}, {"at": 0.45, "event": "fields fill"}, {"at": 0.85, "event": "aggregator listings"}],
  constructed=True),
 beat("B02",
  "Here's what Sasha can't see. A job page can look open long after the employer closed the role. She can't tell whether a company that sponsors visas sponsors this role, or whether a live posting is even her level. And every dead application costs time, because once OPT starts she gets only ninety days of unemployment.",
  "B02_CantSee",
  "Three 'can't see' cards appear one by one (still open?, sponsors this role?, her level?), each with a closed-eye mark; then a 90-day clock whose hand sweeps.",
  [{"at": 0.15, "event": "card 1"}, {"at": 0.35, "event": "card 2"}, {"at": 0.55, "event": "card 3"}, {"at": 0.8, "event": "90-day clock"}]),
 beat("B03",
  "The mode runs gates in order. G1 checks the company in the engine's sponsorship data. G2 checks the job is live, and an aggregator saying \"active\" is never enough on its own. A level check makes sure the title fits an entry-level candidate. G3 checks the visa timeline, and G4 is a human. These are gates, not votes. A role that fails one never gets a score: it's held, closed, or over-level.",
  "B03_Gates",
  "A row of five gates (G1 sponsorship, G2 liveness, Level, G3 timeline, G4 human) lights up one by one; a role card rides through; three exit chutes drop below the row: HELD, CLOSED, OVER-LEVEL; label 'gates, not votes'.",
  [{"at": 0.1, "event": "G1"}, {"at": 0.25, "event": "G2"}, {"at": 0.45, "event": "Level"}, {"at": 0.55, "event": "G3, G4"},
   {"at": 0.7, "event": "gates, not votes"}, {"at": 0.85, "event": "HELD / CLOSED / OVER-LEVEL"}]),
 beat("B04",
  "I ran it on thirteen real postings. The key row is a Built In page for an Instacart Data Scientist job. The page says it was removed on June 11, 2025, yet the repo's checker still calls it active, sixteen months later. My first version marked that job Apply. This mode held it.",
  "B04_Removed",
  "Left: the Built In page card with its real banner text 'Sorry, this job was removed … Jun 11, 2025'. Right: the checker's real output line '✅ active'. Then a verdict strip: 'v0.1: Apply ✗ → this mode: HELD ✓'.",
  [{"at": 0.1, "event": "13 postings"}, {"at": 0.3, "event": "removed banner"}, {"at": 0.5, "event": "✅ active"}, {"at": 0.8, "event": "Apply ✗ → HELD ✓"}]),
 beat("B05",
  "Then I opened the pages myself, as the G4 human, and found two bugs in the existing checker. An Airbnb link scored Apply, but it redirected through Greenhouse's own error page to a general job list. And on a Nextdoor page, the checker missed an Apply button I could see.",
  "B05_Bugs",
  "The real Airbnb redirect chain draws hop by hop (301 → 302 ?error=true → 302 all-jobs → 200) beside 'checker: ✅ active'; then the Nextdoor card: 'Apply button visible → checker: uncertain'.",
  [{"at": 0.2, "event": "G4 human"}, {"at": 0.45, "event": "redirect chain hops"}, {"at": 0.6, "event": "checker: active"}, {"at": 0.85, "event": "Nextdoor: uncertain"}]),
 beat("B06",
  "So I fixed both inside my mode. Run 2 asks Greenhouse's job API for the actual job record, follows every redirect, and only trusts known employer and hiring-system sites. Airbnb became Closed, and Nextdoor became live. But that exposed a new problem: two Senior jobs now scored Apply for an entry-level student. Run 3 added a level gate on the title. Against my own decisions on the five postings I reviewed, agreement went three of five, then two, then four.",
  "B06_Fixes",
  "Three fix labels drop in (job record API · redirect chain · trusted-site allowlist); Airbnb Apply flips to CLOSED; two Senior cards flip to Apply; the Level gate stamps them OVER-LEVEL; three bars grow to 3/5, 2/5, 4/5.",
  [{"at": 0.1, "event": "three fix labels"}, {"at": 0.35, "event": "Airbnb → CLOSED"}, {"at": 0.5, "event": "Senior → Apply"},
   {"at": 0.65, "event": "level gate → OVER-LEVEL"}, {"at": 0.85, "event": "bars 3/5, 2/5, 4/5"}], sparse=False),
 beat("B07",
  "Two honest caveats. Those rules were checked on the same five postings I reviewed, so that isn't a held-out test. And some things it still can't see. Figma's title just says \"Data Scientist,\" but the description asks for experience. Sponsorship data is company-wide. And only Greenhouse has a record check so far.",
  "B07_Caveats",
  "A caveat card stamps 'Not a held-out test'; then three limit labels appear one by one (title ≠ description, company-wide sponsorship, Greenhouse only).",
  [{"at": 0.15, "event": "not a held-out test"}, {"at": 0.55, "event": "title ≠ description"}, {"at": 0.75, "event": "company-wide"}, {"at": 0.9, "event": "Greenhouse only"}]),
]

# Beat 8 is the outro (BOUT), drawn in Manim, as in the final-project film. No narration is added.
bout = beat("BOUT",
  "So the recipe stays DRAFT: it ran live three times, but typed TODOs are still open. My next step is a held-out test: decide on new postings first, then run the mode.",
  "BOUT_Status",
  "A status board: 'Status: DRAFT · ran live 3× · typed TODOs open'; then 'Next: held-out test' with its two steps (decide first → then run); the film title beneath.",
  [{"at": 0.2, "event": "status line"}, {"at": 0.6, "event": "Next: held-out test"}, {"at": 0.85, "event": "title"}])
bout["act"] = "outro"
bout["shot"]["remotion"] = {"props": {"title": TITLE, "handle": "INFO 7375 · Reallocation Engine", "subline": ""}}
bout["outro_note"] = ("As in the final-project film: beat 8 is the outro, drawn in Manim with the film title. The stock "
                      "ClaudeTitleOutro hard-codes the instructor's channel handle and mascot, which this student film may not carry. "
                      "No narration was added beyond Rithika's beat 8.")
B.append(bout)

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "INFO 7375 · REALLOCATION ENGINE MODE", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "info-7375", "channel_title": "",
    "persona": "Rithika Sankar Rajeswari (first person)", "author": "Rithika Sankar Rajeswari", "course": "INFO 7375",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro", "kokoro_speed": SPEED,
    "voice_reason": ("Same rule as Rithika's final-project film: Kokoro af_bella, first person, as her. The skill's LIAM BY DEFAULT law "
                     "(am_onyx, with an instructor greeting) belongs to the instructor's channel; this film carries no instructor identity."),
    "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "caption_reason": "As in the final-project film, no burned-in captions.",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Rithika's script is eight beats, read verbatim, with a hard 4:00 maximum. "
                              "(1) Runtime: the hesitant writer, key-terms card and Your Turn composer would add narration outside her script and push past 4:00. "
                              "(2) Branding: those components carry the instructor's identity, which this student film may not show. "
                              "(3) Beat 1 already introduces the persona and the problem; beat 3 defines the terms (gates, HELD, CLOSED, OVER-LEVEL). "
                              "The outro is never exempt: beat 8 is BOUT, drawn in Manim with the film title."),
    "privacy_rule": ("On screen: no screenshots, no personal information, no home-folder paths. The persona is fictional (Sasha Jones). "
                     "Real job URLs appear only as the host and path shown in the repo's own transcripts."),
    "constructed_rule": "B01 carries an on-screen 'fictional persona' label. All other figures are real output from the Reallocation Engine run files.",
    "pronunciation": [{"written": a, "spoken": b} for a, b in PRONUNCIATION],
    "audience": "the INFO 7375 grader; complete beginners to the Reallocation Engine",
    "source_doc": ("the-reallocation-engine, branch mode/rithika-sr-ds-h1b-liveness @ 817801c (read-only): "
                   "course/2026fa/submissions/rithika-sr/mode/{G4-HUMAN-REVIEW.md, WORKED-RUN.md, worked-run/EVALUATION.md, worked-run/terminal/*.txt}"),
    "playlist": "INFO 7375", "tags": ["job search", "H-1B", "liveness", "Greenhouse", "evaluation"]},
    "beats": B}
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(B), "beats;", sum(len(b["script_text"].split()) for b in B), "words; est", round(sum(b["estimated_duration_s"] for b in B)), "s")
