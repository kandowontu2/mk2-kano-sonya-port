"""Qualify actual shrinking/recovery, retain failed Shao outcome separately.

Called in the ORIGINAL terminal campaign host, with its original RAM. No game
launch, state/input writes, screenshot/audio files or public promotion. A clean
transport is never credited as a complete tower/ending or visual/audio pass.
"""
import gzip
import hashlib
import json
import re
from pathlib import Path

import capture_native_shang_owned_drain_campaign as capture
import native_process_census_v6647 as census

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_shang_repair_terminal_checked'


def digest(data):
    return hashlib.sha256(data).hexdigest().upper()


def fields(line):
    return dict(re.findall(r'(\w+)=([^\s]+)',line))


def assess(rows):
    required=('enter','cache_call','return')
    need(tuple(row['kind']for row in rows)==required,'One actual complete entry/cache/return handoff')
    first,call,last=rows
    for row in rows:
        need(row['frame']=='480976' and row['owner_id']=='6' and row['victim_id']=='18' and
             row['stage']=='14' and row['writes']=='0' and row['assistance']=='none',
             'Exact originally corrupting true Sonya/Shang frame, no assistance')
        flags=int(row['victim_flags'],16)
        wanted='FFD89F00'if flags&64 else'FFD89500'
        need(row['palette']==wanted and row['victim']=='01034020' and row['owner']=='01034230' and
             row['main']=='010757D0' and row['a11']=='FFD88E00','Own Sonya stream/palette; actual victim costume ownership')
    need(first['actor']==last['actor']==first['owner'] and call['actor']==call['victim'] and
         first['sp']==last['sp'] and first['a1']==call['a1']==last['a1'] and
         int(call['sp'],16)==int(first['sp'],16)-32,
         'Actual A8 borrowed/restored, A1 preserved, stack balanced around exactly one native cache call')
    return dict(actualFrame=480976,actualVictim=18,actualPerformer=6,actualVictimActor=first['victim'],
                normalVictimCostume=True,actualPalette=first['palette'],actualOwnStream=first['a11'],
                actualActorAndScratchStackRecoveryAccepted=True)


def verify(ram):
    need(not OUT.exists() and ram['process'].poll()==0 and not census.census(), 'Same original native terminal; no replay')
    folder=capture.OUT
    terminal=json.loads((folder/'native_terminal.json').read_text())
    need(terminal['nativeExit']==0 and terminal['identity']==ram['identity'] and
         terminal['identity']['ProcessId']==31336 and terminal['identity']['ParentProcessId']==30848 and
         terminal['identity']['createdUnix']==1791721342.2271461,'Exact original birth/path/parent/command/wait terminal')
    captured=ram['capture'];result=captured['result']
    need(result['nativeExit']==0 and result['passed'] and not result['actualNaturalTowerClearAccepted'] and
         not result['fullArtAcceptance'] and not result['fullAudioAcceptance'] and not result['fullPortAcceptance'] and
         result['actualNativeRGBFrameCallbacks']==1125 and result['nativeRGBBytesComparedInRAM']==457200000 and
         not (folder/'stderr.log').read_text(),'Clean transport and complete real RGB callbacks only, no broad success')
    prior_path=ROOT/'audit_native_shang_drain_preceding_campaign_checked/report.json'
    prior=json.loads(prior_path.read_text())
    need(prior['passed'] and prior['accepted']['completeOriginalRows']==1009959 and prior['accepted']['completedOpponents']==13,
         'Complete exact original thirteen-fight regression gate')
    windows=captured['initializedWindows']
    need(windows['actualWindowHashes']=={k:digest(v)for k,v in ram['wanted'].items()} and
         windows['actualWindowBytes']==dict(high=0x100000,owned=0x200000,graphics=65536),
         'All independent initialized windows in THIS original native game')
    pins=dict(result['inputHashes'])
    for proof in (ram['guard'],prior):
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h and (p not in pins or pins[p]==h),'All actual frozen inputs unchanged: '+p);pins[p]=h
    need(captured['text'] and len(captured['text'])==531553099 and len(captured['images'])==45,
         'Exact original full chronology and bounded retained rasters still held')
    chronology_hash=digest(captured['text'].encode())
    disk_hash=hashlib.sha256()
    routes=[];stages=[];wins=[];losses=[];select=[];fights=[];continuing=[];ends=[];native_results=[];fault_rows=[]
    live_count=0;stage16_min_cpu=999
    with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as stream:
        for line in stream:
            disk_hash.update(line.encode())
            if line.startswith('MK2_SHANG_OWNED_DRAIN_ROUTE '):routes.append(fields(line))
            elif line.startswith('MK2_NAT_CAMPAIGN_STAGE '):stages.append(fields(line))
            elif line.startswith('MK2_NAT_CAMPAIGN_WIN '):wins.append(fields(line))
            elif line.startswith('MK2_NAT_CAMPAIGN_LOSS '):losses.append(fields(line))
            elif line.startswith('MK2_NAT_CAMPAIGN_SELECT_ID '):select.append(fields(line))
            elif line.startswith('MK2_NAT_CAMPAIGN_FIGHT '):fights.append(fields(line))
            elif line.startswith('MK2_NAT_CAMPAIGN_LIVE '):
                row=fields(line);live_count+=1
                need(row['human']=='18:18' and row['schedule']=='FFFA3000' and
                     row['stage']in{str(i)for i in (*range(13),14,15,16)} and
                     row['writes']=='0' and row['assistance']=='none',
                     'Every actual live character/state/stage/assistance field valid, including all postfatality attempts')
                if 481852<int(row['frame'])<484674 and row['stage']=='14' and int(row['health'].split(',')[0])>0:
                    if not continuing:continuing.append(row)
                if row['stage']=='16':stage16_min_cpu=min(stage16_min_cpu,int(row['health'].split(',')[1]))
            elif line.startswith(('MK2_NAT_CAMPAIGN_ENDING_START ','MK2_NAT_CAMPAIGN_ENDING_COMPLETED ','MK2_POSTENDING_')):ends.append(line)
            elif line.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ','MK2_MILEENA_CAMPAIGN_OVERRUN ','MK2_SONYA_SHANG_CACHE_CAUSE ')):
                if not line.startswith('MK2_SONYA_SHANG_CACHE_CAUSE ') or fields(line).get('kind')=='first_global_write':fault_rows.append(line)
            if line.startswith(('MK2_NAT_CAMPAIGN_RESULT ','MK2_CURRENT_CAMPAIGN_CACHE_RESULT ','MK2_MILEENA_CAMPAIGN_RESULT ','MK2_SONYA_SHANG_CACHE_CAUSE_RESULT ','MK2_SHANG_OWNED_DRAIN_ROUTE_RESULT ','MK2_CAMPAIGN_HOST_DEADLINE ')):
                native_results.append(line.strip())
    need(disk_hash.hexdigest().upper()==chronology_hash,'Entire531MB original RAM chronology equals complete terminal compressed log')
    need(live_count==590896 and not fault_rows and not ends and continuing,'Every live field verified; actual postfatality ordinary Sonya fight; no hidden cache error or invented ending')
    positive=assess(routes)
    rejected=[]
    for index,key in [(0,'palette'),(1,'actor'),(2,'actor'),(2,'sp'),(2,'a1'),(0,'victim_id'),(0,'a11')]:
        bad=[dict(row)for row in routes];bad[index][key]='00000000'
        try:assess(bad)
        except ValueError as error:rejected.append(dict(index=index,key=key,rejectedBy=str(error)))
        else:raise ValueError('Altered actual handoff accepted')
    for i in range(3):
        try:assess(routes[:i]+routes[i+1:])
        except ValueError as error:rejected.append(dict(omitted=i,rejectedBy=str(error)))
        else:raise ValueError('Omitted actual handoff accepted')
    need(len(rejected)==10 and assess(routes)==positive,'All seven mutations/three omissions reject')
    earned=[]
    for stage,next_stage,cpu in ((14,15,6),(15,16,12)):
        start=next(int(r['frame'])for r in stages if r['stage']==str(stage))
        end=next(int(r['frame'])for r in stages if r['stage']==str(next_stage))
        last_loss=max([int(r['frame'])for r in losses if r['stage']==str(stage) and int(r['frame'])<end]+[start])
        successful=[r for r in wins if r['stage']==str(stage) and r['slot']=='1' and last_loss<int(r['frame'])<end]
        need(len(successful)==2 and all(r['id']=='18' and r['pc']=='FF8296B0' and
             int(r['health'].split(',')[0])>int(r['health'].split(',')[1])for r in successful),
             'Two actual own rounds in a single final winning attempt; paid losses never accumulated')
        earned.append(dict(stage=stage,trueCPU=cpu,nextStage=next_stage,nextStageFrame=end,lastLossFrame=last_loss,actualSuccessfulRounds=successful))
    need(any(r['frame']=='481392' and r['stage']=='14'for r in losses) and
         any(r['frame']=='481852' and r['roster']=='18'for r in select),
         'Fatality actually finishes into real loss and a normal true-Sonya continue, not just absence of a crash')
    need(any('first_bad=-1' in row and 'records=242279' in row for row in native_results) and
         any('global_cache_stores=0' in row for row in native_results) and
         any('limit=18000' in row for row in native_results),'Actual full passive provenance/cache result and ORIGINAL deadline')
    selected_frames={}
    for name in ('shang_victim_provenance_age4.png','shang_shrink_id18_age20.png','shang_shrink_id18_age120.png',
                 'shang_shrink_id18_age320.png','campaign_selection_1_146.png','campaign_fight_selection119_stage16.png'):
        raw=captured['rawImages'][name];image=captured['images'][name]
        need(len(raw)==406400 and image.size==(400,254) and image.mode=='RGB','Complete original native selected pixels')
        rgb=bytes(c for i in range(0,len(raw),4)for c in (raw[i+2],raw[i+1],raw[i]))
        need(image.tobytes()==rgb,'Original PIL view exactly decodes unmodified native BGRX')
        selected_frames[name]=digest(raw)
    for p in (Path(__file__).resolve(),Path(capture.__file__),prior_path,folder/'native_terminal.json',folder/'result.json',
              folder/'run.log.gz',folder/'initialized_windows_proof.json',ROOT/'tools/read_live_shang_drain_frames.py',
              ROOT/'tools/read_live_shang_drain_frames_remote.py',ROOT/'tools/read_retained_mk2_frames.py',ROOT/'tools/read_retained_mk2_frames_remote.py'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()) and not census.census() and ram['process'].poll()==0,'Exact same terminal and all complete original inputs intact')
    report=dict(passed=True,finiteSonyaNormalShrinkingCrashAndOrdinaryRecoveryAccepted=True,
        actualNativeIdentity=ram['identity'],sameOriginalNativeTerminal=True,nativeExit=0,
        originalRAMChronologyBytes=len(captured['text']),wholeTerminalChronologySHA256=chronology_hash,
        actualNativeFrameLimit=984724,actualLiveStateFields=live_count,actualRGBAFrameCallbacks=1125,
        actualRGBBytesObserved=457200000,actualRGBStreamSHA256=result['nativeRGBStreamSHA256'],
        actualOwnedHandoff=positive,actualRouteRows=routes,alteredActualHandoffFaultsRejected=rejected,
        actualNextOrdinaryLiveField=continuing[0],actualShangAndKintaroEarnedClears=earned,
        completeNativeTerminalResults=native_results,viewedOriginalNativeFrameSHA256=selected_frames,
        originalShaoControllerLosses=sum(r['stage']=='16'for r in losses),
        originalShaoControllerOwnWinReads=sum(r['stage']=='16' and r['slot']=='1'for r in wins),
        originalShaoControllerMinimumObservedCPUHealth=stage16_min_cpu,
        wholeCampaignOutcome='Did not clear Shao before original unassisted deadline; not a tower/ending success.',
        finiteEarlierThirteenGate=prior['accepted'],inputHashes=pins,
        requiredArtFollowup='Source-qualified18-byte coordinate correction matches actual stock phase anchors; not compiled/native-verified yet. Selection numeral/blink needs multi-phase comparison, not acceptance from one screenshot.',
        actualFatalityNoLongerCorruptsGlobalsForThisTrueVictimAndCostume=True,
        bothTrueVictimsAndBothCostumesAccepted=False,selectionAccepted=False,fullTowerAccepted=False,
        endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,fullPortAcceptance=False,
        originalNaturalIntegrationRequirements=ram['guard']['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=ram['guard']['originalRemainingWorkGroups'],
        newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawGameplayMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    ram['terminalRecoveryReport']=report
    print(json.dumps(dict(passed=True,finiteSonyaNormalShrinkingCrashAndOrdinaryRecoveryAccepted=True,
                         actualFrames=984724,actualLiveStateFields=live_count,earnedAdditionalCPU=[6,12],
                         shaoLosses=report['originalShaoControllerLosses'],fullTowerAccepted=False,fullPortAcceptance=False)),flush=True)
    return report
