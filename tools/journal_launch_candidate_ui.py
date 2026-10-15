"""Exact current UI/owner/visual evidence and unchanged entire port scope."""
import json,subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_launch_candidate_ui_progress_storage'

def main():
 need(not OUT.exists()and not native.census(),'Fresh journal; actual native jobs terminal')
 current.expected();parent_path=ROOT/'audit_native_dual_roll_progress_storage/report.json'
 parent=json.loads(parent_path.read_text());need(parent['passed']and len(parent['remaining'])==6,'Complete original integration/release scope carried forward')
 pins={};migrations=[]
 for p,h in parent['inputHashes'].items():
  path=Path(p).resolve()
  if path.parent==ROOT and path.name in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'):
   old=ROOT/'status_history_launch_candidate_ui'/path.name;need(sha(old)==h,'Exact previous document bytes retained')
   migrations.append(dict(priorLogicalPath=str(path),priorSHA256=h,exactHistoricalBytes=str(old),currentSHA256=sha(path)));path=old
  need(sha(path)==h,'Whole previous source/evidence pin unchanged: '+str(path));pins[str(path)]=h
 pins[str(parent_path)]=sha(parent_path)
 proof_paths=[ROOT/name/'report.json'for name in('audit_launch_candidate_ui_checked','audit_launch_candidate_ui_cold_owner_faults','audit_launch_candidate_ui_image_backing')]
 proofs=[json.loads(p.read_text())for p in proof_paths];ui,owner,backing=proofs
 need(all(p['passed']and not p['fullPortAcceptance']for p in proofs)and ui['candidate']==current.NAME and
      ui['currentBothSlotSelectionLadderFirstMatchPixelsAccepted']and ui['wholeActualGuestGFXAccepted']and
      ui['originalStatePixelFaultMethods']==46 and len(ui['cases'])==4,'Complete actual current finite UI gate and all original failure methods')
 need(owner['completeColdBattleOwnerFields']==15952 and len(owner['actualOwnerFaultsRejected'])==24 and
      backing['totalCurrentNativePixels']==1219200 and len(backing['actualCurrentFrames'])==12 and
      not backing['historicalRuntimeAcceptanceTransferred'],'Entire cold owner counterexamples and exact visual backing, no old runtime substitute')
 need(all(c['nativeTerminal']['nativeExit']==0 and not c['nativeTerminal']['hostDecodeErrors']and c['passed']and
          c['actualDisplayedCallbacks']==171 and c['state']['first_match_participant_fields']==362 and
          c['rendered']['native_name_shadow_checks']>=4 for c in ui['cases']),'All four actual natural native terminals and full original presentation scope')
 need({c['nativeTerminal']['pid']for c in ui['cases']}=={169048,159136,49512,38996},'Exact four physical jobs, never replayed after timeout')
 for path,proof in zip(proof_paths,proofs,strict=True):
  pins[str(path)]=sha(path)
  for p,h in proof['inputHashes'].items():need(sha(p)==h,'Actually executed source/candidate/evidence/backing unchanged');pins[p]=h
 inspected=[('kano_p1',986),('sonya_p2',986),('kano_p2',1288),('sonya_p2',1288),('kano_p2',1874),('sonya_p1',1874)]
 reviewed=[r for r in backing['actualCurrentFrames']if(r['case'],r['actualNativeFrame'])in inspected]
 need(len(reviewed)==6,'Six actual current byte-backed native frames inspected by main agent')
 leaves=[ROOT/'audit_launch_candidate_ui_ram',ROOT/'status_history_launch_candidate_ui']+[p.parent for p in proof_paths]
 files={p for leaf in leaves for p in leaf.rglob('*')if p.is_file()}
 files.update(ROOT/p for p in('mk2ks_launch_candidate_ui.lua','tools/capture_launch_candidate_ui.py','tools/check_launch_ui_cold_owner_faults.py',
                             'tools/check_launch_ui_image_backing.py','tools/journal_launch_candidate_ui.py','CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
 need(all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files)and
      not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),'Exact finite new source/evidence compression only, no raw media/build/ROM/ZIP')
 storage=[];seen=set();total=0
 for p in sorted(files):
  h=sha(p);stat=p.stat();before=allocated(p);key=stat.st_dev,stat.st_ino
  need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact-target compression')
  after=allocated(p);unique=key not in seen;seen.add(key)
  if unique:total+=after
  storage.append(dict(path=str(p),sha256=h,logicalBytes=stat.st_size,beforeAllocatedBytes=before,allocatedBytes=after,uniqueSelectedAllocation=unique));pins[str(p)]=h
 builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and not native.census(),'No new build/cache or live native job')
 need(all(sha(p)==h for p,h in pins.items()),'All inherited and actual source/evidence bytes unchanged, including normal launcher')
 report=dict(passed=True,candidate=current.NAME,goalStatus='active',fullPortAcceptance=False,remaining=parent['remaining'],
             previousGoalTurnClassification=parent['thisGoalTurnClassification'],
             thisGoalTurnClassification='progress: four real current campaign-slot selection/ladder/first-match state/pixel gates, all46 original reported-failure methods,15952 cold-owner fields/24 actual faults,12 full byte-backed frames/six visual reviews',
             nextAction='Continue launch KO/selection/reset/morph/overlap cleanup and current complete ground/render/audio verification, including source-bound sole placement; retain every other integration/release group.',
             finiteProofs=[str(p)for p in proof_paths],actualNativePIDs=[c['nativeTerminal']['pid']for c in ui['cases']],
             currentDisplayedCallbacks=684,originalStatePixelFaultMethods=46,completeColdOwnerFields=15952,actualOwnerFaultsRejected=24,
             mainAgentActuallyInspectedFrames=reviewed,finiteVisualReview='Native numbered blinking CSS borders/poses; native small ladder icons with no full CSS portrait/pose; true fight bodies and stock name shadows. Universal sole/shadow/raster coverage remains open.',
             allRAMHostsReleased=True,publicPlayableChanged=False,inputHashes=pins,intentionalDocumentationPinMigrations=migrations,
             exactCompressedTargets=storage,selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,retainedCompiledCandidates=16,
             compilerCacheAbsent=True,newNativeBootsThisGoalTurn=4,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,newRasterFiles=0,deletedOldArtifacts=0)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless finite journal')
 print(json.dumps({k:report[k]for k in('passed','currentDisplayedCallbacks','originalStatePixelFaultMethods','actualOwnerFaultsRejected','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds','publicPlayableChanged')}),flush=True)

if __name__=='__main__':main()
