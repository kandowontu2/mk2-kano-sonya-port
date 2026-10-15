# v1517 native arena coverage in progress

No playable game, source, ROM payload, control settings, health, positions,
difficulty, stage, RNG or CPU choices changed. v1517 remains the development
playtest launched by PLAY_CURRENT_V1517_TEST_BUILD.cmd.

The new v1560 campaign drawing observer layers read-only native FIFO, cache,
DMA/CPU-write, display-flip and compressed shadow-row observations over v850.
v1562 independently strips the added observer and requires the entire remaining
source to equal the immutable accepted v850 physical-input policy byte for byte.
Cold selection, combat buttons, actual wins/losses, paid continues, original
health-store provenance, true human IDs and original-derived CPU schedules are
checked by the unchanged campaign contract, not supplied as diagnostic writes.

Two fresh 65-second smoke captures are terminal and independently verified:
Kano P1 and Sonya P2. v1563 reconstructs all 30 saved scanouts exactly, with
source-bound graphics/composites/cache/FIFO ownership, native palettes, indexed
VRAM and actual display flip. All 790 observed imported shadow components and
19,729 original shadow-row copies verify. This is Dead Pool coverage only;
all-nine-regular-arena and all-move-phase grounding claims remain false.

Two 900-second campaigns were started using the unchanged validated observer:

- audit_v1564_native_arenas_kano_p1; command session 20824.
- audit_v1564_native_arenas_sonya_p2; command session 37741.

Both handles were re-polled as live, and both were observed visiting native
arena IDs 0,1,2,3 through normal gameplay. Do not restart them because a polling
call times out. Re-poll these handles or inspect authoritative process state.
Their changing logs/captures are not immutable completed evidence yet. When
terminal, run verify_current_native_arenas_v1563.py against each folder and save
to a new non-existing output path. The report records observed arena IDs and
explicitly distinguishes all-nine sampling from all-move-phase/full-port proof.

Rendered sole observations are retained, not interpreted as universal ground
contact acceptance: camera motion, pose recovery, clipping and render timing
must be accounted for before using a body-mask bottom as a physical floor line.
The broader arena checks, other physical slots, remaining AI/audio/finishers,
completed towers/bosses/endings/secrets, final ZIP and old-build cleanup remain
open. No additional old build folders were deleted in this work.
