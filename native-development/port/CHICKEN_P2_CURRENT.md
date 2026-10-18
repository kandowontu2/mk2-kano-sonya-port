# Current player-two native cluck evidence

Three new9000-field stock-MAME runs complete normally on current6AE0:
stock_wolf_6ae0_audio_p2_native, p2_muted and p2_track3. One hidden BelowNormal
emulator at a time, bounded recording/analysis memory, no production ROM or
development ZIP changes. The isolated bank is diagnostic, not a release bank.

The player-two production/all-muted pair has identical frozen physical
controllers, actual current program/graphics, corresponding qualified sound
banks and39 matching cluck events. All four variants are observed. The fixed
five-second window one second after the last command is exactly identical PCM
between native/control:240000 samples, maximum/RMS difference0, nativeRMS
278.81165180697406. This verifies only that window, not every preceding tail.

The player-two track3-only/all-muted pair retains all39 command events and has
nine audible track3 calls. All four source variants occur, including variant1
which was absent from the player-one track3 sequence. All nine have evaluable
disjoint pre-command tails and correlate above0.98 after the entire alignment
search interval is excluded. Together with the existing player-one track1/2
checks this provides observed source-variant coverage on all three tracks;
it is not every timing/overlap pattern or all game audio acceptance.

Matched/mirrored/isolated proof filenames are now explicitly separated by
chicken_evidence_names.py. A mirrored matched proof cannot overwrite its
player-one counterpart. Event and isolated inspectors verify the physical
side, actual26 ROMs/frozen controls/command timing as appropriate, and pin the
naming helper. Both convergence reports remain distinct.

requalify_chicken_recordings.py rechecks all four existing control-bank
qualifications, six paired event proofs, four isolated analyses, both fixed
convergence windows and the existing unfitted player-one track-sum comparison.
All pass against current evidence/source hashes without launching MAME or a
compiler. Legacy additive-reference model reports remain diagnostics, not
acceptance.290 local tests pass. No emulator/compiler remains running.
