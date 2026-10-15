"""Qualify original physical navigation observations, not a transport banner.

Covers fresh selection, four single-pulse directions from all14 cells in both
slots, every routing step, native number registration and final17/18 admission.
Does not claim continues, held-repeat timing, all audio/moves or the full port.
"""
import copy,gzip,json,re,subprocess
from pathlib import Path
from PIL import Image
import capture_native_selector_navigation as capture
import selector_navigation_contract as contract

ROOT=capture.ROOT
OUT=ROOT/'audit_native_selector_navigation_checked'
need,sha,digest=capture.need,capture.sha,capture.digest
FIELDS=re.compile(r'(\w+)=([^\s]+)')


def parsed(text,tag):
    return [dict(FIELDS.findall(s))for s in text if s.startswith(tag+' ')]


def accept_step(row,side,index,step,css):
    return (int(row['side'])==side and int(row['index'])==index and int(row['origin'])==step['origin']and
        row['direction']==step['direction']and int(row['expected'])==step['destination']and
        int(row['observed'])==step['destination']and int(row['actor_id'])==step['destination']and
        0x01000000<=int(row['actor'],16)<0x01100000 and row['test']==str(step['test']).lower()and
        row['css']=='true'and row['pass']=='true'and row['writes']=='0'and row['assistance']=='none'and
        int(row['age'])==65+(index-1)*12+10 and int(row['frame'])==css+int(row['age']))


def verify(ram):
    need(not OUT.exists()and set(ram['cases'])==set(contract.DIRECTIONS),'Fresh proof; all four actual original walks available')
    need(not capture.startup.initial.identity.census(),'All original native handles actually terminal, no unknown replacements')
    pins=dict(ram['pins']);cases={};coverage=set();mutations=[];total_steps=0
    cold=json.loads((capture.startup.OUT/'report.json').read_text())
    for direction in contract.DIRECTIONS:
        held=ram['cases'][direction];folder=capture.OUT/direction;proof=held['report']
        need(held['process'].poll()==0 and held['terminal']==dict(nativeExit=0,exactNativeAbsent=True)and
             proof['nativeExit']==0 and held['identity']==proof['actualNativeIdentity']and held['windowProof']and
             not held['errors']and proof['initializedWindowHashes']==cold['actualWindowHashes'],
             'Every actual original native handle terminal and initialized whole model accepted')
        need(held['identity']['CommandLine']==subprocess.list2cmdline(held['command']), 'Original exact physical command preserved')
        with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as stream:log=stream.read().splitlines()
        native_log=[s for s in log if not s.startswith(('MK2_DRAIN_STARTUP ','MK2_DRAIN_STARTUP_COMPLETE ','MK2_NAV_FRAME '))]
        need(native_log==[s.rstrip('\n')for s in held['text']], 'Every held original native observation equals frozen terminal log')
        results=parsed(held['text'],'MK2_NAV_RESULT');need(len(results)==1,'Exactly one original physical-walk predicate')
        result=results[0];css=int(result['css']);hud=int(result['hud']);exit_frame=int(result['exit'])
        plans={side:contract.plan(start,direction)for side,start in ((1,1),(2,9))}
        need(plans==held['plans']and {int(k):v for k,v in json.loads((folder/'physical-input-plan.json').read_text()).items()}==plans,
             'Actual physical plan equals independent required layout, never driver map')
        steps=parsed(held['text'],'MK2_NAV_STEP');wanted=sum(len(p)for p in plans.values())
        need(result['pass']=='true'and result['direction']==direction and int(result['checks'])==wanted and
             int(result['expected_checks'])==wanted and int(result['errors'])==0 and len(steps)==wanted and
             0<css<exit_frame<hud<int(result['frame'])and int(result['combat_fields'])>600 and
             result['writes']=='0'and result['assistance']=='none','All actual original finite controller gates, not transport-only pass')
        observations={};step_map={}
        for side in (1,2):
            rows=[r for r in steps if int(r['side'])==side]
            need(len(rows)==len(plans[side]),'Complete ordered native steps for BOTH slots')
            current=1 if side==1 else 9
            for index,(step,row)in enumerate(zip(plans[side],rows),1):
                need(step['origin']==current and step['destination']==contract.target(current,step['direction'])and
                     accept_step(row,side,index,step,css),'Actual native roster AND actual preview actor follow every independent expected edge')
                current=step['destination'];step_map[side,index]=row
                if step['test']:
                    key=(side,step['origin'],direction);need(key not in coverage,'No duplicate accepting edge substituted for missing edge')
                    coverage.add(key);observations[side,step['origin']]=row
                    for field,value in (('observed',str((current+1)%19)),('actor_id',str((current+1)%19)),
                        ('origin',str((step['origin']+1)%19)),('age',str(int(row['age'])+1)),('css','false'),('pass','false')):
                        changed=dict(row);changed[field]=value
                        need(not accept_step(changed,side,index,step,css),'One changed ACTUAL native navigation field must reject')
                        mutations.append(dict(direction=direction,side=side,origin=step['origin'],field=field))
            need(current==(17 if side==1 else 18),'Both walks finish on true own identities before normal button confirmation')
        list_rows=parsed(held['text'],'MK2_NAV_LIST_COMPLETE');object_rows=parsed(held['text'],'MK2_NAV_OBJECT')
        images=held['images'];need(len(images)==len(list_rows)==32 and int(result['snapshots'])==32,'Complete bounded native lists and rasters for all28 tests plus joined/exit/HUD/intro')
        render_observations=[]
        raster_log=parsed([s for s in log if s.startswith('MK2_NAV_FRAME ')],'MK2_NAV_FRAME')
        need(len(raster_log)==len(images),'All actual RAM rasters accounted in terminal digest log')
        for index,(image,complete,logged)in enumerate(zip(images,list_rows,raster_log),1):
            row=image['header'];raw=image['raw'];im=image['image']
            need(int(row['seq'])==index and all(row[k]==complete[k]for k in ('seq','label','frame','writes','assistance'))and
                 len(raw)==406400 and row['width']=='400'and row['height']=='254'and row['bytes']=='406400'and
                 row['writes']=='0'and row['assistance']=='none'and im.size==(400,254)and im.mode=='RGB'and
                 digest(raw)==image['SHA256']==logged['sha256']and all(logged[k]==v for k,v in row.items())and
                 im.tobytes()==Image.frombytes('RGB',(400,254),raw,'raw','BGRX').tobytes(),'Entire exact original raster/header/raw/decode/list/log, no substituted frames')
            objects=[r for r in object_rows if int(r['seq'])==index]
            need(len(objects)==int(complete['count'])and [int(r['order'])for r in objects]==list(range(1,len(objects)+1))and
                 len({r['actor']for r in objects})==len(objects)and
                 all(r['frame']==row['frame']and r['label']==row['label']and r['writes']=='0'and r['assistance']=='none'for r in objects)and
                 all(r['next']==(objects[n+1]['actor']if n+1<len(objects)else'00000000')for n,r in enumerate(objects)),
                 'Complete real native sorted-list chronology, including empty retired list')
            label=row['label'];frame=int(row['frame']);summary=dict(index=index-1,header=row,SHA256=image['SHA256'])
            if label.startswith('edge_'):
                match=re.fullmatch(r'edge_p([12])_(\d+)_(up|down|left|right)',label);need(match and match[3]==direction,'Exact edge-specific native frame label')
                side,origin=int(match[1]),int(match[2]);obs=observations[side,origin]
                need(frame==int(obs['frame']),'Native image on actual observed successful edge, not a later lucky screenshot')
                number_checks=[]
                for number_side,descriptor in ((1,'FFC09B30'),(2,'FFC09BA0')):
                    number=[r for r in objects if r['descriptor']==descriptor];need(len(number)==1,'Both original unconfirmed native player numbers present')
                    recent=[r for r in steps if int(r['side'])==number_side and int(r['frame'])<=frame]
                    cell=int(recent[-1]['observed'])if recent else(1 if number_side==1 else 9)
                    x,y=contract.XY[cell];number=number[0]
                    need((int(number['x'],16),int(number['y'],16),int(number['z'],16))==(x+26,y+(12 if number_side==1 else 44),0x52),
                         'Native player number remains correctly registered to EVERY selected cell for BOTH slots')
                    number_checks.append(dict(side=number_side,cell=cell,x=x+26,y=y+(12 if number_side==1 else 44),depth=0x52))
                photos=[r for r in objects if r['descriptor']in('FFFF2800','FFFF2900')]
                need(len(photos)==2 and all((int(r['x'],16),int(r['y'],16),int(r['z'],16))==
                     ((23 if r['descriptor']=='FFFF2800'else 323),24,0x51)for r in photos),
                     'Both dedicated native top portraits remain stationary and correctly layered throughout all edge walks')
                summary.update(actualNumberRegistrations=number_checks)
            elif frame>=exit_frame:
                need(not any(r['descriptor']in('FFFF2800','FFFF2900','FFC09B30','FFC09BA0')for r in objects),
                     'Observed native exit/HUD/intro fields contain no selection portraits or player markers')
                if label in ('native_match_hud','native_match_intro'):
                    ids={int(r['id'],16)for r in objects}
                    need({17,18}<=ids,'Actual final match rendered true Kano AND Sonya actors')
            render_observations.append(summary)
        cases[direction]=dict(actualNativeIdentity=held['identity'],result=result,actualSteps=steps,
            actualCompleteNativeFrames=render_observations,fullInitializedWindowHashes=proof['initializedWindowHashes'])
        for leaf in ('report.json','process.json','terminal.json','physical-input-plan.json','run.log.gz'):
            path=folder/leaf;pins[str(path.resolve())]=sha(path)
        total_steps+=wanted
    expected={(side,cell,d)for side in (1,2)for cell in contract.CELLS for d in contract.DIRECTIONS}
    need(coverage==expected and len(coverage)==112 and len(mutations)==672,'Complete actual14cell x4direction x2slot coverage; every changed-native-field trial rejected')
    for path in (Path(__file__),Path(contract.__file__),capture.OUT/'input_hashes.json'):pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'All actual inputs/logs/current private build/public playable immutable')
    report=dict(passed=True,freshBothSlotsAll14CellsAllFourSinglePulseDirectionsAccepted=True,
        nativePreviewIdentityAndPlayerNumberRegistrationOnEveryEdgeAccepted=True,actualNativeWalks=4,
        actualDirectionalEdges=len(coverage),actualRoutingAndTestSteps=total_steps,actualFaultsRejected=mutations,
        actualCases=cases,inputHashes=pins,heldRepeatTimingAccepted=False,selectionAcrossContinuesAccepted=False,
        fullEveryFrameTransitionRasterAccepted=False,fullGroundShadowMatrixAccepted=False,audioAccepted=False,
        allMovesAccepted=False,allFinishersAccepted=False,fullTowerEndingFreshJoinAccepted=False,fullPortAcceptance=False,
        newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');ram['navigationReport']=report
    print(json.dumps(dict(passed=True,actualDirectionalEdges=112,actualSteps=total_steps,actualFaultsRejected=len(mutations),
        fullPortAcceptance=False,publicPlayableChanged=False)),flush=True)
    return report
