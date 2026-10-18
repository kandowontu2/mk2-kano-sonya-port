# Physical counter-policy comparison (538–540)

Correction: references below to opponent ID 7 as "Mileena" are historical
mislabels. ID 7 is RAIDEN; ID 5 is MILEENA. See CAMPAIGN_ID_CORRECTION.md.

No native game, AI, difficulty or ROM changes were made. The new optional
`--campaign-female-counter` policy changes only physical controls against
Kano/Kitana and Sonya/Mileena or Kitana. Paid continue ordinal selects a
sweep/approach, retreating jump-kick or crouch-block/uppercut profile. It is
experimental and unsuccessful; it must not be described as a gameplay fix.

Run 538 accidentally omitted the previously successful `--campaign-jump-grapple`
baseline flag and therefore lost to Baraka. Its 20,609-field failure is retained,
not treated as a comparison of the target matchup or silently discarded.

Run 539 restores that flag plus Kano's Reptile/Jax/Mileena Knife policy. It
earns Baraka, Reptile and Jax wins, then clears Mileena on the first normal
paid continue. It reaches Kitana at map position 4 but loses across the
remaining continues, ending at 32,566 fields. Kitana takes almost no damage
from this counter policy (one round minimum 154/161). This is worse offensive
performance than the earlier zoning experiments, not progress past Kitana.

Run 540 uses Sonya's successful jump-grapple baseline with kick age 18 and
Jax Ring option. It earns Baraka, Reptile and Jax wins, then loses to Mileena
through five accepted native continues, ending at 34,410 fields. The new
counter policy does not meaningfully damage Mileena (first round minimum
154/161, remaining rounds 161). Do not rerun this policy unchanged.

Both valid target comparisons pass actual full 26-ROM verification, true
selected/active identities, no missing-animation markers, no illegal-opcode
recovery and no Lua fault. These are failed controller strategies, not proof
that every move works against these CPUs, and not full-campaign acceptance.
Later opponents, bosses, earned endings and credits remain unverified.

Next controller work should inspect attack timing, actual grounded heights and
spacing from observed states before adding more speculative policies. Current
best campaign positions remain Kano/Kitana and Sonya/Mileena. Ending sources
still provide only provisional own text; final artwork and earned runtime
verification are separate unfinished requirements.

The 14 CPU-action/boss-category/campaign-round/IPS tests pass. An initial unit
test invocation used the nonexistent singular module `test_boss_category`;
the corrected invocation of `test_boss_categories` and all four suites passes.
Two ending-source/PCM tests also pass. These source checks do not prove ending
runtime. No release was refreshed or published from these failed campaigns.

## Instrumented coordinate diagnosis (541–542)

Run 541 repeats the Kano path with only one accepted paid continue, adding
per-field target-matchup physical-input/height logging. The trace shows Y
65533 being interpreted as a huge positive coordinate, yielding bogus heights
around -65,423. Native positions are signed 16-bit words. The controller now
uses explicit signed reads for X/Y and grounded Y; IDs, health and actions
remain unsigned. This changes only observation/controller decisions, not ROMs.

Run 542 validates the correction on the same finite path: observed own heights
range -17 to 113 instead of wrapped negative 65K values. All four earlier
opponent wins remain, all 26 ROMs and true identities pass, and no missing,
recovery or Lua fault is observed. However, Kitana still wins both rounds with
161 HP. Correct coordinate decoding is not a successful combat strategy.
The counter trace records 59 Up, 44 HK, zero HP and 635 Block fields in 1,130
live target-matchup observations. Attempted inputs therefore need to be aligned
with actual ready/takeoff states rather than assuming a jump began when Up was
requested. No further unchanged counter run is justified.

test_campaign_coordinates checks all 65,536 signed words, the negative-Y
height regression and controller read-type contracts. Together with the other
four suites, all 16 tests pass. Full campaign and ending acceptance remain false.

## Observed takeoff rather than requested takeoff (543)

The audit of 542 establishes zero native jump fields and zero flying kicks,
despite 59 Up and 44 HK input fields. This means the original policy was not
actually testing its proposed jump-kick strategy. Native JOY separates rising
from crouch (0301) from stance and uses 0308/030b for actual jumps.

The optional `--campaign-counter-takeoff` policy releases crouch/block for nine
fields, requests Up, and starts its kick timer only after observing 0308/030b.
It never treats arbitrary airborne reactions or a requested button as proof
of takeoff. Run 543, using the same finite Kano path, now produces eight native
jump episodes (144 observed fields) and eight flying-kick episodes (135 observed
fields). All 16 HK-request fields occur during a native jump. Kitana loses
26 HP in the second round, but still wins the match; first round damage is zero.

All earlier four opponent wins, exact 26-ROM identity and no-fault checks pass.
This fixes a demonstrated controller timing defect, not a ROM defect or full
campaign completion. The next strategy comparison can now measure genuine
jump-kick spacing/direction instead of button requests that never activate.
`audit_counter_takeoff.py` keeps separate input/state evidence for 542 and 543;
it does not infer a campaign win from successful move activation.

## New ending-enabled link, forward and grounded comparisons (545–546)

Run 545 uses the first two-page-ending program (8769E42C...18A46C8) and an
explicit forward-jump/sweep profile. It earns the first four match wins but
still loses Kitana through three accepted paid continues, ending at 28,955
fields. It observes 17 genuine jump episodes and 40 HK-request fields during
native jumps; successful activation is not a match win.

Run 546 tries a grounded Knife/duck-block policy instead, on that same program.
It again clears the first four matches and loses Kitana through three paid
continues, ending at 28,036 fields. Kitana minima across eight rounds are
161,161,161,161,139,161,139,139: this is not sufficient offensive performance.
Both runs pass actual current-ROM and no-fault audits before the subsequent
ending-cleanup program rebuild. Neither proves earned ending runtime; do not
silently reinterpret these failures as an AI or game-code defect.
