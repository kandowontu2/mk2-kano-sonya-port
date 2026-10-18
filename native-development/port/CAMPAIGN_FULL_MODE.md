# Bounded full-campaign test mode

The previous long harness allowed45000 fields and900 guest seconds. Those
bounds can truncate a complete expanded-roster campaign with introductions,
ladder pans, retries and credits. `--campaign-full` now explicitly selects
90000 fields,1800 guest seconds and a300-second host wall limit. It requires
the native gameplay candidate and campaign observer, rejects combination
with CPU-attract mode, and does not change ordinary/long test defaults.
Execution receipts record the host and guest limits. Read-only damage windows
may address these later fields but remain limited to300 fields each.

This is a capacity change in the test harness, not a forced progression or
successful play-through. Only ordinary controller inputs and explicitly
logged paid continues are used. There are no writes to game RAM, registers,
AI, health, difficulty, map progress, or victory state. Existing terminal
conditions still stop on faults, exhausted continues, natural game exit or
the bounded field budget. No saved state or debug ending entry is used.

## First current-program run

Run583 uses native program
F65002019A05D47400BD755B95C06546B9ADD104140472A111F1D107C3F6D512,
Sonya's established Jax-safe Ring and guarded Raiden Ring policy, a24-field
post-hit guard, and up to five normal paid continues. It ends normally at
35253 fields, well before all three capacity limits, after all five continues
are spent on Raiden. Baraka, Reptile and Jax are naturally defeated first.
Raiden wins all12 rounds; CPU health minima by attempt are129/102,29/36,
95/129,68/117,151/19,51/68. These are not match wins or later-stage coverage.

The current full26-chip/true identity/no missing marker/no illegal recovery
audit passes.43 source/tooling unit tests pass. The test capacity issue is
fixed, but this control policy still cannot verify the campaign or endings.
No ROM code or release package changed for this harness work.

## Expanded native continues and strict partial evidence

Full mode alone now permits at most20 explicitly requested normal paid
continues; ordinary and long modes retain the5-continue maximum. Every
buy-in, selection and continued combat remains logged. This is not an
unlimited retry, game-state write, difficulty adjustment or a1-credit claim.

Current-build Kano run584 completes normally at36023 fields with five
continues. Native same-attempt result counters prove Baraka, Reptile, Jax
and Raiden match wins; Kitana wins the remaining attempts. This is four
verified ladder advances, not a full campaign.

Run585 extends that unchanged policy to20 requested continues. Its initial
trace through the first five continues reproduces584 byte-for-byte. The
180-second host bound then terminates the run at76868 complete fields while
still at Kitana. Twenty buy-ins occur, but only19 continued combats start;
the final selection is interrupted. It is explicitly timed-out/partial,
not completed or passed. No recorded missing marker or illegal recovery
appears, and actual input chips match the current independently rebuilt26.
The future full-mode wall bound is increased to300 seconds to allow for
below-normal scheduling under other laptop work; game/field limits stay fixed.
This policy is not rerun solely to finish the twentieth lost-stage attempt.

The completed campaign audit now requires counters1 then2 on distinct rounds
of the same attempt. Earlier one-round wins are reported separately and never
added to a later match. A separate audit_partial_campaign.py writes only
CAMPAIGN_PARTIAL_AUDIT.json with completedTest/fullCampaign/fullPort/release
all false, rejects incomplete rows except a single interrupted final CSV row,
and keeps the strict completed-test gate unchanged.47 source/tooling tests pass.
