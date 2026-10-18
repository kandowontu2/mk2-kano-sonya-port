# Collapsed-pose shoulder gush anchors

The early arm drip runs during the standing armless pose. The later three
pairs of gushes run after the five-pose reaction reaches its kneeling pose.
Reusing the standing y24 offset there put their origin above the collapsed
body. Only the own-ID late-gush path was changed; early drip and all
original-character paths remain unchanged.

Authored collapsed-image anchor pixels (left/right script roles) are Kano
(36,10)/(4,20), Sonya(38,20)/(12,25). Relative to each actual frame origin
these are Kano(0,81)/(-32,91), Sonya(-2,82)/(-28,87). Each lies in the
shoulder-cap neighborhood, with nearby dark-red pixels. The right effect's
native flip_single adds a seven-pixel shift, so its encoded x values
compensate for that. Initial measurement runs231/232 exposed the shift;
the final constants are verified on both sides rather than assumed from
unflipped object coordinates.

Final hidden compile passed22.66 seconds with no window. Stock MAME runs
233–236 each completed9,000 fields after two natural Jax round wins. Both
own fighters on both physical sides retain all five body/arm phases and
147-field native fatality activation followed byffff completion. No guest
writes, custom driver, missing-art, illegal recovery, Lua error or timeout.

Read-only object logging now includes flags and the exported original
GUSHER1 image marker. `qualify_arm_blood_positions.py` reads its compiled
17x22 image header and(1,20) animation point, restores each single-part
object's actual anchor, normalizes the victim's horizontal flip, and
compares against the collapsed own body in the SAME frame. Each case has
24 matched object rows: two shoulder anchors, four fields per effect,
three distinct waves. All96 rows across both sides match exactly.
ARM_BLOOD_QUALIFICATION.json records that narrow proof and screenshot hashes.
Viewed final captures233/236 place the gushes at the collapsed wounds.

This does not qualify early drip placement, every animation pixel, stage
edges, original-roster controls or a clean rebuild of the current link.
Those gates stay open; source preparation's zero structural differences
are not fresh compiler-reproduction evidence. No release was promoted.
