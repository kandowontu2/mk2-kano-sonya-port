# Current short-table review

## Opponent-word and adjustment caller inspection

Current direct CALLA get_his_char_word callers were inspected in MKDEATH,
MKPROP and MKZAP. MKUTIL swaps both object/process to the opponent and
delegates to get_char_word, restoring them through him_rets. The spear
adjustments table has19 words (own124/124); ochar_dived_poses has19 words
(own0/0). MKDEATH's kissed_coor_adj call has explicit17/18 branches;
dizzy_wait similarly branches before its caller-provided table lookup and
uses own32*5 offset. This is source-level bounds/dataflow evidence, not
proof of visual alignment or every indirect caller.

The direct adjust_him_tbl call inspected in Jax's clap loads clapped_lineups.
The helper forwards A0 through get_his_char_long, then splits its packed
coordinate pair into X/Y. The existing linked19-pair qualification remains
the byte-level evidence for that table. No guessed table extension or ROM
change was made. Generic helpers are not universally certified by this
finite set of direct CALLA sites.

## Current6AE0 reinspection

The scanner is refreshed against current source hashes:84 helper calls,
15 short candidates,59 capacity-covered candidates and10 unresolved
nearest-load references. qualify_common_table_link.py independently checks
the current6AE0 ROM's seven named common table labels, including19-entry
getup/sweepup speeds, reaction hooks, throw speeds, anti-air distances,
fatality-distance pairs and fixed Jax-clap victim lineups. Own slots pass.
This supersedes older linked addresses/program hashes below.

Manual classification of the ten unresolved scanner references:

- MKBLOOD::gush_lineup and MKDEATH::dizzy_wait have explicit17/18 bypasses
  before the original native lookup. A missing nearby A0 load is not an
  unguarded own-ID table access in those inspected branches.
- MKDRONE::drone_getup and MKREACT::gup2 transfer their chosen A11 table
  into A0 after get_char_ani; the named getup/sweepup linked tables have
  the required19 slots. This is not blanket caller-register preservation.
- MKDRONE::ochar_do_or_rets plus MKUTIL::ochar_call, ochar_jump,
  adjust_him_tbl, get_his_char_long and get_his_char_word are six generic
  forwarders consuming caller-provided A0. They cannot be assigned one
  guessed local table or declared universally safe from this scan.

The corresponding source files matched the earlier pinned hashes during
inspection; no game source, table values or ROM bytes were changed. Generic
caller/dataflow and arbitrary manual indexing remain outside exhaustive
safety proof. Do not turn these candidate counts into release acceptance.

The refreshed `CURRENT_CHARACTER_TABLE_AUDIT.json` scans current `srcp`
sources: 80 helper calls, 15 short-table candidates, 51 capacity-covered
candidates and 14 unresolved nearest-load references. This is not an exhaustive
indexed-load or caller-reachability proof. A short table alone is not a bug.

The arm, freeze, Shang-entry, kiss, inflation, ingestion and split candidates
have explicit own-ID bypasses before the original lookup. Their original
tables intentionally remain unchanged; relevant source helpers and runtime
qualifiers must be checked instead of appending arbitrary rows.

`MKREACT.ASM::b_superkang` likewise checks IDs 17/18 and branches to
`b_superk_lite` before the short `ochar_block_superk` lookup.
`MKSLAM.ASM::do_body_slam` transfers IDs 17/18 to own throw implementations
before the original `body_slam_jumps` dispatch.

## Throw-damage candidate

`MKREACT.ASM::tossed_flight` temporarily loads the opponent object into A8
before indexing `flip_damage_table`. It therefore indexes by the **attacker**,
not the victim. The table has 17 entries. The original post-flip dispatcher
now has own-ID rows pointing to `tossed_flight`; an own attacker reaching that
path could read outside this damage table.

However, `asm/KSTHROW.ASM` uses `ks_throw_wait`/`ks_throw_release` takeover
paths, with explicit 34 damage in the release routine, and finishes through
`land_on_my_back`, not `tossed_flight`. Thus an ordinary own throw is not
shown to reach this candidate merely because the table is short. Do not
claim a reproduced damage bug or silently alter throw damage from this scan.
Remaining caller/secondary throw reachability needs a dedicated audit and
physical-control runtime tests. No game source was changed by this review.

Follow-up: current-ROM runs 309 (Kano -> Sonya) and 310 (Sonya -> Kano)
passed `qualify_own_throw.py`: 34 damage, all own owner poses, victim takeover,
recovery, 221 grounded settled observations each, and 9000 observed fields.
`audit_throw_helpers.py` now verifies the only direct executable source
reference to `do_air_body_slam` is in `MOVES.ASM::sc_block`; current block
dispatch rows select `sucide` / `ks_sonya_block` for IDs17/18, not `sc_block`.
The own throw module has no references to the native post-flip/damage path.
This narrows the ordinary/direct air-throw concern, but does not prove arbitrary
indirect, interruption or morph caller safety. No table rows were guessed.

Unresolved helper references and arbitrary manual indexing remain open even
where this candidate list has a guard. Full moves/AI/campaign and release
acceptance are not established by a table capacity scan.

## Current-source reinspection after F650

The candidate report was regenerated against current source hashes; counts
remain80 helper calls,15 short candidates,51 capacity-covered and14 unresolved.
Manual inspection identifies scanner limitations, not new game defects:
MKDRONE::def2 loads ochar_fatality_distances on an inline label;
MKDRONE::rh_ooa loads rh_air_distances similarly; MKSLAM::slam2 loads
throw_ani_speeds; MKREACT::rst0 loads rs_calls. The nearest-load regex misses
those label/instruction lines. MKREACT getup passes the chosen getup/sweepup
table through A11; MKDRONE getup likewise uses A11. Generic MKUTIL helpers
receive caller-provided A0 rather than loading their own table.

These observations explain why nearest-load resolution is incomplete, but
do not establish all caller tables or runtime safety. No guessed table rows
or gameplay changes were introduced. The report intentionally retains its
unresolved status until the scanner and caller checks are strengthened.

## Newly exposed victim-table defect: Jax head clap

The wrapper inventory now includes adjust_him_tbl (MKUTIL selects the
victim via get_his_char_long) and ochar_do_or_rets (MKDRONE dispatches via
get_char_long). Five lexical/wrapper regression tests pass. The current
report now has84 helper calls,16 short candidates,58 capacity-covered
candidates and10 unresolved references. These are not exhaustive counts.

The newly exposed MKDEATH::do_clap call at1939 loads clapped_lineups at1938.
The table at1967 has16 pairs of16-bit words =512 bits, hence16 entries
at the actual32-bit victim stride. get_his_char_long changes A8 to the
other actor and get_char_long indexes ochar<<5 without an ID bound.
There is no own-victim guard in this call sequence. IDs17/18 therefore
read beyond this table when used as Jax head-clap victims; ID16 is also
outside its declared capacity. The next executable label do_tongue begins
immediately after the16 rows (local listing offsets e850→ea50).

This is a concrete static bounds defect, not a reproduced runtime crash.
No offsets have been guessed or native source changed in this review.
The fix needs explicit native victim entries derived from the own pose
alignment, followed by linked bounds/value checks and physically earned
Jax-fatality tests with Kano/Sonya victims. Until then, full victim safety
and release completion remain unproven even though their own finishers
have separate finite tests. No MAME process or compilation was launched.

## Inline-label scanner correction

instruction_code now preserves GSPA column-zero label semantics, removes
inline labels before scanning instructions and ignores comments/DOS EOF.
Four lexical regression tests cover inline MOVI/CALLA, colon labels,
indented instructions, bare labels/comments and mixed code/table labels.
The current report now finds83 helper calls,15 short candidates,58
capacity-covered candidates and10 unresolved references. No previously
short candidate disappeared. Three newly detected calls are MKGUYS::pnorm2,
MKSEL::psda and MOVES::fat4. Counts remain candidate evidence, not safety.

Manual inspection confirms19 slots in ochar_fatality_distances (two words
per character, hence32-bit stride), rh_air_distances (16-bit stride),
throw_ani_speeds (16-bit stride) and rs_calls (32-bit stride). Own fatality
distance pairs are040h/0c0h for Kano and0c0h/0e0h for Sonya. Own anti-air
distances are040h, throw animation rates4, and reaction hooks0. Zero hooks
mean the native helper returns without a special boss reaction. These
entries were already present: the correction changes no native source or
ROM. The10 remaining unresolved candidates and arbitrary indexing still
need caller/dataflow coverage.53 source/tooling tests pass; full gameplay,
campaign and release acceptance remain unproven.

## Linked common-table bounds check

qualify_common_table_link.py passes against programF65002019A05D47400BD755B95C06546B9ADD104140472A111F1D107C3F6D512.
It reconstructs the interleaved program and resolves private tables using
current module listings plus linked global anchors, with bit-address bounds.
The shared getup/sweepup table is atff8cf580, has19 words, and own entries
17/18 are4. All19 values are checked, including Raiden's original2. Reaction
hooks atff8be2a0 have zero own entries; throw speeds atff89feb0 have4/4;
anti-air distances atff90e580 are040h for all19; fatality-distance pairs at
ff903490 contain the expected two-word own entries.

The get-up source paths choose getup_speeds/sweepup_speeds in A11, and
MKREACT transfers A11 to A0 after get_char_ani. That animation helper uses
A0/A9/A14, not A11. MKDRONE's getup path similarly transfers the inherited
A11 after selecting animation12h. This is finite source/data inspection,
not proof of every caller's register preservation or every runtime get-up.
The generic MKUTIL wrappers still take their tables from callers, so they
cannot be marked safe by assigning one guessed nearest load. MKBLOOD and
MKDEATH own-ID guards bypass their flagged original lookups as previously
reviewed. No game code or ROM bytes were changed by this verification.
