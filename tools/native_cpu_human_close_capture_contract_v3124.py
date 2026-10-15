"""Exact jumping/approaching human buttons; original native observers/guest."""
import json
from pathlib import Path
import native_cpu_human_hold_capture_contract_v3111 as parent
original=parent.original;assembly=original.assembly;ROOT=original.ROOT;need=original.need
rows=original.rows;ledgers=original.ledgers;square=original.square
COPIES=[["mk2ks_physical_p2_cpu_round_trace_v1998.lua","mk2ks_physical_p2_cpu_round_trace_v3114.lua","mk2ks_physical_p2_cpu_continuation_v1997.lua","mk2ks_physical_p2_cpu_continuation_v3113.lua"],["mk2ks_physical_p2_cpu_overlap_trace_v1999.lua","mk2ks_physical_p2_cpu_overlap_trace_v3115.lua","mk2ks_physical_p2_cpu_round_trace_v1998.lua","mk2ks_physical_p2_cpu_round_trace_v3114.lua"],["mk2ks_physical_p2_cpu_choice_trace_v2035.lua","mk2ks_physical_p2_cpu_choice_trace_v3116.lua","mk2ks_physical_p2_cpu_overlap_trace_v1999.lua","mk2ks_physical_p2_cpu_overlap_trace_v3115.lua"],["mk2ks_physical_p2_cpu_square_trace_v2038.lua","mk2ks_physical_p2_cpu_square_trace_v3117.lua","mk2ks_physical_p2_cpu_choice_trace_v2035.lua","mk2ks_physical_p2_cpu_choice_trace_v3116.lua"],["mk2ks_native_cpu_bicycle_display_v3024.lua","mk2ks_native_cpu_bicycle_display_v3118.lua","mk2ks_physical_p2_cpu_square_trace_v2038.lua","mk2ks_physical_p2_cpu_square_trace_v3117.lua"],["mk2ks_native_cpu_mobility_boundary_v3025.lua","mk2ks_native_cpu_mobility_boundary_v3119.lua","mk2ks_native_cpu_bicycle_display_v3024.lua","mk2ks_native_cpu_bicycle_display_v3118.lua"]]
def input_source():
    parent.input_source()
    driver=(ROOT/'mk2ks_physical_p2_cpu_continuation_v3095.lua').read_text()
    expected=driver.replace("or continuation=='neutral_hold','Only real", "or continuation=='neutral_hold' or continuation=='jump_hold' or continuation=='approach_hold','Only real").replace(
      "and continuation~='neutral_hold' then","and continuation~='neutral_hold' and continuation~='jump_hold' and continuation~='approach_hold' then").replace(
      "continuation=='jump_guard'","(continuation=='jump_guard' or continuation=='jump_hold')").replace(
      "        if controllable and continuation=='neutral_hold' then",
      "        if controllable and continuation=='approach_hold' and gap>90 then\n            fields['P1 Block']:set_value(0)\n            fields['P1 '..(v.x<s.x and 'Right' or 'Left')]:set_value(1)\n        end\n        if controllable and continuation=='neutral_hold' then")
    need((ROOT/'mk2ks_physical_p2_cpu_continuation_v3113.lua').read_text().rstrip()==expected.rstrip(),
      'Entire established human driver except normal approach/jump controls; no special/AI/state/RNG writes')
    for old,new,from_path,to_path in COPIES:
        text=(ROOT/old).read_text();needle="dofile('"+from_path+"')"
        need(text.count(needle)==1 and(ROOT/new).read_text().rstrip()==text.replace(needle,"dofile('"+to_path+"')").rstrip(),
          'Entire unchanged native observer body, declared load-link only '+new)
def capture(folder,build,player,approach,policy,pins):
    need(policy in ('jump_hold','approach_hold'),'Only source-declared ordinary human close policy')
    input_source()
    log,guest,case=original.capture(folder,build,player,approach,policy,pins)
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    required={'run_native_cpu_human_close_v3120.ps1','mk2ks_physical_p2_cpu_continuation_v3113.lua'}|{c[1]for c in COPIES}
    need(required<={Path(p).name for p in before},'Every actual physical driver/load/observer file frozen')
    runner=(folder/'input_sources/run_native_cpu_human_close_v3120.ps1').read_text()
    need('-autoboot_script "$root/mk2ks_native_cpu_mobility_boundary_v3119.lua"'in runner,'Actual top observer directly loads declared physical chain')
    return log,guest,case

