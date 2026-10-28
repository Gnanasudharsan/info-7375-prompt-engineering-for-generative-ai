#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for the INFO 7375 final-project pitch film.

Built on the show-tell chassis (skills/make/show-tell/SKILL.md), copied from
reference/example-make_sheet.py. Every body beat is ONE drawn isometric Manim
illustration on the Claude cream stage, with at most a few words of label; the
narration carries the explanation.

FOUR DELIBERATE DEVIATIONS from show-tell doctrine, all forced by the course
assignment ("Narrate as yourself. Do not use the instructor's name, persona, or
credit line."). Each one is logged in FRICTIONAL.md:

  1. BIDEA greeting is NOT "Hallo. This is Liam, in for Bear." — it is the
     author's own first-person opening.
  2. metadata.persona / channel name the author, not "Liam (in for Bear)".
  3. folderLabel in BDEFS and BHTF, and handle + narration in BOUT, name the
     author, not @NikBearBrown. SKILL.md marks the outro "never exempt" and
     OUTRO-LOCK.md enforces it, so the bookend/outro check is expected to flag
     this film. That report ships as-is with the reason, not papered over.
  4. Voice is Kokoro af_bella rather than the default am_onyx ("Liam"). It is a
     synthetic voice reading the author's own words, and it is disclosed as such
     in BIDEA, on the BOUT end card, and in SOURCES.md — the same practice the
     author used on her week-01 film for this course. Swap to a real recording of
     her voice if one is made; then the disclosure comes out and nothing else changes.

HONESTY (assignment rule): nothing in this film exists yet except the Unity game
referenced in B04 and B08. Every drawing of the proposed tool carries a
"proposed" label on screen; the one beat describing past experience carries
"spring 2026". Past tense is used ONLY in B04 and B08.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "show-tell-the-names-nothing-checks"
TITLE = "The Names Nothing Checks"
AUTHOR = "Weiting Wang"
HANDLE = "@WeitingWang0704"


def beat(bid, narration, cls, image, show):
    return {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
            "narration_text": narration,
            "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
            "voice": "af_bella", "engine": "kokoro",
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image,
                     "show": show, "manim": {"class": cls}, "motion_claim": image}}


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate,
         "narration_text": narration,
         "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "af_bella", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show,
                  "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


# ---------------------------------------------------------------- body (drawn)
# Cast, kept for the whole film: the project crate (left half = C# pages,
# right half = asset blocks), the string thread between them, two gates, the
# effect lamp, and the checklist slip.

B = [
 beat("B00",
      "This is a Unity project. One side holds the C sharp scripts. The other "
      "holds the assets, and the assets hold the project's real names.",
      "B00_Project",
      "An open isometric crate divided in two: pale pages stack on the left, dark asset "
      "blocks rise on the right. Labels beside each half: 'scripts' and 'assets'.",
      [{"at": 0.15, "event": "crate lands with floor shadow"},
       {"at": 0.45, "event": "pages stack on the left, label"},
       {"at": 0.75, "event": "asset blocks rise on the right, label"}]),

 beat("B01",
      "Code can only reach those names as text. A string. Material dot set float, "
      "open quote, glow active, close quote. That quoted word is the whole link.",
      "B01_StringReach",
      "A single ink thread draws from a page on the left across to one asset block on the "
      "right, ending in a small terracotta dot. One label beside the thread: 'string'.",
      [{"at": 0.2, "event": "page lifts forward"},
       {"at": 0.55, "event": "thread draws across, lands before the midpoint"},
       {"at": 0.85, "event": "terracotta end dot, label"}]),

 beat("B02",
      "Get that word wrong and nothing stops you. The compiler lets it through. "
      "The console stays quiet. The game runs. The glow simply never happens.",
      "B02_SilentPass",
      "The thread now ends in empty space. A crate rides between two open gates labelled "
      "'compiler' and 'console'; both stay open; an effect lamp at the end stays dark grey.",
      [{"at": 0.15, "event": "two gates draw, both open"},
       {"at": 0.5, "event": "crate rides through, fully opaque, lands before the midpoint"},
       {"at": 0.85, "event": "lamp stays dark; a small ring grows and fades"}]),

 beat("B02B",
      "Not everything is silent. Unity does warn you about a wrong animator parameter, once that "
      "line runs. It says nothing at all about a wrong shader property.",
      "B02B_WhatWarns",
      "Two terracotta runners approach the gates. The upper one is stopped by a bar that drops "
      "across it; the lower one passes straight through both and reaches the dark lamp. "
      "Labels beside: 'warns', 'silent'.",
      [{"at": 0.15, "event": "two runners line up"},
       {"at": 0.45, "event": "bar drops on the upper runner, lands before the midpoint"},
       {"at": 0.8, "event": "the lower runner reaches the lamp; labels"}]),

 beat("B03",
      "An assistant that only reads your C sharp files cannot know the name inside the shader "
      "graph. So the name in its answer is a guess, and no gate here catches a guess.",
      "B03_HalfRead",
      "A scan line sweeps only the left half of the crate and stops at the divider; the "
      "right half sits behind a pale ghost panel. One ink label: 'guess'.",
      [{"at": 0.2, "event": "ghost panel covers the right half"},
       {"at": 0.45, "event": "scan line sweeps the left half only, finishes before the midpoint"},
       {"at": 0.8, "event": "'guess' label lands beside the thread"}]),

 beat("B04",
      "Last spring I tried a tool that puts a model inside the Unity editor. I asked it "
      "to lay out a scene. It put things in the wrong places.",
      "B04_WritesIn",
      "A mechanical arm swings over the crate and drops three blocks at visibly wrong angles. "
      "Labels beside: 'writes', and a small corner stamp 'spring 2026'.",
      [{"at": 0.2, "event": "arm swings in, fully opaque"},
       {"at": 0.5, "event": "blocks drop crooked, settle before the midpoint"},
       {"at": 0.85, "event": "labels land"}]),

 beat("B04B",
      "What I got back was not a warning. It was a broken scene to undo. After that I "
      "built my scenes by hand.",
      "B04B_ByHand",
      "The arm fades to ghost grey; the three crooked blocks lift and a row of correctly "
      "seated blocks draws in beneath them. Label beside: 'by hand'.",
      [{"at": 0.15, "event": "arm fades to ghost"},
       {"at": 0.45, "event": "straight block row draws in, complete before the midpoint"},
       {"at": 0.8, "event": "crooked blocks fade; label lands"}]),

 beat("B05",
      "What I will build does the opposite. It reads the assets and writes down every "
      "name that really exists.",
      "B05_Checklist",
      "A paper slip draws itself beside the asset half and fills with ink tick rows, one per "
      "asset block. Labels beside: 'checklist', 'proposed'.",
      [{"at": 0.2, "event": "slip draws in beside the asset half"},
       {"at": 0.5, "event": "tick rows fill, complete before the midpoint"},
       {"at": 0.8, "event": "'proposed' stamp lands"}]),

 beat("B05B",
      "Then it checks each string in the code against that list, and marks what it cannot "
      "find. It never writes to your project.",
      "B05B_ReadOnly",
      "The thread from B01 re-routes from the page into the slip; one row turns to an ink cross. "
      "A large ink-outlined padlock draws over the crate. Labels beside: 'marked', 'read only'.",
      [{"at": 0.2, "event": "thread re-routes into the slip"},
       {"at": 0.45, "event": "one row turns to a cross, before the midpoint"},
       {"at": 0.8, "event": "padlock draws over the crate; labels land"}]),

 beat("B06",
      "The first piece I will make run is the shader property path. A test project with "
      "three wrong names planted in it. It has run when the report names those three, "
      "and nothing else.",
      "B06_Fixture",
      "A small crate beside the slip; three rows on the slip turn to ink crosses while the "
      "rest stay ticks. Labels: 'test project', 'proposed'.",
      [{"at": 0.2, "event": "small crate lands with shadow"},
       {"at": 0.5, "event": "three crosses land, before the midpoint"},
       {"at": 0.85, "event": "labels"}]),

 beat("B07",
      "What could sink it is false alarms. A string is not always written out in full. "
      "Flag good code, and nobody runs the tool twice.",
      "B07_FalseAlarm",
      "A grey bar stack grows on a plinth beside a correct tick row that flips to a cross; "
      "gaps between every segment. Labels beside: 'false alarms', 'proposed'.",
      [{"at": 0.2, "event": "plinth and axis draw"},
       {"at": 0.45, "event": "bar stack grows, settles before the midpoint"},
       {"at": 0.8, "event": "a good row flips to a cross; labels land"}]),

 beat("B07B",
      "So version one reads only strings written out in full. Everything else is marked "
      "cannot determine. And I publish both numbers, not just the flattering one.",
      "B07B_TwoNumbers",
      "A second and third grey bar stack grow beside the first, with gaps: 'caught' and "
      "'cannot tell'. One terracotta dot tops the middle stack. Label beside: 'proposed'.",
      [{"at": 0.2, "event": "second stack grows"},
       {"at": 0.45, "event": "third stack grows, settles before the midpoint"},
       {"at": 0.8, "event": "terracotta dot lands on the middle stack; labels"}]),

 beat("B08",
      "Why me. The Unity half I can already do. I shipped a Unity dungeon game last spring, "
      "and its glowing sword runs on exactly this kind of string.",
      "B08_HaveTray",
      "A shallow tray lands and fills with solid ink objects: a page, an asset block, a small "
      "sword with one terracotta spark on its top face. Label beside: 'have'.",
      [{"at": 0.15, "event": "tray lands with floor shadow"},
       {"at": 0.45, "event": "objects land in the tray, before the midpoint"},
       {"at": 0.8, "event": "terracotta spark on the sword; label lands"}]),

 beat("B08B",
      "Building an evaluation set and reporting real numbers, I have never done. That is why "
      "I picked this project.",
      "B08B_NewTray",
      "A second tray draws in beside the first and stays an outline; a ghost-grey slip and a "
      "ghost-grey bar stack draw inside it as outlines only. Label beside: 'new'.",
      [{"at": 0.15, "event": "second tray outline draws"},
       {"at": 0.45, "event": "ghost slip and bar outlines draw, complete before the midpoint"},
       {"at": 0.8, "event": "label lands"}]),
]

# ------------------------------------------------------------------- bookends

OPEN = [
 remotion("BIDEA", "the question",
    f"Hi. These are {AUTHOR}'s words, read by a synthetic voice. I build games in Unity. "
    "When I asked an AI for gameplay code, I used to check whether it compiled. That turned "
    "out to be the wrong question.",
    "BrutalistHesitantWriter",
    {"text": "Can an AI write Unity code\nthat compiles",
     "triggerWords": "that compiles", "replacementWords": "that actually runs",
     "fontSize": 70, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1,
     "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'Can an AI write Unity code'"},
     {"at": 0.65, "event": "backspaces 'that compiles' -> 'that actually runs' on the spoken correction"}],
    lead_silence_s=0.8,
    motion_claim="The writer types the naive compile question and corrects it to the real one: whether it runs.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),

 remotion("BDEFS", "terms",
    "Three terms. A shader property: a name stored in a Unity asset, not in the code. "
    "A string reference: code reaching that name as quoted text. And a silent failure: "
    "wrong code that compiles, runs, and does nothing.",
    "ClaudeDefinitions",
    {"title": "Terms In This Film",
     "terms": [{"term": "shader prop", "meaning": "a name stored in a Unity asset, not in the code"},
               {"term": "string ref", "meaning": "code reaching that name as quoted text"},
               {"term": "silent fail", "meaning": "wrong code that compiles, runs, and does nothing"}],
     "folderLabel": HANDLE},
    [{"at": 0.15, "event": "'shader prop' lands"},
     {"at": 0.5, "event": "'string ref' lands"},
     {"at": 0.8, "event": "'silent fail' lands"}], gate="CARD",
    qc={"sparse_by_design": True, "sparse_reason": "TERMS card: three prerequisites, one line each."}),
]

YT_PROMPT = ("Pick a project you know well and ask your AI assistant for code that uses a name "
             "stored outside the source files: an animator parameter, a shader property, a config "
             "key. Then open the file that actually defines that name and compare. Tell me whether "
             "the assistant read it or guessed it.")

YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude. " + YT_PROMPT + " Then check two things yourself. Did it "
    "say out loud that it was unsure? And would anything in your build have caught it if it was wrong?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN",
     "segment": "Find One Guessed Name", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did it say it was unsure?",
                "Check: would anything in your build have caught it?"],
     "folderLabel": HANDLE, "modelLabel": "Opus 5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"},
     {"at": 0.1, "event": "the prompt types in full"},
     {"at": 0.85, "event": "two check lines land"}])

SPARSE_REASON = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal "
                 "labels, with the voice carrying the explanation. The negative space is the style, "
                 "so only underfill and clustered are waived; edge-bleed, empty-frame and contrast "
                 "still apply.")
for b in B:
    if b["lane"] == "manim":
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}

B = OPEN + B + [YOURTURN]

B.append({"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
          "narration_text": f"{TITLE}. Read by a synthetic voice, for {AUTHOR.split()[0]}.",
          "estimated_duration_s": 4.0, "voice": "af_bella", "engine": "kokoro",
          "shot": {"type": "REMOTION", "source": "own",
                   "show": [{"at": 0.0, "event": "title restates; author handle"}],
                   "remotion": {"pattern": "ClaudeTitleOutro",
                                "props": {"title": TITLE, "slug": SLUG,
                                          "handle": HANDLE, "subline": ""}}},
          "kind": "outro_voice", "tail_silence_s": 1.0})

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "UNITY · VERIFICATION",
    "skill": "show-tell", "style_preset": "show-tell",
    "channel": "weiting-wang", "channel_title": HANDLE,
    "persona": ("Synthetic Kokoro af_bella voice reading Weiting Wang's own words "
                "(disclosed in the opening beat, on the end card, and in SOURCES.md)"),
    "voice": "af_bella", "voice_kokoro": "af_bella", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "plain",
    "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "English (Hi)",
    "bookend_exempt": ["cold-open", "bvdt"],
    "bookend_exempt_reason": (
        "show-tell style: opens on the hesitant writer plus the terms card, no verdict card; "
        "Your Turn is the Claude.ai composer. The spoken outro stays, but names the author "
        "instead of the instructor: the INFO 7375 assignment requires narrating as oneself and "
        "forbids the instructor's name, persona or credit line, so the outro handle and "
        "narration are the author's. OUTRO-LOCK is expected to flag this; see FRICTIONAL.md."),
    "audience": "Unity gameplay programmers who write code with an AI assistant, and reviewers "
                "looking at tools and AI-engineering work",
    "honesty_note": (
        "Nothing in this film exists yet except the Unity game referenced in B04 and B08. "
        "Every drawing of the proposed tool is labelled 'proposed' on screen. Past tense appears "
        "only in B04 and B08, both of which describe work actually done in spring 2026. "
        "CORRECTED 2026-10-13: an earlier cut claimed the console says nothing about a wrong "
        "animator parameter. Unity does warn about that one. The claim now names the shader "
        "property, which Unity's own documentation says has no effect and no message, and B02B "
        "states the difference out loud. See FACTCHECK.md rows 3 and 4."),
    "source_doc": "PROJECT-BRIEF.md (this repository); brutalist.art skills/make/show-tell/SKILL.md",
    "playlist": "INFO 7375 Fall 2026", "chapter_number": 0,
    "tags": ["Unity", "C#", "verification", "source grounding", "evaluation",
             "prompt contracts", "INFO 7375"]},
    "beats": B}

(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(B), "beats; est", round(sum(b["estimated_duration_s"] for b in B)), "s")
