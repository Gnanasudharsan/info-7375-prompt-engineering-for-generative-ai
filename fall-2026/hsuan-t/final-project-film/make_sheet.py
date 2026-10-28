import json
from pathlib import Path

HERE = Path(__file__).parent
SLUG = "final-project-pitch"
TITLE = "The Reallocation Engine Pitch"

def card_beat(bid, narration, kind, heading, sub, word, show, **custom_props):
    card_props = {
        "kind": kind,
        "heading": heading,
        "sub": sub,
        "word": word,
        "onTwos": True
    }
    card_props.update(custom_props)
    return {
        "beat_id": bid,
        "act": "show-tell",
        "lane": "card",
        "proof_gate": "SHOW",
        "narration_text": narration,
        "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
        "voice": "am_puck",
        "engine": "kokoro",
        "shot": {
            "type": "REMOTION",
            "source": "own",
            "show": show,
            "remotion": {
                "pattern": "ShowTellCard",
                "props": card_props
            }
        }
    }

CONSTRUCTED = "CONSTRUCTED MOCK-UP"
REAL_0410 = "REAL OUTPUT · role-scores.md · 2026-10-04"

B = [
    card_beat("B01", "When it's done, it will be a CLI that an F-1 STEM OPT job seeker opens with a job link, and it will score SWE, DevOps and QA roles with a clear Apply or Skip. What exists today is a prototype recipe: on October fourth it scored three test roles against the DOL and SEC file.",
              "search", "tisaac-swe-stem-opt · 3 test roles", "", "",
              [{"at": 0.2, "event": "type"}, {"at": 0.6, "event": "results"}],
              stamp=REAL_0410,
              items=[
                  {"label": "1LIFE HEALTHCARE INC — Software Engineer", "sub": "Apply · 0.580 · sponsorship [record]", "value": ""},
                  {"label": "Isaac Super Fake Tech LLC — Software Engineer", "sub": "Apply · 0.300 · sponsorship [no-matched]", "value": ""},
                  {"label": "Non-ATS Startup — Software Engineer", "sub": "Skip · -0.300 · liveness gate [record]", "value": ""}
              ]),

    card_beat("B02", "I tried ChatGPT for this first. I had to ask about one company at a time, and every answer still had to be checked by hand. This tool will turn that check into a fixed script: sponsorship will come straight from government records: the Labor Department's visa filings and the SEC's funding filings. AI will only do what it's good at, reading the job description.",
              "tabs", "ChatGPT vs This Tool", "One by one vs one script", "",
              [{"at": 0.40, "event": "tab switches from ChatGPT to the planned tool"}],
              stamp=CONSTRUCTED,
              labels=["ChatGPT (tried)", "Tool (will)"],
              cues=[0.40],
              durationSeconds=18.0,
              items=[
                  {"label": "Companies per chat", "value": "One", "sub": ""},
                  {"label": "Answer checked", "value": "By hand", "sub": ""},
                  {"label": "Same steps each time", "value": "No", "sub": ""}
              ],
              items2=[
                  {"label": "DOL H-1B Filings", "value": "15 Approved", "sub": ""},
                  {"label": "SEC Form D (Series B)", "value": "$24M Raised", "sub": ""},
                  {"label": "AI's only job", "value": "Read JD", "sub": ""}
              ]),

    card_beat("B03", "An F-1 student will run the CLI with a job URL. The pipeline will extract and clean the company, title and description, and the student will get a decision in under a minute.",
              "workspace", "Job Extraction Pipeline", "Paste URL -> Decision (planned)", "",
              [{"at": 0.2, "event": "workspace expands"}],
              stamp=CONSTRUCTED,
              items=[
                  {"label": "1. Extract", "value": "", "sub": ""},
                  {"label": "2. Clean", "value": "", "sub": ""},
                  {"label": "3. Score", "value": "", "sub": ""}
              ]),

    card_beat("B04", "It will prove I can build AI workflows that check facts against real data: prompt contracts, rules that stop the AI from making things up; gates that drop bad jobs early; and tests that measure how often it decides right.",
              "paths", "Source-Grounded Workflows", "Prompt Contracts · Eval", "",
              [{"at": 0.2, "event": "paths connect data to AI"}],
              stamp=CONSTRUCTED,
              items=[
                  {"label": "Job URL", "value": "", "sub": ""},
                  {"label": "Phase Gates", "value": "", "sub": ""},
                  {"label": "Decision", "value": "", "sub": ""},
                  {"label": "DOL & SEC", "value": "", "sub": ""},
                  {"label": "Eval Suite", "value": "", "sub": ""}
              ]),

    card_beat("B05", "It will include a lightweight duplicate tracker, but it will deliberately not be an auto-apply bot. The first piece I will make run is the sponsor lookup against H-1B filing records.",
              "stack", "Project Scope", "Sponsor Lookup", "",
              [{"at": 0.2, "event": "stack of features"}],
              stamp=CONSTRUCTED,
              items=[
                  {"label": "Sponsor Lookup", "value": "FIRST (Core)", "sub": ""},
                  {"label": "Hash Deduplication", "value": "NEXT (UX)", "sub": ""},
                  {"label": "Auto-Apply Bot", "value": "OUT OF SCOPE", "sub": ""}
              ]),

    card_beat("B06", "What could sink it: company names. A posting says Toast, but the filing file has Toast Inc, Toast Holdings and Moontoast. A wrong match means a wrong verdict. So I will confirm each legal name myself, and when a name doesn't match, the tool will hold the role instead of scoring it.",
              "dashboard", "Posting says \"Toast\": which legal name?", "Names with TOAST in the DOL/SEC file", "9 name matches",
              [{"at": 0.2, "event": "drops in the candidate legal names"}],
              stamp="REAL CSV ROWS · LAYOUT CONSTRUCTED",
              items=[
                  {"label": "TOAST INC", "value": "CHECK", "sub": "150 H-1B approvals · Form D: $38.2M raised"},
                  {"label": "TOAST HOLDINGS INC", "value": "HOLD", "sub": "No H-1B approvals · Form D: $9.7M raised"},
                  {"label": "MOONTOAST INC", "value": "HOLD", "sub": "No H-1B approvals · Form D: $1.7M raised"}
              ]),

    card_beat("B07", "Why this project: I face this check myself on every application, and I used to trust AI answers blindly. My friction logs and source tags already show how I check AI work; next, I will learn to replace prompt-pasting with strict verification gates.",
              "focus", "Audit Trail & Provenance", "Friction Logs · Source Tags", "",
              [{"at": 0.2, "event": "lens focuses on model judgment"}],
              stamp="REAL OUTPUT · 2026-10-04",
              items=[
                  {"label": "[record] sponsorship", "value": "0.8", "sub": ""},
                  {"label": "[model-judgment] fit", "value": "1", "sub": ""},
                  {"label": "[no-matched] sponsorship", "value": "0", "sub": ""},
                  {"label": "FRICTIONAL.md Log", "value": "Auditable", "sub": ""}
              ],
              focus=1),
]

def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_puck", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b

OPEN = [
    remotion("BIDEA", "the question",
        "Hallo. I'm Isaac Tai, an F-1 student in INFO 7375. My final project will be a command-line tool for F-1 STEM OPT students that checks, before you apply, whether a company has really sponsored work visas before, using government records instead of AI guesses.",
        "BrutalistHesitantWriter",
        {"text": "A CLI that guesses visa sponsorship\nbefore you apply", "triggerWords": "guesses", "replacementWords": "checks",
         "fontSize": 70, "charMs": 22, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20,
         "seed": SLUG, "banner": ""},
        [{"at": 0.0, "event": "types"}, {"at": 0.6, "event": "backspaces on the spoken correction"}],
        lead_silence_s=0.8, motion_claim="The writer types what the tool is and corrects guesses to checks.",
        qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."})
]

B = OPEN + B
B.append({"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
          "narration_text": f"{TITLE}. Isaac Tai.", "estimated_duration_s": 4.0, "voice": "am_puck", "engine": "kokoro",
          "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates"}],
                   "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@IsaacTai", "subline": ""}}},
          "kind": "outro_voice", "tail_silence_s": 1.0})

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "PITCH FILM", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "claude-liam", "persona": "Isaac (in for Bear)", "voice": "am_puck", "voice_kokoro": "am_puck", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "German/Dutch (Hallo)",
    "bookend_exempt": ["cold-open", "bvdt", "your-turn"],
    "bookend_exempt_reason": "Pitch film structure. No your-turn required.",
    "playlist": "INFO7375 Pitch", "chapter_number": 1,
    "tags": ["Pitch", "The Reallocation Engine"]},
    "beats": B}

(HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(f"Generated {len(B)} beats for the Pitch Film.")
