"""Build scenes.py = show-tell iso_kit.py + iso_originals_25.py + scene_body.py.
The skill says paste, don't import: Gate A copies only scenes.py into its sandbox."""
import os
from pathlib import Path
HERE = Path(__file__).resolve().parent
# $TOOLKIT = your brutalist.art clone; default is the layout this film was built in
TOOLKIT = Path(os.environ.get("TOOLKIT", HERE.parents[1] / "toolkit/brutalist.art"))
KIT = TOOLKIT / "skills/make/show-tell/templates"
parts = [(KIT / "iso_kit.py").read_text(), (KIT / "iso_originals_25.py").read_text(), (HERE / "scene_body.py").read_text()]
(HERE / "scenes.py").write_text("\n\n".join(parts))
print("scenes.py:", sum(p.count("\n") for p in parts), "lines")
