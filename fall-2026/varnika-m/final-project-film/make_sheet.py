#!/usr/bin/env python3
"""make_sheet.py — writes beat_sheet.json for Varnika M's final project pitch film.

Show-tell style (brutalist.art skills/make/show-tell): one drawn picture per beat, labels of
one to three words, the voice explains. First person, as Varnika; no instructor persona,
greeting, handle or credit line (assignment rule), so the hesitant-writer, terms and Your Turn
bookends are exempt and the outro is a drawn Manim scene showing the title and her name.

Re-running this file DROPS measured durations; run it only before (re)voicing.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "varnika-final-project-pitch"
TITLE = "Terraform Docs, Quoted"
HANDLE = "Varnika M"
VOICE = "am_onyx"
SRC = "AWS provider v6.68.0 docs · fetched 2026-10-11"
SPARSE = ("show-tell: one drawn object or scene on a cream stage, minimal labels, the voice "
          "carries the explanation; only underfill and clustered are waived.")


def beat(bid, question, narration, cls, visual, labels, constructed, status="DRAFT", **extra):
    b = {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
         "question": question, "narration_text": narration, "narration_status": status,
         "estimated_duration_s": round(len(narration.split()) / 3.3, 1),
         "voice": VOICE, "engine": "kokoro",
         "qc": {"sparse_by_design": True, "sparse_reason": SPARSE},
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": visual, "motion_claim": visual,
                  "show": [{"at": 0.1, "event": visual}], "manim": {"class": cls},
                  "labels": labels, "constructed": constructed}}
    for k in ("source_tag", "evidence"):
        if k in extra:
            b["shot"][k] = extra.pop(k)
    b.update(extra)
    return b


B = [
 beat("B01", "1 · What is it",
      "I'm Varnika. My final project will be a tool that answers questions about Terraform from the official docs, and proves every answer with the exact line it came from.",
      "B01_Ask", "A question card slides onto a kraft docs page; one line on the page lights up and a check lands beside it.",
      ["question", "docs", "proof"], True),
 beat("B02", "1 · What exists when done",
      "When it's done, it will be a public GitHub repository: a Python command-line tool, a saved copy of the docs, a test suite, and an evaluation log.",
      "B02_Repo", "An open box (the repo) receives four parts one by one: a terminal block, a page stack, a test tray, a logbook.",
      ["GitHub repo", "planned"], True),
 beat("B03", "2 · Why care (real example)",
      "Here's a real example. You might guess that an S3 bucket's name is required. The AWS provider docs say it's optional: if you leave it out, Terraform picks a random, unique name.",
      "B03_Optional", "The docs page zooms to one line; a 'Required?' tag is crossed out and 'Optional' lands with a check.",
      ["bucket", "Optional", "line 54"], False,
      source_tag=SRC + " · aws_s3_bucket line 54", evidence="evidence/aws-provider-docs/s3_bucket.html.markdown:54"),
 beat("B04", "2 · Why care (things change)",
      "On the same page, versioning is marked deprecated, with a separate resource to use instead. Facts like these change between versions, so an answer is only useful if you can see which docs it came from.",
      "B04_Deprecated", "A second line on the same page gets a grey 'deprecated' stamp; an arrow points to a new small page.",
      ["versioning", "Deprecated", "line 70"], False,
      source_tag=SRC + " · aws_s3_bucket line 70", evidence="evidence/aws-provider-docs/s3_bucket.html.markdown:70"),
 beat("B05", "1 · How it will work",
      "It will work in three steps. Find the docs lines that match the question. Ask Claude to answer using only those lines, and to quote one. Then my code checks that the quote really exists in the docs before showing the answer.",
      "B05_Conveyor", "The question card rides a conveyor through three gates: find, answer, check. A scan line sweeps the quote at the last gate.",
      ["find", "answer", "check"], True),
 beat("B06", "2 · Why care (says when it doesn't know)",
      "If no line in the docs supports an answer, the tool will say: not in the docs. That counts as a correct answer, not a failure.",
      "B06_NotFound", "A question card reaches the check gate with no matching line; it is set down in an 'unanswered' tray, which gets a check.",
      ["not in the docs"], True),
 beat("B07A", "2 · Alternative 1: the docs site",
      "On October eleventh I tried two things. On the Terraform docs site, the answer is there. The page menu gets you to it, but searching the page for bucket found two hundred and twenty matches. The right one was number seventy.",
      "B07A_Registry", "A long docs page with a find box; the counter climbs to 70 / 220 while a marker steps down the page.",
      ["docs site", "70 / 220", "redrawn"], "redrawn from Varnika's real screenshots",
      status="APPROVED by Varnika 2026-10-11",
      source_tag="redrawn from my screenshot, registry.terraform.io, 2026-10-11",
      evidence="evidence/alternatives/2026-10-11_registry_cmdf-bucket-70-of-220.png"),
 beat("B07B", "2 · Alternative 2: asking Claude",
      "Then I asked Claude. It said optional, which is right, but it added two details that aren't on the docs page, and it didn't say which docs it used. My tool will answer from one stated version, and show the line.",
      "B07B_Chat", "A reply card: the 'optional' line gets a check; two lines get grey 'not on page' tags; then a planned answer card with one quoted line slides in beside it.",
      ["Claude reply", "not on page", "redrawn"], "redrawn summary of a real claude.ai reply; planned card constructed",
      status="APPROVED by Varnika 2026-10-11",
      source_tag="redrawn from my screenshot, claude.ai Sonnet 5.5, 2026-10-11",
      evidence="evidence/alternatives/2026-10-11_claude-ai_sonnet-5-5_answer_cropped.png"),
 beat("B08", "3 · Who opens it, first sixty seconds",
      "The role I'm aiming for is AI software developer, so the person I'm building this for is a hiring manager or engineer looking at my GitHub. In the first minute, they'll run one command with a question, see the answer with its quoted line, and then run the tests.",
      "B08_FirstMinute", "The repo box opens, a terminal block prints one answer line, then a test tray fills with checks while a clock hand sweeps one minute.",
      ["one command", "tests", "planned"], True),
 beat("B09", "4 · What it proves",
      "It's meant to show what this course teaches: a prompt contract, where Claude must reply in a fixed shape with an answer, a quote and a line number; source grounding; verification in code; and an evaluation that lists every miss. It won't prove the tool works on all of Terraform, only on the questions I test.",
      "B09_Proves", "Four evidence binders drop onto a shelf, one per skill; a fence line marks the edge of what was tested.",
      ["contract", "grounding", "verify", "evaluate"], True),
 beat("B10", "5 · In, out, first",
      "It covers about ten AWS resource pages at one pinned version. It will not write or run Terraform, and it never touches a cloud account. The first piece is the quote checker, and you'll know it runs when its tests pass offline, including one where a made-up quote is rejected.",
      "B10_Scope", "Ten pages stack inside a fence; a run button sits outside with an 'out' tag; the checker block lights first and a fake quote drops into a reject bin.",
      ["in", "out", "first"], True),
 beat("B11", "6 · Risk",
      "The risk I can already see: on the same page, bucket is optional at the top, but required inside the replication block. A search for the word bucket could pick the wrong line, and the quote would still be real. So I'll track which section every line belongs to, and put this exact case in my tests.",
      "B11_Risk", "The docs page splits into two sections; two 'bucket' lines light up, one tagged Optional at the top, one Required lower down; a divider drops between them.",
      ["line 54", "line 221"], False,
      source_tag=SRC + " · aws_s3_bucket lines 54 and 221", evidence="evidence/aws-provider-docs/s3_bucket.html.markdown:54,221"),
 beat("B12A", "7 · Why this project (already have)",
      "Why this project? It's a mix. I've used Python and Terraform on my co-op, and Terraform in a cloud computing course project. I've also built a small, tested Python tool with Claude Code: my last one, for the Reallocation Engine, has twenty-two offline tests, and I wrote down where it fell short.",
      "B12A_Have", "An 'already have' tray receives a Python block, a Terraform page and a test tray tagged 'PR #21 · 22 tests'.",
      ["already have", "PR #21 · 22 tests"], "drawing; PR #21 and its 22 tests are real",
      evidence="https://github.com/nikbearbrown/the-reallocation-engine/pull/21 (open, head 8b79712, checked 2026-10-11)"),
 beat("B12B", "7 · Why this project (new)",
      "What's new to me is finding the right section of a long document, and building a test set to score the answers.",
      "B12B_New", "A 'new to me' tray receives a long page with one section highlighted and a scored question sheet.",
      ["new to me"], True),
 beat("B13", "Exists today vs will exist",
      "What exists today: a licence check, one saved docs page pinned to version six point sixty-eight, and my two tests from October eleventh. The tool itself is still a plan.",
      "B13_Ledger", "Two shelves: 'today' holds one page, a licence slip and two test cards; 'will exist' holds the outlined, empty shapes of the repo parts from B02.",
      ["today", "will exist"], False, evidence="evidence/"),
]
B.append(beat("BOUT", "Outro", f"{TITLE}. {HANDLE}.", "BOUT_Title",
              "Title and name on the cream stage, beside the docs page and its check from B01.",
              [TITLE, HANDLE], False, tail_silence_s=1.0))
B[-1]["shot"]["remotion"] = {"props": {"title": TITLE, "handle": HANDLE, "subline": ""}}
B[-1]["shot"]["outro_note"] = ("Drawn in Manim (BOUT_Title), not the ClaudeTitleOutro component, which hard-codes the "
                               "instructor's handle. These props record exactly the title and name the scene shows, "
                               "so bookend_check.py can verify them.")

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "INFO 7375 · FINAL PROJECT PITCH",
    "skill": "show-tell", "style_preset": "show-tell",
    "channel": "varnika-m", "channel_title": HANDLE, "author": "Varnika M", "course": "INFO 7375",
    "persona": "Varnika M (first person)", "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro",
    "voice_reason": ("Varnika chose a computer voice on 2026-10-11, then asked to reuse her Week 01 voice, Kokoro am_onyx. "
                     "The toolkit also uses am_onyx for the instructor's 'Liam, in for Bear' narrator; this film uses only "
                     "the stock voice, with no Liam name, greeting, or @NikBearBrown outro."),
    "clock": "narration", "palette": "claude", "register": "Plain",
    "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160, "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
    "bookend_exempt_reason": ("The hesitant writer, terms card and Your Turn composer carry the instructor's narrator and "
                              "channel identity, which this student film may not show (assignment: narrate as yourself; "
                              "no instructor name, persona or credit line). B01 is the hook. BOUT is kept, drawn in Manim "
                              "with the film title and Varnika's name."),
    "constructed_rule": ("Drawings of anything that does not exist yet carry a 'planned' label. Real docs lines carry a "
                         "source tag. B07A and B07B redraw Varnika's real 2026-10-11 screenshots and say 'redrawn'; the "
                         "screenshots themselves are in evidence/alternatives/."),
    "claude_output_rule": ("B07B summarises one real claude.ai reply (Sonnet 5.5, 2026-10-11), redrawn and dated on screen. "
                           "No other Claude reply is shown."),
    "audience": "a hiring manager or engineer reviewing Varnika's GitHub; the INFO 7375 graders",
    "source_doc": "PROJECT-BRIEF.md; evidence/",
    "tags": ["Terraform", "AWS provider", "source grounding", "verification", "Claude", "Python"]},
    "beats": B}

(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
words = sum(len(b["narration_text"].split()) for b in B)
print(len(B), "beats;", words, "words; est", round(words / 201 * 60), "s at the Week 01 am_onyx rate")
