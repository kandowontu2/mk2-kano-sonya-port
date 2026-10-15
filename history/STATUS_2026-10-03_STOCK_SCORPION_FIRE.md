# Stock Scorpion fire verified against real Kano/Sonya; full port incomplete

Current candidate remains diagnostic_v1130_owned_split_invariant_blood. No
game code, executable, payload, installed emulator, play CMD or release ZIP
changed in this pass. Prior v1182 checkpoint was fully revalidated:43,792 pins,
zero mismatches. The status-only preceding goal turn made no new progress;
this pass took the next safe gate and gathered new current runtime evidence.

Original ROM inspection and real stock controls resolve Scorpion as ID10 and
fire as primary action FF8C6790. The 69..128 distance gate belongs to the
other fatality; fire requires144..176. Initial80-unit controls fail; later
160-unit commands pass input/distance but are rejected at the original shared
gate because the victim is still recovering from the last uppercut. v1192
observes FF83C3D0 there, not the accepted original dizzy continuation. The
physical v1193 driver waits naturally for FFA17E10 before Up Up /release Block/
HP. It never writes guest state, health, IDs, timers, positions, CPU or graphics.

Six v1194 and six fresh v1199 cold games earn two genuine collision KOs/322
damage and activate fire without assistance: both true added victims in both
slots plus Kitana P1/Liu P2 stock controls. Every game ends0 at5198. All actions
wrap natively258 fields after activation; true victim IDs17/18 persist through
the original victim coroutine. P2's coroutine is naturally scheduled one field
later than P1's, matching same-slot stock controls. No gameplay fix is claimed
from changes to physical diagnostic timing or read-only observation.

v1201 passes all six full drawing proofs: exact current independently rebuilt
1MiB guest; byte-exact original fire/gate/facing routines; original/imported
CRC/SHA1-checked ROM graphics; all native component descriptors, caches, F0 pixel
facing, FIFO/DMA classification, actual palettes, event-ordered VRAM and actual
scanout. Original flames occlude early burn bodies; they are included in the
full replay, not removed to make an isolated sprite score pass. All seven burn
groups positively contribute visible pixels. All59 original burn palette pens
match actual hardware values. Exactly four original halfword stores clear the
physical actors, and later replayed fields have no attached-fire draws.

The stock Scorpion coroutine temporarily saves/cooperates as two original
flame actors. Its main+C0 saved A8 therefore changes at ages57..104; this does
not replace either physical fighter. v1201 binds exact original same-slot owner
phases plus independent physical actor/main/roster identities and unchanged
native save/restore code. v1200's incorrect permanent-C0 assumption remains a
preserved failure. Earlier v1195/1196 verifier exceptions and v1197's incorrect
body-flags/fixed-slot-timing/unoccluded-sprite assumptions remain preserved,
as do all unsuccessful command attempts. No failed acceptance gate is waived.

v1204 records main-agent inspection of192 unaltered actual scenes in six
contacts, including visible continue screens. Correct own pre-burn bodies/names,
native flame/skeleton/scatter/win/fatality presentation and clean continues are
present. Every burn-group vertical geometry matches the original same-slot
control. This does not prove all standing/airborne/knockdown foot heights or
floor shadows, all arenas, alternate fire victims, audio or unsampled fields.

Still required: remaining stock fatalities/victim variants and applicable
natural alternate paths; final donor choreography/audio/finisher scope; genuine
towers/Kintaro/Shao/continues/endings; complete move/human/CPU regression;
relevant arenas, secrets, cameras and cinematics; final combined CSS blinking,
border/player-number/backdrop and immediate ladder teardown/own ladder icons;
MK2 name shadows and all applicable floor shadows/foot heights. Finally promote
the matching playable CMD/release ZIP and safely remove obsolete builds. Full
natural official-roster membership remains the active goal.
