"""Exact normal-human launch response, original full native capture assertions."""
import inspect, json
from pathlib import Path
import native_cpu_mobility_capture_contract_v3036 as original
import native_cpu_human_hold_capture_contract_v3111 as hold
import current_cpu_capture_contract_v3270 as snapshots
ROOT=original.ROOT; assembly=original.assembly; need=original.need
LINKS=[["mk2ks_physical_p2_cpu_round_trace_v3101.lua","mk2ks_physical_p2_cpu_round_trace_v3290.lua","mk2ks_physical_p2_cpu_continuation_v3095.lua","mk2ks_physical_p2_cpu_continuation_v3289.lua"],["mk2ks_physical_p2_cpu_overlap_trace_v3102.lua","mk2ks_physical_p2_cpu_overlap_trace_v3291.lua","mk2ks_physical_p2_cpu_round_trace_v3101.lua","mk2ks_physical_p2_cpu_round_trace_v3290.lua"],["mk2ks_physical_p2_cpu_choice_trace_v3103.lua","mk2ks_physical_p2_cpu_choice_trace_v3292.lua","mk2ks_physical_p2_cpu_overlap_trace_v3102.lua","mk2ks_physical_p2_cpu_overlap_trace_v3291.lua"],["mk2ks_physical_p2_cpu_square_trace_v3104.lua","mk2ks_physical_p2_cpu_square_trace_v3293.lua","mk2ks_physical_p2_cpu_choice_trace_v3103.lua","mk2ks_physical_p2_cpu_choice_trace_v3292.lua"],["mk2ks_native_cpu_bicycle_display_v3105.lua","mk2ks_native_cpu_bicycle_display_v3294.lua","mk2ks_physical_p2_cpu_square_trace_v3104.lua","mk2ks_physical_p2_cpu_square_trace_v3293.lua"],["mk2ks_native_cpu_mobility_boundary_v3106.lua","mk2ks_native_cpu_mobility_boundary_v3295.lua","mk2ks_native_cpu_bicycle_display_v3105.lua","mk2ks_native_cpu_bicycle_display_v3294.lua"]]
ADDED="        if controllable and continuation=='close_on_launch' then\n            fields['P1 Block']:set_value(0)\n            local advancing=s.action==0x204 and gap>68\n            local guarding=s.action==0x204 and gap<=68\n            if advancing then fields['P1 '..(v.x<s.x and 'Right' or 'Left')]:set_value(1)end\n            if guarding then fields['P1 Block']:set_value(1)end\n            log('LAUNCH_RESPONSE',string.format('policy=%s cpu_action=%04X gap=%d advancing=%d guarding=%d',\n                continuation,s.action,gap,advancing and 1 or 0,guarding and 1 or 0))\n        end\n"

def source_contract():
    hold.input_source()
    base=(ROOT/'mk2ks_physical_p2_cpu_continuation_v3095.lua').read_text()
    expected=base.replace("or continuation=='neutral_hold','Only real","or continuation=='neutral_hold' or continuation=='close_on_launch','Only real").replace(
        "and continuation~='neutral_hold' then","and continuation~='neutral_hold' and continuation~='close_on_launch' then").replace(
        "        log('CONTINUATION_INPUT',",ADDED+"        log('CONTINUATION_INPUT',")
    need((ROOT/'mk2ks_physical_p2_cpu_continuation_v3289.lua').read_text().rstrip()==expected.rstrip(),
         'Only ordinary human buttons after a naturally selected native launch; no guest/CPU/HP/RNG writes')
    for old,new,from_path,to_path in LINKS:
        base=(ROOT/old).read_text(); needle="dofile('"+from_path+"')"
        need(base.count(needle)==1 and (ROOT/new).read_text().rstrip()==base.replace(needle,"dofile('"+to_path+"')").rstrip(),
             'Entire original native observer unchanged except explicit driver load-link')
    original.metadata_contract_source()

def capture(folder,pins):
    source_contract()
    source=inspect.getsource(original.capture)
    before="if Path(file).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)"
    after="if Path(file).suffix in('.lua','.ps1','.json'):snapshots.pin_snapshot(folder,file,wanted,pin)"
    need(source.count(before)==1,'Exactly one flat snapshot address; all other native capture assertions unchanged')
    namespace=dict(vars(original)); namespace['snapshots']=snapshots
    exec(compile(source.replace(before,after),str(Path(__file__).resolve())+'::original_capture_snapshot_address_only','exec'),namespace)
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    need(meta.get('snapshot_schema')==2 and meta['candidate']=='diagnostic_v3172_native_morph_shadow','Actually run current candidate and collision-free snapshots')
    return namespace['capture'](folder,'new','kano','guard_until_close','close_on_launch',pins)

