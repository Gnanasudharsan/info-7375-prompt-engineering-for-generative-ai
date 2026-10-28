#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for the Final Project Pitch Film, v3 (resubmission)
"Source Check for Support AI" (Mayank Bhadrasen, INFO 7375). v1 (2026-10-14) is in _v1/.

v3 answers the v1 feedback (41/50):
  * professor: @Mayank on screen at all times (the toolkit now stamps metadata.handle on every
    frame); more detail; why it is a problem; what I am doing and why it matters;
  * TA: who is doing it (BWHO); a plain explanation a non-technical viewer can follow (BKID);
    concise but technically complete (B03-B06); "shown, not asserted": the core check is drawn as
    the bot's words beside the policy line with the conflicting word marked (B00, B05);
    the TA's next step is built and shown with its real output (B07, B09).
Body beats are HyperFrames compositions (code/hf_scenes.py); the bookends stay Remotion.
Honesty: past tense only for what ran (the slice in slice/); everything else says "will", and the
on-screen chip says "proposed design", "real case" or "real output" on every body beat.
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
SLUG = "source-check-pitch"
TITLE = "Source Check for Support AI"
VOICE = "am_onyx"   # "Mayank" / "Bhadrasen" are respelled for Kokoro in runtime/pronunciation/mayank.json


def est(text):
    return round(len(text.split()) / 3.0, 1)


def hf(bid, act, chip, narration, image):
    return {"beat_id": bid, "act": act, "lane": "hyperframes", "proof_gate": "SHOW",
            "narration_text": narration, "estimated_duration_s": est(narration),
            "voice": VOICE, "engine": "kokoro",
            "shot": {"type": "HYPERFRAMES", "source": "own", "visual_intent": image,
                     "hyperframes": {"composition": f"hyperframes/{bid}", "chip": chip}},
            "qc": {"sparse_by_design": True,
                   "sparse_reason": "One picture per beat with a caption band kept clear at the bottom."}}


def remotion(bid, act, narration, pattern, props, **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


BEATS = [
    remotion("BIDEA", "the question",
             "Hola, I'm Mayank Bhadrasen, and this is my final project pitch. "
             "It starts with one question: can a support bot answer policy questions from a current source?",
             "BrutalistHesitantWriter",
             {"text": "Can a support bot answer\npolicy questions safely", "triggerWords": "safely",
              "replacementWords": "from a current source", "fontSize": 70, "charMs": 24,
              "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
              "seed": SLUG, "banner": ""},
             lead_silence_s=0.8,
             motion_claim="The writer corrects a vague goal (safely) into the checkable one (from a current source).",
             qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),

    hf("BWHO", "who", "",
       "Who's doing it? I'm a master's student in Information Systems at Northeastern. "
       "Claude Code is my assistant, but I decide what to build and what counts as correct.",
       "Name card: Mayank Bhadrasen, M.S. Information Systems, Northeastern; solo project; me vs Claude split."),

    hf("BKID", "the idea, simply", "",
       "Here's the idea, simply. A company has a robot helper that answers customers. Sometimes it sounds very sure and is still wrong. "
       "My project is a checker at the door: before an answer goes out, it looks it up in the company's rule book. "
       "If the book agrees, it goes out. If not, a person looks first.",
       "Robot speech bubble -> a checker at a door holding a rule book -> 'goes out' or 'a person looks first'."),

    hf("B00", "why it is a problem", "real case",
       "Why is this a problem? It already happened. In 2024, Air Canada's chatbot told a grieving customer "
       "he could claim a bereavement fare after his trip. The policy said the request had to come before. "
       "One word was flipped, and a Canadian tribunal held the airline responsible for what its chatbot said.",
       "The chatbot's claim beside the policy line; 'after' and 'before' marked; the ruling caption."),

    hf("B01", "why it matters at scale", "",
       "And it isn't one customer. A bot gives the same answer to everyone who asks, just as confidently, "
       "so one wrong rule becomes a wrong promise to all of them. "
       "Today's safety net is usually someone reading transcripts later, after customers were told.",
       "One wrong bubble copies into a wall of identical bubbles; a 'reviewed later' clock sits after the send arrow."),

    hf("B02", "what I am building", "proposed design",
       "So here's what I'm building. Source Check sits between any support bot and the customer, "
       "checks each policy answer against the current, dated policy, and holds it for a person when the policy doesn't back it up. "
       "It catches the mistake before the customer sees it.",
       "Bot -> Source Check -> customer; the check sits before the send, transcript review after it."),

    hf("B03", "how it works", "proposed design",
       "Under the hood, five steps. The bot's draft arrives at an n8n webhook. Claude splits it into claims. "
       "Python checks each claim against the policy store. The answer passes, or waits in Slack for a support lead. "
       "Every decision is logged with its policy version.",
       "Five-box architecture lighting up in order: n8n webhook, Claude extract, Python check, pass/hold, log."),

    hf("B04", "step one: the contract", "proposed design",
       "Step one is a prompt contract. Claude returns each claim as JSON with five fields: topic, condition word, amount, unit, "
       "and what it's measured from, like travel or purchase. "
       "My code validates the JSON, and if a field is missing or extra, the answer is held.",
       "The bot's sentence turns into a JSON claim, field by field, with the condition word marked."),

    hf("B05", "step two: the check", "real output",
       "Step two is the check. Python code, not the model, finds the current policy and compares the claim field by field. "
       "The claim says after travel; the policy says before travel. That's a mismatch, so the answer is held, "
       "and the reason quotes the policy line. Claude only extracts. Plain code decides, because a model can be confidently wrong.",
       "Claim row beside policy row; after vs before marked; HOLD with the quoted policy line (real checker output)."),

    hf("B06", "pass or hold", "proposed design",
       "If every claim matches, the answer goes out and the log records the policy version. "
       "If a claim has no source, is outdated, or contradicts the policy, it's held, "
       "and a support lead sees the reason in Slack, then approves, edits, or rejects it.",
       "Two lanes: PASS to the customer with a log line; HOLD to a Slack card mock-up with approve / edit / reject."),

    hf("B07", "what runs today", "real output",
       "And the core already runs. Since the first pitch, the checker and the tests the TA asked for are built. "
       "The Air Canada case: held. Within ninety days against ninety days after: held. A matching answer: passes. "
       "All twenty-one tests pass, and when the check is broken on purpose, tests fail, so they can say no. "
       "The claims are written by hand for now.",
       "Real pytest output, then the real mutation run: 6 failed."),

    hf("B08", "alternatives", "",
       "How do today's tools handle this? Intercom Fin is an AI agent trained on a company's policies and procedures. "
       "Teams test changes in simulations before going live, and it hands hard cases to people. "
       "Zendesk's AI agents answer from the help-center articles you connect, and escalate to a human when they can't answer. "
       "Manual review reads transcripts after answers are sent. What I didn't find on their public pages "
       "is a check of each answer, at send time, against the current dated policy.",
       "Three cards (Fin, Zendesk, manual review) on a before/after-send timeline; the empty slot before send."),

    hf("B09", "who opens it", "real output",
       "Who opens it? A support lead, or a hiring manager. In their first minute, one command shows the Air Canada answer held, "
       "with the reason and the policy line, and that command works today.",
       "A terminal: python3 -m source_check.demo and its real output."),

    hf("B10", "what it will prove", "proposed design",
       "It will prove prompt contracts, source grounding, deterministic checks, approval gates, and evaluation. "
       "I'll measure how many wrong answers slip through and how many good ones get held, "
       "and report no numbers until I've measured them.",
       "Five skill tiles; a labelled test set splitting into correct / outdated / invented; two empty meters."),

    hf("B11", "scope and risk", "proposed design",
       "The scope: refunds, fees, and eligibility for one fictional airline, on synthetic data. "
       "It won't write answers or replace the bot. The biggest risk is Claude dropping a condition word. "
       "So uncertain claims default to hold, and the test set will be full of condition flips.",
       "In / out lists; the risk drawn as 'before' sliding out of a claim; default HOLD."),

    hf("B12", "what is new for me, and what is next", "",
       "What's new for me is building an evaluation set and measuring the misses. "
       "Next: Claude extraction, the n8n workflow, the Slack hold queue, and the labelled test set.",
       "Exists today vs will exist, two columns, with the slice now in 'exists'."),

    {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
     "narration_text": f"{TITLE}: check the answer before the customer sees it. I'm Mayank. Thank you for watching.",
     "estimated_duration_s": 7.0, "voice": VOICE, "engine": "kokoro",
     "shot": {"type": "REMOTION", "source": "own",
              "remotion": {"pattern": "TcTitleOutro", "props": {"title": TITLE + ".", "slug": SLUG + "-film",
                                                               "handle": "@Mayank", "showMascot": False,
                                                               "inkPeriod": True}}},
     "kind": "outro_voice", "tail_silence_s": 1.0},
]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "FINAL PROJECT PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "mayank", "persona": "Mayank (narrating as myself)", "voice": VOICE, "voice_kokoro": VOICE,
    "engine": "kokoro", "clock": "narration", "palette": "claude", "register": "plain", "fps": 24, "aspect_ratio": "16:9",
    "caption_policy": "burned (HyperFrames edit pass)", "greeting_language": "Spanish (Hola)",
    "handle": "@Mayank", "folderLabel": "@Mayank", "in_for_bear": False, "version": "v3 (resubmission)",
    "bookend_exempt": ["cold-open", "terms", "bvdt", "handoff"],
    "bookend_exempt_reason": ("Pitch film (INFO 7375 Final Project Pitch): hesitant-writer open; the terms card is replaced by "
                              "BKID, a plain explanation for non-technical viewers (TA feedback); no verdict card and no Your Turn "
                              "prompt; narrated as myself, so no instructor persona or credit line; outro is TcTitleOutro (@Mayank)."),
    "audience": "a non-technical viewer first; hiring managers for AI automation engineers; INFO 7375 reviewers",
    "source_doc": "PROJECT-BRIEF.md; Moffatt v. Air Canada (BC CRT, 2024); fin.ai public page (read 2026-10-14); slice/evidence/",
    "honesty": "the slice in slice/ ran (past tense, real output shown); everything else is a plan said with 'will' and chipped 'proposed design'",
    "tags": ["AI automation", "n8n", "Claude", "support AI", "source grounding", "INFO 7375"]},
    "beats": BEATS}

(REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
words = sum(len(b["narration_text"].split()) for b in BEATS)
print(len(BEATS), "beats;", words, "words; ~", round(words / 3.1), "s at Kokoro's pace")
