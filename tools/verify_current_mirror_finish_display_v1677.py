"""Current native mirror finisher components, sampled DMA/scanout, retirement.

Exact runtime copying/presentation proof, not all donor-art/choreography/audio
or all fatalities acceptance. Reuse original native replay without waiving its
component, actual palette, visible-pose or retirement contracts.
"""
import argparse,hashlib,json,re,struct,zlib
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import verify_current_natural_mirror_finish_v1674 as state
import verify_current_ground_shadow_v1269 as graphics_model
import verify_finish_display_v798 as native
ROOT=state.ROOT
_data_original=native.raster.data
_data_cache={}
def data_once(folder):
 key=str(Path(folder).resolve())
 if key not in _data_cache:
  _data_cache.clear();_data_cache[key]=_data_original(folder)
 return _data_cache[key]
native.raster.data=data_once
def verify(name,side):
 case=f'audit_v1675_{name}_mirror_finish_winner_p{side}_confirm_p1'
 baseline_case=f'audit_v1672_{name}_mirror_finish_winner_p{side}_confirm_p1'
 folder=ROOT/case;baseline_folder=ROOT/baseline_case;identity={'kano':17,'sonya':18}[name]
 pins={}
 def pin(path,wanted=None):
  path=Path(path);actual=state.digest(path);assert wanted is None or actual==wanted,'Changed input '+str(path);pins[str(path)]=actual
 baseline_path=ROOT/'audit_v1674_current_natural_mirror_finish_checked/report.json'
 baseline=json.loads(baseline_path.read_text());assert baseline['passed'] and baseline_case in baseline['cases'];pin(baseline_path)
 for file,wanted in baseline['inputHashes'].items():pin(file,wanted)
 log=(folder/'run.log').read_text(encoding='utf-8-sig')
 assert not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',log,re.I)
 launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 build=json.loads((ROOT/state.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
 assert launch['exit_code']==0 and launch['candidate']==state.CANDIDATE
 assert launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256']
 assert launch['winner']==side and launch['player']==name and launch['seconds']==95 and launch['confirm_first']==1
 assert launch['assistance']=='none' and launch['guest_writes']==0 and launch['cheats_enabled'] is False
 before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
 assert before==launch['input_hashes'] and all(before.get(p)==h for p,h in build['input_hashes'].items()),'Full before/after compiled-input binding'
 for file,wanted in launch['input_hashes'].items():
  pin(file,wanted)
  if Path(file).suffix in ('.ps1','.lua','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
 pin(folder/'input_hashes_before.json')
 # Read-only render observation must not change even one native input/state
 # event in the independently accepted fresh unassisted mirror sequence.
 tags={'INPUT','FLAG_WRITE','FIRST_LIVE','ACTION','WRAP','MODE','HEALTH','WIN','RESULT','CONFIRM','FINISH_STATE','FINISH_FIFO'}
 actual=[(t,r) for t,r in state.rows(log) if t in tags]
 expected=[(t,r) for t,r in state.rows((baseline_folder/'run.log').read_text(encoding='utf-8-sig')) if t in tags]
 assert actual==expected,'Render observation changed accepted physical/native chronology'
 for t,r in actual:
  if t=='FINISH_STATE' or t=='PALETTE':
   assert (folder/r['file']).read_bytes()==(baseline_folder/r['file']).read_bytes(),'Actual hardware palette changed'
 for file in ('mk2ks_natural_mirror_finish_v1166.lua','mk2ks_natural_mirror_finish_display_v1176.lua'):
  source=(ROOT/file).read_text()
  assert not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',source),'Read-only physical/observer source'
 guest,_,payload=state.current.expected()
 assert (folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual current guest'
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 groups,_,_,_,_=native.raster.data(folder)
 # Bind captured imported graphics to independent immutable ROM-chip bytes,
 # rather than treating the runtime graphics dump as its own source oracle.
 imported=bytearray(graphics_model.graphics(pins))
 for header,magic,source,dest in ((0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),(0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
  assert payload[header:header+4]==magic,'Current native effect allocation'
  first,count,destination=struct.unpack_from('<III',payload,header+4)
  assert first==source and destination==dest and count>0,'Exact native effect transfer'
  imported[dest:dest+count]=payload[source:source+count]
 assert payload[0x1e0000:0x1e0004]==b'KKS2'
 orb_size=struct.unpack_from('<I',payload,0x1e0008)[0];assert 0<orb_size<=0x1c000
 imported[0x1e0c000:0x1e0c000+orb_size]=payload[0x1e4000:0x1e4000+orb_size]
 source_records=0
 for capture in groups['FLOOR_GFX']:
  first,count=capture['first'],capture['bytes'];last=first+count
  assert 0<=first<last<=len(imported),'Actual graphics range'
  assert bytes.fromhex(capture['data'])==imported[first:last],'Every actual stock/imported/UI/effect stream equals independent ROM/payload source'
  source_records+=1
 assert source_records>30,'Positive independently sourced whole-scene graphics coverage'
 assert len(groups['FLOOR_BEGIN'])==len(groups['FLOOR_RESULT'])==1
 begin=groups['FLOOR_BEGIN'][0];result=groups['FLOOR_RESULT'][0]
 assert begin['human_slot']==side and begin['id']==identity and begin['entry']==(0xfffaae00 if name=='kano' else 0xfffab200)
 assert begin['origin']==baseline['cases'][baseline_case]['action']==result['origin']
 cache=native.composites(groups,payload,guest,(identity,identity),guest,side)
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
 for file in ('tools/verify_current_mirror_finish_display_v1677.py','tools/verify_current_natural_mirror_finish_v1674.py',
  'tools/verify_finish_display_v798.py','tools/inspect_finish_display_v680_v1.py'):
  pin(ROOT/file)
 return dict(passed=True,case=case,fighter=name,winner=side,nativeAlternateSlot=2,
  cache=cache,palette=palettes,replayed=drawn,heldScanout=held,
  visiblePoses={s:[f'{p:08X}' for p in sorted(v)] for s,v in visible.items()},
  nativeTeardown=teardown,postTransitionReplayedSamples=len(after),inputHashes=pins,
  independentlySourceBoundGraphicsRecords=source_records,
  naturalMirrorSampledRenderAccepted=True,allFatalityArtAccepted=False,
  donorChoreographyAccepted=False,audioAccepted=False,allArenasAccepted=False,fullPortAccepted=False)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--winner',type=int,choices=(1,2),required=True);args=parser.parse_args()
 out=ROOT/f'audit_v1677_{args.fighter}_mirror_finish_p{args.winner}_render_checked'
 assert not out.exists(),'Preserve rendering evidence'
 try:report=verify(args.fighter,args.winner)
 except Exception as error:
  report=dict(passed=False,error=str(error),fighter=args.fighter,winner=args.winner,fullPortAccepted=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','replayed','cache','palette')},indent=2))
 raise SystemExit(0 if report['passed'] else 1)
