# Sonya/Mileena current034F campaign controller

749 reached map7 after naturally beating Sub-Zero2–0, but its generic
Mileena policy had no match win and minimum CPUHP81 in8373 combat samples.
Native source identifies sai actions00a/00bh, teleport0208h and roll020eh.
Normal action tags can be stale; threat tags are conservative input guards,
not an assertion of exact active-hitbox frames.

The opt-in --campaign-sonya-mileena-guard-leg requires Sonya. It extends
existing native Ring/RFP-ready uppercut/guarded Leg input decisions to
Mileena only, guards the sai/teleport/roll tags and generic projectile list,
retains low block, and permits the same neutral standing/grounded enemy
window within80 pixels. Four-prior-field guard, four-field LP+Block+Down
chord, own measured shortness/normal flags, cooldown and threat gates remain.
121 local tests pass, including native action constants and wrapper setup.
No ASM, ROM, AI, damage, health, difficulty or outcome changes were made.

750 completes normally at90000 fields (field-budget, mode2/map7/attempt18),
not a host timeout. Current26-chip/stock-MAME/frozen-read-only/identity18/
no-marker/no-recovery audit passes. All27252 pre-Mileena rows exactly match
749; SHA256 prefix D9C9F80C76DC6EC5A941FC0FFECC51C3C24AEC46706D1A9B4A053DC6955F30F1.
Thus earlier victories, including Sub-Zero2–0, remain unchanged.

Three native Mileena round wins, not a match win:
55934 attempt8 counters1–0, Sonya8HP/Mileena0;
70534 attempt12 counters1–1, Sonya34HP/Mileena0;
75096 attempt13 counters1–1, Sonya22HP/Mileena0.
These must not be aggregated across paid continues into a full match.
Dense traces show25 complete paired Leg21ah/21bh holds, each46 fields
(1150 total), not merely command requests. Progress still ends at Mileena.
Later roster/bosses/earned endings/cast/credits and full campaign are open.

Frozen controller SHA256:
441E2ACC52FB618DB1A6EC2D5B9D35BB449ABF3B3D4B4A50413C6460EBC7665A.
campaign.csv SHA256:
927CBA624985D266ADF0748AA883389D3C25963E8A0970B8A29515F3AFA1ED89.
Single MAME remained windowless/BelowNormal/about200MiB RAM. No capture or
new compiler build was needed. Existing proof files pin mutable tooling;
after harness changes their source hashes need deliberate requalification,
not silently relabeling historical files as fresh final acceptance.

##751 no-Ring input-policy experiment: not an improvement

An opt-in --campaign-sonya-mileena-no-ring requires the existing Mileena
guard policy. It cancels only pending Lua Ring input sequences and prevents
new ones in Sonya/Mileena; it does not cancel native moves, disable guest
buttons or alter the game. Guarded Leg, RFP counters and threat guards remain.
122 local tests pass, including the matchup scope and both cancellation/new
command gates. Earlier trace observations included HP loss with action tag
530, but tags can persist: that was not proof Ring caused most damage.

751 exits normally at90000, field-budget/mode2/map7, not a timeout. Current
26-chip/stock-MAME/read-only/frozen-controller/identity18 audit passes. All
27252 pre-Mileena rows exactly match750 with the same prefix SHA256 recorded
above, preserving all earlier match wins. No completed native Mileena winning
round is verified before the stop, versus three in750; no match win or later
progression occurs. The final finish-window state is not relabeled a completed
round result. The no-Ring flag remains default-off and is not adopted as a
winning policy. This narrows the controller experiment, not native playability.

No native source, ROM, damage, AI, difficulty, health or outcome changes were
made. Single MAME remained headless/BelowNormal/about200MiB. The campaign,
later bosses/earned endings and broader acceptance remain incomplete.

##752 neutral Leg window85: native2–0 at the field cap

751's normal grounded Down+Block observations within80/85 pixels numbered
222/425, respectively. These are guard contexts, not all valid enemy-standing
openings. The opt-in --campaign-sonya-mileena-leg85 extends only Mileena's
neutral controller distance80→85, retaining the existing shared85 ceiling,
standing/grounded enemy/normal flags, own shortness, four prior guard fields,
cooldown90 and four-field physical chord. Rings are restored (no-Ring flag
off); native collision/strike data remains unchanged.123 local tests pass.

752 exits normally at90000, field-budget/mode5/map7/winner1. Current26-chip,
stock-MAME/frozen-input-only/identity18/no-marker/no-recovery audit passes.
All27252 pre-Mileena rows exactly match750, same prefix SHA256 above.
Six native winning rounds are verified across separate continues; do not
aggregate those into a match. Crucially, attempt17 itself has round1 result
88968 counters1–0 and round2 result90000 counters2–0. The earliest sampled
mode5 score2–0 is89990, Sonya64HP/Mileena0. Thus a native winning2–0 score
is recorded, not merely low CPU health or a requested move.

The high-level naturallyDefeatedOpponents list intentionally requires actual
later-map observation, so it does not yet list Mileena: the field budget
stops during this result screen before progression. Do not claim map8 or
campaign completion. Next extend the bounded observation enough to inspect
the normal next ladder transition, keeping all game/AI/difficulty unchanged.

Frozen controller SHA256:
2E50E4E88CCBD316AC5068413F7554DD0B7C6B050B6ED290640B52EA46E16859.
campaign.csv SHA256:
299E0A786315B9B195EAA9F8B1A71763D7EA35B02360986CBDBB5B0DD5FAA6E7.
Single MAME stayed headless/BelowNormal/about200MiB. No native build or ROM
change was needed. Full campaign/bosses/earned endings remain unverified.

##753 extended observation verifies advancement

--campaign-extended explicitly requires --campaign-full and raises only
the field cap90000→120000 plus guest safety duration1800→2400 seconds.
Host limit300 seconds, maximum20 paid continues, hidden/below-normal MAME,
game bytes and all input policies remain unchanged. Optional passive damage
observation retains its300-field maximum window.128 local tests pass,
including legacy/default bounds and exact extension-prefix rejection tests.

753 exits normally101496, left-campaign/map8/Johnny Cage, not timeout or
the new field cap. Stock/current26-chip/frozen-read-only/identity18/no-marker
audit verifies Mileena2–0 on attempt17: native results88968 counters1–0 and
90186 counters2–0, followed by map8 gameplay. This closes the earlier result-
screen advancement gap. It does not prove the rest of the campaign.

compare_campaign_extension.py requires identical ROM/emulator receipts,
arguments differing only by the extension flag, completed receipts and
exact old trace prefix. All45000 recorded data rows through90000 match;
normalized-text prefix SHA256:
D78030B002E804263595B880A3BDBAFFB9796F1ACF030F3D63C5F4A709F31810.
It records extendedOutcomeVerified false: native outcome proof is the
separate campaign audit, not the prefix comparison.

Cage is not defeated: no native player winning round is verified before
the20-continue budget is exhausted. Later roster/bosses/earned endings/
cast/credits remain open. No ASM, ROM, AI, difficulty, health, selection or
outcome writes were introduced. Single MAME stayed headless/BelowNormal
and about200MiB RAM, with no large capture or native rebuild.
