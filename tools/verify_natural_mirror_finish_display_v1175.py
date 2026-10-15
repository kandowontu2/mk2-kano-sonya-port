"""Current native mirror finisher components, sampled DMA/scanout, retirement.

Exact runtime copying/presentation proof, not all donor-art/choreography/audio
or all fatalities acceptance. Reuse original native replay without waiving its
component, actual palette, visible-pose or retirement contracts.
"""
import argparse,json,re
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import verify_natural_mirror_finish_v1169 as state
import verify_finish_display_v798 as native
ROOT=state.ROOT
def verify(name,side):
 case=f'audit_v1174_{name}_mirror_finish_winner_p{side}_confirm_p1'
 baseline_case=f'audit_v1167_{name}_mirror_finish_winner_p{side}_confirm_p1'
 folder=ROOT/case;baseline_folder=ROOT/baseline_case;identity={'kano':17,'sonya':18}[name]
 pins={}
 def pin(path,wanted=None):
  path=Path(path);actual=state.digest(path);assert wanted is None or actual==wanted,'Changed input '+str(path);pins[str(path)]=actual
 baseline_path=ROOT/'audit_v1169_natural_mirror_finish_checked/report.json'
 baseline=json.loads(baseline_path.read_text());assert baseline['passed'] and baseline_case in baseline['cases'];pin(baseline_path)
 for file,wanted in baseline['inputHashes'].items():pin(file,wanted)
 log=(folder/'run.log').read_text(encoding='utf-8-sig')
 assert not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',log,re.I)
 launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 build=json.loads((ROOT/state.split.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
 assert launch['exit_code']==0 and launch['candidate']==state.split.CANDIDATE
 assert launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256']
 assert launch['winner']==side and launch['player']==name and launch['seconds']==95 and launch['confirm_first']==1
 assert launch['assistance']=='none' and launch['guest_writes']==0 and launch['cheats_enabled'] is False
 for file,wanted in launch['input_hashes'].items():pin(file,wanted)
 # Read-only render observation must not change even one native input/state
 # event in the independently accepted fresh unassisted mirror sequence.
 tags={'INPUT','FLAG_WRITE','FIRST_LIVE','ACTION','WRAP','MODE','HEALTH','WIN','RESULT','CONFIRM','FINISH_STATE','FINISH_FIFO'}
 actual=[(t,r) for t,r in state.rows(log) if t in tags]
 expected=[(t,r) for t,r in state.rows((baseline_folder/'run.log').read_text(encoding='utf-8-sig')) if t in tags]
 assert actual==expected,'Render observation changed accepted physical/native chronology'
 for t,r in actual:
  if t=='FINISH_STATE' or t=='PALETTE':
   assert (folder/r['file']).read_bytes()==(baseline_folder/r['file']).read_bytes(),'Actual hardware palette changed'
 for file in ('mk2ks_natural_mirror_finish_v1166.lua','mk2ks_natural_mirror_finish_display_v1173.lua'):
  source=(ROOT/file).read_text()
  assert not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',source),'Read-only physical/observer source'
 guest,_,_,payload=state.split.reconstruct()
 assert (folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual current guest'
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 groups,_,_,_,_=native.raster.data(folder)
 assert len(groups['FLOOR_BEGIN'])==len(groups['FLOOR_RESULT'])==1
 begin=groups['FLOOR_BEGIN'][0];result=groups['FLOOR_RESULT'][0]
 assert begin['human_slot']==side and begin['id']==identity and begin['entry']==(0xfffaae00 if name=='kano' else 0xfffab200)
 assert begin['origin']==baseline['cases'][baseline_case]['action']==result['origin']
 cache=native.composites(groups,payload,stock,(identity,identity),guest,side)
 palettes=native.palettes(folder,groups,guest,(identity,identity),side)
 print(case+' native components/palettes accepted; replaying actual passes',flush=True)
 drawn=native.raster.inspect(folder)
 assert drawn['frames']>100 and all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in drawn['records'])
 publications={(r['frame'],r['cursor']):r for r in groups['FLOOR_QUEUE']};dispatched=defaultdict(list)
 for r in groups['FLOOR_QUEUE_DISPATCH']:dispatched[r['frame']].append(publications[r['queue_frame'],r['cursor']])
 visible=defaultdict(set)
 for record in drawn['records']:
  for q in dispatched[record['frame']-1]:
   if record['body'][q['slot']]['pixels']>0:visible[q['slot']].add(q['pose'] if q['multipart'] else q['cache'])
 for slot in (1,2,3):
  required={int(p,16) for p in cache['poses'].get(slot,[]) if int(p,16)!=0}
  if slot==3:required|={int(p,16) for p in cache['single_frames']}
  assert required<=visible[slot],'Missing positively presented own/victim/effect pose slot'+str(slot)
 teardown=native.retirement(groups,begin,guest,(identity,identity),side)
 assert teardown>begin['origin']+150
 assert not any(r['slot']==3 for r in groups['FLOOR_QUEUE_DISPATCH'] if r['frame']>teardown)
 after=[r for r in drawn['records'] if r['frame']>teardown+1]
 assert len(after)>5 and all(r['body'][3]['pixels']==0 for r in after)
 snapshots={r['frame']:r for r in groups['FLOOR_SNAP']};displays={r['frame']:r for r in groups['FLOOR_DISPLAY']};held=[]
 for h in groups['FLOOR_HELD']:
  assert h['frame']==h['snapshot'] and h['reason']=='no_current_flip_or_prior_DMA'
  image=np.asarray(Image.open(folder/'snap'/snapshots[h['frame']]['file']).convert('RGB'))
  display=displays[h['frame']];assert all(h[k]==display[k] for k in ('start','control','tap'))
  checked=native.check_latch(image,(folder/h['file']).read_bytes(),(folder/display['palette_file']).read_bytes(),h['start'],h['control'],h['tap'])
  held.append(dict(frame=h['frame'],pixels=checked['pixels'],DMAReconstructed=False))
 assert result['snapshots']==drawn['frames']+len(held)==len(snapshots)
 for path in folder.rglob('*'):
  if path.is_file():pin(path)
 for file in ('tools/verify_natural_mirror_finish_display_v1175.py','tools/verify_natural_mirror_finish_v1169.py',
  'tools/verify_finish_display_v798.py','tools/inspect_finish_display_v680_v1.py'):
  pin(ROOT/file)
 return dict(passed=True,case=case,fighter=name,winner=side,nativeAlternateSlot=2,
  cache=cache,palette=palettes,replayed=drawn,heldScanout=held,
  visiblePoses={s:[f'{p:08X}' for p in sorted(v)] for s,v in visible.items()},
  nativeTeardown=teardown,postTransitionReplayedSamples=len(after),inputHashes=pins,
  naturalMirrorSampledRenderAccepted=True,allFatalityArtAccepted=False,
  donorChoreographyAccepted=False,audioAccepted=False,allArenasAccepted=False,fullPortAccepted=False)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--winner',type=int,choices=(1,2),required=True);args=parser.parse_args()
 out=ROOT/f'audit_v1175_{args.fighter}_mirror_finish_p{args.winner}_render_checked'
 assert not out.exists(),'Preserve rendering evidence'
 try:report=verify(args.fighter,args.winner)
 except Exception as error:
  report=dict(passed=False,error=str(error),fighter=args.fighter,winner=args.winner,fullPortAccepted=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','replayed','cache','palette')},indent=2))
 raise SystemExit(0 if report['passed'] else 1)
