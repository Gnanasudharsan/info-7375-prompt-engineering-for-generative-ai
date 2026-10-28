# Toolkit changes needed to rebuild this film

Toolkit: `~/Desktop/Brutalist/brutalist.art` (existing clone, not re-cloned).

## Baseline (recorded 2026-10-14 09:31 EDT, before any work on this film)

- Branch `main`, HEAD `519fcbb96e9e1898d374c8794117cab494ffc5cb` ("Pin Manim to the 0.20 series").
- Python env: conda `brutalist-daythread` (Python 3.12.14, Manim 0.20.1). Put it on PATH:
  `eval "$(/usr/libexec/path_helper)" && export PATH="/opt/anaconda3/envs/brutalist-daythread/bin:/opt/homebrew/bin:$PATH"`
- `./setup` → exit 0, all 7 features ready.

## Local changes to toolkit files

| File | Change | Why | Since |
|---|---|---|---|
| `setup` | `--exclude-dir=youtube` added to both ElevenLabs `grep -r` calls (lines ~107 and ~112) | Without it, setup's "Kokoro-only" guard scans the toolkit's `youtube/` study folders and fails on their text | Before this film (pre-existing, uncommitted); sha256 after change `c33424dd940d8793a6348c94481fb2ff634198494cc149039b6f37ecf24840b8` |

No toolkit changes have been made *for this film* yet. Any later change gets a row here, with a
patch saved in `toolkit-patches/`.

## 2026-10-14 — 15-second preview (`preview/`)

- **No toolkit source files were changed for the preview.** Verified afterwards: `git status` shows only the
  pre-existing `setup` change (sha256 still `c33424dd…`), HEAD still `519fcbb`.
- The preview uses toolkit code *by copy*, not by edit: `preview/assemble_scenes.py` pastes
  `skills/make/show-tell/templates/iso_kit.py` verbatim, plus the data for two props (`review-desk`,
  `permission-gate`) and the `make_original` factory from `iso_originals_25.py`, into `preview/scenes.py`.
- Byproduct: Claude's diagnostic import of `runtime/scripts/type_check.py` updated the git-ignored cache
  `runtime/scripts/__pycache__/type_check.cpython-312.pyc`. Claude deleted that cache file. Python recreates
  it on the next import. No source changed.
- **Approved, not yet made:** an optional name/handle setting for the outro (`ClaudeTitleOutro`), with
  existing defaults preserved. Only the full film needs it. A patch and rebuild steps will be added here
  when it is made.

### Rebuild the preview
```bash
cd ~/Desktop/Brutalist
eval "$(/usr/libexec/path_helper)" && export PATH="/opt/anaconda3/envs/brutalist-daythread/bin:/opt/homebrew/bin:$PATH"
P=my-videos/youtube/daythread/preview
python $P/make_sheet.py                                                      # keeps measured audio fields
python brutalist.art/runtime/scripts/generate_audio_kokoro.py $P             # only if narration changed
rm -rf $P/mp3/raw && python $P/pad_audio.py                                  # only after fresh audio
python $P/assemble_scenes.py
mkdir -p $P/_superseded/old && mv $P/manim $P/media $P/_superseded/old/ 2>/dev/null   # art run only renders missing clips
./brutalist.art/art run   $P --height 2160
./brutalist.art/art final $P --height 2160 --out $P/exports
```

## 2026-10-14 — full film (`film/`)

- **No toolkit source files changed for the film.** Verified after the final render: `git status` shows only
  the pre-existing `setup` change (sha256 still `c33424dd…`), HEAD `519fcbb`. The only ignored entries are
  the toolkit's normal caches and model folder (`runtime/scripts/__pycache__/`, `runtime/models/`, `renders/`, …).
- **The approved optional outro name/handle setting was NOT applied — it was not needed.** The outro is a
  drawn Manim scene (`BOUT_Outro` in `film/scenes_body.py`) instead of `ClaudeTitleOutro`, whose handle and
  mascot are hardcoded. Consequence, by design: `runtime/scripts/bookend_check.py` reports the outro rule as
  failed ("handle must be '@NikBearBrown'"). It is not run by `art run` / `art final`.
- Pronunciation fixes were made by rewording two narration lines in `SCRIPT.md`, **not** by editing the toolkit's
  `runtime/pronunciation/liam.json` (that file is shared with other videos).
- Toolkit code reused by copy: `skills/make/show-tell/templates/iso_kit.py` (verbatim) and 11 props' data plus
  `make_original` from `iso_originals_25.py`, pasted into `film/scenes.py` by `film/assemble_scenes.py`.

Rebuild instructions: `README.md` → "Rebuild (exact)".

## 2026-10-25 — v4 rebuild for the resubmission (B04 and B15)

- **No toolkit source files changed.** Verified after the final render: `git status` shows only the
  pre-existing `setup` change (sha256 still `c33424dd…`), HEAD `519fcbb`.
- GATE T failed twice on B04 during the rebuild (see `gate-reports/revision-attempts/`). It was
  fixed in the film's own `scenes_body.py`, not by adding an exemption to
  `runtime/scripts/type_check.py`.
- New film-side helper: `source/final_checks.py`, which reruns the extra checks on the master. It
  only calls the toolkit's `bookend_check.py`.
