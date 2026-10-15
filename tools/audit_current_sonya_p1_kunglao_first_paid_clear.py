"""First-paid Kung result and later real route cost; never infer whole-campaign shortening."""
import json
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify();root=sync.ROOT
path=root/'audit_current_sonya_p1_kunglao_guard_ready_runtime/run.log'
out=root/'audit_current_sonya_p1_kunglao_first_paid_clear_checked';assert not out.exists()
rows=load(path)
def gate(rows):
 start=next(r for r in rows['FIGHT'] if r['stage']=='4');advance=next(r for r in rows['FIGHT'] if r['stage']=='5')
 assert start['human']==advance['human']=='18:18' and start['cpu']=='0:0' and advance['selection']==start['selection']
 lo,hi=int(start['frame']),int(advance['frame'])
 wins=[r for r in rows['WIN'] if r['stage']=='4' and lo<int(r['frame'])<hi]
 assert len(wins)==2
 for r in wins:
  hp=list(map(int,r['health'].split(',')))
  assert r['slot']=='1' and r['id']=='18' and r['entry']=='FFFEFA40' and r['pc']=='FF8296B0' and hp[0]>0 and hp[1]==0
 assert not any(lo<int(r['frame'])<hi for r in rows['LOSS'])
 assert not any(lo<int(r['frame'])<hi for r in rows.get('SELECT',[]))
 return dict(firstPaidAttempt=start,wins=wins,nextFight=advance,fieldCost=hi-lo)
clear=gate(rows);faults=[]
for name,broken in (
 ('missing_round',dict(rows,WIN=[r for r in rows['WIN'] if r['frame']!='15142'])),
 ('continued_between_rounds',dict(rows,LOSS=rows['LOSS']+[dict(frame='14000',stage='4')])),
 ('proxy_at_advance',dict(rows,FIGHT=[dict(r,human='1:1') if r['frame']=='15647' else r for r in rows['FIGHT']])),
):
 try:gate(broken)
 except AssertionError:faults.append(name)
 else:raise AssertionError('Paid clear fault accepted')
costs=[]
for i,r in enumerate(rows['STAGE']):
 nxt=rows['STAGE'][i+1] if i+1<len(rows['STAGE']) else None
 costs.append(dict(stage=int(r['stage']),firstNativeFight=int(r['frame']),fieldCostToNextStage=int(nxt['frame'])-int(r['frame']) if nxt else None,actualPaidLosses=sum(l['stage']==r['stage'] for l in rows['LOSS'])))
report=dict(currentKungFirstPaidMatchAccepted=True,clear=clear,rejectedFaults=faults,
 baselineKungFieldCost=16802,currentKungFieldCost=clear['fieldCost'],kungFieldsSaved=16802-clear['fieldCost'],
 actualLaterStageCosts=costs,ownSubZeroIndividualRounds=[r for r in rows['WIN'] if r['stage']=='11' and r['slot']=='1'],
 ownEarlyLegEntryObservationIntentionallyDeferred=True,fullCampaignShorteningAccepted=False,
 bossClearAccepted=False,fullPortAccepted=False,logSHA256=sync.sha(path))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(clear=clear,rejectedFaults=faults,laterCosts=costs,kungFieldsSaved=report['kungFieldsSaved'])))
