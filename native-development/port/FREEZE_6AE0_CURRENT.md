# Current native freeze/thaw checks

Four fresh9000-field runs complete normally with exact current26 ROM chips,
stock MAME0.289 and frozen read-only physical controllers:
stock_wolf_6ae0_freeze_{17,18}_p{1,2}. One hidden BelowNormal emulator runs at a
time; no production ASM, ROM, AI or sound changes were made.

The linked19-entry frozen-palette table points at each own65-color palette.
Both victims retain own body shapes for160 contiguous frozen fields, use a
distinct palette selector, then restore the pre-hit selector and return to
native stance. Missing-body/illegal-opcode recovery and Lua errors are absent.
The report pins current verifier/helper/map/generated-palette source, actual
receipts/frozen controllers/traces, logs and all seven freeze160..400 captures
per case. It no longer silently defaults to158-era test folders or accepts an
incomplete two-case set. Both identities/both victim sides are required.

Kano-player2 freeze200, Sonya-player1 freeze200 and Kano-player2 thaw400 PNGs
were individually decoded and visually inspected: own bodies remain visible,
ice tint is visible, and Kano's normal colors return in the thaw capture.
This is sampled visual review, not whole-animation/all-palette/lighting or
full-game audiovisual acceptance. Hardware RGB content is not independently
observed by this older probe; palette-selector restoration is the tested gate.

All268 local tests pass, including finite actor/side coverage and unsafe-prefix
rejection tests for the new sequential runner. FROZEN_VICTIM_QUALIFICATION.json
retains false whole-port/release flags. No emulator/compiler remains running.
