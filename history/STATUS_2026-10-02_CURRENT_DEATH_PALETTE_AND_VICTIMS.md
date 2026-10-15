# Native death-palette lookup and Reptile victims; art still unfinished

Current experimental build is diagnostic_v873_native_headless_palettes.
EXE SHA256 CFF2453AA529CB3B06744CFED5F4E52F235A20A4E0C2EFA1C89F60D3445D0F23.
Graphics payload remains 7896C93822473376AD724BB5E747EDE88C198203786F3F9B928CD1D860BAE019.
Production, all existing launchers and release ZIP remain unchanged.

## Exact current native repair

FF90C800's native ID-indexed palette lookup previously ran beyond its short
FF90C900 table for true Kano17/Sonya18, reading color data as pointer words.
The v873 repair copies every original 17-row byte to an independent 19-row
table at FFFD4800, adds both owned normal/alternate costume palettes, and
redirects the original FF90C840 operand. The original dispatcher, flag-6
alternate selection, palette data and art are unchanged. Relative to the
preceding Reptile-overrun repair, exactly 119 guest-program bytes change.

audit_v882_native_death_palette_checked verifies the full guest delta,
unchanged input hashes, paired native halfword fetches and actual A0 pointer,
true physical actor/Main binding, original health writers and no cache
overrun/reset. The Sonya boot600 campaign and boot630 scout exercise five
physical normal-palette selections. All three 1,800-second campaigns exit0
at field98473, including Kano P2 reaching Kintaro. They do not clear a tower;
Kano's long campaign does not happen to exercise this palette hub. The first
13,189 input/state records in the boot600 Sonya replay match the preceding
build exactly before its first repaired palette-table use at field27622.
audit_v884_native_death_palette_units passes 14 corruption methods.

## Direct stock Reptile sequence in all four true victim cases

The new standalone physical-input test earns two genuine Reptile round wins
against an idle second human, then inputs Back, Back, Down, LP. No guest
writes, actor IDs, HP, positions, RNG, difficulty or finisher entry are forced.
The read-only observers retain their handles for the entire capture.

audit_v887_sonya_p2_stock_reptile_victim and the three audit_v888 cases cover
Kano P1/P2 and Sonya P1. Each actual case has 322 collision damage over ten
native hits and two KOs, both native round wins, distinct physical owners,
the original Reptile action at field3135, all four correct true-ID victim-row
reads at age97, native head creation and the owned normal palette at age129,
and original completion at age187 (90 fields after the row read). The
physical body, not just an effect actor, receives its own valid palette.
All four runs exit0 at field5198 and retain 31 real 400x254 finisher snapshots
each. These are actual game executions, not a simulated command or builder
report. audit_v890_current_reptile_victims_checked independently passes;
audit_v891_current_reptile_victim_units passes 16 corruption methods.

These observations prove the current native victim-row and normal-palette
paths for both added IDs and physical slots. They do not prove alternate
palette runtime, every stock fatality, full rendered-pixel correctness,
complete towers, or whole-port acceptance.

## Actual remaining death-art defects

All four real native head creations still read Liu Kang descriptor FFB4A4B0
from the owned main61 streams FF00B910 / FF02B910. Age140 screenshots also
show the ordinary headed Kano/Sonya body beside the detached wrong head.
Kano P1 and both Sonya-slot age140 images were inspected directly. Correct
palette lookup does not fix the wrong anatomy/identity. Main60 headless-body
and main61 detached-head assets must be replaced with proper owned art while
preserving the original native animation tokens, timings and cleanup.

The earlier AI-generated art_native_death_drafts_v875 atlases are not
installed or accepted. Their saved prompt/review manifest records overlapping
bodies, incorrect rolling-head orientations and remaining costume/palette
review. Original MK3 pose references/scans are preserved. No generated draft
has changed the payload or the current executable.

## Diagnostic failures preserved

audit_v874's first palette observer recursively read its own tapped table;
that confirmed diagnostic recursion was canceled, not called a native game
failure. v876 fixes the recursion and completes normally.

The v879/v880/v881 test starts did not join a second human correctly. v883
joined but used an incorrect combat-mode assumption. v885 used the wrong
field for the finish prompt. v886 corrected the prompt but did not retain
all Lua memory-tap handles; its game sequence ran but its observers ceased
recording. The final v887 retains all nine observers and distinguishes the
game mode from the native winner/finish field. None of those incomplete
captures is accepted as native finisher proof.

The first v889 checker incorrectly treated a duplicated FIRST_LIVE `victim`
body field as the log's fighter-name header. Its failed gate is retained;
v890 explicitly parses the header separately. No gameplay requirement or
runtime failure was waived to obtain acceptance.

## Remaining full goal

Install and verify correct owned death/headless art; cover other stock
finisher victim paths, required cinematic/art/audio and arena/state variants;
demonstrate both genuine full towers through bosses, continues and endings;
rerun the final integrated gameplay/UI/shadow/move regressions; then update
the actual play CMD, matching release ZIP and clean obsolete build data.
Earlier v786 proofs remain evidence for their exact build, not blanket v873
whole-port acceptance. The goal remains active and the port is not complete.
