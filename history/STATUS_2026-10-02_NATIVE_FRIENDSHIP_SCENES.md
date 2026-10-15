# Native Friendship scene integration — not release acceptance

Experimental candidate: diagnostic_v768_native_friendship_layer.
EXE SHA256: 3D115438A30B43C97F170CCC497B343511318430178765BB2DEB44EC2DFE8430.
Payload SHA256: 7896C93822473376AD724BB5E747EDE88C198203786F3F9B928CD1D860BAE019.
Latest-test CMD remains on verified Babality candidate v737. Production CMD
and release ZIP are unchanged. No data was deleted during this work.

## Implemented

Own real-ID Friendship command/action rows, without proxy characters:
Kano LK,Block,Block,HK; Sonya B,F,B,D+Block. MK3 Run is mapped to Block because
MKII has no Run. The actual original MKII finish/no-HP-or-LP gate, scheduler,
common setup, announcement and screen cleanup remain native. Kano uses the
original button-history matcher; Sonya/stock fighters keep the original
direction/facing matcher. Rejected commands retain Kano's fatality fallback
and Sonya's leg-grab fallback. Stock command/action rows are preserved.

All 18 Kano body groups, seven separate bubble groups and eleven Sonya groups
were extracted from original MK3 and independently matched against original
native renders: 92,513 visible source pixels. Original scene captures explicitly
use opponent-health-only assistance and are not unassisted gameplay acceptance.
Native reference pose changes precede their visible output; frame-by-frame
capture resolved that delay. Sonya was physically moved away from a foreground
candle that hid four hand pixels; no position/identity/state writes were used.

The payload artwork-only import changes exactly 161 bytes across typed group
component pointers, graphic sources and optional palette pointers. All original
descriptor geometry/DMA commands and the whole second-MiB gameplay data remain
unchanged. No MK3 action code is executed. The new body and bubble animation
run through MKII group coroutines. The bubble is separately allocated, palette-
owned and registered with original MK3 foreground priority 51h. Earlier v761
showed wrong bubble colors; v764 corrected palette loading but still hid four
small-bubble pixels behind Kano's face. Both attempts are retained, not accepted.
v768 corrects sorting priority before native registration without moving art.

## Bounded verification

Eight cold physical-input-only v768 cases: each character in both player slots,
wrong-command cases for both P1 performers, and punch-used winning-round cases
for both P2 performers. Each earns two actual native knockouts / 322 damage,
with no cheats, health assistance or guest RAM writes. Own body actor/owner,
roster and actual ID remain intact. Intro body order and five-field cadence,
Sonya's fourteen-pose three-field chicken loop, complete bubble pose order and
timing, unchanged actor origin/native floor anchor, common finish handoff and
next-screen retirement are independently checked. Both rejection categories
remain outside the Friendship action and cleanly leave the finish window.
All seven bubble images match original source pixels in both player slots,
including the formerly occluded first frame. Its separate palette matches
every original pen after the native deferred copy. ROM verification passes.

Checkpoint audit_v769_native_friendship_dispatch_checked/verification.json
checks 214 inputs and eight terminal cases, including the original-art oracle
and reproducible exact payload import. tools/test_native_friendship_dispatch_v769.py
passes 22 baseline/corruption test methods. Guest-ROM differences from v737
are confined to reserved Friendship storage and the five explicit bindings;
stock rows, own commands, matchers and fallbacks are independently checked.

## Still required before promotion / completion

Friendship-specific original audio is NOT integrated. Kano's FFAA65A0 callback
uses the two-entry sound table (identical entries 006E1F21); Sonya's FFAA6AA0
uses four chicken variants 00A51010/00AA1017/00AF1014/00961012. Read-only
disassembly identified these next inputs; they still require original DCS
capture, isolated playback and timing verification. Do not substitute unrelated
MKII sounds or claim audio acceptance from silent (-sound none) scene tests.

Full body display/palette/cinematic verification under MKII's native finisher
dimming, stock Friendship controls, broader button/timing/distance/arena/CPU
coverage, and current-candidate Babality/fatality/stage-special regression remain.
Historical floor-shadow/UI/combat/ending evidence is not wholesale recertified
by these bounded Friendship runs. Full unassisted towers/boss clears, whole-
scope regression, final production CMD and matching release ZIP also remain.
Full port and full finisher acceptance are false; the complete original goal
stays active.

Preserved pre-edit sources: audit_v760_pre_friendship_implementation_inputs
(v737 full tracked inputs), audit_v763_pre_friendship_palette_fix (v761 changed
sources), audit_v767_pre_friendship_layer_fix (v764 driver). Historical build
hashes must resolve through those snapshots, not current changed live sources.
