# toolkit-changes — what the SponsorScout pitch film adds to brutalist.art

Base revision: `6a8380ae169cca81e0633664a65c958f5c12ab4b`.

| File | Change | Why |
|---|---|---|
| `runtime/remotion/src/illustrations/pitch.tsx` (new, copy here) | `PitchOutro`: title, "a pitch by Akshit Verma", course | `ClaudeTitleOutro` hardcodes `@NikBearBrown`. The assignment forbids the instructor's credit line |
| `runtime/remotion/src/Root.tsx` | one import + one `<Composition id="PitchOutro">` | registers the outro |
| `runtime/scripts/compile.py:767` | `ART_CHANNEL_TITLE=0` opt-in: don't burn `metadata.channel_title` into beat one | that burn-in sat under the first caption. The field stays set for `bookend_check.py` |

`root-and-compile.diff` is `git diff 6a8380a` of those two files. **It also contains my Week 01
changes** to the same files: Week 01's scene registrations in `Root.tsx`, its `ART_BURNIN=0` switch
and its `drawtext` font-path fix in `compile.py`. Those were already in my checkout and this film
uses them. They are documented in my Week 01 folder (`week-01-video/toolkit-changes/`).

Apply, on a clean checkout of `6a8380a` (verified 2026-10-14: these three steps reproduce every changed
toolkit file byte for byte):

```bash
git apply --exclude=runtime/remotion/src/Root.tsx --exclude=runtime/scripts/compile.py \
    <week-01-video>/toolkit-changes/toolkit.patch          # Week 01's other files (setup, smoke, scenes ...)
git apply <this folder>/toolkit-changes/root-and-compile.diff   # both shared files, Week 01's hunks included
cp <this folder>/toolkit-changes/pitch.tsx runtime/remotion/src/illustrations/
```
