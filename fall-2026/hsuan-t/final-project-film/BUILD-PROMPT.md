# BUILD PROMPTS & REPRODUCTION — The Reallocation Engine Pitch Film

This document records the exact command pipeline, build prompts, and parameters used to author, render, and verify the final pitch film.

## 1. Pipeline Environment
* **Platform**: macOS (Apple Silicon Darwin)
* **Framework**: Brutalist (`~/IsaacPARA/Projects/info7375_prompt_eng_agentic_ai/brutalist.art`)
* **Target Project**: `film/youtube/final-project-pitch-film`
* **Resolution**: Native 4K UHD (3840 × 2160), 24 fps

## 2. Key Authoring Prompts & Decisions
The film was structured around the 7 mandatory pitch questions and the strict **Honesty Rule**. Every card is stamped REAL OUTPUT, REAL CSV ROWS, or CONSTRUCTED MOCK-UP (revision 2026-10-25):
- **Cold Open (`BIDEA`)**: Who I am and what the tool is; hesitant writer types "A CLI that guesses visa sponsorship" and corrects "guesses" to "checks".
- **Product Scope (`B01` - `B03`)**: B01 shows the real 2026-10-04 prototype output; B02 compares ChatGPT (the tool I tried) with the planned script; B03 sketches the planned 3-stage pipeline.
- **Dataflow (`B04`)**: Visualizing URL ingest through verification gates and DOL/SEC databases to the final decision.
- **Scope Discipline (`B05`)**: Demonstrating In-Scope items (Sponsor lookup, Hash deduplication) while explicitly marking "Auto-Apply Bot" as OUT OF SCOPE.
- **Risk (`B06`)**: Company-name mismatch, shown with real CSV rows for "Toast".
- **Why this project (`B07`)**: Real source tags from `role-scores.md`, lens on `[model-judgment]`.
- **Outro (`BOUT`)**: Creator card crediting Isaac Tai with portfolio links.

## 3. Reproduction Commands

### Step 1: Generate Kokoro Audio
```bash
python3 runtime/scripts/generate_audio_kokoro.py ../film/youtube/final-project-pitch-film
```

### Step 2: Render Beats & Check Gates (Review Cut)
```bash
./art run ../film/youtube/final-project-pitch-film --height 2160
```

### Step 3: Verify Deterministic Typography (Gate T)
```bash
python3 runtime/scripts/type_check.py ../film/youtube/final-project-pitch-film
```

### Step 4: Export Verified 4K Master Final Cut
```bash
./art final ../film/youtube/final-project-pitch-film --height 2160 --out ../film/youtube/final-project-pitch-film/exports/landscape
```
Output artifact: `exports/landscape/final-project-pitch.mp4` (126.2s, 4K, 0 Gate Failures).
