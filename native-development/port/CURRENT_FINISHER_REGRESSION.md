# Current-program finisher regression

Program SHA256:
F65002019A05D47400BD755B95C06546B9ADD104140472A111F1D107C3F6D512.
These are new physical-input replays on stock MAME, not inferred approval
from videos or checks of a previous program. Both qualifiers verify all26
actual ROM chips, the frozen controller, no guest writes/custom driver,
normal process exit, and no captured Lua/finisher faults.

## Sonya Friendship, player2: run589

Physical Friendship completes and selection returns at6502. A fresh match
starts7053 and runs600 observed fields with correct own identities, full
starting health, damage and reset death/winner state. Original palette sources
and78000 actual hardware palette-color comparisons pass. The dedicated
lifecycle check observes128 completion-context fields, no completion context
after native completion, and no dance context from selection through those
600 fresh fields. No new chicken commands occur after selection (last6414).

This does not verify rendered audio tails, the full overlapping mix, or
exclude every possible process leak. Broad acceptance flags remain false.

## Kano eye laser, player1: run590

Physical fatality completes; tracked object/process retirement occurs5335.
Selection returns5782, fresh combat begins6333 and runs600 observed fields.
True own identities, full health, live damage and reset winner/death state
pass.18 tracked prior effect shapes are absent from the fresh active list.
The tracked finisher object/process are gone, original palette sources are
restored, and78000 hardware palette-color comparisons pass.

This is one finite victim/side case, not all laser interruptions, palettes,
sound tails, or all finishers. No source/ROM change was necessary. Remaining
current-build finisher cases, full campaigns, later ladders, earned endings,
remaining audio and final release acceptance are still open.

## Opposite-side Friendships: runs635/636

Kano player2 run635 completes and returns through selection6022 to fresh
combat6573. Sonya player1 run636 returns through selection6502 to fresh
combat7053. Both pass600 consecutive fresh fields of own identities, full
starting health, live damage, winner/death reset and original palette
sources plus78000 hardware palette-color comparisons. Actual26-chip and
frozen read-only controller checks pass; both runs exit normally.

Sonya's dedicated lifecycle check observes128 completion-context fields,
then none after native completion. Dance context is absent from selection
through the600 fresh fields, with no chicken commands after selection
(last6478). This adds the opposite sides to594/589. It does not qualify
all process leaks or audio tails/mix; those flags remain false. No ROM,
native source or emulator change was required.

## Kano heart extraction and Sonya kiss, player1: runs591/592

Both physical-input runs exit normally and pass the current-ROM rejoin
qualifier. Each records231 fields of the appropriate native action
(540 extraction /542 kiss) with fatality death state1 before completion.
Selection returns5902 and fresh combat begins6453 in each run, followed by
600 consecutive observed combat fields with correct own identities, full
starting health, live damage, and reset winner/death state. Original palette
sources and78000 hardware palette-color comparisons pass per run.

Six extraction and eight kiss prior effect shapes are absent from the fresh
active object list. Neither case proves every effect object/process retired
at the exact completion field: that qualification remains false, as do full
audio-tail, interruption, all-victim and release acceptance. These tests
required no source or ROM changes.

## Mirrored extraction / kiss: runs633/634

The physical player2 cases both complete the231-field native action/death1
interval, return through selection5902 and start fresh combat6453.600
consecutive fresh fields pass true identities, full starting health, live
damage and reset death/winner checks. Original palette sources and78000
hardware palette-color comparisons pass per run. Six extraction/eight kiss
prior effect shapes are absent from the fresh active object list.

Both runs exit normally, verify all26 actual current ROM chips and frozen
read-only controller provenance, and report no faults. Combined with591/592,
this covers both performer sides for these defined own-victim cases. It
does not prove exact completion-time retirement of every object/process,
every victim/interruption or full audio-tail/mix acceptance. No game/ROM or
emulator change was required.

## Sonya energy orb, player1: run593

Normal exit and current26-chip verification pass. Native action544/death2
lasts176 observed fields. The tracked effect object/process retire5343;
selection returns5782 and fresh combat starts6333. The600-field fresh-match
checks pass for own identities, health, live damage, reset winner/death,
original palette sources and78000 hardware palette-color comparisons.
Fourteen prior effect shapes are absent from the fresh active object list.
This proves this finite side/victim replay, not all interruptions or audio
tails. No source or ROM change was needed.

## Mirrored eye laser / energy orb: runs631/632

Both physical player2 cases pass the same current26-chip/frozen read-only
controller and finite finisher/rejoin checks. Each completes the176-field
native action/death2 interval, returns through selection5782, starts fresh
combat6333 and observes600 consecutive fields of correct identities, full
initial health, live damage and reset winner/death state. Original palette
sources and78000 actual hardware palette-color comparisons pass per run.

Tracked object/process retirement is verified at completion for both;
18 laser/14 orb prior effect shapes are absent from fresh active lists.
This adds the opposite performer side to590/593, not all victims,
interruptions, sample tails or general allocator/process lifetime. Both
runs exit normally without faults. No native source/ROM/emulator changed.

## Kano Friendship, player1: run594

Native Friendship death7 is observed for193 fields. Selection returns6022,
fresh combat starts6573 and the600-field identity, starting-health, damage,
winner/death reset and palette checks pass. Seven prior effect shapes are
absent from the fresh active list. This does not prove exact completion-time
object/process retirement or audio tails.

## Kano and Sonya Babalities: runs595/596

Run595 uses Kano player1 against Sonya; run596 uses Sonya player2 against
Kano. Both physically activate native Babality death5 for192 observed fields,
complete, return through selection and run600 fields of fresh combat.
Run595 selection/fresh frames are5902/6453; run596 frames are6502/7053.
Own identities, full starting health, live damage and winner/death reset
pass. Each run verifies original palette sources and78000 hardware palette
color comparisons. The native baby image is observed before rejoining and
is absent from all600 fresh active-object lists.

## Opposite-side Babalities: runs637/638

Kano P2 run637 completes the192-field death5 case, returns through
selection5902 and starts fresh combat6453. Sonya P1 run638 returns through
selection6502 to fresh combat7053. Both pass600 consecutive fresh fields
with own identities, full starting health, live damage and winner/death
reset. The baby image was observed before rejoining and is absent from
every fresh active-object list. Original palette sources and78000 hardware
RGB comparisons pass per run, as do all26 actual current ROM byte checks.

Both exit normally without faults or guest writes. Combined with595/596,
these cover both performer sides of the defined own-victim Babality fixture,
not every eligibility/input-order/victim/audio case. No game/ROM change.

All three runs exit normally and verify the current26 ROM chips, stock MAME,
frozen physical-input controller and no guest writes. They add finite
side/victim coverage, not all interruptions, all victims or audio tails.
No source/ROM changes were required. The48 source/tooling unit tests also
pass; that count is not a whole-game or full-campaign qualification.
