"""Bind fresh actual lifecycle observations to byte-identical MKII helpers."""
import json
from pathlib import Path
import verify_human_projectile_display_v1293 as hit
import verify_human_projectile_negative_display_v1297 as defense
ROOT=hit.ROOT;OUT=ROOT/'audit_v1298_projectile_native_library_checked'
REGIONS=((0xff8b5d20,0xff8b5fc0),(0xff8b6450,0xff8b6830),(0xff8b6820,0xff8b68c0))

def verify():
    pins={};cases=[];source=ROOT/'mk2/mk2-maincpu.bin';original=source.read_bytes()
    pins[str(source)]=hit.current.digest(source)
    for move in('knife','ring'):
        for side in(1,2):
            for scenario in('hit','block','miss'):
                version=1293 if scenario=='hit'else 1297
                suffix=f'{move}_p{side}'if scenario=='hit'else f'{move}_{scenario}_p{side}'
                path=ROOT/f'audit_v{version}_projectile_{suffix}_render_checked/report.json'
                proof=json.loads(path.read_text());assert proof['passed']and proof['candidate']==hit.current.CANDIDATE
                pins[str(path)]=hit.current.digest(path)
                folder=ROOT/f'audit_v{1291 if scenario=="hit"else 1296}_projectile_{suffix}'
                guest_path=folder/'guest_maincpu.bin';guest=guest_path.read_bytes();pins[str(guest_path)]=hit.current.digest(guest_path)
                code=[]
                for start,end in REGIONS:
                    first,last=(start-0xff800000)//8,(end-0xff800000)//8
                    assert guest[first:last]==original[first:last],'Changed original MKII scheduler/allocation/cleanup helper'
                    code.append(dict(start=f'{start:08X}',end=f'{end:08X}',bytes=last-first))
                assert proof['allocation']['entry']==0xff8b6530 and proof['spawn']['entry']==0xff8b5fb0 and proof['retirement']['entry']==0xff8b6820
                assert proof['retirement']['frame']<proof['replayed']['records'][-1]['frame']
                assert proof['publicationInventory']['postCleanup']>0
                cases.append(dict(move=move,side=side,scenario=scenario,code=code,cleanup=proof['retirement']['frame']))
    pins[str(Path(__file__))]=hit.current.digest(__file__)
    return dict(passed=True,candidate=hit.current.CANDIDATE,cases=cases,inputHashes=pins,
        currentProjectileSchedulerAllocationCleanupNative=True,fullPortAccepted=False)

if __name__=='__main__':
    assert not OUT.exists()
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Native projectile helper/source binding passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed']else 1)
