"""Real full Bicycle miss and first-chance branch corruptions, no saved edits."""
import json,traceback
from pathlib import Path
import verify_native_cpu_bicycle_round_boundary_v3128 as model
import verify_native_cpu_mobility_inventory_v3038 as choices
from test_current_cpu_overlap_v1912 import mutate

ROOT=model.ROOT;OUT=ROOT/'audit_v3141_native_cpu_bicycle_round_phase_units';need=model.need

def verify():
    path=model.OUT/'report.json';proof=json.loads(path.read_text());need(proof['passed']and proof['actualCandidateBicycleMissAccepted']and proof['actualRoundRevealToLiveBoundaryAccepted'],'Actual extended control only')
    pins=dict(proof['inputHashes']);pins[str(path)]=model.capture.assembly.sha(path);case=proof['cases']['new_kano']
    folder=ROOT/case['case'];log=(folder/'run.log').read_text(encoding='utf-8-sig');guest=(folder/'guest_maincpu.bin').read_bytes()
    start,fall,ready=(case['phase'][k]for k in('start','fall','ready'));P='MK2_CPU_PAIR_';O='MK2_CPU_OVERLAP_';M='MK2_MOBILITY_';results=[]
    tests=[
      ('missing intro callback',P+'FIELD',{'frame':str(start+3)},None,None,'phase'),
      ('wrong original intro pose',P+'FIELD',{'frame':str(start+3)},'pose','FE83EA40','phase'),
      ('wrong intro horizontal step',P+'FIELD',{'frame':str(start+3)},'xraw','00000000','phase'),
      ('wrong intro vertical step',P+'FIELD',{'frame':str(start+3)},'yraw','00510000','phase'),
      ('wrong original upward acceleration',P+'FIELD',{'frame':str(start+9)},'gravity','0000A000','phase'),
      ('missing seek callback',P+'FIELD',{'frame':str(start+10)},None,None,'phase'),
      ('wrong seek pose',P+'FIELD',{'frame':str(start+10)},'pose','FE83EA40','phase'),
      ('wrong seek horizontal speed',P+'FIELD',{'frame':str(start+10)},'vx','00050000','phase'),
      ('wrong native falling parameters',M+'EVENT',{'kind':'native_fall'},'a2','00009000','phase'),
      ('native ceiling crossing shifted',M+'EVENT',{'kind':'native_fall'},'frame',str(fall-1),'phase'),
      ('wrong falling pose',P+'FIELD',{'frame':str(fall+5)},'pose','FE83EA40','phase'),
      ('wrong falling fixedpoint Y',P+'FIELD',{'frame':str(fall+5)},'yraw','00000000','phase'),
      ('wrong fall gravity',P+'FIELD',{'frame':str(fall+5)},'gravity','00008000','phase'),
      ('missing landing callback',P+'FIELD',{'frame':str(ready)},None,None,'phase'),
      ('fractional landing discarded',P+'FIELD',{'frame':str(ready+1)},'yraw','00510000','phase'),
      ('recovered native lock retained',O+'EVENT',{'frame':str(ready),'kind':'regain','a8':'010350A0'},'flags','0010','phase'),
      ('native victim role replaced',P+'FIELD',{'frame':str(start+10)},'vid','1','phase'),
      ('wrong native floor',P+'FIELD',{'frame':str(start+10)},'floor','82','phase'),
      ('invented miss damage',P+'FIELD',{'frame':str(start+10)},'vhp','134','phase'),
      ('wrong lock acquisition',M+'FLAG',{'frame':str(start),'slot':'2','kind':'flags'},'after','0000','phase'),
      ('missing native first chance result','MK2_CPU_CHOICE_EVENT',{'frame':str(start),'kind':'first_result'},None,None,'choice'),
      ('fake first chance carry','MK2_CPU_CHOICE_EVENT',{'frame':str(start),'kind':'first_result'},'carry','0','choice'),
      ('first RNG outside Bicycle threshold','MK2_CPU_CHOICE_EVENT',{'frame':str(start),'kind':'first_result'},'a0','000001F4','choice'),
      ('first chance jumps wrong native branch','MK2_CPU_CHOICE_EVENT',{'frame':str(start),'kind':'bicycle'},'entry','FFFBC2F0','choice'),
      ('one native seek check omitted',M+'EVENT',{'frame':str(start+10),'kind':'bicycle_collision'},None,None,'choice'),
      ('false native seek contact',M+'EVENT',{'frame':str(start+10),'kind':'bicycle_collision'},'carry','1','choice'),
    ]
    for label,tag,criteria,column,value,contract in tests:
        changed=mutate(log,tag,criteria,column,value);need(changed!=log,'Actual nonvacuous Bicycle mutation '+label)
        try:
            if contract=='phase':model.phase.verify(changed,guest)
            else:choices.native_choices(changed,guest,'kano')
        except(AssertionError,ValueError,StopIteration)as error:results.append(dict(name=label,rejected=True,contract=contract,error=repr(error)))
        else:raise ValueError('Accepted corrupted actual Bicycle '+label)
    need(model.phase.verify(log,guest)==case['phase'],'Untouched original full Bicycle miss phase proof')
    for file,wanted in pins.items():need(model.capture.assembly.sha(file)==wanted,'Actual immutable Bicycle evidence '+file)
    pins[str(Path(__file__).resolve())]=model.capture.assembly.sha(__file__);pins[str(Path(choices.__file__).resolve())]=model.capture.assembly.sha(choices.__file__)
    return dict(passed=True,actualCounterexamplesRejected=len(results),counterexamples=results,actualCapturesUnmodified=True,
      candidateBicycleMissAccepted=True,candidateBicycleHitOrBlockedAccepted=False,gameChanged=False,allCPUOrOtherContactsArtAudioKOAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual extended Bicycle counterexamples')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('counterexamples','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
