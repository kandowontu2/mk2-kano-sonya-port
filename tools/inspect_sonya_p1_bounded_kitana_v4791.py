"""Read-only diagnosis of the actual bounded P1 campaign, not clear acceptance.

Preserve the failed whole-context checker. Summarize real guest observations;
never manufacture missing mirror/range/boss/ending contexts or alter the ROM.
"""
import collections,json,re,subprocess
from pathlib import Path
import run_current_p1_campaign_ram_v4782 as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4792_sonya_p1_bounded_kitana_diagnosis'
FOLDER=ROOT/'audit_v4785_sonya_current_p1_campaign_ram'

def main():
    need(not OUT.exists(),'Fresh bounded diagnosis leaf')
    observed_path=ROOT/'audit_v4786_sonya_current_p1_campaign_observed/report.json'
    failed_path=ROOT/'audit_v4788_sonya_current_p1_whole_campaign_checked/report.json'
    parent_path=ROOT/'audit_v4790_actual_p1_campaign_progress/progress.json'
    observed=json.loads(observed_path.read_text())
    failed=json.loads(failed_path.read_text())
    parent=json.loads(parent_path.read_text())
    need(observed['passed'] and observed['nativeExit']==0 and observed['physicalSlot']==1
         and observed['actualStages']==[0,1,2] and observed['endingStarts']==0
         and observed['endingCompletions']==0 and not observed['actualNaturalTowerClearAccepted'],
         'Actual terminal capture is incomplete, never a clear')
    need(not failed['passed'] and 'One complete native field and physical decision per observed field' in failed['error'],
         'Original mandatory supplemental context failure retained')
    pins={}
    for p,h in observed['inputHashes'].items():
        need(sha(p)==h,'Actual terminal source and native capture unchanged')
        pins[p]=h
    for p in [observed_path,failed_path,parent_path,Path(__file__).resolve()]:pins[str(p)]=sha(p)
    stages=set();specials=collections.Counter();wins=collections.Counter()
    tags=collections.Counter();damage=collections.Counter();live=0
    last_stage=None;first_kitana=None;window=[];final=None;deadline=[]
    with (FOLDER/'run.log').open(encoding='utf-8') as stream:
        for line in stream:
            match=re.match(r'^MK2_NAT_CAMPAIGN_(\w+) ',line)
            if not match:
                if line.startswith('MK2_CAMPAIGN_HOST_DEADLINE '):deadline.append(line.rstrip())
                continue
            tag=match[1];tags[tag]+=1
            f=dict(re.findall(r'(\w+)=([^\s]+)',line));frame=int(f['frame'])
            need(f['human_slot']=='1' and f['fighter']=='sonya' and f['writes']=='0'
                 and f['assistance']=='none','Every observed native row retains genuine P1/no assistance')
            if tag=='FIGHT':last_stage=int(f['stage'])
            if tag=='LIVE':
                live+=1;stages.add(int(f['stage']))
                need(f['human']=='18:18','Every actually sampled human remains Sonya18, not proxy')
                if f['stage']=='2':
                    need(f['cpu']=='4:4','Actual scheduled stage2 opponent is true Kitana4')
                    if first_kitana is None:first_kitana=frame
            if tag=='SPECIAL':
                need(f['id']==f['roster']=='18' and f['actor']==f['a8'] and f['main']==f['a13'],
                     'Observed real special fetch belongs to Sonya')
                specials[(int(f['stage']),f['move'])]+=1
            if tag=='WIN':wins[(int(f['stage']),int(f['slot']))]+=1
            if tag=='HEALTH' and f['pc']=='FF836700' and int(f['after'])<int(f['before']):
                damage[(last_stage,int(f['slot']))]+=int(f['before'])-int(f['after'])
            if first_kitana is not None and first_kitana<=frame<=first_kitana+180 and tag in ('LIVE','SPECIAL','HEALTH','INPUT'):
                window.append(line.rstrip())
            if tag=='RESULT':
                need(final is None,'Single actual terminal summary');final=f
    need(stages=={0,1,2} and final is not None and final['ending']=='-1'
         and final['ending_completed']=='-1' and final['losses']=='103'
         and len(deadline)==1 and 'limit=5900' in deadline[0],
         'Actual finite host deadline, paid losses, no ending')
    policy_path=ROOT/'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'
    wrapper_path=ROOT/'mk2ks_kintaro_pressure_guard_long_campaign_ram_v4436.lua'
    policy=policy_path.read_text();wrapper=wrapper_path.read_text()
    need("elseif strategy=='zoning' then" in policy and 'frame-projectile_start<64' in policy
         and 'elseif gap<80 then' in policy and "if age>=15 then press('Down');press('Block')end" in policy
         and "elseif strategy=='zoning' or strategy=='guard_punish' then" in wrapper,
         'Kitana uses original generic zoning, not the separate mirror or range guards')
    report=dict(passed=True,scope=__doc__,parentAdditiveJournal=str(parent_path),
        mergeRule='Read with parent4790 and its complete4557/additive chain; retain all five original scope groups and exclusions.',
        remaining=parent['remaining'],inputHashes=pins,physicalSlot=1,identity=18,
        actualNativeTerminalExit=0,exec9959TerminalConsumed=True,exec86822CheckerTerminalConsumed=True,
        nativeStages=sorted(stages),actualInitialKitanaLiveFrame=first_kitana,
        sampledTrueSonyaLiveRows=live,actualTagCounts=dict(tags),
        actualNativeSpecialFetches=[dict(stage=s,move=m,count=n) for (s,m),n in sorted(specials.items())],
        actualNativeRoundWinnerReads=[dict(stage=s,slot=p,count=n) for (s,p),n in sorted(wins.items())],
        actualCollisionDamageTotals=[dict(stage=s,targetSlot=p,damage=n) for (s,p),n in sorted(damage.items())],
        actualFirstKitanaWindow=window,actualTerminalSummary=final,actualHostDeadline=deadline[0],
        completeMandatoryContextCheckerPassed=False,completeMandatoryContextCheckerError=failed['error'],
        failedCheckerPreserved=True,missingLaterContextsNotFabricated=True,
        interpretation='The observed ring activates and real collision damage occurs; the first sampled Kitana flight overlaps the committed ring sequence, followed by Sonya damage. The generic zoning controller has no dedicated anti-air branch and retains a64-field sequence. This is evidence to improve physical test tactics, not proof that the native character is defective. Sparse30-field LIVE samples do not supply complete per-field projectile ownership/AI/action histories.',
        nextAction='Use a fresh physical-input-only Kitana anti-air/guard observer and controller, retaining actual native scheduling, paid continues, selection, guest initialization and all original later policies. Do not restart this terminal capture or relax whole-context requirements; independent later contexts must genuinely be reached.',
        actualNaturalP1TowerClearAccepted=False,fullP1EndingPixelsAccepted=False,
        completeP1CampaignAudioAccepted=False,fullPortAcceptance=False,goalStatus='active',
        candidateAndPublicChanged=False,newBuilds=0,rawMediaFilesWritten=0,newDeletedFiles=0)
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Full scope and immutable real evidence retained')
    OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','nativeStages','sampledTrueSonyaLiveRows','actualNativeSpecialFetches','actualNativeRoundWinnerReads','completeMandatoryContextCheckerPassed','actualNaturalP1TowerClearAccepted','newBuilds','rawMediaFilesWritten','fullPortAcceptance')},indent=2),flush=True)

if __name__=='__main__':main()
