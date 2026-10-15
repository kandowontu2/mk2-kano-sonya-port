"""Terminal normal arm audio proof; original five full-goal groups remain."""
import json,subprocess
from pathlib import Path
import verify_jax_arms_audio_closure_v4237 as closure
ROOT,need,sha=closure.ROOT,closure.need,closure.sha
PARENT=ROOT/'audit_v4222_storage_campaign_arm_audio_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4240_arm_audio_terminal_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable terminal full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    for p,h in pins.items():need(sha(p)==h,'Every inherited logical byte unchanged')
    def pin(p,wanted=None):
        p=Path(p).resolve();key=str(p);h=sha(p)
        need(key not in pins or pins[key]==h,'Inherited/shared actual evidence remains unchanged')
        need(wanted is None or wanted==h,'Exact executed evidence hash');pins[key]=h
    pin(PARENT);pin(__file__)
    reports={}
    for name in ('audit_v4233_jax_arms_complete_audio_checked','audit_v4236_remaining_arm_packet_callers_observed','audit_v4238_jax_arms_audio_closure_checked','audit_v4226_jax_arms_direct_packet_callers_observed','audit_v4230_sonya_p2_arm_audio_reject_observed'):
        p=ROOT/name/'report.json';r=json.loads(p.read_text());need(r['passed']and not r['fullPortAcceptance'],'Actual completed bounded proof, not full port');pin(p);reports[name]=r
        for p,h in r['inputHashes'].items():pin(p,h)
    r=reports['audit_v4238_jax_arms_audio_closure_checked']
    need(r['actualContexts']==4 and r['actualPairedCaptures']==8 and r['additionalReadOnlyCallerTraceCaptures']==4 and r['totalActualCounterexamplesRejected']==151,'Actual four normal owned contexts/eightpairedcaptures/fourcallertraces/151faults')
    need(r['actualNativeSelectorCommands']==220 and r['actualNativeAdmittedSelectorPackets']==219 and r['actualNativePriorityDeclines']==1 and r['actualDirectCallerPackets']==16 and r['actualNativeDCSBytesDelivered']==470,'Complete original native selector/direct packet/priority decline/DCS inventory')
    need(r['fullNativePCMExactlyUnaffectedBySamples']and r['actualAllFourDirectCallerOriginsObservedAndSourceBound']and r['normalDeadPoolJaxArmAudioBoundedAcceptance'],'Whole mixed native PCM and all4actual original caller origins independently qualified')
    need(not r['allArenasAccepted']and not r['alternateCostumesAccepted']and not r['allFinisherAudioAccepted']and not r['stockReferenceWholeWaveformFidelityAccepted'],'Full original fidelity scope is not narrowed to4normal tests')
    failed=ROOT/'audit_v4220_jax_arms_native_audio_routes_checked/report.json';f=json.loads(failed.read_text())
    need(not f['passed']and len(f['completed'])==3 and 'One actual original priority slot'in f['error'],'Third false every-selector-admitted assumption and actual3completed partialcases preserved');pin(failed)
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process -Filter "ProcessId=11348 OR ProcessId=124616 OR ProcessId=118888 OR ProcessId=126724" | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'Old audio11348/fullqualifier124616/storage118888/campaign126724 actually terminal; their tool handles consumed')
    for name in ('mk2ks_jax_arms_audio_callers_ram_v4223.lua','tools/run_jax_arms_direct_packet_callers_v4224.py','mk2ks_jax_arms_audio_reject_ram_v4227.lua','tools/run_sonya_p2_arm_audio_reject_v4228.py','tools/verify_jax_arms_native_audio_routes_v4231.py','tools/verify_jax_arms_complete_audio_v4232.py','tools/run_remaining_arm_packet_callers_v4234.py','tools/verify_jax_arms_audio_closure_v4237.py'):pin(ROOT/name)
    state.update(inputHashes=pins,previousCheckpoint=str(PARENT),inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='All inherited full-scope requirements/exclusions and logical bytes preserved.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: consumed storage7745 and campaign2326 terminal0; exact33517files preserved/reversible3392749568B savings; bounded campaign33wins/99losses/Mileena9/noending, no towerclear. Completed12native normal DeadPool earned arm audio captures:8trueown17/18paired on/off in4contexts plus4readonlycaller/rejecttraces; all original1074physicalBBBBLPgap96/322collisiondamage/2nativeKOs/trueIDtables/2proppaletteconsumers/147fieldwrap preserved. Original3952complete PCM/channel/packet/ADSP grammar retained with source-bound50Hzdeadline; actual220selectors219admitted1genuinebloodprioritydecline16directpackets470DCSbytes, all native PCM unchanged on/off. Actual native priority22 beneath112/96/80 slots and rejectPCFFA129E0 observed, not forced. Actual four direct caller origins observed inall4contexts and originalnativeclear0/fatalbegin34/mode2wrap35/continue38 code unchanged.151real state/audio/palette/priority/direct-caller counterexamples rejected. Preserved false4214deadline,4217overwidewindow and4220all-selector-admitted reports; no repeated capture for checker repair. Finished4233/4236/4238proofs terminal0, no stale live-job claims. No native raster/VRAM/PCM/wholeguest copies to disk, no newbuild/gamepublic edits. All original five remaining groups intact.',
      currentDevelopmentArmAudioReport=str(ROOT/'audit_v4238_jax_arms_audio_closure_checked/report.json'),
      armAudioState=dict(completeBoundedNormalDeadPoolProof=True,report=str(ROOT/'audit_v4238_jax_arms_audio_closure_checked/report.json'),actualOwnContexts=4,actualPairedNativeCaptures=8,actualAdditionalReadonlyCallerTraceCaptures=4,actualOriginalSelectorCommands=220,actualAdmittedSelectorPackets=219,actualNativePriorityDeclines=1,actualDirectCallerPackets=16,actualNativeDCSBytesDelivered=470,actualCounterexamplesRejected=151,
        originalPhysicalBBBBLPGap96=True,trueOwnVictims17And18=True,realCollisionDamagePerCase=322,nativeRoundsPerCase=2,nativeWrapAge=147,completeOriginalEarnedStatePaletteTableAlgorithmRetained=True,completeGenericPCMChannelsPacketsADSPAlgorithmRetained=True,wholeMixedPCMExactlyIdenticalOnOff=True,all4ActualDirectCallerOriginsSourceBound=True,
        immutableFalseAssumptionReports=[str(ROOT/n/'report.json')for n in('audit_v4214_jax_arms_native_audio_routes_observed','audit_v4217_jax_arms_native_audio_routes_checked','audit_v4220_jax_arms_native_audio_routes_checked')],
        completedExecHandles=[4904,98319,31306,57921,97417,88195,46848],hostExit750=True,rawNativeMediaCopiesWritten=0,allArenasAccepted=False,alternateCostumesAccepted=False,allFinisherAudioAccepted=False,stockReferenceWholeWaveformFidelityAccepted=False,fullPortAcceptance=False),
      currentTurnReclaimedAllocatedBytes=3392749568,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnNewNativeAudioRasterROMCopies=0,
      cleanupAccounting='Only completed4207report total3392749568B counted this turn. Earlier4205sample41115648B and4207partial rows are not added again; historical cleanup accounting unchanged.',
      nextImplementationAction='Normal DeadPool Jax arm native state/voice/PCM/priority/direct packets are now bounded source-qualified in4trueown contexts with151faults, not allfinishers/arenas/alternates/stockwholewaveform. All4233/4236/4238audio jobs andold4207storage/4197campaign jobs actually terminal and consumed; do not restart them. Next broaden actual arm alternate palette/allstage execution and other native finishers/cinematics, or advance remaining native Pit/Tomb victim/mirror/branch/stage audio coverage. Full SonyaP2 natural tower/ownending/attract still absent; combinedmirror+zoning failedMileena9 after99paidlosses, use new actual native feedback before different physical strategy, not an identical losing rerun or health/AI/roster/difficulty/RNG/position override. All five original groups remain: broader Pit/Tomb branches/mirrors/victim/stage audio; all move art/ground/shadows/cleanup/CPU/repeat/KO/overlap arenas; other finishers/victims/morphs/secrets/cinematics; full natural towers/own endings/attract; combined UI/ladder/names/audio, dependency-aware cleanup and refreshed finalZIP. Public1836/ZIP installed binary and dirty12file source unchanged; no retired dependency resurrection or broad rejected deletion retry.',
      gameSourceAndPlayableBytesChangedThisTurn=False,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'Entire original goal retained')
    for p,h in pins.items():need(sha(p)==h,'All aggregated native evidence unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writing')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),pins=len(pins),normalArmNativeAudioContexts=4,actualCounterexamplesRejected=151,currentCompletedReclaimedBytes=3392749568,allOriginalRemainingGroups=len(remaining),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
