"""Seal actual checked-WIP promotion, route migration and retained allocation.

The full integration scope remains active. Historical compiled/capture reports
are not rewritten; deliberate mutable alias changes are mapped to exact old
byte copies. No further deletion, new build, ROM payload copy or release ZIP.
"""
import ctypes,datetime,json,re,subprocess
from pathlib import Path
import native_projectile_identifiers_context_v6509 as candidate
import capture_current_cmd_specials_v6261 as host
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
TASK=Path(r'C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port')
OUT=ROOT/'audit_v6564_repaired_public_handoff'
PREVIOUS=ROOT/'audit_v6558_repaired_projectile_storage/report.json'

def main():
 need(not OUT.exists()and not host.census(),'Fresh final handoff; actual native jobs terminal')
 candidate.expected();pins={};children={}
 paths={'ordinaryLauncher':ROOT/'audit_v6554_repaired_default_launcher_checked/report.json',
        'bothSlotProjectileCombat':ROOT/'audit_v6562_repaired_public_contract_checked/report.json'}
 for key,p in paths.items():
  r=json.loads(p.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual current scoped promotion proof')
  for k,h in r['inputHashes'].items():need(sha(k)==h,'Every current actually executed child input intact '+k);pins[str(Path(k).resolve())]=h
  pins[str(p.resolve())]=sha(p);children[key]=r
 old=json.loads(PREVIOUS.read_text());need(old['passed']and old['goalStatus']=='active','Entire pre-promotion goal scope remains active')
 migrations={
  (ROOT/'PLAY_MK2_KANO_SONYA.cmd').resolve():ROOT/'launcher_history_v6552/PLAY_MK2_KANO_SONYA.cmd',
  (TASK/'PLAY_LATEST_MK2_KANO_SONYA.cmd').resolve():ROOT/'launcher_history_v6552/TASK_PLAY_LATEST_MK2_KANO_SONYA.cmd'}
 changes=[]
 for k,h in old['inputHashes'].items():
  p=Path(k).resolve();actual=sha(p)
  if actual!=h:
   need(p in migrations and sha(migrations[p])==h,'Only declared mutable launcher routing migration; exact historical bytes preserved')
   changes.append(dict(path=str(p),oldSHA256=h,currentSHA256=actual,oldBytesAt=str(migrations[p])))
   pins[str(migrations[p].resolve())]=h
  else:pins[str(p)]=h
 need(any(Path(r['path'])==(ROOT/'PLAY_MK2_KANO_SONYA.cmd').resolve()for r in changes),'Historical route change explicitly audited, not claimed intact')
 combat=children['bothSlotProjectileCombat'];need(combat['actualCases']==4 and combat['actualVerifiedSpecialCycles']==8 and
  combat['actualContiguousPostFields']==3210 and len(combat['actualSemanticFaultsRejected'])==50,'Full current-CMD physical and corresponding original fault matrix')
 need(children['ordinaryLauncher']['preExistingUserSettingsUnchanged']and
  len(children['ordinaryLauncher']['actualSourceCheckerDenialSimulations'])==5,'Actual ordinary boot and five rejection controls')
 files={PREVIOUS.resolve(),Path(__file__).resolve(),(ROOT/'PLAY_CURRENT_V6508_CHECKED.cmd').resolve(),
        (ROOT/'PLAY_MK2_KANO_SONYA.cmd').resolve(),(TASK/'PLAY_LATEST_MK2_KANO_SONYA.cmd').resolve()}
 for p in ROOT.iterdir():
  m=re.match(r'^audit_v(\d+)_',p.name)
  if p.is_dir()and m and 6554<=int(m[1])<=6562:files.update(q.resolve()for q in p.rglob('*')if q.is_file())
 files.update(p.resolve()for p in(ROOT/'launcher_history_v6552').rglob('*')if p.is_file())
 for p in(ROOT/'tools').iterdir():
  m=re.search(r'_v(\d+)\.(?:py|ps1)$',p.name)
  if m and 6552<=int(m[1])<=6563:files.add(p.resolve())
 sizes=[];allocation=ctypes.WinDLL('kernel32',use_last_error=True).GetCompressedFileSizeW
 allocation.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];allocation.restype=ctypes.c_uint32
 for p in sorted(files):
  need(p.suffix.lower()not in('.bin','.png','.wav','.rgb','.pcm','.vram'),'No new promotion raw-media output')
  h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Hash-preserving exact promotion-file compression')
  hi=ctypes.c_uint32();ctypes.set_last_error(0);lo=allocation(str(p),ctypes.byref(hi));need(lo!=0xffffffff or ctypes.get_last_error()==0,'Actual allocated selected-file bytes')
  sizes.append(dict(path=str(p),logicalBytes=p.stat().st_size,allocatedBytes=(hi.value<<32)|lo));pins[str(p)]=h
 for p in (ROOT/'CURRENT_PLAYTEST_STATUS.md',ROOT/'WORKSPACE_CLEANUP_CURRENT.md'):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items())and not host.census()and not(ROOT/'mame-mkp/build/mingw-gcc').exists(),
      'Current pins intact, native jobs terminal and compiler cache still absent')
 remaining=list(old['remaining']);remaining[0]='Remaining repaired projectile/CPU/arena/shadow/audio contexts; finite Ring hit/block/miss, Kano blade/knife and Ring audio gates passed; repaired checked-WIP launcher promoted.'
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  candidate=candidate.NAME,executableSHA256=candidate.EXE_SHA,guestSHA256=candidate.GUEST_SHA,
  actualPassingChildReports={k:str(p)for k,p in paths.items()},prePromotionRuntimeQualification=str(PREVIOUS),
  actualCheckedWIPLauncherPromoted=True,normalCMDBothCharacterBothSlotProjectileCombatAccepted=True,
  exactHistoricalRoutingMigrations=changes,historicalReportsAndCompileTimeManifestUnchanged=True,
  fallbackVersionedBuildLauncherZIPAndSavedSettingsUnchanged=True,currentSettingsDirectory='play_v5219_checked',
  actualPhysicalCycles=8,actualActorFields=3210,actualFullRGBDigests=71,actualSemanticFaultsRejected=50,
  previousGoalTurnClassification='progress: repaired projectile renderer/audio qualifications completed.',
  thisGoalTurnClassification='progress: repaired build promoted through ordinary CMD, full denial/ROM/unscripted coldboot and four both-slot physical combat/fault checks; storage compressed and full remaining scope retained.',
  immutableUnstartedHostBindingFailurePreserved=str(ROOT/'audit_v6556_repaired_public_special_host_failure/failure.json'),
  remaining=remaining,nextAction='Current single-player paid continue/post-ending joins and remaining native arena/audio/secret/morph/cinematic integration, then final combined regression and matching release.',
  newBuilds=0,newROMPayloadCopies=0,newRawMedia=0,newZIPs=0,regeneratedCompilerCacheAbsent=True,
  cleanupReclaimedBytesUnknown=True,selectedPromotionFileRows=sizes,
  selectedPromotionAllocatedBytes=sum(r['allocatedBytes']for r in sizes),
  allocationScope='Exact6554..6562 reports/captures,6552..6563 sources, runtime checkpoint, new/default aliases and exact old alias copies; excludes this output and pre-existing candidate/payload.',
  inputHashes=pins,finishedReleasePromoted=False,fullPortAcceptance=False,scope=__doc__)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact final handoff receipt compressed')
 print(json.dumps(dict(passed=True,candidate=candidate.NAME,actualCycles=8,actorFields=3210,promotionAllocatedBytes=report['selectedPromotionAllocatedBytes'],goalStatus='active')),flush=True)

if __name__=='__main__':main()
