# Reptile victim-table memory repair; port remains unfinished

Current experimental candidate: `diagnostic_v860_native_reptile_victims`.
This is not a final release. Existing production executable, launchers and ZIP
have not been replaced. No old evidence/builds were deleted in this turn.

## Actual failure and repair

The current v786 Sonya P2 natural campaign resets at field 79,346 during
Reptile's tongue/head-eating fatality. The read-only v858 replay reproduced
the same failure. Native victim-table FF8C9900 lacks rows for true IDs 17/18;
Sonya reads executable words FF84,0D5F,2710,FF84 as X,Y,animation,offset.
Animation 2710 ultimately supplies A001F608 as a composite list. The original
FF838860 body-cache store overruns the cache, writes 7E7F into both health
fields and corrupts the global actor/schedule/state pointers. This is a real
native game reset, not a host emulator exit or a harmless observer reentry.

The source repair allocates an independent 19-row native table at FFFD4000,
preserves every original ID-indexed byte, adds real Kano/Sonya high-hit rows,
and changes only the original FF8C8A70 table operand. No renderer bounds
workaround, ID proxy, collision/difficulty/health/AI assistance or fatality
timing replacement was added. Guest-program comparison proves exactly this
data/pointer change: 123 changed bytes. The .mdata art payload is unchanged.

## Evidence accepted

- `audit_v864_sonya_p2_reptile_replay`: cold P2, physical inputs only,
  1,800 native emulated seconds, terminal exit 0. Its 37,537 original
  input/state/combat records before the old fault are byte-identical to v858.
- Actual original runtime reads all four independent Sonya row fields at
  field 79,346. Its interpreter gets FF024FF0, a properly terminated own
  high-hit stream, rather than arbitrary data.
- Original native fatality completes 90 fields later. Real paid continuation
  and reselect return Sonya ID18 to eight subsequent matches. All 13,659
  observed health writes use their exact original physical-slot writers;
  there is no body-cache global write or machine reset through field 98,473.
- `audit_v865_reptile_native_overrun_checked`: bounded memory-repair proof,
  including 16 snapshots of the actual finisher.
- `audit_v866_reptile_native_overrun_units`: 13 verifier tests pass; mutations
  reject original table bytes/code changes, wrong native row/PC/animation,
  changed input chronology, missing completion/reselection, resets, boot
  snapshots misidentified as gameplay, and concealment of remaining Liu art.

`audit_v861` has the same successful game repair, but its first diagnostic
observer incorrectly treated its own boot ROM dump as the start of the
fatality. The stronger gate deliberately fails that capture in `audit_v862`.
Both are preserved, not relabeled as visual proof. v864 scopes the observer to
the exact native consumer, true Reptile owner, defeated true victim and FFFF
mask, and captures the real finisher instead.

## Remaining fidelity defects exposed, not accepted

The detached-head main-61 streams still contain Liu Kang's native descriptors
(FFB4A4B0 first frame) for both imported fighters. v864 observes Sonya's
actual head descriptor at fatality age32, not just a builder report. The
headless/body appearance also remains incorrect in the actual age40/80
screenshots. Native headless palette dispatcher FF90C800 still indexes the
short original FF90C900 table: true IDs17/18 fetch non-pointer color data
(10842108/7FB80C63 and 7F977FC0/7C607CE0). The visible green victim palette
needs an independent native-table/art repair, not acceptance as finished.

`audit_v863_original_detached_head_candidates` is read-only original MK3
component inspection; it did not install cropped/generated replacement art.
No complete Reptile finisher-art acceptance is claimed. Kano's new row is
statically verified but still needs real native runtime proof. The two
physical slots and other stock-performer victim paths remain in scope.

Earlier v786 UI, floor-shadow, human-special and CPU-grab proofs remain
historical evidence for that exact build; they are not automatically
upgraded to whole v860 acceptance. Neither fighter has a verified complete
native tower/boss clear/ending. Final art/audio/gameplay regression, native
victim finishers, other UI flows and final packaging remain unfinished.

## Next work

Correct both true-ID headless palette rows and the real detached-head/body
assets, then test the complete original Reptile sequence with both fighters
in both slots. Preserve original stock victim behavior and prove full
native continuation/cleanup, rather than only absence of a crash.
