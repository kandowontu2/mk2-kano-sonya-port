# Current6AE0 finite morph regression

## All eight transformed lethal-finisher recovery cases qualify

The two additional morph_bubble_rejoin_p1/p2 cases pass detailed Orb and
fresh-match checks. Orb duration is predicted independently from its native
two-pixel travel,177 contact threshold and137 fixed animation fields; the
short-range morph cases predict146 rather than assuming the ordinary176.
Both facings/signed coordinates and invalid direction/range are unit-tested;
the ordinary current Orb fixture still qualifies with predicted176.

MORPH_FINISHER_REJOIN_MATRIX_QUALIFICATION.json now checks eight explicit
completed runs, exact four-kind/two-side coverage, actual26 ROMs, frozen
controllers, detailed finisher/identity/completion proof and600-field
freshShang recovery/palette/effect gates, with current source/evidence pins.
All eight pass. Existing six cases were requalified, not rerun/duplicated.
No native ROM/AI/game-rule changes; no emulator remains running. This is
finite transformed-finisher recovery evidence, not all interactions/audio
tails or Kano campaign clearance.

## Transformed fatality -> fresh Shang transition checks

Six morph_{extract,kiss,laser}_rejoin_p1/p2 cases complete normally and pass
both detailed fatality and physical-rejoin qualifiers on current26 ROMs/
stock MAME. SelectedShang6 performs each fatality as actual17/18, then coin/
Start/select controls enter a fresh match. All600 consecutive fresh combat
fields retain selected AND actualShang6, full initial161HP, actual damage,
zero death/winner state, no tracked child or old effect shapes, original
palette sources and exact hardware palette RGB restoration. Laser's tracked
effect object/process retirement is independently checked as before.

refresh_morph_finisher_rejoin.py runs these sequentially and only reuses
existing evidence if its terminal receipt/profile exactly matches; it never
overwrites failed runs or overlaps an existing MAME. Native ROM unchanged.
This is finite next-match evidence for these three transformed fatalities,
not orb/rejoin, every object/audio tail or whole-port completion. All six
emulator processes terminal. No visible window was opened.

## Transformed Babality cases complete

morph_baby2_17_p1/p2 and morph_baby2_18_p1/p2 complete9000 fields normally
and qualify on stock MAME/current26-ROM bytes. Kano's LK morph preserves
zero HP/LP timestamps; valid FFDD+LK at>=160 separation activates native
192-field Babality. Own Sonya baby image, dimensions, grounding and native
spawn timing pass. ActualKano17 is observed at command entry; original
MKBABY::do_babality immediately enters victory_animation, whose st_victory
calls back_to_shang_form. ActualShang6 throughout delayed Babality is thus
expected native behavior, not identity substitution. Exact timing/art gates
remain, and MKCANNED is pinned with the other source/ROM evidence.

Sonya's LP morph produces a valid DD,F+LK command at>=160 with nonzero LP
and zero HP timestamps, and native eligibility rejects it on both sides.
No activation/completion is claimed for those negative cases. Initial
unblocked-direction fixtures moved below160 and remain unqualified; the
corrected physical fixture holds Block during directions and releases it
before LK. The shared eligibility checker now requires native minimum
distance as well as actual command/punch history. Prior morphed Sonya
Friendship rejections still qualify under that stronger gate. No native
distance/eligibility/timer/ROM changes. All four processes terminal.

## Prepared transformed Babality cases

qualify_baby.py now recognizes explicit finisher-morph: selectedShang6
with actualKano17 for the positive case, or actualSonya18 at valid command
frames for the expected LP-morph native-eligibility rejection. The common
eligibility helper keeps its prior punch-rejection wrapper and adds an
explicit zero-punch command check for positive cases. Both facings and
wrong timestamp polarity are tested;15 targeted eligibility/morph tests
pass. Existing192-field timing, native completion and own baby-victim
image/dimensions/grounding gates are unchanged. Runtime pending behind
single active campaign799; no Babality pass claimed yet.
Next four cases: --game --baby --own-victim --finisher-morph --sound-candidate,
both sides; add --sonya for the two expected LP-morph rejection cases.

## Kano-morph Friendship positive control complete

morph_kano_friend_p1/p2 both complete9000 fields normally and qualify.
Shang6 wins two physical kick-only KOs, morphs to actualKano17 and performs
native193-field Friendship. Observed LK/Block/Block/HK command history has
zero HP/LP timestamps; body/bubble timing, native completion and effect
retirement pass on both sides, with actual17 throughout running fields.
This complements the LP-morph Sonya rejection: the port retains native
punch-history eligibility rather than disabling all morphed nonlethals.
No native code/ROM changes. Both emulator processes terminal.

## Pending Kano-morph nonlethal positive control

qualify_kano_friend.py now accepts explicit finisher-morph only for its
positive kick-win profile, requiring actualKano17 during all193 running
Friendship fields while selectedShang6. Existing two-KO, native LK/Block/
Block/HK history, zero HP/LP timestamps, exact body/bubble timing, completion
and effect retirement checks remain. This tests the complementary native
eligibility case: Kano's LK morph does not itself punch. Runtime remains
pending behind single hidden campaign796; no positive pass claimed.
Next physical cases: stock_wolf_6ae0_morph_kano_friend_p1/p2, --game --friend
--kano --finisher-morph --sound-candidate (plus --mirror for p2).

## Transformed Friendship native-rule rejection verified

morph_friend_negative_p1/p2 both complete9000 fields normally and pass the
explicit native-eligibility rejection check. Two natural HK-won KOs, selected
Shang6, actual Sonya18, valid B,F,B,D+Block history and no Friendship action/
completion are observed. HP/LP timestamps are both zero before the morph;
at every qualifying command observation HP remains0 and LP is nonzero.
This isolates the LP-based morph's native punch-history effect, rather than
ordinary punch-wins or an unentered command. Current26 chips/stock executable/
frozen no-write controller qualify. MOVELIST_NATIVE.txt now explains the
native nonlethal limitation. No rule exemption, timestamp clear or ROM change.
Babality's same-rule conclusion remains source-supported, not independently
runtime-certified by these Friendship cases. Both processes terminal.

## Native nonlethal eligibility caveat (source evidence, runtime pending)

The physical finisher-morph fixture now permits --friend/--baby and uses
the unchanged native minimum160 retreat target. qualify_sonya_friend.py
recognizes selectedShang6 only for an explicit finisher-morph profile;
it requires actualSonya18 at the observed command frames, native direction/
button history, nonzero punch timestamp, two natural KOs and no completion.
This is a negative native-eligibility case, not a positive Friendship pass.
Runtime remains queued behind active campaign794; no overlapping emulator
was launched. All238 local tests pass. Suggested next case:
stock_wolf_6ae0_morph_friend_negative_p1 --game --friend --finisher-morph
--sound-candidate, followed by the matching mirrored case.

MKFRIEND::fs_check requires both fs_get_tsl(l_hp) and fs_get_tsl(l_lp) to
return zero. fs_get_tsl reads the player's timestamp directly; MOVES::
bj_lo_punch calls update_tsl_a1 before button/character dispatch, and that
routine stores current tick without a winner-status exemption. Sonya's
added morph uses LP. Thus a physical Sonya morph during Finish Him can
invalidate Friendship eligibility even when Shang won using only kicks.
Do not erase the timestamp or exempt IDs17/18 merely to pass a transformed
Friendship fixture. Original native-rule compatibility is required; runtime
command/history observation remains needed before declaring this negative
case demonstrated. Ordinary selected-Sonya nonlethals have separate tests.
MKBABY::bb_check independently has the same zero-HP/LP timestamp tests
before command lookup. The corresponding Babality caveat is therefore
source-supported too; a runtime rejection is not yet certified here.

## Transformed orb completion checkpoint

morph_bubble3_p1/p2 complete9000 fields normally and qualify with actual
Sonya18 during the finisher while selectedShang6. Physical two-KO/morph/
orb commands yield146 running fields (nine travel), all14 orb poses,
growth/enclosure/burst/salute, native victim stumble, completion and actual
object/dummy retirement. Native completion retains action0220h (544), unlike
laser's immediate0404h morph-back; the qualifier keeps the original exact
orb completion action. No guessed laser behavior is applied to orb.

The failed initial/bubble2 traces show first morph inputs overlapping
Shang's post-KO reaction; the modulo retry loses a command cycle. The
controller now starts its morph clock only after actual0303h neutral
stance. Combined with physical retreat to native minimum160, the full
command fits the unchanged prompt. No ROM distance/timer/AI changes.
All237 local tests pass. Finite both-sided transformed checks now include
all four own lethal fatalities; wider interactions/audio/rejoin and Kano
campaign clearance remain open. No emulator remains running.

## Additional transformed-finisher checkpoint

morph_laser_p1/p2 and morph_kiss_p1/p2 complete9000 fields normally and
pass existing detailed art/timing/retirement qualifiers plus actual own
identity checks with selectedShang6. Laser completion immediately enters
native morph-back0404h at exactly first+176, rather than retaining0547h;
the morphed-only completion check names that exact state/timing and keeps
all beam/dummy retirement gates. Kiss passes its existing231-field checks.
All237 local tests pass. No native ASM/ROM changes.

Both initial morph_bubble cases lack activation and remain unqualified.
After morphing, retreat to the fixture's220 target consumes the remaining
prompt. bubble2_p1 now targets the native required160 separation through
physical movement only. Activation/completion remain pending; no range or
Finish Him timer change. Earlier failed evidence is retained.

## Transformed extraction checkpoint

morph_extract2_p1/p2 both complete9000 fields normally; qualify_extract
passes the full existing animation/completion checks with explicit selected
Shang6 versus actual Kano17 identity observation. Two physical KOs precede
the native winner3 prompt; the morph command occurs then, and all231 running
fatality fields remain actual17. Nine body poses, six skeleton phases, six
victim phases, age83 spawn and eight-field early skeleton cadence pass.
No health/identity/winner/death writes or custom driver. All236 local tests
pass. This does not certify the other transformed fatalities, next-match
teardown or complete audio. Native program/package remain unchanged6AE0.

## Pending transformed-finisher fixture

--finisher-morph selects Shang6, earns rounds using physical attacks and
requests the own morph during the native winner3 prompt before the own
finisher command. A separate read-only morph_finish.csv logs selected vs
actual identity. First morph_extract_p1 did not navigate selection: the
wrapper lacked KS_SELECT tables for this new profile, so no requested match
or KOs occurred. It is not a finisher/morph failure or qualifying evidence.
The wrapper now supplies the existing KSNAV tables; morph_extract2_p1 is
running hidden/BelowNormal. No guest writes, native source or ROM changes.

## Completed transformed Square Wave checkpoint

extended_square_p1/p2 both complete9000 fields normally and pass the
current26-ROM/stock/frozen-controller morph qualifier. The grounded command
attempt does not produce0207h; the later physical opponent jump does.
Actual Sonya18 Square Wave lasts44 observed action fields, deals27 native
damage and recovers before524-field morph expiry. The launch observes the
opponent's native jump state, not an injected airborne flag. Own art/IDs
and automatic return pass. All235 local tests pass. No native code/ROM
changes or emulator left running. Together with projectile/Ball/melee/
grapple fixtures this supplies finite both-sided transformed coverage for
all eight named specials, not every move/victim/edge or transformed finisher.

## Completed transformed Choke/Leg Grab checkpoint

extended_grapples_p1/p2 both finish9000 fields normally and qualify on
stock MAME/current26 chips. Selected Shang6 transforms natively; Kano's
535 owner/536 victim hold lasts69 consecutive fields and deals32 damage.
Sonya's538 owner/539 victim hold lasts46 consecutive fields and deals35.
Both actor and idle Sonya victim return to stance before native morph
expiry. Actual own IDs/poses and all three524-field segments pass. The
observer now records victimAction explicitly instead of inferring takeover
from the owner's state. All234 local tests pass. Native ASM/ROM unchanged;
neither emulator remains live. This is a finite transformed-pair check,
not every victim, interruption, edge, late-expiry, or finisher path.

## Completed transformed Blade/Bicycle checkpoint

extended_melee3_p1 and extended_melee3_p2 both complete9000 fields normally
and pass qualify_morph.py on stock MAME/current26-ROM bytes. Selected Shang
remains6 while active own IDs/poses are17 and18. Blade0117h activates and
deals26; bicycle0204h enters owner hit0214h and deals22. Both recover to
stance before automatic native return, with524-field own segments. The
idle opponent is Sonya18. This is finite owner-state/contact/recovery
evidence, not exhaustive victim takeover/edge/interruption/audio proof.
The command-timing failure and subsequent whiff fixtures remain failed;
only melee3 is qualified. All233 local tests pass. No native ASM/ROM/game
balance changes; no emulator remains running.

## Pending transformed Blade/Bicycle extension

melee2_p1 completed: corrected command activates bicycle0204h for19 fields,
then whiff recovery0611h for42 fields, without paired0214h state. The
qualifier rejects the missing hit/damage, not activation. Blade still deals
26. Next physical fixture approaches during Sonya1040..1094 to64 pixels
before requesting the unchanged B,B,D,HK command. No move range/damage or
native code is altered to satisfy the fixture.

The optional --morph-melee physical fixture first approaches to84 pixels,
then requests Blade after Kano morph and bicycle after Sonya morph.
extended_melee_p1 completed but failed qualification: Blade dealt26, while
bicycle did not activate. Its first-back-to-HK interval was50 fields, longer
than KSCMD::ks_bike_command's024h history window. This is a fixture timing
failure, not evidence of a transformed-move defect. The corrected melee2_p1
run uses B at1100, B1110, D1120 and HK1126, the same26-field interval as
the established native bicycle fixture. Result pending; no native changes.
The failed completed evidence is retained, not overwritten or marked passed.

## Completed transformed Ball checkpoint

stock_wolf_6ae0_extended_ball_p1 and ball_p2 both finish9000 fields normally
and qualify on exact stock MAME/current26 ROM chips. Selected actor remains
Shang6; transformed Kano17 enters020bh for18 fields, deals24 damage to the
idle Sonya opponent, recovers before expiry and returns automatically.
The existing three morph segments retain524-field duration each and all
observed actor poses belong to own/native transition tables. Neither guest
identity/timer/health nor result is written by the controller. Both requested
100-field LK holds are physical input. This extends finite transformed-move
coverage beyond Knife/Ring and paired throws, not every transformed move or
finisher/edge/audio path. No native ROM changes. Both processes terminal.

Prepared next runtime case: --morph-ball, mutually exclusive with projectile
and throw profiles, physically holds LK for100 fields at fight250..349.
qualify_morph.py now requires actual020bh state only while Kano17,24 damage
against the idle opponent, recovery before expiry, and the existing full
identity/pose/native-return/current-ROM gates. Runtime evidence is not yet
collected; adaptive campaign793 currently owns the single hidden emulator.
Full local discovery passes231 tests. No native source/program change.

The sequential runner now accepts explicit --ball-only and produces ball_p1/
ball_p2 fixtures, preserving its existing-emulator guard and no-overwrite
rule. Eight morph source/plan tests pass. After793 terminates, run:
python refresh_morph_regression.py stock_wolf_6ae0_extended --ball-only
No Ball runtime pass is claimed until both completed receipts qualify.

Program6AE0A069BDFCF4AB2E2F2A1E3B0B7481735AC2654E0036D9331280037BB8BAF9.
Four stock_wolf_6ae0_morph runs complete9000 fields normally on stock MAME:
special_p1/special_p2 and late_p1/late_p2. Each detailed qualification.json
verifies actual26 current ROM chips and frozen physical-input observation.

Special cases keep selected Shang6 while active identities transition
6→17→6→18→6→18→6. Own morph commands, both Sonya button orders, actual
own poses, temporary duration/reversion and the tested Knife/Ring hit gates
pass. The two art traces additionally verify forward/reverse intermediate
pose order, four-field cadence and measured entry/reverse grounding.

Late cases initiate an actual paired throw before nominal morph expiry.
Own identity persists through the throw, native damage is34, and return
occurs after the held victim is safely released, not mid-hold. Neither
identity nor timer is forced by the controller. No game/ROM/AI changes.

These are finite projectile/paired-throw expiry and art-trace cases, not
all transformed specials/finishers, every victim/edge/interruption or full
palette/audio/visual acceptance. Kano's earned campaign and final broader
acceptance remain open. No final release completion is claimed.
