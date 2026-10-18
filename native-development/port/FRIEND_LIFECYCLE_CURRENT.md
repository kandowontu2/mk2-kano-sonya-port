# Current native Sonya Friendship lifecycle

Stock-MAME runs 536 (P1 Sonya) and 537 (P2 Sonya) completed normally on the
current native program and SoundP bank. All 26 actual ROM bytes were verified
by qualify_finisher_rejoin.py before lifecycle qualification. No game writes,
forced win/state, custom driver or visible emulator window was used.

The appended friend_lifecycle.lua observer walks the complete active process
list each field with pointer/cycle bounds. It counts saved A9 contexts inside
the actual linked chicken animation table and saved wake PCs at the completion
helper's post-sleep instruction. Addresses derive from current MAP/LST plus
the relocated MOVI operand in the actual linked program. MAINEQU/MPROC define
the observed saved-register offsets. Source/listing/map hashes are pinned in
each FRIEND_LIFECYCLE_QUALIFICATION.json.

Both sides showed the completion context for exactly 128 fields, then none
after native completion. Dance context was present during the performance,
then absent from selection field 6502 through the entire fresh match interval
7053–7652 (600 fields). No chicken sound commands occurred after selection.
Last commands were field 6478 for P1 and 6414 for P2. These are command-stop
observations, not proof of sample-tail silence.

Both rematches also passed true-character identity, full initial health,
live combat damage, death/winner reset and 78,000 actual hardware RGB palette
comparisons each (156,000 total). This finite check excludes the observed
Friendship contexts persisting into these fresh fights; it is not a blanket
proof against every process leak. Full audio-tail/mix and complete campaigns
remain unverified. No playable ROM change or new release was made.

Reproduce qualification after a completed run:

    qualify_finisher_rejoin.py stock_wolf_game536
    qualify_friend_lifecycle.py stock_wolf_game536

The equivalent mirrored evidence is in stock_wolf_game537.
