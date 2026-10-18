# Current Raiden controller evidence

Current native program/IPS remain unchanged. Raiden is native7, not Mileena5.
All tests below use stock MAME, physical controls, the current26 verified ROMs,
no cheats/game writes, and explicitly logged ordinary paid continues.

Run551 retains earned Baraka/Reptile/Jax wins; Jax is2–0 at135/93 health. Its
guard/Ring/Leg dive-recovery policy fails Raiden through three continues. The
counter telemetry records756 fields of native Raiden dive recovery0602, but
many opportunities occur while Sonya is blocking, rising or in another state.
The raw tag alone is not proof a new command can activate.

Run552 replaces the recovery punish with Bicycle B,B,D+HK, using the earlier
isolated-move timing (Back at0/10, Down20, HK26). It preserves the first three
match wins but fails Raiden, ending27,655 fields. No Bicycle0204 activation
occurs in the target matchup. This is not a valid test of Bicycle's effectiveness
against Raiden, and must not justify altering its game implementation.

Run553 shortens the sequence (Back0/6, Down9, HK12) and uses one paid continue.
It again preserves Jax2–0 at135/93, then loses four Raiden rounds, ending21,063
fields. Target telemetry has32 HK-request fields but no Bicycle0204; ordinary
high-kick0103 episodes occur instead. One Leg Grab hold021a lasts46 fields and
accounts for35 observed damage (Raiden minimum126) in one round.

The first attempted short sequence illustrates the remaining input issue:
fields13796–13801 hold Left+Down+Block;13802 releases;13803–13808 show native
backup0301 while the first Back press occurs; native stance0303 appears13809,
after the second Back press has begun. HK13814–13817 becomes ordinary kick0103.
A button request is not a recognized complete special command. Next activation
work should establish a released/ready native stance before the first Back and
inspect the actual combo queue, rather than repeat either sequence unchanged.

Source review of JOY.tchk4/is_stick_away rejects another tempting assumption:
native throw-away direction is based on is_he_right (relative position), not
the sprite flip flag. The current signed-coordinate relative-away calculation
is consistent with that helper; it was not replaced by a facing-based guess.
The native source contract is now regression-tested.

All current full-ROM/own-identity/no-fault audits pass; none of these runs reaches
later enemies, bosses, earned ending or credits. Full-port and release acceptance
remain false. No new release or ROM patch was generated for controller changes.

## Current-program extended Ring replay

Run603 repeats the currentF650 Sonya Ring/guard strategy with20 explicit
paid continues instead of5. It uses the same physical gameplay policy as583,
with native difficulty/AI/health left unchanged. The hidden below-normal
stock-MAME run is pending until terminal audit; do not count a live trace as
a completed campaign.

Campaign report identity checks now optionally cover all19 native actors,
including Kintaro/Kahn and the hidden trio, rather than naming them UNKNOWN.
The selectable name map still has14 entries. Both own IDs are now checked
against actual ft_kano/ft_sonya equates, not blindly appended. Two new tests
cover the full map and reject changed own equates;55 source/tooling tests
pass. The existing completed602 full-ROM/no-fault audit passes with this map.
These reporting changes do not prove any boss gameplay or alter the ROM.

Run603 now exits normally at79631 fields. Full current26-chip, identity,
no-marker and no-illegal-recovery auditing passes. Sonya again defeats
Baraka/Reptile/Jax, then beats Raiden2–0 on paid attempt7: native winning
results39514 and40958 have round counters1/0 then2/0, with Sonya14/28 HP.
The campaign advances to Kitana, then loses28 rounds without a player win
before the20-continue budget is exhausted. This is a currentF650 Raiden
match win, not a1CC or completed campaign. No game/AI/difficulty change.
