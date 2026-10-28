#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for the INFO 7375 Final Project Pitch Film.

Format: brutalist.art show-tell (skills/make/show-tell/SKILL.md, upstream 4115560):
one drawn isometric picture per beat, labels of one to three words, the narration
carries the explanation. Changed from the skill's defaults because the assignment
says "narrate as yourself; do not use the instructor's name, persona, or credit line":
no "Liam, in for Bear" greeting, not the am_onyx Liam voice, no claude-liam channel,
and the outro credits Akshit Verma instead of @NikBearBrown. The BDEFS terms card is
dropped to stay inside 2-4 minutes; each term is defined in the breath it is first
used (show-tell law 3).

Honesty rule (assignment): every drawn beat carries an on-screen corner tag saying it
is a constructed drawing, plus whether what it shows RAN (with the date) or is PROPOSED.
Every number spoken or shown comes from Assignment 1's committed run outputs; the
source of each claim is in FACTCHECK.md.

Run: python make_sheet.py   (writes beat_sheet.json next to this file)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "sponsorscout-final-project-pitch"
TITLE = "SponsorScout"
AUTHOR = "Akshit Verma"
VOICE = "am_michael"          # Kokoro v1.0, free and local; NOT am_onyx ("Liam")
WPS = 2.6                     # measured for am_michael at speed 1.0 on 2026-10-14 (2.57-2.73 w/s); audio sets the real length
TODO = "[AKSHIT TO WRITE"     # sentinel: narration that must be written by Akshit, not Claude
# Akshit's own look at myvisajobs.com, as YYYY-MM-DD. None = not yet checked: B04 cannot be voiced,
# because the assignment requires alternatives "you actually looked at" and no invented competitor claims.
MYVISAJOBS_CHECKED = "2026-10-07"   # Akshit's own look, reported to Claude on 2026-10-14


def est(text):
    return round(len(text.split()) / WPS, 1)


def beat(bid, answers, tag, narration, cls, image, show, labels, prop=None):
    """One body beat: one Manim drawing, labels beside objects, corner honesty tag."""
    return {
        "beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
        "answers": answers,
        "honesty_tag": tag,
        "narration_text": narration, "estimated_duration_s": est(narration),
        "voice": VOICE, "engine": "kokoro",
        "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image,
                 "labels": labels, "prop": prop,
                 "show": [{"at": 0.02, "event": f"corner tag lands: '{tag}'"}] + show,
                 "manim": {"class": cls}, "motion_claim": image},
    }


def remotion(bid, act, answers, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate, "answers": answers,
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show,
                  "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


RAN = "constructed drawing · ran 2026-10-03"
PROPOSED = "constructed drawing · proposed"

OPEN = [
    # 2026-10-14 revision (Akshit): open on the project's name, then explain. The toolkit's hesitant-writer
    # card is replaced by Manim drawings in the film's own style. The voice says "a pitch BY Akshit Verma",
    # so it never claims to BE Akshit; that the narration is synthetic is disclosed in README.md and SOURCES.md.
    beat("BOPEN", "title", "",
        "SponsorScout. A final project pitch by Akshit Verma. I'll show what already ran, and what I will build.",
        "BOPEN_Title",
        "The word SponsorScout writes itself in large serif type above a short terracotta rule; a small crate "
        "settles beside it; 'a final project pitch by Akshit Verma' fades in below; on 'already ran' and "
        "'will build' two key chips appear: a solid chip 'ran' and a dashed chip 'proposed'. That's the "
        "legend for every corner tag that follows.",
        [{"at": 0.05, "event": "SponsorScout writes on"}, {"at": 0.35, "event": "byline"},
         {"at": 0.7, "event": "legend chips: ran (solid) / proposed (dashed)"}],
        ["SponsorScout", "ran", "proposed"]),
    beat("BIDEA", "the question", "",
        "The question isn't which companies to apply to. It's which ones to network with.",
        "BIDEA_Question",
        "The question writes itself on a card: 'Which companies should I apply to?'. On 'network with', "
        "'apply to' greys out with a cross beside it and lifts away; 'network with' drops into its place.",
        [{"at": 0.05, "event": "question writes on"}, {"at": 0.6, "event": "apply to -> network with"}],
        ["apply to", "network with"]),
]

B = [
    # Q1 — what is it
    beat("B00", "Q1 what is it", PROPOSED,
        "SponsorScout will be a Claude Code workflow that tells an international student, for each company, "
        "whether to apply, network, check by hand, or skip, with the record behind every answer.",
        "B00_Company",
        "One kraft crate (a company) drops onto the stage. A verdict slip slides out of it, and a small record "
        "receipt clips onto the slip.",
        [{"at": 0.15, "event": "crate drops in, floor shadow"}, {"at": 0.55, "event": "verdict slip slides out"},
         {"at": 0.80, "event": "record receipt clips on"}],
        ["company", "verdict", "record"], prop="context-crate"),
    beat("B01", "Q1 the artifact", PROPOSED,
        "Done, it will be a repository, in Python and Claude Code on public data: "
        "a recipe, a prototype, tests, an evaluation log, and a report you can trace row by row.",
        "B01_Repository",
        "The same crate's lid lifts; five parts rise out in a row: a recipe page, a dark code block, a test strip of "
        "checks, an evaluation binder, and a report sheet.",
        [{"at": 0.12, "event": "lid lifts"}, {"at": 0.30, "event": "recipe page and code block rise"},
         {"at": 0.62, "event": "tests, binder, report rise"}],
        ["recipe", "tests", "report"], prop="release-parcel"),
    # How it works (exists)
    beat("B02", "Q1 how it works", RAN,
        "Each company gets three checks. Has it sponsored data roles, in public H one B records? "
        "Has it raised money recently, in S E C Form D filings? "
        "Is an entry-level data job open on its board today?",
        "B02_ThreeGates",
        "The crate rides a conveyor through three gates in turn; each gate's lamp lights as the crate passes.",
        [{"at": 0.10, "event": "conveyor and three gates"}, {"at": 0.30, "event": "gate 1 lamp"},
         {"at": 0.55, "event": "gate 2 lamp"}, {"at": 0.85, "event": "gate 3 lamp"}],
        ["sponsor", "funding", "open today"], prop="conveyor"),
    # Q2 — what makes it different
    beat("B03", "Q2 alternative 1: engine scorer", RAN,
        "The engine's own scorer, which I had Claude Code run on October third, gives a sponsor with no open job "
        "a zero, and skips it. SponsorScout puts it on a networking list. So a student can stop applying where nothing is open, "
        "and keep the sponsors worth contacting.",
        "B03_Route",
        "At a branch junction the crate's third gate stays dark. A ghost path toward 'skip' draws in grey; the crate "
        "takes the other branch to 'network' instead.",
        [{"at": 0.15, "event": "junction, third lamp dark"}, {"at": 0.40, "event": "ghost path to skip draws in grey"},
         {"at": 0.70, "event": "crate takes the network branch"}],
        ["skip", "network"], prop="branch-junction"),
    beat("B04", "Q2 alternative 2: MyVisaJobs",
        f"constructed drawing · looked {MYVISAJOBS_CHECKED or '[date]'}",
        "I also looked at My Visa Jobs. It lists sponsors and their past job counts. "
        "It doesn't take a sponsor with nothing open and tell you to network there.",
        "B04_Compare",
        "Two comparison trays. Left tray: a ledger of past counts. Right tray: the same crate with a lamp marked "
        "'open today?'. No logos, no site UI.",
        [{"at": 0.15, "event": "left tray: ledger"}, {"at": 0.55, "event": "right tray: crate + lamp"}],
        ["past counts", "open today?"], prop="comparison-trays"),
    # Q3 — who opens it
    beat("B05", "Q3 reader + first 60 seconds", PROPOSED,
        "I'm targeting data analyst and data engineer roles, so my reader is a data hiring manager. "
        "In sixty seconds, they'll run one offline command, open the report, and trace a networking row to its source.",
        "B05_Trace",
        "A review desk. A report sheet slides onto it; an inspection lamp settles on one row, and a thin line draws "
        "from that row back to a source sheet beside the desk.",
        [{"at": 0.15, "event": "report onto desk"}, {"at": 0.50, "event": "lamp settles on one row"},
         {"at": 0.75, "event": "trace line to source sheet"}],
        ["60 seconds", "source row"], prop="review-desk"),
    # Exists today — real numbers (card)
    # The show-tell ShowTellCard is upstream-only (not in this checkout, 6a8380a), so the real
    # numbers are drawn: four trays, each with its real count from runs/run-2/network-targets.md.
    beat("B06", "evidence: run-2", "real counts · run-2 · 2026-10-03",
        "This already ran. On October third, the prototype fetched sixteen job boards and sorted "
        "one hundred twenty-three sponsors: two to apply, one to network, one hundred seven to check by hand, thirteen to skip. "
        "The job seeker is fictional.",
        "B06_RunTwo",
        "Four trays in a row, each with its REAL run-2 count as a number beside it (2 · 1 · 107 · 13); an "
        "inspection lamp settles on the NETWORK tray. No crates are drawn per company (no invented objects).",
        [{"at": 0.15, "event": "four trays land"}, {"at": 0.45, "event": "real counts appear on the spoken numbers"},
         {"at": 0.80, "event": "lamp settles on NETWORK 1"}],
        ["apply 2", "network 1", "check 107", "skip 13"], prop="comparison-trays"),
    # Q4 — what it proves
    beat("B07", "Q4 verification: the caught bug", "constructed drawing · ran 2026-10-03 & 10-12",
        "Run one got one wrong: Zoox landed in apply on part-time, contract student-worker postings. "
        "Claude flagged it. I chose the fix, and a test pins it. "
        "All twenty-five tests passed again on October twelfth.",
        "B07_Caught",
        "A crate rides into a checkpoint scanner; the scan line stops on it and it is pulled aside. A test strip "
        "with a check clips onto the scanner.",
        [{"at": 0.15, "event": "crate enters scanner"}, {"at": 0.40, "event": "scan stops, crate pulled aside"},
         {"at": 0.80, "event": "test strip with check clips on"}],
        ["run 1", "test"], prop="checkpoint-scanner"),
    beat("B08", "Q4 source grounding + gates", RAN,
        "What can a reviewer conclude? Source grounding: every number is labelled a record or my own input. "
        "Verification: an unconfirmed board never reaches the scorer, which would treat it as open.",
        "B08_Binder",
        "An evidence binder opens; two tabbed pages separate, one tagged 'record', one 'your input'. Beside it a gate "
        "stays shut in front of one unconfirmed crate.",
        [{"at": 0.15, "event": "binder opens"}, {"at": 0.35, "event": "two tags"},
         {"at": 0.75, "event": "gate holds the unconfirmed crate"}],
        ["record", "your input"], prop="evidence-binder"),
    beat("B09", "Q4 agent loop + evaluation", "constructed drawing · gates ran · eval proposed",
        "Agent loops: Claude Code stops at the human gates for my sign-off. "
        "Evaluation is still to come: a hand-checked set of verdicts, with the wrong ones logged.",
        "B09_SignOff",
        "A work parcel moves along a short track and stops at a gate; an approval stamp comes down on it. Beside it "
        "an empty binder (ghost outline) appears: the evaluation log, not built yet.",
        [{"at": 0.15, "event": "parcel stops at gate"}, {"at": 0.40, "event": "stamp comes down"},
         {"at": 0.75, "event": "ghost binder outline appears"}],
        ["sign-off", "eval log"], prop="approval-stamp"),
    # Q5 — out / first
    beat("B10", "Q5 what it will not do", PROPOSED,
        "It will never apply, email, or contact anyone. The person decides. "
        "And it won't score résumé fit, so no real résumé goes in.",
        "B10_Never",
        "A permission gate with its barrier down; an outgoing envelope slides up to it and stops. A list slip passes "
        "to the side instead.",
        [{"at": 0.15, "event": "gate, barrier down"}, {"at": 0.40, "event": "envelope stops"},
         {"at": 0.70, "event": "list slip passes aside"}],
        ["never sends", "list"], prop="permission-gate"),
    beat("B11", "Q5 first piece + how you'd know", "16/123 real · resolver proposed",
        "First, I'll build a board resolver. Today sixteen of the hundred twenty-three companies have a confirmed board. "
        "You'll know it ran when that number rises, each new board saved with its raw response and a test.",
        "B11_Coverage",
        "A big hero number '16 / 123' lands. Below it a row of slots: sixteen filled, the rest empty outlines. "
        "Nothing fills during the beat (no invented progress).",
        [{"at": 0.15, "event": "16 / 123 lands"}, {"at": 0.45, "event": "slot row draws, 16 filled"}],
        ["boards"], prop="budget-slots"),
    # Q6 — risk + unknown
    beat("B12", "Q6 risk", PROPOSED,
        "What could sink it: many of the other hundred and seven may have no public board, and I don't know how many. "
        "I'll use only public Greenhouse, Lever and Ashby boards, never scrape, and report coverage even if it's low.",
        "B12_Locked",
        "A locked vault (a closed job system) beside three open boards; a crate tries the vault and stays outside, "
        "then joins a 'check by hand' tray.",
        [{"at": 0.15, "event": "vault + three open boards"}, {"at": 0.45, "event": "crate stopped at vault"},
         {"at": 0.75, "event": "crate to the hand-check tray"}],
        ["no public API", "check by hand"], prop="secure-vault"),
    beat("B13", "Q6 what I don't know yet", PROPOSED,
        "I also don't know if recent funding predicts hiring. I'll find out by re-checking the networking targets' "
        "boards after fourteen days, and logging whether a posting appeared.",
        "B13_Experiment",
        "An experiment bench; a sample crate slides in under a lamp; a fourteen-day tick row draws beside it, "
        "ending in an empty result box.",
        [{"at": 0.15, "event": "bench"}, {"at": 0.40, "event": "sample slides in"},
         {"at": 0.75, "event": "14-day row + empty result box"}],
        ["14 days", "result?"], prop="experiment-bench"),
    # Q7 — why this project
    beat("B14", "Q7 why this project", "constructed drawing",
        # Akshit's reason, in Akshit's words (2026-10-14): "I believe this is something I am also going through
        # job applications, and I needed to understand what's the best and efficient strategy to get a job rather
        # than just doing 100-200 applications every day." Tightened by Claude at Akshit's request; meaning unchanged.
        "I picked it because I'm job hunting too, and I wanted a smarter strategy than a hundred-plus applications a day. "
        "It's a mix. What I can show is judgment, not code: Claude Code wrote most of the prototype; "
        "I set its rules, like requiring recent funding, and signed its human gates. "
        "New for me: evaluation, and resolving boards at scale.",
        "B14_Stack",
        "A skill stack: lower blocks solid kraft (have), upper blocks ghost outlines (new) that settle on top.",
        [{"at": 0.15, "event": "solid lower blocks"}, {"at": 0.60, "event": "ghost upper blocks settle"}],
        ["have", "new"], prop="skill-stack"),
]

OUTRO = {
    "beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW", "answers": "outro",
    "narration_text": f"{TITLE}. A pitch by {AUTHOR}.",
    "estimated_duration_s": 5.0, "voice": VOICE, "engine": "kokoro",
    "shot": {"type": "REMOTION", "source": "own",
             "show": [{"at": 0.0, "event": "title restates; author credit; no instructor handle"}],
             # PitchOutro (runtime/remotion/src/illustrations/pitch.tsx), not ClaudeTitleOutro:
             # that component hardcodes @NikBearBrown and the assignment forbids the instructor's credit line.
             "remotion": {"pattern": "PitchOutro",
                          # handle = the credit shown on screen (author); bookend_check matches it to channel_title
                          "props": {"title": TITLE, "handle": AUTHOR, "author": AUTHOR, "course": "INFO 7375 · Final Project Pitch"}}},
    "kind": "outro_voice", "tail_silence_s": 1.0,
}

SPARSE_REASON = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, the voice "
                 "carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and "
                 "contrast still apply.")
for b in B:
    if b["lane"] == "manim":
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}

# The visual plan AS BUILT (scenes.py, revision of 2026-10-14 after Akshit's notes): every scene builds in
# (staggered rise), times each reveal to its spoken word (mp3/words.json), and fades to the stage at its end.
# Nothing is drawn below y = -2.5 (the burned-in caption band).
AS_BUILT = {
    "BOPEN": ("SponsorScout writes on beside its mark (a crate under a scout's lens); a terracotta rule; the byline; "
              "the legend for every corner tag: a solid dot = ran, a dashed ring = proposed.",
              ["SponsorScout", "a final project pitch by Akshit Verma", "ran", "proposed"]),
    "BIDEA": ("'Which companies should I apply to?' writes on a card; 'apply to?' greys out with a cross beside it (a strike line THROUGH the words failed Gate B) and lifts away; "
              "'network with?' drops into its place on the spoken words.", ["apply to?", "network with?"]),
    "B00": ("A company (crate on a dark plinth) -> the SponsorScout block -> a fan of four arrows to four trays, "
            "each verdict landing on its word: apply, network, check by hand, skip. A small crate drops into "
            "'network' and its record slip appears.", ["a company", "SponsorScout", "apply", "network", "check by hand", "skip", "record"]),
    "B01": ("An open box on a plinth = the repository; 'Python · Claude Code · public data' under it; five parts "
            "fly out of the box in a row, each on its word: recipe, prototype, tests, eval log, report; a terracotta "
            "ring steps down the report's rows.", ["repository", "recipe", "prototype", "tests", "eval log", "report"]),
    "B02": ("A moving conveyor through three depth-correct gates (the crate passes BETWEEN back and front posts); "
            "at each spoken question the crate rides to the gate, the lamp pulses terracotta and its label lands "
            "below the post.", ["sponsored? (H-1B records)", "funded? (Form D)", "open today? (job board)"]),
    "B03": ("A sponsor crate with a dark 'open today?' lamp. Top path, grey and dashed: engine scorer -> '0' -> skip. "
            "Bottom path, solid: SponsorScout -> network list; the crate travels into it; a check.",
            ["no open job", "engine scorer", "0", "skip", "SponsorScout", "network list"]),
    "B04": ("A MyVisaJobs panel whose rows fill with past-count bars; on the right a sponsor crate with nothing open, "
            "a dashed route to a network tray, crossed out.", ["MyVisaJobs", "sponsors · past job counts", "network", "no network step"]),
    "B05": ("A briefcase (no person drawn) for the reader: data analyst, data engineer, hiring manager. A 60 s clock "
            "whose hand advances with three steps: one command (terminal) -> report (a row ringed) -> source record.",
            ["data analyst", "data engineer", "hiring manager", "60 s", "one command", "report", "source record"]),
    "B06": ("Four trays; the REAL run-2 counts appear on their spoken numbers (2 · 1 · 107 · 13); a terracotta ring on "
            "network; '16 boards fetched', '123 sponsors sorted', 'job seeker: fictional'.",
            ["16 boards fetched", "123 sponsors sorted", "apply", "network", "check by hand", "skip"]),
    "B07": ("The Zoox crate lands in 'apply'; 'part-time contract postings'; a terracotta scan line and a flag "
            "('flagged'); the crate moves to 'excluded'; a test pill with a check; '25 / 25 tests pass · Oct 12'.",
            ["Zoox · run 1", "apply", "flagged", "excluded", "test", "25 / 25 tests pass · Oct 12"]),
    "B08": ("A report panel whose rows carry a solid dot (record) or a hollow ring (my input); then a dark wall: an "
            "unconfirmed crate is stopped (x) before the scorer, which 'would read it as open'.",
            ["every number, labelled", "record", "my input", "unconfirmed", "scorer", "would read it as open"]),
    "B09": ("A loop (Claude Code runs the recipe) with two dark human-gate squares; a terracotta token travels to the "
            "first and stops; a check = my sign-off; a dashed, empty 'eval log (proposed)'.",
            ["Claude Code runs the recipe", "human gates", "my sign-off", "eval log", "(proposed)"]),
    "B10": ("Three outgoing items (an application, an email, a message) slide to a dark wall and are crossed out; "
            "a list goes to 'you decide'; a résumé crossed out ('no résumé').", ["apply", "email", "contact", "you decide", "no résumé"]),
    "B11": ("The board resolver block; the REAL '16 / 123'; a bar with 16/123 filled in dark that never grows (no "
            "invented progress); a dashed up-arrow for 'that number rises'.",
            ["board resolver", "16 / 123", "boards confirmed today", "+ raw response + a test, per board"]),
    "B12": ("A dark vault (no public board?) blocks a crate (x); the crate goes to 'check by hand'; three public boards "
            "appear on their names (Greenhouse, Lever, Ashby); 'public boards only · no scraping'; 'coverage, reported "
            "as a number'.", ["no public board?", "check by hand", "Greenhouse", "Lever", "Ashby"]),
    "B13": ("A crate on a plinth ('recent funding') -> '→ hiring?'; a 14-day calendar fills day by day; a dashed, empty "
            "result box '?' ('posting appeared?').", ["recent funding", "→ hiring?", "14 days", "posting appeared?"]),
    "B14": ("A pile of eight application sheets ('100+ applications a day') gives way to one short list; a stack built "
            "on the spoken words: grey layer 'prototype code: Claude Code', kraft layers 'the rules: mine' and 'gate "
            "sign-offs: mine', dashed layers 'new: evaluation', 'new: resolving boards'.",
            ["100+ applications a day", "a short list", "prototype code: Claude Code", "the rules: mine",
             "gate sign-offs: mine", "new: evaluation", "new: resolving boards"]),
}
for b in OPEN + B:
    if b["beat_id"] in AS_BUILT:
        desc, labels = AS_BUILT[b["beat_id"]]
        b["shot"]["visual_intent"] = desc
        b["shot"]["motion_claim"] = desc
        b["shot"]["labels"] = labels
        b["shot"].pop("prop", None)

for b in OPEN:   # the two title cards are sparse by design (a name; a question), like the bookend they replace
    b["qc"] = {"sparse_by_design": True, "sparse_reason": "Title card: one name or one question, centred on the stage."}
BEATS = OPEN + B + [OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "INFO 7375 · FINAL PROJECT PITCH",
    "skill": "show-tell", "style_preset": "show-tell", "kind": "pitch",
    "author": AUTHOR, "channel": AUTHOR, "channel_title": AUTHOR,
    "persona": f"{AUTHOR}'s script, read by a synthetic voice (Kokoro {VOICE}); 'a pitch BY {AUTHOR}', never 'I am'; the voice is disclosed in README.md and SOURCES.md (Akshit's choice, 2026-10-14)",
    "presenter": f"synthetic voice (Kokoro {VOICE}), narrating {AUTHOR}'s script — not the instructor's persona",
    "in_for_bear": False,
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown",
    "fps": 24, "aspect_ratio": "16:9", "width": 1920, "height": 1080,
    "captions": True,
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Pitch film, not an explainer: opens on its own title beat (BOPEN) and question beat (BIDEA), both Manim; "
                              "no verdict card (show-tell drops it); no Your Turn, because a pitch has no viewer task "
                              "and a Claude.ai-styled composer would look like a Claude exchange that never happened. "
                              "No terms card, to stay inside 2-4 minutes. The outro stays, credited to the author."),
    "audience": "a hiring manager for Data Analyst / Data Engineer roles; INFO 7375 graders",
    "source_doc": "PROJECT-BRIEF.md; Assignment 1 run outputs (the-reallocation-engine @ a1d321f, runs/run-1, "
                  "runs/run-2, runs/engine-baseline); MyVisaJobs homepage viewed 2026-10-12",
    "honesty_rule": "Past tense only for things that exist and can be shown; every drawn beat tagged "
                    "'constructed drawing' plus RAN <date> or PROPOSED on screen.",
    "playlist": "INFO 7375", "cut": "review",
    "tags": ["INFO 7375", "final project pitch", "Reallocation Engine", "H-1B", "data analyst", "data engineer"]},
    "beats": BEATS}

# Carry measured audio forward: a beat whose narration is unchanged keeps its voiced take, duration and
# word-clock cues (the show-tell skill warns that dropping audio_file makes `art run` refuse).
CARRY = ("audio_file", "actual_duration_s", "render_duration_s", "build")
old_path = HERE / "beat_sheet.json"
if old_path.exists():
    old = {b["beat_id"]: b for b in json.loads(old_path.read_text(encoding="utf-8")).get("beats", [])}
    for b in BEATS:
        o = old.get(b["beat_id"])
        if o and o.get("narration_text") == b["narration_text"]:
            for k in CARRY:
                if k in o:
                    b[k] = o[k]
            cues = (((o.get("shot") or {}).get("remotion") or {}).get("props") or {}).get("cues")
            if cues and b["shot"].get("remotion"):
                b["shot"]["remotion"]["props"]["cues"] = cues
            if b.get("actual_duration_s") and b["shot"].get("remotion"):
                b["shot"]["remotion"]["props"]["durationSeconds"] = b["actual_duration_s"]

(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

total = sum(b["estimated_duration_s"] for b in BEATS)
words = sum(len(b["narration_text"].split()) for b in BEATS)
print(f"{len(BEATS)} beats · {words} words · est {total:.0f}s ({total/60:.1f} min) at {WPS} words/s")
for b in BEATS:
    print(f"  {b['beat_id']:6} {b['estimated_duration_s']:5.1f}s  {b.get('answers','')}")
blocked = [f"{b['beat_id']} (needs Akshit's own words)" for b in BEATS if TODO in b["narration_text"]]
if not MYVISAJOBS_CHECKED:
    blocked.append("B04 (Akshit has not yet looked at MyVisaJobs; set MYVISAJOBS_CHECKED and reword to what Akshit saw)")
if blocked:
    print("\nNOT READY TO VOICE:\n  " + "\n  ".join(blocked), file=sys.stderr)
    sys.exit(2)
if not 120 <= total <= 240:
    print(f"\nWARNING: estimate {total:.0f}s is outside 2-4 min.", file=sys.stderr)
