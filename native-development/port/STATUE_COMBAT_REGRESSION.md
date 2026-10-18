# Same-link ordinary combat regression

After the separate statue palettes, current stock MAME runs207–210 test
ordinary Sub-Zero freeze for Kano and Sonya on both physical sides. Each
completed9,000 fields with true IDs/own bodies,160 contiguous frozen fields,
normal palette restoration and native thaw to stance. The freeze qualifier
now additionally checks the complete main trace for9,000 fields, missing-art
and illegal recovery, and normalized attacker/victim IDs.

Runs211–214 independently test Raiden lightning against both own fighters
on both sides on exactly the same program link. Each completed9,000 fields,
took22 damage, flashed the own frozen palette for10 fields, restored the
normal palette and returned to stance. The lightning qualifier now accepts
explicit2/4-run lists and validates flags/sides; mirrored coverage is no
longer inferred from player-two cases.

All eight use stock emulator AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3,
physical controls, read-only observations and exact current ROM/graphics
pins. No game-memory writes, custom driver, missing-art, illegal recovery,
Lua error or timeout. There was no game-code edit or compile in this step.

FROZEN_VICTIM_QUALIFICATION.json, LIGHTNING_VICTIM_QUALIFICATION.json and
STATUE_PALETTE_QUALIFICATION.json now agree on both current lane hashes:
0F6249552EEE20861FE088EEF2173354A09123AE79035B666813E9611F6481ED and
8863BEF112C7B80F7D8D85D472BC895C23AA2B648AC4790116E0680F90004009.
The statue qualifier requires those same-link four-case reports and records
their hashes before marking ordinary combat regression verified.

This closes only that narrow regression gate. Full visual polish, other
victim fatalities, original-roster controls, clean build, campaigns and
release qualification remain unfinished. No release was promoted.
