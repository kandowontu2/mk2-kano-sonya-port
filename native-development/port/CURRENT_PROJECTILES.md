# Current-link Knife / Ring checks

Runs333/334 passed qualify_projectiles.py on opposite player sides, using
stock MAME and the current morph-grounding-corrected ROM. Each run observes
9000 fields. Both moves activate19 times: Knife spawns after3 fields, Ring
after15; native projectile identity/art,22 hit damage,5 observed block damage,
wrong-direction rejection, recovery and observed cleanup pass. No missing
animation markers. All22 Knife and12 Ring shapes are observed.

The qualifier pins actual archive program bytes and every current graphics
socket, the immutable read-only observer, stock emulator and current map/
sources. Results are per-run qualification.json. No game code changed.

These do not establish all spacing, whiffs, interrupted-projectile cases,
AI/boss matchups or audio acceptance. The report's old hardcoded
nativeLaunchAudioImplemented=false has been renamed to
nativeLaunchAudioQualifiedByThisTest=false: this test does not listen to or
prove implementation of audio, so it must not make an implementation claim.
Neither full moveset acceptance nor release readiness is established.

## F650 current-program refresh: runs612/613

Both normal and mirrored runs exit normally at9000 fields on the current
F650 program. The verifier now checks all26 actual chips, including current
sound/original MKII graphics, and pins itself plus the shared byte verifier.
All existing behavior assertions remain unchanged.

Each side profile observes19 Knife and19 Ring activation episodes; first
spawn latencies are3 and15 fields respectively. All22 Knife/12 Ring shapes
are observed with own projectile IDs/art.22 hit damage,5 observed blocked
damage, initial wrong-direction rejection, recovery and observed projectile
cleanup pass. No missing markers or Lua faults. These are paired finite
fixtures, not every spacing, whiff, interruption, boss or audio case.
No native source or ROM changed; full moveset/release flags remain false.
