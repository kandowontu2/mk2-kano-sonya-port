# Current native cluck track-1 isolation

This diagnostic bank preserves the production game program, all455 compressed
inputs, event timing, track routing, priorities and play commands. Only eight
track2/3 volume operands are muted; track1 remains audible. The production
development patch ZIP and sound ROMs are not changed.

The original PLBUILD compile completes hidden/BelowNormal in18.787 seconds,
without a window. The location map differs only in its generated timestamp.
U3/4/5 sample payloads from0x0e onward are byte-identical; their14-byte
headers differ only in date/checksum, with header checksum sum preserved.
U2 differs in nine bytes (eight volume operands plus checksum). The explicit
metadata checks reject any sample/map-body alteration. Both track1 and the
original all-muted controls qualify; no metadata differences are described
as literal whole-ROM identity.

stock_wolf_6ae0_audio_track1 and audio_track1_muted complete normally using
stock MAME/current6AE0 game ROMs, identical frozen physical controllers and
matched event timings. Only one emulator runs at a time, hidden/BelowNormal.
The39 recorded cluck commands include15 track1 calls. Paired PCM analysis
uses sub-second windows, never full-match floating-point arrays.

The original nine uninterrupted-tail scores exceeded0.98, covering all four
variants, but that legacy metric excluded only the winning4096-sample prefix,
not all samples inspected by the alignment search. It is not an independent
held-out result. The corrected disjointPreCommandTail fields exclude the full
8895-sample search interval and stop before the next same-track command.
Ten clips have at least1024 remaining validation samples; all ten exceed0.98.
The other five intervals are too short for this independent check. The six
legacy low-scoring full tails all have another same-track command before the
reference ends; this does not prove the exact replacement timing.

This supports same-track voice replacement as a missing term in the old
additive-full-tail model; it is not independent proof of every DSP/mixer
mechanism or production three-track overlap acceptance. A preemption-aware
production model using frozen additive-prefix alignments has now been tested:
it did not materially reduce residual error. See CHICKEN_PREEMPTION_MODEL_CURRENT.md.
All release/whole-port flags remain false.
