# Sonya launch-audio candidate; current playable remains v1411

Run PLAY_CURRENT_V1411_TEST_BUILD.cmd for the current checked playtest. It has
not been changed or promoted during this turn. The new development candidate is
diagnostic_v1473_sonya_launch_audio, EXE SHA256
42151DB8134D8D68A2DD68DB5E1B81EA5B3CB0298DCDB5DAA8748421C6CA0209.
Its payload remains 5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D.

## Completed progress

- Extracted actual original Sonya square-wave launch, bicycle startup grunt,
  and bicycle cry. All five original hardware channel variants per cue are
  PCM-identical. Original delivery latency and complete tails are retained;
  gain changes compensate only the existing 0.70 sample route.
- Added native startup requests with independent physical-player channels.
  Audio ownership/health observation is read-only: no fighter ID, health,
  position, RNG, stage or scheduler writes. Normal recovery retains natural
  finite tails; damage, ownership change, noncombat and reset stop owned voices.
- audit_v1489_sonya_launch_audio_checked passes ten real-input human cases:
  square, bicycle, leg and choke in both slots, plus both square airborne-target
  cases. All 30 prior full screens and every original native human event match.
  Entire actual guest ROMs independently reconstruct from v1411 plus only the
  declared two startup insertions and internal branch relocation. Driver and
  header changes are confined to audio assets/channels/ownership lifecycle.
- Actual normal mixed launch PCM matches the original cue prefixes at the
  real markers, approximately 0.699 route gain and correlation above 0.99999.
  Native DCS contact/landing sounds vary between recordings, so full-tail mixed
  subtraction is not claimed. Four independent read-only channel captures
  show complete finite source playback, correct own physical channels, no
  opponent channel activity and eventual audio-owner cleanup.
- audit_v1493_launch_interruption_checked passes one genuine incoming-hit case:
  P1 Sonya square wave takes the original 40-damage uppercut, sample playback
  stops mid-cue and ownership clears by the next callback, then normal native
  recovery, walking, jumping and high punch respond. Seven in-memory corrupted
  copies are rejected; actual evidence was not altered.
- Three other uppercut attempts did not damage Sonya. They are explicitly NOT
  interruption acceptance. Both-slot/bicycle interruption coverage remains open.
- Restored historical canonical machine/driver/header sources and installed EXE.

## Cleanup

Deleted only the obsolete mame_mkprobe and mame_mkwport compiler-library folders
under mame-mkp/build/mingw-gcc/bin/x64/Release: eight .a files, 22,678,330 logical
bytes. They regenerate from retained source. Installed and frozen executable
hashes, current CMD, source and test logs remain intact.

audit_v1496_old_compiler_cache_cleanup_checked independently confirms deletion
and preservation. The initial cleanup report's dictionary summation returned
null; v1496 sums the actual captured file lengths. Logs were already NTFS
compressed and the compaction command skipped them: zero additional allocated
bytes were reclaimed. This is partial cleanup, not all obsolete build removal.

## Full goal remains open

Current playable v1411 retains the previous selection, immediate teardown,
native ladder/identity/lifebar-shadow, bounded Dead Pool grounding/shadow and
both-slot genuine Sonya CPU leg evidence from checkpoint v1467.

Before promoting v1473, extend defensive/UI/floor/CPU regressions and the missing
interruption/repeated/simultaneous/KO cases. Remaining move choreography/audio,
full CPU repertoire/opponents, finisher consumers, other arenas/shadow phases,
genuine towers/bosses/continues/endings/secrets/cinematics, release ZIP and
larger obsolete-build cleanup still require work. This is not full release
acceptance. The objective remains natural integration in all aspects.

## Preserved diagnostic limitations

Channel observer attempts v1480-v1482 preserve malformed runner/script and
hexadecimal item-name errors; v1483 uses the actual A/B/C/D channel names and
reads item data only. The original guest reconstruction helper omitted the
bicycle ceiling JAHI opcode and trimmed the square routine's final FFFF operand
as padding. Successors retain the source/disassembly-backed instruction and
the complete 0x11c-byte original square routine. No game code or captured
evidence changed to resolve those verifier errors. v1488's full mixed-waveform
check is preserved; v1489 uses uncontaminated launch PCM and actual live source
positions to distinguish original cue playback from variable native contacts.
