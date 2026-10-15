"""Seal repaired native projectile rendering/audio evidence before routing changes.

The full integration objective remains active; finite native cases are not a
finished-release claim. Failed captures and source-only/preflight mistakes
remain preserved. No raw media, new build, ROM copy or workspace deletion.
"""
import ctypes,datetime,json,re,subprocess
from pathlib import Path
import native_projectile_identifiers_context_v6509 as candidate
import capture_current_cmd_specials_v6261 as host
import save_repaired_candidate_progress_v6534 as prior
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
OUT=ROOT/'audit_v6551_repaired_projectile_progress'

def main():
 need(not OUT.exists()and not host.census(),'Fresh checkpoint; actual native games terminal')
 candidate.expected();pins={};children={}
 paths={'previous':ROOT/'audit_v6535_repaired_candidate_progress/report.json',
        'ringHit':ROOT/'audit_v6539_repaired_ring_hit_checked/report.json',
        'ringBlock':ROOT/'audit_v6539_repaired_ring_block_checked/report.json',
        'ringMiss':ROOT/'audit_v6539_repaired_ring_miss_checked/report.json',
        'kanoEffects':ROOT/'audit_v6543_repaired_kano_effects_checked/report.json',
        'ringAudio':ROOT/'audit_v6547_repaired_ring_audio_checked/report.json',
        'kanoTaskID':ROOT/'audit_v6549_repaired_kano_chronology_checked/report.json'}
 for key,p in paths.items():
  r=json.loads(p.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual scoped child passes, not whole port')
  for k,h in r['inputHashes'].items():need(sha(k)==h,'Actual executed/qualified child pin intact '+k);pins[str(Path(k).resolve())]=h
  pins[str(p.resolve())]=sha(p);children[key]=r
 failure=ROOT/'audit_v6541_repaired_kano_effects_ram/result.json'
 rejected=json.loads(failure.read_text())
 need(rejected['passed']is False and children['kanoTaskID']['originalCaptureRejectionPreserved'],'Actual strict historical-ID rejection remains false')
 files=set()
 for p in ROOT.iterdir():
  m=re.match(r'^audit_v(\d+)_',p.name)
  if p.is_dir()and m and 6536<=int(m[1])<=6549:files.update(q.resolve()for q in p.rglob('*')if q.is_file())
 for p in (ROOT/'tools').iterdir():
  m=re.search(r'_v(\d+)\.py$',p.name)
  if m and 6536<=int(m[1])<=6550:files.add(p.resolve())
 sizes=[];allocated=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 allocated.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];allocated.restype=ctypes.c_uint32
 for p in sorted(files):
  need(p.suffix.lower()not in('.bin','.png','.wav','.rgb','.pcm','.vram'),'No persisted new raw media')
  h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Hash-preserving exact-file compression')
  hi=ctypes.c_uint32();ctypes.set_last_error(0);lo=allocated(str(p),ctypes.byref(hi))
  need(lo!=0xffffffff or ctypes.get_last_error()==0,'Actual selected file allocation')
  sizes.append(dict(path=str(p),logicalBytes=p.stat().st_size,allocatedBytes=(hi.value<<32)|lo));pins[str(p)]=h
 need(all(sha(p)==h for p,h in pins.items())and not host.census(),'All current pins intact; no pending native job')
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  candidate=candidate.NAME,executableSHA256=candidate.EXE_SHA,guestSHA256=candidate.GUEST_SHA,actualGuestByteDelta=158,
  actualPassingChildReports={k:str(p)for k,p in paths.items()},
  repairedRingFullRenderBranches=['hit','block','miss'],ringContinuousFields=247,ringExactRGBPixels=25095200,
  kanoContinuousFields=641,kanoExactRGBPixels=65125600,kanoNativeArtFaultsRejected=8,kanoRetirementFaultsRejected=1,
  exactTaskIDChronologyRows=14238,taskIDFaultsRejected=6,ringCompleteStereoFrames=561600,
  ringNativePackets=20,ringAudioFaultsRejected=10,
  immutableFailuresPreserved=True,kanoRejectedCaptureReason='Historical comparison expected old instruction-overread task ID CB0C; actual source-derived repaired P2 ID0800 is the only differing field. Additive qualifier retains the original false report.',
  missPreflightMistake='6536 preflight selected5324 physical reference lacking full CODE windows. Actual new miss capture with unchanged6410 observer passed the complete6411 branch and6538 lifecycle/raster fault gates. No failing native miss run was replaced.',
  publicPlayableUnchanged=True,publicCandidate=candidate.old.NAME,remaining=prior.REMAINING,
  newBuilds=0,newROMPayloadCopies=0,newRawMedia=0,newZIPs=0,cleanupReclaimedBytesUnknown=True,
  newlyRetainedSelectedAllocatedBytes=sum(r['allocatedBytes']for r in sizes),retainedNewFileRows=sizes,
  allocationScope='Exact6536..6549 native evidence and6536..6550 source files, excluding this checkpoint output and pre-existing shared candidate/payload.',
  previousGoalTurnClassification='progress: repaired challenger/special/UI qualification and compiler-cache recovery receipt.',
  thisGoalTurnClassification='progress: new native Ring hit/block/miss full raster/shadow/lifecycle gates, full Kano blade/knife641-scene art/retirement proof and full repaired Ring source audio.',
  nextAction='Promote checked repaired work-in-progress launcher, then broader native routes/finishers/audio/secret/morph/cinematic and final combined release qualification.',
  inputHashes=pins,fullPortAcceptance=False,scope=__doc__)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact checkpoint compressed')
 print(json.dumps(dict(passed=True,fields=888,completeStereoFrames=561600,allocatedBytes=report['newlyRetainedSelectedAllocatedBytes'],checkpointSHA256=h)),flush=True)

if __name__=='__main__':main()
