# Native snapshot validation

This describes `native-rom/`, not the withdrawn MAME overlay. It is not a
finished-game certificate or a claim that all local developer tests are bundled.

## Reproduce the bundled IPS tests

From the repository root, with Python 3.10 or later:

```text
python -m unittest discover -s native-rom -p test_ips_codec.py -v
```

These five synthetic tests check the IPS codec without requiring game ROMs.
They do not test gameplay. No third-party Python packages are needed.

## Patch your matching inputs

```text
python native-rom/patch_native_roms.py --mk2 PATH_TO_MK2.zip --mk3 PATH_TO_MK3.zip --output isolated/roms/mk3.zip
```

Use your own hash-matched inputs from `PATCH_MANIFEST.json`; do not patch ZIP
container bytes. The patcher verifies source, patch and resulting chip hashes,
refuses an existing output, and never modifies your input archives.

The published checkout was exercised from an isolated temporary working
directory, without the original developer tools on Python's import path. All
121 snapshot files matched their file-hash manifest. Its patcher reproduced
all 26 chip bytes of the stock-MAME-tested candidate. The local deterministic
ZIP output had SHA256:

```text
454772BC6831B6B2F672E59F23FC5456ADCEB886CBC98FE1D8DEC4559EFD0C38
```

Per-chip manifest hashes, not ZIP compression metadata, are the portable
correctness criterion. The temporary verification ROM was removed afterward.

## Build and runtime boundaries

The source snapshot contains 59 added ASM modules and the diff to 40 original
engine files. The patches cover two native program lanes, eight added graphics
sockets and four sound sockets; twelve original MKII graphics sockets are
copied unchanged. The program runs on the emulated TMS34010. Stock MAME 0.289
supplies the existing Wolf-unit hardware, not the added gameplay.

Independent local program, sound and added-graphics builds match the tested
chip bytes. This does not make the snapshot a standalone replacement for the
original source/data or proprietary build tools. See the source guide.

Local finite runtime checks cover both added identities, selection cleanup,
normal/special moves, finishers, morphs and fresh-match recovery. Sonya has an
earned current-ROM campaign clear. Kano's earned boss clear/ending and final
audiovisual/release acceptance remain open. Source hashes, patcher tests,
successful move requests or low remaining boss health do not prove completion.
