"""Actual post-change schedule and same-paid owned rounds, never inherit old RNG chronology."""
import json,re
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify();root=sync.ROOT
case=root/'audit_current_sonya_p1_kunglao_guard_ready_runtime'
old=root/'audit_current_sonya_p1_default_kick_deferred_runtime/run.log'
out=root/'audit_current_sonya_p1_kunglao_guard_ready_progress_checked';assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['observerSha256']=='8ECAC31E7E9B81A26F29B6B7B383C45C1D91FBFA363D75A3714728D95B1BC00F' and terminal['limitReason'] in (None,'wall_limit')
assert not (case/'stderr.log').read_text().strip()
def prefix(path):return [s for s in path.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and int(re.search(r'\bframe=(\d+)',s)[1])<=12471]
assert prefix(old)==prefix(case/'run.log')
rows=load(case/'run.log');fights=rows['FIGHT'];stages=rows['STAGE']
assert all(r['human']=='18:18' and r['writes']=='0' and r['assistance']=='none' for r in fights)
timeouts=[]
def owned_round(r):
 hp=list(map(int,r['health'].split(',')))
 assert r['slot']=='1' and r['id']=='18' and r['entry']=='FFFEFA40' and r['pc']=='FF8296B0' and hp[0]>0
 if hp[1]==0:return 'native KO'
 assert hp[0]>hp[1]
 states=[s for s in rows['STATE'] if s['stage']==r['stage'] and s['winner']=='1' and s['mode']=='5' and s['health']==r['health'] and 0<=int(s['frame'])-int(r['frame'])<=2]
 assert states,'Positive opponent HP needs native higher-health winner/mode5 corroboration'
 timeouts.append(dict(win=r,nativeWinnerState=states[0]));return 'native higher-health round result'
for r in rows['WIN']:
 if r['slot']=='1':owned_round(r)
clears=[]
for previous,current in zip(stages,stages[1:]):
 stage=previous['stage'];advance=next(r for r in fights if r['frame']==current['frame'] and r['stage']==current['stage'])
 candidates=[r for r in fights if r['stage']==stage and int(r['frame'])<int(advance['frame'])]
 selection=candidates[-1]['selection'];start=next(r for r in candidates if r['selection']==selection)
 lo,hi=int(start['frame']),int(advance['frame'])
 wins=[r for r in rows['WIN'] if r['stage']==stage and lo<int(r['frame'])<hi]
 own=[r for r in wins if r['slot']=='1'];cpu=[r for r in wins if r['slot']=='2']
 assert len(own)==2 and len(cpu)<2 and advance['selection']==selection
 assert not any(lo<int(r['frame'])<hi for r in rows['LOSS'])
 assert not any(lo<int(r['frame'])<hi for r in rows.get('SELECT',[]))
 clears.append(dict(stage=int(stage),attempt=start,ownNativeWins=own,cpuNativeWins=cpu,advance=advance))
kung=next((r for r in stages if r['stage']=='4'),None);after=next((r for r in stages if r['stage']=='5'),None)
kungcost=dict(firstFight=kung['frame'] if kung else None,nextStage=after['frame'] if after else None,fieldsToAdvance=int(after['frame'])-int(kung['frame']) if kung and after else None,paidLosses=sum(r['stage']=='4' for r in rows['LOSS']))
report=dict(exactOriginalPrechangePrefixThrough=12471,matchingPrefixRecords=len(prefix(old)),actualSamePaidNativeClears=clears,
 actualStageFirstFights=[next(r for r in fights if r['frame']==s['frame'] and r['stage']==s['stage']) for s in stages],
 actualKungCost=kungcost,oldKungCost=dict(fieldsToAdvance=16802,paidLosses=3),
 nativeHigherHealthRoundCorroboration=timeouts,earlyNativeSpecialEntryObservationIntentionallyDeferred=True,
 physicalKungLegPlans=len([r for r in rows.get('KUNGLAO_GUARD_ATTEMPT',[]) if r['stage']=='4']),ownedEarlyLegActivationAccepted=False,
 ownBossRoundWins=[r for r in rows['WIN'] if r['slot']=='1' and r['stage'] in ('15','16')],
 lastObservedFrame=max(int(r['frame']) for entries in rows.values() for r in entries),terminal=terminal,
 logSHA256=sync.sha(case/'run.log'),wholeCampaignAccepted=False,endingAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(kungcost=kungcost,clearStages=[r['stage'] for r in clears],actualFirstCPU=[(r['stage'],r['cpu']) for r in report['actualStageFirstFights']],nativeHigherHealthRounds=len(timeouts),bossOwnWins=report['ownBossRoundWins'],lastObserved=report['lastObservedFrame'],terminal=terminal,logSHA256=report['logSHA256'])))
