"""Entire original finite Kano gate; periodic samples are not continuous.

The native special tap reads current published actor/Main at the instruction,
independently of periodic LIVE rows. Bind each to the actually observed nearest
matching prior/following snapshot within30 fields, never the previous match.
Original failure and full unchanged source/chronology/HP/fault gate retained.
"""
import inspect
import json
from pathlib import Path
import verify_native_kano_first_three_complete_prefix as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_kano_prefix_owned_snapshot_windows_checked'


def run():
    failed_path=previous.OUT/'failure.json'
    failed=json.loads(failed_path.read_text())
    need(not failed['passed'] and failed['error']=="ValueError('All181 actual native knife instruction entries belong to current true Kano actor/Main, not merely intended inputs')",
         'Original failed periodic-snapshot assumption preserved')
    observer_path=ROOT/'mk2ks_natural_campaign_shao_knife_retreat_v3510.lua'
    observer=observer_path.read_text()
    for exact in (
        'local a,m=p:read_u32(slots[side].actor),p:read_u32(slots[side].main)',
        'if not valid(a)or not valid(m)or cpu.A8.value~=a or cpu.A13.value~=m or',
        'p:read_u16(a+0x1f0)~=identity or p:read_u16(slots[side].roster)~=identity then return end',
        'move_name,move_entry,at,cpu.PC.value,a,m,cpu.A8.value,cpu.A13.value,'):
        need(observer.count(exact)==1,'Actual full native instruction observer reads and tests current published own actor/Main')
    source=inspect.getsource(previous.fields)
    before="        prior=[l for l in live if int(l['frame'])<=int(q['frame'])][-1]"
    after="""        at=int(q['frame'])
        preceding=[l for l in live if int(l['frame'])<=at]
        following=[l for l in live if int(l['frame'])>=at]
        candidates=([preceding[-1]] if preceding else [])+([following[0]] if following else [])
        matching=[l for l in candidates if abs(int(l['frame'])-at)<=30 and l['stage']==q['stage'] and
                  l['human_actor']==q['actor'] and l['human_main']==q['main']]
        need(matching,'Actual nearest observed actor/Main snapshot within30 fields confirms current instruction-owned context')
        prior=matching[0]"""
    need(source.count(before)==1,'Exactly one whole original periodic-snapshot binding corrected')
    scope=dict(vars(previous),__file__=__file__,OUT=OUT,failed_path=failed_path,observer_path=observer_path,previous=previous)
    exec(compile(source.replace(before,after),__file__+'::entire_original_fields_with_actual_owned_snapshot_witness','exec'),scope)
    run_source=inspect.getsource(previous.run)
    old='for p in (Path(__file__),Path(capture.__file__),Path(prepared.__file__),Path(reader.__file__),Path(native_health.__file__),'
    new='for p in (failed_path,observer_path,Path(previous.__file__),Path(__file__),Path(capture.__file__),Path(prepared.__file__),Path(reader.__file__),Path(native_health.__file__),'
    need(run_source.count(old)==1,'Exactly one entire original frozen input-pin extension')
    exec(compile(run_source.replace(old,new),__file__+'::entire_original_current_Kano_progression_gate','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual successor source/snapshot gate outcome')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),fullPortAcceptance=False),indent=2)+'\n')
        raise
