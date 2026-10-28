#!/bin/sh
# Build the LMS upload: reallocation-professor-bear-mode.zip. Contains the mode file, the domain justification, the worked run,
# the RUN_LOG entry, the new script and its tests, and the public run outputs. Never contains private/.
set -e
cd "$(dirname "$0")"
rm -f reallocation-professor-bear-mode.zip
zip -rq reallocation-professor-bear-mode.zip README.md recipes 01-domain-justification.md 02-worked-run.md 03-run-log-entry.md 04-show-and-tell-notes.md scripts runs -x '*/__pycache__/*' -x 'private/*'
unzip -l reallocation-professor-bear-mode.zip | tail -3
