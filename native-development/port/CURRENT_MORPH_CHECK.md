# Historical morph fixtures and current refresh notes

## F650 current-program refresh: runs615/616

Normal and mirrored physical-input runs both complete9000 fields without
faults or missing markers. All26 actual current ROM chips are verified by
the strengthened qualifier. Actual own identity segments follow
6->17->6->18->6->18->6, each own form lasting524 observed fields. Both
Sonya LP/Block input orders activate her morph. Transformed Knife and Ring
activate and deal22 damage each (25 Knife action fields/15 Ring charge
fields). Automatic return and own pose families pass on both player sides.

This closes the current-ROM gate for these finite cases. It does not
certify all transformed moves, expiry interruptions, every intermediate
pixel/palette, boss/victim/edge cases or the complete visual style. The
qualifier's bespokeMorphArtComplete=false is an acceptance limitation;
it must not be read as proof that current intermediate artwork is absent.
No native game source or ROM changed during this refresh.

## Earlier fixtures

Runs `stock_wolf_game311` and `stock_wolf_game312` physically select Shang
Tsung and issue both own-character morph commands, on opposite player sides.
Both passed `qualify_morph.py` on the current split-enabled program link:

- True object IDs follow 6 -> 17 -> 6 -> 18 -> 6 -> 18 -> 6.
- Each own-character identity lasts 524 observed fields before native return.
- Both LP/Block input orders activate Sonya's morph.
- Transformed Kano Knife and Sonya Ring activate and deal 22 damage each.
- Own poses, no missing-root markers, and observation through frame 9000.
- Actual archive program bytes and all current graphics sockets are checked;
  stock MAME SHA, observer SHA and read-only guest-memory policy are checked.

Both per-run `qualification.json` files pin sources, map and linked program.
This does not prove all transformed moves, throws, interruptions, edges or
palette/visual acceptance. In particular `morph_source.py::MORPH_ROWS` still
uses temporary own stance frames instead of bespoke intermediate morph art;
that was an implementation gap at that historical link, not accepted morph art.

Current-source clarification: MORPH_ROWS now uses three authored intermediate
ks_mo_kano_pose0..2 / ks_mo_sonya_pose0..2 records, palette/entry-ground
helpers, the native cadence and final own stance. The old placeholder warning
above does not describe the current F650 source. MORPH_ART_TRACE_QUALIFICATION
records finite phase/ground/palette observations from519/520; those older
runtime observations are not automatically current-program acceptance.
The basic identity/return verifier still does not certify bespoke visual art.
Its ROM gate now checks all26 actual current chips, including sound/original
graphics; current replays are needed before claiming that gate passed.
No ROM code was changed by these tests. Program lane hashes remain
9AA9B8E18D637DE536E979B2875530CC1378883FD564C82037D5821834549660 and
6E35523D4B48645263CACA80411B41414E306FCA4CE94C814EE5D469F724CE9A.

## Transformed throw trials

Runs 313/314 used a controller distance threshold below normal collision
spacing, so no throw was commanded. They are not evidence of a game defect.
The observer was corrected to the original native 64-pixel throw range;
no game rule or ROM was changed.

Run 315 passes the extended morph qualifier: transformed Kano throws for
34 damage over 28 owner-action fields; transformed Sonya throws for 34 over
52. Both recover while still transformed, then return at the same 524-field
identity duration. All observed actor poses belong to the transformed
character (including authored throw poses), no missing markers/recovery,
and physical inputs only. Mirrored run 316 also passed the same qualifier:
34 damage and 28/52 owner-action fields, recovery before return, identical
524-field morph durations, correct identities/poses and observation to 9000.
This does not cover throws begun near morph expiry or interrupted releases.

## Throw overlapping morph expiry

Runs 317/318 add physical throw inputs just before native expiry, on opposite
player sides. Both passed the extended qualifier on unchanged ROM bytes.
Kano's throw runs fight fields 662–689 and returns to Shang at 702; Sonya's
runs 1542–1593 and returns at 1606. Each deals 34 damage and remains in the
correct own identity/pose family through release. Return is 13 fields after
the last owner throw-action field. Morph durations extend to 554/582 fields;
the later idle Sonya morph remains 524. Do not force an exact 524-field
duration when the native return check waits for an active move to finish.

`MKUTIL.ASM::back_to_shang_check` uses elapsed `040H*8` and transfers back
through the native reaction-exit path. No timer or move code was changed.
These bounded expiry tests do not cover opponent interruption, all throw
victims, all specials at expiry, or bespoke morph artwork acceptance.

## F650 late-throw refresh: runs617/618

Both player-side profiles exit normally at9000 fields, verify all26 actual
current ROM chips, preserve own identity/poses and have no missing markers
or Lua faults. Kano's near-expiry throw deals34 damage in28 owner-action
fields662–689, then returns at702. Sonya's deals34 in52 fields1542–1593,
returning1606. In each case the nominal expiry falls inside the active
throw; return waits until13 fields after its final owner-action field.
Actual transformed durations extend to554/582, while the later idle Sonya
morph remains524. This reproduces the defined historical expiry behavior
on the current F650 link. No native timer/throw/morph or ROM code changed.
Interruption, other victims and all other specials at expiry remain open.
