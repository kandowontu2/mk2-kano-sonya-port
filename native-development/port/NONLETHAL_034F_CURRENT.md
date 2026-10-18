# Current034F nonlethal-finisher regression

Stock-MAME runs699 Kano Friendship,700 Sonya Friendship,701 Kano Babality,
702 Sonya Babality exit normally and pass detailed move qualification plus
FINISHER_REJOIN_QUALIFICATION. Each is Player1 versus the other own fighter,
with physical selection, two earned KOs and native finishing commands.
All26 actual runtime chip bytes match current034F; no custom driver or
guest-memory writes. Native active fields are193/176/192/192 respectively.
Each has600 fresh combat fields, correct own identities/full initial health,
live damage, cleared winner/death state, no tracked finisher child and
78000 hardware palette comparisons with original palette sources restored.
Both observed baby images are absent from the fresh active object list.

Sonya700 additionally passes FRIEND_LIFECYCLE_QUALIFICATION:128 observed
completion-context fields, completion context absent after native completion,
dance context absent through selection/fresh600 fields, and no further
chicken commands after selection. This does not establish audio-tail mixing
or absence of every possible process leak. Those flags remain false.

Detailed Friendship/Babality validators now use the same strict pinned
finisher_observation_end helper as lethal finishers: ordinary runs still
require9000 fields; an explicit rejoin run requires its separate current
evidence proof and exact600-field fresh interval. Timing, command eligibility,
pose and native completion assertions remain intact. Reports record actual
total fields and pin the helper.119 selected tests pass; interval helper
regressions also exercise actual Kano/Sonya Friendship proof receipts.

Opposite-side034F refresh, negative punch-eligibility refresh, audio tails,
broader victims/edges, stages, specials and campaigns remain open. Historical
F650 fixtures are not silently called current034F tests. No ASM or ROM bytes
changed in this turn; all four tests were headless and sequential, with no
large media capture. This is not final release acceptance.

## Mirrored034F positive cases

703 Kano Friendship,704 Sonya Friendship,705 Kano Babality,706 Sonya
Babality repeat the same tests with Player2 performing. All exit normally,
pass detailed move/actual26-chip qualification and600-field fresh-match
proof, and retain193/176/192/192 native active fields. Sonya704 also passes
the observed completion/dance-process and chicken-command cutoff checks.
Both mirrored baby images are absent from the fresh active object list.

qualify_nonlethal_matrix.py rechecks all eight699–706 current actual ROM
archives, frozen controller hashes, current detailed proof pins, actor/
victim/side, native durations/completion and exact fresh-match interval
proofs. Sonya Friendship lifecycle proofs and Babality image retirement
are required where applicable. NONLETHAL_MATRIX_QUALIFICATION.json records
allEightPositiveCasesPassed true, but currentNegativeEligibilityVerified,
arbitraryVictimCoverage, allCleanupAndAudioVerified, fullPortVerified and
releaseReady false. This supersedes only the mirrored positive open item.
Negative punch-eligibility, sound tails and remaining full-port gates are
not inferred from positive cases. No native game or ROM changes this turn.

## Current punch-ineligible command rejection

Runs707–710 Player1 and711–714 Player2 cover Kano Friendship, Sonya
Friendship, Kano Babality, Sonya Babality respectively after physical
punch-based round wins. All eight exit normally at9000 fields and pass
current26-chip detailed qualifiers. Each earns two KOs, records a native
nonlethal finishing command in the finish window with nonzero punch
history, and observes zero nonlethal action fields/no native completion.
Native command observation counts are32/48/48/56 on each side. Kano's
Friendship uses its existing exact button-queue check; Sonya Friendship
and Babalities use the direction/button-history helper. These are recorded
history contexts, not assertions of every precise live-button boundary.

qualify_negative_nonlethal_matrix.py checks all707–714 archives/controllers,
proof pins, actor/victim/side, natural KO counts, native command evidence,
zero activation and rejection flags. NEGATIVE_NONLETHAL_MATRIX_QUALIFICATION
records allEightPunchIneligibleCasesPassed/currentAll26ROMsVerified true,
but exactInputTimingBoundariesVerified/allInvalidCommandsVerified and full
port/release flags false. The positive699–706 matrix was rechecked too;
119 selected local tests pass. No native source, ROM or difficulty changes.
All runs were headless, sequential and below-normal priority.

This closes the finite current punch-ineligibility refresh, not audio tails,
all invalid commands, arbitrary victims, stages/specials/full campaign or
earned ending acceptance. Do not infer full-port completion from these16
positive/negative nonlethal cases.
