# Next integration work (full goal unchanged)

The baseline, stance and 51-script initial-phase diagnostics are established.
Do not spend the next pass merely reproducing those checks. Move to an isolated
real roster/game build; do not alter the accepted srcw baseline or its receipts.

## First native roster/game candidate

- Build a separate DOS-8.3 source directory, e.g. srcp, under the same mounted
  baseline root so its ../data paths and native TI tools remain usable.
- Add independent 66-entry main and 7-entry special animation roots. 51 main
  entries exist. Main 30 is the ordinary flip kick, NOT an excuse to hijack it
  for a signature move; translate its native template using own jump-kick art.
  Other missing entries are 38/39 and 54..65. Track missing work explicitly;
  no silent Liu/stance fallback and no claim of full playability while incomplete.
- Extend MKGUYS's existing 17-row animation/palette roots, stance rates, shadow,
  forward/back walk info and ochar_ground_offsets with deliberate typed rows.
  Own imported palettes are exported by KANOART/SONYAART. First opaque stance
  measurements are in GROUNDING_MEASUREMENTS.json. Existing fighters' soles
  sit 5..11 pixels relative to ground_y (median 8), not universally zero; use
  actual source/runtime comparisons rather than descriptor heights alone.
- Give the new IDs their own strike descriptor blocks and reaction vectors
  using the native common reaction engine; sharing common routines is not
  substituting the actor's ID. Inspect MKSTK strike_tables and MKREACT
  reaction_tables explicitly: the first source-call inventory is not exhaustive.
- MOVES char_* switch tables have 12 entries in places. Extend deliberately
  through IDs 17/18; do not let an added actor read the next table as code.
  Route char_lok_open to the Kano held-LK gate and char_hi_punch to Sonya's gate.
  Others need their actual new moves, not an existing fighter's special set.
- MKSEL: add own mug_shot_table entries at (23,24)/(323,24), own picked palettes,
  and source references to KSUI. Retain original cursor segment/number/blink code.
  Use KSNAV menu IDs/inverse IDs, 19-row maps and counted sans tables. Both
  new_cursor_position and new_auto_position must use the absolute-coordinate
  delta helper; default auto-select count also changes from 12 to 14.
- Do not leave short eligibility/name/announcement/ladder/winner tables indexing
  past their ends. MKDISP powerbar names are TWO DWORDS per character. Proper
  native name images and matching shadows now have four-entry/two-sided pixel
  checks (`qualify_hud_names.py`); retain those in future builds. Do not label a new actor
  Liu, use a proxy slot, or mistake a temporary missing UI item for acceptance.

## Signature moves and remaining acceptance

KANOMOV/SONYAMOV now use dedicated own-pose cannonball and Square Wave scripts.
Their physical command activation, an invalid-command case, first hit and
return-to-stance have bounded stock-MAME evidence (see STATUS and qualification
receipts). They still need block/whiff, timing/hitbox/balance, mirrored-side and
native launch-audio acceptance. All four specials per character remain required;
Knife and Ring now also have native ASM actions and two-sided command, hit/block,
art/identity and cleanup smoke tests (`qualify_projectiles.py`). They retain gaps
in launch audio, interrupted/alternate palette cases, spacing/whiff and broader
victim coverage. Blade Swipe now has native source and two-sided whiff/hit/block/
interruption checks (`qualify_blade.py`), with broader victim, spacing and audio
acceptance outstanding. Bicycle Kick now has native source and two-sided command,
paired motion, block, duck/far miss and release/get-up checks (`qualify_bike.py`),
with broader victims/bosses, stages, AI and audio acceptance outstanding. Choke
now has native source and two-sided Sonya-victim plus original Liu-victim
trajectory/pulse/release checks (`qualify_choke.py`), with broader victims, edges,
AI and audio acceptance outstanding. Leg Grab now has native source and
two-sided Kano-victim plus original Liu-victim command/46-field hold/35-damage
release checks (`qualify_leg.py`). Wolf live-button masking is corrected in ASM;
Block-first/simultaneous chords work, but LP four fields early starts a normal
punch. Broader victims, stage edges, AI, audio and timing acceptance remain.
Choke's shared paired-helper regression passes on the same binary; rerun the
other older special suites after the input correction. All individual fatalities, friendship/babality,
three stage finishers, Shang morphs, own victims/reactions, native DCS audio,
AI, grounding/shadows, clean selection-to-ladder transition, native UI and
complete playability still require implementation and runtime verification.

Sonya Death Orb is now a distinct native ASM action with two-sided Kano-victim,
Liu-victim and broken-continuous-Block-hold cases (`qualify_bubble.py`). Bounded
runtime proof includes effect poses, native victim stumble, completion and
active-list retirement of both its own object and dummy process. Native helper
`kmo_proc` is corrected for never-woken dummies. Broad cleanup/audio/AI/victim
coverage remains; these checks do not complete the port.

Sonya flame kiss is now a native ASM action with two-sided Kano-victim and
original Liu-victim physical round-win/motion/burn/completion checks
(`qualify_kiss.py`). Its headless compile, native orb deletion and stage-relative
motion are verified in finite cases. Exact new DCS cues, all victims/edges/AI
and fresh-match cleanup are not accepted yet.

Kano extraction is now an actual native ASM action with two-sided Sonya-victim
and original Liu-victim physical round-win/activation/completion checks
(`qualify_extract.py`). Kano Eye Laser now has a distinct native action and
finite two-sided Sonya/Liu-victim checks plus held-Block rejection
(`qualify_laser.py`); broader acceptance remains outstanding. Complete native
audio, all victims/edges/AI and retained skeleton teardown into a fresh match
remain acceptance gaps. All older special receipts require a current-binary
regression after this new full-game source link.

Keep stock MAME unchanged, including CPU, video, sound and memory-map support.
Final ROM patches must reproduce the accepted chips from documented original
inputs. Initial-phase graphics playback does not certify any complete move,
paired throw, campaign, or final release. The GitHub release remains withdrawn.
