"""Specific real Bicycle hit/phase corruption tests; actual capture untouched."""
import json
import traceback
from pathlib import Path
import verify_current_cpu_launch_jump_v3319 as model
import verify_native_cpu_mobility_inventory_v3038 as choices
from test_current_cpu_overlap_v1912 import mutate
ROOT=model.ROOT;OUT=ROOT/'audit_v3328_current_cpu_bicycle_hit_phase_counterexamples';need=model.need

def run():
    path=model.OUT/'report.json';proof=json.loads(path.read_text());need(proof['passed'],'Actual current hit proof required')
    pins=dict(proof['inputHashes']);pins[str(path)]=model.current.assembly.sha(path)
    folder=ROOT/model.CASE;log=(folder/'run.log').read_text(encoding='utf-8-sig');guest=(folder/'guest_maincpu.bin').read_bytes()
    P='MK2_CPU_PAIR_FIELD';M='MK2_MOBILITY_';C='MK2_CPU_CHOICE_EVENT';O='MK2_CPU_OVERLAP_EVENT'
    def field(frame,column,value,reason):return (column+' at '+str(frame),P,{'frame':str(frame)},column,value,'phase',reason)
    tests=[
        field(2666,'pose','FE83EA40','All six original startup fields'),
        field(2666,'xraw','00000000','All six original startup fields'),
        field(2666,'yraw','00510000','All six original startup fields'),
        field(2672,'vy','FFFA0000','Every original rising seek velocity and cycle pose'),
        field(2672,'pose','FE83EA40','Every original rising seek velocity and cycle pose'),
        field(2672,'floor','82','Entire actual HP/floor/stage history'),
        field(2681,'vhp','134','Entire actual HP/floor/stage history'),
        field(2681,'vid','1','Every actual owner, real ID and physical role retained'),
        field(2682,'vpose','FE829620','Every paired original four-field attacker/victim animation step'),
        field(2682,'vvx','00000000','Full paired lift/float velocity publication on both physical actors'),
        field(2682,'vxraw','02260000','Original paired integration and +48/-32 owned victim offset'),
        field(2697,'vvy','FFFD0000','Full paired lift/float velocity publication on both physical actors'),
        field(2711,'vaction','1286','Every victim native paired phase lock/action'),
        field(2717,'pose','FE83EAE0','All twelve original reverse-intro release fields'),
        field(2726,'gravity','0000A000','Original stationary own falling pose'),
        field(2726,'vy','00030000','Every original own vertical fall step'),
        field(2739,'vy','00008000','Every own grounded landing hold'),
        field(2743,'flags','00000010','Both real control callbacks restored separately'),
        field(2750,'vflags','00000005','Every victim grounded hurt recovery field'),
        field(2768,'vaction','1286','Both real control callbacks restored separately'),
        ('contact damage changed',M+'HEALTH',{'frame':'2680','slot':'1'},'after','134','phase','Exactly 22 actual HP through original owned health store'),
        ('victim release gravity changed',O,{'frame':'2712','kind':'fling'},'a2','00008000','phase','Actual owned victim release parameters'),
        ('own drop before reverse intro',O,{'frame':'2724','kind':'fling'},'frame','2723','phase','Original own drop only after full reverse intro'),
        ('CPU ready retains body lock',O,{'frame':'2742','kind':'regain'},'body','0016','phase','Both individual native ready events actually clean'),
        ('victim ready retains lock',O,{'frame':'2767','kind':'regain'},'flags','0005','phase','Both individual native ready events actually clean'),
        ('native collision carry fabricated',M+'EVENT',{'frame':'2680','kind':'bicycle_collision'},'carry','0','choice','Every actual native collision/fall entry owned and source-bound'),
        ('native first RNG outside threshold',C,{'frame':'2663','kind':'first_result'},'a0','000001F4','choice','Original first chance threshold and actual status'),
        ('native first carry fabricated',C,{'frame':'2663','kind':'first_result'},'carry','0','choice','Every actual native choice status/opcode/role/owner source-bound'),
    ]
    need(model.phase.verify(log,guest)==proof['case']['phase'],'Same-path real phase positive control')
    original_choices=choices.native_choices(log,guest,'kano');results=[]
    for label,tag,criteria,column,value,contract,reason in tests:
        changed=mutate(log,tag,criteria,column,value)
        if tag==P and column in {'xraw','yraw','vxraw','vyraw'}:
            word=(int(value,16)>>16)&65535; signed=word-65536 if word&32768 else word
            view={'xraw':'x','yraw':'y','vxraw':'vxpos','vyraw':'vyraw'}[column]
            if column=='vyraw':view='vypos'
            changed=mutate(changed,tag,criteria,view,str(signed))
        try:
            if contract=='phase':model.phase.verify(changed,guest)
            else:choices.native_choices(changed,guest,'kano')
        except (ValueError,AssertionError) as error:
            need(reason in str(error),'Specific intended rejection, not an unrelated missing-event/parser exception: '+label+' '+repr(error))
            results.append(dict(name=label,rejected=True,reason=str(error)))
        else:raise ValueError('Accepted corrupt native Bicycle contact: '+label)
    need(model.phase.verify(log,guest)==proof['case']['phase'] and choices.native_choices(log,guest,'kano')==original_choices,'Untouched real contact remains identical')
    for file,digest in pins.items():need(model.current.assembly.sha(file)==digest,'Actual capture/source never modified')
    for file in (__file__,mutate.__globals__['__file__'],choices.__file__):pins[str(Path(file).resolve())]=model.current.assembly.sha(file)
    return dict(passed=True,actualCounterexamplesRejected=len(results),counterexamples=results,
                specificRejectionReasonsRequired=True,unrelatedMissingEventExceptionsNeverAccepted=True,
                samePathPositiveControlsAccepted=True,actualCapturesUnmodified=True,gameChanged=False,
                fullMovePhaseHorizontalPushAndAudioAccepted=False,fullPortAcceptance=False,inputHashes=pins)

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite counterexamples')
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('counterexamples','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
