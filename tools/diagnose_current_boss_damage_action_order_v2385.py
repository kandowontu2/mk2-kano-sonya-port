"""Read-only diagnostic: actual action at each native damage store versus pre-input field.
The complete ordered action ledger is checked; no guest or captured bytes are changed.
This does not rerun the prior full source/campaign verifier or certify every move.
"""
import json, argparse
from pathlib import Path
from collections import Counter
import verify_current_shao_grounded_hp_boss_ledger_v2366 as ledger
ROOT=ledger.ROOT

def classify(rows,side):
 fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'}
 current=None;items=[]
 for r in rows:
  f=fields.get(r['frame'])
  if r['tag']=='BOSS_FIELD':
   current=dict(frame=r['frame'],actor=r['human_actor'],main=r['human_main'],action=r['human_action'])
  elif r['tag']=='BOSS_ACTION'and f:
   assert current and current['frame']==r['frame'] and current['actor']==r['actor'] and current['main']==r['main'],'Ordered action belongs to this actual field'
   assert current['action']==r['before'],'Every original store follows the preceding same-field action'
   current['action']=r['after']
  elif r['tag']=='HEALTH'and f and r['pc']==0xff836700 and r['slot']==3-side and r['after']<r['before']and r['a8']==f['human_actor']and r['a13']==f['human_main']:
   assert current and current['frame']==r['frame'] and current['actor']==r['a8']and current['main']==r['a13'],'Actual damage writer action is independently tracked'
   items.append(dict(frame=r['frame'],event=r['event'],stage=f['stage'],preInputAction=f['human_action'],actualDamageWriterAction=current['action'],damage=r['before']-r['after'],humanActor=r['a8'],humanMain=r['a13']))
 return items

def verify():
 pins={};cases={}
 guest=ledger.native.current_source.expected()[0]
 for case,(fighter,side,capture,positive)in ledger.CASES.items():
  folder=ROOT/capture;proof_path=ROOT/positive/'report.json'
  proof=json.loads(proof_path.read_text());assert proof['passed']and proof['bounded_campaign_evidence_proven']
  log=folder/'run.log';raw=(folder/'guest_maincpu.bin')
  assert raw.read_bytes()==guest,'Whole actual captured guest equals independent source reconstruction'
  rows=ledger.native.parse(log.read_text(encoding='utf-8-sig'),side,fighter);ledger.check(rows,17 if fighter=='kano'else 18,side)
  items=classify(rows,side)
  pre=[r for r in items if r['preInputAction']==0x107]
  actual=[r for r in items if r['actualDamageWriterAction']==0x107]
  changed=[r for r in items if (r['preInputAction']==0x107)!=(r['actualDamageWriterAction']==0x107)]
  assert sum(r['damage']for r in pre)==proof['actualBossUppercutDamage'],'Reproduces prior pre-input classification exactly'
  cases[case]=dict(ownedBossDamageStores=len(items),preInput107Damage=sum(r['damage']for r in pre),actualWriter107Damage=sum(r['damage']for r in actual),classificationDifferenceStores=len(changed),differences=changed,allActualWriterActions={f'{action:04X}':sum(r['damage']for r in items if r['actualDamageWriterAction']==action)for action in sorted(set(r['actualDamageWriterAction']for r in items))})
  for path in(log,raw,proof_path):pins[str(path.resolve())]=ledger.launch.sha(path)
 pins[str(Path(__file__).resolve())]=ledger.launch.sha(__file__);ledger.launch.module_pins(pins)
 return dict(passed=True,cases=cases,inputHashes=pins,gameOrCaptureModified=False,priorFullCampaignGraphRerun=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();assert not a.output.exists(),'Immutable diagnostic'
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:{key:value for key,value in row.items()if key!='differences'}for k,row in r['cases'].items()},indent=2),flush=True)

