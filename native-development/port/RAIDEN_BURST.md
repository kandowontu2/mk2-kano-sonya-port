# Raiden explosion: native late effects

MOVES rd_hp_open requires a384-field HP charge, release during Finish Him,
and close range052h. The physical controller holds HP throughout combat,
wins by pulsed HK instead, closes to68 and releases HP. No health/AI/state
forcing or native input-rule changes are used.

Runs279/280 select actual Kano17/Sonya18 as victims. Each reaches9000
fields, two natural KOs,166 fatality-state fields and native completion,
without missing/illegal recovery or Lua errors. The victim becomes invisible
and native chunks render. Read-only snapshots are scheduled60..400 fields
after activation, independently of mode/selection logging conditions.
Age240 captures were viewed and show the head during the win display;
age320 captures show the subsequent scene continuing. The existing own
main3d head roots are used, not another character's identity.

RAIDEN_BURST_QUALIFICATION.json pins current program/graphics, stock MAME,
controllers, traces and all delayed captures. Mirrored/original controls,
complete head trajectory and final visuals remain unqualified. No game
code or ROM changed in this diagnostic step.

Important evidence correction: a native completion flag does not end every
effect process or immediately leave the visible fight scene. A victim CSV
restricted to mode2/locked selection can stop before those effects finish.
The earlier Kitana first-link inference that missing post-flag pop rows
proved animation cutoff is therefore unproven. Recheck it using captures
scheduled beyond completion, then test whether the added own-only wait is
actually necessary for native-feeling behavior. Preserve the known facing,
palette and invalid-table fixes; do not use this timing review to discard
independently established defects. Subsequent tests281..284 confirmed full
rendering with the original delay, so the additional wait has been removed.
See NATIVE_KISS_TIMING.md for the superseding current evidence.

## Current-link mirrored head tracing

Runs285/286 added mirrored activation checks. The stronger287..290 runs
then repeat both own actors on both physical sides with read-only active
object-list tracing through the late win-display effects. All four reach
9000 fields, two natural KOs,166 fatality-state fields and completion,
without missing/illegal recovery or Lua error. One detached head object
retains true17/18 and cycles all seven corresponding ks_hd frames.
Age240 head captures for all four current runs were viewed.

The trace covers372/373 fields per head, starting after the completion
flag, from signedY=-72 above the screen to native ground_y-20=196.
Kano has four raw coordinate contacts with196; Sonya has three, consistently
on both sides. Native code calls head_grav four times, but changing single
image animation points can alter raw object-coordinate transitions.
This discrepancy needs original-head controls and animation-point analysis;
do not silently lower a four-bounce acceptance criterion or call it solved.

RAIDEN_BURST_QUALIFICATION.json now records own identity, seven-frame
coverage, observed contacts and both sides while explicitly retaining
completeHeadTrajectoryVerified:false. The game ROM is unchanged in these
diagnostics. Current lanes are those in NATIVE_KISS_TIMING.md; older279/280
are historical. No release promoted.

## Original controls resolve the contact-count concern

Runs291/292 select actual original Liu1 and Kitana4, using the linked
main3d script to identify their seven head images without a proxy or
hardcoded own-frame list. Both complete two natural KOs,166 fatality-state
fields and9000 fields. Liu has four raw floor contacts; Kitana has three,
matching Kano/Sonya respectively. All retain their real head object IDs
and seven native image frames, starting above screen and settling at196.

HEAD_CONTACT_COMPARISON.json pins all six current traces and ROM inputs.
It also compares native head_grav and MKDISP anig1 instruction blocks to
the original source ZIP. Both are unchanged. anig1 explicitly adjusts
oyval by the old-minus-new image animation offset; the changing head
origins make raw coordinate contacts an unsuitable universal measure of
head_grav invocation count. The four source-level head_grav calls were
not replaced or suppressed for Sonya. No physics patch is justified by
this count alone, and none was made.

This resolves the suspected port-only contact-count regression, not every
pixel of head trajectory or the whole original roster. Full visual
acceptance remains false. Current game ROM is unchanged.
