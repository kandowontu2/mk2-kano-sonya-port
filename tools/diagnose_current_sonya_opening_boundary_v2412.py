"""Diagnose a terminally clipped natural Sonya selection without accepting it.
No identity/game/observer gate is waived, and no recorded or guest bytes change.
"""
import json,argparse
from pathlib import Path
import verify_current_boss_shao_opening_guard_v2397 as native
ROOT=native.ROOT
def verify():
 folder=ROOT/'audit_v2398_current_sonya_p1_shao_taunt_guard_campaign'
 failed_path=ROOT/'audit_v2399_current_sonya_p1_shao_taunt_guard_checked/report.json'
 failed=json.loads(failed_path.read_text())
 assert not failed['passed']and failed['errors']==['Own true ID before native confirm']
 pins=dict(failed['inputHashes'])
 for file,wanted in pins.items():assert native.current_launch.sha(file)==wanted,'Unchanged failed actual graph '+file
 pins[str(failed_path)]=native.current_launch.sha(failed_path)
 rows=native.parse((folder/'run.log').read_text(encoding='utf-8-sig'),1,'sonya')
 selections=[r for r in rows if r['tag']=='SELECT'];final=next(r for r in rows if r['tag']=='RESULT')
 last=selections[-1];first_due=last['frame']+130;second_due=last['frame']+146;confirm_due=last['frame']+148
 assert last['number']==22 and last['frame']==131231 and final['frame']==131297 and final['frame']<first_due
 assert not any(r['tag']=='SELECT_ID'and r['number']==last['number']for r in rows),'No wrong ID observation: final confirmation observations have not occurred'
 for selection in selections[:-1]:
  confirmed=[r for r in rows if r['tag']=='SELECT_ID'and r['number']==selection['number']]
  assert len(confirmed)==2 and all(r['roster']==18 and r['state']==3 for r in confirmed),'Every completed actual selection keeps true Sonya18'
  assert [r['frame']-selection['frame']for r in confirmed]==[130,146],'Original source-exact selection observation timing'
 assert all(r['human']=='18:18'for r in rows if r['tag']=='LIVE'),'Every actual live Sonya identity remains18'
 source=(ROOT/'mk2ks_natural_campaign_boss_shao_opening_guard_v2395.lua').read_text()
 assert 'if age==130 or age==146 then'in source and "if age>=148 and age<156 then press('High Punch')end"in source
 pins[str(Path(__file__).resolve())]=native.current_launch.sha(__file__);native.current_launch.module_pins(pins)
 return dict(passed=True,originalFullCampaignStillRejected=True,completedTrueSonyaSelections=21,
  incompleteSelection=22,lastSelectionFrame=last['frame'],terminalFrame=final['frame'],
  firstMissingObservationDue=first_due,secondMissingObservationDue=second_due,confirmInputDue=confirm_due,
  reason='Actual run ended66fields into selection,64fields before its first own-ID observation and82fields before physical HP confirmation. No wrong confirmed or live identity is present. Preserve this incomplete run; obtain a fresh longer complete-selection capture under the same driver and unchanged gates.',
  inputHashes=pins,gameOrCaptureModified=False,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();assert not a.output.exists()
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
