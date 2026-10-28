#!/usr/bin/env python3
"""voice.py: the toolkit's generate_audio_kokoro.py, plus this film's pronunciation.json.

The toolkit keeps pronunciation fixes per voice in brutalist.art/runtime/pronunciation/, and it has
entries only for Liam (am_onyx). Rather than edit the toolkit, this applies pronunciation.json
(same format) first, then the toolkit's own rules. Only the text sent to the voice changes.

    python voice.py --speed 0.95            # all beats
    python voice.py --speed 0.95 --only B10 # one beat (then re-pad BOUT/BIDEA via finish_audio.py)
    python voice.py --check                 # verify each example against Kokoro's phonemizer
"""
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = Path(os.environ.get("ART_HOME", HERE.parent / "brutalist.art"))
sys.path.insert(0, str(ART / "runtime" / "scripts"))
import pronunciation  # noqa: E402

RULES = json.loads((HERE / "pronunciation.json").read_text(encoding="utf-8"))
for e in RULES["entries"]:
    e["_re"] = [re.compile(p) for p in e["patterns"]]
_toolkit_apply = pronunciation.apply


def apply(text, voice):
    if voice == RULES["voice"]:
        for e in RULES["entries"]:
            for rx in e["_re"]:
                text = rx.sub(lambda m, e=e: m.group(0)[:m.start("w") - m.start()] + e["say"]
                              + m.group(0)[m.end("w") - m.start():], text)
    return _toolkit_apply(text, voice)


pronunciation.apply = apply

if __name__ == "__main__":
    if "--check" in sys.argv:
        import generate_audio_kokoro as g
        tok = g.load_engine().tokenizer
        bad = 0
        for e in RULES["entries"]:
            for ex in e["examples"]:
                ph = tok.phonemize(apply(ex["text"], RULES["voice"]), "en-us")
                ok = ex["expect"] in ph
                bad += not ok
                print(f"[{'ok ' if ok else 'BAD'}] {e['id']}: {ex['text']!r} -> {ph}")
        raise SystemExit(1 if bad else 0)
    import generate_audio_kokoro as g
    sys.argv = [sys.argv[0], str(HERE)] + sys.argv[1:]
    raise SystemExit(g.main())
