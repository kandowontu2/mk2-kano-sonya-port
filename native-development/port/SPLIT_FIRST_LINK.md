# Split fatality first link — candidate, not release

Stock MAME 0.289, windowless physical-input tests `stock_wolf_game297`
(Kano) and `stock_wolf_game298` (Sonya) both reached native completion
and ran through field 9000. Both used the same pinned ROM archive, without
game-memory writes or a custom driver. Kano's split halves were visually
confirmed in `snap/laosplit_05302.png`.

Program lane SHA256:

- `9AA9B8E18D637DE536E979B2875530CC1378883FD564C82037D5821834549660`
- `6E35523D4B48645263CACA80411B41414E306FCA4CE94C814EE5D469F724CE9A`

Archive SHA256:
`AB547A8703493C5E5784F177FC680263E8B4575AAEE0121C5617C1E0A19491FE`

The dispatch preserves the original table path for original characters.
IDs 17/18 use own together/peel scripts and distinct secondary-half scripts;
the original sleep/frame cadence, stance construction, and physics remain.
Generated source is included in `prepare_game_candidate.py` and the native
link/explicit assembler module lists. Eight pre-link tests passed.

Still required: full pose/timing trace qualification, both final visuals,
mirrored runs, original-character controls, and post-fatality cleanup review.
Mode 3 attract-state object pointers after the match must not be treated as
live fighter objects. MAME exit zero alone is not a gameplay acceptance gate.
Clean rebuild/patch qualification predating this link is historical.

## Four-case follow-up

`stock_wolf_game299` and `stock_wolf_game300` add mirrored Kano/Sonya.
`qualify_lao_split.py` now verifies all four pinned archives, all 34 compiled
image headers, both natural knockouts per run, all 17 own components per
actor/case, true IDs throughout the victim and component traces, native
completion, and observation through field 9000. Results are saved in
`LAO_SPLIT_RUNTIME_QUALIFICATION.json`.

Mirrored in-game captures `game299/snap/laosplit_05302.png` and
`game300/snap/laosplit_05291.png` (under the full `stock_wolf_` run names)
were visually inspected: both own split bodies render, rather than a donor
character. These captures are during separation, not proof of final floor
alignment or full costume continuity. Original-roster controls, exact timing,
final visual acceptance and cleanup acceptance remain open.

## Removal trace and render caveat

Runs 303/304 add a read-only per-field object-list count, with no ROM change.
`qualify_split_cleanup.py` verifies every field 3001–9000: Kano's split
objects leave the list at 5736, Sonya's at 5725, and neither returns through
9000. This proves native object-list removal, not framebuffer clearing.
The immediate removal captures were inspected and still show the previous
floor bodies. Therefore these captures do **not** prove visible clearing;
later-render captures and transition review are still required. Do not infer
a persistent-object bug or visual acceptance from this one-field observation.

## Delayed-render follow-up

Runs 305/306 record captures 3/12/30/60 fields after list removal, with the
same ROM archive. The first three delayed images are byte-identical to the
immediate removal image, disproving the proposed one-frame capture-delay
explanation. At +60 Sonya's capture shows the native side-panel screen wipe
over the final fight image. This is compatible with retained framebuffer
content during the transition; it is not proof of persistent live objects.
Compare an original-character transition and inspect the completed wipe before
accepting visible cleanup or changing game code. Object-list removal remains
verified independently. The qualification script now pins the actual ROM
archive lanes/sockets, stock emulator, controller hash and all delayed captures.

## Original transition comparison

Runs 307 (actual Liu Kang, ID 1) and 308 (Sonya, ID 18) extend capture
to +120/+240 after object-list removal. The +60 Liu capture was inspected:
the original split body likewise remains in the old fight framebuffer under
the native side-panel wipe. Both +240 captures were inspected and show the
fully closed MKII continue screen, without split bodies or fight content.
Thus the retained image during the wipe is not a demonstrated own-character
cleanup regression. No cleanup code change is warranted by this evidence.
This bounded Sonya/original comparison does not cover every transition or
replace final ground/costume alignment acceptance. The latest cleanup JSON
pins these two extended cases; previous runs and raw captures remain intact.
