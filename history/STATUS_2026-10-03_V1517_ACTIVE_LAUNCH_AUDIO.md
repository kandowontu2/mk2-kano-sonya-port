# Current playtest: v1517; full native-integration goal remains open

Run PLAY_CURRENT_V1517_TEST_BUILD.cmd. Its actual ordinary CMD boot passed from
another working directory, with no diagnostic autoboot or checksum warnings.
The checker binds the executable, payload, exact manifest and external voice
assets. Previous v1411 CMD and controls remain unchanged. The two existing
control CFG files were copied into v1517's separate play directory; that copy
can be customized independently. This is a development playtest, not a release.

Candidate EXE SHA256:
B0142C979C56C3906E8645D47CBE5CBE37D7AB33931A3447E3A6911DEC4911E8.
Payload remains 5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D.

## Concrete implementation and verification

The voice cleanup timer now stays unscheduled while neither physical player
owns launch playback, starts at actual native square/bicycle launch, and stops
when both owners clear. One player's cleanup does not cancel the other's timer.
The original MAME timer API sets enabled=true even for adjust(never); the final
candidate correctly tests expiry==never when arming. v1514's incorrect guard
was not accepted or promoted. The final machine source has exactly three
timer-only edits relative to v1473; driver, header, assets, native graphics,
CPU/frontend and the entire observed guest program are unchanged.

Fresh v1517 results:

- v1520: four real-input finite voice-channel cases, square/bicycle in both
  slots, exact original lengths, full source playback and owned cleanup.
- v1524: all 52 bounded human move/contact/block/miss/air/recovery cases pass;
  every original native event and all 156 before/recovered/final screens match.
- v1522: all four Kano/Sonya physical-slot selection-to-first-match checks pass,
  including animation, backdrop, thick blinking borders/player numbers,
  immediate portrait/pose teardown, native ladder IDs and name shadows.
- v1523: all four Dead Pool mobility/grounding/floor-shadow cases pass, with
  original compressed rows, soles, palettes and exact sampled native raster.
- v1525: three genuine CPU leg-contact cases pass, covering both CPU slots
  and both new human fighters; 263 full native scanouts are independently exact.
- v1535: three actual incoming-hit audio cases pass: square P1 and bicycle in
  both slots. Each takes the original 40-damage uppercut, owned voices stop
  mid-cue by the next callback, native knockdown/recovery and ordinary follow-up
  work. Twenty-four in-memory corruptions are rejected. P2 square attempts
  did not damage Sonya, so P2 square interruption is NOT accepted.

## Important unresolved CPU evidence

The repeated P1 Sonya CPU vs P2 Kano fixture still has zero completed leg grabs
on v1473 and v1517, while ordinary combat finishes. It is not a freeze and is
not accepted as repeated-grab coverage. A fresh v1411 baseline reproduces its
two completed grabs at frames 2746 and 2856 with the same physical inputs.
v1540 locates the first old/new native-state divergence at frame 2141, after
both candidates' square-wave launch at frame 1872. The always-polling v1473 and
active-only v1517 shared CPU states are identical. The idle timer therefore
has NOT explained or fixed this discrepancy. Next investigation should inspect
the launch-code/return-state or subsequent native AI/RNG path, not force CPU
choices, health, IDs, positions or ladder state to obtain a green fixture.

## Cleanup and restoration

The discarded v1514 intermediate build folder was removed: 110,569,233 logical
bytes, 44,445,000 allocated bytes (about 42 MiB). Its frozen source, build log
and manifest remain under audit_v1538_discarded_timer_build_cleanup/preserved;
its executable regenerates with the retained v1513 builder and v1512 stage.
Current/previous playable builds, source and launchers were hash-checked intact.
This is additional partial cleanup, not all obsolete builds or several GiB.
Historical canonical machine/driver/header and installed mkport.exe are restored.

## Still required for the full goal

Resolve/understand the repeat-CPU discrepancy; verify P2 square interruption,
simultaneous/repeated/KO/round audio, remaining native audio/choreography and
the complete AI repertoire. Extend shadows/grounding to other arenas and move
phases; finish victim/finisher coverage, actual full towers, bosses, continues,
endings, secrets and cinematic teardown. Final release ZIP and larger old-build
cleanup remain open. Neither bounded green checks nor this playtest CMD prove
that Kano/Sonya are natural official characters in every aspect yet.
