# Native ring startup/interrupt fix staged; full natural-roster goal remains open

Playable CMD remains PLAY_CURRENT_V1250_TEST_BUILD.cmd, launching v1250.
The fixes below are NOT yet promoted to that launcher or a release ZIP.

## What changed

The preceding status-only goal turn made no implementation progress. Its
reports and launcher were revalidated before this continuation resumed work.
Both v1306 ring miss full-render checks now pass (v1312). Together with the
previous hit/block checks, this covers six ordinary ring cases on v1306.
The preceding v1293/v1297 ordinary knife/ring render family covers12 real
hit/block/miss cases. Its old mechanical passes did not establish correct
charge colors: manual review found the gold-tinted Sonya startup, and the
original-game color contract rejects24 actual old-palette samples. That is
why the native pink-palette fix was required despite those green checks.

Real close-range startup-interruption/retry tests then exposed another defect:
the ring could miss a standing opponent 63 pixels away. The original MK3
read-only close reference v1320 hits at release, before a travelling frame.
It uses a distinct startup descriptor FFA5AA10, (77,35,47,27), rather than
the narrower travelling descriptor FFA5A9A0, (108,35,36,11).

Staged candidate: diagnostic_v1340_native_ring_lookup.
EXE SHA256: A050762309CADA040B85214CCA435F10A37DD3AAA98173F2E17D12D70F034159.
Payload SHA256: 5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D.

The native fix retains v1306's source-correct pink charge palette and restoration
on the next non-charge body group. It adds Sonya's original startup rectangle
as her own native attack slot23. All 23 prior descriptor pointers and every
stock character row remain unchanged. The shared MKII collision lookup really
re-resolves the attack slot, so changing only a process descriptor was not
sufficient. No character proxy, host drawing, injected damage, loaded state,
forced position, altered RNG, or widened travelling hitbox is used.

The v1323/v1329 attempts and v1317/v1343/v1345 failed verifier reports remain
preserved. v1323 used the travel core at startup; v1329 supplied a distinct
process descriptor but the shared collision lookup still selected travel.
v1343 incorrectly assumed no ordinary follow-up jab damage; v1345 still used
the first (cancelled) entry for the retry's child-allocation timing.
v1346 explicitly distinguishes the real 40-damage uppercut, 22-damage ring,
and 11-damage ordinary jab, and the retry's own 15-field release interval.

## Verified current staged scope

v1342 independently reconstructs the entire actual one-MiB guest, binds the
compiled source/payload, preserves every byte outside the isolated additions,
and passes the native ROM audit. Compiled source is frozen in the candidate's
input_sources. Canonical historical sources and the installed emulator were
restored and hash-verified; do not mistake those historical files for the
staged candidate's compiled source.

Both v1341 cold real-input Sonya mirror cases finish at field2000, exit0.
v1346 passes both slots, including the actual normal P1 / alternate P2 costumes:

- 1,082 paired fields per case, true ID18 and native physical actor/Main owners.
- Uppercut cancels the first charge, with no first-attempt projectile spawn.
- Retry performs all five original release poses and contacts at native spawn.
- Actual native startup bounds overlap the actual opponent; damage is22.
- All seven original impact groups are drawn; no fictitious travel is required
  after an immediate close hit. Original native cleanup retires the child.
- Each case replays all334 captured full native drawing passes/scanouts exactly,
  with zero VRAM/display mismatch, and checks104 full projectile palettes.
- Both normal/alternate physical costume palettes restore correctly, including
  uppercut reactions, retry recovery, walking, jumping, and an ordinary jab.
- Charge palette has exactly its active physical reference count and no leaked
  reference after interruption (194/195 observed fields) or retry recovery.

The main agent reviewed all four v1344 unchanged full-frame contact sheets:
pink charge, original-costume reactions, close burst, cleanup and ordinary
follow-up. This is sampled manual visual review, not review of all668 raw frames.
v1349 also rejects six actual earlier close misses and14 in-memory palette/
identity corruptions through the same state/color validators. Actual evidence
remains unchanged. The v1347 counter-test failure is preserved; its harness
initially caught AssertionError but not the palette validator's ValueError.

## Still required

Next: fresh v1340 ordinary hit/block/miss and close guard/duck regressions, repeated
specials/KO interruptions, then broader authored-move and stock-character/UI
regression before updating the playable CMD. v1335 ordinary-hit captures belong
to v1329, NOT v1340, and cannot accept v1340 gameplay.

The full original goal is unchanged: remaining move choreography/audio, wider
CPU/opponents, remaining native finisher/alternate interactions, other shadow/
grounding phases and arenas, full genuine towers/bosses, continues/endings/
secrets/cinematics, final integrated acceptance and matched source/CMD/release
ZIP still need completion. Old build-folder deletion remains unfinished; this
continuation deleted no material files. No full-port or release-ready claim.
