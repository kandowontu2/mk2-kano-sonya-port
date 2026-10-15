"""Bounded, lossless startup-work compression with hardlink-aware accounting.

Only named version6622..6660 startup leaves and their sources are selected.
Old artifacts remain intact. The existing shared payload is accounted as an
existing allocation, never charged as a new copy. Any PNG/WAV is disclosed.
"""
import json,re,subprocess
from pathlib import Path
import native_process_census_v6647 as process
import kano_ball_launch_context_v6642 as candidate
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
OUT=ROOT/'audit_v6662_kano_launch_storage_checked'

def version(path):
 m=re.search(r'_v(\d+)',path.name);return int(m[1])if m else None

def main():
 need(not OUT.exists()and not process.census(),'Fresh exact-target storage receipt, actual native jobs terminal')
 parent=ROOT/'audit_v6660_kano_launch_progress_checked/report.json';proof=json.loads(parent.read_text())
 need(proof['passed']and proof['actualSpecialCases']==16 and proof['actualNativeAudioContexts']==4 and
      proof['sourceExactHumanLaunchBothSlotsAccepted']and not proof['fullPortAcceptance'],'Full finite same-run move and source-audio proofs')
 pins=dict(proof['inputHashes']);pins[str(parent.resolve())]=sha(parent)
 need(all(sha(p)==h for p,h in pins.items()),'All bound input/evidence hashes intact before compression')
 dirs=[p for p in ROOT.iterdir()if p.is_dir()and version(p)is not None and 6622<=version(p)<=6660 and
       p.name.startswith(('audit_','source_','diagnostic_'))]
 dirs.append(ROOT/'status_history_v6659')
 files=[p for folder in dirs for p in folder.rglob('*')if p.is_file()]
 files.extend(p for p in(ROOT/'tools').iterdir()if p.is_file()and version(p)is not None and 6622<=version(p)<=6661)
 files.extend(p for p in ROOT.iterdir()if p.is_file()and version(p)is not None and 6622<=version(p)<=6661)
 files.extend(ROOT/n for n in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
 need(len(files)==len(set(files))and all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files),
      'Unique exact resolved startup targets, no broad workspace cleanup')
 payload=ROOT/candidate.NAME/'roms/mk2ks/mk2ks.mdata';prior_payload=ROOT/'diagnostic_v6508_native_projectile_identifiers/roms/mk2ks/mk2ks.mdata'
 need(payload.samefile(prior_payload)and sha(payload)==candidate.PAYLOAD_SHA,'Payload is the exact existing allocation, not a data copy')
 source_asset=ROOT/'audit_v6635_kano_launch_native48k/kano_ball_launch.wav'
 need((ROOT/candidate.NAME/'samples/mk2ks/kano_ball_launch.wav').samefile(source_asset),'Registered asset shares exact authored source allocation')
 rows=[];seen=set();logical=physical=0;media=[]
 for p in sorted(files):
  h=sha(p);stat=p.stat();key=stat.st_dev,stat.st_ino
  before=allocated(p)
  shared_payload=p==payload
  if not shared_payload and p.suffix.lower()!='.exe':
   result=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
   need(result.returncode==0 and sha(p)==h,'Exact file bytes unchanged by lossless compression')
  after=allocated(p);unique=key not in seen;seen.add(key);logical+=stat.st_size
  if unique and not shared_payload:physical+=after
  row=dict(path=str(p.resolve()),sha256=h,logicalBytes=stat.st_size,beforeAllocatedBytes=before,
           allocatedBytes=after,hardlinks=stat.st_nlink,uniqueSelectedFileAllocation=unique,existingSharedPayloadExcluded=shared_payload)
  rows.append(row)
  if p.suffix.lower()in('.png','.wav'):media.append(row)
 need(all(sha(p)==h for p,h in pins.items()),'Every protected source/compiled/public/evidence byte unchanged after compression')
 need(not process.census()and not(ROOT/'mame-mkp/build/mingw-gcc').exists(),'Actual native jobs terminal and generated compiler cache still absent')
 builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16,'Authoritative count of real retained compiled candidates')
 release=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(release)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C','Historical portable ZIP unchanged')
 result=dict(passed=True,files=len(rows),logicalSelectedBytes=logical,uniqueSelectedAllocatedBytesExcludingExistingPayload=physical,
             exactTargets=rows,authoredAssetsAndNativeImagesDisclosed=media,existingPayloadAllocatedBytes=allocated(payload),
             newExecutableAllocatedBytes=allocated(ROOT/candidate.NAME/'mkport_candidate.exe'),retainedCompiledCandidates=16,
             priorGameplayAcceptance=str(parent),priorGameplayAcceptanceSHA256=sha(parent),unchangedProtectedPins=len(pins),
             compilerCacheAbsent=True,compilerCacheReclaimedBytesNotMeasured=True,newBuilds=1,newPayloadAllocations=0,newZIPs=0,
             deletedOldArtifacts=0,rawGameplayPCMGuestDACOrRGBFilesCreated=0,publicPlayableChanged=False,fullPortAcceptance=False,goalStatus='active')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(result,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Storage receipt compressed losslessly')
 print(json.dumps({k:result[k]for k in('passed','files','uniqueSelectedAllocatedBytesExcludingExistingPayload','newExecutableAllocatedBytes','retainedCompiledCandidates','compilerCacheAbsent','newPayloadAllocations','fullPortAcceptance')}),flush=True)

if __name__=='__main__':main()
