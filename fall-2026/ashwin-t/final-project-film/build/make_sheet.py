#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for the TraceCase pitch film (INFO 7375 final project pitch).

Replaces the ProvenDocs film of 2026-10-11 (why: FRICTIONAL.md, 2026-10-13).

Built on Brutalist's show-tell skill: one drawn isometric picture per beat, minimal labels,
the narration carries the explanation. Two deliberate departures from the skill, because the
assignment governs ("Narrate as yourself. Do not use the instructor's name, persona, or credit
line"): the narrator is me (Ashwin), first person; the outro handle is my name.

Honesty rule: nothing of TraceCase exists yet. Every body beat that pictures the product is a
sketch and carries an on-screen "constructed" tag. Every sentence about the product says "will".
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "tracecase-pitch"
TITLE = "TraceCase: An Agent That Finds Out Why"
VOICE = "am_michael"
HANDLE = "Ashwin Thankachan"


def beat(bid, narration, cls, image, show, sparse=True):
    b = {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.4, 1),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                  "manim": {"class": cls}, "motion_claim": image}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE_REASON}
    return b


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.4, 1),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show,
                  "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


SPARSE_REASON = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, "
                 "the voice carries the explanation. Only underfill and clustered are waived; edge-bleed, "
                 "empty-frame and contrast still apply.")

# ── body: one beat per idea, in the order of the assignment's seven questions ──────────────
# Cast kept for the whole film: the SERVICE (dark server stack, light turns terracotta when it
# breaks), LOG pages, the TRACE (horizontal span bars), the AGENT (a magnifying glass), the
# PROPOSAL card, and the GATE (a barrier arm that lifts only on approval).
BODY = [
    # Q1 — what is it, and what exists when it is done
    beat("B00",
         "It's called TraceCase, and it isn't built yet. It will read a small Spring Boot service's logs, traces, and deploy history, and propose one fix. A person must approve that fix before it runs.",
         "B00_WhatItIs",
         "A server stack sits left with a terracotta warning light; three sources (log page, trace bars, deploy "
         "timeline) appear beside it; a magnifying glass passes over them; a proposal card slides right and stops "
         "at a closed barrier arm.",
         [{"at": 0.15, "event": "service + name"}, {"at": 0.45, "event": "logs, traces, deploys"},
          {"at": 0.7, "event": "proposal card"}, {"at": 0.88, "event": "stops at the gate"}]),
    beat("B01",
         "When it's done, it will be one public repo: the demo service, the agent, an approval screen, failures I can trigger on purpose, and an evaluation report.",
         "B01_Repo",
         "An open repo box; five objects rise out of it one by one: server, magnifier, approval page, a red switch, report bars.",
         [{"at": 0.2, "event": "open box"}, {"at": 0.45, "event": "service, agent"}, {"at": 0.7, "event": "approval, switch"},
          {"at": 0.88, "event": "report"}]),
    # Q2 — why anyone would care, and the alternatives
    beat("B02",
         "My Cloud Pulse team project answered one question: is the service healthy? When the answer is no, an engineer still digs through logs by hand, under pressure, to find out why.",
         "B02_Why",
         "A health light goes from grey to terracotta; log pages pile up beside it; a cursor digs through them; a "
         "large question mark appears.",
         [{"at": 0.25, "event": "health light turns red"}, {"at": 0.6, "event": "pile of logs"}, {"at": 0.85, "event": "why?"}]),
    beat("B03",
         "Holmes G P T, an open-source agent, already investigates incidents, and asks a person before any change. Microsoft's A I Ops Lab evaluates agents like this, on Kubernetes. Or you dig by hand.",
         "B03_Alternatives",
         "Three plinths in a row, each with one object: a magnifier with a small approve gate, a lab flask on a cluster, a "
         "dashboard page with a cursor.",
         [{"at": 0.25, "event": "HolmesGPT"}, {"at": 0.55, "event": "AIOpsLab"}, {"at": 0.85, "event": "by hand"}]),
    beat("B04",
         "TraceCase will be smaller, and easy to check. It will run on a laptop with no Kubernetes, come with its own service to break, and every claim must point to a real log line or trace.",
         "B04_Different",
         "A fourth plinth: TraceCase. A claim card with a leader line pinned to one trace span; then a barrier arm "
         "that stays down when the card is swapped.",
         [{"at": 0.3, "event": "claim pinned to evidence"}, {"at": 0.75, "event": "gate stays shut on a mismatch"}]),
    # Q3 — who opens it, first sixty seconds
    beat("B05",
         "A hiring manager for a backend role. In the first minute, they'll start the demo, break it with one command, watch the agent investigate, and approve or reject its fix.",
         "B05_FirstMinute",
         "A terminal block; a switch flips and the service light turns terracotta; step cards appear one by one; a "
         "pair of approve / reject pills, the cursor clicks approve.",
         [{"at": 0.3, "event": "start + break"}, {"at": 0.6, "event": "steps"}, {"at": 0.85, "event": "approve / reject"}]),
    # Q4 — what it proves, tied to the course
    beat("B06",
         "What will it show about me? First, a loop with a budget. Observe, pick a tool, record the evidence, update the guess. It stops on a supported cause, or at a limit. Never because the model says it's done.",
         "B06_Loop",
         "Four stations on a ring (observe, tool, record, update); a terracotta dot travels the ring; a budget "
         "meter beside it drains with each lap; three exit doors light up one at a time.",
         [{"at": 0.2, "event": "ring"}, {"at": 0.5, "event": "dot loops, budget drains"}, {"at": 0.8, "event": "three exits"}]),
    beat("B07",
         "Second, control. Each step must match a fixed format, a prompt contract that code checks. Tools come from an allow-list, never a shell. And a claim citing evidence that doesn't exist is rejected.",
         "B07_Grounding",
         "A short menu card of three safe actions with a lock; a shell prompt block is crossed out; then two claim "
         "slips: one pinned to a real span gets a check, one pinned to nothing gets a cross.",
         [{"at": 0.3, "event": "allow-list menu, shell crossed out"}, {"at": 0.7, "event": "real citation ✓"},
          {"at": 0.9, "event": "missing citation ✗"}]),
    beat("B08",
         "Third, a human gate. The approval records the exact action, its target, and its evidence. If any of those change, it stops counting.",
         "B08_Gate",
         "An approval card with three fields and a seal; the barrier lifts; then one field changes, the seal breaks "
         "and the barrier drops again.",
         [{"at": 0.3, "event": "card fields"}, {"at": 0.6, "event": "gate lifts"}, {"at": 0.85, "event": "field changes, gate drops"}]),
    beat("B09",
         "Fourth, evaluation. About thirty failure scenarios, ten locked away before I tune anything, against a summarize-the-logs baseline. I'll count right answers, honest I-don't-knows, and unsupported claims. I have no numbers yet.",
         "B09_Eval",
         "Thirty small tiles drop into a grid; ten of them slide into a locked box; a big hero counter reads '? / 10' "
         "because nothing has been measured.",
         [{"at": 0.2, "event": "thirty tiles"}, {"at": 0.45, "event": "ten locked away"}, {"at": 0.85, "event": "? / 10"}]),
    beat("B10",
         "The demo will be realistic: a Spring Boot API and a worker, Postgres, and Redis as a cache and a queue, so there are real failures to find, like a stale cache. Open Telemetry traces will tie it together.",
         "B10_Stack",
         "API and worker stacks, a Postgres cylinder, a dark Redis block between them; a queue of small crates backs "
         "up into the Redis block; one trace line threads through every part.",
         [{"at": 0.2, "event": "API, worker, Postgres"}, {"at": 0.45, "event": "Redis"}, {"at": 0.7, "event": "queue backs up"},
          {"at": 0.9, "event": "trace threads through"}]),
    # Q5 — in, out, first
    beat("B11",
         "In scope: one demo service, and failures I design. That's also my honest limit: it won't prove anything about real production systems. And it never runs arbitrary commands.",
         "B11_Boundary",
         "A fenced square holds the service; a terminal prompt outside the fence is crossed out.",
         [{"at": 0.3, "event": "fence + service"}, {"at": 0.75, "event": "outside crossed out"}]),
    beat("B12",
         "The first piece: the demo with one failure I can trigger, and a trace that shows it. A saved trace and a dated log will prove it ran.",
         "B12_FirstPiece",
         "A service with a switch; the switch flips and one span on a trace waterfall turns terracotta; a dated log "
         "page slides underneath.",
         [{"at": 0.3, "event": "switch flips"}, {"at": 0.6, "event": "red span in trace"}, {"at": 0.85, "event": "dated log"}]),
    # Q6 — what could sink it
    beat("B13",
         "The biggest risk is approving one thing and running another. So I'll trigger it on purpose. Approve fix A, swap in fix B, and the system must refuse until a person looks again.",
         "B13_Swap",
         "Card A is approved (seal); a hand-off swaps it for card B; the barrier stays down and a cross lands on B.",
         [{"at": 0.3, "event": "A approved"}, {"at": 0.6, "event": "swap to B"}, {"at": 0.85, "event": "refused"}]),
    # Q7 — why this project
    beat("B14",
         "Why this project? Mostly to learn. The jobs I apply for ask for agents, observability, and evaluation, and my resume doesn't show them yet. I'm building on Spring Boot work from Cloud Pulse, and language-model services from my My Ed Master internship.",
         "B14_Shelves",
         "Two shelves: 'new' holds ghosted outline blocks; 'built before' holds solid blocks that land one by one.",
         [{"at": 0.3, "event": "new shelf"}, {"at": 0.75, "event": "built-before blocks land"}]),
    # exists vs will exist
    beat("B15",
         "Where it stands today: a written brief, and this film. No TraceCase code exists yet. Everything else you saw, I will build by December.",
         "B15_ExistsWill",
         "Two trays: 'exists' holds a page and a film frame; 'will exist' holds a ghosted server outline.",
         [{"at": 0.3, "event": "exists tray"}, {"at": 0.7, "event": "will-exist ghost"}]),
]

OPEN = [
    remotion("BIDEA", "the question",
             "Hi, I'm Ashwin. When a service breaks, a dashboard tells you that something is wrong. It doesn't tell you why. So I want to build an agent that finds out, shows its evidence, and lets a person decide what happens next.",
             "BrutalistHesitantWriter",
             {"text": "Monitor: is it down?", "triggerWords": "is it down",
              "replacementWords": "why is it down",
              "fontSize": 70, "charMs": 26, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2,
              "jitter": 20, "seed": SLUG, "banner": ""},
             [{"at": 0.0, "event": "types 'Monitor: is it down?'"},
              {"at": 0.6, "event": "backspaces 'is it down?' → 'why is it down?'"}],
             lead_silence_s=0.8,
             motion_claim="The writer types the monitoring question and corrects it to the real one: why.",
             qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
]

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": f"{TITLE}. A pitch by {HANDLE}.", "estimated_duration_s": 4.0,
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; my name"}],
                  "remotion": {"pattern": "ClaudeTitleOutro",
                               "props": {"title": TITLE, "slug": SLUG, "handle": HANDLE, "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

BEATS = OPEN + BODY + [OUTRO]

# Carry forward measured audio fields if the sheet already exists (re-running must not wipe them),
# but only while the narration is unchanged.
old = {}
p = HERE / "beat_sheet.json"
if p.exists():
    for b in json.loads(p.read_text())["beats"]:
        old[b["beat_id"]] = b
for b in BEATS:
    o = old.get(b["beat_id"])
    if o and o.get("narration_text") == b["narration_text"]:
        b.update({k: o[k] for k in ("actual_duration_s", "audio_file") if k in o})

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "FINAL PROJECT · PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "ashwin-t", "channel_title": HANDLE, "persona": "Ashwin Thankachan (first person)",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9",
    "width": 3840, "height": 2160, "caption_policy": "none", "greeting_language": "English (Hi)",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Course pitch film, not a channel reel: opens on the hesitant writer per show-tell; "
                              "no verdict card; no Your Turn (the assignment asks for a pitch, not a viewer exercise). "
                              "Narrated as myself with my own name on the outro, as the assignment requires."),
    "audience": "INFO 7375 instructor and TAs; backend engineering hiring managers",
    "source_doc": "PROJECT-BRIEF.md (2026-10-13); HolmesGPT and AIOpsLab public pages (read 2026-10-13)",
    "playlist": "INFO 7375 Final Project", "chapter_number": 0,
    "tags": ["TraceCase", "pitch", "agent", "OpenTelemetry", "Redis", "Spring Boot", "INFO 7375"]},
    "beats": BEATS}
p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
words = sum(len(b["narration_text"].split()) for b in BEATS)
print(len(BEATS), "beats;", words, "words; est", round(sum(b["estimated_duration_s"] for b in BEATS)), "s")
