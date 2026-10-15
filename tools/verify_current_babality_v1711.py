"""Current actual-input Babality performers/victims and rejection regression.
Original baby pixels, source palettes/floor anchors and native retirement;
not audio, every arena, every field's full raster or full-port acceptance.
"""
import json,re,struct,hashlib,traceback
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_ground_throw_source_v1598 as current
import verify_native_babality_performers_v739 as baba
import run_current_babality_matrix_v1707 as matrix
ROOT=current.ROOT;OUT=ROOT/'audit_v1711_current_babality_checked'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
def verify(texts=None):
 pins={};summaries={}
 def pin(path,wanted=None):
  path=Path(path);key=str(path.resolve())
  if key not in pins:pins[key]=sha(path)
  assert wanted is None or wanted.upper()==pins[key],'Changed input '+key
 guest,_,payload=current.expected()
 buildpath=ROOT/current.NAME/'build-info.json';build=json.loads(buildpath.read_text(encoding='utf-8-sig'));pin(buildpath)
 pin(ROOT/current.NAME/'mkport_candidate.exe',build['executable_sha256'])
 pin(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
 for p,h in build['input_hashes'].items():pin(p,h)
 priorpath=ROOT/'audit_v794_current_babality_regression_checked/verification.json';prior=json.loads(priorpath.read_text());pin(priorpath)
 assert prior['boundedCurrentHumanBabalityRegressionAcceptance']
 oldpath=ROOT/'audit_v790_kano_friendship_p1/guest_maincpu.bin'
 wanted=prior['checked_inputs'].get(str(oldpath.resolve()));assert wanted,'Pinned historical Babality source guest'
 pin(oldpath,wanted);old=oldpath.read_bytes()
 off=lambda a:(a-0xff800000)//8
 for first,last in ((0xf9600,0xf98a0),(off(0xff87e120),off(0xff880000)),(0xff2c0,0xff2c0+19*4)):
  assert guest[first:last]==old[first:last],'Entire native Babality/action/own bindings unchanged from historical accepted implementation'
 originalpath=ROOT/'mk2/mk2-maincpu.bin';original=originalpath.read_bytes();pin(originalpath)
 refpath=ROOT/'audit_v726_original_baby_reference/reference.json';reference=json.loads(refpath.read_text());pin(refpath)
 for p,h in reference['input_hashes'].items():pin(p,h)
 assert guest[0xf9600:0xf9600+17*4]==original[off(0xff87f020):off(0xff87f020)+17*4]
 for name in ('kano','sonya'):
  ref=reference['records'][name];frame=bytearray.fromhex(ref['descriptor_hex'])
  struct.pack_into('<I',frame,8,ref['source_bits']+0x10000000)
  struct.pack_into('<I',frame,14,0xff800000+baba.v.PALETTES[name]*8)
  at=off(baba.v.FRAMES[name]);assert guest[at:at+len(frame)]==frame
  palette=bytes.fromhex(ref['palette_hex']);at=baba.v.PALETTES[name]
  assert guest[at:at+len(palette)]==palette
 baba.original_reference(ROOT)
 for name in ('audit_v734_original_babality_commands','audit_v735_original_babality_directions'):
  case=ROOT/name;pin(case/'result.json');pin(case/'run.log')
  for p,h in json.loads((case/'result.json').read_text(encoding='utf-8-sig'))['input_hashes'].items():pin(p,h)
 for winner,victim,label,side,command in matrix.SPECS:
  case=f'audit_v1710_{label}_p{side}' if winner=='kitana'and side==2 else f'audit_v1706_{label}_p{side}';folder=ROOT/case
  expected_seconds=180 if winner=='kitana'and side==2 else 95
  meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  assert meta['exit_code']==0 and meta['candidate']==current.NAME and meta['seconds']==expected_seconds
  assert (meta['winner'],meta['victim'],meta['winner_side'],meta['command_case'])==(winner,victim,side,command)
  assert meta['assistance']=='none'and meta['guest_writes']==0 and meta['cheats_enabled']is False
  assert meta['executable_sha256']==build['executable_sha256']and meta['payload_sha256']==build['payload_sha256']
  before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'));assert before==meta['input_hashes']
  assert all(before.get(p)==h for p,h in build['input_hashes'].items())
  for p,h in before.items():
   pin(p,h)
   if Path(p).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(p).name,h)
  driver=(folder/'input_sources/mk2ks_native_babality_performer_probe_v738.lua').read_text()
  assert not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|dofile\(',driver)
  assert '-nocheat' in (folder/'input_sources/run_current_babality_v1705.ps1').read_text()
  assert (folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual guest equals current independent source model'
  log=texts[case]if texts is not None else (folder/'run.log').read_text(encoding='utf-8-sig')
  assert not re.search(r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|Lua error|fatal error|stack traceback|access violation',log,re.I)
  rows=baba.v.records(log);initial=baba.v.entries(rows,'FINISH_WINDOW')
  assert len(initial)==1 and initial[0]['damage']=='322'and initial[0]['native_kos']=='2'
  damage=baba.v.entries(rows,'DAMAGE');health=161;kos=0
  for r in damage:
   assert int(r['before'])==health and 0<=int(r['after'])<health and r['pc']=='FF836700'
   health=int(r['after'])
   if health==0:kos+=1;health=161
  assert kos==2 and sum(int(r['before'])-int(r['after'])for r in damage)==322
  report=dict(winner=winner,victim=victim,side=side,command=command,originalBabyPixelChecks=[],unchangedStockFrames=0)
  if command=='positive':
   baba.v.runtime_check(rows,victim,side,reference,winner_id=baba.WINNERS[winner])
   baba.command_check(rows,winner,side,command)
   for r in baba.v.entries(rows,'FIELD'):
    if int(r['slot'])==side:
     assert int(r['id'])==int(r['roster'])==baba.WINNERS[winner]and r['actor']==r['owner']
   if victim in baba.v.FRAMES:
    photo=refpath.parent/f'{victim}_baby.png';pin(photo)
    sprite=np.asarray(Image.open(photo).convert('RGBA'))
    assert hashlib.sha256(sprite.tobytes()).hexdigest()==reference['records'][victim]['rgba_sha256']
    for age in (160,200,240):
     path=folder/'snap'/f'babality_{age}.png'
     origin,pixels=baba.v.image_match(np.asarray(Image.open(path).convert('RGB')),sprite)
     report['originalBabyPixelChecks'].append(dict(age=age,origin=origin,pixels=pixels))
   else:
    baseline=ROOT/f'audit_v793_stock_liu_p{side}'
    for age in range(0,721,8):
     path=baseline/'snap'/f'babality_{age}.png'
     expected=prior['checked_inputs'].get(str(path.resolve()));assert expected
     pin(path,expected)
     assert path.read_bytes()==(folder/'snap'/path.name).read_bytes(),'Stock complete native Babality scene unchanged'
    report['unchangedStockFrames']=91
  else:baba.negative_check(rows,winner,victim,side,command)
  captures=sorted((folder/'snap').glob('babality_*.png'),key=lambda p:int(p.stem.split('_')[-1]))
  assert [p.name for p in captures]==[f'babality_{age}.png'for age in range(0,721,8)]
  for path in captures:assert Image.open(path).size==(400,254);pin(path)
  for file in ('run.log','result.json','input_hashes_before.json','guest_maincpu.bin'):pin(folder/file)
  summaries[case]=report
 for module in (baba,baba.v,current,matrix):pin(Path(module.__file__))
 pin(__file__)
 return dict(passed=True,candidate=current.NAME,cases=summaries,inputHashes=pins,
  currentHumanBabalityPerformersVictimsAndRejectionAccepted=True,originalBabyArtPaletteAndFloorAccepted=True,
  unchangedStockWholeSceneSamples=182,exactFullEveryFieldRasterAccepted=False,audioAccepted=False,
  allArenasAccepted=False,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 assert not OUT.exists()
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2))
 raise SystemExit(0 if report['passed']else 1)
