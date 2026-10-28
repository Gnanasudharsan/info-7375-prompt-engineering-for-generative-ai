#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for the Remnix Agent pitch film (INFO 7375).

Format: Brutalist show-tell (one drawn picture per beat, minimal labels, the
voice explains), adapted for a student pitch:
  - narration is first person as Revan C, read by a free Kokoro voice
    (af_bella) and labelled "synthetic voice" on screen;
  - no instructor persona greeting, handle or portraits;
  - no Claude.ai "Your Turn" composer (bhtf exempt) and no verdict card;
  - the outro is our own drawn card (Revan's name), not ClaudeTitleOutro,
    whose handle is hard-coded to the instructor's channel.

Honesty rule: only Money Map exists today. Every Remnix line says "will".
Real material: one screenshot of the public Money Map page taken 2026-10-14
16:20 EDT (pantry/money-map-2026-10-14.png). The one mock-up (B05) is
labelled CONSTRUCTED on screen and uses only numbers from that screenshot.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "remnix-agent-pitch"
TITLE = "Remnix Agent"
NAME = "Revan C"   # the course repo stores no full names
VOICE = "af_bella"
WPS = 2.5  # words per second, for the estimate only; measured audio is the clock

SPARSE_REASON = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal "
                 "labels, the voice carries the explanation. Only underfill and clustered are waived.")


def est(text):
    return round(len(text.split()) / WPS, 1)


def beat(bid, narration, cls, image, show, sparse=True):
    b = {"beat_id": bid, "act": "pitch", "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                  "manim": {"class": cls}, "motion_claim": image}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}
    return b


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": est(narration),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show,
                  "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


OPEN = [
    remotion("BIDEA", "the question",
        "Hola. I'm Revan, a graduate student at Northeastern. This film pitches a project that doesn't exist yet, for people sending money to family in Mexico. The obvious question is which way is cheapest. Remnix will also answer why.",
        "BrutalistHesitantWriter",
        {"text": "Which way to send $500\nto Mexico is cheapest?",
         "triggerWords": "is cheapest", "replacementWords": "is cheapest and why",
         "fontSize": 70, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1,
         "mistakeRate": 2, "jitter": 20, "seed": SLUG,
         "banner": "", "brandLabel": "Synthetic voice (Kokoro) · written with Claude, reviewed by Revan"},
        [{"at": 0.0, "event": "types the naive question"},
         {"at": 0.75, "event": "'is cheapest' → 'is cheapest and why' on the spoken correction"}],
        lead_silence_s=0.8,
        motion_claim="The writer types the naive 'cheapest' question and corrects it to 'cheapest and why'.",
        qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
]

BODY = [
    beat("BPLAIN",
         "When you send money home to Mexico, part of it disappears in fees and the exchange rate. Remnix will be like a calculator that shows its work: you ask what it costs, and it shows every number and where it came from.",
         "BPLAIN_Simple",
         "A stack of bills labelled '$500'; two bills slide off into a small tray labelled 'fees'; then a receipt "
         "page appears and its lines write in (the calculator showing its work).",
         [{"at": 0.1, "event": "$500 stack"}, {"at": 0.35, "event": "bills slide into 'fees'"},
          {"at": 0.7, "event": "receipt writes in"}]),
    beat("B00",
         "First, what's real. As a software engineer co-op at the MIT Digital Currency Initiative, I built Money Map, a public dashboard that's live today. It compares banks, apps, transfer services and stablecoins for sending dollars to Mexico.",
         "B00_MoneyMap",
         "The real Money Map screenshot (cropped header + map) slides onto the stage inside an ink frame; "
         "a tag beside it lands: 'real screenshot · 2026-10-14'.",
         [{"at": 0.1, "event": "screenshot slides in"}, {"at": 0.4, "event": "date tag"}],
         sparse=False),
]
# B00 shows a real screenshot: shot.type STILL tells GATE T the small text inside the
# screenshot is the page's own content, not this film's typography.
BODY[1]["shot"]["type"] = "STILL"
BODY += [
    beat("B02",
         "Money Map is a dashboard: you pick filters and read numbers. So I will build Remnix, an agent you can ask in plain words, like: why is Wise cheaper than my bank? It will answer with Money Map's data, showing the math and the source behind every number. None of it exists yet.",
         "B02_Remnix",
         "A sealed kraft crate drops onto the stage, drawn in dashed outline (not built); "
         "labels 'Remnix' and 'proposed' sit beside it.",
         [{"at": 0.1, "event": "dashed crate drops"}, {"at": 0.6, "event": "'proposed' tag"}]),
    beat("B03",
         "It will be a public GitHub repo. A Postgres database will hold three tables: quotes, exchange rates and snapshots, each row stamped with its source and time. A Fast API endpoint, POST slash ask, will take the question.",
         "B03_Data",
         "Database drawers with three table labels beside them (quotes, fx_rates, snapshots); then a server "
         "tower labelled 'POST /ask' appears and a cable draws from it to the drawers.",
         [{"at": 0.1, "event": "drawers + table labels"}, {"at": 0.7, "event": "POST /ask server + cable"}]),
    beat("B04",
         "Then Claude will pick one of two tools: get quotes, which reads prices from the database, or compute cost, which does the math in Python, not in the language model. The answer will come back with the row IDs and timestamps it used.",
         "B04_Tools",
         "An agent workstation with two tool blocks beside it (get_quotes, compute_cost); the compute_cost tool "
         "undocks; an answer page appears with its 'row IDs' label.",
         [{"at": 0.15, "event": "two tools"}, {"at": 0.6, "event": "compute_cost undocks"},
          {"at": 0.8, "event": "answer + row IDs"}]),
    beat("B05",
         "Its rule will be a prompt contract: no number without a source. This card is a constructed mock-up; its number is real, from my Money Map screenshot: a thousand dollars with Wise cost seven fifty-four.",
         "B05_Answer",
         "An answer page with a large hero number '$7.54'; a source tag 'Money Map · Oct 14' clips to its "
         "edge; a big 'CONSTRUCTED' label sits beside the page the whole beat.",
         [{"at": 0.0, "event": "'CONSTRUCTED' label"}, {"at": 0.35, "event": "$7.54 lands"},
          {"at": 0.7, "event": "source tag clips on"}]),
    beat("B06",
         "Money Map models a stablecoin sandwich: dollars become a stablecoin, a digital dollar, cross a blockchain, then become pesos. Remnix will show the cost of each layer.",
         "B06_Sandwich",
         "Three slabs stack one at a time (buy, send, sell); a terracotta dot lights on each slab as it lands.",
         [{"at": 0.25, "event": "buy slab"}, {"at": 0.45, "event": "send slab"}, {"at": 0.65, "event": "sell slab"}]),
    beat("B07",
         "I checked three alternatives on October fourteenth. Wise's comparison page and Monito didn't include stablecoin routes, and the World Bank's newest data for this corridor is from August twenty twenty-five. Remnix will include them, every number sourced.",
         "B07_Alternatives",
         "Three comparison trays in a row labelled Wise, Monito, World Bank; the sandwich slab tries each of the "
         "first two and doesn't fit; a dated tag drops on the third.",
         [{"at": 0.2, "event": "three trays"}, {"at": 0.45, "event": "slab misses Wise, Monito"},
          {"at": 0.75, "event": "date tag on World Bank"}]),
    beat("B08",
         "Who opens it? Hiring managers and engineers at fintech and crypto companies, my target role as a software engineer, plus researchers and policymakers who study remittance costs. In sixty seconds, they'll run one command and trace every number to a database row.",
         "B08_Reviewer",
         "A README page opens; a dark terminal block runs (a terracotta cursor light); an answer page appears and "
         "leader lines run from it to one drawer; a '60 s' counter climbs.",
         [{"at": 0.2, "event": "README"}, {"at": 0.45, "event": "terminal runs"},
          {"at": 0.7, "event": "answer → drawer"}]),
    beat("B09",
         "The first piece I'll make run: load Money Map's Mexico data into Postgres and answer one question with sources. You'll know it ran when the total matches Money Map's snapshot, sources printed.",
         "B09_FirstRun",
         "Records drop into the drawers; one answer page and one Money Map page sit side by side with the same "
         "number; a check mark draws between them.",
         [{"at": 0.2, "event": "records load"}, {"at": 0.55, "event": "two matching pages"},
          {"at": 0.8, "event": "check"}]),
    beat("B10",
         "Then twenty known-answer questions: a pie test suite will score them the same way every run, and write each wrong answer, and how it was caught, to a log.",
         "B10_TestSet",
         "A queue of question cards in a row passes a checkpoint scanner one by one; a hero '20' sits above; "
         "one card is pulled aside into an open binder (the wrong-answer log).",
         [{"at": 0.15, "event": "20"}, {"at": 0.4, "event": "cards pass the scanner"},
          {"at": 0.75, "event": "one card into the log"}]),
    beat("B11",
         "What's out: Remnix will not move money, or tell anyone which provider to choose. It will explain costs, for one corridor only: U S to Mexico.",
         "B11_Out",
         "A parcel rolls toward a permission gate; the barrier drops and stops it; one single arrow 'US → MX' "
         "draws beside it.",
         [{"at": 0.2, "event": "parcel"}, {"at": 0.45, "event": "barrier drops"}, {"at": 0.75, "event": "US → MX"}]),
    beat("B12",
         "What could sink it? Money Map's prices are live. On October fourteenth, the stablecoin route moved from seven forty-two to eight ninety-nine within about an hour. So known answers go stale. I'll freeze a dated snapshot for testing.",
         "B12_Risk",
         "A price page's number ticks up (7.42 → 8.99); then a copy of the page is clamped and dropped into a "
         "vault with a date tag; the vault bar locks.",
         [{"at": 0.25, "event": "number ticks"}, {"at": 0.6, "event": "snapshot clamped"}, {"at": 0.8, "event": "vault locks"}]),
    beat("B13",
         "What will this prove? Source grounding, tool calling, prompt contracts and evaluation. A reviewer could fairly conclude I can build a small, checked AI tool on real payment data, backed by the test scores and the wrong-answer log.",
         "B13_Proves",
         "A review desk: a results page slides onto it (test scores); an evidence binder lands beside it "
         "(wrong-answer log).",
         [{"at": 0.1, "event": "results page onto the desk"}, {"at": 0.8, "event": "binder lands"}]),
    beat("B14",
         "Why this project? It's a mix. It builds on Money Map and points at the fintech work I want. Cost modeling, dashboards and GitHub Pages I already have; Money Map is the evidence. New to me: source grounding, tool calling, evaluation, Postgres and Fast API.",
         "B14_Skills",
         "Two shelves: left 'have' holds three solid blocks next to the Money Map page; right 'new' shows five "
         "dashed outlines that draw in one by one.",
         [{"at": 0.2, "event": "'have' shelf"}, {"at": 0.55, "event": "'new' outlines draw"}]),
    beat("B15",
         "So today, one thing exists: Money Map. Everything else in this film is a plan.",
         "B15_ExistsWill",
         "Left: Money Map page, solid, a check mark draws. Right: the Remnix crate and its parts, all dashed. "
         "Labels 'exists' and 'will exist'.",
         [{"at": 0.2, "event": "check on Money Map"}, {"at": 0.55, "event": "dashed Remnix parts"}]),
]

OUTRO = beat("BOUT", f"{TITLE}. {NAME}.", "BOUT_Close",
             "Title 'Remnix Agent' and 'Revan C' on the cream stage; a small line beneath reads "
             "'synthetic voice · pitch, not a build'; the dashed crate from B02 sits beside.",
             [{"at": 0.0, "event": "title and name"}, {"at": 0.4, "event": "crate"}])
OUTRO["act"] = "outro"
OUTRO["kind"] = "outro_voice"
OUTRO["tail_silence_s"] = 1.0

BEATS = OPEN + BODY + [OUTRO]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "INFO 7375 · FINAL PROJECT PITCH",
    "skill": "show-tell", "style_preset": "show-tell",
    "channel": "revan-chonnad", "channel_title": NAME,
    "persona": "Revan C (first person, synthetic Kokoro voice)",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24,
    "aspect_ratio": "16:9", "width": 3840, "height": 2160, "caption_policy": "none",
    "greeting_language": "Spanish (Hola)",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Student pitch on the show-tell chassis: opens on the hesitant writer, then a plain-language beat instead of the terms card, "
                              "no verdict card, and no Claude.ai Your Turn composer (the film shows no Claude "
                              "interface or response). Outro is the student's own card, narrated as themselves."),
    "audience": "hiring managers and engineers at fintech and crypto companies; INFO 7375 reviewers",
    "source_doc": ("PROJECT-BRIEF.md (2026-10-14); Money Map, https://mit-dci.github.io/payments-dashboard/ "
                   "(viewed and screenshotted 2026-10-14); World Bank Remittance Prices Worldwide methodology and "
                   "US→Mexico corridor pages (viewed 2026-10-14); Wise and Monito checks by Revan (2026-10-14)"),
    "tags": ["Remnix", "remittances", "USD to MXN", "stablecoins", "source grounding", "evaluation", "INFO 7375"]},
    "beats": BEATS}

if __name__ == "__main__":
    (HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
    total = sum(b["estimated_duration_s"] for b in BEATS) + 1.0 + 0.8
    words = sum(len(b["narration_text"].split()) for b in BEATS)
    print(f"{len(BEATS)} beats; {words} words; est {total:.0f} s ({total/60:.1f} min)")
