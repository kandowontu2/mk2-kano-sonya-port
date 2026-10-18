# Native head-clap table fix: program034F

The previously reported16-entry clapped_lineups defect is source-fixed,
not yet runtime-fatality-qualified. prepare_game_candidate.py now appends
three explicit rows after verifying the original size, preserving all16
original entries: Jade(-96,0), Kano(-96,8), Sonya(-96,7).

match_ani_points copies Jax's world X/Y anchor. Jax's ground offset139
minus own131/132 gives8/7 vertical compensation, preserving body bottoms.
Horizontal spacing follows the standard96-pixel native lineup; contact
with authored poses still requires visual approval.

Hidden game rebuild succeeded31.48s with286 no-window checks. Program SHA256:
034F1179440C024A041A330F349A5F8F6C1EF3B919DC1FB701115223C15CB4F7.
qualify_common_table_link.py verifies all38 signed linked words atff8af4f0
and exact19*32-bit extent before do_tongue. The scanner reports84calls,
15short/59capacity-covered/10unresolved. Arbitrary indexing remains open.
115 selected tests pass, including original-row preservation and ground
anchor arithmetic. All26-chip verifier tests read the actual current684
archive, not the intentionally older development patch roundtrip.

Stock-MAME684 is ordinary baseline smoke, not own-character coverage.
685 uses select-new: its trace contains71 sampled mode2 Kano/Sonya rows,
then74 Kano/Baraka rows. Both runs exit normally, not timed out. Neither
proves Jax head-clap completion, so do not claim fatality runtime approval.

Source reproduction audit finds no structural difference for MKDEATH;
the existing MKSOUND structural difference and lexical differences in28
files remain reported. No new clean-rebuild claim is made. Development
ZIP/launcher still contain earlierF650 bytes and need regeneration after
qualification. HistoricalF650 move/campaign results do not automatically
qualify this new program. No custom emulator/driver changes were made.

## Current034F runtime qualification

qualify_clap_runtime.py passes686(Kano/P1 performer),688(Sonya/P1),
689(Kano/P2 performer),690(Sonya/P2). All four exit normally and verify
the actual26 runtime chips, stock MAME hash, frozen input-only controller,
two naturally earned KOs, own victim identity, all seven body poses,
native death flag1→65535, next ladder transition and later live combat.
116 selected tests pass, including the physical release-command contract.

Kano KO frames4139/5052, native start5165/completion5353; Sonya4127/4976,
start5090/completion5278. Each side has177 exact-field Kano grounding
observations or178 Sonya observations. Performer completion intentionally
precedes the final parallel victim collapse by several fields; all seven
poses must occur before the next screen, not before that performer flag.
Sparse samples and corpse objects spanning a ground_y change are not used
to infer grounding. No guest state, AI, health or outcome was forced.

687 was an unsuccessful controller test: a fresh LP press in the finish
window ordinarily killed nearby Sonya before the release-only fatality.
It has no qualified head-clap claim. The controller now starts LP charge
before the KO, retaining it through the physically entered F,F,F command
and releasing afterward. Native jx_lp_open requires elapsedLP>=40h and
forbids the other attack buttons. Game bytes remain unchanged034F.

Sonya/P1 upright and final-collapse screenshots were inspected: own body
art and grounded corpse are visible. This is not comprehensive visual or
audio approval. Exact effect-process cleanup and fresh move/finisher
regressions remain open.

## Clean build and development patch refresh

The earlier pre-refresh package statements above are historical. Current034F
clean assembly rebuilds130 objects without importing any; all four program
parts match the working build. All26 independently rebuilt/copied chips match
stock run690. Ending, cast and ladder linked records were refreshed for034F.
The development IPS package now includes the head-clap native source fix and
tests. It remains explicitly unfinished, with no full campaign, comprehensive
regression, final release or GitHub publication claim. The old generated ZIP
and roundtrip were hash-validated and replaced, not kept as extra archives.
