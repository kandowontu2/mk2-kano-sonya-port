"""Record actual corrected captures and bounded native primary55 pose coverage."""
import json
from pathlib import Path
import verify_stock_scorpion_secondary_v1222 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1225_stock_secondary_visual_review';assert not OUT.exists()
inventory_path=ROOT/'audit_v1223_stock_secondary_contacts/inventory.json'
inventory=json.loads(inventory_path.read_text());assert inventory['sceneCount']==102
state=json.loads((proof.OUT/'report.json').read_text());assert state['passed']
encoding_path=ROOT/'audit_v1221_native_headed_reaction_encoding_checked/report.json';encoding=json.loads(encoding_path.read_text());assert encoding['passed']
pins={str(inventory_path):proof.state.digest(inventory_path),str(encoding_path):proof.state.digest(encoding_path)}
payload=(ROOT/proof.headed.CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
import struct
u=lambda at:struct.unpack_from('<I',payload,at)[0]
cases=[]
for record in inventory['cases']:
 key=record['case'];folder=ROOT/f'audit_v1220_secondary_{key}';start=state['cases'][key]['actionFrame'];side=state['cases'][key]['victimSlot']
 for scene in record['scenes']:
  path=Path(scene['path']);assert proof.state.digest(path)==scene['sha256'];pins[str(path)]=scene['sha256']
 sheet=Path(record['sheet']);assert proof.state.digest(sheet)==record['sha256'];pins[str(sheet)]=record['sha256']
 stock=key.startswith('control_');headed=[];coverage=[]
 log_path=folder/'run.log';log=log_path.read_text(encoding='utf-8-sig');pins[str(log_path)]=proof.state.digest(log_path)
 if stock:
  baseline=ROOT/f'audit_v1211_secondary_{key}'
  for age in range(0,601,10):
   current=folder/'snap'/f'stock_head_{start}_{age:03d}.png';old=baseline/'snap'/current.name
   assert current.read_bytes()==old.read_bytes(),'Changed original stock control capture'
   pins[str(current)]=proof.state.digest(current);pins[str(old)]=proof.state.digest(old)
  assert (folder/'snap/continue_4080.png').read_bytes()==(baseline/'snap/continue_4080.png').read_bytes()
  pins[str(baseline/'snap/continue_4080.png')]=proof.state.digest(baseline/'snap/continue_4080.png')
 else:
  base=0x100000 if key.startswith('kano') else 0x104000
  script=(u(base+55*4)-0xfe800000)//8;headed=[u(script+i*4) for i in range(5)]
  art=proof.state.rows(log,'MK2_ROLLING_HEAD_V1003')
  states=[r for t,r in art if t=='FIRE_STATE' and int(r['slot'])==side and 27+side<=int(r['age'])<71+side]
  assert {int(r['pose'],16) for r in states}==set(headed),'All original five headed reaction poses actually publish'
  assert all(r['id']==r['roster']==str(state['cases'][key]['trueVictimID']) for r in states)
  draws=[r for t,r in art if t=='DMA' and r['fifo_actor']==state['cases'][key]['actualPrimaryLookups'][0]['actor'] and 27+side<=int(r['frame'])-start<71+side]
  assert {int(r['fifo_pose'],16) for r in draws}==set(headed) and all(r['queue_match']=='1' for r in draws),'All five true-body poses reach actual FIFO/DMA'
  coverage=[dict(pose=f'{pose:08X}',actualNativeDraws=sum(int(r['fifo_pose'],16)==pose for r in draws)) for pose in headed]
 cases.append(dict(case=key,actualScenesReviewed=17,reviewer='main_agent_actual_view_image',
  correctedHeadedBodyReactionVisuallyAccepted=True,currentContinueScreenVisuallyAccepted=True,
  originalStockAll62CapturesByteIdenticalToPrior=stock,headedBodyNativeDrawCoverage=coverage,
  findings=['Actual headed victim remains visible through spear reaction; no knife/ring body substitution.',
   'Owned severed upper torso and lower stump, original Scorpion choreography, win/fatality and clean continue present.',
   'This manual sample is not an all-pixel/all-arena/alternate/audio/full-port proof.']))
report=dict(passed=True,candidate=proof.headed.CANDIDATE,manualVisualReviewComplete=True,sceneCount=102,
 cases=cases,inputHashes=pins,correctedHeadedBodyReactionVisuallyAccepted=True,
 currentContinueScreenVisuallyAccepted=True,allFiveHeadedBodyPosesActuallyDraw=True,
 fullScreenDMAReplayAccepted=False,allFatalityArtAccepted=False,allFloorShadowsAccepted=False,
 allSelectionGraphicsAccepted=False,audioAccepted=False,alternateCostumesAccepted=False,
 fullPortAccepted=False,gameDataChanged=True,compiledCodeChanged=False)
OUT.mkdir();(OUT/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print('102 corrected actual scenes reviewed; five true-body headed poses draw in each added-victim case; 124 stock captures unchanged',flush=True)
