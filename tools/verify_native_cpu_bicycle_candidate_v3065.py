"""True candidate Bicycle miss, exact original phases and preceding recovery.

Two real guard/jump fixtures retained, including the Sonya mirror which did not
choose Bicycle. Whole guest/state/HP/native choice/initial write chains and
the Square-to-Bicycle clean bridge checked. No all-contact/arena/audio claim.
"""
import inspect,json,struct,sys,traceback
from pathlib import Path
import native_cpu_mobility_capture_contract_v3036 as capture
import native_cpu_bicycle_miss_contract_v3064 as phase
import verify_native_cpu_bicycle_extended_v3055 as control
import verify_native_cpu_mobility_inventory_v3038 as choices
import run_native_cpu_mobility_guard_dispatch_v3061 as dispatch
import verify_current_cpu_overlap_v1911 as overlap

ROOT=capture.ROOT;OUT=ROOT/'audit_v3066_native_cpu_bicycle_candidate_checked';need=capture.need

def initial_and_bridge(log,guest,typed):
    start=typed['start'];fields=capture.ledgers.pair.rows(log,'FIELD');by={r['frame']:r for r in fields}
    snapshots=capture.rows(log,'MK2_MOBILITY_ENTRY_STATE')
    pair=[r for r in snapshots if r['move']=='bicycle'and r['frame']==start]
    need(len(pair)==2 and {r['slot']for r in pair}=={1,2},'Both actual Bicycle entry state snapshots')
    stores=capture.rows(log,'MK2_MOBILITY_FLAG');health=capture.rows(log,'MK2_MOBILITY_HEALTH')
    for snapshot in pair:
        side=snapshot['slot'];prefix=''if side==2 else 'v';native=by[start+1]
        for kind in('action','body','flags'):
            value=snapshot[kind]
            for row in stores:
                if row['frame']!=start or row['slot']!=side or row['kind']!=kind:continue
                need(row['mask']==65535 and row['writes']==0 and row['assistance']=='none'and
                     (row['actor'],row['main'],row['owner'])==(snapshot['actor'],snapshot['main'],snapshot['actor'])and
                     row['before']==value and row['at']==(snapshot['actor']+0x160 if kind=='body'else snapshot['main']+(0x1f0 if kind=='action'else 0x210))and
                     struct.unpack_from('<2H',guest,(row['pc']-32-0xff800000)//8)==(row['op0'],row['op1']),
                     'Every independently observed original initial lock/state store is source-bound and replayable')
                value=row['after']
            need(value==native[prefix+kind],'Independent entry write chain equals first native callback')
        hp=snapshot['hp']
        for row in health:
            if row['frame']==start and row['slot']==side:
                need(row['before']==hp,'Actual entry health write chain');hp=row['after']
        need(hp==native[prefix+'hp'],'Actual entry health agrees with first native callback')
        need(all(snapshot[k]==native[prefix+k]for k in('actor','main','owner','id','roster','state','floor')),
             'Initial and first native callback agree on true physical actors/Main/role/floor')
    actual=[r for r in stores if start<=r['frame']<=typed['ready']]
    legacy=[r for r in capture.ledgers.pair.flag_rows(log)if start<=r['frame']<=typed['ready']]
    keys=('frame','slot','kind','at','before','after','pc','a8','a13','actor','main','id','state','op0','op1')
    need([tuple(r[k]for k in keys)for r in actual]==[tuple(r[k]for k in keys)for r in legacy],
         'Independent and original complete two-slot state writers agree through Bicycle recovery')
    entries=[r for r in overlap.rows(log,'EVENT')if r['kind']=='bicycle']
    need(len(entries)==1,'One actual candidate Bicycle for this capture')
    entry=entries[0];actor,main=entry['a8'],entry['a13']
    preceding=[r for r in overlap.rows(log,'EVENT')if r['frame']<start and (r['a8'],r['a13'])==(actor,main)]
    previous=next(r for r in reversed(preceding)if r['kind']=='regain')
    square=next(r for r in reversed(preceding)if r['kind']=='square')
    need(previous['frame']==start-1 and previous['entry']==0xff861500 and previous['pc']==0xff861510 and previous['action']==0 and
         previous['id']==18 and previous['main_owner']==actor and previous['flags']&0x1c==previous['body']&12==0 and
         previous['vx']==previous['vy']==previous['gravity']==previous['trail']==0 and previous['pose']==0xfe835bc0,
         'The actual preceding Square fully regains at its own original ready before Bicycle entry')
    need(square['frame']==start-55 and previous['frame']==square['frame']+54,'Original full54-field Square miss precedes separate Bicycle choice')
    bridge=by[start]
    need((bridge['actor'],bridge['main'],bridge['owner'],bridge['id'],bridge['roster'],bridge['state'])==(actor,main,actor,18,18,0)and
         bridge['action']==0x303 and bridge['flags']&0x1c==bridge['body']&12==0 and bridge['trail']==bridge['vy']==bridge['gravity']==0 and
         bridge['pose']==0xfe835bc0 and bridge['y']==bridge['floor'],
         'True clean native callback between distinct specials, no persistent lock/pose/identity substitution')
    return dict(previousSquare=square['frame'],previousSquareRegain=previous['frame'],firstBicycle=start,
                cleanBetweenSpecials=True,independentInitialWritesAccepted=True)

def verify():
    control.original_phase_source();capture.metadata_contract_source()
    need(inspect.getsource(phase.verify)==inspect.getsource(control.phase.verify),'Entire accepted original Bicycle physics/phase function retained exactly, no eased candidate criteria')
    pins={};cases={}
    for build,player,approach,policy in dispatch.CASES:
        folder=ROOT/dispatch.name((build,player,approach,policy))
        log,guest,case=capture.capture(folder,build,player,approach,policy,pins)
        native=choices.native_choices(log,guest,player);bicycles=[r for r in native if r['move']=='bicycle']
        typed=phase.verify(log,guest)if bicycles else None
        bridge=initial_and_bridge(log,guest,typed)if typed else None
        case.update(case=folder.name,player=player,build=build,branches=native,phase=typed,cleanSpecialBridge=bridge,
                    actualBicycleChosen=bool(bicycles),noBicycleScenario=not bicycles,allCPUOrArtAudioAccepted=False)
        cases[build+'_'+player]=case
        print(folder.name+': actual Bicycle='+str(bool(bicycles))+'; whole native identity/source/state/HP checked',flush=True)
    need(cases['new_kano']['actualBicycleChosen']and cases['new_kano']['phase']['fields']==61 and
         cases['new_kano']['phase']['fractionalLandingY']==40960 and cases['new_kano']['cleanSpecialBridge']['cleanBetweenSpecials']and
         cases['new_sonya']['noBicycleScenario']and cases['new_sonya']['phase']is None,
         'Candidate actual Bicycle miss accepted; genuine mirror choice remains a no-Bicycle scenario')
    path=ROOT/'audit_v3062_native_cpu_mobility_guard_dispatch/report.json';pins[str(path)]=capture.assembly.sha(path)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':pins[str(Path(file).resolve())]=capture.assembly.sha(file)
    for file,wanted in pins.items():need(capture.assembly.sha(file)==wanted,'Immutable candidate Bicycle source/capture '+file)
    return dict(passed=True,cases=cases,actualPhysicalFixtures=2,actualCandidateBicycleMissAccepted=True,
      entireOriginalBicyclePhaseChecksRetained=True,actualCleanSquareToBicycleBridgeAccepted=True,
      actualCandidateFirstChanceResult=126,candidateBicycleHitOrBlockedAccepted=False,
      allCPUOrArenaArtAudioKOAccepted=False,gameChanged=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual candidate Bicycle miss evidence')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
