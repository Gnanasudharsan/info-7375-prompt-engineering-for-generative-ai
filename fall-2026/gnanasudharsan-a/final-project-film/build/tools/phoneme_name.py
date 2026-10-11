"""phoneme_name.py — Kokoro narration with my name pronounced from hand-set IPA.

Kokoro's own G2P mispronounces "Gnanasudharsan Ashokumar" (five respellings
failed). kokoro-onnx 0.6.1 accepts a phoneme string directly
(Kokoro.create(..., is_phonemes=True)), so this tool phonemises each sentence
normally with Kokoro's tokenizer and replaces ONLY the name with an IPA string.

Everything else — model, voice, text normalisation, mp3 writing, duration
measurement — is the toolkit's own code (imported from
brutalist.art/runtime/scripts/generate_audio_kokoro.py), so these beats match
the other Kokoro beats in format and loudness.

  python3 tools/phoneme_name.py samples <reel>                 # samples/name-<X>.mp3 for every variant
  python3 tools/phoneme_name.py beats <reel> --variant A --only B00 B12

`beats` writes mp3/beat-<ID>.mp3 and records audio_file, actual_duration_s and a
phoneme_note (variant, IPA, full phoneme string) in beat_sheet.json. Those beats
carry engine "kokoro-phoneme", which generate_audio_kokoro.py skips, so the
standard script can never overwrite them.

ART_HOME (default ~/Downloads/7375/brutalist.art) locates the toolkit.
"""
import argparse
import json
import os
import sys
from pathlib import Path

ART_HOME = Path(os.environ.get("ART_HOME", "~/Downloads/7375/brutalist.art")).expanduser()
sys.path.insert(0, str(ART_HOME / "runtime" / "scripts"))
import generate_audio_kokoro as g  # noqa: E402  (toolkit helpers: load_engine, write_mp3, measure, normalize_for_tts)
from kokoro_onnx.tokenizer import Tokenizer  # noqa: E402

NAME = "Gnanasudharsan Ashokumar"
VOICE = "af_heart"
LANG = "en-us"

# Guide: "Nyahn-ah-soo-dhar-shahn Ah-shohk-koo-mahr"
VARIANTS = {
    "A": "ɲˈɑːnɑːsuːdɚʃˌɑːn ɑːʃˈoʊk kuːmˌɑːɹ",
    "B": "njˈɑːnɑːsuːdɚʃˌɑːn ɑːʃˈoʊk kuːmˌɑːɹ",
    "C": "ɲˈɑːnɑːsˌuːdəɹʃɑːn ɑːʃˈoʊkkuːmˌɑːɹ",
    # added: breathy "dh" via aspiration mark ʰ (the dental mark ◌̪ is not in Kokoro's vocabulary)
    "D": "ɲˈɑːnɑːsuːdʰɚʃˌɑːn ɑːʃˈoʊk kuːmˌɑːɹ",
    # added: syllable-even reading of the guide — secondary stress on "soo", primary on "mahr"
    "E": "ɲˈɑːnɑːsˌuːdʰɚʃɑːn ɑːʃˈoʊk kuːmˈɑːɹ",
}


def check_vocab(tok, ipa):
    missing = sorted({c for c in ipa if c != " " and c not in tok.vocab})
    if missing:
        raise SystemExit(f"IPA {ipa!r} uses symbols not in Kokoro's vocabulary: {missing}")


def phonemes_for(tok, text, ipa):
    """Phonemise `text` normally, with NAME replaced by `ipa` (must occur exactly once)."""
    if text.count(NAME) != 1:
        raise SystemExit(f"expected the name exactly once in: {text!r}")
    pre, post = text.split(NAME)
    punct = post[:len(post) - len(post.lstrip(".,;:!?"))]
    rest = post[len(punct):].strip()
    parts = []
    if pre.strip():
        parts.append(tok.phonemize(g.normalize_for_tts(pre.strip()), LANG))
    parts.append(ipa + punct)
    if rest:
        parts.append(tok.phonemize(g.normalize_for_tts(rest), LANG))
    return " ".join(parts)


def synth(engine, phonemes, out):
    samples, sr = engine.create(phonemes, voice=VOICE, lang=LANG, is_phonemes=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    g.write_mp3(samples, sr, out)
    return g.measure(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["samples", "beats"])
    ap.add_argument("reel", type=Path)
    ap.add_argument("--variant", choices=sorted(VARIANTS))
    ap.add_argument("--only", nargs="+", default=["B00", "B12"])
    a = ap.parse_args()
    reel = a.reel.expanduser()
    tok, engine = Tokenizer(), g.load_engine()
    for ipa in VARIANTS.values():
        check_vocab(tok, ipa)

    if a.mode == "samples":
        for key, ipa in VARIANTS.items():
            ph = phonemes_for(tok, f"I'm {NAME}.", ipa)
            dur = synth(engine, ph, reel / "samples" / f"name-{key}.mp3")
            print(f"name-{key}.mp3  {dur:.2f}s  {ph}")
        return

    if not a.variant:
        raise SystemExit("--variant is required for beats")
    ipa = VARIANTS[a.variant]
    sheet_path = reel / "beat_sheet.json"
    sheet = json.loads(sheet_path.read_text(encoding="utf-8"))
    timings_path = reel / "mp3" / "timings.json"
    timings = json.loads(timings_path.read_text()) if timings_path.exists() else {}
    for b in sheet["beats"]:
        if b["beat_id"] not in a.only:
            continue
        ph = phonemes_for(tok, b["narration_text"], ipa)
        out = reel / "mp3" / f"beat-{b['beat_id']}.mp3"
        dur = synth(engine, ph, out)
        b.update({"engine": "kokoro-phoneme", "voice": VOICE, "audio_file": f"mp3/beat-{b['beat_id']}.mp3",
                  "actual_duration_s": round(dur, 2),
                  "phoneme_note": {"tool": "tools/phoneme_name.py", "variant": a.variant, "name_ipa": ipa,
                                   "phonemes": ph}})
        timings[b["beat_id"]] = round(dur, 2)
        print(f"beat-{b['beat_id']}.mp3  {dur:.2f}s  {ph}")
    sheet_path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False), encoding="utf-8")
    timings_path.write_text(json.dumps(timings, indent=1))


if __name__ == "__main__":
    main()
