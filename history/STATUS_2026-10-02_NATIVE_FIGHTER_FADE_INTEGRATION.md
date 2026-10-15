# Native fighter fade integration — experimental, not release acceptance

Candidate: diagnostic_v786_native_fighter_fade_exclusions.
EXE SHA256: 8DD83D7300BBC3872B1F829EA2A557CA968F5148464C3518AAB16B8559A76B55.
Payload SHA256: 7896C93822473376AD724BB5E747EDE88C198203786F3F9B928CD1D860BAE019.
Driver SHA256: 86841B405FC36B56965B9D30EDBE3CD17EC5B0179D245991F6AD71EA4A69B5A0.

PLAY_LATEST_TEST_BUILD.cmd remains v737. Production CMD and release ZIP are
unchanged. Installed EXE was restored to its pre-build hash:
413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891.
No files were deleted during this work.

## Corrected integration defect

The earlier statement that imported Friendship bodies should be dimmed with
the background was incorrect. Genuine stock ID2 Cage and ID1 Liu Kang control
runs prove that native playable fighters stay bright while the scenery dims.
Kano and Sonya's new palette records were missing from MKII's fade exclusions,
so the native colour converter reduced their RGB555 channels to 48/128.

The driver now copies all 46 original FF908120 exclusion entries unchanged,
appends the six actual normal/alternate/frozen Kano/Sonya palette pointers,
and adds the native zero terminator. The three original consumers are rebound
to this extended list. The original native fader and channel converter remain
byte-identical; this does not disable background fading or repaint actors.
All six palette records, the original list, commands, art, scene choreography,
audio code and unrelated gameplay bytes are untouched.

Actual guest delta against v777: exactly 169 differing bytes, confined to the
reserved fa700..fa800 list storage and three pointer operands FF80F760,
FF80F7F0 and FF8CDF10. The list includes both palettes for each character and
both frozen records; actual alternate/frozen runtime remains a separate gate.

## Current evidence

- Eight cold v786 runs: Kano, Sonya, Cage and Liu Kang, each in both human
  player slots. Native selection produces the actual IDs; each winner earns
  two original-combat KOs / 322 damage and enters the native Friendship using
  physical controls. No guest RAM writes, identity substitution or cheats.
- audit_v787_native_fade_exclusions_checked: 2,312 checked inputs. Both
  fighter palettes remain exactly their native source colours for every
  action field 0..240 in all eight cases: 3,856 fighter-field observations.
  Scenery fades retain the ten original 120..48 factors. Neither fighter
  palette bank is passed to the colour-scaling routine.
- Stock controls: all traces unchanged relative to v784 and all 241 captured
  Friendship frames per slot are byte-identical: 964 stock frame comparisons.
  Kano/Sonya's non-palette gameplay/choreography traces are unchanged.
- audit_v787_native_fade_units: 18 baseline/corruption test methods pass,
  including every list binding and all six records, original list order,
  terminator, reserved padding, fader/converter/source edits, missing/duplicated
  field captures, wrong IDs, dimming and incorrectly disabled scenery fades.
- Original body render checks: all 18 Kano and 11 Sonya body groups match
  every nontransparent original-art pixel, with full native brightness,
  for both player slots. No percentage tolerance or arbitrary occlusion mask.
- The first Sonya P2 capture has two hands partially covered by a native arena
  chain. Its exact-pixel gate correctly remains false for those two groups.
  A new genuine-control run at physical command gap 140, rather than 160,
  captures all 11 Sonya groups unobscured without changing code/art/positions
  through guest writes. The native ground anchor and choreography still pass.
- Four stock controls observed for 1,600 fields after the finish window all
  retire and reach mode 3 with both old actor pointers invalid and a changed
  next-screen render. Their initial 720-field traces still match the original
  bounded controls; the old short stock observation was not a softlock.
- audit_v789_friendship_visual_supplement_checked combines the immutable v787
  proof with the unobscured Sonya P2 and extended stock runs. All 58 unique
  character/slot body-group combinations and stock next-screen transitions
  pass. Full finisher acceptance and full port acceptance remain false.

Pre-edit source preservation: audit_v785_pre_fade_exclusion_fix contains the
v777 inputs, samples, payload, build-info and latest CMD, with snapshot hashes.
Historical input checks resolve the changed driver through that snapshot.
Executed Lua harnesses, runners and prior proofs were cloned/versioned rather
than edited in place.

## Still required

Current-candidate audio acceptance is not inferred from the v777 audio proof:
skipping fighter palette work changes sub-field CPU timing, and the new mix
captures are not byte-identical to their pre-fix captures. Exact native cue/
waveform/overlap checks need rerunning against this candidate.

Broader Friendship command rejection/distance/arena/CPU checks, alternate and
frozen palette runtime, current-candidate Babality/fatality/stage-finisher
regression, selection/ladder cleanup/names/floor shadows/combat/endings,
unassisted towers through both bosses, interruptions/secret stages, and final
production launcher/release ZIP remain. These targeted positive Friendship
cases do not recertify the entire port or authorize release promotion.
