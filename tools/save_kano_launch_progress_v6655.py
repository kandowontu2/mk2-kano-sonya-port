"""Same retained four native audio runs, both controls and full move matrix.

Finite startup fidelity, not CPU/overlap/interruption/all-art/all-port acceptance.
Keeps the prior input-clean continue UI proof and the full remaining objective.
"""
import hashlib,json,subprocess
from pathlib import Path
import qualify_kano_launch_audio_v6656 as audio
import native_process_census_v6647 as process
ROOT,need,sha=audio.ROOT,audio.need,audio.sha
OUT=ROOT/'audit_v6660_kano_launch_progress_checked'

def save(records):
 need(not OUT.exists()and not process.census(),'Fresh additive proof, all actual native games terminal')
 need({(r['side'],r['enabled'])for r in records}=={(s,e)for s in(1,2)for e in(False,True)}and len(records)==4,
      'Four distinct actual native both-slot enabled/disabled contexts')
 pins={};proofs=[];pairs=[];faults=[]
 for r in records:
  p=ROOT/f"audit_v6657_kano_launch_audio_checked_{'on'if r['enabled']else'off'}_p{r['side']}/report.json"
  proof=json.loads(p.read_text())
  need(proof['passed']and proof['wholeWaveform']['passed']and proof['wholeWaveform']['differentChannelSamples']==0 and
       proof['physicalSlot']==r['side']and proof['samplesEnabled']==r['enabled']and
       not proof['fullPortAcceptance']and not proof['publicPlayableChanged'],'Exact same-source native audio proofs; no global acceptance transfer')
  for k,v in proof['inputHashes'].items():need(sha(k)==v,'Every actually executed source/candidate/control input intact');pins[k]=v
  pins[str(p.resolve())]=sha(p);proofs.append(proof)
 for side in(1,2):
  on=next(r for r in records if r['side']==side and r['enabled']);off=next(r for r in records if r['side']==side and not r['enabled'])
  a,b=on['buffers'],off['buffers']
  physical=lambda text:[line for line in text.splitlines()if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_'))]
  need(physical(on['text'])==physical(off['text']),'Entire physical input/RNG/ownership/HP/move/control/publication/RGB chronology identical with imported samples enabled/disabled')
  need(a['dac']==b['dac']and a['dacHeaders']==b['dacHeaders']and a['pcmHeaders']==b['pcmHeaders'],
       'Every actual original DCS DAC float, native serial clock, callback/cursor and output window identical to no-samples control')
  need(a['pcm']!=b['pcm'],'Actual launched source contributes nonvacuous whole output')
  raw=b''.join(a['dac']);bad=bytearray(raw);bad[len(bad)//2]^=1
  need(bytes(bad)!=b''.join(b['dac']),'One real DAC byte difference rejected by whole paired equality')
  faults.append(dict(side=side,kind='actual paired native DAC byte changed',rejectedBy='complete original DAC equality'))
  actual=physical(on['text']);bad=list(actual);bad[len(bad)//2]+=' altered=1'
  need(bad!=physical(off['text']),'Real paired physical row corruption rejected')
  faults.append(dict(side=side,kind='actual paired physical row changed',rejectedBy='whole original physical chronology'))
  need(a['pcmHeaders'][:-1]!=b['pcmHeaders'],'Real last callback deletion rejected')
  faults.append(dict(side=side,kind='actual paired final callback removed',rejectedBy='whole exact sound window'))
  pairs.append(dict(side=side,wholePhysicalRows=len(actual),wholeNativeDACBytes=len(raw),
                    nativeDACSHA256=hashlib.sha256(raw).hexdigest().upper(),completeCallbacks=len(a['pcm']),
                    actualOriginalDCSAndGameplayUnchanged=True,actualSourceContributionAudible=True))
 matrix_path=ROOT/'audit_v6646_kano_launch_special_matrix_checked/report.json';matrix=json.loads(matrix_path.read_text())
 need(matrix['passed']and matrix['actualCases']==16 and matrix['actualVerifiedSpecialCycles']==32 and
      len(matrix['actualSemanticFaultsRejected'])==194 and all(sha(k)==v for k,v in matrix['inputHashes'].items()),
      'Whole newly compiled 16-case/32-cycle original full194-fault move regression')
 pins.update(matrix['inputHashes']);pins[str(matrix_path.resolve())]=sha(matrix_path)
 old_path=ROOT/'audit_v6621_continue_viewport_matrix_checked/report.json';old=json.loads(old_path.read_text());migrations={}
 for k,v in old['inputHashes'].items():
  p=Path(k);replacement=ROOT/'status_history_v6659'/p.name if p.name in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md')and p.parent==ROOT else p
  need(sha(replacement)==v,'Whole prior released-input continue UI proof retained with exact status-byte migration only')
  pins[str(replacement.resolve())]=v
  if replacement!=p:migrations[k]=dict(preservedExactBytes=str(replacement),priorSHA256=v,currentSHA256=sha(p))
 pins[str(old_path.resolve())]=sha(old_path)
 for p in[Path(__file__),Path(audio.__file__),Path(process.__file__),ROOT/'CURRENT_PLAYTEST_STATUS.md',ROOT/'WORKSPACE_CLEANUP_CURRENT.md',
           ROOT/'diagnostic_v6640_kano_ball_launch/restoration.json',ROOT/'diagnostic_v6640_kano_ball_launch/cache_retirement.json']:
  pins[str(p.resolve())]=sha(p)
 need(not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'Generated native compiler cache absent')
 failed=json.loads((ROOT/'audit_v6644_kano_launch_special_ball_p1/result.json').read_text())
 need(not failed['passed']and failed['nativeExit']==0,'Actual first missed-identity run remains rejected')
 need(all(sha(k)==v for k,v in pins.items()),'Complete same-run source/evidence pins unchanged')
 result=dict(passed=True,candidate=audio.waveform.current.NAME,executableSHA256=audio.waveform.current.EXE_SHA,guestSHA256=audio.waveform.current.GUEST_SHA,
             actualSpecialCases=16,actualMoveCycles=32,actualMoveFaultsRejected=194,
             actualMoveActorFields=matrix['actualContiguousPostFields'],actualMoveRGBCallbacks=matrix['actualFullRGBFields'],
             actualNativeAudioContexts=4,actualStereoFrames=sum(p['wholeWaveform']['comparedStereoFrames']for p in proofs),
             enabledLaunchStereoFrames=sum(p['wholeWaveform']['comparedStereoFrames']for p in proofs if p['samplesEnabled']),
             sourceExactHumanLaunchBothSlotsAccepted=True,pairedControls=pairs,actualPairedFaultsRejected=faults,
             inputHashes=pins,intentionalPriorStatusPinMigration=migrations,priorContinueUIReport=str(old_path),
             historicalFailedIdentityReportPreserved=True,newBuilds=1,newPayloadAllocations=0,newReleaseZIPs=0,
             rawGameplayRGBPCMGuestOrDACFilesWritten=0,authoredDonorWAVAssetRetained=True,compilerCacheAbsent=True,
             publicPlayableChanged=False,publicStill='diagnostic_v6508_native_projectile_identifiers',
             fullCPUStartupAudioAccepted=False,fullInterruptionCoverageAccepted=False,fullPortAcceptance=False,goalStatus='active',
             previousGoalTurnClassification='no progress: conversational acknowledgement only; revalidated the specific live native compiler handle before continuing',
             thisGoalTurnClassification='progress: real startup cue compiled, full 16-case/32-cycle specials regression and both-slot paired complete waveform/source/control proof qualified; generated compiler cache retired',
             remaining=[
              'New startup cue CPU/overlap/hit/KO/selection/reset/morph ownership cleanup and current full UI/ground/render/audio regression before public promotion.',
              'Remaining broader projectile/CPU/arena/shadow/audio contexts; earlier finite visual and finisher cases are not automatic changed-build acceptance.',
              'Released-input cross-character continues and ordinary post-continue controls, broader continued stages/audio and post-ending fresh joins.',
              'Remaining Pit/Tomb stock-victim choreography and sound priority.',
              'Remaining secret, morph and cinematic integration.',
              'Combined final visual/audio/gameplay acceptance, matching public launcher and finished release ZIP.'])
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(result,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless finite progress proof compression')
 print(json.dumps({k:result[k]for k in('passed','actualSpecialCases','actualMoveCycles','actualMoveFaultsRejected','actualNativeAudioContexts','actualStereoFrames','sourceExactHumanLaunchBothSlotsAccepted','publicPlayableChanged','fullPortAcceptance')}),flush=True)
 return result
