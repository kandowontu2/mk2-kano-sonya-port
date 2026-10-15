"""Bind actual default-launcher correction without reducing full-port scope."""
import datetime,json
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v6236_current_mileena_source_audio_progress/progress.json'
EVIDENCE=ROOT/'audit_v6241_current_default_launcher_checked/report.json'
OUT=ROOT/'audit_v6243_current_default_launcher_progress'

def run():
 need(not OUT.exists(),'Fresh additive checkpoint')
 current.expected()
 parent=json.loads(PARENT.read_text());report=json.loads(EVIDENCE.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,
      'Full original scope retained')
 need(report['passed']and report['defaultNowUsesCurrentV5219']and
      report['actualForwardingCMDBootExitCode']==0 and report['actualROMAuditExitCode']==0 and
      report['preExistingUserSettingsUnchanged']and report['currentExePayloadAndAll16VoicesChecked'],
      'Actual checked current default boot and ROM/voice/settings evidence')
 pins=report['inputHashes'].copy()
 need(all(sha(p)==h for p,h in pins.items()),'Every tested input/evidence byte still exact')
 terminal=json.loads((EVIDENCE.parent/'native_terminal.json').read_text())
 need(terminal['exitCode']==0 and terminal['naturalTerminal']and terminal['observationError']is None,
      'Natural terminal recorded before host acceptance')
 retained=sorted(str(p.resolve())for p in ROOT.glob('diagnostic_v*')if(p/'mkport_candidate.exe').is_file())
 need(len(retained)==14,'Actual retained compiled-folder count, not highest version label')
 archive=ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'
 need(sha(archive)=='4D14CE6DD8F3D878BA02EDB112BAF43988A3E28B37EF1AC2FB7CE54F89E8670C',
      'Existing portable playtest unchanged')
 for p in(PARENT,EVIDENCE,Path(__file__).resolve(),archive,ROOT/'CURRENT_PLAYTEST_STATUS.md',
          ROOT/'WORKSPACE_CLEANUP_CURRENT.md',ROOT/'audit_v6239_current_default_launcher_checked/report.json'):
  pins[str(p)]=sha(p)
 OUT.mkdir()
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
      parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],inputHashes=pins,
      previousGoalTurnClassification='progress: actual ordinary default changed from obsolete1836 to current5219; initial host observation failed',
      thisGoalTurnClassification='progress: actual default CMD executable/ROM/voices/dependency denials/natural terminal/settings verified; handoff and storage policy corrected',
      currentDefaultLauncher=str(ROOT/'PLAY_MK2_KANO_SONYA.cmd'),currentDefaultBootEvidence=str(EVIDENCE),
      retainedCompiledCandidateFolders=retained,retainedCompiledCandidateCount=len(retained),
      versionLabelIsNotBuildCount=True,oldVersionedLauncherAndExactDefaultHistoryPreserved=True,
      originalFailedHostObservationPreserved=True,previousAttemptNativeExitCodeUnknown=True,
      currentReleaseZIPUnchanged=True,newBuilds=0,newZIPs=0,newRawMedia=0,
      interactiveVideoAndPhysicalAudioDeviceAcceptance=False,fullPortAcceptance=False,fullGoalComplete=False,
      nextActions=['Audit actual source-required remaining cinematic/finisher/arena contexts against existing current evidence; do not repeat completed campaigns',
                   'Complete combined normal-launcher selection/ladder/match/moves/KO/audio acceptance and final matching handoff'])
 (OUT/'progress.json').write_text(json.dumps(result,indent=2)+'\n')
 return {k:v for k,v in result.items()if k not in('inputHashes','retainedCompiledCandidateFolders')}

if __name__=='__main__':print(json.dumps(run(),indent=2),flush=True)
