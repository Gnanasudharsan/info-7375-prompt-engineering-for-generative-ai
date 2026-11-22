# Persona grep — decisiontrace-lite-film

2026-11-22. A case-insensitive search for instructor persona and toolkit default strings in the
working folder's `beat_sheet.json`, `scenes.py`, and every `*.md`:

```bash
grep -rIl -iE "NikBearBrown|\bBear\b|Liam|Talofa|Hola|ELEVENLABS" beat_sheet.json scenes.py *.md
```

Result: **no hits.** The metadata has no `channel_title` or persona fields, and no beat uses a Remotion
or toolkit outro scene.
