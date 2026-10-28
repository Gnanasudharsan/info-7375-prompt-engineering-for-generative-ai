# PROMPTS

**Voice generation:** the narration is generated locally and free by **Kokoro-82M** (kokoro-onnx) with voice `af_heart`, at speed 0.95. The input text is each beat's `narration_text` in `beat_sheet.json`, which is my first-person script. Two respellings are applied only to the text sent to the voice, and are listed in `pronunciation.json`: "RAG" becomes "rag", and "Kommuri" becomes "Kommu-ree". There are no other prompts: Kokoro takes text, not instructions. The voice is synthetic. It is not my voice, and not the instructor's Liam voice (`am_onyx` / `am_liam`).

**No image or video generation:** the pictures are native Manim vector drawings (the toolkit's show-tell kit and its approved original props), and the opener is the toolkit's Remotion `BrutalistHesitantWriter` component.

The prompts I gave Claude Code to build the film are in BUILD-PROMPT.md.
