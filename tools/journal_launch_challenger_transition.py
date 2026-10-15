"""Journal bounded completed P1 selection-transition evidence, no builds."""
import json,subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha

def main():
 out=ROOT/'audit_launch_challenger_transition_progress_storage'
 need(not out.exists()and not native.census(),'Fresh journal after authoritative native terminals')
 parentpath=ROOT/'audit_bicycle_launch_ko_round_progress_storage/report.json';parent=json.loads(parentpath.read_text())
 need(parent['passed'],'Previous accepted checkpoint retained');pins=dict(parent['inputHashes']);pins[str(parentpath)]=sha(parentpath)
 proofs=[];fields=frames=channels=faults=0
 for move,pid in(('ball',157700),('square',125680)):
  path=ROOT/f'audit_launch_challenger_transition_checked_{move}_p1/report.json';p=json.loads(path.read_text());proofs.append(path)
  need(p['passed']and p['nativeTerminal']['pid']==pid and p['nativeTerminal']['nativeExit']==0 and not p['fullPortAcceptance'],'Exact same-terminal finite P1 proof')
  need(p['completeSourceWaveform']['differentChannelSamples']==0 and p['completeNativeDCSDelivery']['selectionWrites']==2 and p['completeNativeDCSDelivery']['ownedStartupWrites']==1 and p['wholeOriginalJoinedGameplay']['ordinaryTailFieldsPerSlot']==600,'Whole source and rebuilt match contract')
  fields+=p['completePhysicalAndHealthInventory']['continuousPhysicalFields'];frames+=p['completeSourceWaveform']['comparedStereoFrames'];channels+=p['completeIndependentOwnership']['completeBattleChannelFields']
  path=ROOT/f'audit_launch_challenger_transition_faults_{move}_p1/report.json';f=json.loads(path.read_text());proofs.append(path)
  need(f['passed']and len(f['actualFaultsRejected'])==16,'Same capture semantic faults');faults+=16
 for name in('audit_launch_challenger_transition_packet_inventory_rejection_ball_p1','audit_launch_challenger_transition_packet_inventory_rejection_square_p1','audit_launch_challenger_transition_vacuous_fault_rejection_square_p1'):
  path=ROOT/name/'failure.json';need(not json.loads(path.read_text())['passed'],'Executed original checker rejection retained');proofs.append(path)
 failed=ROOT/'audit_launch_challenger_transition_ball_p1_delay1/report.json';f=json.loads(failed.read_text());proofs.append(failed)
 need(not f['passed']and f['nativeTerminal']['pid']==112576 and f['nativeTerminal']['nativeExit']==3,'Original pre-game observer delimiter failure retained')
 view=ROOT/'audit_launch_challenger_transition_visual_square_p1/report.json';v=json.loads(view.read_text());proofs.append(view)
 need(v['passed']and len(v['viewedFrameHeaders'])==3 and not v['fullRasterAcceptance'],'Finite actual viewed native frames, no full pixel acceptance')
 for path in proofs:
  p=json.loads(path.read_text());pins[str(path)]=sha(path)
  for source,h in p.get('inputHashes',{}).items():need(sha(source)==h,'All original executed source pins stable');pins[source]=h
 need(fields==7246 and channels==14492 and frames==3177600 and faults==32,'Exact completed P1 scope')
 leaves=[p.parent for p in proofs]+[ROOT/'audit_launch_challenger_transition_v2_ball_p1_delay1',ROOT/'audit_launch_challenger_transition_rgb_square_p1_delay1']
 files={p for leaf in leaves for p in leaf.rglob('*')if p.is_file()}
 files.update(ROOT/name for name in('mk2ks_launch_challenger_transition.lua','mk2ks_launch_challenger_transition_v2.lua','tools/capture_launch_challenger_transition.py','tools/capture_launch_challenger_transition_v2.py','tools/capture_launch_challenger_transition_rgb.py','tools/qualify_launch_challenger_transition.py','tools/qualify_launch_challenger_transition_v2.py','tools/check_launch_challenger_transition_faults.py','tools/check_launch_challenger_transition_faults_v2.py','tools/review_launch_challenger_ram_frames.py','tools/journal_launch_challenger_transition.py'))
 need(all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files)and not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),'Bounded sources and compressed receipts, no raw media')
 storage=[];total=0;seen=set()
 for p in sorted(files):
  h=sha(p);stat=p.stat();key=stat.st_dev,stat.st_ino;before=allocated(p)
  need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact compression')
  after=allocated(p)
  if key not in seen:total+=after;seen.add(key)
  pins[str(p)]=h;storage.append(dict(path=str(p),sha256=h,beforeAllocatedBytes=before,allocatedBytes=after))
 current.expected();builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and not native.census()and all(sha(p)==h for p,h in pins.items()),'Original sources/public launcher unchanged, no compiler cache or new builds')
 report=dict(passed=True,candidate=current.NAME,goalStatus='active',fullPortAcceptance=False,parentJournal=str(parentpath),remaining=parent['remaining'],completedScope='P1 Kano ball and Sonya Square live startup to real challenger selection and true-ID joined match with ordinary controls',nextAction='Complete unstarted P2 transition cases and concrete morph ownership gaps, then combined integration and matching release. Do not replay completed P1 contexts merely to relabel them.',actualNativePIDs=[112576,157700,125680],continuousPhysicalFields=fields,completeBattleChannelFields=channels,comparedStereoFrames=frames,differentChannelSamples=0,semanticFaultsRejected=faults,actualViewedNativeFrames=3,fullRasterAcceptance=False,allSelectionMorphCoverageAccepted=False,allRAMHostsReleased=True,rootStatusDocumentsUnchanged=True,publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,retainedCompiledCandidates=16,selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,inputHashes=pins,exactCompressedTargets=storage)
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(report,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Lossless final journal')
 print(json.dumps({k:report[k]for k in('passed','continuousPhysicalFields','comparedStereoFrames','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds')}),flush=True)

if __name__=='__main__':main()
