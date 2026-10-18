# Kano physical boss policy trial

Diagnostic clarification: the failed84-range trial has6 requests,4 native
uppercut activations and4 corresponding observed20HP-drop windows. Zero
40HP windows must not be read as zero damage: this boss scenario uses20HP
drops. It still has no native round or match win. The inspector now reports
boss requests/activations/20HP windows separately from native round/match
counters, with tests rejecting health-window-as-win inference.332 tests pass.

## Boss-range readiness trial (active)

`stock_wolf_2219_kano_kintaro_wide` uses explicit
`--campaign-kano-kintaro-wide-prepare`, requires Kano boss policy and rejects
both prior experimental flags. Source/ROM rules remain unchanged. Recorded
successful baseline uppercut entries typically began at94..99 center gap;
the failed readiness experiment's84 limit missed those windows. Baseline
CPU health drops are primarily20, not the human-opponent40 expectation.

New physical-controller HP range is105 only against selected Kintaro12.
Human range84 and all actual grounded/flags/duck-table/height/preparation/
cooldown gates are retained, as are early stomp evasion and407h/507h guard.
Inspector rejects human requests at95 and all boss requests beyond105;
boss observations require an explicit recorded experimental argument.
All331 unit tests pass. No boss-clear/hit claim before terminal audit.
Move-family proof pins need normal refresh after this harness change.

## Explicit jump-kick trial (active)

Terminal correction: the forward-jumpkick experiment is REJECTED as a boss
strategy. It finishes151769 fields normally, exit0/not timed out, with
current-ROM/stock/frozen-input/identity audit passing. Sixteen Kintaro rounds
yield no native round win; bestCPUHP110. The earlier simple uppercut/evasion
policy remains the better observed baseline (two individual round wins).
This is another physical-controller loss, not a demonstrated native defect.
Do not enable this opt-in policy in production defaults.

`stock_wolf_2219_kano_kintaro_jumpkick` runs hidden/BelowNormal. Its new
opt-in flag requires the prior Kano boss policy and rejects simultaneous
readiness-experiment use. Only Kano17 versus selected Kintaro12 initiates
the existing physical jumpkick plan: approach if distance>260, otherwise
start only when grounded with native reaction/attack flags clear. The plan
already supplies three fields of Up+toward and the normal delayed HK pulse.
Existing early stomp evasion precedes it and retains priority; no extra
top-level Lua locals were added. Human/Kahn branches are unchanged.

All330 unit tests pass. No ASM/ROM/AI/difficulty/health/damage/position/result
edits. Terminal ROM/identity/input audit and native result evidence remain
required. A requested jump/kick is not a proven hit or campaign clear.
Recorded move-family proof pins need refresh after this harness change.

## New explicit readiness trial (pending)

Terminal correction: this experiment is REJECTED as a boss strategy. It
finished153740 fields normally, exit0/not timed out, with current-ROM/
stock/frozen-controller audit passing. Kintaro16 rounds yield no native
round win, bestCPUHP141. Six readiness HP requests give4 observed native
uppercut activations and zero40HP damage windows. The prior simple policy
earned two individual Kintaro rounds and was materially better. Do not
promote the experimental readiness flag into defaults or describe it as a
game fix. Retain the explicit opt-in/frozen trace for reproducibility.
Source/ROM/AI/rules remain unchanged. Spear/lightning/shock refreshes now run
sequentially after the terminal campaign.

`stock_wolf_2219_kano_kintaro_prepare` is the new hidden/BelowNormal run.
`--campaign-kano-kintaro-prepare` requires the existing Kano boss policy,
which itself requires the human-preparation/duck-table options and rejects
Sonya. Only selected Kintaro12 receives the additional physical readiness
policy; all prior human decisions and the Kahn counter remain unchanged.
Early stomp evasion retains priority. Grounded ordinary windows reuse the
existing actual-duck/table/height/flags gates,<=84 HP range,4-field minimum
preparation,60-field request spacing and3-field HP hold.407h/507h otherwise
guard instead of requesting an uppercut into stomp/throw states.

This is an experimental controller policy, not a native character fix or
boss-clear claim. No ASM/ROM/rules/AI/damage/health/position/result changes.
The terminal audit and finite activation/damage evidence are still required.
The inspector admits selected/active Kintaro12, but continues rejecting a
Shang-to-Kintaro morph.328 full-suite tests passed before the last gating
test; all9 targeted neutral-uppercut evidence/policy tests now pass.
Move-family proof pins require normal refresh after the harness change.

## Terminal result (current 2219 ROM)

The hidden trial finished normally at164920 fields: execution exitCode0,
timedOut=false. The terminal campaign audit and human-input diagnostic pass.
All14 human opponents were cleared again; Kintaro was not cleared before
the32-continue cap. Kahn and the earned ending were therefore not reached.
This is a controller loss, not evidence of a native softlock.

The stomp log contains1694 rows in34 contiguous escape episodes. Every
episode observes Kano airborne after the physical jump request. This rules
out a completely inactive escape selector; it does not prove every stomp
was avoided. Native result counters independently confirm two earned
Kintaro round wins: attempt27/frame141002 and attempt31/frame157298,
each tying that match1–1. Both deciding rounds were lost; no match-clear
or ending claim follows from these individual wins.

The recorded current-ROM move-family requalification also finished exit0:
16 ordinary-special side cells,8 own lethal/recovery cells,14 morph cases,
8 transformed lethal/fresh-Shang cells,16 nonlethal positive/negative cases,
and16 stage/chord/Pit/rejoin cases. No emulator rerun or native-ROM change
was needed. The explicit Kano/Sonya Kahn-profile unit suite passes6 tests.

The active-trial description below is historical, not a live-process claim.

`stock_wolf_2219_kano_boss_guard` is active hidden/BelowNormal, one stock
MAME,180000-field finale/ending observation and the same32-continue cap.
Existing background-margin option allows the full observation window; it
does not alter gameplay. No ending/clear is claimed before actual evidence.

The successful historical Sonya787 controller used early stomp evasion,
NOT the optional Sonya Kintaro guard branch. The explicit new Kano boss flag
therefore enables the same physical early407h takeoff tracking, one escape
jump and stable away-from-edge direction using native left/right edge data.
The optional Sonya-only Kintaro guard branch remains unchanged and disabled
for Kano; the rest of Kano's existing attacks remain physical inputs.

For Kahn13 only, Kano shares the verified read-only charge-routine/contact-wake
classification, actual duck-height/button-table readiness,36-field counter
spacing and physical opening back-jump. The native MAP/listing validates the
observed routine bounds and contact wake; no process/action pointer is written.
Earlier human strategies are untouched by the boss selectors.

All326 full-suite tests pass, including explicit Kano flag/prerequisite/actor
and native-state gating. Existing source-inspection tests now identify the
shared Sonya/Kano boss branch and retain their readiness/edge/write-prohibition
assertions. No native ASM/ROM, AI/difficulty/health/positions/damage/results
change. Terminal full current-ROM/stock/frozen-input/native-counter/ending
audit is still required. Prior recorded proof pins need normal refresh after
the new harness flag; no frozen records were edited.
