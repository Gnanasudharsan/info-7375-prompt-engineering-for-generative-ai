#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for rithika-final-project-pitch (show-tell).

INFO 7375 final-project pitch film for "Agentic Retrieval Lab", by Rithika Sankar Rajeswari.
Show-tell: every beat is ONE drawn isometric Manim illustration on the same cast (the library,
two librarian carts, the robot, the answer key, decoy books, the pile). Bella narrates in the
first person, as Rithika.

`script_text` is Rithika's approved wording, verbatim. `narration_text` is what Kokoro voices:
identical except for the pronunciation respellings listed in PRONUNCIATION (audio only;
on-screen labels keep the standard spelling).

Audio: generate_audio_kokoro.py <reel> --speed 1.04, then pad BOUT with a 1.0 s silent tail.
Re-running this file rewrites beat_sheet.json from scratch and DROPS measured audio fields;
run generate_audio_kokoro.py (and pad BOUT) again afterwards.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "rithika-final-project-pitch"
TITLE = "Agentic Retrieval Lab"
HANDLE = "Rithika Sankar Rajeswari · github.com/rithika-sr"
VOICE = "af_bella"
WPS = 2.86   # af_bella, measured 2026-10-10 on the beat-6 draft (65 words / 22.7 s)

# audio-only respellings (Rithika's list). Applied in order to script_text → narration_text.
PRONUNCIATION = [
    ("BM25", "B M twenty-five"),
    ("MS MARCO", "M S Marco"),
    ("Q2D-Web", "Q two D Web"),
    ("8.8 million", "eight point eight million"),
    ("LLM", "L L M"),
]


# per-beat, audio-only rewrites approved by Rithika (2026-10-10): Kokoro slurred "agent-written".
NARRATION_ONLY = {"B04": [("agent-written", "agent written")],
                  "B13": [("AI and ML", "A-I and M-L"), ("RAG", "rag")]}   # Rithika, 2026-10-11 ("A I and M L" slurred to "a I&M L" in whisper; hyphens voice cleanly)
SPEED = 1.04   # Rithika, option B (2026-10-10): voice speed for the 3:55 cap. Pass --speed 1.04 to generate_audio_kokoro.py.


def spoken(text, bid=None):
    for a, b in PRONUNCIATION:
        text = text.replace(a, b)
    for a, b in NARRATION_ONLY.get(bid, []):
        text = text.replace(a, b)
    return text


SPARSE = ("show-tell style: one drawn scene on a cream stage per beat, labels only, the voice carries "
          "the explanation. The negative space is the style, so only underfill and clustered are waived; "
          "edge-bleed, empty-frame and contrast still apply.")


def beat(bid, script, cls, image, show, constructed=False, sparse=True):
    b = {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
         "script_text": script, "narration_text": spoken(script, bid),
         "estimated_duration_s": round(len(script.split()) / WPS / SPEED, 1),
         "voice": VOICE, "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show,
                  "manim": {"class": cls}, "motion_claim": image}}
    if constructed:
        b["constructed"] = True
        b["constructed_note"] = "Shows something that does not exist yet, or an invented example; carries an on-screen CONSTRUCTED label."
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}
    return b


B = [
 beat("B01",
  "Picture asking a question online. More and more, an AI assistant does the searching for you. But it doesn't type your question. It rewrites it into several searches of its own. My project asks one thing: when the AI writes the search, does the right answer still come back?",
  "B01_Hook",
  "A search box; a cursor types one question as a speech bubble. The robot rolls in; the bubble splits into four smaller bubbles that fly toward the library shelves.",
  [{"at": 0.1, "event": "search box + one bubble ('one question')"}, {"at": 0.4, "event": "robot arrives"},
   {"at": 0.6, "event": "bubble splits into four ('four searches')"}, {"at": 0.85, "event": "bubbles fly to the shelves"}]),
 beat("B02",
  "A search step has to find the right page among millions, like a librarian pulling a hundred books off the shelves. If the right book isn't in that pile, the AI never sees it.",
  "B02_Pile",
  "Endless isometric shelves ('8.8M books'); a librarian cart carries a pile to the desk where the robot waits ('top 100'); the glowing right book is left behind on a shelf.",
  [{"at": 0.1, "event": "shelves stretch back"}, {"at": 0.4, "event": "pile lands on the desk"}, {"at": 0.75, "event": "the glowing book stays on the shelf"}]),
 beat("B03",
  "There are two kinds of librarian. One matches your exact words; it's called BM25. The other matches meaning, using an AI model called an embedding.",
  "B03_Librarians",
  "Two librarian carts side by side: the magnifying glass sweeps over a book with the same words; the lightbulb lights a book with different words but the same meaning.",
  [{"at": 0.2, "event": "two carts"}, {"at": 0.35, "event": "magnifier matches 'same words'"}, {"at": 0.7, "event": "bulb lights 'same meaning'"}],
  constructed=True),
 beat("B04",
  "I'm Rithika, and this is Agentic Retrieval Lab. When it's done, it will be a public GitHub repository: a Python pipeline, tests, dated result files, and a short write-up of where search fails. \"Agentic\" here means agent-written queries. I'm not building an autonomous agent.",
  "B04_Repo",
  "A repository cabinet with three drawers (pipeline, tests, results) that slide open one by one.",
  [{"at": 0.15, "event": "cabinet"}, {"at": 0.4, "event": "drawers open one by one"}]),
 beat("B05",
  "Some of it already exists. This week I took 300 real search questions from the public MS MARCO dataset, had Claude Haiku rewrite each into four agent-style searches, indexed all 8.8 million passages, and built a 200,000-passage test set. 103 tests pass.",
  "B05_Built",
  "Four blocks drop in and stack (300 questions, 1,200 rewrites, 8.8M passages, 103 tests); a check lands on '103 tests'; small label 'built Oct 5–9, 2026'.",
  [{"at": 0.15, "event": "300 questions"}, {"at": 0.35, "event": "1,200 rewrites"}, {"at": 0.6, "event": "8.8M passages"},
   {"at": 0.85, "event": "103 tests + check"}]),
 beat("B06A",
  "My first result: the keyword librarian found the right passage in its top 100 for 64 percent of human questions and 60 percent of main rewrites, but only 42 percent of support searches.",
  "B06A_Bars",
  "Three bars grow to 64%, 60% and 42% (human, main rewrite, support); a question mark pops over the 42% bar.",
  [{"at": 0.25, "event": "64%"}, {"at": 0.5, "event": "60%"}, {"at": 0.75, "event": "42% + question mark"}], sparse=False),
 beat("B06B",
  "I don't trust that drop yet. The answer key usually lists just one correct book per original question, so a support search can find a good book and still be marked wrong.",
  "B06B_AnswerKey",
  "The robot hands over a good book; the answer-key clipboard has one tick per question and marks this book with a question mark instead of a check.",
  [{"at": 0.2, "event": "answer key, one tick per question"}, {"at": 0.55, "event": "robot hands over a good book"}, {"at": 0.85, "event": "marked: question mark"}],
  constructed=True),
 beat("B07",
  "I looked at two alternatives. Perplexity's Q2D-Web paper studies agent searches over 190 million documents, but its data is private; the public gets a leaderboard, not the data. MS MARCO is public, but its questions are written by humans, with about one answer each.",
  "B07_Alternatives",
  "A big vault labelled Q2D-Web whose locking bar slides shut ('private'); a small open box labelled MS MARCO whose lid opens to handwritten question slips ('human-written').",
  [{"at": 0.25, "event": "vault locks"}, {"at": 0.7, "event": "box opens, handwritten slips"}]),
 beat("B08",
  "That paper found something surprising: on its main measure, the keyword librarian scores lowest, yet finds the most books no one else finds. It suggests testing whether the two work better as a team. My project will run that test at small scale, on public data, on one laptop, with every number traceable to a file.",
  "B08_Team",
  "The two carts side by side; the keyword cart adds books the other missed to a shared pile ('team up?'). Then a laptop: an arrow traces from a number to a file ('traceable').",
  [{"at": 0.15, "event": "keyword cart adds unique books"}, {"at": 0.4, "event": "team up?"}, {"at": 0.75, "event": "laptop: number → file"}]),
 beat("B09",
  "The person opening it is a hiring manager for ML or AI engineering roles. In the first minute, they'll read the results table, click one number through to its source file, and see one command that reruns the tests. Today that table is still empty.",
  "B09_Reader",
  "A README window seen from the reader's side with a 60-second timer; three steps light up in turn (table, number → file, one command); the table is still empty.",
  [{"at": 0.2, "event": "window + timer starts"}, {"at": 0.45, "event": "step 1 table"}, {"at": 0.6, "event": "step 2 number → file"},
   {"at": 0.75, "event": "step 3 command"}, {"at": 0.9, "event": "the table is empty"}],
  constructed=True),
 beat("B10",
  "A reviewer should conclude that I can design a fair test, ground every number in a file, and check a pipeline with tests. Not that I've shipped a production system.",
  "B10_Badges",
  "Three badges stamp on (fair test, sourced numbers, checked code); a fourth, 'production RAG', fades and is struck through.",
  [{"at": 0.15, "event": "fair test"}, {"at": 0.35, "event": "sourced numbers"}, {"at": 0.55, "event": "checked code"}, {"at": 0.8, "event": "production RAG struck"}]),
 beat("B11",
  "In scope: meaning models versus keyword search, human versus agent searches, the team-up test, and a hand-written failure analysis. Out: a chatbot, or writing answers. First, I'll race one meaning model against the keyword librarian. I'll know it ran when a new dated results folder appears and the keyword score matches its earlier run.",
  "B11_Scope",
  "An 'in' tray and an 'out' tray; items sort into them; then an arrow marked 'first' points at the meaning cart racing the keyword cart, and a dated results folder appears.",
  [{"at": 0.1, "event": "in-tray items"}, {"at": 0.35, "event": "out-tray items"}, {"at": 0.5, "event": "race (first)"}, {"at": 0.8, "event": "dated folder"}]),
 beat("B12",
  "What could sink it: in my test set, the decoys the keyword librarian picked average about 65 words, and the correct passages about 54. A librarian who simply grabs short books could look smarter than it is. So first, I'll test a lazy librarian that only picks short passages. If it beats random, I'll fix the test set before trusting any ranking.",
  "B12_Decoys",
  "A balance scale: a thick grey decoy book (65 words) against a thin correct book (54 words); the scale tips. A lazy cart grabs only thin books; its score bar rises suspiciously; a check stamp lands: test it first.",
  [{"at": 0.15, "event": "scale tips"}, {"at": 0.45, "event": "lazy cart grabs thin books"}, {"at": 0.65, "event": "suspicious bar"}, {"at": 0.85, "event": "test-first stamp"}],
  constructed=True),
 beat("B13",
  "Why this project? I'm aiming for AI and ML engineering or data science roles, and I'm especially interested in RAG systems: retrieval, generation, and evaluation. It's mostly learning, built on data-engineering skills I already use. New to me: retrieval metrics, embedding models, and using an LLM as a judge.",
  "B13_Learning",
  "Two piles, 'already have' and 'learning'; blocks move from 'learning' toward 'already have' as a progress bar fills.",
  [{"at": 0.3, "event": "two piles"}, {"at": 0.6, "event": "blocks move across"}, {"at": 0.8, "event": "progress fills"}]),
]

# Beat 14 is the outro (Rithika's decision, option B, 2026-10-10): drawn in Manim, no added narration.
CLOSE = "Everything I said in the past tense, you can open today. Everything else is a plan, and I'll log every change as I go."
bout = beat("BOUT", CLOSE, "BOUT_Close",
            "Two columns: solid checks under 'exists', dotted outlines under 'will' that pulse gently; the title and Rithika's handle sit beneath.",
            [{"at": 0.2, "event": "exists column"}, {"at": 0.5, "event": "will column pulses"}, {"at": 0.7, "event": "title + handle"}])
bout["act"] = "outro"
bout["shot"]["remotion"] = {"props": {"title": TITLE, "handle": HANDLE, "subline": ""}}   # read by bookend_check; no pattern → nothing renders in Remotion
bout["tail_silence_s"] = 1.0
bout["outro_note"] = ("Rithika, 2026-10-10 (option B): beat 14 is the outro, drawn in Manim with her own title and handle. "
                      "The stock ClaudeTitleOutro hard-codes the instructor's channel handle and the Claude mascot, which this student film may not carry. "
                      "No narration was added; the 1.0 s silent tail is padded onto the mp3 after generation.")
B.append(bout)

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "INFO 7375 · FINAL PROJECT PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "rithika-sr", "channel_title": HANDLE, "persona": "Rithika Sankar Rajeswari (first person)",
    "author": "Rithika Sankar Rajeswari", "course": "INFO 7375",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro", "kokoro_speed": SPEED,
    "voice_reason": ("Rithika's rule 4 (2026-10-10): Kokoro af_bella, first person, as her. The skill's LIAM BY DEFAULT law "
                     "(am_onyx, with an instructor greeting) belongs to the instructor's channel; this film carries no instructor identity."),
    "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "caption_reason": "Rithika chose to skip captions; the compiler has no burn-in step.",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("Rithika, 2026-10-10: the hesitant writer, key terms card and Your Turn composer are skipped. "
                              "(1) Runtime: the pitch has a hard 4:00 maximum and her narration alone measures about 3:40, so ~40 s of "
                              "bookends would push it over. (2) Branding: those components carry the instructor's identity "
                              "(the instructor's narrator greeting and channel handle on the folder labels), which this student film may not show. "
                              "(3) Beats 1-3 already do their jobs: beat 1 is the hook/question, beats 2-3 define the terms. "
                              "The outro is never exempt: beat 14 is BOUT, drawn in Manim with her own title and handle."),
    "people_rule": ("Cartoon people authorised by Rithika (2026-10-11): generic flat figures drawn in Manim (ME/Rithika, keyword librarian = BM25, meaning librarian = embedding, lazy librarian, searcher, reviewer). No portrait, likeness or name of the instructor; the toolkit's portrait house rule does not apply to this student film. The robot stays the AI agent."),
    "constructed_rule": "Beats flagged constructed=true carry an on-screen CONSTRUCTED label (B03, B06B, B09, B12).",
    "pronunciation": [{"written": a, "spoken": b} for a, b in PRONUNCIATION] + [{"beat": k, "written": a, "spoken": b} for k, v in NARRATION_ONLY.items() for a, b in v],
    "audience": "complete beginners and the INFO 7375 grader; hiring managers later",
    "source_doc": "~/agentic-retrieval-lab (README.md, results/foundation/, git log; read-only); Schall et al. 2026 arXiv:2609.08887v2",
    "playlist": "INFO 7375 final projects", "tags": ["retrieval", "RAG", "BM25", "embeddings", "MS MARCO", "agentic search"]},
    "beats": B}
(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(B), "beats; est", round(sum(b["estimated_duration_s"] for b in B)), "s")
