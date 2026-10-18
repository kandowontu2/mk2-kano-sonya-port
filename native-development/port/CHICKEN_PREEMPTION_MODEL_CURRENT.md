# Same-track replacement diagnostic

## Independent-window correction

The isolated inspector now excludes the entire 8,895-sample alignment search
window, rather than only the winning 4,096-sample prefix. Older tail fields
are retained as explicitly labelled legacy diagnostics, not independent
validation. Validation also stops before the next same-track command, without
fitting a replacement latency. Ten clips have at least 1,024 remaining samples;
all ten disjoint pre-command tails correlate above 0.98. Five short intervals
cannot provide independent pre-command validation under this search procedure.
Four boundary tests cover search exclusion, early/late interruption and short
references. This strengthens source playback evidence but does not identify
the production mixer or certify interrupted whole tails.

The current production 6AE0 program and packaged ROM patches were not changed.
The track-1 isolation report observes nine uninterrupted tails, all above 0.98
correlation, covering all four source variants. Six other clips have another
same-track command before the expected reference end. This supports investigating
voice replacement, but does not prove the complete native mixer behavior.

`inspect_chicken_joint_mix.py --full-dance --matched-control --track-preemption`
now tests truncating each source reference at the next same-track onset. Onsets
and phases remain frozen from the earlier prefix-only search; gains use only
training prefixes. No held-out samples select the replacement boundary.

For 214,781 held-out samples, the replacement model gives correlation
0.992711679539291 and relative residual norm 0.16882248900323. The untruncated
baseline gives 0.991930841342522 and 0.16844627462174 respectively. Correlation
improves slightly but residual error does not: replacement alone, using these
previously fitted onsets, is insufficient. The earlier prefix fits themselves
used an additive model and may be biased during interrupted/overlapping clips.

The separate TRACK_PREEMPTION diagnostic report retains false release/scene
verification flags. The next useful check is replacement-aware prefix alignment
or additional isolated-track observations, not changing native audio samples or
relaxing acceptance thresholds. This diagnostic does not certify all game audio.
