# Current-ROM Sonya / Kitana campaign evidence

## Run677: native input-readiness counter, first observed Kitana round win

The optional --campaign-sonya-kitana-rfp-duck requires Sonya and the existing
guarded Kitana Ring policy. It uses the same bounded native RFP context,
signed rendered height, actual linked duck-button table, normal process
flags and readiness-timed12-field counter cooldown verified for Kano/Sub-Zero.
Only target18/opponent4 uses this new policy. Low/final/recovering punches
retain crouch-block; high punches can be ducked and countered with native
HP when actual attack dispatch is enabled. No move, collision, health, AI,
difficulty, position, result register or ROM code is changed.

The shared nativeDuckCounter selector retains the old Sub-Zero predicate
when this new option is disabled. Native table validation still checks all
five real linked bt_duck handlers against JOY.LST/MAP and actual program ROM.
Existing tests were updated for the shared predicate without removing the
Sub-Zero readiness, bounds, geometry, cooldown, ground or flag checks.
106 selected local tests pass. A new source-contract test scopes Sonya's
option and dependency; its initial lexical block split was corrected not
to split the letters "end" inside renderedHeight. No game/test behavioral
condition was relaxed by that test repair.

677 freezes controller SHA256:
B48E33C568DB7A7AE5D2B42CE6A60DFC0F4F1E35D972B88A2A4495C13058C1E4.
It exits normally86706, reason left-campaign after20 bounded paid continues.
Full current26-chip, true actor18/selected18, immutable read-only controller,
no missing-root/no-illegal-recovery checks pass. All20634 trace data rows
before Kitana exactly match603, SHA256
0E18BD570D748504B7614553136D84A2AE912970B3FE43420B592EAA545D7918.
That includes native results/intro rows, not only combat observations.
Baraka, Reptile and Jax are defeated on attempt0 and Raiden on attempt7,
preserving the earlier natural same-attempt match results.

## Observed native counters

The RFP log records3613 classified fields and six HP requests. All six have
rendered height64, native flags clear of reaction/special/sitduck, actual
bt_duck=ff831ae0, grounded actor, Down held/Block released and distance78–79.
Each leads to actual uppercut action107h and a corresponding victim HP drop:

| HP request | First sampled uppercut | Damage observation | Kitana HP |
| --- | --- | --- | --- |
| 57839 | 57844 | 57848 | 156→116 |
| 64837 | 64842 | 64846 | 139→99 |
| 70836 | 70840 | 70844 | 117→77 |
| 71065 | 71070 | 71074 | 77→37 |
| 82352 | 82356 | 82360 | 73→33 |
| 82580 | 82584 | 82588 | 33→0 (KO, remaining health clamped) |

The first five observed drops are40; the last removes the remaining33.
This is request-linked native activation/contact evidence, not only input
requests or aggregate action tags. Fan source review also confirms Kitana's
get_fan_obj/spawn_proj_proc uses generic P2 projectile PID0800h; no Sub-Zero-
style ice PID extension was needed or silently added for this run.

## Native round result, not match/campaign completion

On attempt20, native round1 result82782 has winner1 and match counters1/0
with Kitana0HP. Sonya's minimum HP during that winning round is77.
There is one certified Kitana winning round out of29 observed Kitana rounds,
not a full match win. Kitana wins the next two rounds, so the attempt ends
1–2 and map position remains4. No Liu/later-roster/boss/earned-ending runtime
coverage is implied. This is new finite Sonya campaign progress; full
campaigns, later bosses, endings/cast/credits and release acceptance remain
unverified. No custom MAME driver or game-memory writes were used.

Evidence SHA256 pins: rfp_control.csv
1895158BF3145F4F2F4B7CF1D0B368B123471F7FE5BC226755EA725AB0B69923;
campaign.csv
64FC731EC910E2DC5408886C4BE745933FD1A2C62F54E36D322B5B1BA8B2FB80.

## Run678: recovery-window uppercuts are executable but not safe openings

677 contains738 classified recovery fields,455 within105 pixels with the
player's reaction/special/sitduck flags clear. The optional
--campaign-sonya-kitana-recover-counter tests an18-field bounded wait after
such a recovery: release Block naturally, wait for rendered shortness and
the actual native duck table, then request HP with the existing cooldown.
It cancels on detected threat/pressure, reaction, airborne state or lost
spacing. A separate recovery log records waiting/fired/cancelled cases;
existing controls remain unchanged when the option is disabled.

678 freezes controller SHA256:
9CE1E9225342AE6FD902AF2B1520D684922E7CB62CE1CAC087A5EEC5E5C5A0B3.
It exits normally83977 (left-campaign) and passes full26-chip/identity/
frozen-read-only/no-marker/no-recovery audit. All20634 pre-Kitana rows exactly
match603.107 selected local tests pass; native table, bounds and safety
conditions were retained. No native game/AI/health/difficulty/ROM code changes.

The recovery log has485 waiting,44 cancelled and37 fired fields, with
maximum observed age15 (within the18-field limit). All fired inputs have
height64, duck tableff831ae0, clear reaction/special/sitduck flags, Down held,
Block released and HP requested.35 requests are followed by uppercut action
within14 fields. None has an observed CPU HP drop in that14-field window.
The other two requests do not have sampled uppercut activation in that
window and are not counted as successful dispatch. Early14-field windows
also show no own damage; that does NOT imply the attempts were safe, because
throw damage lands later.

At41572 HP is requested with Sonya112HP/Kitana139HP. Uppercut appears41576,
then Kitana enters native body-slam507h at41578, Sonya becomes airborne and
her process gains reaction flags. By41600 Sonya's HP is82 (30 lost), while
Kitana remains139. This is direct startup punishment, not merely a harmless
whiff or evidence that the uppercut's collision box is broken. The observed
CPU shapes do not match the sampled native duck/duck-block frame lists, so
ducking is not assigned as the cause of this example. MKDRONE's native
body-slam routine checks airborne/height/away-stick conditions; those rules
were not disabled or weakened to obtain a test win.

All28 observed Kitana rounds are lost (best CPU minimum28);677's winning
round is not reproduced under this changed policy. The recovery-counter
option therefore remains experimental/default-off, not an adopted campaign
strategy. The guarded high-punch counter from677 remains separately
qualified. The new result disproves treating every RFP recovery as a safe
uppercut opening. Full campaign, later bosses and earned endings remain open.
SHA256 pins: recovery_counter.csv
2063422E66C8BBE9A12E034AC7A5EC6EF942062BA60DD53E06810BAA87BEE0FF;
campaign.csv
A46255A78F98F0592A5214DD850C49EFC2A68FE33F9D18CEBD4ED91685F8F7E0.

## Run679: recovery re-arming bug fixed, tactic remains unqualified

Further inspection of678 finds a real controller defect: after HP41572,
it re-arms waiting41573 (age0), keeps Block/away released through own
special flags17 at41574–41577, and cancels only on reaction flags21 at41578.
The initial arming predicate lacked the firing cooldown. Thus678's unsafe
startup included a harness-caused guard release; it was not a clean test
of the intended recovery policy.

The arming condition now also requires the12-field cooldown, and an active
wait cancels on any native reaction/special/sitduck flag, not only reaction.
No game state is altered to enforce either rule. Frozen679 controller:
7872C4184DD6FB0E809B34A61F637CD52D9D2DF6B0C007DB5C8D615FED007295.
108 selected local tests pass, including explicit arming-gate cooldown and
the recorded41572→41573 regression. Earlier safety assertions are retained
and the cancellation mask is strengthened.

679 exits normally83822, left-campaign. Full26-chip/identity/frozen-read-
only/no-marker/no-recovery audit passes; all20634 pre-Kitana rows match603.
The recovery log records211 waiting,7 cancelled and46 fired fields, maximum
age15, and zero new age0 waits inside the prior request's12-field cooldown.
The first example now holds Block+away at41573–41578 rather than dropping
guard. This verifies the correction is actually exercised.

There is still no Kitana round win in28 rounds (best CPU minimum36).
38 recovery requests have nearby sampled uppercut actions, five have a
nearby CPU HP drop, and27 have a body-slam action within14 fields. These
are correlated windows, not five independently certified counter hits or
27 unique throws. In the original41572 example, the body slam is avoided:
Kitana now ducks during Sonya's uppercut41578–41580, then uses her own
uppercut41584–41586; Sonya loses40HP by41588 (112→72), Kitana remains139.
Displayed shapesff9e5ec0/ff9e5f40 match the actual linked duck animation
index5 frame list, so the duck interpretation does not rely on a tag alone.
Thus fixing the guard bug changes the response but does not turn that
recovery into a safe uppercut opening. The optional recovery policy remains
default-off;677's high-punch counter remains separately qualified.
Native game/ROM/AI/difficulty/health rules are unchanged. Full campaigns,
later bosses and earned endings remain unfinished.
SHA256 pins: recovery_counter.csv
E06E77995C757C7C0A6DB8A7D61CC7348C30E2F6880AE1D9505524E559D237A8;
campaign.csv
12291815F276697F34D39898EC8DF7B4229FD2B32B2FAC658EB520A6B83B5501.

## Run680: native crouching low-kick comparison, not a winning tactic

The optional --campaign-sonya-kitana-recover-kick requires the bounded
recovery-counter option and substitutes only Low Kick for recovery HP.
The separate high-RFP uppercut remains unchanged. Duck-table, body-height,
ground, process flags, cancellation and cooldown checks are retained; the
log adds LK alongside HP to distinguish actual requested buttons. The
actual native bt_duck slot4 maps to joy_duck_kickl, whose MOVES handler uses
act_duck_kickl=11ah and animation1ah. No new executable game code, hitbox,
strength, AI, health or difficulty change is introduced.

680 freezes controller SHA256:
43EF3B4672733DCE09A85812D1E2702E00D2EEC3269E4C87577A021717F1AD47.
It exits normally85111, left-campaign. Full26-chip/identity/read-only/frozen
controller/no-marker/no-recovery audit passes. All20634 pre-Kitana rows
match603 exactly, preserving Baraka/Reptile/Jax/Raiden match wins.109
selected local tests pass, including optional button routing, dependency
and the native crouching low-kick handler. The old HP path remains checked.

All36 recovery fires have LK1/HP0, rendered shortness, validated duck table,
normal flags and Down held/Block released. Each has a sampled native11ah
action within14 fields, confirming dispatch of the intended crouching kick.
Five nearby CPU damage windows show four2-HP drops and one6-HP drop;31 have
no CPU drop.31 request windows include a CPU body-slam tag. These are finite
nearby-window observations, not proof of31 unique throws or certification
of each damage source. Native input dispatch is working, but counter safety
or a winning tactic is not established.

All28 Kitana rounds lose (best CPU minimum55); this is worse than677's
one native round win. The recovery-kick option remains experimental and
default-off. No game/ROM/MAME-driver code was changed to make the tactic
pass. Full campaigns, later bosses, earned endings and final acceptance
remain unfinished.

SHA256 pins: recovery_counter.csv
B9293D6F2BEA24D41B5011C51F208792686B54195809B2929A6C1E190457F17F;
campaign.csv
599C03E223D7B8D167CBEA3EA3CCC336852E886C87EBA5448BA5B7800C3B722B.

## Run681: established-guard Leg Grab, native2–0 Kitana match win

The optional --campaign-sonya-kitana-guard-leg requires the punch-aware
guarded Ring profile. It counts prior grounded/normal-flag Down+Block
fields, then during a detected RFP recovery within85 pixels and with at
least4 established guard fields requests the existing Down+LP+Block chord
for4 fields. It requires measured initial shortness and no detected threat/
pressure, cancels on reaction and retries no faster than90 fields. Existing
high-punch uppercut counters remain. No forced neutral/move state, proxy ID,
damage/AI/difficulty/health/collision or ROM changes are used.

KSCMD's native LP and Block handlers check the live leg chord before normal
button dispatch, and do_switches_match masks the required Down bit. Thus
this special is not incorrectly required to leave block and install the
normal bt_duck attack table. The native handler/owner/busy checks remain
unchanged. Fallback guard is prevented from clearing Down during the chord.
110 selected local tests pass, including prior guard, four-field LP hold,
native chord masks, bounds and no guest writes. An old lexical fallback
assertion was updated to require the added chord protection as well.

681 freezes controller SHA256:
1D1B4EE4ACAC99CFA0B41344897751B2D0EC90FC72FB2BF0C12E9455D2F59181.
It exits normally82693, left-campaign. Full26-chip/identity18/frozen-read-
only/no-marker/no-recovery audit passes. All20634 pre-Kitana rows exactly
match603, preserving the Baraka/Reptile/Jax and attempt7 Raiden match wins.

Two4-field chords start41573/43462, after4/9 prior guard fields respectively,
with initial measured heights62/80, flags1 and distance79. Both retain
Down+Block while LP is held. Actual Leg Grab paired states21ah/21bh run
for46 consecutive dense counter observations each:41586–41631 and
43475–43520. The main trace observes35-HP release damage139→104 by41634
and73→38 by43522, consistent with the separately qualified native release
timing. There is no merely-requested/seek-only grab claim here.

Native same-attempt result counters verify Kitana2–0 on attempt7:
42576 winner1/counters1–0, Sonya30HP/Kitana0;
43998 winner1/counters2–0, Sonya78HP/Kitana0.
This is the first observed current-program full Sonya/Kitana match win,
not an aggregation of wins across continues. Native progression reaches
map5/Liu while Sonya's selected/object identity stays18.

Liu is not defeated:28 observed rounds across attempts7–20 have no player
KO win, and the run ends on map5. Later roster/bosses/endings/cast/credits
and full campaign completion are not implied by the Kitana improvement.
Native game and stock MAME code are unchanged.

### 682: Liu-specific guarded Leg controller

The opt-in `--campaign-sonya-liu-guard-leg` extends the physical-input
guarded Ring/RFP/Leg policy to Sonya versus Liu only. It uses the same
linked native duck-button table, measured body height, bounded cooldown,
prior Down+Block guard and four-field LP chord. No ROM, CPU difficulty,
health, selection or outcome writes were added. 111 selected tests pass.

Run stock_wolf_game682 exits normally at87975, not a timeout. The stock
MAME/actual26-chip/read-only-controller/identity18 audit passes. All22154
rows before Liu exactly match681; prefix SHA256:
95FCFB34516A56693BAC215CCE5E24F47ADCF9C039710114B1507925FE98DA02.
Thus the earlier Kitana2–0 and earlier match results remain unchanged.

Liu is naturally defeated2–1 on attempt8: native result50330 has counters
1–1 and result51354 has counters2–1, with opponent HP0 in both winning
rounds. The audit does not aggregate separate continues into a match.
Native progression reaches map6/Sub-Zero, but no full campaign is proven:
the run ends left-campaign on map6 after exhausting the bounded continues.
Later roster, bosses, endings, cast and credits still require earned proof.
This demonstrates campaign progression, not complete move/cleanup coverage.

Frozen controller SHA256:
4088A1BF2B8CB819D792DFB517D65D57CC5725B85B2AAA075DE2E730221761A8.
campaign.csv SHA256:
09CD882DABD6C0FB233DA732AE1A3792284FBBEE70EAA9E66570F4E92CA22545.
MAME was observed with no window, BelowNormal priority, about200MiB RAM.

SHA256 pins: guard_leg.csv
A7EA4A048FB748C926656892FCFC6668D202B7A9E03EE87656E524C1942B1167;
campaign.csv
408AFF3214C9A97E46D6DA28FE08CAEAA734812017430D668B78BDADD8654FBB.
