"""Preserve full-port scope and stage collision evidence, without build promotion."""
import json
import subprocess
from pathlib import Path
import verify_native_sound_packet_guard_v3669 as guard
import compact_current_tomb_logs_v3654 as storage

ROOT,need,sha=guard.ROOT,guard.need,guard.sha
PREVIOUS=ROOT/'audit_v3659_current_tomb_matrix_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3672_native_sound_packet_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh full-scope checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=list(state['remaining'])
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],
         'Original full objective and all five remaining groups retained')
    report_file=guard.OUT/'report.json';report=json.loads(report_file.read_text())
    need(report['passed']and report['stagedFixRequiresCompilationAndRuntimeRegression']and
         report['actualWrongImportedFireTransitions']and not report['publicBuildChanged']and
         not report['nativeDCSStageOrVictimWaveformFidelityAccepted'],'Real staged bug fix, no compiled/runtime/audio promotion')
    fresh={}
    def pin(p,wanted=None):
        key=str(Path(p).resolve());digest=sha(p)
        need(wanted is None or digest==wanted,'Actual current source/evidence remains unchanged')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Never relabel inherited pins')
        need(key not in fresh or fresh[key]==digest,'Consistent fresh evidence')
        fresh[key]=digest
    for p,h in report['inputHashes'].items():pin(p,h)
    for p in(PREVIOUS,report_file,Path(__file__).resolve()):pin(p)
    compressed=[]
    for name in('audit_v3662_current_kano_tomb_audio_p1_samples','audit_v3662_current_kano_tomb_audio_p1_nosamples',
                 'audit_v3666_current_kano_tomb_audio_p1_samples','audit_v3666_current_kano_tomb_audio_p1_nosamples'):
        leaf=ROOT/name;terminal=json.loads((leaf/'result.json').read_text())
        need(terminal['exit_code']==0 and terminal['rawAudioFilesWritten']==0,'Sealed actual terminal RAM-only capture')
        log=leaf/'run.log';before=storage.allocated(log);digest=sha(log);size=log.stat().st_size
        result=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(log)],capture_output=True,text=True)
        need(result.returncode==0 and sha(log)==digest and log.stat().st_size==size,'Lossless sealed-log compression only')
        compressed.append(dict(path=str(log),logicalBytes=size,beforeAllocatedBytes=before,afterAllocatedBytes=storage.allocated(log),sha256=digest))
        for file in leaf.rglob('*'):
            if file.is_file():pin(file)
    state.update(previousCheckpoint=str(PREVIOUS),
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentSHA256=sha(PREVIOUS),
        mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten historical map.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: current compiled source/checkpoint inspected before editing. Four actual current3172 earned KanoP1 Tomb samples-on/off captures terminal0, PCM streamed solely to RAM. First3663 rejects boot-ROM-read false origin; fresh3664 actual CPU-fetch qualification removes false action.3667 rejects wrong female packed-byte expectation; original program independently proves proper38h/39h selection and trueID18/owned victim. Actual3666late nativeFFA13D60 FFF8 packet incorrectly starts sample6/channel2 nextfield: imported Sonya fire replaces a valid DCS packet after Tomb retirement. Fresh3668 staged whole current machine adds only originalpacket-site discrimination to3FFmarker conditions, preserving every native packet and all direct cues.3670 source/fullguest/storeopcodes/currentchanneltransition and196608word routing comparisons pass. No working user checkout, executable, ROM, public CMD/ZIP or historical capture source changed. Fix is staged, still requires current-source compile and runtime regression; no universal audio or finished-port claim.',
      stagedNativeSoundPacketFix=dict(source=report['stagedSource'],sha256=report['stagedSourceSHA256'],report=str(report_file),
        confirmedBug='Native sign-extended F8 at FFA13D60 after Tomb wrongly plays Sonya burn fire and is swallowed instead of reaching DCS',
        compiled=False,runtimeRegressionPassed=False),
      currentStageAudioAcceptance=False,
      sealedAudioCaptureCompression=compressed,
      sourceAndPlayableStateThisTurn=dict(stagedFix=True,userCheckoutChanged=False,playableBytesChanged=False,newBuilds=0,rawAudioFiles=0),
      nextAction='Compile the staged3668native sound packet guard against actual current3172 source/payload without restoring retired data or promoting public1836. Verify exact guest unchanged and original native commands reach DCS, while all direct selection/winner/kiss/extract/burn cues still play on correct finite channels. Repair diagnostic female range from source38h/39h and identify idle channels by source_numFFFFFFFF rather than stale source_len. Bind full mixed audio to originals; distinguish stage lifetime/retirement from following attract/selection audio rather than falsely requiring all later sound to be silent. Continue bothslots/stock/new/mirror/Pitbranches and full remaining5groups, then combinedUI/ladder/names/audio and refreshed release. Do not rerun completed Tomb visual or P1campaign/endings/Friendship gates merely for metadata. Preserve public CMD/ZIP and dirty historical checkout. No more ordinary bulk build/audio/raster/VRAM copies; required builds fresh compressed leaf with exact restoration.')
    state['inputHashes']=fresh
    need(state['remaining']==remaining and not state['fullPortAcceptance']and not state['finishedRelease'], 'No narrowed objective')
    OUT.mkdir();file=OUT/'checkpoint.json';file.write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(file),freshPins=len(fresh),stagedFixAwaitingBuild=True,
      newExecutableROMRasterAudioCopies=0,losslessLogAllocatedBytesFreed=sum(r['beforeAllocatedBytes']-r['afterAllocatedBytes']for r in compressed),
      fullPortAcceptance=False),indent=2))

if __name__=='__main__':main()
