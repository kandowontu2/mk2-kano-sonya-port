"""Exact ordinary-human-button extensions and unchanged native observations."""
from pathlib import Path
import native_cpu_mobility_capture_contract_v3036 as original
assembly=original.assembly;ROOT=original.ROOT;need=original.need
rows=original.rows;ledgers=original.ledgers;square=original.square
COPIES=[
 ('mk2ks_physical_p2_cpu_round_trace_v1998.lua','mk2ks_physical_p2_cpu_round_trace_v3101.lua','mk2ks_physical_p2_cpu_continuation_v1997.lua','mk2ks_physical_p2_cpu_continuation_v3095.lua'),
 ('mk2ks_physical_p2_cpu_overlap_trace_v1999.lua','mk2ks_physical_p2_cpu_overlap_trace_v3102.lua','mk2ks_physical_p2_cpu_round_trace_v1998.lua','mk2ks_physical_p2_cpu_round_trace_v3101.lua'),
 ('mk2ks_physical_p2_cpu_choice_trace_v2035.lua','mk2ks_physical_p2_cpu_choice_trace_v3103.lua','mk2ks_physical_p2_cpu_overlap_trace_v1999.lua','mk2ks_physical_p2_cpu_overlap_trace_v3102.lua'),
 ('mk2ks_physical_p2_cpu_square_trace_v2038.lua','mk2ks_physical_p2_cpu_square_trace_v3104.lua','mk2ks_physical_p2_cpu_choice_trace_v2035.lua','mk2ks_physical_p2_cpu_choice_trace_v3103.lua'),
 ('mk2ks_native_cpu_bicycle_display_v3024.lua','mk2ks_native_cpu_bicycle_display_v3105.lua','mk2ks_physical_p2_cpu_square_trace_v2038.lua','mk2ks_physical_p2_cpu_square_trace_v3104.lua'),
 ('mk2ks_native_cpu_mobility_boundary_v3025.lua','mk2ks_native_cpu_mobility_boundary_v3106.lua','mk2ks_native_cpu_bicycle_display_v3024.lua','mk2ks_native_cpu_bicycle_display_v3105.lua'),
]
def input_source():
    original.metadata_contract_source()
    driver=(ROOT/'mk2ks_physical_p2_cpu_continuation_v1997.lua').read_text()
    expected=driver.replace(
      "assert(continuation=='retreat' or continuation=='jump_guard','Only real human continuation buttons')",
      "assert(continuation=='retreat' or continuation=='jump_guard' or continuation=='guard_hold' or continuation=='neutral_hold','Only real human continuation buttons')").replace(
      "        if controllable and gap<220 then",
      "        if controllable and gap<220 and continuation~='guard_hold' and continuation~='neutral_hold' then").replace(
      "        log('CONTINUATION_INPUT',",
      "        if controllable and continuation=='neutral_hold' then fields['P1 Block']:set_value(0)end\n        log('CONTINUATION_INPUT',")
    need((ROOT/'mk2ks_physical_p2_cpu_continuation_v3095.lua').read_text().rstrip()==expected.rstrip(),
      'Whole original driver retained except allowlist and only ordinary human standing/neutral buttons after recovery')
    for old,new,from_path,to_path in COPIES:
        text=(ROOT/old).read_text();needle="dofile('"+from_path+"')"
        need(text.count(needle)==1 and(ROOT/new).read_text().rstrip()==text.replace(needle,"dofile('"+to_path+"')").rstrip(),
          'Entire unchanged native observer body, only declared load-link '+new)
def capture(folder,build,player,approach,policy,pins):
    need(policy in ('guard_hold','neutral_hold'),'Only source-declared ordinary human hold policy')
    input_source()
    log,guest,case=original.capture(folder,build,player,approach,policy,pins)
    before=__import__('json').loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    required={'run_native_cpu_human_hold_v3107.ps1','mk2ks_physical_p2_cpu_continuation_v3095.lua'}|{c[1]for c in COPIES}
    need(required<={Path(p).name for p in before},'Every actual extended physical driver/load/observer file frozen')
    runner=(folder/'input_sources/run_native_cpu_human_hold_v3107.ps1').read_text()
    need('-autoboot_script "$root/mk2ks_native_cpu_mobility_boundary_v3106.lua"'in runner,'Actual top observer directly loads the declared chain, no global wrapper redirection')
    return log,guest,case
