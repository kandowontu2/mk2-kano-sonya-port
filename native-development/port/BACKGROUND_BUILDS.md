# Background builds

Use `start_background_compile.ps1 -Target game` for the full native ROM build,
or `-Target finish` for the isolated finisher asset assembly check.

All eight port DOSBox configurations use `videodriver=dummy`, `autolock=false`
and `waitonerror=false`. The launcher also sets SDL's dummy video/audio drivers
before startup, requests no console window and below-normal process priority,
and checks that DOSBox does not create a window. A visible-window result or
timeout terminates only that launched process and fails the run; it never
falls back to a visible renderer. Game/finish build markers must be fresh.

The first headless finish build succeeded with no window observed across 13
process checks. The full game build then succeeded in 18.52 seconds with no
window observed across 167 process checks. The native assembler logs remain
in the normal build folder.
Stock-MAME automated tests use `-video none` and `CREATE_NO_WINDOW` on Windows.
Do not return to ordinary visible DOSBox launches for automated compilation.

`-Target sound` builds the isolated soundp candidate with original HENRY and
PLBUILD tools. It requires fresh SP_OK.TXT and no SPFAIL.TXT, with the same
hidden-window/priority/time bounds as the game build. `-Target sound-info` only
collects original-tool help and reference-decode diagnostics; exit0 is not a
claim of audio/gameplay acceptance. See NATIVE_DCS_AUDIO.md for exact scope.
# Isolated clean program check

`prepare_clean_sound_check.py` replays the own-WAV staging chain into that
same isolated root and refuses existing sound output. `sound-clean` invokes
the original compressor/linker through the hidden launcher. It imports no
candidate ROMs or precompressed own samples;439 original CMP inputs are
archive-verified and hard-linked. `qualify_clean_sound.py` verifies regenerated
PCM, original inputs and the four resulting sound ROMs against the current
candidate. Final audio mix and asset provenance are separate acceptance gates.

`prepare_clean_program_check.py` stages regenerated sources without objects
in `baseline/clean_program` and refuses to overwrite that directory. The
`clean` target of `start_background_compile.ps1` uses the same dummy SDL,
hidden-window checks, below-normal priority and180-second bound as other
builds, with success/failure markers in the isolated root. It imports no
existing program objects or linked outputs. `qualify_clean_program.py`
compares the four resulting ROM parts against the current native build.
This checks program-source reproduction only, not graphics or sound closure.

