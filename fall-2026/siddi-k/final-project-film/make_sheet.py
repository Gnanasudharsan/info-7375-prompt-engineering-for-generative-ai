#!/usr/bin/env python3
"""make_sheet.py: writes beat_sheet.json for the Sponsor Triage pitch film.

Format: Brutalist show-tell (one drawn isometric picture per beat, labels only, the voice
explains). Departures from the skill's defaults, because the assignment says "Do not use the
instructor's name, persona, or credit line":
  * the narration is my first-person script voiced by Kokoro `af_heart` (free, local), not Liam
    (`am_onyx`/`am_liam`, "in for Bear"); a TA confirmed on 2026-10-14 that a Brutalist voice is fine;
  * the outro is my own Manim title card, not ClaudeTitleOutro (which hard-codes
    @NikBearBrown and the mascot); there are no BDEFS/BHTF composer bookends.

Re-running this script keeps measured audio fields (actual_duration_s, audio_file) from an
existing beat_sheet.json, so it is safe to run after the audio has been measured.

Honesty labels used on screen (the `tag` field, drawn bottom-left by scenes.py):
  RECORD   a real file/observation, with its date
  SKETCH   a constructed illustration of something that does not exist yet
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "sponsor-triage-pitch"
TITLE = "Sponsor Triage: A Final Project Pitch"
VOICE = "af_heart"   # Kokoro; not am_onyx / am_liam (the instructor's Liam persona)
SPARSE = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, the voice "
          "carries the explanation. Only underfill/clustered are waived; edge-bleed, empty-frame and contrast apply.")


def beat(bid, cls, narration, image, tag, show, sparse=True):
    b = {"beat_id": bid, "act": "pitch", "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration,
         "estimated_duration_s": round(len(narration.split()) / 2.4 + 0.6, 1),
         "voice": VOICE, "engine": "kokoro",
         "audio_file": f"audio/{bid}.wav",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                  "manim": {"class": cls}, "motion_claim": image, "tag": tag}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}
    return b


IDEA_TEXT = "Which companies sponsor\nH-1B visas"
BEATS = [
    {"beat_id": "BIDEA", "act": "the question", "lane": "bookend", "proof_gate": "SHOW",
     "narration_text": ("Hi, I'm Siddi Kommuri. I'm on an F-1 student visa, looking for data jobs. "
                        "The easy question is, which companies sponsor H-1B visas? "
                        "The one I actually need is narrower: which ones sponsor data roles?"),
     "estimated_duration_s": 15.0, "voice": VOICE, "engine": "kokoro",
     "audio_file": "audio/BIDEA.wav", "lead_silence_s": 0.8,
     "shot": {"type": "REMOTION", "source": "own",
              "show": [{"at": 0.0, "event": "types 'Which companies sponsor H-1B visas'"},
                       {"at": 0.7, "event": "backspaces 'H-1B visas' and types 'data roles'"}],
              "remotion": {"pattern": "BrutalistHesitantWriter",
                           "props": {"text": IDEA_TEXT, "triggerWords": "H-1B visas", "replacementWords": "data roles",
                                     "fontSize": 70, "charMs": 240, "hesitateBetween": 6, "hesitateWithin": 1,
                                     "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""}}},
     "motion_claim": "The writer types the general sponsor question and corrects it to the narrower one: data roles.",
     "qc": {"sparse_by_design": True, "sparse_reason": "Hesitant-writer opener: the correction is the motion."}},

    beat("B00", "B00_Triage",
         "My final project is Sponsor Triage, an agent that will check each job posting three ways: "
         "has this company sponsored a data role, is the posting live, and is there time left on my OPT? "
         "It will be a GitHub repo: the agent, tests, an evaluation, and a report.",
         "A queue of posting crates; the front one slides out and passes three check points (sponsor, live, time).",
         "SKETCH · proposed",
         [{"at": 0.1, "event": "queue of postings"}, {"at": 0.35, "event": "three check points appear"},
          {"at": 0.8, "event": "repo tag"}]),

    beat("B01", "B01_BigCount",
         "Why care? The usual shortcut is the approval count. In the 80 Days CSV, a course-repo table built from "
         "public H-1B data, Databricks has one thousand six hundred forty approvals, but its five top sponsored "
         "titles are software and solutions roles. None is a data role.",
         "A counter climbs to 1,640 beside a stack of five title pages; a scan line checks each page; the 'data role' slot stays empty.",
         "RECORD · 80 Days CSV line 7249",
         [{"at": 0.3, "event": "counter climbs to 1,640"}, {"at": 0.6, "event": "five title pages scanned"},
          {"at": 0.9, "event": "data-role slot stays empty"}]),

    beat("B02", "B02_Ghost",
         "Second, the repo's own page check. On October third, my recipe gave it a Klaviyo job ID that doesn't exist. "
         "The page said active. Greenhouse's API said four oh four. My recipe already lets the API win.",
         "A posting page with an Apply button gets a check (page: active); a server answers 404; the posting drops off the line.",
         "RECORD · constructed job id, 2026-10-03",
         [{"at": 0.2, "event": "page with Apply"}, {"at": 0.5, "event": "page says active"},
          {"at": 0.75, "event": "API says 404; posting dropped"}]),

    beat("B03", "B03_Reader",
         "Who opens it? Students like me, and a hiring manager for data engineering roles. In the first minute, "
         "they'll run one offline command and read the report, every decision and number traced to a file and line.",
         "A workstation runs one command; a report page slides out with four decision rows; a leader line ties one number to 'file:line'.",
         "SKETCH · proposed",
         [{"at": 0.3, "event": "one command"}, {"at": 0.55, "event": "report with four rows"},
          {"at": 0.85, "event": "file:line"}]),

    beat("B04", "B04_Loop",
         "What would it prove? That I can build an agent loop with limits. It'll take a posting, pick the missing "
         "check, call one tool, and record the result with its source. It'll stop when the queue is empty or the "
         "budget runs out, not when a model says so.",
         "Queue to tool to evidence binder in a loop; one budget slot empties per pass; the loop stops when the slots are gone.",
         "SKETCH · proposed",
         [{"at": 0.25, "event": "loop runs once"}, {"at": 0.5, "event": "budget slot spent"},
          {"at": 0.85, "event": "stop"}]),

    beat("B05", "B05_Fence",
         "Its tools will be fenced in code: the CSV and Greenhouse's API, nothing else. It will never apply or "
         "message anyone, and it won't promise that a specific job will be sponsored.",
         "A permission gate lifts for the Greenhouse API request and stays down for any other request, which bounces back.",
         "SKETCH · proposed",
         [{"at": 0.3, "event": "allowed request passes"}, {"at": 0.6, "event": "other request refused"}]),

    beat("B06", "B06_Gate",
         "Every Apply and every Unresolved will come back to me with its evidence, and I'll approve, refuse, or "
         "defer. That's the human gate.",
         "A handoff desk slides the evidence packet across to the human side; a stamp comes down on it.",
         "SKETCH · proposed",
         [{"at": 0.3, "event": "packet handed over"}, {"at": 0.75, "event": "stamp"}]),

    beat("B07", "B07_Eval",
         "The proof will be an evaluation: about forty hand-labelled public postings, some held back, and at least "
         "five planted failures. I don't know yet whether Claude helps classify job titles. I'll test it against "
         "the recipe's patterns, and keep whichever wins.",
         "Two trays (patterns vs Claude) face the same labelled set; a held-back drawer stays shut; the trays wait for a score.",
         "SKETCH · proposed",
         [{"at": 0.25, "event": "labelled set; held-back drawer"}, {"at": 0.65, "event": "patterns vs Claude trays"}]),

    beat("B08", "B08_First",
         "First, I'll build the loop, offline, on the seven postings from that October run, two of them made-up "
         "tests. I'll know it ran if it exits cleanly, stays under budget, and matches the recipe: one Apply, "
         "two Consider, one Skip, three Unresolved.",
         "Seven crates on a conveyor (two marked as tests); four tallies rise to 1, 2, 1, 3, matching the recipe's run.",
         "RECORD · run of 2026-10-03 · next: SKETCH",
         [{"at": 0.2, "event": "seven postings"}, {"at": 0.65, "event": "tallies 1·2·1·3"}]),

    beat("B09", "B09_Risk",
         "The risk is thin data. More than half the sponsoring companies in the CSV list just one title. In my run, "
         "two real postings came out Unresolved, and two only Likely. I'll measure that rate first, and if it's too "
         "high, use the Labor Department's disclosure data, which lists the job title on every application.",
         "'862 of 1,552 list one title'; five real crates: two get a question mark, two a half mark; then a second data source connects by cable.",
         "RECORD · CSV, run of 2026-10-03; DOL link: SKETCH",
         [{"at": 0.0, "event": "862 of 1,552"}, {"at": 0.4, "event": "two unresolved, two likely"}, {"at": 0.8, "event": "DOL source connects"}]),

    beat("B10", "B10_Why",
         "Why this project? It's my own problem, so I'll notice when it's wrong. It's a mix: I've built Python data "
         "work and an NBA RAG app with a retrieval evaluation. Agent loops, permissions and held-out evaluation "
         "are new.",
         "Two shelves: 'built' holds a finished binder (NBA RAG app); 'new' is an experiment bench where a sample slides in.",
         "RECORD · NBA RAG app, Dec 2025",
         [{"at": 0.35, "event": "built shelf"}, {"at": 0.75, "event": "new bench"}]),

    beat("B11", "B11_Honest",
         "One honest note: in the recipe, Claude wrote the code and I accepted it unchanged. This time I'll write "
         "the contract and tests first, and check the rows myself. Today, the recipe and its twelve passing tests "
         "exist. Everything else here is a plan.",
         "A solid small stack (recipe + 12 tests) labelled 'exists' beside a ghost-outlined larger stack labelled 'will exist'.",
         "RECORD · tests re-run 2026-10-14",
         [{"at": 0.3, "event": "contract page lands before code"}, {"at": 0.7, "event": "exists vs will exist"}]),

    beat("BOUT", "BOUT_Title",
         "Sponsor Triage. A pitch by Siddi Kommuri.",
         "Title card: 'Sponsor Triage', my name, and the date; one terracotta dot lands.",
         "", [{"at": 0.0, "event": "title"}, {"at": 0.5, "event": "name"}]),
]
BEATS[-1]["tail_silence_s"] = 1.0

old = {}
p = HERE / "beat_sheet.json"
if p.exists():
    for b in json.loads(p.read_text(encoding="utf-8")).get("beats", []):
        old[b["beat_id"]] = b
for b in BEATS:
    o = old.get(b["beat_id"], {})
    for k in ("actual_duration_s", "audio_file"):
        if k in o:
            b[k] = o[k]
    if b["beat_id"] == "BIDEA" and "actual_duration_s" in b:
        b["shot"]["remotion"]["props"]["durationSeconds"] = b["actual_duration_s"]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "FINAL PROJECT PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "siddi-k", "persona": "Siddi Kommuri (my script; synthetic voice Kokoro af_heart)", "voice": VOICE,
    "voice_kokoro": VOICE, "engine": "kokoro", "clock": "narration", "palette": "claude", "register": "plain", "fps": 24,
    "aspect_ratio": "16:9", "width": 3840, "height": 2160, "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Course pitch film: the assignment forbids the instructor's persona and credit line, "
                              "so the composer bookends and ClaudeTitleOutro (@NikBearBrown, mascot) are replaced "
                              "by my own Manim title card; narration is my script in Kokoro af_heart, not Liam."),
    "audience": "INFO 7375 reviewers; a hiring manager for data/analytics engineering roles",
    "source_doc": "PROJECT-BRIEF.md; evidence/ (recipe report 2026-10-03, test re-run 2026-10-14, CSV line 7249)",
    "tags": ["INFO 7375", "final project pitch", "agentic AI", "H-1B", "F-1", "data engineering"]},
    "beats": BEATS}
p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
words = sum(len(b["narration_text"].split()) for b in BEATS)
print(len(BEATS), "beats;", words, "words; est", round(sum(b["estimated_duration_s"] for b in BEATS)), "s")
