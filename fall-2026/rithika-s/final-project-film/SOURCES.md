# SOURCES — Agentic Retrieval Lab (pitch film)

**Film:** *Agentic Retrieval Lab*, an INFO 7375 final-project pitch by Rithika Sankar Rajeswari. Final master, 2026-10-11 (sha256 5dccfe2315b2c59d932ab076d65a65371cd17ea5b2c945feeb22010c5ed24bf5).

## Project evidence (read-only)
- `~/agentic-retrieval-lab/README.md`, `results/foundation/` (`2026-10-08_rewrites_300/`, `2026-10-08_bm25/`, `2026-10-09_corpus/`), `git log` (2026-10-05 → 2026-10-09). The test count was taken from `uv run pytest -q` on 2026-10-10.

## Evidence excerpt
- `~/final-project-film/evidence/beat1_example_951820.json`: the five records behind beat 1's real example (query 951820 and its four Claude Haiku rewrites), copied verbatim from the git-ignored `data/processed/` files.
- Other real MS MARCO questions shown on screen (B07): `queries_human.jsonl` lines 16 and 108.

## Paper
- M. Schall, S. Eslami, M. Krimmel, A. Chaffin, L. Milliken, B. Wang, D. Bykov. *Q2D-Web: A Large-Scale Benchmark for Retrieval in Agentic RAG Systems.* arXiv:2609.08887v2, 2026 (Perplexity AI). https://arxiv.org/abs/2609.08887v2. Read: abstract, §1, §3.2, §5.1, §6, Ethics statement.
- Leaderboard: https://huggingface.co/spaces/perplexity-ai/q2d-web-leaderboard

## Dataset
- MS MARCO Passage Ranking: P. Bajaj et al., *MS MARCO: A Human Generated MAchine Reading COmprehension Dataset*, arXiv:1611.09268, 2016. Dev/small queries and the 8,841,823-passage collection, used under the MS MARCO research-use terms.

Narration: Kokoro af_bella synthetic voice, first person; script by Rithika.

## Third-party assets and licences

Licences were read from the files on disk. For the four items with no licence file on disk, I checked the official sources online on 2026-10-11; those URLs are given.

| Asset | Used for | Licence | Where the licence was read |
|---|---|---|---|
| Kokoro TTS runtime, `kokoro-onnx` 0.6.1 | Speech synthesis | MIT | `.venv/…/kokoro_onnx-0.6.1.dist-info/licenses/LICENSE` |
| Kokoro voice model, Kokoro-82M by hexgrad (files `kokoro-v1.0.onnx` and `voices-v1.0.bin` from kokoro-onnx model-files-v1.0, voice `af_bella`) | The narrator voice | Apache-2.0 | Model card: https://huggingface.co/hexgrad/Kokoro-82M (licence tag "apache-2.0"). kokoro-onnx README: https://github.com/thewh1teagle/kokoro-onnx ("kokoro model: Apache 2.0"). The model-files-v1.0 release page states no licence |
| EB Garamond font (the only font in the film) | All on-screen text | SIL Open Font License 1.1 | `brutalist.art/runtime/fonts/EB_Garamond/OFL.txt` (© 2017 The EB Garamond Project Authors) |
| Manim Community 0.18.1 | Drawing and animation | MIT | `.venv/…/manim-0.18.1.dist-info/METADATA` (`License: MIT`) |
| MS MARCO Passage Ranking dataset | Real questions, rewrites and figures | No named licence: Microsoft's Terms and Conditions, non-commercial research purposes only, "without extending any license" | https://microsoft.github.io/msmarco/ and https://microsoft.github.io/msmarco/Datasets.html ("Terms and Conditions"). The older http://www.msmarco.org/dataset.aspx fails with a TLS certificate error |
| brutalist.art toolkit (github.com/nikbearbrown/brutalist.art, commit b21f625) | Build pipeline and drawing kit | licence not verified: the repository states no licence | Checked https://github.com/nikbearbrown/brutalist.art (no licence in the sidebar or file list), …/blob/main/LICENSE (404) and https://api.github.com/repos/nikbearbrown/brutalist.art (`"license": null`) |
| Q2D-Web paper (Schall et al., 2026, arXiv:2609.08887v2) | Cited only; no text or figures reproduced | CC BY-NC-ND 4.0 (the paper; the abstract page states nothing about the dataset) | https://arxiv.org/abs/2609.08887v2 → http://creativecommons.org/licenses/by-nc-nd/4.0/ |

## Toolkit and voice
- **brutalist.art toolkit**, `show-tell` skill: Manim drawings in the house isometric style (`iso_kit.py`). Free local pipeline; no API keys, paid services or uploads.
- **Narration:** synthetic voice, Kokoro-82M (kokoro-onnx 0.6.1, model-files-v1.0), voice `af_bella`, speed 1.04. It reads Rithika's script in the first person. It is not a recording of Rithika.
- **No external media.** Every picture is drawn in Manim. There are no stock images, photos, music, or AI-generated images or video.
- **Cartoon people.** Generic flat figures drawn in Manim, which Rithika authorised on 2026-10-11: her own avatar, two librarians, a lazy librarian, a searcher and a reviewer. None is a portrait or likeness of a real person.
- **No instructor identity.** The film carries no name, portrait, voice, handle or mascot from the instructor's brand kit.

## Local toolkit patch
- Local toolkit patch: moved channel_title stamp inside title-safe area; see toolkit-local-patch.diff; not committed upstream.

## Contributions
- **Rithika:** project, decisions,prompting, script edits, review and approval.
- **Claude (chat):** drafted the script and visual plan from Rithika's brief and prompts.
- **Claude Code:** built the reel and ran the gates.

Rithika's script edits: chose the project and scope; rewrote the beat 13 line ; approved the fact-check wording fixes; chose my own drawn outro over the instructor-branded one; rejected the first visuals and asked for real text, labelled key terms, a real ski-season example, cartoon characters and full choreography; reviewed every contact sheet and preview, and flagged fixes such as the B07 “public” chip and my character lingering in B04.
