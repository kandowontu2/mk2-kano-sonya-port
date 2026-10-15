"""Replace obsolete prepared/staged status with terminal, scope-correct status."""
import json
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as evidence

ROOT,need,sha=evidence.ROOT,evidence.need,evidence.sha
PREVIOUS=ROOT/'audit_v3695_native_sound_delivery_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3697_native_sound_terminal_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh terminal status checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=list(state['remaining'])
    need(state['current3680TombBothCharactersBothSlotsNativePacketDeliveryWinnerMixAccepted']and
         state['completedNativeSoundBuild']['terminalExitCode']==0 and state['pendingNativeSoundBuild']is None and
         state['current3680ActualNativeBytesDelivered']==212 and not state['fullPortAcceptance'], 'Terminal compiled runtime proof, not all-port acceptance')
    state['stagedNativeSoundPacketFix'].update(compiled=True,runtimeRegressionPassed=True,
      runtimeRegressionScope='Only both true performers/both physical slots earned Tomb, actual native ADSP delivery, complete winner waveform and recorded state equivalence',
      allOtherDirectCuesSelectionAndFullStageWaveformRegressionPassed=False,candidate=evidence.NAME)
    state['preparedNativeSoundRuntimeRegression'].update(executed=True,terminalExitCode=0,passed=True,
      report=str(ROOT/'audit_v3684_native_sound_delivery_ram_checked/report.json'),
      remainingP2Report=str(ROOT/'audit_v3691_native_sound_delivery_p2_checked/report.json'),fullPortAcceptance=False)
    state['gameSourceAndPlayableBytesChangedThisTurn']=True
    state['sourceAndPlayableStateThisTurn']=dict(newlyCompiledDiagnostic=evidence.NAME,hostSourceGuardChanged=True,
      guestPayloadUnchanged=True,userCheckoutRestored=True,existingPublicPlayableBytesChanged=False,newDiagnosticExecutable=1,
      immutablePayloadHardlinkWithoutNewPayloadData=True,rawAudioFiles=0)
    state['developmentCandidate']=evidence.NAME
    state['previousCheckpoint']=str(PREVIOUS)
    state['inputHashInheritance']=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentSHA256=sha(PREVIOUS),
      mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Never flatten historical map.')
    state['inputHashes']={str(PREVIOUS):sha(PREVIOUS),str(Path(__file__).resolve()):sha(__file__)}
    need(state['remaining']==remaining and len(remaining)==5 and not state['finishedRelease'], 'No altered/narrowed original objective')
    OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),compiledRuntimeGuardValidated=True,publicBuildChanged=False,
      otherDirectCuesAndFullStageAudioPending=True,fullPortAcceptance=False),indent=2))

if __name__=='__main__':main()
