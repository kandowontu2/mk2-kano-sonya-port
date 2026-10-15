"""Full-scope CPU startup progress journal and exact-target storage receipt.

Migrate current-document pins explicitly to their exact historical bytes.
Never alter prior source, failure, capture, proof, launcher or release bytes.
Lossless compression only; no deletion, new build, guest payload or media.
"""
import json,re,subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as process
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6676_kano_cpu_launch_progress_storage_checked'


def main():
 need(not OUT.exists()and not process.census(),'Fresh finite journal; actual native jobs terminal')
 current.expected()
 paths=[ROOT/'audit_v6660_kano_launch_progress_checked/report.json',
        ROOT/'audit_v6666_kano_cpu_launch_motion_checked/report.json',
        ROOT/'audit_v6671_kano_cpu_launch_audio_checked/report.json']
 parent,motion,audio=(json.loads(p.read_text())for p in paths)
 need(parent['passed']and parent['actualMoveCycles']==32 and parent['sourceExactHumanLaunchBothSlotsAccepted'],
      'Previous full both-slot special/human audio progress retained')
 need(motion['passed']and audio['passed']and motion['nativeTerminal']==audio['nativeTerminal']and
      audio['nativeTerminal']['nativeExit']==0 and not audio['nativeTerminal']['hostDecodeErrors']and
      len(motion['proof']['allActualRollPhases'])==2 and len(motion['proof']['declaredCompletedPairs'])==2 and
      len(motion['proof']['actualNativeMotionFaultsRejected'])==47 and
      audio['completeStereoFrames']==1580160 and audio['wholeNativePCM']['differentChannelSamples']==0 and
      audio['allPrecisePhysicalSourceStates']['preciseSourceChannelStates']==23044 and
      audio['nativeDelivery']==dict(packets=74,portWrites=148,nativeDSPReads=148,trueWinnerMarkers=1,ownedStartupMarkers=2,unaccountedPortWrites=0)and
      len(audio['actualAudioRecordFaultsRejected'])==14 and len(audio['allNativeRGBCallbackDigests'])==98,
      'Entire same current CPU match and all actual startup/winner/DAC output proven, no old trajectory substitution')
 need(parent['remaining']==motion['remaining']==audio['remaining']and len(parent['remaining'])==6 and
      not any(p['fullPortAcceptance']for p in(parent,motion,audio)),'Full original objective and all remaining scope groups remain active')
 archive=ROOT/'status_history_v6674'
 prior_documents={'CURRENT_PLAYTEST_STATUS.md':'E427EB2FAB28E9EC1BE403A0B532C1AD306AF61D581EFFE9E1B369BBB8DC2073',
                  'WORKSPACE_CLEANUP_CURRENT.md':'A730C577CB194073F7C87B11E2ED7EB43BAFDBF8FAAB002BA04CC177F32D0479'}
 need(all(sha(archive/name)==digest and sha(ROOT/name)!=digest for name,digest in prior_documents.items()),
      'Exact old current documents preserved before intentional new progress text')
 pins={};migrations=[]
 for proof_path,proof in zip(paths,(parent,motion,audio),strict=True):
  for raw,h in proof['inputHashes'].items():
   p=Path(raw).resolve()
   if p.parent==ROOT and p.name in prior_documents and h==prior_documents[p.name]:
    migrated=archive/p.name
    need(sha(migrated)==h,'Every historical documentation pin resolves to exact archived bytes')
    migrations.append(dict(proof=str(proof_path),priorLogicalPath=str(p),priorSHA256=h,
                           exactHistoricalBytes=str(migrated),currentUpdatedSHA256=sha(p)))
    p=migrated
   need(sha(p)==h,'Actual bound source/evidence bytes intact: '+str(p))
   key=str(p);need(key not in pins or pins[key]==h,'No contradictory inherited proof pins');pins[key]=h
  pins[str(proof_path)]=sha(proof_path)
 docs={name:(ROOT/name).read_text()for name in prior_documents}
 need(all(t in docs['CURRENT_PLAYTEST_STATUS.md']for t in('audit_v6666_kano_cpu_launch_motion_checked/report.json',
      'audit_v6671_kano_cpu_launch_audio_checked/report.json','1,580,160','23,044','ordinary CMD remains on v6508'))and
      'No additional build'not in docs['WORKSPACE_CLEANUP_CURRENT.md'],
      'Current status reflects finite qualified CPU result and unchanged ordinary build')
 def version(path):
  m=re.search(r'_v(\d+)',path.name);return int(m[1])if m else None
 folders=[p for p in ROOT.iterdir()if p.is_dir()and version(p)is not None and 6663<=version(p)<=6674 and
          p.name.startswith(('audit_','status_history_'))]
 files=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
 files.extend(p for p in(ROOT/'tools').iterdir()if p.is_file()and version(p)is not None and 6663<=version(p)<=6675)
 files.extend(ROOT/name for name in prior_documents)
 need(len(files)==len(set(files))and all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files),
      'Only unique exact resolved finite current proof/source/document targets')
 need(not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),
      'No new build/payload/media/release assets in current qualification leaves')
 storage=[];seen=set();total=0
 for p in sorted(files):
  h=sha(p);stat=p.stat();key=stat.st_dev,stat.st_ino;before=allocated(p)
  need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,
       'Lossless exact-target compression preserves every logical byte')
  after=allocated(p);unique=key not in seen;seen.add(key)
  if unique:total+=after
  storage.append(dict(path=str(p.resolve()),sha256=h,logicalBytes=stat.st_size,beforeAllocatedBytes=before,
                      allocatedBytes=after,uniqueSelectedAllocation=unique,hardlinks=stat.st_nlink))
  pins[str(p.resolve())]=h
 need(all(sha(p)==h for p,h in pins.items()),'All protected compiled/source/capture/proof bytes unchanged after compression')
 builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
 need(len(builds)==16 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and not process.census(),
      'Authoritative16 retained compiled folders, no native job and no generated compiler cache')
 result=dict(passed=True,candidate=current.NAME,goalStatus='active',fullPortAcceptance=False,
             priorFullScopeJournal=str(paths[0]),sameNativeMotionProof=str(paths[1]),sameNativeCPUAudioProof=str(paths[2]),
             sourceExactHumanLaunchBothSlotsAccepted=True,sourceExactCPUStartupAudioAccepted=True,
             qualifiedCurrentCPURolls=2,qualifiedDeclaredCompletedChokes=2,wholeNativeHealthStateFields=3602,
             genuineHumanKOFrame=2613,genuineRoundResetFrame=2801,exactCurrentCPUStereoFrames=1580160,
             fullInterruptionCoverageAccepted=False,sourceRasterAcceptance=False,remaining=parent['remaining'],
             intentionalDocumentationPinMigrations=migrations,inputHashes=pins,
             exactCompressedTargets=storage,uniqueSelectedAllocatedBytes=total,selectedFileCount=len(files),
             retainedCompiledCandidates=len(builds),compilerCacheAbsent=True,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,
             deletedOldArtifacts=0,publicPlayableChanged=False,
             previousGoalTurnClassification='no progress: acknowledgement only; actual retained host handle and authoritative native terminal revalidated',
             thisGoalTurnClassification='progress: all actual CPU roll/pair motion, full native state/HP/choice and complete source startup/winner audio qualified from same terminal RAM carrier')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(result,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact bounded journal compressed')
 print(json.dumps({k:result[k]for k in('passed','exactCurrentCPUStereoFrames','selectedFileCount','uniqueSelectedAllocatedBytes',
                                     'retainedCompiledCandidates','compilerCacheAbsent','newBuilds','fullPortAcceptance')}),flush=True)


if __name__=='__main__':main()
