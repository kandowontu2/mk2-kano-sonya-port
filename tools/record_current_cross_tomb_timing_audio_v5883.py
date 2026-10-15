"""Seal full missing-cross audio evidence, retaining all original goal groups.

Entire5844 receipt gates retained. Actual independent timing checks and native
callback counts replace old fixed-profile facts, never trimming audio to an old
fixture. Complete wider victims/art/choreography/release acceptance is not given.
"""
import datetime,inspect,json,subprocess
from pathlib import Path
import record_current_cross_tomb_audio_v5844 as original
import run_current_cross_tomb_timing_audio_v5877 as host
ROOT,need,sha=original.ROOT,original.need,original.sha
current,allocated=original.current,original.allocated
OUT=ROOT/'audit_v5884_current_cross_tomb_timing_audio_progress'
INITIAL_IDENTITIES={
 'kano1':dict(hostPID=148044,hostCreated='2026-10-08T04:38:27.102598-04:00',pid=139728,created='2026-10-08T04:38:32.097564-04:00'),
 'kano2':dict(hostPID=144204,hostCreated='2026-10-08T04:38:27.105709-04:00',pid=131204,created='2026-10-08T04:38:32.074955-04:00'),
 'sonya1':dict(hostPID=142168,hostCreated='2026-10-08T04:38:27.168090-04:00',pid=117808,created='2026-10-08T04:38:32.180446-04:00'),
 'sonya2':dict(hostPID=145532,hostCreated='2026-10-08T04:38:27.169955-04:00',pid=149088,created='2026-10-08T04:38:32.178593-04:00'),
}

def once(code,before,after):
 need(code.count(before)==1,'Exactly declared whole current audio receipt adaptation: '+before)
 return code.replace(before,after,1)

run_source=inspect.getsource(original.run)
changes=(
 ('audit_v5832_current_pressed_tomb_full_scene_matrix_progress/progress.json','audit_v5875_current_cross_tomb_native_timing_progress/progress.json'),
 ("parent['actualCurrentHeldPressedAndRandomMirrorFullScenesRetained']", "parent['actualMissingCrossP1HeldAndP2RandomDropStatesAccepted']and parent['priorCurrentCrossObservedPressedAudioAndFullScenesAndAllMirrorBranchesRetained']"),
 ('audit_v5843_current_cross_tomb_audio_checked/report.json','audit_v5882_current_cross_tomb_timing_audio_checked/report.json'),
 ('actualCurrentBothCharactersBothSidesOppositeTombEnabledWinnerMixAccepted','actualCurrentBothCharactersBothSidesMissingCrossTombEnabledWinnerMixAccepted'),
 ("report['exactStereoPCMFrames']==3863040", "report['exactStereoPCMFrames']==3864000 and report['actualPhysicalTimingFaultsRejected']==20 and report['actualOriginalPCIONativeBranchFaultsRejected']==16"),
 ("  process=json.loads((folder/'process.json').read_text());processes.append(process)",
  "  process=json.loads((folder/'process.json').read_text());processes.append(process)\n  initial=INITIAL_IDENTITIES[case['fighter']+str(case['physicalSlot'])]\n  need(process['pid']==initial['pid']and process['hostPID']==initial['hostPID']and\n   abs(process['startedUnix']-datetime.datetime.fromisoformat(initial['created']).timestamp())<.05,\n   'Actual native and host names, complete commands and creation dates independently inspected live')"),
 ("  channels=case['actualWinnerChannelClockAndRetirement'];wave=live['waveform']",
  "  channels=case['actualWinnerChannelClockAndRetirement'];wave=live['waveform']\n  expected_updates=1007 if(case['fighter'],case['physicalSlot'])==('sonya',1)else 1006\n  expected_frames=expected_updates*960\n  timing=host.selected_profile(case['fighter'],case['physicalSlot'])\n  need(branch==timing['nativeBranch']and falling==(case['physicalSlot']==2)and\n   case['actualPhysicalInputTimingProof']['passed']and\n   case['actualPhysicalInputTimingProof']['physicalCommandDelay']==timing['physicalCommandDelay']and\n   case['actualPhysicalInputTimingProof']['exactPhysicalRecords']>100 and\n   len(case['actualPhysicalTimingFaultsRejected'])==5 and\n   case['actualOriginalPCIONativeBranchFaultsRejected']==live['actualOriginalBranchFaultsRejected']and\n   live['actualPhysicalCommandDelayProof']['nativeBranch']==branch and\n   live['actualPhysicalCommandDelayProof']['physicalCommandDelay']==timing['physicalCommandDelay'],\n   'Actual independent complete paid selection/KO/button/cleanup timeline and five declared-delay counterexamples')"),
 ("channels['preciseSourceChannelStates']==14084", "channels['preciseSourceChannelStates']==14*expected_updates"),
 ("wave['comparedStereoFrames']==965760", "wave['comparedStereoFrames']==expected_frames and meta['mixedPCMUpdates']==expected_updates and meta['mixedPCMBytesVerifiedInRAM']==4*expected_frames"),
 ("len(wave['actualCallbackSourceClocks'])==1006", "len(wave['actualCallbackSourceClocks'])==expected_updates"),
 ('exactStereoPCMFrames=965760,actualSourceWindowChannelFaultsRejected=33',
  "exactStereoPCMFrames=expected_frames,nativeSoundCallbacks=expected_updates,physicalCommandDelay=timing['physicalCommandDelay'],actualPhysicalTimingFaultsRejected=5,actualSourceWindowChannelFaultsRejected=33"),
 ('mk2ks_current_cross_tomb_campaign_v5835.lua','mk2ks_current_cross_tomb_timing_audio_v5876.lua'),
 ('run_current_cross_tomb_audio_v5838.py','run_current_cross_tomb_timing_audio_v5877.py'),
 ('mk2ks_current_cross_tomb_driver_v5833.lua','mk2ks_current_cross_tomb_timing_driver_v5870.lua'),
 ('mk2ks_current_cross_tomb_provenance_v5834.lua','mk2ks_current_cross_tomb_timing_provenance_v5871.lua'),
 ('qualify_current_cross_tomb_audio_v5839.py','qualify_current_cross_tomb_timing_audio_v5878.py'),
 ('verify_current_cross_tomb_audio_v5842.py','verify_current_cross_tomb_timing_audio_v5881.py'),
 ('audit_v5840_current_cross_tomb_audio_source_checked/report.json','audit_v5879_current_cross_tomb_timing_audio_source_checked/report.json'),
 ('actualCurrentBothCharactersBothSlotsOppositeTombEnabledAudioAccepted=True',
  'actualCurrentBothCharactersBothSlotsMissingCrossTombEnabledAudioAccepted=True,priorCrossObservedPressedAudioAndFullScenesRetained=True'),
 ('allCurrentCrossHeldPressedRandomContextsAccepted=False',
  'allCurrentCrossHeldPressedRandomEnabledAudioAccepted=True,allCurrentCrossHeldPressedRandomFullScenesAccepted=False'),
 ('exactStereoPCMFrames=3863040,actualSourceWindowChannelFaultsRejected=132',
  'exactStereoPCMFrames=3864000,retainedAll12CrossContextsExactStereoPCMFrames=11590080,actualPhysicalTimingFaultsRejected=20,actualSourceWindowChannelFaultsRejected=132'),
 ('consumedCaptureToolSessions=[35686,35359,19246,67771],consumedMatrixToolSessions=[80852]',
  'consumedCaptureToolSessions=[84413,32114,39287,6216],consumedMatrixToolSessions=[54695],initialLiveProcessIdentities=INITIAL_IDENTITIES'),
)
for before,after in changes:
 if before in ('mk2ks_current_cross_tomb_campaign_v5835.lua','run_current_cross_tomb_audio_v5838.py'):
  need(run_source.count(before)==2,'Exactly the terminal process predicate and immutable source pin: '+before)
  run_source=run_source.replace(before,after,2)
 else:run_source=once(run_source,before,after)
start=run_source.index("  previousGoalTurnClassification='")
end=run_source.index("',\n",start)+2
run_source=run_source[:start]+"  previousGoalTurnClassification=parent['thisGoalTurnClassification'],"+run_source[end:]
classification='progress: four actual current missing cross Tomb heldP1/random-dropP2 enabled audio cases completed. Every independent normal input timeline and genuine RNG outcome agrees with prior bare timing runs. Full original earned/PC/IO/actor/Main/held or269drop/801cleanup, initial and late victim roles, all general cue/queue/port/DSP and precise14channel/start/retirement gates pass. All3,864,000actual stereo frames exactly equal native source mixer prediction, with132window/source,48earned16branch8phase16voice20timing and16raw/16source-operation faults rejecting. Earlier observed/pressed cross cases complete finite12context audio coverage, not broader victims or scene/cinematic/all-port acceptance. All original five goal groups remain active.'
start=run_source.index("  thisGoalTurnClassification='")
end=run_source.index("',\n",start)+2
run_source=run_source[:start]+'  thisGoalTurnClassification='+repr(classification)+','+run_source[end:]
next_work='Use these four actual missing-cross audio references for complete native one-base CPU/DMA/shift/VRAM/palette/RGB/body/composite/cache/projection/ground/compressed floor-shadow/retirement+30 scene checks. No repeat of completed timing/audio matrices for status. Continue broader native Pit/Tomb stock victims, exact source audio priority/RNG choices, independent stock choreography, all original move/arena/CPU/repeated/KO/overlap and other finisher/victim/morph/secret/cinematic requirements, retained natural campaigns/own endings and final combined UI/ladder/names/audio plus dependency-aware cleanup and refreshed release ZIP. Never regenerate permanently retired builds/raw history.'
start=run_source.index("  next='")
end=run_source.index("')",start)+1
run_source=run_source[:start]+'  next='+repr(next_work)+run_source[end:]
run_scope=dict(vars(original),__file__=__file__,__doc__=__doc__,OUT=OUT,host=host,INITIAL_IDENTITIES=INITIAL_IDENTITIES)
exec(compile(run_source,__file__+'::whole5844_actual_missing_cross_audio_receipt','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':run()
