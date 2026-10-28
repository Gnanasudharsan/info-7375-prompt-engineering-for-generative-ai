# BUILD-PROMPT: how to rebuild this film

Everything is local and free: no API keys, no paid generation, no accounts.

## Requirements
- macOS or Linux, Python 3.12, Node 18+, ffmpeg
- The Brutalist toolkit at `~/brutalist.art`, commit `519fcbb` or later

```bash
git clone https://github.com/nikbearbrown/brutalist.art ~/brutalist.art
```

```bash
cd ~/brutalist.art && ./setup --install
```

The setup installs the Python venv and Remotion node modules, and downloads the Kokoro model (about 340 MB).

## Rebuild, step by step (run from this folder)

```bash
cp pronunciation/aditya.json ~/brutalist.art/runtime/pronunciation/
```

```bash
python3 prepare_crops.py
```

(This needs Aditya's uncropped screenshots in `~/PEAI_Class/baseline-v2-originals/`. The crops it makes are already committed in `research/film-crops/`.)

```bash
python3 make_sheet.py
```

```bash
~/brutalist.art/.venv/bin/python ~/brutalist.art/runtime/scripts/generate_audio_kokoro.py "$PWD"
```

Then pad the outro tail and write its length back. Run `make_sheet.py` again; it keeps the measured durations.

```bash
ffmpeg -y -i mp3/beat-BOUT.mp3 -af apad=pad_dur=1.0 mp3/tmp.mp3 && mv mp3/tmp.mp3 mp3/beat-BOUT.mp3
```

```bash
./build_scenes.sh
```

```bash
PATH="$HOME/brutalist.art/.venv/bin:$PATH" ~/brutalist.art/art run "$PWD" --height 2160
```

```bash
PATH="$HOME/brutalist.art/.venv/bin:$PATH" ~/brutalist.art/art final "$PWD" --height 2160 --out "$PWD/exports/landscape"
```

## The prompts that produced this folder (Aditya → Claude Code, 2026-10-14)
These are paraphrased to the instruction itself. The full session isn't included, because it's a private transcript.
1. "This is my assignment. Break it down into phases… ask me for permission or input wherever needed, and don't push anything."
2. "Create a folder in PEAI… you can [read brutalist.art]… list the guidelines for the project."
3. "Pull the latest brutalist.art and check for show-tell. Keep my local package-lock change safe."
4. "My project is the AI Product Failure Lab [blueprint doc attached]… you can improve or change the scope."
5. "AI product manager · run the baseline [on plain Claude] · use my portfolio for my skills · build it all with Claude Code in two weeks."
6. "Run the baseline prompt on logged-out ChatGPT."
7. "[Storyboard doc attached] The script is my idea; the visuals and flow were written by ChatGPT. Feel free to change it to the new scope and the guidelines."
8. "Use a local Kokoro voice in the first person, disclosed in SOURCES.md. Let me hear samples." → "am_michael", surname version A.
9. "Build the Manim scenes, starting with low-res stills." → "Looks good, render the final output."

## The baseline prompt (sent to plain Claude ×3 and ChatGPT ×1)
See `research/baseline-prompt.md` for the exact text and the checks decided in advance.

## Resubmission prompts (Aditya → Claude Code, 2026-10-25)
10. "[Grader feedback pasted] Read this feedback… we need to fix this and resubmit."
11. "[ProductLens script attached] Go through this and compare it against the assignment, let me know if any changes are required."
12. "A. merge, do what you have to, fix and update it." Then: "the script needs to be simple and actually explain my project."
13. "Here are the screenshots" (Aditya's own ChatGPT run), plus answers for FRICTIONAL in his own words.
14. "Script approved. Build the film."

## The v2 test prompt (run by Aditya himself)
See `research/baseline-v2-prompt.md`.
