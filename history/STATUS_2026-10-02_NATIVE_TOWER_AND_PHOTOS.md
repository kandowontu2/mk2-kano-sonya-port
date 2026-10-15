# Current native campaign/photo checkpoint — not a finished release

Candidate remains `diagnostic_v680_native_pit_initial_cache`, launched with
`PLAY_LATEST_TEST_BUILD.cmd`. No gameplay source, executable, payload, production
launcher or release ZIP changed in this continuation. No material data was deleted.

The six additional both-slot fatality cases and 25 tests are now frozen at
`audit_v704_finish_slots_checked_inputs`. All 14,621 prior v692 inputs were
rechecked unchanged; the combined bounded checkpoint pins 20,507 inputs. Its
fatalityAcceptance and fullPortAcceptance flags remain false.

## Current photo records verified

A freshly decoded original-ROM oracle supplies all four ending pages and both
native BATTLE/ladder photographs. The running current candidate matches all
107,064 ending-photo pixels and 43,608 BATTLE-photo pixels, their complete
256-entry palettes, native headers/codebooks, and retained stock table entries.
216,371 ending checks and 88,332 BATTLE checks pass. Sixteen tests of the actual
production C++ photo decoder pass against an independent original-ROM decoder.

Evidence: `audit_v702_original_photo_oracle`, `audit_v702_current_ending_records`,
`audit_v702_current_battle_records`. This proves the actual guest photo records,
NOT their whole ending slideshow, every rendered transition, story text, audio,
or a cleared tower. The older v701 BATTLE attempt lacked oracle files and is
retained as a failed test-input attempt, not a game-art failure.

## Genuine current campaign progress, explicitly not a clear

`audit_v706_native_tower_kano_p1` is a fresh, cold, input-only run at unchanged
native difficulty. It selects true Kano, traverses stages 0-12 and 14, and
reaches Kintaro at stage 15. Stage 13 is the original endurance sentinel,
not a manually skipped opponent. The independent v2 verifier proves actual
schedule/actor/Main ownership, 31 own native round wins, 771 original combat
damage stores, 25 losses with coin/start continue inputs and true-ID reselection,
and advancement only after two wins in the successful attempt. Sixteen in-memory
baseline/corruption tests pass. The checker does not count original health-bar
teardown writes as combat damage and does not accumulate wins across failed
matches to invent an advance.

This run does not defeat Kintaro, reach Shao Kahn, or enter/complete an ending.
`unassisted_clear_proven` and `fullPortAcceptance` remain false. The bot's repeated
stomp losses are not proof that the port is defective; native victim recovery
needs a stock-character comparison before making any gameplay correction.

Earlier v697-v705 scouts are preserved, not upgraded to accepted tower clears.
The initial v25 logger inherited a Lua `table` shadowing error; its feedback bot
could remain guarding indefinitely. Later jump/zoning scouts inform strategy.
The v29 continue driver could enter its route search before the native roster
became valid, causing observer errors; v30 waits for a real roster ID <=18.
Sonya's attempted input-only campaigns have not cleared their opening match.
The older full-tower harness uses explicitly labeled health assistance and is
not evidence of an unassisted clear on this candidate.

## Still required for the full natural-character goal

- Genuine complete towers and bosses for both characters/slots, native loss/
  continue/reselection and actual ending/story/audio/return-to-play presentation.
- Full finisher/cinematic and character audio/art fidelity beyond the bounded
  tested individual fatalities and Pit paths; more victim/alternate coverage.
- Wider human/CPU special choreography, interruptions/KO, secret-stage and
  camera/grounding paths, followed by whole-scope regression.
- Matching final production CMD and release ZIP after those gates pass.
