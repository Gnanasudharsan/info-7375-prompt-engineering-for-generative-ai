"""Write scenes.py = show-tell iso_kit.py (pasted, as the skill requires) + scene_body.py."""
from pathlib import Path
R = Path(__file__).resolve().parent
KIT = Path.home() / "Desktop/College/CSYE7375/brutalist-final/skills/make/show-tell/templates/iso_kit.py"
(R / "scenes.py").write_text(KIT.read_text() + "\n\n" + (R / "scene_body.py").read_text())
print("scenes.py written")
