# FRICTIONAL.md — Final Project Pitch Film

Dated log of friction while working. Only things that actually happened.

---

## 2026-10-09 — Brutalist setup record

**Where the setup facts come from.** I installed Brutalist before this
assignment. The file timestamps put the Kokoro model download on
2026-09-14 at 12:54 and the `.venv` creation at 12:56 on the same day. The
command list below comes from my zsh history. That history has no
timestamps and no command output, so it shows the commands I ran and their
order, but not the error messages. Everything marked **verified today** I
re-ran on 2026-10-09.

### Install commands, in the order my shell history shows them

```bash
git clone https://github.com/nikbearbrown/brutalist.art
./setup --install                 # run 3x from ~/Downloads/7375 — the wrong directory
chmod +x setup.sh art.sh          # copied from a guide; this repo has no .sh files —
./setup.sh --install              #   the scripts are named `setup` and `art`
./setup.sh
cd brutalist.art                  # repeated the same .sh commands from inside the repo
less setup                        # read the real script before running it
./setup --install
brew install ffmpeg
brew install python@3.12
$(brew --prefix python@3.12)/bin/python3.12 -m venv .venv
source .venv/bin/activate
python -V
./setup --install
brew install pkg-config cairo pango        # system libraries for Manim's text rendering
which -a node npm
brew list --versions node
brew link --overwrite node
brew install node
./setup --install
brew install --cask basictex               # LaTeX, needed only for Manim equation beats
brew list --cask
which latex dvisvgm
ls /Library/TeX/texbin | head -20
ls /usr/local/texlive
brew uninstall --cask mactex --force
brew install --cask basictex
eval "$(/usr/libexec/path_helper)"
which latex dvisvgm
sudo tlmgr update --self
sudo tlmgr install dvisvgm standalone preview
./setup
```

### Errors and fixes

- **Wrong file names and wrong directory.** I ran `setup.sh` and `art.sh`,
  which don't exist; the scripts are `setup` and `art`. I also ran
  `./setup --install` from `~/Downloads/7375` instead of from inside the
  repo. **Fix:** I `cd`'d into `brutalist.art`, read `setup` with `less`, and
  ran `./setup --install`.
- **Missing system dependencies.** After each `./setup --install` I installed
  another dependency and ran it again: ffmpeg, Python 3.12 in a `.venv`,
  cairo/pango/pkg-config, Node, then BasicTeX with `dvisvgm`. History doesn't
  keep the error text, so I can't quote what each failure said. I only know
  the order of the fixes.
- **LaTeX not found after install.** I removed a MacTeX cask, reinstalled
  BasicTeX, and ran `eval "$(/usr/libexec/path_helper)"` to put
  `/Library/TeX/texbin` on my PATH. Then I used `tlmgr` to add `dvisvgm`,
  `standalone` and `preview`.
- **Readiness check gives false failures without the venv** (still true
  today). Running `./setup` without `source .venv/bin/activate` first reports
  Kokoro, Manim and compile as blocked. With the venv active, they all pass.

### Tool versions — verified today (2026-10-09)

| Tool | Version |
|---|---|
| Python (in `.venv`) | 3.12.14 (Homebrew `python@3.12`) |
| System `python3` | 3.14.0 (not used by Brutalist) |
| ffmpeg / ffprobe | 9.0.1 (Homebrew) |
| TTS engine | Kokoro, run locally with `kokoro-onnx` 0.6.1 and `onnxruntime` 1.30.0. Model files: `kokoro-v1.0.onnx` and `voices-v1.0.bin` |
| Manim | 0.18.1 |
| Node / npm | v26.8.2 / 11.19.1 |
| Remotion | 4.0.486 |
| LaTeX | pdfTeX 3.141592653-2.6-1.40.29 (TeX Live 2026), dvisvgm 3.6 |
| Brutalist checkout | commit `ba2d0e0` |

### `./setup` readiness check — verified today

With `.venv` active, every row came back `✅ ready`: Kokoro audio, captions
and word clock, Manim beats, Manim equation beats, Remotion beats and
bookends, slates/previz/compile, and fonts. Cost reported: $0.00.

### Did the sample film render? First no, then yes after a workaround (verified today)

- **`./art smoke` FAILED.** It stopped at GATE 0 (Kokoro narration) with
  `generate_audio_kokoro.py failed`. The smoke script deletes its temp
  folder when it exits, so the log went with it. I ran the audio step by hand
  on a copy of `examples/_smoke/` and got the real error:
  `[kokoro] REFUSED: metadata.slug must be a filename, not a path`.
- **Cause:** a bug in the toolkit, not in my setup. The smoke fixture's
  slug is `_smoke`. The slug check (`runtime/scripts/build_safety.py`, line
  186) only accepts slugs that start with a letter or digit, so the
  toolkit's own test fixture fails its own safety check.
- **Workaround (toolkit not modified):** I copied the fixture to a scratch
  folder and changed the slug to `smoke`. Then I ran the same steps the smoke
  script runs:
  `python3 runtime/scripts/generate_audio_kokoro.py <copy>`, then
  `ART_FACTS=0 ART_QC=1 ART_STRICT=0 bash runtime/scripts/run.sh <copy>`.
- **Result:** both narration beats were synthesized (B00 8.73 s, B01 5.12 s,
  cost $0.00). It compiled `smoke-slate.mp4`: h264 3840×2160 video plus AAC
  audio, 13.9 s, 579,600 bytes, audio mean volume −24.2 dB. All three of
  the smoke script's checks pass: volume above −40 dB, real video and audio
  streams, and the file is larger than 20,000 bytes. I looked at
  `qc-sheet.png` myself: two readable slate frames, B00 and B01, showing the
  narration text.
- GATE V (visual QC) reported 0 BLOCKER and 4 MAJOR `underfill` (content
  fills about 42% of the safe area; the minimum is 55%). The smoke script
  expects this on its bare slates and runs with `ART_STRICT=0` for that
  reason, so this doesn't show a broken pipeline.
- **Still open:** `./art smoke` itself will keep failing until the fixture
  slug or the regex is fixed upstream. I didn't edit the toolkit.
