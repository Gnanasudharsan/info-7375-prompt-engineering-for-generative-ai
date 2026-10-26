#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for coop-sponsor-check-pitch.

INFO 7375 Final Project pitch film by Arundhati Kandelkar. Built with the brutalist.art
`show-tell` skill: one drawn picture per beat, minimal labels, the voice explains.

Assignment overrides of the skill's house defaults (the assignment governs):
  - narrated in my name, not "Liam, in for Bear"; voice Kokoro bf_emma (my choice, 2026-10-12)
  - no instructor name, persona, handle or portrait anywhere; outro shows my name
Tense rule: past tense = exists and is in evidence/; everything else = "will".
Every body beat carries an on-screen tag: EXISTS (with its evidence) or PLANNED / CONSTRUCTED.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "coop-sponsor-check-pitch"
TITLE = "Co-op Sponsor Check"
VOICE = "bf_emma"
NAME = "Arundhati Kandelkar"


def est(n):
    return round(len(n.split()) / 2.5, 1)


def beat(bid, narration, cls, image, show):
    return {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
            "narration_text": narration, "estimated_duration_s": est(narration),
            "voice": VOICE, "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                     "manim": {"class": cls}, "motion_claim": image}}


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show,
                  "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


OPEN = [
 remotion("BNAME", "who",
    f"Hello. I'm {NAME}, a master's student at Northeastern.",
    "BrutalistHesitantWriter",
    {"text": "Arundhati Kandelkar\nMSIS, Northeastern University", "triggerWords": "", "replacementWords": "",
     "fontSize": 72, "charMs": 22, "hesitateBetween": 2, "hesitateWithin": 0, "mistakeRate": 0, "jitter": 10,
     "seed": SLUG + "-name", "banner": ""},
    [{"at": 0.0, "event": "my name types"}],
    lead_silence_s=0.5, motion_claim="My name and programme type in while I say them.",
    qc={"sparse_by_design": True, "sparse_reason": "Name card: the name is the whole picture."}),
 remotion("BBUILD", "what",
    "I'm building Co-op Sponsor Check: a tool that tells international students whether a company has ever sponsored someone for a software job.",
    "BrutalistHesitantWriter",
    {"text": "I'm building Co-op Sponsor Check", "triggerWords": "", "replacementWords": "",
     "fontSize": 72, "charMs": 18, "hesitateBetween": 0, "hesitateWithin": 0, "mistakeRate": 0, "jitter": 8,
     "seed": SLUG + "-build", "banner": ""},
    [{"at": 0.0, "event": "types 'I'm building Co-op Sponsor Check' as it is spoken"}],
    motion_claim="The one-sentence summary types in as it is spoken.",
    qc={"sparse_by_design": True, "sparse_reason": "One-sentence summary card."}),
 remotion("BIDEA", "the question",
    "When international students like me pick an internship, we need to know one thing: has this company ever sponsored someone for a software job? "
    "Today we guess, and a missing record looks like a no. My tool says I don't know, instead of guessing no.",
    "BrutalistHesitantWriter",
    {"text": "Does this company sponsor visas", "triggerWords": "sponsor visas",
     "replacementWords": "have a record of sponsoring software jobs",
     "fontSize": 64, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
     "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types the naive question"}, {"at": 0.5, "event": "corrects 'sponsor visas' to the narrower question"}],
    motion_claim="The naive question is corrected to the one a tool can answer.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
]

B = [
 beat("BWHAT", "When it's done, it will be a public GitHub repository: the tool, a twenty-five company evaluation set, and a log of where it fails.",
      "BWHAT_Repo", "A repository folder tray holding three things: the company box (the tool), a small grid (the evaluation set), a page (the failure log); tag 'PLANNED · finished form'.",
      [{"at": 0.15, "event": "repo tray"}, {"at": 0.3, "event": "three parts drop in"}, {"at": 0.62, "event": "folder tab"}]),
 beat("B00", "Here is what exists today. On October third I pushed a recipe to my fork of the Reallocation Engine. "
      "It takes a company and the job I want, software or full-stack development.",
      "B00_Arrives", "A kraft company box drops onto the stage beside a flat data page; tag 'EXISTS · 03784b0'.",
      [{"at": 0.1, "event": "box drops in"}, {"at": 0.6, "event": "tag"}]),
 beat("B01", "For each company it checks three things. Is there a record of sponsoring software titles? "
      "Does the co-op start before graduation? And is the job posting still live?",
      "B01_Three", "The box opens; a record page, a calendar block and a check rise out of it, one per question.",
      [{"at": 0.15, "event": "record page"}, {"at": 0.35, "event": "calendar"}, {"at": 0.62, "event": "live check"}]),
 beat("B02", "When a company is missing from the data, it does not treat that as zero. "
      "It says unknown, and tells you to ask a person.",
      "B02_Unknown", "A box rides up to a gate; the gate shows a question mark, never a zero.",
      [{"at": 0.2, "event": "box rides to gate"}, {"at": 0.62, "event": "question mark"}]),
 beat("B03", "Building it, I found its biggest limit. The big banks were not in the dataset at all, because it was built from a list of funded startups taken from S E C filings.",
      "B03_Gap", "A data page with a gap; three bank boxes drop toward it and pass through the gap.",
      [{"at": 0.2, "event": "page with gap"}, {"at": 0.35, "event": "three boxes fall through"}]),
 beat("B04", "Eighteen tests pass today: six failure cases, plus a new test for a bug the evaluation found.",
      "B04_Tests", "A tray of eighteen small slots; each gets a check; tag 'EXISTS · 18 / 18 · 2026-10-24'.",
      [{"at": 0.15, "event": "checks land"}, {"at": 0.62, "event": "tag"}]),
 beat("B05", "The real alternative is the official U S C I S, H-1B Employer Data Hub. Searched on October twelfth, it does list JPMorgan Chase, which my dataset is missing. "
      "But it is searched one employer at a time, by name, place or industry, not by job title.",
      "B05_Hub", "A search window with a query bar and one result row; beside it a 'job title' filter pill gets crossed out; tag 'SEARCHED · uscis.gov · 2026-10-12'.",
      [{"at": 0.15, "event": "search window + one row"}, {"at": 0.62, "event": "job-title pill crossed out"}]),
 beat("B05A", "And a search for Mellon returned four employers: three B N Y companies, and Carnegie Mellon University. "
      "My tool will check a whole list for software titles and co-op dates, and it already has a test that refuses a match on part of a name.",
      "B05A_Mellon", "The four names the hub returned for 'Mellon', in its order; the three BNY rows get kraft markers, Carnegie Mellon gets a cross.",
      [{"at": 0.15, "event": "four names"}, {"at": 0.62, "event": "markers and cross"}]),
 beat("B06", "Now, what will exist. A second public data source, to fill that gap, "
      "so a missing bank becomes a real answer or an honest unknown.",
      "B06_Second", "A second page slides under the gapped page and fills the hole; tag 'PLANNED'.",
      [{"at": 0.2, "event": "second page slides in"}, {"at": 0.62, "event": "gap filled"}]),
 beat("B07", "Then I tested it on twenty-five companies. Every company I looked up in the official hub was there. My tool found a record for only two. "
      "It never guessed no. But that number told me something was wrong.",
      "B07_Eval", "A grid of twenty-five company squares; the first six fill grey and their rows land in the results table; the rest stay empty; tag '6 RAN · 2026-10-12 · 19 PLANNED'.",
      [{"at": 0.15, "event": "grid"}, {"at": 0.3, "event": "six squares fill, six rows land"}, {"at": 0.62, "event": "magnifier moves to square seven"}]),
 beat("B07A", "Two real problems. First, my matcher turned Goldman Sachs and Co, L L C, into Goldman Sachs and. "
      "It is fixed now, with a test that failed before the fix and passes after.",
      "B07A_Bug", "The hub's name 'GOLDMAN SACHS AND CO LLC', an arrow, and the matcher's output 'GOLDMAN SACHS' with a tick; tag 'FIXED · 2026-10-24'.",
      [{"at": 0.15, "event": "hub name"}, {"at": 0.3, "event": "arrow and fixed output"}, {"at": 0.62, "event": "tick"}]),
 beat("B07B", "Second, brand names. Typing Robinhood found nothing, but my data holds Robinhood Markets, with eight hundred and twenty-four approvals. "
      "Chime, and So Fi, failed the same way. That is the next fix.",
      "B07B_Brand", "A typed name 'Robinhood' leads to a question mark; beside it, the dataset row 'ROBINHOOD MARKETS INC · 824' it missed; tag 'FOUND · 2026-10-25'.",
      [{"at": 0.15, "event": "typed name and question mark"}, {"at": 0.62, "event": "the missed row lights up"}]),
 beat("B08", "So the risk that could sink this is names, and my test proved it. B N Y Mellon, and The Bank of New York Mellon, may be one employer or two. "
      "The tool will not guess. It will show the likely legal names to a person, who decides.",
      "B08_Names", "One box with two name tags pulling in different directions; a 'human check' stamp lands between them.",
      [{"at": 0.2, "event": "two tags"}, {"at": 0.62, "event": "human check stamp"}]),
 beat("B09", "One thing it will deliberately not do: give immigration advice, or predict whether anyone gets a visa. It reports history.",
      "B09_Out", "A stop sign beside the box; three small label tags clip onto the box.",
      [{"at": 0.2, "event": "stop sign"}, {"at": 0.62, "event": "three label tags"}]),
 beat("B09P", "What does it prove? Verification: every answer is labelled as a record, a judgment, or your input. "
      "Evaluation: twenty-five answers were checked against the official hub. Source grounding: every sponsor record in the run log cites its C S V line.",
      "B09P_Proves", "Three trays in a row, labelled verification, evaluation, source grounding: label tags on a box; a ticked six-row table; a page with a line pointer; tag 'WHAT IT PROVES'.",
      [{"at": 0.15, "event": "three trays and labels"}, {"at": 0.62, "event": "a terracotta dot lands on each"}]),
 beat("B10", "Who opens it? A hiring manager or engineer hiring software developers. "
      "In the first minute, they will run one command, and see a report that says unknown where the data is silent, "
      "next to a table of where the tool was right and wrong.",
      "B10_Reader", "A laptop window: a terminal line, then a report with a question mark row and a small right/wrong table; tag 'CONSTRUCTED'.",
      [{"at": 0.15, "event": "window"}, {"at": 0.35, "event": "report rows"}, {"at": 0.62, "event": "right/wrong table"}]),
 beat("B11", "Why this project? It's my own question. I'm an international student, and this is what I face when choosing a co-op.",
      "B11_Why", "The company box beside a calendar block, with a large question mark above the box; tag 'WHY THIS PROJECT'.",
      [{"at": 0.15, "event": "box and calendar"}, {"at": 0.62, "event": "question mark lands"}]),
 beat("B11A", "So it's a mix. I already build Java and Spring Boot services. I did it for three years as a software developer at G plus D, but this project doesn't show that. "
      "What's new for me is joining a second public data source into a small Python tool.",
      "B11A_Skills", "Two trays: 'already have' with greyed blocks, labelled Giesecke+Devrient; 'new' with the second data page sliding in.",
      [{"at": 0.15, "event": "two trays"}, {"at": 0.62, "event": "second page into the new tray"}]),
]

YT_PROMPT = ("List every legal name [company] might file U.S. work-visa paperwork under. Mark the ones you are not sure of.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_PROMPT.replace("[company]", "a company you choose").replace("U.S. work-visa", "United States work visa") +
    " Then look each name up in the U S C I S hub, and count the ones that were wrong.",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Check One Company", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: look each name up in the USCIS H-1B Employer Data Hub.",
                "Check: count the names that were wrong or made up."],
     "folderLabel": NAME, "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.1, "event": "the prompt types in full"},
     {"at": 0.8, "event": "two check lines land"}])

SPARSE_REASON = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, the voice "
                 "carrying the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and contrast still apply.")
for b in B:
    b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}

BEATS = OPEN + B
BEATS.append({"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
              "narration_text": f"{TITLE}. Pitched by {NAME}.", "estimated_duration_s": 4.0,
              "voice": VOICE, "engine": "kokoro",
              "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title; my name"}],
                       "remotion": {"pattern": "ClaudeTitleOutro",
                                    "props": {"title": TITLE, "slug": SLUG, "handle": NAME, "subline": ""}}},
              "kind": "outro_voice", "tail_silence_s": 1.0})

# carry measured audio forward across regenerations (SKILL.md card trap 4)
old = {}
if (HERE / "beat_sheet.json").exists():
    for b in json.loads((HERE / "beat_sheet.json").read_text()).get("beats", []):
        old[b["beat_id"]] = b
for b in BEATS:
    o = old.get(b["beat_id"])
    if o and o.get("narration_text") == b["narration_text"]:
        for k in ("actual_duration_s", "audio_file"):
            if k in o:
                b[k] = o[k]
        if b["shot"].get("remotion") and "actual_duration_s" in b:
            b["shot"]["remotion"]["props"]["durationSeconds"] = round(b["actual_duration_s"], 2)

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "INFO 7375 · FINAL PROJECT PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "info7375-student", "channel_title": NAME, "persona": NAME, "voice": VOICE, "voice_kokoro": VOICE,
    "engine": "kokoro", "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24,
    "aspect_ratio": "16:9", "width": 3840, "height": 2160, "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": "Your Turn cut for concision (TA feedback 2026-10-21: concise pitch). show-tell style: opens on the hesitant writer + terms card, no verdict card; Your Turn is the composer; spoken outro stays (with the student's name, per the assignment).",
    "audience": "INFO 7375 instructor and TAs; later, hiring managers for software developer roles",
    "source_doc": "PROJECT-BRIEF.md; the-reallocation-engine fork at 03784b0; evidence/recipe-rerun-2026-10-10.txt",
    "playlist": "INFO 7375 Final Project", "chapter_number": 0,
    "tags": ["INFO 7375", "final project", "pitch", "H-1B", "co-op", "evaluation"]},
    "beats": BEATS}
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(BEATS), "beats; est", round(sum(b["estimated_duration_s"] for b in BEATS)), "s")
