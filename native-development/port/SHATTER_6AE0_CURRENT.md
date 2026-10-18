# Current native deep-freeze/shatter victim checks

Four fresh9000-field stock-MAME runs complete normally on the exact current
26-chip ROM set: stock_wolf_6ae0_shatter_{17,18}_p{1,2}. Each physically earns
two round KOs, enters the original deep-freeze command, walks into range and
enters the native shatter follow-up. No health/state/result writes, cheats,
custom driver or production ASM/ROM/package changes. Runs are hidden,
BelowNormal and sequential.

All four show143 frozen victim fields after the second KO, own body identities,
65 native fatality fields, then a native completion field immediately after.
The own legs image remains for40 fields on victim-player2 or41 on player1 and
is still selected at completion. Missing-root/illegal-opcode recovery, Lua
errors and fault markers are absent.

The verifier now requires four distinct explicit actor/side profiles, checks
all26 actual ROM chips and existing source contracts, and pins current
verifier/helper/map/MKDEATH sources, frozen observers, receipts, both traces,
logs and sampled superfreeze captures. It no longer silently defaults to
199-era builds. SHATTER_VICTIM_QUALIFICATION.json records the current runs.

Sonya victim-player1 completion capture superfreeze_05367.png was individually
decoded and inspected. This is one sampled view, not whole-fatality visual/
ice-art, sound, edge/interruption or original-roster regression acceptance.
The old standalone deep-freeze-without-follow-up report remains historical;
these new cases verify freeze followed by native shatter completion.

All280 local tests pass. Whole-port/release flags remain false. No emulator or
compiler remains running after completion.
