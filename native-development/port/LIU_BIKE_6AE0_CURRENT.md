# Current native Liu bicycle-kick victims

Four fresh9000-field recordings complete normally using current26 ROM chips,
stock MAME0.289 and frozen physical read-only controllers:
stock_wolf_6ae0_liu_bike_{17,18}_p{1,2}. One hidden BelowNormal emulator at a
time; no production ASM, native game rules, ROM or development ZIP changes.

All four show68 native bicycle-kick action fields, real victim damage, all five
own victim poses and the attacker's saved pointer traversing the linked own
reaction script. Both fighters are in stance for99 consecutive post-recovery
fields. Missing markers, native illegal-opcode recovery and Lua errors are absent.

The old verifier compared current program hashes only to receipt claims. It
now verifies the actual complete26-chip archive, exact stock executable pin,
frozen controller hash and absence of guest-write code; requires the right
fixture/identity profiles and full actor/side coverage; checks paired recovery;
and pins current verifier/helper/map, receipts/controllers/traces/logs and three
sampled captures per case. LIU_BIKE_VICTIM_QUALIFICATION.json records the four
explicit current cases without claiming whole-port/release acceptance.

After all emulator recordings completed, the initial verifier attempt was
cancelled because its new per-row recovery-PC check repeated a map regex lookup
thousands of times. The lookup is now hoisted once outside the loop. Rechecking
the unchanged completed recordings with this optimized verifier exits0 in about
1.25 seconds. The initial runner's nonzero result records that cancelled
verifier, not a failed emulator run. No gameplay was restarted or overwritten.

All276 local tests pass. Whole-animation visuals, audio tails, edges and
interruptions are not certified by this finite fixture. No emulator/compiler
remains running after completion.
