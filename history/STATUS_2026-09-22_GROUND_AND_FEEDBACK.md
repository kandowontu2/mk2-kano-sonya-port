# Kano/Sonya candidate: grounded stance and bicycle feedback

The current playable candidate is
`diagnostic_v48_ground_alignment_candidate/mkport_candidate.exe` (SHA-256
`71AA8E43755C6D85F1808A4402B3C8A7866D3931FAC15A42A8E075AFA651FB12`)
with `diagnostic_v46_bicycle_assets/roms/mk2ks/mk2ks.mdata` (SHA-256
`5CA9EE80B2737F7A295554C22BF3D4068C2552F90C744BA1D125B41251945D55`).
The matched user launcher is
`diagnostic_v48_ground_alignment_candidate/PLAY_CANDIDATE.cmd`. The installed
`mame-mkp/mkport.exe` remains the older v42 build.

## Ground contact

In stock MKII, Kitana's standing composite extends 138 game pixels below its
origin while its native floor-table entry is 133: the visible soles end five
pixels below the logical stage baseline. The eight imported Kano stance frames
have a 139-pixel bottom; Sonya's eight have a 140-pixel bottom. The previous
floor entries were 139/140, so both imported fighters' soles stopped on the
baseline, visibly above nearby stock feet. Their native floor entries are now
134/135, applying the same five-pixel contact distance as Kitana. This moves
their actual actors and all grounded states; sprite descriptors and stage art
are unchanged.

The saved old candidate fails the new contact observer with 528 errors.
`regression_v48_ground_verified_side{1,2}_{kano,sonya,sub_zero}_kitana` all
pass: each 40-second input-driven run checks both live identities, actor and
process floors, real composite bottoms and the stock contact reference over
stance, jump landing, crouch release and walking (1,591 checks per case).
`sub_zero` is a stock-only control; the parent harness's custom name/shadow
markers correctly have no samples there. Screen captures at
`regression_v48_ground_verified_side1_{kano,sonya}_kitana/snap/mk2ks/0020.png`
show the corrected foot line.

## Native bicycle feedback

The prior v47 gameplay patch is present in this build: the actual paired kick
routine invokes MKII's shared hard-hit sound command on the first paired field
and every seven fields, and creates/removes MKII's native camera task with the
original three-pixel, three-field cadence. The observer verifies the real DCS
command bytes and screen-memory displacements. A v46 negative control has
zero impacts and camera steps and fails the observer, as expected.

On v48, 16 contact cases (two player sides, Kano/Kitana victims, near/air/
block/far) pass. In near/air cases, each hit gives seven impact commands,
seven complete DCS deliveries and 16 camera steps. Eight nine-cycle KO/next-
round cases pass against Kano, Sonya, Kitana and Sub-Zero on both sides; each
has 63 impacts and 144 camera steps without a lingering task. Four real
uppercut interruption and retry cases pass on both sides.

## Acceptance scope

`diagnostic_v48_ground_alignment_candidate/verification.json` verifies the
exact executable, payload, source inputs, 62 direct runtime case records, one
CMD-driven real match, and 45 asset tests with the payload selected. Its
63-case runtime total is six ground cases, 12 core, four choke, 12 leg-grab,
16 bicycle contact, eight bicycle round, four bicycle interruption and one CMD
case. All terminal cases exited zero and the applicable native display,
identity, names, HUD shadows and stall/trap markers passed. The CMD also
passed `-verifyroms` with one good ROM set. This inventory is deliberately
scoped: it does not re-run every v47 victim/input mode on v48.

The existing release ZIPs and installed CMD were not promoted to v48. Full
completion still needs original fighter voices/announcements, complete
throw/victim artwork and semantics, finishers, AI participation, full ladder
progression/endings, boss and projectile interactions, bicycle corners and
broader cross-move acceptance. The shared unvoiced MKII hard-hit sound is
present; original Sonya voice samples have not been ported.
