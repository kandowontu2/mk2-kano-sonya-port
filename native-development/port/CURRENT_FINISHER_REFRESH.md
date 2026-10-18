# Current-link finisher regression refresh

Eye Laser runs418 (player1) and419 (player2) use the current native program
and16-clip sound bank. Each runs9,000 fields with ordinary physical controls.
The qualifier now checks actual bytes of all26 chips: current compiled program,
added graphics, native sound and unchanged original MKII graphics. It also
checks controller/MAME pins, no guest writes, no Lua faults and matchup identity.

418 passes: two natural knockouts,176-field native action,164 beam fields,
96 victim-reaction fields, exact body/beam event sequence, own Sonya victim
pose, beam object/process retirement and native completion.419 is recorded
in its own qualification receipt after the mirrored validator succeeds.

An initial overbroad identity assertion rejected418 because Kano legitimately
entered a later CPU match against Baraka after the two-player defeat. The
corrected assertion requires fixed identities throughout the tested matchup,
not throughout every later match in the9,000-field observation. No ROM fix
or waived in-match identity change was involved.

These finite checks do not certify exact audio, every victim/edge/AI case,
fresh-match cleanup, the entire moveset or final release readiness.

419 mirrored Eye Laser qualification passed with the same event/lifetime
checks as418. Negative420/421 also pass on both player sides: holding Block
at finalHK rejects the fatality despite two natural knockouts. Each negative
trace covers9,000 fields and matches all26 current ROM chips, with no observed
missing-animation, illegal-opcode recovery or Lua fault. These are finite
invalid-command checks, not exhaustive input-window or eligibility coverage.

Sonya Death Orb422 (player1, Kano victim) passes on the same current link.
The strengthened qualifier checks all26 actual ROM chips. Two physical-input
round wins lead to the176-field finisher:39 travel fields at2 pixels/field,
21 growth fields,39 enclosure fields,12 burst fields,32 salute fields. All14
own Orb poses, native victim stumble, completion and object/process retirement
are observed. Mirrored/current-link negative Orb coverage remains to refresh;
exact audio and fresh-match cleanup are still unqualified by this test.

Orb423 now passes the mirrored player2 check with the same14-pose sequence,
native completion and object/process retirement. Negative424/425 pass on
both sides: breaking continuous Block hold rejects Orb, the performer stays
grounded, and the168-field finish window is observed without Orb completion.
All three traces cover9,000 fields with no detected missing marker, recovery
or Lua fault.422 was requalified with the strengthened matchup identity gate;
all four receipts explicitly certify actual26-chip byte comparisons. These
results supersede the mirrored/negative refresh note above, but do not close
the remaining audio/edge/victim/fresh-match or campaign gates.

Extraction426/427 and flame-kiss428/429 pass on both player sides,9,000 fields
each. Each trace has two physical-input round wins before the231-field native
fatality. Extraction verifies9 body poses,6 skeleton phases,6 own Sonya victim
phases and spawn age83. Flame kiss verifies all fixed-point projectile steps,
60 projectile fields, deletion before burn,116 burn fields/15 burn poses,
preserved Kano victim standing origin and native completion. Both qualifiers
now compare all26 actual chips through verify_finisher_roms.py and reject
explicit recovery-fault receipts. The helper is hash-pinned in qualifications.

All four main own fatalities now have current-link positive evidence on both
sides against the other added character. This does NOT establish all original
victims, screen edges, AI cases, sound mixes, fresh-match teardown, stage
finishers, Friendships/Babalities, complete campaigns or final visual approval.

New post-fatality physical rejoin probe:430 failed the600-consecutive-field
criterion because the aggressive controller caused another round transition.
No game fault was inferred or waived.431 uses bounded sparse uppercuts after
rejoining via normal coins/start/selection; it passes600 consecutive combat
fields after Eye Laser, full starting health, correct own IDs, subsequent
damage, zero winner/death state and no tracked finisher child. Current26-chip
bytes match. Selection occurs5782, fresh combat6333. This qualifies finite
state reset only, not all object/process/palette/audio-tail retirement.

Post-fatality rejoin matrix now passes for all four fatalities on both sides:
Eye Laser431/435, Orb432/436, extraction433/437, flame kiss434/438. Each uses
physical coin/start/selection, confirms the prior native fatality active
duration/completion, then600 consecutive combat fields with full starting
health, correct own IDs, subsequent damage, zero winner/death state and no
tracked finisher child. All26 ROM bytes are compared. Orb's performer tag in
the new verifier was corrected from the victim's545 to544 before acceptance;
the original motion verifier and actual native actions were unchanged.
The verifier SHA is pinned in each receipt. Comprehensive process/object-list,
palette and audible-tail cleanup still is not established by these checks.

Stronger active-object check439 after Eye Laser passes: the read-only observer
records18 actual child-effect shapes during the fatality, then traverses the
complete bounded active-object list for each of600 fresh combat fields.
None of those observed shapes remains in the list. Traversal validates every
pointer, rejects cycles/oversized lists and requires at least the two fighter
objects; a cleared child pointer alone cannot satisfy this check. Addresses
are deliberately not treated as persistent identities because the object pool
can legitimately reuse them. Process-list, palette and audible-tail cleanup
remain open, as does this stronger object check for the other fatalities.

Player1 object-list extension440/441/442 passes for Orb/extraction/flame kiss:
14/6/8 actual child-effect shapes captured respectively; all absent during
600 complete bounded active-list traversals in each next fight. Existing
identity/health/damage/state-reset and26-chip checks also pass. This closes
that finite player1 observed-shape test, not arbitrary effect/palette leakage.

Process audit caution:439's saved child-object address is absent in all600
fresh fields, while its saved process address is active in all600. A recycled
pool slot is not a durable process identity. This observation is not proof of
a surviving effect process or proof of retirement. A future process verifier
must inspect live role/context and/or lifetime transitions; do not assert
address absence across new allocations or silently report process cleanup.

Completion-time process qualification now passes for439 Eye Laser and440 Orb:
each tracked object/process was observed active during the fatality and both
were absent at native completion (frames5335/5343 respectively), well before
selection5782 and new combat6333.439's process address later reappears at6333,
so the trace proves retirement before later allocation reuse, not a lingering
beam process. The rejoin verifier now requires this exact completion check
for Laser/Orb and pins its evidence CSVs/receipt/controller/helper. Broader
process populations, extraction/kiss processes, palettes and audio tails still
remain unqualified; the report retains its comprehensive-cleanup=false flag.

Native source review: KSFATAL keeps the attached skeleton through its victory
display; KSKISS uses a single object, delete_slave before the victim burn,
and no dedicated dummy process. A blanket kill-at-completion rule would not
correctly describe both designs. Extraction443 passes the existing rejoin and
active-object checks with added read-only palette-slot observations. Fresh
slots are0404/0505 versus initial0202/0303. MKUTIL.swpal/getfpal explicitly
allocates double-byte palette slot numbers, so differing slots do not prove
different colors or broken restoration. The new CSV retains those raw values;
palette-content restoration remains unqualified until the slots are resolved
through palette allocation data. No ROM fix was inferred from slot movement.

Extraction444 resolves that allocator ambiguity using the linked palram symbol
and native64-bit record layout (PALL/MAINEQU): slot low byte selects palid,
the palette source pointer. New slots0404/0505 resolve to FFC3FFB0/FFC572B0,
exactly the initial0202/0303 source pointers. Both sources match through the
first60 fresh combat fields. Existing26-chip/600-field/state/object checks
pass. The qualifier now reports source restoration separately from hardware
RGB acceptance; matching source pointers do not verify palette-RAM contents,
full RGB transfer correctness, every scene or audible cleanup.

Flame-kiss445 adds actual Wolf palette RAM comparisons: existing hardware map
01880000, xRGB555,256 colors per slot; native PALL transfers the count-prefixed
ROM palette's words into that slot. For each of600 fresh combat fields the
observer compares every used color, masking only the unused high bit. Both
fighters use65 colors; all78,000 comparisons match. Initial palette source
restoration also passes, along with26-chip/gameplay/object cleanup gates.
This qualifies this finite post-kiss palette transfer, not arbitrary palette
reference leaks, every finisher/side or visual art acceptance. No custom
emulator driver or guest memory writes were used; the memory-map source was
read for hardware layout only, and execution remains pinned stock MAME0.289.

Full finite post-fatality palette/object matrix445-452 passes: kiss445/452,
laser446/449, Orb447/450, extraction448/451 (player1/player2). Each verifies
all26 actual ROM chips,600 uninterrupted fresh combat fields, original palette
sources in the first60, and all65 used colors for both fighters throughout
600 fields. Combined624,000 hardware xRGB555 comparisons have zero mismatches.
All observed old child-effect shapes are absent from complete active-object
traversals; identities, health, damage, death/winner reset also pass. Laser/Orb
tracked object/process absence at completion passes both sides. This closes
this explicit four-fatality/two-side finite matrix, not all palettes/processes,
audible tails, other victims/edges/finishers, campaigns/bosses/endings or release.

Current-link player1 Friendship/Babality refresh453-456 passes. Kano453 has
193-field Friendship, own body/bubble timing and native retirement; Sonya454
has176-field Friendship with all intro/loop poses and native completion.
Kano455 and Sonya456 each have192-field Babality and correct other-added-
character baby art. All start from two physical-input round wins and run
9,000 fields. Their strengthened qualifiers compare all26 actual ROM chips,
pin the common helper and retain audio/edge/cleanup/full-port flags as false.
These positives do not refresh mirrored or punch-ineligible cases by inference.

Mirrored positive457-460 passes: both Friendships and both Babalities activate
and complete on player2 with native193/176/192/192-field timing, expected own
art/poses, two physical round wins and full26-chip verification. Punch-win
negatives461-464 pass on player1: each fixture physically wins two rounds,
then the requested Friendship/Babality has zero active fields and no native
completion; native punch eligibility rejects it. No guest-state writes or
driver patches. Player2 punch-negatives, audio and post-scene cleanup are not
qualified by these runs; no broad all-victim or full-port acceptance implied.

Player2 punch-win negatives465-468 also pass for both Friendships and both
Babalities, completing this finite positive/negative two-side eligibility
matrix453-468. Each negative reaches two physical knockouts, verifies all26
current chips, and has zero finisher action fields/no completion. Correct
native rejection is the expected passing outcome, not successful activation.
No new ROM builds or custom driver changes. Audio, general edge/victim/AI and
post-Friendship/Babality scene cleanup remain separate unclosed gates.

Physical player1 rejoins469-472 pass after Kano/Sonya Friendship and Babality.
The generic verifier checks the correct7/5 native death tags and193/176/192/
192 action durations, then normal reselection and600 consecutive fresh combat
fields. All26 chips, own identities, initial health, subsequent damage, zero
death/winner state, first60 original palette sources and78,000 hardware color
comparisons per case pass. Kano Friendship's seven observed bubble shapes
are absent from the complete fresh active-object list. Sonya Friendship and
Babalities have no tracked p_slave shapes: their object absence remains false,
not vacuously accepted. Baby-image and dance-process retirement, audio tails
and mirrored rejoin remain open. No ROM code changed for these tests.

Mirrored post-Friendship/Babality473-476 passes: each has600 consecutive fresh
combat fields, normal identities/health/damage/state, all26 actual chips and
78,000 matching hardware color comparisons. Kano bubble shape absence also
passes. New baby-image tracking observes the actual image before rejoin and
requires zero matching images in complete active-object traversal afterward;
both player2 Babalities475/476 pass all600 frames. Earlier player1 baby runs
did not capture this image-specific evidence and must not inherit that claim.
Sonya dance process/audible tails remain unqualified. All comprehensive cleanup
and releaseReady flags stay false; these tests do not establish full campaigns.

Current native video483: bounded actual screen:pixels capture of176 Eye Laser
fields plus native DCS WAV, encoded as4:3 MP4 (183,903 bytes), SHA256
3A8EB8E718899C7B2417B59EEC7C7BAE1146F60C46B1F2FC6E72376BD5FA3055.
All176 video frames survive and full AV decode passes. Current26 chips and
the ordinary physical Eye Laser validator pass. A middle-frame visual check
shows correct colors, own Kano/Sonya, horizontal beam and victim blood pose;
this is not complete visual/audio-sync approval. First encoding failed aspect
validation due setsar's default denominator bound; corrected max1000 produces
exact4:3. Failed clip SHA6586FA1B4D81A549BBE6242584F3B0569105BFF809ADA5E60FE33776F93A9C9B
was verified then removed; successful source raw/WAV intermediates were hash-
pinned and removed after roundtrip/decode checks. No multi-gigabyte AVI kept.
The clip is a finisher demonstration, not all moves or a campaign video.

Remaining native fatality clips484-486 now encode/decode and motion-qualify:
Orb176, extraction231, flame kiss231 frames. Their FINISHER_VIDEO.json receipts
pin MP4/raw/WAV/observer hashes and all26 current ROM bytes; no synthetic frames
or old custom-driver execution is used. Each is actual4:3 native frames plus
native DCS audio, with full AV decode and exact recorded-frame preservation.
Decoded frame100 of each was visually inspected for expected scene/color data;
the Orb reaches the viewport edge, so this is not an all-edge layout approval.
All four clips total1,085,213 bytes; raw/WAV files are removed per completed
clip to avoid accumulated large temporary captures. NATIVE_VIDEO_INDEX.md
links them. Whole-movelist/full-campaign videos, exact sync and final whole-
clip audiovisual review are not established by these bounded demonstrations.

Native Friendship/Babality clips487-490 also pass motion/eligibility-positive
validators and bounded AV encoding:193/176/192/192 actual frames respectively.
All26 actual ROM chips match current build; frame preservation, exact4:3 and
full AV decode pass. Source raw/WAV files were hashed then removed per clip.
Eight retained native finisher clips now total1,847,666 bytes and are linked
in NATIVE_VIDEO_INDEX.md. Sonya Friendship capture covers its native176-field
intro/cycle, not the indefinitely repeated post-completion dance or complete
cluck tails. These clips retain visualReviewPassed=false and exact audio-sync
approval=false; full movelist and earned complete-campaign videos remain open.

Special-move capture observer added as an appended read-only Lua chunk, without
changing physical controller inputs. It starts on a specified native action,
captures at most400 fields and ends after eight stance fields.491 failed before
gameplay because stock0.289 has no emu.register_stop API; no acceptance claimed.
The unnecessary hook was removed. Fresh492 Kano Ball passes:13 activations,
deliberately short first charge rejected, first valid hit and return to stance.
Its first move/recovery clip preserves69 frames, exact4:3, native audio and full
AV decode, with all26 actual ROM-chip comparison. MP4 is265,771 bytes; raw/WAV
were hashed/deleted. Other seven specials are not covered by that Ball clip.

Special493-495 pass native Blade/Choke/Leg motion validators plus all26-chip,
frame-preservation and AV checks. Blade493 exercises17 activations,26 hit
damage/3 block damage and trail retirement. Choke494 has eight69-field holds
with four8-damage pulses, rejection and recovery checks. Leg495 has seven
46-field holds/35 release damage with own/victim poses and grip trajectory.
Their first captured46/48/78-field attempts are intentional whiffs/misses,
not successful hit demonstrations. In495's clip Kano HP stays161 and no Leg
hold tag is observed. All three are explicitly labeled; do not substitute
these clips for hit footage. Raw/WAV files were removed after encoding.
Successful Blade/Choke/Leg footage and remaining specials still need recording.

Successful episode captures496-498 use read-only not-before recording windows
derived from493-495 traces, without altering the physical input policy. Whole
move validators and26-chip/AV/frame checks pass. New captured-interval verifier
checks actual clip hash and exact CSV frames: Blade46 fields/26 damage/both
stance; Choke100 fields with69-field hold/four8-damage pulses; Leg75 fields
with46-field hold/35 release damage. The latter two clips end with performer
stance but victim still in throw recovery, explicitly flagged incomplete-
recovery footage. Do not equate a whole-run recovery result with recovery
shown in the clip. Raw/WAV files removed after encoding; index labels scope.

Complete paired recovery499/500 now passes. The grab capture observer waits
for both processes to reach native stance for eight fields (still capped400).
Choke135 fields:69-field hold/four8-damage pulses, both return to stance.
Leg185 fields:46-field hold/35 release damage, both return to stance. Exact
captured interval and clip-hash qualifiers pass, alongside whole-run native
motion and actual26-chip/AV/frame-count checks. No gameplay/controller-input
changes; only observation duration changed. Index now links these full clips
instead of the earlier incomplete-recovery recordings. Raw/WAV files removed.

Remaining special captures501-504 pass native move validators and actual26-
chip/AV/frame-count checks. Captured-interval hit proof verifies Bicycle95
fields/22 damage, Square53 fields/27 damage, Knife120 fields/22 damage and
Ring120 fields/22 damage. Projectile minimum120-field observation changes
recording only, not inputs. All performers return to stance; Ring victim also
reaches stance. Knife victim remains in recovery; Bicycle/Square victims have
action0 rather than the verifier's strict303 stance, so full victim-recovery
video flags remain false. Source raw/WAV files removed after verified encoding.
Index now covers all eight specials plus eight finisher sequences, still not
stage finishers, Shang morphs, full normal-move showcase, campaigns or release.

Dead Pool505/506 whole-run native qualifications pass, but their generic
nonzero-f_death capture incorrectly selects a later64-field Tomb sequence.
Dead Pool f_death stays0 until65535. The exact-interval stage verifier catches
the wrong arena and intended own-victim mismatch; those clips are excluded
from the showcase rather than relabeled as valid own-pair Tomb evidence.
Read-only recording was corrected to trigger on native slime-fall action050a
in background0. Fresh507/508 pass runtime and captured-stage validation for
Kano/Sonya against their actual own victim:148 consecutive fall fields, all
in Dead Pool, native completion immediately after capture. Actual26 chips,
exact recorded frames, native audio and full AV decode pass. These clips omit
the uppercut startup, explicitly marked false; not complete stage-move videos.
Raw/WAV intermediates removed after encoding. Tomb/Pit and full-stage startup
footage remain open; no gameplay source or driver modifications were made.

Startup-complete Dead Pool509/510 captures152 fields from native uppercut0107
through slime fall to completion. Arena0 and both actual own identities are
required. The captured-stage verifier now derives startup inclusion from the
first recorded action rather than a hardcoded kind flag. Tomb511/512 uses
physical --stage-rematch, four real knockouts and capture background1; both
whole-stage and captured-interval qualifiers pass64 native spike fields, own
performer/victim art, stage gate rejection in initial Dead Pool and completion.
All four clips pass actual26-chip/frame/AV checks; raw/WAV intermediates removed.
Index replaces the partial-start Dead Pool links and adds true own-pair Tomb
clips. Full visual/audio approval, Pit, morphs and campaigns remain open.

Pit513/514 whole runtime passes after seven physical versus matches/fourteen
knockouts, all five own fall poses and impact. Their29-field videos are partial:
native mode2 transitions to cinematic9.515/516 cross mode9 but stop at207 fields
when native result mode5 starts. Neither is labeled a complete Pit clip.
Observer-only correction preserves capture through mode9 and mode5, collecting
stage environment each field and a60-field result hold, still bounded400.
Fresh517/518 qualify266 exact recorded fields:206 native death6 fields then60
death65535 fields, modes2/9/5 and arena6 with correct own pair throughout.
Native motion/26 actual chips/frame preservation/AV decode pass; raw/WAV deleted.
Decoded Sonya clip frame230 visibly shows Kano's own impact art and native
winner result. Uppercut startup inclusion is not certified by the strict0107
check; complete prior input/startup footage and whole audiovisual approval
remain open. Single-player campaigns/bosses/endings are not implied by these
earned versus-stage tests. Index links517/518 instead of partial Pit recordings.

Native morph519/520 passes on physical player1/player2. Whole-run commands,
all three transformations,524-field true identities, native timed returns and
22-damage transformed Knife/Ring qualify. Current forward/reverse art trace
also passes all three4-field phases and measured grounding in both directions.
Bounded recording allows800 fields only for morph0404 (other moves remain400),
ends after return to Shang plus eight stance fields; both clips are552 frames.
Exact captured intervals prove selected ID remains6, actual ID changes6->17/18
for524 fields, transformed projectile deals22 damage, then actual6 returns.
All26 chips, frame preservation, native AV and full decode pass; raw/WAV removed.
Index includes both clips. Final audiovisual approval, paired-throw timer edges
on this link, full normal-move showcase and single-player campaigns remain open.
