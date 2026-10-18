# Current2219 native Friendship audio pair

stock_wolf_2219_audio_native and stock_wolf_2219_audio_control both finish
exit0/not timed out. Each uses unmodified stock MAME and read-only physical
inputs. Native run uses actual current SoundP; the control is deliberately
diagnostic, with only chicken-playlist volume operands muted. It is not a
release sound bank. The control's source/ROM qualification passes.

Current program/graphics/native-or-explicit-control sound bytes, frozen
observer, native DCS register writes and normal earned Friendship qualify
in generated_dcs/DCS_CHICKEN_MATCHED_EVENTS.json.39 matching cue events,
all four variants, result-cue cadence and end cleanup are checked. No host
sample device is used.

generated_dcs/DCS_CHICKEN_CURRENT_CONVERGENCE.json reads only a fixed240000
sample window: five seconds beginning one second after the final cue.
Native/control PCM is exactly identical there (max/rms difference0), with
native RMS278.879575354668, non-silent. This is bounded post-cue convergence,
not individual full-tail or entire overlapping-mix acceptance.

Older6AE0 isolated-track/full-mix diagnostics remain historical, not current
2219 runtime proof. No ASM/ROM/AI/game-rule changes were made for this pair.

Fresh2219 isolated-track1/2/3 recordings are now collecting sequentially,
hidden/BelowNormal. Each uses an explicitly diagnostic sound bank and the
same physical Friendship scenario. The existing current muted-control WAV
will be shared for comparison if native cue/timing gates pass. No isolated
tail pass is claimed before terminal and event/held-out analysis checks.
The isolated analyzer bounds each PCM read below48000 samples; it never
loads a full match into floating-point arrays. These banks are not release
payloads and do not replace current SoundP.

Terminal update: all three recordings and analyses exit0. Native event/
current-program/graphics/explicit-diagnostic-sound gates pass against the
current muted-control recording. Independent disjoint pre-next-command
tails exceed0.98 correlation in10/10 track1,13/13 track2 and9/9 track3
evaluable cases. Tracks1/2 observe all four uninterrupted variants;
track3 observes0/2/3, so variant1 still needs the mirrored diagnostic.
Legacy tail metrics include alignment-search samples and are not used as
independent validation. Preempted tails and the production overlapping
three-track mix remain unaccepted. No emulator remains from this batch.

Mirrored update: stock_wolf_2219_audio_p2_track3 and matching muted control
finish normally. Current-byte/native-event gates and bounded analysis pass:
9/9 independently evaluable tails exceed0.98; all four uninterrupted variants
are observed. Across the four isolated diagnostics,41/41 evaluable independent
pre-command tails exceed0.98. The named missing variant is now covered.

Current production-minus-muted PCM compared with the sum of the three
isolated-track-minus-muted recordings gives correlation0.9999028731477925,
residual RMS0.8881187870888836 PCM16 units and max residual12. This uses zero
fitted parameters and16384-sample chunks. It supports finite native track
superposition, not exact equality or every-audio certification. See
DCS_CHICKEN_TRACK_SUM_DIAGNOSTIC.json. All recording/analysis jobs are terminal.
