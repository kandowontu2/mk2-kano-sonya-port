"""Actual stock-clock comparison for both physical held/released cursors.

Original stock observations establish2-field onset/12-field held repeat.
The required extended row adds17/18, not a different input-repeat policy.
Every observed field and raster is bound to its original native terminal log.
"""
import gzip,json
from pathlib import Path
import qualify_native_selector_navigation as navigation
import capture_native_selector_held as capture

ROOT=capture.ROOT
OUT=ROOT/'audit_native_selector_held_checked'
need,sha,digest=navigation.need,navigation.sha,navigation.digest


def layout_trace(classic):
    board=(1,0,2,9)if classic else(17,1,0,2,9,18)
    cells=[1,9];wanted=[1,9]if classic else[17,18];rows=[]
    events={}
    for start,length,dirs in ((65,48,('right','left')),(125,48,('left','right')),
        (185,4,('right','left')),(197,4,('right','left')),(209,4,('left','right')),(221,4,('left','right'))):
        for offset in range(0,length,12):events[start+offset+2]=dirs
    for start in range(250,346,12):events[start+2]=('left','right')
    for age in range(60,361):
        if age in events:
            for side,direction in enumerate(events[age]):
                if age>=250 and cells[side]==wanted[side]:continue
                index=board.index(cells[side]);delta=1 if direction=='right'else-1
                cells[side]=board[max(0,min(len(board)-1,index+delta))]
        inputs=['none','none']
        if 65<=age<113:inputs=['right','left']
        elif 125<=age<173:inputs=['left','right']
        elif 185<=age<189 or 197<=age<201:inputs=['right','left']
        elif 209<=age<213 or 221<=age<225:inputs=['left','right']
        elif 250<=age<346 and(age-250)%12<4:
            inputs=['left'if cells[0]!=wanted[0]else'none','right'if cells[1]!=wanted[1]else'none']
        rows.append(dict(age=str(age),p1=str(cells[0]),p2=str(cells[1]),input1=inputs[0],input2=inputs[1]))
    return rows


def accepts(row,wanted,css):
    return(all(row[k]==v for k,v in wanted.items())and int(row['frame'])==css+int(row['age'])and
        row['css']=='true'and row['writes']=='0'and row['assistance']=='none'and
        all(row['actor_id'+str(side)]==row['p'+str(side)]and
            0x01000000<=int(row['actor'+str(side)],16)<0x01100000 for side in (1,2)))


def verify(ram):
    need(not OUT.exists()and set(ram['cases'])=={'current','classic'}and
         not capture.original.startup.initial.identity.census(),'Both exact original reference games actually terminal')
    pins=dict(ram['pins']);cases={};rejected=[];actual_traces={}
    for mode in ('current','classic'):
        held=ram['cases'][mode];folder=capture.OUT/mode
        need(held['process'].poll()==0 and held['terminal']==dict(nativeExit=0,exactNativeAbsent=True)and
             held['windowProof']and not held['errors']and held['report']['nativeExit']==0,
             'Original same native handle clean terminal and entire initialized bytes equal independent model')
        result=navigation.parsed(held['text'],'MK2_HELD_RESULT');need(len(result)==1,'Exactly one original native stop result')
        result=result[0];css=int(result['css']);exit_frame=int(result['exit']);hud=int(result['hud'])
        need(result['pass']=='true'and result['classic']==str(mode=='classic').lower()and
             0<css<exit_frame<hud<int(result['frame'])and int(result['combat'])>600 and
             result['writes']=='0'and result['assistance']=='none','Actual post-hold confirmation and native match admission')
        rows=navigation.parsed(held['text'],'MK2_HELD_FIELD');predicted=layout_trace(mode=='classic')
        need(len(rows)==len(predicted)==301,'Every original consecutive held/released native field, no sampling gap')
        for row,wanted in zip(rows,predicted):
            need(accepts(row,wanted,css),'Every actual native selected/preview ID and physical input equals stock-clock extended-layout trajectory')
            for side in (1,2):
                for field in ('p'+str(side),'actor_id'+str(side)):
                    altered=dict(row);altered[field]=str((int(row[field])+1)%19)
                    need(not accepts(altered,wanted,css),'One changed ACTUAL cursor or preview identity cannot inherit success')
                    rejected.append(dict(mode=mode,age=int(row['age']),field=field))
        with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as stream:log=stream.read().splitlines()
        need([s for s in log if not s.startswith(('MK2_DRAIN_STARTUP ','MK2_DRAIN_STARTUP_COMPLETE ','MK2_NAV_FRAME '))]==
             [s.rstrip('\n')for s in held['text']],'All held chronology equals original frozen terminal log')
        frames=held['images'];completes=navigation.parsed(held['text'],'MK2_NAV_LIST_COMPLETE')
        objects=navigation.parsed(held['text'],'MK2_NAV_OBJECT');raster_log=navigation.parsed(log,'MK2_NAV_FRAME')
        need(len(frames)==len(completes)==len(raster_log)==int(result['snapshots'])==15,'All15 complete original native held/list/exit/match fields')
        for index,(image,complete,logged)in enumerate(zip(frames,completes,raster_log),1):
            head=image['header'];raw=image['raw'];im=image['image']
            need(int(head['seq'])==index and all(complete[k]==head[k]for k in ('seq','label','frame','writes','assistance'))and
                 len(raw)==406400 and head['width']=='400'and head['height']=='254'and head['bytes']=='406400'and
                 head['writes']=='0'and head['assistance']=='none'and digest(raw)==image['SHA256']==logged['sha256']and
                 all(logged[k]==v for k,v in head.items())and
                 im.tobytes()==navigation.Image.frombytes('RGB',(400,254),raw,'raw','BGRX').tobytes(),'Exact full original raster bytes, decode and header')
            listed=[r for r in objects if int(r['seq'])==index]
            need(len(listed)==int(complete['count'])and [int(r['order'])for r in listed]==list(range(1,len(listed)+1))and
                 len({r['actor']for r in listed})==len(listed)and
                 all(r['next']==(listed[n+1]['actor']if n+1<len(listed)else'00000000')for n,r in enumerate(listed))and
                 all(r['frame']==head['frame']and r['label']==head['label']and r['writes']=='0'and r['assistance']=='none'for r in listed),
                 'Complete actual original native sorted lists, including retired empty lists')
            if head['label'].startswith('held_age'):
                age=int(head['label'][8:]);row=rows[age-60]
                need(int(head['frame'])==css+age,'Held raster on same actual observed native field')
                for side,descriptor in ((1,'FFC09B30'),(2,'FFC09BA0')):
                    number=[r for r in listed if r['descriptor']==descriptor];need(len(number)==1,'Native player number survives holds/releases')
                    x,y=navigation.contract.XY[int(row['p'+str(side)])];number=number[0]
                    need((int(number['x'],16),int(number['y'],16),int(number['z'],16))==
                         (x+26,y+(12 if side==1 else44),0 if mode=='classic'else0x52),'Correct native held player-number registration/depth')
                photos=[r for r in listed if r['descriptor']in('FFFF2800','FFFF2900')]
                need(len(photos)==(0 if mode=='classic'else2),'Added top portraits only in actual current game, not reference')
                need(all((int(r['x'],16),int(r['y'],16),int(r['z'],16))==
                     ((23 if r['descriptor']=='FFFF2800'else323),24,0x51)for r in photos),'Own native portraits stationary through holds and repeated inputs')
            else:
                need(not any(r['descriptor']in('FFFF2800','FFFF2900','FFC09B30','FFC09BA0')for r in listed),
                     'Observed native versus/HUD/intro fields retire selection objects')
        actual_traces[mode]={side:[dict(age=int(r['age']),id=int(r['p'+str(side)]))for n,r in enumerate(rows)
            if n==0 or r['p'+str(side)]!=rows[n-1]['p'+str(side)]]for side in (1,2)}
        cases[mode]=dict(actualNativeIdentity=held['identity'],originalNativeResult=result,actualNativeFields=rows,
            completeInitializedWindowHashes=held['report']['initializedWindowHashes'],
            completeNativeFrames=[dict(header=f['header'],SHA256=f['SHA256'])for f in frames])
        for leaf in ('report.json','process.json','terminal.json','physical-input-plan.json','run.log.gz'):
            path=folder/leaf;pins[str(path.resolve())]=sha(path)
    # The shared original first three steps are exact in both slots. Added
    # fourth steps reach the own cells at103, on the SAME12-field native clock.
    for side in (1,2):
        need(actual_traces['current'][side][:4]==actual_traces['classic'][side][:4], 'Original stock onset/repeat timestamps match exactly for BOTH slots')
        need(actual_traces['current'][side][4]==dict(age=103,id=18 if side==1 else17),'Extra own cell uses same native repeat clock without skipping stock cells')
    need(len(rejected)==2408,'Every actual selected/preview field in both modes rejected when changed')
    for path in (Path(__file__),Path(capture.__file__),Path(capture.original.__file__),ROOT/'mk2/mk2-maincpu.bin',
        ROOT/'roms/mk2.zip',ROOT/'audit_native_selector_navigation_checked/report.json'):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'All actual original source/model/reference/log/public-build inputs immutable')
    report=dict(passed=True,finiteBothSlotsNativeHeldAndReleasedSelectionTimingAccepted=True,
        nativeOnsetFields=2,nativeHeldRepeatFields=12,actualConsecutiveFieldsPerMode=301,
        originalStockTimingComparedToCurrent=True,actualSelectionTimelines=actual_traces,
        actualCases=cases,actualFaultsRejected=rejected,inputHashes=pins,
        selectionAcrossContinuesAccepted=False,fullGroundShadowMatrixAccepted=False,audioAccepted=False,
        allMovesAccepted=False,allFinishersAccepted=False,fullTowerEndingFreshJoinAccepted=False,fullPortAcceptance=False,
        newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');ram['heldTimingReport']=report
    print(json.dumps(dict(passed=True,actualConsecutiveNativeFields=602,actualFaultsRejected=len(rejected),
        onsetFields=2,heldRepeatFields=12,fullPortAcceptance=False)),flush=True)
    return report
