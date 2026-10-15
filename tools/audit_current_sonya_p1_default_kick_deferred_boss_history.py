"""Original retained trace and actual per-paid-attempt round results; no isolated-win merging."""
import json,re
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify();root=sync.ROOT
old=root/'audit_current_sonya_p1_boss_light_runtime/run.log'
case=root/'audit_current_sonya_p1_default_kick_deferred_runtime'
out=root/'audit_current_sonya_p1_default_kick_deferred_boss_history_checked';assert not out.exists()
def retained(path):
 return [s for s in path.read_text().splitlines() if s.startswith('MK2_NAT_CAMPAIGN_') and not s.startswith('MK2_NAT_CAMPAIGN_SPECIAL ') and int(re.search(r'\bframe=(\d+)',s)[1])<=111442]
assert retained(old)==retained(case/'run.log')
rows=load(case/'run.log');terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['observerSha256']=='9E2B00213DED0CFDBCE466C3CCD65575ECB9C769D0004AE1839E300CAA56D173' and terminal['limitReason'] in (None,'wall_limit')
all_fights=rows['FIGHT'];attempts=[]
for stage in (15,16):
 unique=[]
 for r in all_fights:
  if int(r['stage'])==stage and r['selection'] not in [x['selection'] for x in unique]:unique.append(r)
 for start in unique:
  assert start['human']=='18:18' and start['writes']=='0' and start['assistance']=='none'
  lo=int(start['frame'])
  next_attempt=next((r for r in all_fights if int(r['frame'])>lo and (r['selection']!=start['selection'] or int(r['stage'])!=stage)),None)
  hi=int(next_attempt['frame']) if next_attempt else 10**9
  wins=[r for r in rows['WIN'] if int(r['stage'])==stage and lo<int(r['frame'])<hi]
  own=[r for r in wins if r['slot']=='1'];cpu=[r for r in wins if r['slot']=='2']
  for r in own:
   hp=list(map(int,r['health'].split(',')));assert r['id']=='18' and r['entry']=='FFFEFA40' and r['pc']=='FF8296B0' and hp[0]>0 and hp[1]==0
  loss=[r for r in rows['LOSS'] if int(r['stage'])==stage and lo<int(r['frame'])<hi]
  advance=next_attempt if next_attempt and int(next_attempt['stage'])!=stage else None
  if loss:assert len(own)<2 and len(cpu)==2
  if advance:assert len(own)==2 and len(cpu)<2 and not loss and advance['selection']==start['selection']
  attempts.append(dict(start=start,ownNativeRoundWins=own,cpuNativeRoundWins=cpu,paidLoss=loss,nativeAdvance=advance,
   classification='native match clear with same paid advance' if advance else 'native paid match loss' if loss else 'censored; no later match outcome observed'))
report=dict(retainedNativeAndPhysicalHistoryExactlyEquivalentThrough=111442,matchingRecords=len(retained(old)),excludedOnlyIntentionalEarlySpecialEntryTags=True,
 actualPaidBossAttempts=attempts,endingEvidence=[r for tag in ('ENDING_STARTED','ENDING_COMPLETED','PICTURE','TEXT') for r in rows.get(tag,[])],
 endingAccepted=False,wholeCampaignAccepted=False,fullPortAccepted=False,
 terminal=terminal,logSHA256=sync.sha(case/'run.log'))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(matchingRecords=report['matchingRecords'],bossAttempts=attempts,terminal=terminal,logSHA256=report['logSHA256'])))
