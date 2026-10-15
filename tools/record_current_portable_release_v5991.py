"""Additive current portable playtest handoff, keeping the all-aspects goal open."""
import datetime,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5992_current_portable_release_progress'
PARENT=ROOT/'audit_v5983_current_launcher_handoff_progress/progress.json'
PROOF=ROOT/'audit_v5990_current_portable_terminal_checked/report.json'
PACKAGE=ROOT/'release_v5986_current_playtest/package-report.json'

def run():
 need(not OUT.exists(),'Fresh immutable full-objective portable handoff')
 current.expected();parent=json.loads(PARENT.read_text());proof=json.loads(PROOF.read_text());package=json.loads(PACKAGE.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
      all(sha(p)==h for p,h in parent['newInputHashes'].items()),'Actual prior finite evidence and complete original requirement scope remain intact')
 need(proof['passed']and proof['goalStatus']=='active'and not proof['fullPortAcceptance']and
      proof['actualTerminalEvidenceQualifiedWithoutRerun']and proof['standalonePackageCheckerAccepted']and
      proof['actualTemporaryDependencyFaultsRejected']==4 and proof['actualROMAuditPassed']and
      len(proof['actualNativeBoots'])==2 and all(b['actualFiniteExitCode']==0 for b in proof['actualNativeBoots'])and
      proof['physicalVideoAudioBackendInitializationObserved']and not proof['developmentRuntimeToolsOnPATH']and
      proof['preExistingUserSettingsUnchanged']and not proof['interactiveVisualAudibleQualityAccepted']and
      not proof['integratedWholeReleaseRegressionComplete'],'Whole actual portable evidence, not implied interactive/full-port acceptance')
 removal=proof['temporaryExtractionRemoved']
 need(removal['removed']and removal['recoverableFromRetainedZIP']and removal['removedFiles']==70 and
      not Path(removal['removedExactPath']).exists()and len(proof['automaticTimedStopPNGs'])==2,
      'Actual sole extraction and both new PNGs removed, no development/staging recovery copy retained')
 need(package['passed']and package['files']==64 and package['newZIPs']==1 and
      package['all16CompiledVoiceAssetsIncluded']and package['nativeScreenOnlyArtworkIncluded']and
      package['correspondingModifiedMidwaySourceModulesIncluded']and
      package['zip']==proof['zip']and package['zipSHA256']==proof['zipSHA256']==sha(proof['zip'])and
      all(sha(p)==h for p,h in package['sourceHashes'].items()),'One exact requested current-state portable ZIP, all tested dependencies/source modules byte matched')
 pins=dict(proof['inputHashes'])
 for p in(PARENT,PROOF,PACKAGE,Path(__file__).resolve()):pins[str(p)]=sha(p)
 audit=parent['requirementAudit']
 need(len(audit)==7 and audit[-1]['requirement']=='Matching refreshed release ZIP and dependency-aware cleanup of obsolete data',
      'Retain all original explicit requirements; update only delivered package evidence')
 audit[-1]=dict(requirement=audit[-1]['requirement'],
               status='Matching current5219 playtest ZIP and standalone checker/ROM audit/headless plus default D3D/DirectSound startup qualified. Sole temporary extraction removed. Earlier32.49GiB and1.67GiB obsolete cleanup retained. Final integrated whole-port release remains unproven.',
               evidence=[dict(path=str(PACKAGE),sha256=sha(PACKAGE)),dict(path=str(PROOF),sha256=sha(PROOF))],
               refreshedCurrentZIP=True,standaloneCurrentPlaytestAccepted=True,finishedRelease=False)
 sealed=[ROOT/'tools/package_current_playtest_v5985.py',ROOT/'tools/verify_portable_current_playtest_v5987.py',
         ROOT/'tools/qualify_portable_terminal_evidence_v5989.py',Path(__file__).resolve(),PACKAGE]
 for folder in(ROOT/'tools/playtest_release_v5984',ROOT/'audit_v5988_current_portable_playtest_checked',ROOT/'audit_v5990_current_portable_terminal_checked'):
  sealed.extend(p for p in folder.rglob('*')if p.is_file()and p.suffix.lower()in('.json','.ps1','.cmd','.txt','.py'))
 sealed=list(dict.fromkeys(p.resolve()for p in sealed))
 for p in sealed:pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All package/current/source/failed evidence/user settings preserved')
 before=sum(allocated(p)for p in sealed)
 for p in sealed:
  done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(done.returncode==0 and sha(p)==pins[str(p)],'Exact finished text losslessly compressed with no recovery copies')
 after=sum(allocated(p)for p in sealed)
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
             parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],requirementAudit=audit,newInputHashes=pins,
             previousGoalTurnClassification='progress: requested current-state ZIP was streamed from existing tested inputs and every archive byte checked; portable runtime proof was still pending.',
             thisGoalTurnClassification='progress: sole external temporary extraction verified with Windows-only PATH; actual dependency byte faults denied/restored; native ROM audit and headless/default-windowed CMD boots exited0. Actual Direct3D/HLSL and48k DirectSound initialization observed. Original optional-device false-positive and Python-string cleanup-guard failure retained, terminal evidence independently qualified without rerun. Removed the exact terminal extraction and two auto-stop PNGs; sources/settings/old launchers/old ZIP unchanged. Full native-roster scope remains active.',
             refreshedCurrentPlaytestZIP=proof['zip'],zipSHA256=proof['zipSHA256'],zipBytes=proof['zipBytes'],
             portableCurrentPlaytestVerified=True,physicalVideoAudioBackendInitializationObserved=True,
             interactiveVisualAudibleQualityAccepted=False,finalIntegratedReleaseAcceptance=False,fullPortAcceptance=False,
             temporaryFilesRemoved=removal['removedFiles'],temporaryLogicalBytesRemoved=removal['logicalBytesRemoved'],
             temporaryFilesRecoverableFromRetainedZIP=True,automaticTimedStopPNGsCountedAndRemoved=2,
             priorNoRawRecordingWordingCorrection=proof['priorNoRawRecordingWordingCorrection'],
             preExistingUserSettingsAndSourceBytesUnchanged=True,newBuilds=0,newZIPsThisVerificationTurn=0,
             consumedPortableTestSession=59301,actualNativeFiniteBoots=proof['actualNativeBoots'],
             sealedTextFiles=len(sealed),sealedAllocatedBytesBefore=before,sealedAllocatedBytesAfter=after,sealedAllocatedBytesReclaimed=before-after,
             next='Continue the remaining broad gameplay/visual integration from actual current sources: complete move phases and ordinary attacks/ground/shadow/cleanup in wider arena/CPU/KO/overlap contexts; close remaining victim/finisher/morph/secret/cinematic gaps; finish the combined native UI/ladder/names/gameplay/audio acceptance. Keep completed genuine natural campaigns/own endings intact. The new portable ZIP is current-state playtest, not evidence that these remaining requirements are complete. Never regenerate retired builds/raw captures or retain temporary package copies.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,'Full-objective additive handoff losslessly sealed')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','requirementAudit','remaining')},indent=2),flush=True)

if __name__=='__main__':run()
