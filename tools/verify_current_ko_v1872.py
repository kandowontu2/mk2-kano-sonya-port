"""Current native blade/bicycle repeated KO and following-round integration.

Both moves, both slots and both new victims, plus original Kitana/Sub-Zero
references. Actual full-health cold matches and naturally earned first KOs.
The original independent per-field v824/v2 lifecycle contract is unchanged.
Not every victim, move, arena, match transition, CPU, full raster or audio.
"""
import json
import verify_current_interrupt_v1870 as launch
from verify_current_lifecycle_v2 import verify,rows

ROOT=launch.ROOT
OUT=ROOT/'audit_v1872_current_ko_checked'
CASES=[(move,side,victim)for move in ('blade','bicycle')for side in (1,2)for victim in ('kano','sonya')]
CASES+=[('blade',2,'kitana'),('bicycle',2,'sub_zero')]

def check():
    pins=launch.source_pins();cases=[]
    for move,side,victim in CASES:
        folder=ROOT/f'audit_v1871_ko_{move}_p{side}_{victim}'
        meta=launch.matched(folder,pins)
        assert (meta['move'],meta['side'],meta['victim'])==(move,side,victim)
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        proof=verify(log,move,side,victim)
        assert proof['passed'],'Unchanged full native lifecycle contract: '+str(proof['errors'])
        assert all(event['pc']==0xff835480 for event in rows(log,'EVENT')if event['kind']=='strike')
        cases.append(proof)
        print(f'{move} p{side} vs {victim}: {proof["cycles"]} native cycles, earned KO and following-round move passed',flush=True)
    launch.module_pins(pins)
    return dict(passed=True,candidate=launch.NAME,cases=cases,actualFields=sum(case['actual_fields']for case in cases),
                originalPerFieldAcceptanceUnchanged=True,gameBytesChanged=False,inputHashes=pins,
                allKOPathsAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:report=check()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Current KO verification passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed']else 1)
