# Three-track native audio isolation

Player-two follow-up now fills the previously unobserved track3/variant1 cell:
all nine independent track3 tails pass above0.98, with all four variants present.
Its native/muted pair also verifies39 matched commands and an identical fixed
five-second post-cue PCM window. See CHICKEN_P2_CURRENT.md. The table below is
the original player-one sequence, not the combined observation coverage.

All recordings use the current production 6AE0 game program, stock MAME0.289,
the same frozen physical controller and identical39 cluck command events.
The production sound ROMs and development release ZIP are unchanged.

Track2 and track3 diagnostic banks were compiled hidden/BelowNormal in15.23
and17.50 seconds, with no compiler window. Their455 compressed inputs and
sample payload bytes are unchanged; only eight playlist volume operands and
generated checksums/date headers differ. Both banks qualify before runtime.
Both9000-field emulator runs exit0 without timeout. During track2 playback,
MAME was observed BelowNormal, window handle0, working set200MiB.

Corrected isolated validation excludes the entire alignment-search window and
ends before the next same-track command. At least1024 independent samples are
required per evaluated tail:

| Track | Commands | Evaluable tails | Above0.98 correlation | Variants observed |
| --- | ---: | ---: | ---: | --- |
| 1 | 15 | 10 | 10 | 0,1,2,3 |
| 2 | 15 | 13 | 13 | 0,1,2,3 |
| 3 | 9 | 9 | 9 | 0,2,3 |

Track3 variant1 is not exercised by this recorded command sequence. No coverage
is inferred for it. Seven short/interrupted intervals across tracks1/2 do not
provide independently evaluable pre-command tails under this search procedure.

## Native-recording superposition

`inspect_chicken_track_sum.py` compares production-minus-all-muted PCM against
the sum of the three isolated-track-minus-all-muted recordings. This uses no
fitted gain, phase, latency, filter or source-reference parameters. Every event
proof pin is checked first, including actual ROM verification performed by the
event inspector; all controls must have identical complete WAV hashes.

Across500755 samples from the first cluck command through one second after the
last, correlation is0.9999028731477925, residualRMS0.8881187870888836 PCM units,
maximum absolute residual12, and392388 samples match exactly. Relative residual
norm is0.01396665397432902. Processing is in16384-sample chunks, not full-match
float arrays. Results and input/source hashes are in
`generated_dcs/DCS_CHICKEN_TRACK_SUM_DIAGNOSTIC.json`.

This is much stronger agreement than the source-reference additive model,
which had relative residual about0.168. It points toward reference alignment,
resampling or replacement modelling as the larger discrepancy, rather than a
large three-track native mixing error. This is an inference, not identification
of the remaining PCM rounding/mixer mechanism. Whole-game audio, every track/
variant combination and the full port are not certified by this check; all
release acceptance flags remain false.
