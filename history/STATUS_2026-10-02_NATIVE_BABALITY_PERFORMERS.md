# Own human Babality integration — not full finisher/release acceptance

The latest test CMD now opens diagnostic_v737_native_babality_performers.
Production launcher and release ZIP are unchanged. Candidate SHA256:
4571A2021014EBBA56FF5EE92A28F5C5CD4D03AADC05D6EF4271D6D0829D9A64.
Unchanged payload SHA256:
1367D5A0D42C661CF555F42231A20A650C28E107AB9C80BD821C0BEA7EB4D5EF.
Pre-edit v728 sources and previous test CMD are preserved in audit_v736.

## Original command evidence and implementation

Read-only, no-cheat original MK3 traces genuinely select Kano0 and Sonya1.
Their physical Low Kick events reach records FF986470 and FF98AA80, each
dispatching the original shared Babality. Separate physical-direction traces
confirm MK3 Up/Down/Left/Right codes 6/7/8/9 in both slots. Both engines' native
facing comparisons are the same. Port records translate to MKII codes 5/6/7/8.

Commands are Kano F,F,D,D + LK and Sonya D,D,F + LK, within the original
40-field history window. No borrowed fighter ID or command record is used.
The extended performer table preserves its 17 preexisting words. Only the
added IDs' LK event bindings change. Each calls original FF87E120, then falls
back to its previous handler if rejected (Kano's stage-finish parser; Sonya's
existing no-special handler). MKII's original finish-mode/no-HP-or-LP usage
eligibility, matcher, scheduler, victory animation, victim baby construction,
cinematic and cleanup are untouched. MK3's different no-Block rule is not
substituted. Complete actual guest ROMs differ from v728 by exactly 139 bytes,
wholly accounted for by the new table, two commands, two wrappers and operands.

## Actual bounded verification

Four cold physical-input-only runs cover each own performer in both slots and
opposite facings, with Kano/Sonya as the reciprocal victims. Each earns both
rounds via actual native damage stores (322 total) without RAM writes, health
assistance, cheats or state fixtures. Native finish eligibility, command
acceptance, actual human ownership, true victim IDs, baby construction and
height-to-floor placement, palette words, ownership handoff, retirement,
object reuse and next-screen transition are checked. Twelve rendered snapshots
match all 10,536 nontransparent original baby pixels exactly.

Four earned-win negative runs cover both characters' wrong-direction rejection
and native winning-round punch restriction. The wrong commands are otherwise
eligible; punch-used cases exercise the actual winner's nonzero HP counter.
Neither enters the native action or constructs a baby, and both cleanly leave
the finish window. These are narrow human eligibility checks, not an exhaustive
wrong-button/timing/input matrix or CPU finisher certification.

Both stock Kitana-on-Liu runs match all 182 saved frames / 18,491,200 display
pixels against v728. The first P2 stock attempt hit its 95-second limit before
earning a second win, so it is retained as incomplete; a 180-second rerun
completed cleanly. Ten complete cases have terminal exit zero. Forty-three
baseline/in-memory corruption checks pass. The independently checked handoff
sample follows actual baby construction: Kano's longer command activates later
than Kitana's, so a fixed age-128 sample was not valid for Kano's handoff.

Evidence: original v734/v735 traces, v738 ten attempts (one incomplete), v740
longer stock rerun, verifier/runtime checks/test tools v739, checkpoint v741.
The wrapper's retained Kano stage-finish fallback is byte-checked; actual stage
action on this candidate remains part of final regression, not newly certified.
Visual snapshots show character-owned victory poses and correct winner names;
this is not a complete cinematic timing/banner, all-arena or audio audit.

## Remaining full goal

Friendship performer integration and remaining finishers/cinematic/CPU coverage,
full unassisted towers and boss clears, broader human/CPU specials and
interruption/audio checks, whole-scope regression, and matching final production
CMD/release ZIP still remain. Historical floor-shadow, UI, selection, mobility,
special and ending evidence is not wholesale recertified by these bounded runs.
Full-port and full-finisher acceptance remain false. No material data deleted.
