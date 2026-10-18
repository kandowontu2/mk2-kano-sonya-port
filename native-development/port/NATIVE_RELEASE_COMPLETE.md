# Native release completion record

Published native-v1.0.0:
https://github.com/kandowontu2/mk2-kano-sonya-port/releases/tag/native-v1.0.0

Release source target:9d0f68de49c3be5768fc71a765a160650b6440f8.
All eight GitHub assets were checked for uploaded state, exact size and SHA256
against the local qualified files before publication; the public non-draft
state was then read back successfully.

- Player ZIP:98,331,772 bytes,34 members,
  SHA2563611CB268EC6950ED07DD41368D6A4243A6F2805E52293F1D6D93575EBAC4C62.
- Source/IPS ZIP:5,645,778 bytes,122 members,
  SHA2561ED9E077250570ABCF31085310C1A4E709E2D62F46E5F435598C975BC7EC069B.
- Both distributed ZIPs independently patch original user inputs into the exact
  tested26-chip archive, SHA256
  454772BC6831B6B2F672E59F23FC5456ADCEB886CBC98FE1D8DEC4559EFD0C38.
- Stock MAME0.289 binary, legal notices and corresponding official source are
  supplied; no custom driver or complete game ROM is distributed.
- Compiled native sources comprise59 authored ASM modules plus40 original-file
  diffs. The14 IPS patches cover the changed program/sound/graphics sockets.
- Both true identities have dedicated portraits, native selection cursors and
  previews, ladder art, names/shadows, normals, specials, finishers and morphs.
  Completion evidence includes136 contact cells,16 special/side cases,
  112 lethal victim/side cases with fresh-match recovery, stage/nonlethal and
  transformed-move checks, selection P1/P2, floor shadow/grounding checks and
  independent clean rebuild equivalence. See RELEASE_EVIDENCE.json inside
  each ZIP for the actual scoped reports; narrow checks are not exhaustive.
- Both characters have continuous physical-input full-game clears without
  loaded states or guest-memory edits; their complete videos, own ending/cast/
  credits samples and move/finisher/morph demonstrations are published.
- Source/test/build tools are public in the native-development snapshot.
- All482 local unit cases pass. This is a count of cases, not builds/suites.
- The superseded98,257,403-byte V3 player ZIP was hash-checked and deleted after
  replacement verification. Final ZIPs and rebuild inputs are retained.
- All release work remained background/hidden; no interactive renderer window
  was opened. The port targets stock mk3 Wolf hardware, not a T-unit PCB.

The publication receipt is separate from RELEASE_QUALIFICATION.json, whose
publicationVerified:false correctly describes its earlier pre-upload scope.
Neither record claims exhaustive every-input/arena/interruption coverage or
subjective every-frame A/V perfection. No known functional release blocker
remained in this completion audit.
