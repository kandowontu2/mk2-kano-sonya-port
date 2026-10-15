"""Exact proven-route prefix and current same-paid native match progress."""
import json,re
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT
old=root/'audit_current_sonya_p1_subzero_short_leg_runtime/run.log'
new=root/'audit_current_sonya_p1_liukang_short_leg_runtime/run.log'
out=root/'audit_current_sonya_p1_liukang_short_leg_progress_checked'
assert not out.exists()
terminal=json.loads((new.parent/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['limitReason'] in (None,'wall_limit')
def prefix(path):
 return [s for s in path.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and int(re.search(r'\bframe=(\d+)',s)[1])<=93653]
assert prefix(old)==prefix(new)
rows=load(new)
assert all(r['human']=='18:18' and r['writes']=='0' and r['assistance']=='none' for r in rows['FIGHT'])
actual=[]
for r in rows['FIGHT']:
 pair=dict(stage=int(r['stage']),cpu=r['cpu'])
 if pair not in actual:actual.append(pair)
def certify(rows,stage,nextstage):
 advance=next((r for r in rows['FIGHT'] if int(r['stage'])==nextstage),None)
 if advance is None:return None
 attempt=[r for r in rows['FIGHT'] if int(r['stage'])==stage and int(r['frame'])<int(advance['frame'])][-1]
 assert attempt['human']=='18:18' and advance['human']=='18:18' and advance['selection']==attempt['selection']
 lo,hi=int(attempt['frame']),int(advance['frame'])
 allwins=[r for r in rows['WIN'] if int(r['stage'])==stage and lo<int(r['frame'])<hi]
 wins=[r for r in allwins if r['slot']=='1']
 assert len(wins)==2
 assert len([r for r in allwins if r['slot']=='2'])<2
 for r in wins:
  hp=list(map(int,r['health'].split(',')))
  assert r['slot']=='1' and r['id']=='18' and r['entry']=='FFFEFA40' and r['pc']=='FF8296B0' and hp[0]>0 and hp[1]==0
 assert not any(lo<int(r['frame'])<hi for r in rows['LOSS'])
 assert not any(lo<int(r['frame'])<hi for r in rows.get('SELECT',[]))
 return dict(attempt=attempt,wins=wins,opponentRoundWins=[r for r in allwins if r['slot']=='2'],advance=advance)
clears={}
faults=[]
for stage,nxt in ((11,12),(12,14),(14,15),(15,16)):
 clear=certify(rows,stage,nxt)
 if clear is None:continue
 clears[str(stage)]=clear
 lastwin=clear['wins'][-1]['frame'];advanceframe=clear['advance']['frame']
 for name,broken in (
  ('missing_round',dict(rows,WIN=[r for r in rows['WIN'] if r['frame']!=lastwin])),
  ('wrong_human',dict(rows,FIGHT=[dict(r,human='1:1') if r['frame']==advanceframe else r for r in rows['FIGHT']])),
  ('continued_between_rounds',dict(rows,LOSS=rows['LOSS']+[dict(frame=lastwin,stage=str(stage))])),
  ('different_paid_selection',dict(rows,FIGHT=[dict(r,selection='999') if r['frame']==advanceframe else r for r in rows['FIGHT']])),
 ):
  try:certify(broken,stage,nxt)
  except AssertionError:faults.append(str(stage)+':'+name)
  else:raise AssertionError('Fault accepted: '+name)
report=dict(samePaidNativeClears=clears,rejectedFaults=faults,
 unchangedPhysicalAndNativePrefixThrough=93653,matchingPrefixRecords=len(prefix(old)),
 actualStageCPUIdentities=actual,physicalLiuLegPlans=len(rows.get('SONYA_LIUKANG_LEG_PLAN',[])),
 ownedStage12LegEntries=[r for r in rows.get('SPECIAL',[]) if r['stage']=='12' and r['move']=='leg'],
 ownStage12RoundWins=[r for r in rows['WIN'] if r['stage']=='12' and r['slot']=='1'],
 endingAccepted=False,fullCampaignAccepted=False,fullPortAccepted=False,
 terminal=terminal,logSHA256=sync.sha(new))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(clearStages=list(clears),rejectedFaults=faults,actualStageCPUIdentities=actual,physicalLiuLegPlans=report['physicalLiuLegPlans'],ownedStage12LegEntryCount=len(report['ownedStage12LegEntries']),ownStage12RoundWins=report['ownStage12RoundWins'],terminal=terminal,logSHA256=report['logSHA256'])))
