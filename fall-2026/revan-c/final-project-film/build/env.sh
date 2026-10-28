# source this before any build command: the toolkit's venv + the espeak-ng fix (see FRICTIONAL.md)
: "${TOOLKIT:?set TOOLKIT to your brutalist.art clone first}"
export PATH="$TOOLKIT/.venv/bin:$PATH"
export PHONEMIZER_ESPEAK_LIBRARY="${PHONEMIZER_ESPEAK_LIBRARY:-/opt/homebrew/lib/libespeak-ng.dylib}"
