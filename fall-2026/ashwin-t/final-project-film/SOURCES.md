# SOURCES.md: TraceCase pitch film

## What I made

- The project choice, the seven answers in `PROJECT-BRIEF.md`, and the decisions in `FRICTIONAL.md`.
- The narration script (in `beat_sheet.json`) and the visual plan, reviewed and approved by me.

## What AI contributed

**Claude Code (Opus 5.5), 2026-10-09 to 2026-10-13:**
- Brainstormed project ideas with me and ran the web searches behind them. I rejected most of them.
- Counted skill keywords across the job postings my own pipeline had stored, so I could see which skills my
  resume lacks. The postings and my resume are private and are not in this folder; only the percentages are.
- Checked the HolmesGPT, AIOpsLab, OpenTelemetry and Jaeger primary sources used in the fact check. That check
  removed one claim from my draft: human approval is not what makes TraceCase different, because HolmesGPT's
  remediation toolset already asks for approval.
- Drafted `PROJECT-BRIEF.md`, `FRICTIONAL.md` (from my chats and the command output), this file, `README.md`
  and `BUILD-PROMPT.md`.
- Wrote `make_sheet.py`, `scene_body.py` (16 Manim drawings), the helper scripts, and ran the toolkit's render
  and gates.

**Codex (ChatGPT), 2026-10-11 and 2026-10-13:**
- Gave me a brutal second opinion on ProvenDocs (6/10 as pitched) and suggested an incident investigation
  assistant.
- Reviewed other pitches I pasted in, and corrected claims in them. For example, the EvilGenie paper found that
  hidden tests helped only a little.

I chose TraceCase, and I am responsible for everything in this folder.

## What I used

| Thing | Use | Licence / terms |
|---|---|---|
| Brutalist toolkit, github.com/nikbearbrown/brutalist.art at `b21f625` | show-tell skill, `iso_kit.py` drawing kit (pasted into `scenes.py`), Remotion bookends (`BrutalistHesitantWriter`, `ClaudeTitleOutro`), render pipeline and quality gates | Course-provided toolkit; the repository has no licence file |
| Kokoro-82M via kokoro-onnx 0.6.1, voice `am_michael`, speed 0.95 | all narration (I recorded my own intro and outro, then chose the synthetic voice instead); generated locally, cost $0 | Kokoro-82M: Apache-2.0; kokoro-onnx: MIT |
| faster-whisper 1.2.1 (`base.en`) | transcript check of the narration | MIT |
| Manim Community 0.18.1 | every body-beat drawing | MIT |
| Remotion (from the toolkit) | opening and closing bookend cards | Remotion licence (free for individuals) |
| EB Garamond (bundled with the toolkit) | on-screen labels | SIL Open Font License |
| ffmpeg (Homebrew) | audio cleanup, padding and assembly | LGPL/GPL |

## Local changes to the toolkit (saved in `build/`)

- `build/patches/ClaudeTitleOutro-handle.patch`: the outro card hardcoded the instructor's handle. The assignment
  forbids the instructor's credit line, so the card takes an optional `handle` prop; mine is my name.
- `build/patches/ClaudeDefinitions-meansize.patch`: from the ProvenDocs build. It is not used by this film
  (there is no terms card) but stays applied in my toolkit checkout.
- `build/ashwin.json`: a voice-only pronunciation fix, so "Redis" is said "RED-iss".

## What I read for facts (all public, read 2026-10-13)

- https://github.com/HolmesGPT/holmesgpt: "Open-source AI agent for investigating production incidents and
  finding root causes"; read-only by default; CNCF sandbox; Apache-2.0.
- https://holmesgpt.dev/latest/data-sources/builtin-toolsets/kubernetes-remediation-mcp/: optional remediation
  toolset, with mutating actions gated behind human approval.
- https://github.com/microsoft/AIOpsLab: a framework for the design, development and evaluation of AIOps agents;
  runs on a kind or other Kubernetes cluster; MIT. Paper: "AIOpsLab: A Holistic Framework to Evaluate AI Agents
  for Enabling Autonomous Clouds" (MLSys 2025).
- https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md:
  Spring Web MVC, Lettuce and Jedis are supported.
- https://www.jaegertracing.io/docs/latest/getting-started/: Jaeger all-in-one runs as one Docker container.

## Third-party assets

None. No stock images, music, sound effects, or generated media. Every picture is a native Manim vector drawing.

## Private data

None. The film and this folder contain no resume, contacts, application tracker, job postings, or conversation
transcripts. The skill percentages are aggregate counts. My CloudPulse and MyEdMaster work is described in one
sentence, and no private code is shown.
