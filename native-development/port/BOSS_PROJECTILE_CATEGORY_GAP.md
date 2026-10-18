# Boss projectile classification gap

audit_boss_action_categories.py confirms the working MKBOSS.ASM is unchanged
from the supplied original source ZIP. Kintaro and Shao Kahn extract the action
high byte, then index their9-entry category dispatch tables. Their category0
route handles projectiles, category1 stationary attacks, category2 propulsion.

Current Knife/Ring entry tags0211/0212 are unique port states, but their high
byte incorrectly dispatches these projectile launches to boss propulsion
counters. BOSS_ACTION_CATEGORY_AUDIT.json records exact source hash, entry tags
and route labels. This is a source-path mismatch; boss runtime is not exercised
or accepted by this audit. It does not explain the human controller's Jax losses.

Required correction: native classification for own projectile entries before
these category lookups, preserving original character states, true IDs and
original boss counter tables. Do not weaken boss AI or substitute character IDs.
Keep raw action tags stable for existing move lifecycle consumers unless a full
caller migration is deliberately audited. Original-state fallthrough and exact
own identity checks need tests, followed by assembly/link/runtime validation.
The current development package remains unfinished; no release promotion.

Native source correction implemented: boss_category_source.py replaces only
the two boss category-extraction instructions with a local identity-checked
helper. (Kano17,0211)/(Sonya18,0212) return category0; every other identity/tag
falls through to the original high-byte extraction. A0 is saved/restored; no
process action or character ID is written. Original boss counter tables are
unchanged. prepare_game_candidate regenerates the patch from canonical input;
stage_boss_categories verifies the old source before staging one file.

test_boss_categories.py checks preservation of every original typed table and
interprets the actual authored helper's small instruction subset for43776
identity/action combinations, checking stack/register restoration. Only the
two intended pairs differ from original category extraction. This is a host
source-level interpreter test, not target-machine or boss gameplay proof.
Working hidden compile exits0 in24.73s, no window. Source audit now matches
the canonical transformation and routes both entries to projectile counters.
Clean rebuild, compiled-helper validation and actual boss runtime remain open;
the existing development package predates this classification correction.

Compiled instruction audit now passes. qualify_boss_category_link.py scans the
actual interleaved program ROM for CALLR encoding/relative targets and finds
exactly two calls to FF922650 (FF91D7B0/FF9213D0). The pinned helper slice is
disassembled by the local TMS34010 tool: exact211/212 action checks, true17/18
identity checks, CLR category returns, original SRL8 fallback and A0 push/restore
are present. Its first assertion expected MMTM for the push macro; actual GSPA
emits equivalent MOVE A0,-*SP,1, which is now checked explicitly. No runtime
execution claim is made from disassembly. Source interpreter tests still pass.

Independent clean inputs verified;134 hash-pinned generated files2912360bytes
removed without touching source/rebuild inputs. Only MKBOSS.ASM regenerated;
hidden clean compile is running.411's ordinary projectile regression passes
19activations each,22hit/5block damage, own art, recovery and cleanup. It does
not execute boss classification. Full boss/ending/campaign acceptance remains
open; no ZIP/public release update yet.

Clean compilation exits0 in72.17s, no window. All129 fresh objects/four program
parts compare byte-identical to working, and all26 rebuilt/copied chips match
the actual411 stock-MAME input. Compiled/source/rebuild gates now pass for the
classification fix; actual boss execution is still unverified.

Common-dispatch follow-up supersedes any inference that the helper alone fixes
boss behavior: drone_beware performs a raw action-category/low-byte lookup before
its final Kintaro/Kahn branches. counter_propell has15 entries, while Knife211,
Ring212, Choke216/217 and Leg219/21a exceed that table. Reads can reach the next
table, with no valid own reaction contract; a zero result returns before either
boss helper executes. CPU_ACTION_LOOKUP_AUDIT.json records exact current bounds.
This explains why compiled/source classifier checks are not boss acceptance.

Next correction must add identity-checked common reaction dispatch for own
actions, preserving original tables/counter policies and stored action tags.
Projectile reactions must retain own repeat-history identity, not borrow another
fighter's action ID; valid paired/recovery behavior needs explicit routes.
The current ZIP/ROM remain development-only; the common AI gap is not fixed yet.

Common lookup implementation: cpu_action_source.py adds true17/18 sparse
action/reaction records before the original raw lookup, with an explicit
handled/not-owned return. Original tables and p_otheract history write remain
unchanged. Own projectile/body/grab handlers reload the actual action before
react_jump_table, preserving native repeat/difficulty decisions. Paired victim/
hold states explicitly skip countering; own recovery uses native sitting-duck
policy/sweep logic. Jade's original projectile exception is retained.

Initial build412 failed at4442 with illegal-opcode recovery and is retained as
failed evidence. The first table terminator usedFFFF while a signed word read
could yieldFFFFFFFF; the positive immediate comparison could miss it. Tables
and scan now use zero (action0 already returns before this lookup). A source
regression checks both zero terminators and the comparison. Four source tests
pass, preserving original typed rows. Hidden corrected compile exits0 in23.01s,
no window. This fix is not yet independently rebuilt or fully machine-audited.

Corrected413 completes13541 observed fields, Baraka2-0/Reptile2-0, then loses to
Jax. The full current ROM/identity/no-missing/no-recovery/no-Lua-error audit
passes, including Ring and paired Leg actions. This is bounded genuine CPU
runtime with changed reactions, not exhaustive lookup semantics or bosses.
The current developer ZIP predates both new dispatch changes and is historical.
