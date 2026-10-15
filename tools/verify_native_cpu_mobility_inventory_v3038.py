"""True normal-input mobility branch inventory, no forced CPU identity or RNG.

Whole guest, state and health ledgers checked. Actual collision carries and
native contact entry/HP stores identify hits, not unrelated later damage.
Not complete hit/Bicycle/interrupt/KO/raster/audio or all-port acceptance.
"""
import json,struct,sys,traceback
from pathlib import Path
import native_cpu_mobility_capture_contract_v3036 as capture
import run_native_cpu_mobility_dispatch_v3027 as dispatch
import verify_current_cpu_overlap_v1911 as overlap

ROOT=capture.ROOT;OUT=ROOT/'audit_v3039_native_cpu_mobility_inventory_checked';need=capture.need

def native_choices(log,guest,player):
    events=capture.rows(log,'MK2_MOBILITY_EVENT');snapshots=capture.rows(log,'MK2_MOBILITY_ENTRY_STATE')
    entries=[r for r in events if r['kind']in('square_entry','bicycle_entry')]
    originals=[r for r in overlap.rows(log,'EVENT')if r['kind']in('square','bicycle')]
    need(len(entries)==len(originals)and len(snapshots)==2*len(entries),'Every actual mobility entry has both independently recorded physical states')
    choices=capture.square.rows(log,'MK2_CPU_CHOICE_EVENT');health=capture.rows(log,'MK2_MOBILITY_HEALTH')
    for row in health:
        need(row['mask']==65535 and row['writes']==0 and row['assistance']=='none'and row['at']==(0x010602f0 if row['slot']==1 else 0x01060ec0),
             'Every actual mobility health store targets the real physical lifebar')
        need(struct.unpack_from('<3H',guest,(row['pc']-48-0xff800000)//8)==tuple(row[f'op{i}']for i in range(3)),
             'Every additional boundary HP writer source-bound')
    result=[]
    for entry,old in zip(entries,originals):
        start,serial,move=entry['frame'],entry['serial'],entry['move'];actor,main=entry['actor'],entry['main']
        need((old['frame'],old['kind'],old['a8'],old['a13'])==(start,move,actor,main),'Independent actual native action entries agree')
        states=[r for r in snapshots if r['serial']==serial]
        need(len(states)==2 and {r['slot']for r in states}=={1,2},'Both actual native entry actors')
        for r in states:
            identity=18 if r['slot']==2 else capture.ledgers.pair.HUMANS[player]
            need(r['frame']==start and r['move']==move and r['owner']==r['actor']and
                 (r['id'],r['roster'],r['state'],r['mode'])==(identity,identity,0 if r['slot']==2 else 1,2)and
                 r['hp']>0 and r['floor']==r['stage_floor']-(135 if identity==18 else 134)and r['schedule']==0xfffa3180 and r['stage']==0,
                 'True entry identity, physical role, Main, life and native floor')
        own=next(r for r in states if r['slot']==2)
        need((own['actor'],own['main'])==(actor,main)and own['action']==0x303 and own['flags']&0x1c==own['body']&12==0,
             'Real clean CPU mobility entry')
        native=next(r for r in choices if r['kind']==move and r['frame']==start)
        calls=[r for r in choices if r['serial']==native['serial']]
        expected_kinds=['entry','first_call','first_result',move]if move=='bicycle'else ['entry','first_call','first_result','second_call','second_result',move]
        need([r['kind']for r in calls]==expected_kinds,
             'Actual source-derived native RNG router (first-chance Bicycle, second-chance Square)')
        for r in calls:
            need(r['frame']==start and (r['actor'],r['main'],r['owner'],r['id'],r['roster'])==(actor,main,actor,18,18)and
                 (r['state'],r['human_state'],r['mode'],r['stage'],r['schedule'])==(0,1,2,0,0xfffa3180)and
                 r['carry']==(r['status']>>30)&1 and r['pc']==r['entry']+16 and r['mask']==65535 and r['writes']==0 and r['assistance']=='none'and
                 struct.unpack_from('<H',guest,(r['entry']-0xff800000)//8)[0]==r['opcode'], 'Every actual native choice status/opcode/role/owner source-bound')
        need(calls[1]['a0']==250 and 0<=calls[2]['a0']<1000 and calls[2]['carry']==int(calls[2]['a0']<250),'Original first chance threshold and actual status')
        if move=='bicycle':
            need(calls[2]['carry']==1 and calls[-1]['a0']==calls[2]['a0']and calls[-1]['entry']==0xfffbc320,
                 'Original short first-chance Bicycle branch, no second RNG call invented')
        else:
            need(calls[2]['carry']==0 and calls[3]['a0']==400 and 0<=calls[4]['a0']<400 and calls[4]['carry']==1 and
                 calls[-1]['a0']==calls[4]['a0']and calls[-1]['entry']==0xfffbc2f0,'Original second-chance Square branch')
        group=[r for r in events if r['serial']==serial]
        for r in group:
            need(r['owner']==r['actor']==r['a8']==actor and r['main']==r['a13']==main and r['id']==18 and r['writes']==0 and
                 r['assistance']=='none'and r['pc']==r['entry']+16 and r['mask']==65535 and r['carry']==(r['status']>>30)&1 and
                 struct.unpack_from('<H',guest,(r['entry']-0xff800000)//8)[0]==r['opcode'],'Every actual native collision/fall entry owned and source-bound')
        checks=[r for r in group if r['kind']==move+'_collision'];contact=[r for r in group if r['kind']==('square_hit'if move=='square'else 'bicycle_contact')]
        need(checks and [r['frame']for r in checks]==list(range(start+(9 if move=='square'else 7),checks[-1]['frame']+1)),
             'Every reached native seek collision callback without gaps')
        hit=bool(contact)
        need(len(contact)==int(hit)and [r['carry']for r in checks]==[0]*(len(checks)-int(hit))+([1]if hit else []),
             'Actual collision carry leads to its native contact entry, no invented hit')
        if hit:need(contact[0]['frame']==checks[-1]['frame'],'Native collision and contact entry share the actual field')
        damage=[r for r in health if hit and r['frame']==contact[0]['frame']and r['slot']==1 and r['before']>r['after']]
        if move=='square':
            need((len(checks)<26 if hit else len(checks)==26)and [r['a11']for r in checks]==list(range(26,26-len(checks),-1)),
                 'Actual original Square countdown, complete miss or genuine early contact')
            need(len(damage)==int(hit)and all(r['before']-r['after']==27 and r['pc']==0xff836700 and r['a8']==actor and r['a13']==main for r in damage),
                 'Unblocked actual Square contact inflicts exactly27 through original owned health routine')
        result.append(dict(start=start,serial=serial,move=move,nativeChoiceSerial=native['serial'],firstRandomResult=calls[2]['a0'],
             secondRandomResult=calls[4]['a0']if move=='square'else None,actualCollisionChecks=len(checks),nativeContact=hit,actualContactFrame=contact[0]['frame']if hit else None,
             actualContactDamage=[dict(frame=r['frame'],before=r['before'],after=r['after'],pc=r['pc'])for r in damage],
             fullMovePhaseAccepted=False,renderOrAudioAccepted=False))
    return result

def verify():
    capture.metadata_contract_source();pins={};cases={}
    for build,player,approach,policy in dispatch.CASES:
        folder=ROOT/dispatch.name((build,player,approach,policy))
        log,guest,case=capture.capture(folder,build,player,approach,policy,pins)
        branches=native_choices(log,guest,player)
        case.update(case=folder.name,player=player,build=build,branches=branches,noMobilityScenario=not branches)
        cases[folder.name]=case
        print(folder.name+': true native branches='+str([(b['move'],b['nativeContact'])for b in branches])+', complete whole-state/health ledgers checked',flush=True)
    all_moves=[b for c in cases.values()for b in c['branches']]
    need(len(all_moves)==5 and sum(b['move']=='bicycle'for b in all_moves)==1 and
         sum(b['move']=='square'and b['nativeContact']for b in all_moves)==1 and sum(c['noMobilityScenario']for c in cases.values())==1,
         'Actual naturally reached Square hit/Bicycle miss/repeated Square and genuine no-move scenario kept distinct')
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':pins[str(Path(file).resolve())]=capture.assembly.sha(file)
    path=ROOT/'audit_v3028_native_cpu_mobility_dispatch/report.json';pins[str(path)]=capture.assembly.sha(path)
    for file,wanted in pins.items():need(capture.assembly.sha(file)==wanted,'Actual captured native mobility input unchanged '+file)
    return dict(passed=True,cases=cases,actualPhysicalFixtures=5,actualMobilityEntries=5,actualSquareContactDamage=27,
      actualCandidateSquareContact=True,actualControlBicycleMiss=True,genuineNoMobilityScenarios=1,
      wholeNativeStateHealthLedgersAccepted=True,allMovePhaseOrCPUOrRasterAudioAccepted=False,
      gameChanged=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual CPU mobility branch inventory')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
