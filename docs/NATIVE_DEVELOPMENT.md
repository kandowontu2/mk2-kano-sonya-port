# Native developer and test source snapshot

[`native-development/`](../native-development/) contains the source-only native
development tooling:678 files, approximately3MB, including its hash manifest.
This is separate from the historical custom-driver tools elsewhere in this
repository. It contains no complete ROMs, proprietary toolchain, runtime ROM
archives, raw game assets, screenshots, recordings or bulk test-run dumps.

## Read it in this order

- Canonical compiled game changes: [`native-rom/source/`](../native-rom/source/).
- Native source guide: [`NATIVE_SOURCE_GUIDE.md`](../native-development/port/NATIVE_SOURCE_GUIDE.md).
- Physical-input observers/controllers: [`port/diagnostics/`](../native-development/port/diagnostics/).
- Stock-MAME runner and bounded ROM-cache handling:
  [`baseline/test_wolf_baseline.py`](../native-development/baseline/test_wolf_baseline.py)
  and [`test_rom_cache.py`](../native-development/baseline/test_rom_cache.py).
- Qualifications and `test_*.py` files in
  [`port/`](../native-development/port/): conditions actually checked, including
  deliberately rejected cases and narrower scope limits.
- [`FILES.json`](../native-development/FILES.json): exact snapshot hashes.

The last complete local unittest run at this checkpoint passed413 test cases.
That is not413 separately compiled builds or413 independent test suites.
Bundled standalone IPS-codec tests are a smaller five-case subset; see the
native validation document. Runtime fixtures, source/build qualifications,
unit tests and media comparisons establish different things. None alone is a
full-port completion certificate.

The side-swapped normal-combat stress checks observed29054 controlled combat
fields across12 fresh matches, requiring true character IDs and native active
human states. Earlier attempts that included CPU fights were rejected, not
counted as valid two-player evidence. Details and limitations are retained in
[`NORMAL_SOAK_2219_CURRENT.md`](../native-development/port/NORMAL_SOAK_2219_CURRENT.md).

## Reproduction boundaries

This preserves the real developer directory shape and source, not a newly
portable one-command test runner. Many scripts require the original licensed
game/build inputs, generated intermediate assets, external utilities, or local
runtime evidence. Those inputs are intentionally absent. Historical checkpoint
names and absolute paths in scripts/notes are provenance, not files that the
repository downloads or recreates automatically. Do not execute arbitrary
developer scripts as the player launch workflow.

For patching and playing, use `native-rom/README_PATCHING.txt`. For a source
rebuild, start with its source guide and supply the original required inputs.
Authored ASM templates in the development tree are generator inputs; the
canonical current linked ASM/diff snapshot is under `native-rom/source/`.

The port remains unfinished: Kano's earned boss clear/ending, final audiovisual
acceptance and final release review are open. A controller losing is not by
itself a game bug. Controllers/observers are test tools, never shipped gameplay
logic or a replacement for the ROM implementation.
