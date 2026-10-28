"""overlap05.py — every-0.5 s overlap audit: the layout audit's own text-on-text, text-on-line and
off-safe tests, sampled on the LIVE scene every 0.5 s of scene time (not only at steady states).
usage: python3 overlap05.py <scenes.py> <Class> [<Class> ...]"""
import sys, os, json, math, importlib.util
from pathlib import Path
sys.path.insert(0, os.path.expanduser("~/brutalist-v2/runtime/qc"))
import manim_layout_audit as A

scene_path = Path(sys.argv[1]).resolve()
snaps_all = {}
dummy = []
A._import_manim_and_patch(dummy)                      # sets A.TEXT_TYPES / A.config; patches wait/play (harmless)
from manim import Scene, tempconfig
orig_utt = Scene.update_to_time
def utt(self, t):
    orig_utt(self, t)
    g = float(getattr(self.renderer, "time", 0.0) or 0.0) + float(t)
    k = int(g / 0.5)
    if k != getattr(self, "_o05_last", -1):
        self._o05_last = k
        A._snapshot(self, "t", round(g, 2), self._o05)
Scene.update_to_time = utt
os.chdir(scene_path.parent); sys.path.insert(0, str(scene_path.parent))
spec = importlib.util.spec_from_file_location("o05_scene", str(scene_path)); mod = importlib.util.module_from_spec(spec)
sys.modules["o05_scene"] = mod; spec.loader.exec_module(mod)
opt = dict(safe_w=A.DEFAULTS["safe_w"], safe_h=A.DEFAULTS["safe_h"], min_overlap=A.DEFAULTS["min_overlap"],
           curve_inset=A.DEFAULTS["curve_inset"], max_segs=A.DEFAULTS["max_segs"], curve_strict=True)
bad = 0
for cls in sys.argv[2:]:
    with tempconfig({"write_to_movie": False, "disable_caching": True, "quality": "low_quality", "frame_rate": 10, "verbosity": "ERROR"}):
        sc = getattr(mod, cls)(); sc._o05 = []; sc.render()
    f = A._analyze(sc._o05, opt)
    ts = sorted({s["t"] for s in sc._o05})
    print(f"{cls}: {len(sc._o05)} samples ({ts[0] if ts else '-'}–{ts[-1] if ts else '-'} s) → " +
          ("CLEAN" if not f else "; ".join(f"{x['severity']} {x['type']} {x.get('text') or (x.get('a'),x.get('b'))} @t={x.get('t')}" for x in f)))
    bad += len(f)
sys.exit(1 if bad else 0)
