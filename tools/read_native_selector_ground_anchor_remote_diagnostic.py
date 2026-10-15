"""Preserve failed all-state floor assertion; expose bounded actual exceptions."""
from pathlib import Path
root=Path('C:/Users/kando/Documents/Codex/2026-08-29/i-ha/work/mk2port')
source=(root/'tools/read_native_selector_ground_anchor_remote.py').read_text()
source=source.replace("fields=sys.modules['__main__'].control_fields",
    "fields=sys.modules['qualify_native_selector_fresh_lowkick_controls'].ledger.original.pair.rows(prepared.RAM_CASES[prepared.SCOPE['KEY']][1],'FIELD')",1)
old="""        for r in fields:
            assert (r['vid'],r['id'])==(17,18)
            assert r['vfloor']+table[r['vid']]==r['stage_floor']
            assert r['floor']+table[r['id']]==r['stage_floor']"""
new="""        exceptions=[]
        for r in fields:
            assert (r['vid'],r['id'])==(17,18)
            for slot,prefix in ((1,'v'),(2,'')):
                floor=r['vfloor'] if slot==1 else r['floor']
                identity=r['vid'] if slot==1 else r['id']
                if floor+table[identity]!=r['stage_floor']:
                    exceptions.append(dict(frame=r['frame'],slot=slot,floor=floor,stageFloor=r['stage_floor'],
                        action=r['vaction'] if slot==1 else r['action'],y=r['vypos'] if slot==1 else r['y'],
                        body=r['vbody'] if slot==1 else r['body'],flags=r['vflags'] if slot==1 else r['flags']))
        answer.update(actualAnchorExceptions=len(exceptions),firstActualExceptions=exceptions[:8])"""
assert source.count(old)==1;source=source.replace(old,new,1)
source=source.replace('bothPhysicalFloorAnchorsAgreeWithStageBaseline=True','bothPhysicalFloorAnchorsAgreeWithStageBaseline=not exceptions')
exec(compile(source,str(root/'tools/read_native_selector_ground_anchor_remote_diagnostic.py')+'::bounded_actual_exceptions','exec'))
