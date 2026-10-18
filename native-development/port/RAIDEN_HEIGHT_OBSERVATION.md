# Native throw protection: bounded runtime check

Stock MAME run `stock_wolf_game558`, fields 13750–14050, observes actual
player multipart RAM without changing game memory. The observer mirrors
`MKUTIL.highest_mpart` (112-bit records, signed Y offset at bit 96) and uses
the linked global `ground_y`, as `get_my_height` does. `p_ganiy` is an
animation anchor, **not** the ground used by this native height calculation.

Sonya's sampled action 0303 heights: 103–120 pixels (3 fields).
Standing block 0700: 117 pixels (15 fields).
Crouch block 0701: 62–75 pixels (81 fields).
This bounded sample contradicts the hypothesis that her sampled standing
bounds always classify her as short; it does not qualify every animation.

`MKDRONE.drone_body_slam` skips joystick Away protection when
`is_he_short` reports height at most 96 pixels. Thus a crouch/Away controller
does not obtain standing/Away throw protection. No native AI or ROM change
was made to bypass this rule. The next controller trial stands and blocks
between attacks, retaining Down during the Leg Grab input itself.

Run 557 was an initial observer trial that logged `p_ganiy` under the misleading
column name `ground`; do not use that column to calculate native height.
Run 558 corrects this and separately logs `animationGround`.
No campaign completion or ending verification is claimed here.

## Standing guard trial

Run 559 completed 30,025 fields with one ordinary paid continue. Baraka,
Reptile and Jax were naturally defeated again. Raiden still won all four
rounds: Sonya's minimum health was 77/127/65/47, while Raiden's was
161/161/161/156. Standing guard improves survival but does not create an
effective punish. The campaign audit verified current full ROMs and found
no missing-animation markers or illegal-opcode recovery. This controller
is not a campaign solution; further work must address actual attack timing
and spacing, not weaken the native AI or claim a successful campaign.

## Interrupted action tag, not a demonstrated startup lock

Run 560 repeats the first attempt with bounded process observations at
13680–13980. Sonya enters Leg startup at 13693, animates through 13710,
then traverses native block-reaction code. At 13745–13980 her saved wake
address is ff831d30, inside the linked native `joy_block_loop`, despite
action 0219 remaining set. Thus thousands of 0219 CSV rows alone are not
proof of a Leg startup freeze. The controller's readiness predicate, which
excluded 0219, could keep holding Block forever after this interruption.
The subsequent trial periodically releases guard with physical input when
this stale-tag condition persists, allowing native stance to refresh it.
No action-state memory is written and no ROM change is claimed.

Run 561 completed 20,970 fields, including one ordinary paid continue.
The physical guard release allowed further attack attempts (five Ring
episodes across the campaign versus two in run 559), but did not solve
Raiden: his four round minima were 161/161/161/134. Sonya still naturally
cleared the first three opponents. Current ROM/identity/no-fault audit
passed; full campaign remains false. The next policy should stop initiating
the slow, duck-blockable Leg Grab into Raiden's neutral crouch and instead
establish a genuine recovery punish. The 26 source/tooling unit tests pass.

## Low-kick and native-guard readiness trials

Run 562 replaces neutral close-range Leg Grab with released-guard Back+LK;
recovery Leg Grab remains unchanged. It reaches Raiden but loses four rounds,
CPU minima 161/141/134/161. Only two sweep (0106) episodes appear across the
campaign. Native `JOY.joy_med_kick` confirms Away+LK selects sweep, except
`knee_check` substitutes a knee at distance at most 64 against grounded targets.

Run 563 additionally recognizes the observed saved wake at
`joy_block_loop+0x50`, read-only, as a guard-ready state even with an old action
tag. It completes 20,731 fields, one paid continue, first three opponents
defeated, Raiden losses with CPU minima 161/68/161/161. This is improved damage
in one round, not a successful matchup or campaign. Seven Ring episodes and
one sweep episode occur across the campaign; requested sweeps must not be
reported as repeated native sweep activations. Current full-ROM/no-fault audit
passes. All 27 source/tooling unit tests pass. No ROM/AI change was made.

Run 564 waits for actual stance 0303 before beginning sweep/Ring input clocks,
rather than spending their first input frames in unblock animation. It completes
19,700 fields with one paid continue; first three opponents defeated again.
Five native sweep and nine Ring action episodes occur across the campaign
(versus one and seven in 563), but Raiden wins all four rounds with minima
117/156/161/151. More recognized commands are not a successful strategy.
Full-ROM/no-fault audit passes; full campaign and port verification stay false.

Run 565 explicitly extends the existing jump-grapple policy to Raiden
(`--campaign-raiden-jump`, no Raiden-counter flag). Previously the generic
uppercut branch intercepted this opponent, so merely specifying jump-grapple
did not test jump-grapple against him. This controlled alternative completes
19,199 fields, clears the first three opponents, and loses Raiden's four
rounds with CPU minima 135/126/100/135. Actual jump 0308 and flying-kick 0200
episode totals increase to 49/43 across the campaign (564: 23/23); Leg hold
021a increases from 15 to 17. The alternative lands more consistent damage
but does not win a round. Current full-ROM/no-fault audit passes; no campaign
completion, ending verification or final release is claimed.

## Stance-ready guarded Ring: first earned Raiden round

Run571 (`--campaign-sonya-raiden-ring`) reuses the guarded-projectile state
machine, but sends Sonya's actual Down/Toward/LP rather than Kano's
Down/Away/HP. It waits for native stance before starting the command clock,
guards active CPU projectile PID0800 and Raiden Bolt000f/Dive0209, and holds
Block+Away during the otherwise idle first60 fields of the Raiden round.
The first three opponents' tested input policy is unchanged. No ROM, native
AI, health, difficulty or driver is modified.

The run completes22931 fields with one ordinary paid continue. Sonya earns
her first Raiden round win in this comparison (remaining HP43, CPU0), loses
round2 (CPU134), then loses the deciding round with Raiden at2 HP. The paid
continue loses two rounds at CPU134/107. Thus Raiden is not defeated and
later stages/endings remain unverified. The first three opponents are again
naturally defeated. Current full-ROM/identity/no-fault audit passes; the
source/tooling unit suite passes32 tests. Across the campaign there are48
native Ring0212 action episodes, not merely requested button sequences.

## Expanded paid-continue coverage

Run572 extends the same policy to three ordinary paid continues, without an
input-policy edit. The initial-attempt CSV prefix before18604 is byte-identical
to571:778274 bytes, SHA256
48EE0A8AA7E2CFF80E12EFDCAA46F83DDC2E1A284F3E777E45C6EB6FD9BB8BB3.
It ends normally at30818 fields. Sonya wins another Raiden round on paid
attempt2, round2, with111 HP remaining, but loses its deciding round (CPU63).
Attempt3 loses both rounds (CPU139/85). Round wins across separate paid
attempts are not a match win; Raiden and later stages remain unverified.

All three paid continues are logged through native buy-in, selection and
combat. Complete current ROM/own identity/no-fault audit passes. No new ROM,
AI change, patch release or ending claim is made. The unchanged policy can
win individual rounds, but the added coverage contradicts treating it as a
reliable campaign controller.

## Guard following observed damage

Run573 adds opt-in `--campaign-guard-after-hit` to the guarded-projectile
controller. Any observed health drop extends a24-field physical guard period
and clears the pending input sequence. It does not cancel an executing native
move, write game state, or modify AI. Standing guard is kept close; Down is
added at distance>=120 as in the preceding policy. This specifically avoids
repeatedly beginning commands during continued close-range pressure.

It completes32954 fields with three ordinary paid continues, again clearing
the first three opponents. Across ten Raiden rounds, CPU minima are
0/24/68,68/19,112/19,2/0/24 (commas separate paid attempts). Two rounds are
won, but on different attempts; **no Raiden match is won**. Mean CPU minimum
health falls from79.8 in572 to43.6 in573, a descriptive comparison of these
finite runs, not a statistical reliability claim. Many losses are now close,
but later stages/endings remain unverified. Full-ROM/identity/no-fault audit
passes;33 source/tooling tests pass. No ROM or final release was generated.

## Shorter guard comparison rejected

MKDRONE.drone_rfp has separate strike/pause and final unpunch animation
phases. This motivated testing a shorter post-hit hold, but source timing
alone does not establish the right punish window. The harness now accepts
bounded `--campaign-post-hit-fields=0..64`, explicitly defaulting to24 so an
inherited host environment cannot silently change that default.

Run574 tests12 fields with three paid continues and the otherwise same
Sonya policy. It ends normally at28077 fields. Raiden wins all eight rounds;
CPU minima68/90,112/139,134/29,107/139. This contradicts the shorter-delay
hypothesis for this comparison. The tested default remains24, not12. All
current ROM/identity/no-fault checks and33 source/tooling tests pass, but
neither delay provides a verified campaign solution. No ROM change is made.
