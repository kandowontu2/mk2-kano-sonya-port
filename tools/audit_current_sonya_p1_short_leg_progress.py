"""Same-paid-attempt progress, unchanged prefix, and bounded passive HP evidence."""
import json,re
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT
old=root/'audit_current_sonya_p1_subzero_guard_release_leg_runtime/run.log'
new=root/'audit_current_sonya_p1_subzero_short_leg_runtime/run.log'
out=root/'audit_current_sonya_p1_short_leg_progress_checked'
assert not out.exists()
def prefix(path):
 return [s for s in path.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and int(re.search(r'\bframe=(\d+)',s)[1])<=73681]
assert prefix(old)==prefix(new)
rows=load(new)
def certify(rows):
 advance=next(r for r in rows['FIGHT'] if r['stage']=='12')
 attempt=[r for r in rows['FIGHT'] if r['stage']=='11' and int(r['frame'])<int(advance['frame'])][-1]
 assert attempt['human']=='18:18' and attempt['cpu']=='8:8'
 assert advance['human']=='18:18' and advance['cpu']=='1:1' and advance['selection']==attempt['selection']
 lo,hi=int(attempt['frame']),int(advance['frame'])
 wins=[r for r in rows['WIN'] if r['stage']=='11' and lo<int(r['frame'])<hi]
 assert len(wins)==2
 for r in wins:
  hp=list(map(int,r['health'].split(',')))
  assert r['slot']=='1' and r['id']=='18' and r['entry']=='FFFEFA40' and r['pc']=='FF8296B0' and hp[0]>0 and hp[1]==0
 assert not any(lo<int(r['frame'])<hi for r in rows['LOSS'])
 assert not any(lo<int(r['frame'])<hi for r in rows.get('SELECT',[]))
 return dict(attempt=attempt,wins=wins,advance=advance)
clear=certify(rows)
faults=[]
for name,broken in (
 ('missing_round',dict(rows,WIN=[r for r in rows['WIN'] if r['frame']!='93033'])),
 ('wrong_human',dict(rows,FIGHT=[dict(r,human='1:1') if r['frame']=='93653' else r for r in rows['FIGHT']])),
 ('continued_between_rounds',dict(rows,LOSS=rows['LOSS']+[dict(frame='92500',stage='11')])),
 ('different_paid_selection',dict(rows,FIGHT=[dict(r,selection='999') if r['frame']=='93653' else r for r in rows['FIGHT']])),
):
 try:certify(broken)
 except AssertionError:faults.append(name)
 else:raise AssertionError('Fault accepted: '+name)
legs=[r for r in rows.get('SPECIAL',[]) if r['move']=='leg' and r['stage']=='11']
cpu_damage=[]
for r in rows['HEALTH']:
 if r['slot']!='2' or int(r['before'])-int(r['after'])!=35 or r['pc']!='FF836700':continue
 matching=[l for l in legs if 0<=int(r['frame'])-int(l['frame'])<=80 and r['a13']==l['main']]
 if matching:cpu_damage.append(dict(health=r,legEntry=matching[-1],classification='native 35HP callback during same Main leg-entry window; not complete hit/recovery coverage'))
actual=[]
for r in rows['FIGHT']:
 pair=dict(stage=int(r['stage']),cpu=r['cpu'])
 if pair not in actual:actual.append(pair)
report=dict(currentTrueSonyaP1SubZeroSamePaidMatchAccepted=True,clear=clear,
 rejectedFaults=faults,unchangedPhysicalAndNativePrefixThrough=73681,matchingPrefixRecords=len(prefix(old)),
 actualStageCPUIdentities=actual,ownedNativeLegEntries=len(legs),
 native35HPCallbacksDuringMatchingLegMainWindow=cpu_damage,
 stage12IndividualOwnWins=[r for r in rows['WIN'] if r['stage']=='12' and r['slot']=='1'],
 stage12MatchAccepted=False,endingAccepted=False,fullCampaignAccepted=False,fullPortAccepted=False,
 logSHA256=sync.sha(new))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(clear=clear,rejectedFaults=faults,prefixRecords=len(prefix(old)),actualStageCPUIdentities=actual,legWindow35HPCallbacks=len(cpu_damage),logSHA256=sync.sha(new))))
