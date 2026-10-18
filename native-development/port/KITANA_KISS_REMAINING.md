# Kitana kiss: reproduced malformed victim reaction

Timing interpretation corrected: RAIDEN_BURST.md records direct late
captures showing native effects can continue beyond the completion flag.
The historical first-link victim trace ended at that flag, so absent pop
rows alone did not prove a visible cutoff. The added own master wait was
removed after late-lifecycle tests281..284 verified the full rendered
sequence with native timing; see NATIVE_KISS_TIMING.md.
Palette, facing and short-table defects have separate evidence and are
not retracted. Current ROM uses the original96-field master delay.

Current native source defines the command in fn1_lk_open/scom_fn1_db:
hold LK at least038h native fields, forward/forward/down/forward and release
at close range045h. The controller uses physical inputs and two naturally
won Kitana rounds, never forced HP/finisher/CPU state.

Trials241/242 did not activate the fatality and cannot establish a ROM
defect. Trials243/244 added a pre-KO LK hold but still missed the168-field
Finish Him window: arming at80 plus releasing at105 exceeded that window.
The corrected controller keeps the pre-KO charge, enters directions at
command6/14/22/30 and releases at38, inside the native timing/range gates.
No game timing or collision rule was changed to make the test pass.

Runs245/246 now activate the real fatality after two natural KOs, each
completing9,000 fields and308 fields of native f_death2 followed byffff.
Both true own IDs remain intact. Nevertheless, inspected final captures
show corrupted colours, wrong placement and no proper inflated own body.
Native completion is therefore not acceptance. Four known unguarded data
tables lack own entries:

- MKDEATH kissed_coor_adj:12 coordinate words.
- MKDIE inflate_animations:16 animation pointers.
- MKDIE inflate_palettes:12 palette pointers.
- MKDIE pop_palettes:12 palette pointers.

`audit_kitana_kiss_failures.py` pins these source dependencies, current
program/graphics, stock emulator and read-only observer, actual own IDs,
two natural KOs, activation/completion and the two inspected screenshots.
KITANA_KISS_FAILURE_AUDIT.json explicitly records behaviorPassed:false.
No native game code or graphics changed in this diagnostic step.

Next inspect the full inflate_pose/r_kissed/get_pop_pal sequence contract,
then supply proper readable own inflation/burst artwork and compatible
palettes as well as correct kiss alignment. Do not replace another actor's
fat body or merely clamp the indexes. Preserve original paths and validate
the actual inflation and burst before claiming the fatality compatible.
Mirrored cases, original-character controls and current-link clean rebuild
remain necessary. No release was promoted.

## Inflation source staging

generate_inflation_sources.py converts the corrected transparent draft to
twelve editable own-palette PGM frames under assets/inflation.
build_inflation_assets.py stages readable generated_inflation/KSINFART.ASM
and packed graphics, preserving the current arm-rip prefix byte-identically.
Each actor has five multipart inflation groups, zero, one pop group, zero,
matching the native consume/advance sequence. Twelve six-bit payloads pass
byte-window round-trip checks; three codec unit tests pass. This is staging
only: no active module, graphics path, socket archive, ROM or release changed.
Kano phases4/5 still touch cell boundaries and need correction before acceptance.

Further direct inspection found a fifth short dependency: MKDEATH
kissed_offset has12 words. dizzy_wait adds the selected word to the victim
main028 animation pointer to choose its stopping frame. This needs an actual
own dizzy-frame offset, not an arbitrary clamp. It is shared with Mileena's
body-suck setup, so both callers need controls. The earlier four-table audit
is historical diagnostic evidence, not an exhaustive dependency list.

## Shared dizzy setup guard linked

kiss_setup_source.py now guards own IDs before the short kissed_offset
lookup, selecting32*5 from the verified seven-pose own main028 loops.
The original helper call and table remain unchanged for all other IDs;
A1 is restored on both branches. prepare_game_candidate.py reproduces it.
Three source tests verify valid pose boundaries, reversible one-anchor
transformation and rejection of duplicate/missing anchors.

The hidden BelowNormal/dummy-video compile succeeded in19.09 seconds
without a window. Current program lanes are now79168E97ADC85F83CAF3BE26425FC25C2B86EF572BED43E6FD53827EE1AF37FF
and B2FC2642645A9E21FD9C96E94F6A279A59FC41F77CF7AA3FD2FB17F11B818FAD.
All previous different-program reports are historical, not current gates.
Runs247/248 each reached9000 fields, two natural KOs, own victim identity,
276 native fatality-state fields and native completion, without missing
markers or Lua errors. KISS_SETUP_AUDIT.json pins the receipts and traces.
This only qualifies bounded setup smoke behavior: inflation art/palettes,
alignment, mirrored cases and original-roster controls remain open.
The staged inflation graphics are still not linked; no release promoted.

The later boundary-repair revision is assets/inflation_v3 and
generated_inflation_v3. Its two replacement Kano poses have transparent
margins; all ten unrelated indexed frames retain their prior hashes.
The viewed indexed preview has complete hands. All12 payloads round-trip
and the existing arm-rip graphics prefix is unchanged. Use this revision,
not the earlier flagged generated_inflation data, for upcoming integration.
It remains unlinked and runtime-unqualified.

## First inflation link:249/250

The corrected v3 module is now linked, with eight standard Wolf graphics
sockets. current_graphics.py and test_wolf_baseline.py select this generation.
kiss_inflate_source.py supplies own-ID guards for inflation scripts, both
palette lookups and the shared tug coordinate. Original rows remain intact;
the own -04cH tug coordinates are provisional visual calibration values.
prepare_game_candidate.py, native_module_order.txt and PBUILD.BAT include
the readable KSINFART source. Hidden compilation succeeded in26.14 seconds.

INFLATION_FIRST_LINK_AUDIT.json pins the new lanes9236BB99A082538A809BB7715071AFCEDB6C13E450622F76A12C01DF1778C3A6
and E6E21895119A0E6ECDBAF2B97E11428373C96E256F430ECAA001006A35CA47AA,
all12 compiled image headers, current graphics, stock MAME, true identities,
two natural KOs and9000 fields for each actor. Both show own inflation
phases0..4 for32,8,8,8,40 sampled fields. No pop pose is observed.

Viewed captures show correctly colored own inflated bodies but wrong
facing. Native sprite orientation must be normalized, including x origin.
The master finishes after96 fields of the victim reaction, before its pop:
victim inflation consumes32+4*8 fields; each of three shake_him_up calls
uses6 shakes with two3-field sleeps, adding108 fields before the pop.
The own reaction needs an appropriate master synchronization fix, with
original-character controls; do not mark native completion as acceptance.
No release promoted. Earlier unlinked-stage notes are historical.

## Facing and completion synchronization

The native encoder now reflects each authored left-facing image row and
its animation point together (xOffset=width-1-sourceXOffset). All12
payloads are byte-window decoded against reflected editable PGM sources;
the existing arm-rip prefix is unchanged. The bounded in-place refresh
checks old ASM, packed data, source manifest and all eight socket hashes
before writing the corrected generation. No new graphics tree was created.

The master retains its original96-field sleep and original timing for
every non-own ID. For17/18 only it then waits, at most256 one-field polls,
for the victim's native m_inviso flag after pop/white flash. It allows64
more fields for the native explosion objects before finishing. No test
health/state writes or emulator changes are involved. This bounded native
wait needs mirrored and original-character controls, not just source proof.

Hidden compilation succeeded in18.62 seconds without a window. Current
lane hashes are DACD31D08690162CC9BB0878994B77A40D6FF25BCF1F0051F430B9CFF2449FE2
and6365372583A5191BC908C349434D4468DEE84CB263E0395B6D071590E0860DF3.
Runs251/252 confirmed pop shape and invisibility;253/254 added read-only
phase/burst captures. First screenshots lagged the shape pointer, so255/256
delay phase captures three fields to observe the rendered pop itself.
Both pop captures and earlier burst30 captures were viewed. Own facing,
colors, cracked pop pose and native explosion are visible. All six own
poses occur; the pop is visible for5 fields, followed by over60 fields of
native explosion time before completion. Both runs reach9000 fields after
two natural KOs with true own IDs and no missing/illegal recovery marker.

INFLATION_RUNTIME_QUALIFICATION.json pins the current program/graphics,
all12 linked headers, stock emulator, controllers, traces and captures.
Two source/encoding unit tests pass. This is a bounded two-victim sequence
proof, not full compatibility acceptance: mirrored sides, original roster,
shared Mileena setup, final alignment/grounding and clean rebuild remain.
No release promoted.

## Mirrored and representative original-victim controls

Runs257/258 exercise Kano/Sonya as physical P1 victims of P2 Kitana,
complementing255/256. All four cases retain true IDs, win two natural
rounds and reach9000 fields with all six own poses,5 visible pop fields,
native invisibility, explosion time and completion. Mirrored pop and
burst30 screenshots were viewed; actors face Kitana on both sides.
INFLATION_RUNTIME_QUALIFICATION.json now records mirroredRuntimeControls:true.
No program or graphics changed for these tests.

Runs259/260 use actual original Liu Kang1 and Mileena5 as victims through
the physical controller's --kitkiss-control flag. Both reach9000 fields
after two natural KOs, retaining original bodies/IDs and276 fatality fields
before completion, with no missing/illegal recovery or Lua error. Their
inflation screenshots were viewed. Five original tables' typed values
match the pinned original source ZIP exactly (line numbers are excluded
from comparison). KISS_ORIGINAL_CONTROLS.json pins this limited evidence.
It is not an all-roster regression or original full-pop-sequence proof.
Mileena as victim does NOT test Mileena as attacker: the shared body-suck
setup still requires its own runtime control. Final alignment/grounding
and independent current-link rebuild also remain open. No release promoted.
