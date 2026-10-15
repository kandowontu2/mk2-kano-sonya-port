# What the tests mean

Development used overlapping scripted tests, native runtime observations,
source/dependency checks, negative mutations, raster reviews and audio checks.
There was not one fixed suite, nor does a script's existence prove it ran.

At the inventory taken on 2026-10-15, the original tools directory contained
322 `test_*.py`, 1,143 `qualify_*.py`, and 1,077 `verify_*.py` files. These 2,542
files include revisions and overlapping checks. They are not 2,542 independent
suites. The final integration decision grouped evidence into 12 feature areas
plus packaging and cleanup, or 14 requirement groups.

## Types of evidence

- Native input-only tests insert credits, navigate selection and use real
  directions/buttons. They must distinguish roster ID, live actor ID, Main
  ownership and slot state. A displayed name alone is insufficient.
- Move tests distinguish accepted input/entry from actual contact, damage,
  block, miss, interruption, recovery and later ordinary controls.
- Campaign recordings require natural native stage changes, real boss wins,
  true character identity and both own ending pages. Bot losses are not
  automatically a game regression; an unfinished recording is not a clear.
- Scalar read/write taps observe the game's own activity. An installed write
  tap that only records a store is different from a script writing guest RAM.
- Qualifiers check log context, ownership, timing and data dependencies;
  negative mutations test whether the qualifier rejects wrong evidence.
- Source conservation checks transfer only explicitly unchanged components;
  they are not a fresh runtime test of every historical case.
- Sampled screenshots are useful visual evidence but do not certify every
  possible frame, input history, palette, arena or RNG outcome.

## Historical tools require care

Some earlier diagnostic tools force health, CPU identity, ladder positions,
or other conditions to isolate a bug. Others capture large memory/media
buffers. They are retained as development source, not recommended launchers
and not proof of unassisted ordinary play. Read a script and its scope before
running it; do not bulk-run the `tools/` directory.

The recent showcase recorder uses bounded native-frame streaming, native
audio, physical controls and no guest-state writes. Its footage is edited
into labelled chapters, not presented as one uninterrupted match or ladder.
The full-playthrough recorder is a separate artifact and does not imply that
every move/finisher was demonstrated during its campaign.

Private runtime dumps, logs, reports and screenshots are not bundled in this
code-only repository. Historical status notes explain their original local
paths and limits; references are not a claim those private artifacts can be
rerun or downloaded from this repository.
