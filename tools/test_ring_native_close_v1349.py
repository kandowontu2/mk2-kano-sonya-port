"""Reject actual earlier close misses and in-memory palette corruptions."""
import copy,json
from pathlib import Path
import numpy as np
import verify_ring_interrupt_display_v1346 as v
ROOT=v.ROOT;OUT=ROOT/'audit_v1349_ring_native_close_counterexamples'

def verify():
    pins={};checks=[];baselines=[];guest,_,_,_=v.current.reconstruct()
    def pin(path,wanted=None):
        path=Path(path);key=str(path);actual=pins.get(key)or v.current.digest(path)
        assert wanted is None or wanted==actual,'Changed evidence '+key;pins[key]=actual
    def reject(label,call):
        try:call()
        except (AssertionError,ValueError) as error:checks.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise AssertionError('Invalid close-contact/palette evidence accepted: '+label)
    for side in(1,2):
        proof_path=ROOT/f'audit_v1346_ring_interrupt_p{side}_render_checked/report.json'
        proof=json.loads(proof_path.read_text());assert proof['passed']and proof['candidate']==v.current.CANDIDATE;pin(proof_path)
        for file,wanted in proof['inputHashes'].items():pin(file,wanted)
        folder=ROOT/f'audit_v1341_ring_interrupt_p{side}';log=(folder/'run.log').read_text(encoding='utf-8-sig')
        state=v.interrupted_state(log,side);assert state['retryContact']['after']==139 and state['ordinaryFollowupContact']['after']==128
        baselines.append(dict(side=side,closeRingDamage=22,ordinaryFollowupDamage=11))
        for version in(1316,1324,1330):
            old=ROOT/f'audit_v{version}_ring_interrupt_p{side}/run.log';pin(old)
            reject(f'actual_v{version}_close_ring_miss_p{side}',lambda old=old,side=side:v.interrupted_state(old.read_text(encoding='utf-8-sig'),side))
        groups,*_=v.raster.data(folder)
        charge=next(q for q in groups['FLOOR_QUEUE']if q['slot']==side and q['pose']in v.current.CHARGE_POSES)
        display=next(q for q in groups['FLOOR_DISPLAY']if q['frame']==charge['frame']+1)
        actual=np.fromfile(folder/display['palette_file'],dtype='<u4');v.current.check_charge_palette(charge,actual)
        for key,value in(('id',1),('roster',1),('slot',3),('bank',0)):
            changed=copy.deepcopy(charge);changed[key]=value
            reject(f'charge_{key}_p{side}',lambda changed=changed:v.current.check_charge_palette(changed,actual))
        for pen in(1,63):
            changed=actual.copy();changed[(charge['bank']&0x7f00)+pen]^=0xffffff
            reject(f'charge_wrong_pen_{pen}_p{side}',lambda changed=changed:v.current.check_charge_palette(charge,changed))
        normal=next(q for q in groups['FLOOR_QUEUE']if q['slot']==side and q['frame']>state['hit']+4 and q['frame']<state['entry']and q['pose']not in v.current.CHARGE_POSES)
        display=next(q for q in groups['FLOOR_DISPLAY']if q['frame']==normal['frame']+1)
        actual=np.fromfile(folder/display['palette_file'],dtype='<u4');v.check_owned_body_palette(normal,actual,guest,(18,18),side)
        bad=actual.copy();bad[normal['bank']&0x7f00]^=0xffffff
        reject(f'wrong_restored_costume_palette_p{side}',lambda:v.check_owned_body_palette(normal,bad,guest,(18,18),side))
    for file,wanted in pins.items():assert v.current.digest(file)==wanted,'Counter test changed actual evidence'
    pin(Path(__file__))
    pin(ROOT/'tools/test_ring_native_close_v1347.py');pin(ROOT/'audit_v1347_ring_native_close_counterexamples/report.json')
    return dict(passed=True,candidate=v.current.CANDIDATE,baselines=baselines,counterexamples=checks,count=len(checks),actualArtifactsUnchanged=True,inMemoryOnly=True,inputHashes=pins,fullPortAccepted=False)

if __name__=='__main__':
    assert not OUT.exists()
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Actual old close misses/palette counterexamples passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed']else 1)
