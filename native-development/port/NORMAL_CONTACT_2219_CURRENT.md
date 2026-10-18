# First normal-contact observations

CURRENT: aggregate136 finite contact cases now pass,17 actual action types
x2 characters x2 player sides x hit/block. See NORMAL_CONTACT_ACCEPTANCE_2219.json.
This covers all14 ordinary attack families plus knee,elbow,throw, at the
explicit tested spacings/guards. Sonya diagonal punch requires a larger
220-gap setup in this fixture; the180 overshoot remains failed contact
evidence. Full range/victim/every-frame audiovisual acceptance is separate.
The historical correction below remains applicable to the rejected100-gap
blocked punch proofs; those are excluded from the aggregate.

CORRECTION: the two100-gap blocked standing-punch pilots with zero damage
were whiffs, NOT confirmed blocks/no-chip behavior. Their earlier proof
claims are invalidated in NORMAL_CONTACT_INVALIDATIONS_2219.json; raw
recordings remain untouched. Native MKSTK packed damage is0b03h HP and0802h
LP (11/3 and8/2 hit/chip). Current qualifier requires those native chip
values. At90 gap Kano P1 HP now confirms11 hit/3 block. The resumed40-cell
matrix uses90 for standing punches and preserves100-edge evidence separately.
Historical zero-chip statements below are superseded by this correction.

Ten additional Kano P1 basic-contact pilots now qualify, each terminal and
current26 checked with frozen read-only observer, native action, exact damage
and recovery/continued guard. These are not yet Sonya/opposite-side cells:

| Request / gap | Actual action | Hit / block damage |
| --- | --- | --- |
| HP /70 |114h elbow|24 /6|
| HP /100 |101h standing HP|11 /0|
| LP /70 |507h ordinary throw; victim226h|34 /34|
| LP /100 |102h standing LP|8 /0|
| LK /100 |104h low kick|26 /6|

The close LP pilots are throw observations, not low-punch coverage, and
standing Block does not stop that throw. Standing punch victims keep303h
in these traces despite actual HP loss; do not require503h for every normal
hit. Blocking punch cases have zero chip and continuous700h guard. These
distinctions are explicit in qualify_normal_contact.py; results are pinned
in each run's NORMAL_CONTACT_QUALIFICATION.json. No game rules were edited.

The completed16-cell matrix now extends these knee/high-kick checks to both
characters and both player sides, at70/100 gaps and with/without standing
Block. All16 pass exact native action/damage and recovery/guard gates;
coordinator exit0. See NORMAL_CONTACT_MATRIX_2219.json. This does not extend
the result to other normal attacks or arbitrary spacing/victims.

Four fresh stock-MAME runs completed exit0/timedOutfalse with actual current
26-chip comparisons. The physical controller walks Kano P1 toward Sonya P2,
then requests HK once; no guest positions, health or results are written.
The blocking profiles hold Sonya's Block throughout. Each request window
has120 observed fields, followed by120 neutral attacker fields.

| Run suffix (`stock_wolf_2219_normal_hk_`) | Initial gap | Actual attacker action | Victim damage |
| --- | --- | --- | --- |
| hit_pilot |70|10fh native knee|20|
| block_pilot |70|10fh native knee|6|
| hit_gap100 |100|103h native high kick|32|
| block_gap100 |100|103h native high kick|8|

Unblocked victims show503h reaction and both actors end303h stance. Blocked
victims remain700h because their controller continues holding Block; the
attacker returns303h. Do not call the latter a two-stance recovery proof.
Close-range HK is correctly recorded as knee, not high-kick coverage.
These observations are finite Kano-P1/Sonya-P2 evidence, not a full contact
matrix, all-frame visual check or all normal-move acceptance. Runtime CSV,
frozen controller, receipt and screenshots remain in each immutable run.
