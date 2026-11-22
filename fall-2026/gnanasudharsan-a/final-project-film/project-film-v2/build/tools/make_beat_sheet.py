"""make_beat_sheet.py — build beat_sheet.json from script.md.

Each beat's narration_text is the exact text of its script lines (L01…), joined
with a space, so the film says what the approved script says, word for word.
BEATS below is the only editorial choice: which lines form each beat, and which
picture fills it.

Usage: python3 tools/make_beat_sheet.py <script.md> <out beat_sheet.json>
"""
import json
import re
import sys
from pathlib import Path

VOICE = "af_heart"
WPM = 130

# beat_id, act, script lines, shot
#   ("manim", SceneClass)  -> rendered by ./art run from scenes.py
#   ("still",)             -> media/<BID>.png   (tools/still_clips.py)
#   ("sequence",)          -> media/<BID>.mp4   (tools/still_clips.py)
BEATS = [
    ("B00", "title",            ["L01"],                      ("manim", "B00_Title")),
    ("B01", "the question",     ["L02", "L03"],               ("manim", "B01_Scattered")),
    ("B02", "what it does",     ["L04", "L05"],               ("manim", "B02_AnswerCard")),
    ("B03", "why it matters",   ["L06", "L07"],               ("manim", "B03_WhyItMatters")),
    ("B04", "existing tools",   ["L08", "L09"],               ("manim", "B04_Tools")),
    ("B05", "research",         ["L11"],                      ("manim", "B05_Research")),
    ("B06", "my test",          ["L13"],                      ("manim", "B06_TestSetup")),
    ("B07", "notebooklm",       ["L14"],                      ("sequence",)),
    ("B08", "chatgpt",          ["L15"],                      ("still",)),
    ("B09", "the gap",          ["L16", "L17"],               ("manim", "B09_Gap")),
    ("B10", "larger system",    ["L18", "L19"],               ("manim", "B10_LargerToLite")),
    ("B11", "data",             ["L20"],                      ("manim", "B11_Data")),
    ("B12", "test set",         ["L21"],                      ("manim", "B12_TestSet")),
    ("B13", "retrieve + answer", ["L22", "L23"],              ("manim", "B13_RetrieveAnswer")),
    ("B14", "verify",           ["L24", "L25"],               ("manim", "B14_VerifyLoop")),
    ("B15", "resources",        ["L26"],                      ("manim", "B15_Resources")),
    ("B16", "five measures",    ["L27", "L28", "L29", "L30", "L31"], ("manim", "B16_Measures")),
    ("B17", "worked or not",    ["L32", "L33"],               ("manim", "B17_Decision")),
    ("B18", "first check",      ["L34"],                      ("manim", "B18_FirstCheck")),
    ("B19", "outro",            ["L35"],                      ("manim", "B19_Outro")),
]
PHONEME_BEATS = {"B00"}          # name spoken from IPA (tools/phoneme_name.py)


def main():
    script, out = Path(sys.argv[1]), Path(sys.argv[2])
    lines = dict(re.findall(r"^\*\*(L\d+)\*\* (.+)$", script.read_text(encoding="utf-8"), re.M))
    used = [lid for _, _, ids, _ in BEATS for lid in ids]
    unused = sorted(set(lines) - set(used))
    missing = [lid for lid in used if lid not in lines]
    if missing or unused or len(used) != len(set(used)):
        raise SystemExit(f"script/beat mismatch: missing={missing} unused={unused}")

    beats = []
    for bid, act, ids, shot in BEATS:
        text = " ".join(lines[i].strip() for i in ids)
        b = {"beat_id": bid, "act": act, "script_lines": ids, "narration_text": text,
             "voice": VOICE, "engine": "kokoro-phoneme" if bid in PHONEME_BEATS else "kokoro",
             "estimated_duration_s": round(len(text.split()) / WPM * 60, 1)}
        if shot[0] == "manim":
            b["shot"] = {"type": "GRAPHIC", "source": "manim", "manim": {"scene_class": shot[1]}}
        else:
            b["shot"] = {"type": "STILL", "motion": "hold", "treatment": "none"}
        beats.append(b)

    sheet = {"metadata": {"title": "DecisionTrace Lite — Project Film", "slug": "decisiontrace-lite-film",
                          "engine": "kokoro", "voice_kokoro": VOICE, "aspect": "16:9", "fit": "pad"},
             "beats": beats}
    out.write_text(json.dumps(sheet, indent=1, ensure_ascii=False), encoding="utf-8")
    words = sum(len(b["narration_text"].split()) for b in beats)
    print(f"{len(beats)} beats, {words} words, ~{words / WPM:.1f} min -> {out}")


if __name__ == "__main__":
    main()
