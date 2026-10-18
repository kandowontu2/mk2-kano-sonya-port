MKII KANO / SONYA - NATIVE ROM DEVELOPMENT CANDIDATE
NOT A FINISHED RELEASE. Do not confuse this with the withdrawn custom-driver build.

This contains classic per-chip IPS patches, hash checks, readable authored ASM,
native-source diffs and patching scripts. It contains NO complete ROM archive,
custom MAME executable, driver patch, host samples or proprietary compiler.

REQUIRES
  Your own MKII ROM archive and MK3 revision2.1 ROM archive matching the per-chip
  SHA256 hashes in PATCH_MANIFEST.json. ZIP container hashes/names need not match;
  chip bytes and internal filenames must. Python3.10+ (standard library only for
  patching). Unmodified stock MAME: tested with Windows x64 MAME0.289.

PATCH ON WINDOWS
  Extract this package to its own writable folder. Do not run inside the ZIP.
  From Command Prompt:
    PATCH.cmd "C:\path\mk2.zip" "C:\path\mk3.zip"
  Or on any OS:
    python patch_native_roms.py --mk2 /path/mk2.zip --mk3 /path/mk3.zip --output roms/mk3.zip
  All chips/patches/results are checked before output creation. Existing output
  is never overwritten. Original input archives are never modified.

PLAY
  PLAY.cmd "C:\path\to\stock\mame.exe"
  Or put your stock mame.exe beside PLAY.cmd, then double-click PLAY.cmd.
  Command on any platform:
    mame mk3 -rompath ./roms
  This native Wolf build uses MAME's existing mk3 hardware/socket definition.
  It is MKII game code, not MK3 gameplay. Run from this isolated folder so this
  candidate does not replace your normal MK3 ROM set or configuration.
  Stock MAME reports checksum warnings because patched ROM hashes differ from
  retail MK3. Those are expected; no emulator hash/driver spoofing is supplied.

WHAT THE PATCHER DOES
  Program: two compiled native TMS34010 lanes, assembled from proper ASM.
  Graphics: maps twelve original MKII chips to the Wolf sockets, then applies
  eight IPS patches for the added native graphics bank. No runtime DMA hacks.
  Sound: four IPS patches produce the current native Wolf DCS ROM images.
  Source program/sound/added-graphics bases come from your MK3 archive; unchanged
  original graphics come from your MKII archive. Never patch the ZIP file itself.
  Manual application: for each manifest operation=ips, extract its source chip,
  apply the named IPS, check targetSHA256 and rename to target. For operation=copy,
  copy the named chip without editing it. ZIP exactly those26 target entries.

SOURCE SNAPSHOT
  source/asm: current authored/generated own ASM modules actually linked.
  source/native_source.patch: byte-preserving8-bit diffs against the supplied
  mk2-rebuild source's src files (a/src/... -> b/src/...). Normalize CRLF line
  endings to LF without character-set conversion before applying with git apply.
  No complete proprietary source tree is included.
  source/PBUILD.BAT and source/MK2NEWW.CMD document the current native build route.
  The proprietary rebuild input, TI tools and original ROMs are not included.
  Independent program, sound and added-graphics rebuilds match the tested ROM
  bytes. This snapshot alone is not a standalone rebuild kit: it still requires
  the original proprietary inputs/tools, which are not redistributed here.

MOVELIST
  MOVELIST_NATIVE.txt includes Kano/Sonya specials, fatalities, stage finishers,
  Friendships, Babalities and the two added Shang Tsung morph commands.

KNOWN OPEN GATES
  This2219 candidate fixes detached-leg grounding in native MKDEATH ASM at four
  consumers, applying only to true IDs17/18. Twelve current Cage/Scorpion/Sub-Zero
  victim cases and an independent130-object byte-identical clean rebuild pass.
  No shared artwork, normal-body pivot, driver or game-balance change is used.
  Current2219 finite checks cover all eight specials, four lethal finishers,
  Friendship/Babality eligibility, stage finishers and transformed specials/
  lethal finishers on both player sides, including tested fresh-match recovery.
  Earned lethal victim coverage now passes112 cases: all four added fatalities,
  all14 selectable victims, both player sides, including same-character matches.
  Independent exact-coverage/hash audits verify native completion and600 fresh
  combat fields with hardware palette restoration for every case. This does
  not certify every interruption, edge, CPU behaviour or audio overlap.
  Normal/proximity contact checks cover136 finite cases:17 actual actions,
  both added characters/player sides, hit and appropriate block, native damage
  and recovery. These do not certify arbitrary ranges, victims or every frame.
  Own ingestion, arm-rip, inflation/burst, split and Raiden-head reactions have
  current runtime checks and separately documented sampled visual reviews.
  Representative original Liu/Kitana controls pass; remaining original-roster/
  Goro/edge coverage is not inferred. Older broad6AE0 evidence remains historical
  unless a current2219 check is explicitly identified here.
  All six native ladder maps now include Kano and Sonya as real opponents,
  without replacing an original fighter. Linked roster/geometry/secret/boss
  tables and the initial portrait pan are checked. One earned Sonya route
  reaches and defeats both added opponents; all six maps are not runtime-tested.
  Current2219 native/control cue checks,41 independent isolated chicken-tail
  windows and a three-track native mix comparison pass. These are finite sound
  checks, not exact full-scene audio-sync/every-overlap acceptance. Nonlethal
  lifecycle and fresh-match recovery checks also pass on the current build.
  Kano/Sonya have source-linked two-page own-photo endings and a native cast
  pair. An earned current2219 Sonya route displays her two pages, the added cast pair,
  sampled native credits and attract return. Named pixel checks support
  observed page stability, not every-field or full audiovisual acceptance.
  Kano's earned ending remains unverified.
  Finite stock-MAME checks cover all eight specials and four lethal finishers
  while Shang is morphed into Kano/Sonya, on both player sides. This does not
  certify every victim, interruption, edge or audio path. Native punch-history
  restrictions still apply to transformed nonlethals; see the movelist.
  Native own-ID CPU reaction and boss projectile classification fixes are
  included. On current2219 Sonya naturally clears both bosses and her ending.
  Kano has earned matches against all14 human opponents across paid continues,
  but his boss match clear/earned ending remain unverified. This is not full-port
  completion. No test controller edits AI, difficulty, health, damage or results.
  Remaining campaign and broad opponent/edge/interruption/AI verification;
  remaining native audio and final visual acceptance; final release validation.
  Existing finite tests are not a claim that all gameplay is complete.
  This package is for development/testing only, not the final GitHub release.
