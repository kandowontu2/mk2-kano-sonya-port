# Native detached-leg grounding fix

Program SHA256:
221919459A4129FFDB37C8A3E9EC7F9AA6210D99AED00A35BC3256842C5E1F5A

The prior6AE0 Cage torso-rip object placed own opaque feet five world pixels
below ground. The shared phase6 artwork has opaque extent141 (last row93 +1
minus signed yOffset-47). It is unchanged. Native MKDEATH now calls
ks_ground_own_legs at three lower-leg object insertions (Goro-family, Scorpion,
Cage) and in the own Sub-Zero shatter branch. The helper preserves A0, applies
only to actual character17/18, and sets the leg object's Y to ground_y-141.
Original IDs take the unchanged-position return path. Upper-body pivots, normal
fighter grounding, move rules, AI, damage and emulator code are not changed.

leg_ground_source.py reproduces these explicit ASM hooks from original source;
prepare_game_candidate.py invokes it after the existing victim integrations.
The actual compiled file is baseline/mk2-rebuild-main/srcp/MKDEATH.ASM. Linked
helper address isFF8AA530. All146 own dispatch cells still match their ASM roots.

## Fresh runtime evidence

- stock_wolf_2219_torso_{17,18}_p{1,2}: all four earned Cage torso rips pass,
  including opaque lower boundary exactly on ground, separate upper/legs,
  native completion,600 fresh-combat fields and77400 hardware-palette
  comparisons per case. One corrected Sonya frame was individually inspected.
- stock_wolf_2219_swipe2_{17,18}_p{1,2}: all four earned Scorpion swipes pass
  the same lower-edge, completion, fresh-combat and palette gates.
- stock_wolf_2219_shatter_{17,18}_p{1,2}: all four deep-freeze/shatter cases
  pass with matching same-field main/victim shapes and the actual opaque
  leg boundary on ground through native completion.

The first swipe run completed its fatality/grounding but did not satisfy the
fresh-combat damage gate. Its controller pressed Down+HP together too briefly
for Scorpion's duck entry. That failed whole-case evidence is retained. The
swipe-only fresh controller now prepares Down12 fields before its HP pulse;
swipe2 succeeds without weakening the actual-damage requirement or changing
native game rules. Other fresh-match profiles are unchanged.

Goro-family runtime and explicit original-roster leg controls are not yet
qualified by these12 cases. Original behavior is source-gated, not universally
runtime-certified. Broader specials/ending/audio results from6AE0 are historical
until refreshed or appropriately reviewed against this new linked program.

## Build/reproduction

Hidden BelowNormal normal build completes31.15 seconds with no window. An
independent130-object clean assembly/link/split completes87.19 seconds,793
window checks, no window. All four program parts are byte-identical to the
tested build; all26 rebuilt/copied chips match a fresh runtime archive.
Only MKDEATH changed in the regenerated clean source set. The inspected
MKSOUND text difference is leading-zero hex formatting, not changed values.
The existing linker GROUP alignment warning remains; assembler logs report
no errors/warnings. No driver hacks or injected emulator callbacks are used.

The existing clean folder was reused:135 hash-verified generated compiler
outputs were removed and rebuilt; all source inputs were preserved, with no
extra archive tree. All300 local tests now pass after the independent runtime
reference was refreshed. Corruption tests additionally validate the untouched
archive outside assertRaises, so stale baseline failures cannot fake mutation
rejection. No emulator/compiler remains running.

The local development IPS ZIP and checked launcher archive are now refreshed
to2219. Both independent IPS decoders and the complete26-chip roundtrip pass;
the source diff applies back to original source and matches the compiled ASM.
PACKAGE_QUALIFICATION.json records matching current runtime evidence, including
the exact patcher-produced archive smoke check. Broader acceptance remains
open. Do not call the new port/release complete from this focused fix.
