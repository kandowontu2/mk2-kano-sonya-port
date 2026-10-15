# Native mirror outfits — separate v43 candidate

Latest working candidate and corner/lifecycle work:
`STATUS_2026-09-05_NATIVE_LEG_EDGES.md`. The 88-case results below remain evidence
for this preceding mirror executable, not the newer boundary-state build.

The full character-port goal remains unfinished. The installed CMD and portable release ZIP remain unchanged on v42. Working C++ now includes this mirror-palette change on top of the contact/pose candidate.

## Build identification

- Executable: `diagnostic_v43_mirror_candidate/mkport_mirror.exe`, SHA-256 `402DC8FE862E09C40B9F694A1D895C27A8EACCC4CF3A135EC4D96EF824FB8ECE`.
- Required payload is unchanged: `diagnostic_v43_jump_candidate/roms/mk2ks/mk2ks.mdata`, SHA-256 `31B89318C7D9C6A15706063A1A953D80E5F426AF6EC980009B5040626CAE206B`.
- Installed v42 executable was restored and its `41385589...D13A891` hash verified after compilation. Do not leave future builds at the normal executable path or mix candidate/installed payloads.

## Actual game fix

Both added fighters' native normal and alternate tables previously pointed to the same color record. Original MKII already set object flag `40h` correctly for one mirror, but there was no alternate record to select. The retained imported-metadata compatibility hook additionally forced primary colors on palette refresh.

`midtunit_m.cpp` now converts the original MK3 normal/alternate table entries (`FFA608B0` / `FFA60AF0`) independently. Kano's source descriptors are bytes `92BBC` / `92C3E`; Sonya's are `92CF2` / `92D74`. Existing primary records stay at `FDA00` / `FDB00`; alternate records occupy checked free bytes `F1500` / `F1600`, beyond the leg routine's exclusive `F1500` limit. Stock table entries remain untouched.

Both normal and debugger CPU execution paths now resolve imported palette requests through the native character table chosen by the actor's existing `40h` flag. They do not force a player number, swap identity, repaint the framebuffer or invent alternate colors. The two imported-frame compatibility hooks remain; this change corrects palette selection, not their removal.

## Independent runtime evidence

`mk2ks_mirror_palette_test.lua` uses ordinary selection, jumps and punches plus read-only observation. It requires distinct normal/alternate table records, unchanged own IDs, exactly one native alternate flag, and exact original donor colors for all 63 visible 6-bit body palette entries in actual palette RAM. It samples repeatedly across animation changes. Optional Sonya near-grab mode delegates controls and strict choreography to the existing leg harness.

Before the fix, `diagnostic_v43_mirror_palette_baseline_sonya` on contact executable `95759BDF...3EDEA` failed with 38 errors: shared records and 19 incorrect P2 colors at every sample, despite a correctly set alternate flag. The primary palette had zero mismatches. This establishes a game defect, not a guessed test expectation.

On the new executable, both `regression_v43_palette_mirrors_{kano,sonya}` and both `regression_v43_palette_leg_sonya_side{1,2}` pass 114 assertions with zero errors and 19 alternate-color samples each. The Sonya grabs also retain exactly 46 paired fields, zero trajectory errors, 35 damage, 48/47-field release, recovery and both fighters' own ring follow-ups. Mirror harness hash: `0B0E85B92C2AC0469F864AF4F470BB9A937C9876094CFE944727B08975332F4C`; base selector/leg harness: `A2334AAD16845D3BA80805E5FA0C0B5297FDB35C35E6B7BCBFB344304D4D209E`.

Reviewed images: `regression_v43_palette_mirrors_kano/snap/mk2ks/0017.png` shows red/blue outfits; the equivalent Sonya image shows green/blue. `regression_v43_palette_leg_sonya_side2/snap/mk2ks/0036.png` preserves different outfits during the paired inversion. These use the original color sets, not newly recolored art.

All **88 current-build emulator cases** completed and passed. Their exact expected case list, individual terminal results and logs were checked; `diagnostic_v43_mirror_candidate/verification.json` records this **partial candidate verification**, not full port acceptance:

- 12 `regression_v43_palette` core cases: both mirror outfits, both whole jumps, both ladder/lifecycle cases, both wins, both 20-action basics, grid and navigation.
- Two additional Sonya mirror-grab sides with strict choreography and palette-RAM checks.
- 20 cannonball, 20 square-wave and 16 knife/ring command cases on this executable, including their existing rejected-input/block/miss checks.
- 18 mixed-victim leg cases: Kano, Kitana and Sub-Zero on both grabber sides, in near/duck-block/air modes. These cover representative original and distinct stock-body/palette families, not all stock victims on this executable.

All 14 asset tests and `git diff --check` pass. The lifecycle Sonya ladder capture `regression_v43_palette_lifecycle_sonya/snap/mk2ks/0014.png` was reviewed: its own ladder icon appears without lingering selector portraits/poses. Candidate processes finished. Installed v42 executable/payload and release ZIP hashes remain unchanged. The preceding contact build's 258 passing runtime cases are documented separately in `STATUS_2026-09-05_LEG_CONTACTS.md` and are not silently counted on this new executable.

## Original corner reference for the next leg tests

`mk3_leggrab_reference.lua` now has `corner_left` / `corner_right` scenarios, preserving the previous scenarios' timing. Ordinary controls move both fighters toward the chosen edge for 500 fields, then approach and issue the grab at frame 4500. Original stock-MAME runs `diagnostic_v43_mk3_leg_corner_{left,right}` both complete: own animation enters at 4502, collision at 4512, 35 damage at release and grounded recovery. Reference script hash: `BA8EA905F3B4B3A90BEA57A0B2F70C3AE309BC0F8140A3696C4E4AEE412AFDED`.

Importantly, the original paired callback keeps the exact original offsets even beyond the normal movement boundary. At the left edge Sonya stays at X=121; the final paired victim pose is X=21 at frame 4555. Only after release is Kano clamped to X=58, with native -3/-6 knockdown velocity and gravity `8000h`. On the right Sonya stays at X=1096, final victim pose X=996, followed by normal leftward knockdown and recovery at X=927. Both end at original health 166/131. Do not weaken paired-offset assertions to clamp every pose just to make a corner test pass. These are original-game references, **not current port corner acceptance**.

## Remaining scope

Complete leg release/retrigger, corner, interrupt, KO and boss coverage before promotion; retain current-build coverage when making further changes. Mirror refresh across every later round/reselect/morph route still needs coverage; startup/actions/paired grabs are not proof of every palette lifecycle. Remaining specials/grabs, native audio/voices, finishers, AI and full ladder/ending/reselect/join behavior remain part of the original full goal.
