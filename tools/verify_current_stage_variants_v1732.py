"""Current earned stage commands and cleanup; preserves all v807 state predicates.
Not full cinematic raster/audio, all victims or full port acceptance.
"""
import json,re,struct,hashlib,wave,traceback
from pathlib import Path
from PIL import Image
import verify_native_ground_throw_source_v1598 as current
import native_stage_variant_checks_v1731 as native
import verify_original_tomb_drop_provenance_v1726 as drop
import run_current_stage_matrix_v1713 as matrix
ROOT=current.ROOT;OUT=ROOT/'audit_v1732_current_stage_variants_checked'
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
def verify():
 pins={};reports={}
 drop_proof=drop.verify();assert drop_proof['passed']and drop_proof['originalRandomTombDropCauseAccepted']
 certified_drop_log=(ROOT/'audit_v1714_sonya_tomb_p2/run.log').read_text(encoding='utf-8-sig')
 def pin(path,wanted=None):
  path=Path(path);key=str(path.resolve())
  if key not in pins:pins[key]=sha(path)
  assert wanted is None or wanted.upper()==pins[key],'Changed proof input '+key
 for p,h in drop_proof['inputHashes'].items():pin(p,h)
 guest,_,payload=current.expected()
 buildpath=ROOT/current.NAME/'build-info.json';build=json.loads(buildpath.read_text(encoding='utf-8-sig'));pin(buildpath)
 pin(ROOT/current.NAME/'mkport_candidate.exe',build['executable_sha256'])
 pin(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
 for p,h in build['input_hashes'].items():pin(p,h)
 originalpath=ROOT/'mk2/mk2-maincpu.bin';pin(originalpath,'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23')
 original=originalpath.read_bytes()
 for first,last in ((0xff876d20,0xff877420),(0xff8bdde0,0xff8be210)):
  begin,end=(first-0xff800000)//8,(last-0xff800000)//8
  assert guest[begin:end]==original[begin:end],'Complete original native stage gates/actions unchanged'
 assert struct.unpack_from('<13H',guest,0xf5400)==(0x38,7,5,5,0,0,0,8,5,5,0,0,0)
 assert struct.unpack_from('<13H',guest,0xf5420)==(0x38,6,8,8,0,0,0,6,7,7,0,0,0)
 for fighter,side,label,arena,command in matrix.SPECS:
  folder=ROOT/f'audit_v1714_{fighter}_{label}_p{side}'
  metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
  manifest=json.loads((folder/'inputs_before.json').read_text(encoding='utf-8-sig'))
  assert metadata['exit_code']==0 and (metadata['winner'],metadata['side'],metadata['arena'],metadata['command_case'],metadata['seconds'])==(fighter,side,arena,command,900)
  assert metadata['candidate']==current.NAME and metadata['cheats_enabled']is False and metadata['guest_writes']==0 and metadata['assistance']=='none'
  assert metadata['executable_sha256']==build['executable_sha256']and metadata['payload_sha256']==build['payload_sha256']
  assert manifest==metadata['input_hashes']and all(manifest.get(p)==h for p,h in build['input_hashes'].items())
  for p,h in manifest.items():
   pin(p,h)
   if Path(p).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(p).name,h)
  driver=folder/'input_sources/mk2ks_native_stage_performer_v806.lua'
  assert driver.read_bytes()==(ROOT/driver.name).read_bytes()
  assert not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',driver.read_text())
  runner=(folder/'input_sources/run_current_stage_performer_v1712.ps1').read_text()
  assert all(s in runner for s in ('-nocheat','-noautoframeskip -frameskip 0','Remove-Item','-wavwrite',current.NAME))
  assert (folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual current guest exactly matches independent source'
  log=(folder/'run.log').read_text(encoding='utf-8-sig')
  assert not re.search(r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|Lua error|fatal error|stack traceback|access violation',log,re.I)
  report=native.check_log(log,fighter,side,arena,command,certified_drop_log=certified_drop_log)
  wavpath=folder/'native_mix.wav';pin(wavpath,metadata['mix_sha256'])
  with wave.open(str(wavpath),'rb')as wav:
   assert wav.getframerate()==48000 and wav.getsampwidth()==2 and wav.getnchannels()==2 and wav.getnframes()>48000
  captures=sorted((folder/'snap').glob('stage_age*.png'))
  assert len(captures)==(31 if report.get('native_action')else 0)
  for p in captures:
   assert Image.open(p).size==(400,254);pin(p)
  for p in ('run.log','result.json','inputs_before.json','guest_maincpu.bin'):pin(folder/p)
  report.update(fighter=fighter,side=side,displayInventory=len(captures));reports[folder.name]=report
 for module in (current,native,native.candidate,matrix,drop):pin(module.__file__)
 pin(__file__)
 return dict(passed=True,candidate=current.NAME,cases=reports,positiveCases=8,rejectionCases=12,inputHashes=pins,
  currentNativeStagePerformerInputAndRetirementAcceptance=True,allOtherOriginalStatePredicatesPreserved=True,originalHeldAndSourceBoundRandomDropVariantsAccepted=True,
  fullStageCinematicAcceptance=False,fullFinisherAcceptance=False,unassistedTowerClearAcceptance=False,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 assert not OUT.exists()
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2))
 raise SystemExit(0 if report['passed']else 1)
