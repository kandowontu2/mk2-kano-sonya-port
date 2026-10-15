"""Real Square contact/startup/attacker/victim corruptions, captures untouched."""
import json,traceback
from pathlib import Path
import verify_native_cpu_square_hit_v3040 as model
from test_current_cpu_overlap_v1912 import mutate

ROOT=model.ROOT;OUT=ROOT/'audit_v3043_native_cpu_square_hit_units';need=model.need

def verify():
    path=model.OUT/'report.json';proof=json.loads(path.read_text());need(proof['passed']and not proof['fullPortAcceptance'],'Actual native CPU contact proof')
    pins=dict(proof['inputHashes']);pins[str(path)]=model.inventory.assembly.sha(path)
    case=proof['cases']['new_kano'];folder=ROOT/case['case'];log=(folder/'run.log').read_text(encoding='utf-8-sig');guest=(folder/'guest_maincpu.bin').read_bytes()
    start,hit,ready,land,vland,vclear,vready=(case['phase'][k]for k in('start','hit','ready','landing','victimLanding','victimHurtClear','victimReady'))
    P='MK2_CPU_PAIR_';B='MK2_SQUARE_BOUNDARY_';L='MK2_SQUARE_LOCK_';O='MK2_CPU_OVERLAP_';results=[]
    tests=[
      ('missing actual CPU initial snapshot',B+'ENTRY_STATE',{'slot':'2'},None,None),
      ('proxy native CPU initial ID',B+'ENTRY_STATE',{'slot':'2'},'id','1'),
      ('wrong physical human role',B+'ENTRY_STATE',{'slot':'1'},'state','0'),
      ('missing initial action write',L+'FLAG',{'frame':str(start),'slot':'2','kind':'action'},None,None),
      ('partial initial body mask',L+'FLAG',{'frame':str(start),'slot':'2','kind':'body'},'mask','00FF'),
      ('wrong initial flag opcode',L+'FLAG',{'frame':str(start),'slot':'2','kind':'flags'},'op0','0000'),
      ('wrong initial CPU owner',L+'FLAG',{'frame':str(start),'slot':'2','kind':'body'},'owner','01034E90'),
      ('missing native first collision',B+'EVENT',{'kind':'collision_return'},None,None),
      ('fake miss carry',B+'EVENT',{'kind':'collision_return'},'carry','0'),
      ('false collision countdown',B+'EVENT',{'kind':'collision_return'},'a11','00000019'),
      ('wrong hit continuation opcode',B+'EVENT',{'kind':'hit_entry'},'opcode','0000'),
      ('detached hit CPU Main',B+'EVENT',{'kind':'hit_entry'},'a13','0106A370'),
      ('invented extra HP damage',L+'HEALTH',{'frame':str(hit),'slot':'1'},'after','72'),
      ('wrong damage physical slot',L+'HEALTH',{'frame':str(hit),'slot':'1'},'slot','2'),
      ('wrong damage instruction',L+'HEALTH',{'frame':str(hit),'slot':'1'},'op0','0000'),
      ('wrong damage owner',L+'HEALTH',{'frame':str(hit),'slot':'1'},'a8','01034E90'),
      ('missing complete rise callback',P+'FIELD',{'frame':str(start+4)},None,None),
      ('shifted fixedpoint rise',P+'FIELD',{'frame':str(start+4)},'yraw','00510000'),
      ('wrong first flight velocity',P+'FIELD',{'frame':str(hit)},'vx','00090000'),
      ('wrong first flight height',P+'FIELD',{'frame':str(hit)},'yraw','FFF20000'),
      ('wrong pause pose',P+'FIELD',{'frame':str(hit+4)},'pose','FF031340'),
      ('missing contact pause callback',P+'FIELD',{'frame':str(hit+4)},None,None),
      ('moving during contact pause',P+'FIELD',{'frame':str(hit+4)},'vx','000A0000'),
      ('own drop too early',O+'EVENT',{'kind':'fling','a8':'010350A0'},'frame',str(hit+9)),
      ('own fall gravity changed',P+'FIELD',{'frame':str(hit+13)},'gravity','00009000'),
      ('own fall pose changed',P+'FIELD',{'frame':str(hit+13)},'pose','FE835C80'),
      ('own held landing raised',P+'FIELD',{'frame':str(land+1)},'yraw','00520000'),
      ('own ready retains lock',O+'EVENT',{'frame':str(ready),'kind':'regain','a8':'010350A0'},'flags','0010'),
      ('missing own ready clear',L+'FLAG',{'frame':str(ready),'slot':'2','kind':'flags','before':'0010'},None,None),
      ('own first control remains special',P+'FIELD',{'frame':str(ready+1)},'action','519'),
      ('victim launch parameters changed',O+'EVENT',{'frame':str(hit),'kind':'fling','a8':'01034E90'},'a1','FFFB0000'),
      ('victim native initial velocity changed',P+'FIELD',{'frame':str(hit+1)},'vvy','FFFB0000'),
      ('victim flight callback omitted',P+'FIELD',{'frame':str(hit+12)},None,None),
      ('victim fixedpoint flight changed',P+'FIELD',{'frame':str(hit+12)},'vyraw','00000000'),
      ('victim prematurely released',P+'FIELD',{'frame':str(hit+12)},'vflags','00000001'),
      ('victim floor clamp shifted',P+'FIELD',{'frame':str(vland)},'vyraw','00530000'),
      ('missing actual victim body clear',L+'FLAG',{'frame':str(vclear),'slot':'1','kind':'body'},None,None),
      ('victim grounded hurt retains lock',P+'FIELD',{'frame':str(vclear+3)},'vflags','00000005'),
      ('victim claimed ready at attacker time',O+'EVENT',{'frame':str(vready),'kind':'regain','a8':'01034E90'},'frame',str(ready)),
      ('victim control callback omitted',P+'FIELD',{'frame':str(vready+1)},None,None),
      ('victim HP reverts after hit',P+'FIELD',{'frame':str(hit+12)},'vhp','100'),
      ('fake first chance status', 'MK2_CPU_CHOICE_EVENT',{'kind':'first_result','frame':str(start)},'carry','1'),
      ('second chance result outside Square', 'MK2_CPU_CHOICE_EVENT',{'kind':'second_result','frame':str(start)},'a0','000001F4'),
      ('state injection declared',P+'FIELD',{'frame':str(hit+4)},'writes','1'),
    ]
    for label,tag,criteria,column,value in tests:
        changed=mutate(log,tag,criteria,column,value);need(changed!=log,'Nonvacuous actual hit mutation '+label)
        try:model.phase.verify(changed,guest,'kano')
        except(AssertionError,ValueError,KeyError,StopIteration)as error:results.append(dict(name=label,rejected=True,error=repr(error)))
        else:raise ValueError('Accepted actual corrupt Square hit '+label)
    need(model.phase.verify(log,guest,'kano')==case['phase'],'Untouched real native hit proof still passes')
    for file,wanted in pins.items():need(model.inventory.assembly.sha(file)==wanted,'Actual source/capture never changed '+file)
    pins[str(Path(__file__).resolve())]=model.inventory.assembly.sha(__file__)
    return dict(passed=True,actualCounterexamplesRejected=len(results),counterexamples=results,actualCapturesUnmodified=True,
      gameChanged=False,allCPUOrOtherContactsOrArenaKOAudioAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual Square hit counterexamples')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('counterexamples','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
