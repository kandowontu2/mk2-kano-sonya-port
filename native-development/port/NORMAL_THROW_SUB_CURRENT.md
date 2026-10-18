# Kano normal throw versus Sub-Zero

Two fresh9000-field stock-MAME fixtures qualify on current26 ROM bytes:
stock_wolf_6ae0_throw_sub_p1 and p2. Each physically approaches and throws
original Sub-Zero8 with actual Kano17:28 owner action fields, seven own body
poses,34 damage and221 grounded paired-stance recovery observations. This
tests a stationary opponent, not a successful campaign strategy.

qualify_own_throw.py now verifies the actual26-chip archive, exact stock
executable receipt pin, frozen no-write observer, native throw profile, paired
grounded recovery and source/runtime/capture evidence hashes. Empty, duplicate
and outside-directory invocations are rejected instead of silent success.

## Completed physical campaign trial

The trial completes120000 fields normally, exit0/no timeout. Current26-ROM/
stock/frozen-controller campaign audit passes.39776 pre-Sub rows exactly match
799. The controller requests approach for2111 fields but requests ZERO throws;
there is no Sub round win or map advance. Last mode4, map6, winner2. This is not
an observed native throw failure: no throw command was issued under CPU pressure.

The nearest both-grounded/not-busy/no-projectile eligible approach separation
is71, above the controller's60-pixel entry gate. The successful stationary
fixture enters its throw at57, from a preceding62-pixel walking field. JOY's
joy_lo_punch loads native040h (64) into A7 before toss_check; get_x_dist must be
within A7. Native MKDRONE slam distances begin at046h (70) and reach050h (80),
with additional native frequency/eligibility rules. Thus merely changing this
controller threshold from60 to64 would still not exercise the observed71-pixel
closest ready state. There is no evidence to widen the game's throw range,
weaken CPU rules or report a thrown match from this trial. Any further physical
strategy must address the CPU-pressure entry window, not assume the command ran.

stock_wolf_6ae0_kano_normal_throw uses --campaign-kano-sub-normal-throw with
the previous799 earlier-route options, excluding its Ball-specific profile.
The new branch is explicitly Kano17 versus Sub8 only. It guards standing with
Away by default; detected projectile/ice/slide threats request crouch-block.
When both fighters are grounded/not busy and no projectile is active, it
requests approach beyond60 pixels; within60 it releases guard/directions,
waits for actual standing action303h, then requests Forward+LP no faster than
every12 fields. Native range, throw rejection, AI, damage and charge rules are
not modified. sub_normal_throw.csv logs observed state and requested inputs.

inspect_sub_normal_throw.py checks the completed campaign's real26-ROM audit,
request/approach/prepare gates and next-eight-field native507h observations.
Requests without an observed activation are not converted to passes; incomplete
windows are null. This does not infer damage, a native match win or campaign
clearance from input requests. Earlier-route exact comparison is still required.

All285 local tests pass. Two old source-inspection tests were narrowed to the
actual Kintaro branch boundary: their previous substring ranges accidentally
included later Kano branches. The Kintaro code itself was not changed.

The campaign is terminal; no emulator/compiler remains running. No successful
campaign result is claimed. Native program and development IPS ZIP unchanged.
The new wrapper source pin will need the normal explicit evidence refresh once
controller work stabilizes; no source-hash gates are relaxed.
