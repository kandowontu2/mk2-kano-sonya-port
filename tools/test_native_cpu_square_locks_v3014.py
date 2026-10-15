"""Actual captured Square/startup corruptions, never rewriting raw captures."""
import json,traceback
from pathlib import Path
import verify_native_cpu_square_locks_v3008 as model
from test_current_cpu_overlap_v1912 import mutate

ROOT=model.ROOT;OUT=ROOT/'audit_v3015_native_cpu_square_locks_units';need=model.need

def verify():
    proof_path=model.OUT/'report.json';proof=json.loads(proof_path.read_text())
    need(proof['passed']and proof['actualInitialEntryStoresCaptured']and not proof['fullPortAcceptance'],'Actual initial-write and miss-phase proof required')
    pins=dict(proof['inputHashes']);pins[str(proof_path)]=model.inventory.assembly.sha(proof_path);results=[]
    for key,case in proof['cases'].items():
        folder=ROOT/case['case'];log=(folder/'run.log').read_text(encoding='utf-8-sig');guest=(folder/'guest_maincpu.bin').read_bytes()
        start,ready,land=(case['phase'][k]for k in('start','ready','landing'));player=case['player']
        P='MK2_CPU_PAIR_';B='MK2_SQUARE_BOUNDARY_';L='MK2_SQUARE_LOCK_'
        tests=[
          ('missing CPU entry snapshot',B+'ENTRY_STATE',{'slot':'2'},None,None,'phase'),
          ('proxy CPU entry',B+'ENTRY_STATE',{'slot':'2'},'id','1','boundary'),
          ('wrong human entry owner',B+'ENTRY_STATE',{'slot':'1'},'owner','010350A0','boundary'),
          ('entry CPU detached Main',B+'ENTRY_STATE',{'slot':'2'},'main','01068EA0','boundary'),
          ('entry unrecorded action',B+'ENTRY_STATE',{'slot':'2'},'action','0207','phase'),
          ('missing initial action writer',L+'FLAG',{'frame':str(start),'slot':'2','kind':'action'},None,None,'phase'),
          ('wrong initial body writer',L+'FLAG',{'frame':str(start),'slot':'2','kind':'body'},'op0','0000','phase'),
          ('partial initial flag mask',L+'FLAG',{'frame':str(start),'slot':'2','kind':'flags'},'mask','00FF','phase'),
          ('wrong initial flag target',L+'FLAG',{'frame':str(start),'slot':'2','kind':'flags'},'at','01060220','phase'),
          ('wrong initial lock before',L+'FLAG',{'frame':str(start),'slot':'2','kind':'flags'},'before','0001','phase'),
          ('wrong initial CPU owner',L+'FLAG',{'frame':str(start),'slot':'2','kind':'body'},'owner','01034E90','phase'),
          ('missing rise callback',P+'FIELD',{'frame':str(start+4)},None,None,'phase'),
          ('wrong rise integration',P+'FIELD',{'frame':str(start+4)},'yraw','00510000','phase'),
          ('wrong actual flight pose',P+'FIELD',{'frame':str(start+14)},'pose','FF031340','phase'),
          ('wrong flight velocity',P+'FIELD',{'frame':str(start+14)},'vx','00000000','phase'),
          ('wrong falling gravity',P+'FIELD',{'frame':str(start+38)},'gravity','00000000','phase'),
          ('wrong landing callback',P+'FIELD',{'frame':str(land+1)},'yraw','00520000','phase'),
          ('retained ready lock','MK2_CPU_OVERLAP_EVENT',{'frame':str(ready),'kind':'regain','id':'18','a8':f"{case['squareBoundaries'][0]['entryStates'][1]['actor']:08X}"},'flags','0010','phase'),
          ('missing ready clear',L+'FLAG',{'frame':str(ready),'slot':'2','kind':'flags','before':'0010'},None,None,'phase'),
          ('wrong physical CPU role',P+'FIELD',{'frame':str(start+20)},'cpu_slot','1','phase'),
          ('wrong true victim ID',P+'FIELD',{'frame':str(start+20)},'vid','1','phase'),
          ('wrong floor height',P+'FIELD',{'frame':str(start+20)},'floor','82','phase'),
          ('assisted state',P+'FIELD',{'frame':str(start+20)},'writes','1','phase'),
          ('missing actual collision',B+'EVENT',{'frame':str(start+15),'kind':'collision_return'},None,None,'boundary'),
          ('fake collision carry',B+'EVENT',{'frame':str(start+15),'kind':'collision_return'},'carry','1','boundary'),
          ('wrong source collision opcode',B+'EVENT',{'frame':str(start+15),'kind':'collision_return'},'opcode','0000','boundary'),
          ('wrong remaining collision checks',B+'EVENT',{'frame':str(start+15),'kind':'collision_return'},'a11','0000001A','boundary'),
          ('fake hit entry',B+'EVENT',{'frame':str(start+15),'kind':'collision_return'},'kind','hit_entry','boundary'),
        ]
        for label,tag,criteria,column,value,contract in tests:
            changed=mutate(log,tag,criteria,column,value);need(changed!=log,'Nonvacuous actual mutation '+label)
            try:
                if contract=='phase':model.phase.verify(changed,guest,player)
                else:model.inventory.boundary(changed,guest,player)
            except (AssertionError,ValueError,KeyError,StopIteration)as error:
                results.append(dict(case=key,name=label,rejected=True,contract=contract,error=repr(error)))
            else:raise ValueError('Accepted actual corrupt Square evidence '+key+': '+label)
        need(model.phase.verify(log,guest,player)==case['phase'],'Untouched actual source-bound phase proof still passes')
        need(model.inventory.boundary(log,guest,player)==case['squareBoundaries'],'Untouched actual native collision boundary still passes')
        print(key+': '+str(len(tests))+' actual startup/phase/collision corruptions rejected',flush=True)
    for file,wanted in pins.items():need(model.inventory.assembly.sha(file)==wanted,'Captured Square evidence never modified '+file)
    pins[str(Path(__file__).resolve())]=model.inventory.assembly.sha(__file__)
    return dict(passed=True,actualPhysicalFixtures=2,actualCounterexamplesRejected=len(results),counterexamples=results,
      actualCapturesUnmodified=True,allCPUOrHitOrArtAudioAccepted=False,gameChanged=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual Square counterexamples')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','counterexamples')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
