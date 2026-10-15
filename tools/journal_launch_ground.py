"""Current native mobility/ground/shadow evidence and unchanged full scope."""
import json, subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_launch_ground_progress_storage'

def main():
 need(not OUT.exists()and not native.census(),'Fresh exact journal; native jobs terminal')
 current.expected();parent_path=ROOT/'audit_launch_candidate_ui_progress_storage/report.json'
 parent=json.loads(parent_path.read_text());need(parent['passed']and len(parent['remaining'])==6,'Entire original integration/release scope retained')
 pins={};migrations=[]
 for p,h in parent['inputHashes'].items():
  path=Path(p).resolve()
  if path.parent==ROOT and path.name in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'):
   old=ROOT/'status_history_launch_ground'/path.name;need(sha(old)==h,'Exact preceding document bytes retained')
   migrations.append(dict(priorLogicalPath=str(path),priorSHA256=h,exactHistoricalBytes=str(old),currentSHA256=sha(path)));path=old
  need(sha(path)==h,'Whole inherited evidence/source pin unchanged: '+str(path));pins[str(path)]=h
 pins[str(parent_path)]=sha(parent_path)
 proof_paths=[ROOT/name/'report.json'for name in('audit_launch_ground_native_names_checked','audit_launch_ground_faults','audit_launch_ground_visual_review')]
 proofs=[json.loads(p.read_text())for p in proof_paths];ground,faults,visual=proofs
 need(all(p['passed']and not p['fullPortAcceptance']for p in proofs)and ground['candidate']==current.NAME and
      ground['currentBothSlotDeadPoolGroundAndShadowAccepted']and len(ground['cases'])==4 and
      not ground['firstCapturedSourceInventoryAccepted'],'Actual current bounded ground gate; first inventory loss not hidden')
 need(faults['actualFaultsRejected']==72 and len(faults['cases'])==4 and
      all(len(c['actualFaultsRejected'])==18 for c in faults['cases']),'Actual row/raster/foot/source fault rejection in all four cases')
 need(len(visual['actualNativeFramesReviewed'])==8 and visual['newRasterFiles']==0 and
      not visual['historicalRuntimeAcceptanceTransferred'],'Eight actual current RAM-native frames reviewed, no old runtime substitute')
 need({c['nativeTerminal']['pid']for c in ground['cases']}=={156896,99320,60748,176020}and
      all(c['nativeTerminal']['nativeExit']==0 for c in ground['cases']),'Exact four actual naturally terminal native jobs')
 need(all(c['wholeGroundAndShadow']['samples']==37 and c['wholeGroundAndShadow']['body_mismatches']==c['wholeGroundAndShadow']['vram_mismatches']==0 and
          c['wholeGroundAndShadow']['idle_sole_rows']=={'1':[228],'2':[228]}and
          c['wholeGroundAndShadow']['idle_native_ground_offsets']=={'1':[-1],'2':[-1]}for c in ground['cases']),
      'Every actual full indexed raster and native stock-matching idle floor contact')
 shadow_copies=sum(c['wholeGroundAndShadow']['native_shadow_copies']for c in ground['cases'])
 need(shadow_copies==120162,'Complete actual native shadow row copies')
 for path,proof in zip(proof_paths,proofs,strict=True):
  pins[str(path)]=sha(path)
  for p,h in proof['inputHashes'].items():need(sha(p)==h,'Actual executed source/candidate/evidence unchanged');pins[p]=h
 original_failure=ROOT/'audit_launch_ground_ram/kano_p1/report.json';failure=json.loads(original_failure.read_text())
 need(not failure['passed']and len(failure['nativeTerminal']['hostDecodeErrors'])==1,'Original first source-inventory rejection preserved')
 pins[str(original_failure)]=sha(original_failure)
 first=ground['cases'][0];need(not first['completeCapturedSourceInventoryAccepted']and first['missingCapturedStreams']==['0F000000_C002_33_10']and
                             first['independentNativeHudPredictionUsedOnlyForRaster'],'First missing name stream is prediction-only, not fabricated actual source evidence')
 need(all(c['passed']and not c['nativeTerminal']['hostDecodeErrors']and c['wholeActualGuestAccepted']for c in ground['cases'][1:]),
      'All three unstarted cases retain whole actual guest/source streams after native HUD oracle repair')
 leaves=[ROOT/'audit_launch_ground_ram',ROOT/'audit_launch_ground_checked',ROOT/'status_history_launch_ground']+[p.parent for p in proof_paths]
 files={p for leaf in leaves for p in leaf.rglob('*')if p.is_file()}
 files.update(ROOT/p for p in('mk2ks_launch_ground_ram.lua','tools/capture_launch_ground_ram.py','tools/launch_ground_model.py',
                             'tools/launch_ground_native_names.py','tools/launch_ground_native_names_v2.py','tools/check_launch_ground_faults.py',
                             'tools/review_launch_ground_ram.py','tools/review_launch_ground_ram_v2.py','tools/journal_launch_ground.py',
                             'CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
 need(all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files)and
      not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),'Exact finite source/gzip/proof compression only, no raw media/build/ROM/ZIP')
 storage=[];seen=set();total=0
 for p in sorted(files):
  h=sha(p);stat=p.stat();before=allocated(p);key=stat.st_dev,stat.st_ino
  need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact-target compression')
  after=allocated(p);unique=key not in seen;seen.add(key)
  if unique:total+=after
  storage.append(dict(path=str(p),sha256=h,logicalBytes=stat.st_size,beforeAllocatedBytes=before,allocatedBytes=after,uniqueSelectedAllocation=unique));pins[str(p)]=h
 builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and not native.census(),'No new build/cache or live native job')
 need(all(sha(p)==h for p,h in pins.items()),'All inherited and actual source/evidence bytes stable, including normal launcher')
 report=dict(passed=True,candidate=current.NAME,goalStatus='active',fullPortAcceptance=False,remaining=parent['remaining'],
             previousGoalTurnClassification=parent['thisGoalTurnClassification'],
             thisGoalTurnClassification='progress: four actual current mobility/ground/raster gates; source-derived HUD-oracle diagnosis without replay;120162 native shadow rows;72 actual row/raster/sole/source faults;8 current native RAM frame visual reviews',
             nextAction='Continue startup KO/selection/reset/morph cleanup and full current audio/render/gameplay integration; keep every broader arena, campaign, finisher, secret and matching release requirement open.',
             finiteProofs=[str(p)for p in proof_paths],actualNativePIDs=[c['nativeTerminal']['pid']for c in ground['cases']],
             actualCurrentGroundFrames=148,actualNativeShadowCopies=shadow_copies,actualFaultsRejected=72,
             firstWholeCapturedSourceInventoryAccepted=False,firstFailedReportPreserved=True,
             sourceOracleDiagnosis='Native Kano HUD mask at0F000000 is generated from actual UI mask and original gold ramp/shadow pen2; compiled ROM lanes alone leave this space empty. Numeric metadata uses the original integer parser.',
             currentIdleSoleRows={'stockKitana':228,'kano':228,'sonya':228},allArenaGroundAcceptance=False,
             mainAgentActuallyInspectedFrames=visual['actualNativeFramesReviewed'],allRAMHostsReleased=True,publicPlayableChanged=False,
             inputHashes=pins,intentionalDocumentationPinMigrations=migrations,exactCompressedTargets=storage,selectedFileCount=len(files),
             uniqueSelectedAllocatedBytes=total,retainedCompiledCandidates=16,compilerCacheAbsent=True,
             newNativeBootsThisGoalTurn=4,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,newRasterFiles=0,deletedOldArtifacts=0)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless finite journal')
 print(json.dumps({k:report[k]for k in('passed','actualCurrentGroundFrames','actualNativeShadowCopies','actualFaultsRejected','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds','publicPlayableChanged')}),flush=True)

if __name__=='__main__':main()
