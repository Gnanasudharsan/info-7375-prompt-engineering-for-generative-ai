#!/usr/bin/env python3
"""make_sheet.py: writes beat_sheet.json for the ProductLens AI pitch film (v2, show-tell style).

Narration is read verbatim from SCRIPT-v2.md (approved by Aditya on 2026-10-25), so the spoken words can't drift from the
approved script. Authorship (see SOURCES.md): Aditya wrote the ProductLens script (refined with ChatGPT); Claude Code merged
it with the Failure Lab evidence work, and Aditya approved the merged version.

Honesty conventions:
- Past tense only for things that exist (the idea, the outline docs, the Oct 14 tests, Aditya's own Oct 25 run).
- Drawings of the unbuilt product carry a bottom subheader ending "· concept sketch" (scenes_body.py SUBHEAD).
- B05/B06 show Aditya's real screenshot; subheaders end "· Oct 25 · colours inverted".
- First person as Aditya; synthetic Kokoro voice (disclosed). No instructor persona.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "productlens-ai-pitch"
TITLE = "ProductLens AI"
NAME = "Aditya Hasija"
VOICE = "am_michael"   # chosen by Aditya 2026-10-14 from voice-samples/. Not am_onyx (the instructor persona's voice).
TAG_C = "constructed"
TAG_R = "real run · Oct 25 · by Aditya"

# ── narration, verbatim from the approved script ──
NARR = {}
for line in (HERE / "SCRIPT-v2.md").read_text().splitlines():
    if line.startswith("| B"):
        c = line.split("|")
        NARR[c[1].strip()] = c[2].strip()
assert "⟦" not in "".join(NARR.values()), "unfilled placeholder in SCRIPT-v2.md"

# beat_id: (scene class, picture, honesty tag, labels)
PLAN = {
 "B00": ("B00_Checkout", "A kraft shopping cart; a four-step strip of checkout pages folds into one page.", TAG_C, ["4 steps", "1 page"]),
 "B01": ("B01_Questions", "Three question cards rise in turn beside the folded page: customers, competitors, risks.", TAG_C, ["customers", "competitors", "risks"]),
 "B02": ("B02_InOut", "A feature card and two article pages slide into a dark machine; one brief page slides out.", TAG_C, ["feature", "brief"]),
 "B03": ("B03_Brief", "The brief page is large: three section bars draw in; 'sourced' and 'assumption' tags land on lines.", TAG_C, ["sourced", "assumption"]),
 "B04": ("B04_Agents", "The idea card splits to three agent blocks; their pages go to a review desk; one goes back once.", TAG_C, ["market", "customers", "risks"]),
 "B05": ("B05_RealRun", "Aditya's real ChatGPT screenshot (cropped to the conversation, date visible); the planted line is underlined.", TAG_R, ["planted claim"]),
 "B06": ("B06_RealGap", "The screenshot pans down; its one source chip is circled; unlabelled rows get grey '?' marks.", TAG_R, ["1 source"]),
 "B07": ("B07_Narrower", "A big 'startup idea' crate beside one small feature card that gets a 'sourced' tag and a check.", TAG_C, ["startup idea", "one feature"]),
 "B08": ("B08_Repo", "A release parcel opens: an app window, a fan of test cards, and a score sheet rise out.", TAG_C, ["GitHub repo"]),
 "B09": ("B09_FirstMinute", "Three pages land on a desk in order (README, brief, scores); a cursor touches each.", TAG_C, ["README", "brief", "scores"]),
 "B10": ("B10_Contract", "An instruction page and a gate; the agent's answer must fit a dashed outline before the barrier lifts.", TAG_C, ["instructions", "format"]),
 "B11": ("B11_FirstRun", "One parcel rides a short conveyor; a single log page drops out and a check draws on it.", TAG_C, ["first run"]),
 "B12": ("B12_NoVerdict", "A card marked 'go / no-go' rides to a gate; the barrier drops and it slides away.", TAG_C, ["no verdict"]),
 "B13": ("B13_RubberStamp", "A cracked page slides under an approval stamp; the stamp approves it anyway.", TAG_C, ["rubber stamp"]),
 "B14": ("B14_CatchRate", "Test samples slide into a bench; a tally grows; a small code block docks beside it.", TAG_C, ["catch rate"]),
 "B15": ("B15_Pivot", "Last pitch's idea crate shrinks away; the product-manager feature card takes its place.", None, ["first pitch", "for PMs"]),
 "B16": ("B16_Shelves", "A filled 'have' shelf beside an outlined 'new' shelf.", None, ["have", "new"]),
 "B17": ("B17_Status", "A small 'exists' tray with three items; a long row of dashed 'will build' slots.", None, ["exists", "will build"]),
}

SPARSE_REASON = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, voice carries the "
                 "explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and contrast still apply.")


def est(n):
    return round(len(n.split()) / 2.5, 1)


def beat(bid):
    cls, image, tag, labels = PLAN[bid]
    n = NARR[bid]
    return {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
            "narration_text": n, "estimated_duration_s": est(n), "voice": VOICE, "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": [],
                     "manim": {"class": cls}, "motion_claim": image, "labels": labels, "honesty_tag": tag},
            "qc": {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}}


def remotion(bid, act, narration, pattern, props, show, **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": est(narration), "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


BEATS = [remotion("BIDEA", "the question", NARR["BIDEA"], "BrutalistHesitantWriter",
    {"text": "Should we build this feature?", "triggerWords": "build this feature?", "replacementWords": "test first?",
     "fontSize": 70, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
     "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'Should we build this feature?'"}, {"at": 0.6, "event": "corrects to 'Should we test first?'"}],
    lead_silence_s=0.8, motion_claim="The writer types the usual question and corrects it to the better one.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."})]
BEATS += [beat(f"B{i:02d}") for i in range(18)]
BEATS.append({"beat_id": "BOUT", "act": "outro", "lane": "manim", "proof_gate": "SHOW",
              "narration_text": NARR["BOUT"], "estimated_duration_s": 3.0, "voice": VOICE, "engine": "kokoro",
              # Own outro, not the toolkit's ClaudeTitleOutro: that card hard-codes the instructor's handle, and
              # OUTRO-LOCK.md limits it to the instructor's channel. The assignment forbids the instructor's credit line.
              "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": "Title 'ProductLens AI' with the feature card above; 'Aditya Hasija' below.",
                       "show": [], "manim": {"class": "BOUT_Title"}, "labels": ["ProductLens AI", "Aditya Hasija"], "honesty_tag": None},
              "qc": {"sparse_by_design": True, "sparse_reason": "Outro title card: title and name only."},
              "kind": "outro_voice", "tail_silence_s": 1.0})

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "PITCH · FINAL PROJECT", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "aditya-hasija", "channel_title": NAME, "persona": f"{NAME} (first person)",
    "voice": VOICE, "voice_kokoro": VOICE, "voice_note": "Synthetic local Kokoro voice reading Aditya's script in first person (disclosed in SOURCES.md).",
    "engine": "kokoro", "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9",
    "width": 3840, "height": 2160, "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Course pitch film (INFO7375 final project pitch, 2–4 min): opens on the hesitant writer, no terms card, "
                              "no verdict card and no Your Turn beat; runtime goes to the seven required pitch answers. Spoken outro stays."),
    "audience": "INFO7375 instructor and TAs; hiring managers for AI product manager roles",
    "source_doc": "SCRIPT-v2.md (approved 2026-10-25); research/baseline-v2-prompt.md (Aditya's own run, 2026-10-25)",
    "honesty": "Past tense only for what exists. Drawings of the unbuilt product tagged 'constructed'; Aditya's real run tagged.",
    "tags": ["AI product management", "decision brief", "multi-agent", "evaluation", "source grounding"]},
    "beats": BEATS}

# Carry measured audio forward (show-tell trap 4) when the narration is unchanged.
_old = HERE / "beat_sheet.json"
if _old.exists():
    prev = {b["beat_id"]: b for b in json.loads(_old.read_text())["beats"]}
    for b in BEATS:
        p = prev.get(b["beat_id"], {})
        if p.get("narration_text") == b["narration_text"]:
            for k in ("audio_file", "actual_duration_s"):
                if k in p:
                    b[k] = p[k]

(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
words = sum(len(b["narration_text"].split()) for b in BEATS)
print(f"{len(BEATS)} beats; {words} words; est {round(sum(b['estimated_duration_s'] for b in BEATS))} s")
