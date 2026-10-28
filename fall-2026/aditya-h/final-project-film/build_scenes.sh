#!/bin/sh
# Assemble scenes.py = toolkit drawing kit + approved props + this film's scenes (Gate A copies only scenes.py).
T="${ART_HOME:-$HOME/brutalist.art}/skills/make/show-tell/templates"
cat "$T/iso_kit.py" "$T/iso_originals_25.py" scenes_body.py > scenes.py && echo "scenes.py: $(wc -l < scenes.py) lines"
