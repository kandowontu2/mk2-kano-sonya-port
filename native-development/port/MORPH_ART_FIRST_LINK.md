# Authored morph intermediates: first linked candidate

KSMOART.ASM supplies six typed image headers, multipart groups and two native
palettes generated from editable PGM/palette sources in assets/morph. Packed
graphics append 46,357 bytes after the split bank, preserving that entire
prefix. Native morph scripts now use three dedicated intermediates, keeping
STSTANCE1, morph_swpal, original frame cadence and final own stance. The same
intermediates play in reverse during native return.

The source generator includes the new module and script edits. A hidden
25.48-second game compile created no window. Runs stock_wolf_game319/320 on
stock MAME 0.289 passed current-byte-pinned qualify_morph.py on both sides:
true IDs17/18, 524-field normal duration, Knife/Ring at 22 damage, own poses
outside morph action, and native timed return through observation field9000.
All six intermediate poses have runtime captures. Kano and Sonya middle-frame
captures on the first side were inspected and show actual transitional
costumes. Final scale/ground/costume and both-side palette visual acceptance
remain open, as do reverse-transition capture qualification and interruption
tests. Artwork is implemented, not yet fully accepted.

The prior clean-rebuild and gameplay reports are historical for this new link.
Current exact chip/program/controller hashes are in the immutable per-run
execution.json files; qualifications also pin the current map/source bytes.
No custom MAME driver, guest-memory write, timer or damage change was used.
No release was promoted.

## Forward/reverse trace

Runs 321/322 record all 18 pose episodes per side, including both Sonya
commands and automatic reverse transitions. The trace qualifier verifies
the exact 0/1/2 then 2/1/0 order, four fields per intermediate and a rendered
capture for every episode, pinned to current ROM/graphics bytes.

The trace exposes an entry grounding mismatch: the native Shang anchor is
ground minus129 while authored images extend131/132 below their anchor.
Entry frames therefore extend 2 pixels (Kano) or 3 (Sonya) below ground.
Reverse frames use the own anchor and measure zero offset. Merely changing
the shared image origin would break the correctly grounded reverse path.
An own-entry-only anchor adjustment, preserving the native palette helper,
cadence, reverse sequence and final ground_ochar behavior, is still needed.
MORPH_ART_TRACE_QUALIFICATION.json explicitly leaves entry acceptance false.

## Entry grounding corrected

An own-entry-only palette callback now calls the original morph_swpal, then
sets the entry image anchor to ground_y minus131/132. Shared image origins,
reverse path, timer and final native ground_ochar remain unchanged. The
regenerated MKST source includes both small callbacks in morph_source.py.

Hidden compile took26.42 seconds with no window. Runs323/324 passed the
full current morph qualifier on both sides. The art trace also passed:
all18 pose episodes per side retain exact forward/reverse order and four
fields each, with zero measured ground delta for every entry and reverse
frame. The previous 2/3-pixel entry error is resolved in this bounded test.
Three source/header/palette/pixel tests pass. Final costume/transition visual
acceptance and wider gameplay/interruption/rebuild acceptance remain open.
Earlier reports stay historical for the new program link; no release made.
