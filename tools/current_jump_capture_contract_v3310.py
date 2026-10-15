"""Whole original native capture checks, exact ordinary forward-jump adaptation."""
import inspect
import json
import re
from pathlib import Path
import current_launch_capture_contract_v3298 as base
ROOT=base.ROOT; assembly=base.assembly; need=base.need; original=base.original
LINKS=[
 ('mk2ks_physical_p2_cpu_round_trace_v3290.lua','mk2ks_physical_p2_cpu_round_trace_v3301.lua','mk2ks_physical_p2_cpu_continuation_v3289.lua','mk2ks_physical_p2_cpu_continuation_v3300.lua'),
 ('mk2ks_physical_p2_cpu_overlap_trace_v3291.lua','mk2ks_physical_p2_cpu_overlap_trace_v3302.lua','mk2ks_physical_p2_cpu_round_trace_v3290.lua','mk2ks_physical_p2_cpu_round_trace_v3301.lua'),
 ('mk2ks_physical_p2_cpu_choice_trace_v3292.lua','mk2ks_physical_p2_cpu_choice_trace_v3303.lua','mk2ks_physical_p2_cpu_overlap_trace_v3291.lua','mk2ks_physical_p2_cpu_overlap_trace_v3302.lua'),
 ('mk2ks_physical_p2_cpu_square_trace_v3293.lua','mk2ks_physical_p2_cpu_square_trace_v3304.lua','mk2ks_physical_p2_cpu_choice_trace_v3292.lua','mk2ks_physical_p2_cpu_choice_trace_v3303.lua'),
 ('mk2ks_native_cpu_bicycle_display_v3294.lua','mk2ks_native_cpu_bicycle_display_v3305.lua','mk2ks_physical_p2_cpu_square_trace_v3293.lua','mk2ks_physical_p2_cpu_square_trace_v3304.lua'),
 ('mk2ks_native_cpu_mobility_boundary_v3295.lua','mk2ks_native_cpu_mobility_boundary_v3306.lua','mk2ks_native_cpu_bicycle_display_v3294.lua','mk2ks_native_cpu_bicycle_display_v3305.lua'),
]

def source_contract():
    base.source_contract()
    source=(ROOT/'mk2ks_physical_p2_cpu_continuation_v3289.lua').read_text().replace('close_on_launch','jump_on_launch')
    before="if advancing then fields['P1 '..(v.x<s.x and 'Right' or 'Left')]:set_value(1)end"
    after="if advancing then fields['P1 Up']:set_value(1);fields['P1 '..(v.x<s.x and 'Right' or 'Left')]:set_value(1)end"
    need(source.count(before)==1 and (ROOT/'mk2ks_physical_p2_cpu_continuation_v3300.lua').read_text().rstrip()==source.replace(before,after).rstrip(),
         'Only ordinary human Up plus forward after a naturally selected CPU launch')
    for old,new,from_path,to_path in LINKS:
        source=(ROOT/old).read_text(); needle="dofile('"+from_path+"')"
        need(source.count(needle)==1 and (ROOT/new).read_text().rstrip()==source.replace(needle,"dofile('"+to_path+"')").rstrip(),
             'Whole original observer unchanged except explicit human-driver load-link')

def responses(log):
    result=[]
    wanted={'frame','cycle','policy','cpu_action','gap','advancing','guarding','cpu_slot','human_slot','writes','assistance'}
    for line in log.splitlines():
        if not line.startswith('MK2_CPU_PAIR_LAUNCH_RESPONSE '):continue
        fields=re.findall(r'(\w+)=([^\s]+)',line)
        need(len(fields)==len(wanted) and {k for k,v in fields}==wanted,'Exact unambiguous launch-response schema')
        result.append({k:v if k in {'policy','assistance'} else int(v,16 if k=='cpu_action' else 10) for k,v in fields})
    return result

def capture(folder,pins):
    source_contract()
    source=inspect.getsource(original.capture)
    before="if Path(file).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)"
    after="if Path(file).suffix in('.lua','.ps1','.json'):snapshots.pin_snapshot(folder,file,wanted,pin)"
    need(source.count(before)==1,'Only snapshot address adapts in entire original source/state/HP capture contract')
    namespace=dict(vars(original)); namespace['snapshots']=base.snapshots
    exec(compile(source.replace(before,after),str(Path(__file__).resolve())+'::original_capture_snapshot_address_only','exec'),namespace)
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    need(meta.get('snapshot_schema')==2 and meta['candidate']=='diagnostic_v3172_native_morph_shadow','Current real matched candidate and collision-free snapshots')
    return namespace['capture'](folder,'new','kano','guard_until_close','jump_on_launch',pins)
