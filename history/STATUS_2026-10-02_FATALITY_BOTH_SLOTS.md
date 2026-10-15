# Current both-slot fatality checkpoint — not a finished release

The playable candidate remains `diagnostic_v680_native_pit_initial_cache`.
`PLAY_LATEST_TEST_BUILD.cmd` points there. No executable, payload, gameplay
source, production CMD or release ZIP was changed by these checks.

Six fresh input-only cases supplement the two previously verified P1 cases:
P2 Kano versus Sonya/Sub-Zero; P2 Sonya versus Raiden/Sonya; P1 Kano versus
Sub-Zero; P1 Sonya versus Sonya. Each earns two genuine native round wins,
with ten native damage stores totaling 322 damage, before its own fatality.
There are no health, identity, position, action or ladder writes and no cheats.

The latest independent v11 verifier passes all six cases. It checks actual
physical-slot identities, native FIFO publication, complete observed own and
victim composites, separate skeleton/orb effect ancestry, facing, source/cache
descriptors and native pointer retirement. 1,344 saved drawing passes match
352,321,536 indexed VRAM words and 136,550,400 displayed pixels. Thirty held
transition samples bind actual full VRAM, palette, display registers and PNGs;
these are explicitly NOT drawing-pass replays. All 961 consecutive actor states
per case and four original halfword pointer-retirement stores are retained.

35,008 applicable palette entries match their actual original stock victim or
own fire palette source. Sub-Zero's headless victim colors pass in both slots;
Sonya's burning-victim colors pass in stock and mirror cases. This does not
establish all donor-art fidelity or imported normal-palette acceptance.

Twenty-five focused baseline/corruption tests pass, including wrong physical
slot, facing, orb descriptor/type, victim palette/bank/alternate selection,
palette truncation, effect parent/Main/roster/native owner, and partial or
wrong-winner retirement. Captured inputs were not edited for a pass.

Evidence: six v693-v695 captures, `verification_v11.json` in the P1 Sonya mirror
case, and terminal v696 regression_v2.log. Prior P1 v691-v692 proof is separate
and preserved. One tested individual fatality per character is NOT complete
finisher or full-port acceptance. Native curtain wipes can retain old arena
pixels deliberately after actor retirement; victory text is not scene teardown.

Remaining scope includes more victims/alternate palettes and contact/timing/art
and audio fidelity, remaining finishers/cinematics, wider combat/CPU/interrupt
and KO paths, secret stages/cameras, genuine complete towers/bosses/continues/
reselection/endings, then final regression and a matching release CMD/ZIP.
No material data was deleted.
