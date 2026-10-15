# Current human special commands, interruptions and KO/round transitions

Candidate remains diagnostic_v786_native_fighter_fade_exclusions.
EXE SHA256: 8DD83D7300BBC3872B1F829EA2A557CA968F5148464C3518AAB16B8559A76B55.
Payload SHA256: 7896C93822473376AD724BB5E747EDE88C198203786F3F9B928CD1D860BAE019.
This work changes test runners/verifiers and evidence only. Gameplay source,
EXE, payload, production CMD and release ZIP are unchanged. No material data
was deleted. The old launcher has not been promoted to this candidate.

## Fresh 52-case physical human matrix

audit_v820_positive_* and audit_v820_negative_* cold-start real two-human
matches against Sub-Zero, with real coin/start/selection and physical commands.
All eight implemented specials are exercised in both player slots: Kano knife,
cannonball, blade swipe and choke; Sonya ring, square-wave, bicycle and leg grab.
There are 18 positive and 34 defensive/miss cases, covering 46,178 paired
actor field records. No game-health, identity, position, process or RNG writes,
cheats, save-state setup or forced match state are used.

The independent verifier binds actual entry instructions to each true actor
and Main, checks the complete original native health-store ledger, contacts,
native ready continuations and clean recovered state. Ordinary walking, jumping
and punching afterward are required in each fixture. Cannonball block/recoil,
native collision geometry, fling stores and shared repel-state cleanup receive
additional checks. Standing square-wave is the expected anti-air non-contact
path; airborne contact is separate. Standing leg block takes native grab damage;
actual crouch-block rejects it. These are not waived hit/block expectations.

audit_v821_current_full_human_checked passes all 52 cases.
audit_v822_current_full_human_units passes nine actual baseline/corruption
methods for missing fields, proxy IDs, missing entries/damage, wrong cannonball
rebound/geometry and incorrect air/crouch-state substitution.
The three 400x254 screenshots per case are retained inventory, not a complete
independent art/pixel/audio fidelity proof.

## Fresh physical startup interruptions, clean retry, repeated KO and round two

audit_v823_interrupt_* contains ten cold two-human actual uppercut counters:
blade versus Sonya in both slots, bicycle and leg versus Kano and mirror Sonya
in both slots. The counter lands after native special entry, not before it.
Its actual 40 damage is written by the original MKII collision writer. The
interrupted attempt never reaches its strike/catch. Both actors then recover,
the cancelled blade attachment is removed by the original hit handoff, and a
second real input succeeds with exactly 26/22/35 damage respectively. Both
actual Main processes return to native ready and clean grounded idle states.

audit_v823_ko_* adds four repeated-special full KO-to-round-two paths:
Kano blade P1 versus Kano and P2 versus Kitana; Sonya bicycle P1 mirror and
P2 versus Sub-Zero. Seven blade hits or eight bicycles earn the KO, using the
original clipped health stores. The next round starts natively at full health,
and one more real command succeeds. No round or health reset is injected.
Full per-field blade body/trail phase and blood-object lifetimes are checked.
Bicycle loop phase comes from actual native animation cursor reads, with
48 consecutive paired updates, original physics/offsets, native corner-clamp
provenance, victim release and grounded cleanup.

audit_v824_current_interrupt_and_ko_checked passes ten interruption/retry and
four KO/round-two cases, with 21,164 paired actor field records.
audit_v825_current_interrupt_and_ko_units passes 30 actual baseline/corruption
methods covering cancel timing, owners, native entries/stores, recovery, stale
attachments/paired flags, blood cleanup, authored loop/cadence, real next-round
health and runtime errors. All 14 capture processes terminated normally.

These are three specific startup interruption families and four chosen KO
paths, not every move/interrupt timing, victim, CPU or arena.

## Scope and next work

audit_v826_current_human_checkpoint pins the new 66 runtime cases and 39
checker methods alongside the prior current UI/ground/shadow and finisher
checkpoints. The combined new paired actor field count is 67,342; it is not
67,342 consecutive frames from one match.

Whole-port acceptance remains open. Remaining work includes broader opponents,
arenas/states, CPU and interruption coverage; remaining move/finisher/cinematic
art/audio variants; complete genuine towers through Kintaro and Shao Kahn,
continues and endings; final whole-port regression and matching production
CMD/release ZIP. No launcher or release promotion is claimed.
