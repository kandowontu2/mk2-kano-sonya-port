# Building the custom emulator

## Exact upstream and source

Upstream: `https://github.com/Zoltan45/mame-mkp`

Pinned commit: `914d2c29749a0ca612d92b1fc69cd62d94e1468d`.

Use a fresh checkout, not a working tree containing changes you need to keep:

```sh
git clone https://github.com/Zoltan45/mame-mkp.git mame-mkp
git -C mame-mkp checkout --detach 914d2c29749a0ca612d92b1fc69cd62d94e1468d
```

Copy the contents of `mame-overlay/` into that checkout, preserving relative
paths. The overlay includes the new `mk2ks_native_picture.h` header; applying
only the tracked-file patch would miss it. Do not copy the rest of this
repository over MAME. Verify the overlay files against `SOURCE_MANIFEST.json`.

Install the compiler/dependencies required by that upstream MAME revision.
The development build used a 64-bit MinGW GCC toolchain and Python. Its native
driver target command, with paths adapted to your installation, was:

```sh
gmake SUBTARGET=mkport SOURCES=src/mame/midway/midtunit.cpp NOWERROR=1 REGENIE=1 PYTHON_EXECUTABLE=/path/to/python MINGW64=/path/to/mingw64 PTR64=1 -j4
```

`make` may be named `gmake` on Windows. Compiler/platform differences can change
the executable hash; matching source does not promise a byte-identical binary.
No new full compiler build was performed just to publish this snapshot. The
15 overlay files were checked against the inputs recorded for the current
compiled release.

## Game data is separate

Building MAME does not build or supply the game ROMs. The `mk2ks` ROM definition
in `midtunit.cpp` describes the exact required files. This integration needs
MKII data, donor MK3 data, and derived character/UI/audio payloads, none of which
are included in the public repository.

Retained code such as `tools/build_mk2ks_mk3.py`,
`tools/build_native_shang_morphs.py`, the native art/sample builders and later
payload revisions explains extraction, native animation translation, source
rebasing, descriptor changes and packing. Those scripts require separately
provided inputs. They do not grant redistribution rights to the resulting
assets.

## Reproducibility limit of this publication

The current emulator source overlay is pinned and complete. The retained
development tooling is published for inspection, **not represented as a clean,
one-command end-to-end payload rebuild**. Many historical scripts reference
private workspace checkpoints and JSON receipts or generated payloads that
are intentionally absent. Running the initial prototype builder alone will
not recreate the final payload.

The manifest records the final payload SHA-256 so that a separately rebuilt
payload can be compared honestly. Do not substitute an older prototype and
claim it is the final release. A portable asset pipeline still requires
consolidating that historical chain around user-supplied original data.
