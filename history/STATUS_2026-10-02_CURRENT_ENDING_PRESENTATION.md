# Actual current ending presentation — assisted setup, not a tower clear

Candidate remains `diagnostic_v680_native_pit_initial_cache`. The playable ROM,
executable, gameplay source, production CMD and release ZIP are unchanged.

The native boss-recovery checkpoint v712 freezes six stock/new-character
comparisons and 25 regressions. Native Kintaro stomp recovery is preserved.
Nine v711/v713/v714 input-strategy scouts still lost to Kintaro. Their results
are not promoted to boss clears or treated as proof of a port-specific defect.

## What the ending tests actually establish

Four current-candidate runs show both characters in both physical player slots
entering their actual native endings, fetching both own picture pages and all
six native text-table segments, and returning to attract mode. Genuine selection
and native actor construction use IDs 17/18, with Shao Kahn ID13. The ending
starts after actual original combat HP stores and native actor retirement.

These are explicitly ASSISTED diagnostics, not complete campaigns: one stage16
index fixture is applied before construction; CPU health is set to1 initially
in each native round. P1 Kano v716 needed no own-health assistance. V717 P2 Kano
and P1 Sonya restored own combat health22 times; P2 Sonya11 times. No actor,
identity, action, position, schedule, winner or ending state is written. All
assistance stops before the native ending/cinematic interval.

The original-derived photograph records match all421,840 visible photographed
pixels across16 early/late page captures. The6416 photo-edge pixels overpainted
by native framing match an actual stock Liu Kang ending on the same candidate.
The checker does not pretend those overpainted pixels show the hidden photo.
Each character's full rendered pages are byte-identical between P1 and P2,
including early/late captures. Both story pages were visually checked against
the five current native story strings: legible, inside the original frame and
with the intended names/story. This is not an independent text-pixel oracle or
certification of every transition/background/cinematic field.

Each run also records nonempty48kHz stereo audio. That does NOT establish exact
native sound timing, mix, imported voice fidelity or full character audio.

Evidence: v716 P1 Kano, three v717 cases, v718 original Liu frame control;
`tools/verify_current_ending_presentation_v680_v1.py` and24 in-memory baseline/
corruption tests. V715 assisted only the first round, and v716 P2 Sonya lost the
second round; both failures are retained, not recast as successful endings.

## Remaining full-goal work

- Genuine full towers/boss clears for both characters/slots, with losses,
  continues/reselection and whole ending/return-to-play paths without fixtures.
- Remaining finisher/cinematic coverage, imported artwork and exact character
  audio fidelity; broader human/CPU specials, interrupts/KO and secret stages.
- Whole-scope final regression and matching production CMD/release ZIP.

This narrows ending-presentation uncertainty; it does not redefine the full
natural-character goal. Full-port and unassisted-clear acceptance remain false.
No material data was deleted.
