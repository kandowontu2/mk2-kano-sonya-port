# Current-link Blade Swipe / Bicycle Kick

Physical-input runs329/330 on stock MAME use the current morph-entry-ground
fix ROM. Both qualifiers now verify actual archive program bytes/current
graphics sockets, frozen observer hash, mirror profile, read-only guest
observation and absence of Lua errors. Each observed9000 fields with no
missing-animation markers. Per-run qualification.json pins current sources.

Blade run329 (Kano P1):17 activations, all10 authored body poses, far whiff
and cleanup,26 hit damage,3 blocked damage. A physical11-damage interruption
retires the attached trail within two observer fields and it stays absent
through the tested post-interruption window.

Bicycle run330 (Sonya P2):11 starts and352 paired fields; all9 body poses,
own Kano victim art, victim in front at48/-32 relative offset after contact,
matching velocities in both phases,22 hit/3 block damage, incomplete-command
rejection, duck/far miss recovery and both actors returning to stance.

These cases are bounded, not all victims, bosses, stage edges, airborne
matchups, AI or final audio-mix acceptance. Mirrored current-link refresh
and broader gameplay/fatality/campaign/release checks remain unfinished.
No gameplay code changed during this verification.

Mirrored refreshes331/332 also passed the same current-byte-pinned qualifiers:
Blade17 activations/10 poses with26/3 damage and interruption cleanup; Bike11
starts/352 paired fields/9 poses with22/3 damage, matched velocities, correct
front-of-owner offset and tested recoveries. These cover opposite player
sides for the defined fixtures, not every possible matchup or spacing.

## F650 current-program refresh: runs610/611

Both runs complete normally at9000 fields without missing markers/Lua faults.
The qualifiers now verify all26 current ROM chips and pin themselves plus
the shared byte verifier. Its five current-ROM/corruption integration tests
and eight synthetic patcher safety tests pass; no ROM files are mutated.

Blade610 (Kano P1):17 activations, all10 body poses, far whiff and cleanup,
26 hit/3 block damage. An11-damage physical interruption retires the attached
trail within two observed fields. A current whiff screenshot (blade_03690)
was inspected and shows own Kano/Sonya sprites and the authored blade effect;
one image is not full animation/style acceptance.

Bike611 (Sonya P2):11 activations and352 paired fields, all9 body poses,
own Kano victim art, front-of-owner48/-32 offset after first contact, matched
velocities in both phases,22 hit/3 block damage. Incomplete command rejection,
duck/far miss recovery and the first pair's release/return to stance pass.

These refreshes do not cover every boss/victim/arena/AI or native audio voice.
No native game source or program/sound/graphics ROM changed.

## Opposite-side F650 refresh: runs622/623

Kano P2 Blade622 passes17 activations/all10 poses,26 hit/3 block damage,
far-whiff cleanup and attached-trail retirement within two fields after an
11-damage interruption. Sonya P1 Bike623 passes11 starts/352 paired fields,
all9 poses, front-of-owner48/-32 offset and matched velocities,22 hit/3 block
damage, incomplete-command rejection, duck/far misses and paired recovery.
Both exit normally at9000 fields with all26 actual ROM chips verified and
no missing markers/Lua faults.

The two verifier CLIs now require explicit current-run names and derive
mirror role from each frozen receipt, rather than defaulting to historical
run names. These commands pass on both current player-side profiles:

    python qualify_blade.py stock_wolf_game610 stock_wolf_game622
    python qualify_bike.py stock_wolf_game611 stock_wolf_game623

Behavior assertions were not relaxed. This closes both physical sides of
the defined own-victim fixtures, not all bosses/victims/arenas/interruptions
or audio. No native source/ROM/emulator changed.
