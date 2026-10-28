#!/usr/bin/env python3
"""make_sheet.py — writes beat_sheet.json for the Cite & Seek pitch film (show-tell format).

Sources: ../PROJECT-BRIEF.md and ../REPO-FACTS.md. Decisions: FILM-PLAN.md.
Script revision approved by Meena on 2026-10-11: course intro, impact hypothesis, the pipeline as it
exists today, scope, "built so far / will build" (no dates anywhere), a one-sentence why.
Honesty rule: past tense only for what exists and can be shown; everything else is "will".
Each beat carries `claim_status` (exists | will | mixed | none) so the honesty check is mechanical.

ASSIGNMENT.md: "Mock-ups and sketches are labelled constructed on screen." Every drawn beat therefore
carries `shot.screen_tag`, which its scene must draw on screen: "constructed", or
"constructed · planned" for beats about future work. It is set per beat, never inferred.
BOUT is a title card and carries none.

Narration spellings for Kokoro: "seventy-three seventy-five" (INFO 7375), "Mini-L-M" (MiniLM),
"four point five" (4.5). The screen shows the normal forms.

Citation tags and chunk ranges drawn on screen are real chunk boundaries from the baseline's own
chunker (src/cite_and_seek/corpus.py, run read-only 2026-10-11): app/api/orders.py 52-84,
app/api/cart.py 27-46, app/api/payments.py 1-24. No query is claimed to have produced them.

Golden-set counts (53 total, 45 answerable, 8 unanswerable) were verified by Meena on 2026-10-11.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "cite-and-seek-pitch"
TITLE = "Cite & Seek"
VOICE = "am_michael"  # chosen by Meena (FILM-PLAN.md)
HANDLE = "@meenuviji"
TAG = "constructed"
TAG_PLANNED = "constructed · planned"
SPARSE = {"sparse_by_design": True,
          "sparse_reason": "Show-tell: one drawn diagram with short labels. Only underfill and clustering waived."}


def est(text):
    # Rough speaking time at about 2.5 words per second (measured on this film's Kokoro narration).
    return round(len(text.split()) / 2.5, 1)


def drawn(bid, cls, narration, image, labels, claim, tag, question):
    assert tag in (TAG, TAG_PLANNED), f"{bid}: every drawn beat shows a constructed tag"
    return {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
            "assignment_question": question,
            "narration_text": narration, "estimated_duration_s": est(narration),
            "voice": VOICE, "engine": "kokoro", "claim_status": claim, "qc": SPARSE,
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image,
                     "motion_claim": image, "labels": labels, "screen_tag": tag, "show": [],
                     "manim": {"class": cls}}}


def card(bid, act, narration, pattern, props, claim, question, **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": "SHOW",
         "assignment_question": question,
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": VOICE, "engine": "kokoro", "claim_status": claim, "qc": SPARSE,
         "shot": {"type": "REMOTION", "source": "own", "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


CITE = "[app/api/orders.py:52-84]"

BEATS = [
    # ── Intro ──────────────────────────────────────────────────────────────────
    # Our own drawn title card (segment headings revision, 2026-10-11), replacing the hesitant writer:
    # "Introduction" large, the course name typed as it is spoken, then "Final Project". A title card,
    # not a sketch, so no "constructed" tag (same reasoning as BOUT). Narration unchanged.
    {"beat_id": "BIDEA", "act": "intro", "lane": "manim", "proof_gate": "SHOW", "assignment_question": "Q1",
     "narration_text": "Hi, I'm Meena. This is my final project for INFO seventy-three seventy-five, "
                       "Prompt Engineering for Generative AI. It's called Cite and Seek.",
     "estimated_duration_s": 9.6, "voice": VOICE, "engine": "kokoro", "claim_status": "none", "qc": SPARSE,
     "lead_silence_s": 0.8,
     "shot": {"type": "GRAPHIC", "source": "own",
              "visual_intent": "'Introduction' large at top left; 'INFO 7375: Prompt Engineering for Generative AI' "
                               "types out as the course name is spoken; then 'Final Project' appears.",
              "labels": ["Introduction", "INFO 7375: Prompt Engineering for Generative AI", "Final Project"],
              "manim": {"class": "BIDEA_Intro"}}},
    drawn("B00", "B00_WhatItIs",
          "A tool that answers questions about a codebase with citations to the exact files, "
          "and refuses when the code doesn't say.",
          f"A question card enters a dark box labelled 'Cite & Seek'. An answer card comes out carrying the "
          f"citation tag {CITE}; a second path ends in a slip labelled 'ABSTAIN'.",
          ["question", "Cite & Seek", CITE, "ABSTAIN"], "exists", TAG, "Q1"),

    # ── Impact (hypothesis, untested) ─────────────────────────────────────────
    drawn("B01", "B01_Hypothesis",
          "My hypothesis is that on a real team, this would help a new engineer understand unfamiliar code "
          "without pulling a senior engineer away from their work,",
          "Two laptops. 'new engineer' sends a question to the Cite & Seek box and gets an answer back; "
          "'senior engineer' keeps a focus light on, undisturbed. Label 'hypothesis'. No drawn people.",
          ["hypothesis", "new engineer", "senior engineer", "Cite & Seek"], "none", TAG, "Q2"),
    drawn("B02", "B02_Checkable",
          "and every answer can be checked. I haven't tested that with real engineers yet.",
          "A magnifier beside a source page labelled app/api/orders.py; lines 52-84 are highlighted. "
          "Label 'untested'.",
          ["app/api/orders.py", "lines 52-84", "untested"], "mixed", TAG, "Q2"),

    # ── Terms ──────────────────────────────────────────────────────────────────
    card("BDEFS", "terms",
         "Three terms. Retrieval: finding the code that matters. A citation: the file and lines behind a claim. "
         "Abstaining: refusing when the code doesn't say.",
         "ClaudeDefinitions",
         {"title": "What It Is · Terms",  # the card's top-left title carries the segment heading
          "terms": [{"term": "Retrieval", "meaning": "finding the code that matters"},
                    {"term": "Citation", "meaning": "the file and lines behind a claim"},
                    {"term": "Abstain", "meaning": "refuse when the code is silent"}],
          "folderLabel": HANDLE},  # durationSeconds is set from the measured audio
         "none", "terms"),

    # ── The data ───────────────────────────────────────────────────────────────
    drawn("B03", "B03_Data",
          "It runs on a real open-source e-commerce codebase from GitHub, standing in for a company's code, "
          "with fifty-three test questions I wrote and checked against the code, plus ten synthetic incident reports.",
          "A repo crate with three file pages, labelled 'e-commerce API' and 'GitHub · MIT'; a binder labelled "
          "'53 questions'; a folder labelled '10 synthetic incidents'.",
          ["e-commerce API", "GitHub · MIT", "53 questions", "10 synthetic incidents"], "exists", TAG, "Q5"),

    # ── The pipeline as it exists today (REPO-FACTS.md, v0.1) ─────────────────
    drawn("B04", "B04_Retrieve",
          "Here's the pipeline that exists today. A question is embedded with Mini-L-M, a small local model, "
          "and compared against every chunk of the codebase, each at most two hundred tokens.",
          "Labelled stages with arrows: question -> MiniLM embed -> search all chunks. Below the search stage, "
          "three chunk strips labelled orders.py 52-84, cart.py 27-46, payments.py 1-24, and '≤ 200 tokens'.",
          ["question", "MiniLM embed", "search all chunks", "orders.py 52-84", "cart.py 27-46",
           "payments.py 1-24", "≤ 200 tokens"], "exists", TAG, "Q5"),
    drawn("B05", "B05_Answer",
          "The top five chunks go to Claude Haiku four point five, with one rule: use only these chunks, "
          "and cite every claim by file and lines.",
          f"Stages with arrows: search -> top 5 (five strips) -> Claude Haiku 4.5 -> answer. The answer carries "
          f"{CITE}; a rule page reads 'only these chunks · cite every claim'.",
          ["search", "top 5", "Claude Haiku 4.5", "answer", CITE, "only these chunks · cite every claim"],
          "exists", TAG, "Q5"),
    drawn("B06", "B06_Abstain",
          "If the chunks don't contain the answer, it replies with a single ABSTAIN line instead of a partial answer.",
          "From the Claude Haiku 4.5 stage, one arrow reaches a half-written page that is dimmed and labelled "
          "'no partial answers'; the other reaches a slip labelled 'ABSTAIN: what is missing'.",
          ["Claude Haiku 4.5", "no partial answers", "ABSTAIN: what is missing"], "exists", TAG, "Q5"),

    # ── What it proves ─────────────────────────────────────────────────────────
    drawn("B07", "B07_Skills",
          "So it shows four AI engineering skills: retrieval, citation, abstention, and evaluation. "
          "The first three exist in the baseline. Evaluation is what I will build next. "
          "In course terms: source grounding, prompt contracts and evaluation.",
          "Four labelled blocks: Retrieval, Citation, Abstention (solid, under 'built') and Evaluation "
          "(outlined, under 'will build').",
          ["Retrieval", "Citation", "Abstention", "Evaluation", "built", "will build"], "mixed", TAG_PLANNED, "Q4"),
    # P5 (approved 2026-10-12): what a reviewer could fairly conclude.
    drawn("B07B", "B07B_Conclude",
          "A reviewer could fairly conclude I can design the test before the system.",
          "The locked '53 questions' binder sits before an empty 'system' outline, with a check mark beside "
          "'test before the system'.",
          ["53 questions", "system", "test before the system"], "exists", TAG, "Q4"),

    # ── Why it is different, and the alternative ──────────────────────────────
    drawn("B08", "B08_Order",
          "What sets it apart is the order: I wrote and checked the test questions before writing any retrieval "
          "code, and eight of them have no answer in the code, so refusing will be tested too.",
          "A locked binder '53 questions' sits before an empty outline 'retrieval code' with an arrow 'first'; "
          "eight pages slide out in a row labelled '8 unanswerable'.",
          ["53 questions", "first", "retrieval code", "8 unanswerable"], "mixed", TAG, "Q2"),
    drawn("B09", "B09_Alternative",
          "The alternative today is reading the code by hand. That's how I checked every answer in my test set. "
          "It works, but it's slow, and nothing tells you when you've missed the right file.",
          "A magnifier crawls over five file pages labelled orders.py, cart.py, auth.py, payments.py, models.py; "
          "it skips auth.py, which stays dim, labelled 'missed file?'. Label 'by hand'.",
          ["by hand", "orders.py", "cart.py", "auth.py", "payments.py", "models.py", "missed file?"],
          "exists", TAG, "Q2"),
    # P3 (approved 2026-10-12): what Cite & Seek does that reading by hand does not.
    drawn("B09B", "B09B_Instead",
          "Cite and Seek points to the exact lines, and its tests will measure how often retrieval misses "
          "the right file.",
          f"A question card leads to the source page app/api/orders.py with lines 52-84 marked by the citation tag "
          f"{CITE}; beside it, an outlined gauge labelled 'misses: will measure'.",
          ["app/api/orders.py", CITE, "misses: will measure"], "mixed", TAG_PLANNED, "Q2"),

    # ── Who opens it ───────────────────────────────────────────────────────────
    drawn("B10", "B10_Reader",
          "It's for someone hiring an entry-level AI engineer. Once it's written up, in their first minute, they will "
          "open the README, compare the baseline with each experiment, and check any cited line themselves.",
          "A README page with an empty table; rows labelled 'baseline' and 'experiment 1' (no numbers). "
          "A magnifier rests on a citation dot. Label 'entry-level AI engineer'.",
          ["README", "baseline", "experiment 1", "entry-level AI engineer"], "will", TAG_PLANNED, "Q3"),

    # ── Scope, and what comes first ───────────────────────────────────────────
    drawn("B11", "B11_Scope",
          "In scope: one codebase of thirty-seven files, small on purpose, not production scale. Out of scope: "
          "agents, fine-tuning, and orchestration frameworks, so every step stays visible.",
          "A crate of pages labelled 'in scope' and '37 files'; three labelled blocks (agents, fine-tuning, "
          "frameworks) roll toward a gate labelled 'out of scope' and are turned back.",
          ["in scope", "37 files", "out of scope", "agents", "fine-tuning", "frameworks"], "exists", TAG, "Q5"),
    drawn("B12", "B12_First",
          "The first thing I will build is the scoring harness: retrieval hits, and an LLM judge I will check "
          "against my own labels. You'll know it ran when its results rebuild with one command.",
          "Stages with arrows: terminal 'one command' -> 'harness' -> 'results'. Below, a 'judge' row of marks "
          "beside a 'my labels' row of dots.",
          ["one command", "harness", "results", "judge", "my labels"], "will", TAG_PLANNED, "Q5"),

    # ── Risk ───────────────────────────────────────────────────────────────────
    drawn("B13", "B13_Risk",
          "The risk is sample size. With an eighty-twenty split, only about six unanswerable questions will be "
          "left for tuning, so one refusal will move the rate by about seventeen points. I will report raw counts "
          "and confidence intervals.",
          "Eight pages split into groups labelled 'about 6' and 'held out'; a gauge needle jumps ('one refusal'), "
          "then gets a shaded band labelled 'raw counts'.",
          ["about 6", "held out", "one refusal", "raw counts"], "will", TAG_PLANNED, "Q6"),

    # ── Built so far / will build (no dates) ──────────────────────────────────
    drawn("B14", "B14_Built",
          "Built so far: the fifty-three question test set, and a first baseline: retrieval I have run, "
          "and a prompt that requires every claim to be cited or the answer to be ABSTAIN.",
          "Column 'Built so far': solid markers beside '53-question test set', 'retrieval (run)' and "
          "'prompt: cite or ABSTAIN'. The 'Will build' column is not shown yet.",
          ["Built so far", "53-question test set", "retrieval (run)", "prompt: cite or ABSTAIN"],
          "exists", TAG, "exists vs will"),
    drawn("B15", "B15_WillBuild",
          "Next, I will build the scoring harness, run the experiments, and write it up in a public GitHub repository.",
          "The 'Built so far' column stays; a 'Will build' column appears with outlined markers beside "
          "'scoring harness', 'experiments', 'write-up' and 'public GitHub repository'.",
          ["Built so far", "Will build", "scoring harness", "experiments", "write-up", "public GitHub repository"],
          "will", TAG_PLANNED, "exists vs will"),

    # ── Why this project ───────────────────────────────────────────────────────
    drawn("B16", "B16_Why",
          "Evaluating models on held-out data isn't new to me; retrieval, embeddings, and using one model to judge "
          "another are. This project is how I learn them in a way someone else can check.",
          "A 'have' tray with one block labelled 'evaluation'; a 'new' tray with three blocks labelled "
          "'retrieval', 'embeddings', 'LLM judge'.",
          ["have", "evaluation", "new", "retrieval", "embeddings", "LLM judge"], "mixed", TAG, "Q7"),

    # ── Closing bookends ───────────────────────────────────────────────────────
    # Your Turn shows only an invitation to the viewer: no output lines, no running text.
    # The composer is a recreated Claude.ai interface, a mock-up, so it is labelled "constructed" on screen
    # twice: in the small grey topic eyebrow, and in the large ink segment title.
    # bookend_check needs "YOUR TURN" in the topic; it stays.
    card("BHTF", "your turn",
         "Your turn. Before you build your next AI tool, write five questions it should answer and two it should refuse.",
         "ClaudeComposerAsk",
         {"greeting": "Your turn.", "topic": "CITE & SEEK · YOUR TURN · CONSTRUCTED",
          "segment": "Test Before You Build · constructed",
          "command": "Write five questions my tool should answer and two it should refuse, before I build it.",
          "runningText": "", "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
          "largeText": True},
         "none", "your turn"),
    # Our own drawn outro (FILM-PLAN.md). shot.remotion.props are read only by bookend_check.py and must
    # match exactly what BOUT_Close draws: the title and the handle, nothing else. It is a title card,
    # not a sketch, so it carries no "constructed" screen tag (Meena, 2026-10-11).
    {"beat_id": "BOUT", "act": "bookend", "lane": "manim", "proof_gate": "SHOW", "assignment_question": "outro",
     "narration_text": "Cite and Seek. I'm Meena P., at meenuviji.",
     "estimated_duration_s": est("Cite and Seek. I'm Meena P., at meenuviji.") + 1.0,
     "voice": VOICE, "engine": "kokoro", "claim_status": "none", "qc": SPARSE, "tail_silence_s": 1.0,
     "shot": {"type": "GRAPHIC", "source": "own",
              "visual_intent": "The title 'Cite & Seek' settles centre stage; '@meenuviji' appears beneath it.",
              "manim": {"class": "BOUT_Close"},
              "remotion": {"props": {"title": TITLE, "handle": HANDLE, "subline": ""}}}},
]

# ── Segment headings (Meena, 2026-10-11) ──────────────────────────────────────
# Each drawn beat shows its segment as a heading at the top left for the whole beat, and an optional
# subheading beneath it. Subheadings use only words from the narration, REPO-FACTS.md, or Meena's own
# wording (B10). Beats with no segment entry fit none of Meena's segments and show no heading; they are
# listed for her decision instead of a new segment being invented.
SEGMENTS = {
    "BIDEA": ("Introduction", None),                       # drawn by BIDEA_Intro itself
    "B00": ("What It Is", "Answers with citations, or refuses"),
    "BDEFS": ("What It Is", None),                         # shown through the card's own title
    "B03": ("What It Is", "A real open-source e-commerce codebase"),
    "B01": ("The Hypothesis", "Help a new engineer understand unfamiliar code"),
    "B02": ("The Hypothesis", "Haven't tested with real engineers yet"),
    "B10": ("Who It's For", "Target reader: hiring manager for an entry-level AI Engineer role"),
    "B04": ("How It Works", "Retrieval"),
    "B05": ("How It Works", "Citation"),
    "B06": ("How It Works", "Abstention"),
    "B07": ("What It Proves", "In course terms: source grounding, prompt contracts, evaluation"),
    "B07B": ("What It Proves", "What a reviewer could fairly conclude"),
    "B08": ("Why It's Different", "Test questions before retrieval code"),
    "B09": ("Why It's Different", "The alternative: reading the code by hand"),
    "B09B": ("Why It's Different", "Cite & Seek points to the exact lines"),
    "B11": ("Scope: In, Out, First", "In scope and out of scope"),
    "B12": ("Scope: In, Out, First", "First: the scoring harness"),
    "B13": ("What Could Sink It", "Sample size"),
    "B16": ("Why This Project", None),
    "B14": ("Built So Far / Will Build", None),
    "B15": ("Built So Far / Will Build", None),
}
UNSEGMENTED = ("BHTF", "BOUT")   # Meena, 2026-10-11: Your Turn and the outro stay without headings

# Beats in segment order. B07 (What It Proves) and B08-B09 (Why It's Different) follow How It Works in
# their original order (Meena, 2026-10-11); BHTF and BOUT close the film.
ORDER = ["BIDEA", "B00", "BDEFS", "B03", "B01", "B02", "B10", "B04", "B05", "B06", "B07", "B07B", "B08", "B09", "B09B",
         "B11", "B12", "B13", "B16", "B14", "B15", "BHTF", "BOUT"]

_by_id = {b["beat_id"]: b for b in BEATS}
assert sorted(ORDER) == sorted(_by_id), "ORDER must list every beat exactly once"
BEATS = [_by_id[i] for i in ORDER]
for _b in BEATS:
    seg = SEGMENTS.get(_b["beat_id"])
    _b["segment"] = seg[0] if seg else None
    if seg and _b["lane"] == "manim" and _b["beat_id"] != "BIDEA":
        _b["shot"]["heading"] = seg[0]
        if seg[1]:
            _b["shot"]["subheading"] = seg[1]

SHEET = {
    "metadata": {
        "slug": SLUG, "title": TITLE,
        "topic": "Final project pitch: an evaluation-first, citation-grounded code question-answering tool",
        "purpose": "INFO 7375 final project pitch film (2-4 min). Honest about what exists and what will.",
        "skill": "show-tell", "style_preset": "show-tell",
        "persona": "Meena P.", "engine": "kokoro", "voice_kokoro": VOICE,
        "channel_title": HANDLE, "clock": "narration",
        "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160, "caption_policy": "none",
        "bookend_exempt": ["cold-open", "bvdt"],
        "bookend_exempt_reason": "Show-tell opens with the hesitant writer and has no verdict card. "
                                 "Your Turn and an outro are kept; the outro is our own drawn beat (FILM-PLAN.md).",
        "source_doc": "../PROJECT-BRIEF.md; ../REPO-FACTS.md",
    },
    "beats": BEATS,
}

MEASURED = ("audio_file", "actual_duration_s")


def carry_forward(sheet, old_path):
    """Keep measured audio for every beat whose narration is unchanged, so only changed beats are re-voiced.

    Matching is by narration text, not beat id, because beats were renumbered. A beat that moved to a new
    id gets its audio copied to mp3/beat-<new id>.mp3 first, so re-voicing another beat under the old id
    can never overwrite it. Changed beats get no carried fields and must be voiced.
    Returns (kept, changed_ids).
    """
    if not old_path.exists():
        return 0, [b["beat_id"] for b in sheet["beats"]]
    old_by_text = {}
    for b in json.loads(old_path.read_text()).get("beats", []):
        if b.get("actual_duration_s") and b.get("audio_file"):
            old_by_text.setdefault(b["narration_text"], b)
    copies, kept, changed = [], 0, []
    for b in sheet["beats"]:
        prev = old_by_text.get(b["narration_text"])
        if not prev:
            changed.append(b["beat_id"])
            continue
        audio = prev["audio_file"]
        if prev["beat_id"] != b["beat_id"]:
            target = f"mp3/beat-{b['beat_id']}.mp3"
            copies.append((HERE / audio, HERE / target))
            audio = target
        b["audio_file"] = audio
        b["actual_duration_s"] = prev["actual_duration_s"]
        if b["shot"].get("remotion", {}).get("pattern") == "ClaudeDefinitions":
            b["shot"]["remotion"]["props"]["durationSeconds"] = prev["actual_duration_s"]
        kept += 1
    # Read every source before writing any target.
    data = [(src.read_bytes(), dst) for src, dst in copies]
    for blob, dst in data:
        dst.write_bytes(blob)
    return kept, changed


if __name__ == "__main__":
    out = HERE / "beat_sheet.json"
    kept, changed = carry_forward(SHEET, out)
    out.write_text(json.dumps(SHEET, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out}: {len(BEATS)} beats ({kept} kept their measured audio)")
    print("needs voicing:", " ".join(changed) if changed else "none")
