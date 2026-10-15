# Native grab audio corrected; broader full-game goal remains open

The new diagnostic candidate is diagnostic_v1411_native_grab_audio.
EXE SHA256: 01EF3950691A890BAA41723D99935E44A28B09A7431EA78EC5DBF8E0E90630C3.
Payload remains 5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D.
Compiled machine source is C603BA057414E2288D157CF2BED0A52CA69BCC69C7C2889AAF63BA8EA8C67CB4.

The playable CMD is still PLAY_CURRENT_V1340_TEST_BUILD.cmd. No new launcher
promotion, release ZIP update, material deletion, or full-game completion claim
has been made. Canonical historical source and installed EXE are restored.

## Actual changes and evidence

The previous goal turn produced new evidence: the v1340 Kano CPU choke/render
check passed, and all sixteen human move audio captures completed. This turn
then verified every capture against current actual input/state events. All 48
before/recovered/final screens remained byte-exact. Both character selection
donors are audible at their actual markers, at the source-bound channel/speaker
level. audit_v1408_current_move_audio_checked is explicitly an inventory and
selection-voice check, not complete move sound fidelity.

Fresh unassisted original MK3 references audit_v1407_original_audio_choke,
leg, and bicycle establish actual cue timing and native DCS commands. The
old notifier API failed in preserved v1405 captures; v1406 changes only its
API spelling and preserves every original control and state observer.

Original evidence exposed omitted cues in the port. The new compiled guest
adds exactly three source blocks:

- Sonya leg-grab startup: original-grounded shared MKII unvoiced swing.
- Sonya leg-grab contact: shared MKII hard contact effect plus actual victim
  pain voice, invoked through the native opponent actor/Main callback.
- Kano choke contact: one actual victim pain request before the lift, not a
  repeated sound at each damage pulse.

audit_v1415_native_grab_audio_checked independently reconstructs the entire
actual guest: declared calls inserted into the two existing owned code ranges,
only corresponding internal absolute branches relocated, every other byte
unchanged. Driver, art, payload and unrelated source are unchanged. All six
choke/leg/bicycle human cases pass in both slots: every native input, identity,
pose, collision, health and recovery event matches prior capture; all eighteen
complete scenes are byte-exact. Read-only request taps prove actual physical
owner/victim IDs and timing; DCS writes and actual PCM changes prove the new
contact requests are not silent logging. This is not an isolated waveform or
perceptual equivalence oracle, and the port deliberately uses MKII equivalents,
not incompatible MK3 numerical sound commands.

audit_v1421_grab_defense_checked passes ten genuine choke/leg block/miss and
leg duck-block cases. All native events and thirty complete scenes remain exact.

audit_v1424_grab_audio_cpu_checked passes actual Kano CPU chokes against human
Kano and Sonya, native individual handoffs and observed follow-ups, with 179
full sampled scanouts reconstructed exactly. The Kano mirror continuation is
a native blade miss followed by original trail cleanup and owning regain; the
Sonya-human continuation is ordinary AI. These are not tests of Sonya CPU.

Preserved v1420 failure correctly rejected a blade continuation declared as
ordinary. v1422 then exposed diagnostic cycle bookkeeping: FIELD labels the
current grab, while FOLLOW_FIELD labels the first completed grab. A real second
choke enters at field1997 during the observation tail. v1423 verifies both
ordinals against the actual entry chronology and compares every other field
exactly; no actual captures or guest state were changed. v1426 rejects nine
in-memory corruptions of ordinals, real entry evidence, identities, Main, HP,
coordinates, velocity and cleanup locks. v1425's final attempted velocity
counterexample was a no-op and remains failed; v1426 explicitly prohibits
no-op counterexamples. The second grab is not claimed completed by this scope.

## Still required

The new candidate needs the complete broad current regression and launcher
check before promotion. Full move sound/choreography, Sonya CPU and both CPU
slots, all relevant victims, repeated moves/interruptions/KO, remaining native
animation and finisher consumers, other arenas/shadow phases, genuine full
towers/bosses/continues/endings/secrets/cinematics, final packaging and obsolete
build cleanup remain open. The objective remains natural game integration in
all aspects; bounded passing checks do not redefine it.
