"""Whole5850 full-scene matrix for remaining actual cross Tomb timings.

Retains complete original raster/body/ground/shadow/retirement+30 and actual
input/earned/branch/phase faults. Independent timing evidence is additional,
not a substitute for native rendering. All five original goal groups retained.
"""
import datetime,gzip,hashlib,inspect,json,re,subprocess
from pathlib import Path
import assemble_current_cross_tomb_full_scene_v5850 as original
import run_current_cross_tomb_timing_render_ram_v5886 as runtime
import record_current_cross_tomb_audio_v5844 as storage
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
OUT=ROOT/'audit_v5890_current_cross_tomb_timing_full_scene_matrix_progress'
INITIAL_IDENTITIES={
 'kano1':dict(hostPID=110580,hostCreated='2026-10-08T04:52:41.2420450-04:00',pid=139960,created='2026-10-08T04:52:55.0650090-04:00'),
 'kano2':dict(hostPID=143456,hostCreated='2026-10-08T04:52:41.2423460-04:00',pid=85404,created='2026-10-08T04:52:54.9831870-04:00'),
 'sonya1':dict(hostPID=145992,hostCreated='2026-10-08T04:52:41.2412480-04:00',pid=139972,created='2026-10-08T04:52:55.0657710-04:00'),
 'sonya2':dict(hostPID=145064,hostCreated='2026-10-08T04:52:41.2427670-04:00',pid=153072,created='2026-10-08T04:52:55.0571750-04:00'),
}
records=original.records
once=runtime.once
run_source=inspect.getsource(original.run)
changes=(
 ('audit_v5845_current_cross_tomb_enabled_audio_progress/progress.json','audit_v5884_current_cross_tomb_timing_audio_progress/progress.json'),
 ("parent['allPriorMirrorHeldPressedRandomFullScenesRetained']",
  "parent['allPriorMirrorHeldPressedRandomFullScenesRetained']and parent['allCurrentCrossHeldPressedRandomEnabledAudioAccepted']and parent['priorCrossObservedPressedAudioAndFullScenesRetained']"),
 ('audit_v5843_current_cross_tomb_audio_checked/report.json','audit_v5882_current_cross_tomb_timing_audio_checked/report.json'),
 ('actualCurrentOppositeNativeTombWholeRenderPaletteShadowEraseAccepted','actualCurrentMissingCrossNativeTombWholeRenderPaletteShadowEraseAccepted'),
 ("  with gzip.open(Path(ref['capture'])/'run.log.gz','rt')as reader:audio_text=reader.read()",
  "  timing=runtime.audio_proof.physical_gate(text,guest,fighter,side)\n  need(report['actualPhysicalInputTimingProof']==timing==ref['actualPhysicalInputTimingProof']and\n   len(report['actualPhysicalTimingFaultsRejected'])==5 and\n   report['actualPhysicalTimingFaultsRejected']==runtime.audio_proof.timing_faults(text,guest,fighter,side),\n   'Entire independent bare timing and enabled-audio physical records and five actual timing counterexamples retained')\n  with gzip.open(Path(ref['capture'])/'run.log.gz','rt')as reader:audio_text=reader.read()"),
 ('actualEarnedFaultsRejected=12,actualBranchFaultsRejected=4,',
  "physicalCommandDelay=timing['physicalCommandDelay'],actualPhysicalTimingFaultsRejected=5,actualEarnedFaultsRejected=12,actualBranchFaultsRejected=4,"),
 ('mk2ks_current_cross_tomb_display_ram_v5846.lua','mk2ks_current_cross_tomb_timing_display_ram_v5885.lua'),
 ('run_current_cross_tomb_render_ram_v5847.py','run_current_cross_tomb_timing_render_ram_v5886.py'),
 ('actualCurrentBothCharactersBothSlotsOppositeTombFullSceneGroundShadowEraseAccepted=True',
  'actualCurrentBothCharactersBothSlotsMissingCrossTombFullSceneGroundShadowEraseAccepted=True'),
 ('actualEarnedFaultsRejected=48,actualBranchFaultsRejected=16,actualRasterFaultsRejected=8,',
  'actualPhysicalTimingFaultsRejected=20,actualEarnedFaultsRejected=48,actualBranchFaultsRejected=16,actualRasterFaultsRejected=8,'),
 ('allCurrentCrossHeldPressedRandomFullScenesAccepted=False,',
  'allCurrentCrossHeldPressedRandomFullScenesAccepted=True,allCurrentCrossHeldPressedRandomEnabledAudioRetained=True,'),
 ('consumedCaptureToolSessions=[91097,53813,16842,61026]',
  'consumedCaptureToolSessions=[96594,35911,1260,71319]'),
 (" sealed=list(dict.fromkeys(p.resolve()for p in sealed));before={str(p):sha(p)for p in sealed}",
  " sealed=list(dict.fromkeys(p.resolve()for p in sealed));before={str(p):sha(p)for p in sealed}\n before_allocated=sum(storage.allocated(p)for p in sealed)"),
 (" need(all(sha(p)==h for p,h in before.items()),'Every sealed full evidence/source byte unchanged')",
  " need(all(sha(p)==h for p,h in before.items()),'Every sealed full evidence/source byte unchanged')\n after_allocated=sum(storage.allocated(p)for p in sealed)\n prior=[]\n for leaf,key in [('audit_v5851_current_cross_tomb_full_scene_matrix_progress','actualCurrentBothCharactersBothSlotsOppositeTombFullSceneGroundShadowEraseAccepted'),('audit_v5869_current_cross_pressed_tomb_full_scene_matrix_progress','actualCurrentBothCharactersBothSlotsCrossPressedTombFullSceneGroundShadowEraseAccepted')]:\n  path=ROOT/leaf/'progress.json';p=json.loads(path.read_text())\n  need(p['passed']and p[key]and len(p['cases'])==4 and sha(path)==parent['newInputHashes'][str(path)]and not p['fullPortAcceptance'],\n   'Whole previous four observed unpressed and four physically pressed cross scenes remain source-bound')\n  prior.append(p)"),
 ('sealedTextSourcesLosslesslyCompacted=len(sealed),initialLiveProcessIdentities=INITIAL_IDENTITIES,',
  "sealedTextSourcesLosslesslyCompacted=len(sealed),sealedAllocatedBytesBefore=before_allocated,sealedAllocatedBytesAfter=after_allocated,sealedAllocatedBytesReclaimed=before_allocated-after_allocated,initialLiveProcessIdentities=INITIAL_IDENTITIES,retainedAll12CrossContextsWholeVisibleFields=sum(p['wholeVisibleFields']for p in prior)+sum(c['wholeVisibleFields']for c in cases),retainedAll12CrossContextsExactVisibleRGBPixels=sum(p['exactVisibleRGBPixels']for p in prior)+sum(c['exactVisibleRGBPixels']for c in cases),"),
)
for before,after in changes:run_source=once(run_source,before,after)
classification='progress: four actual current missing cross Tomb whole scenes completed through native retirement+30. Both P1 held and P2 random-drop branches match independent bare timing and full enabled-audio captures. Complete original one-base CPU/DMA/shift/VRAM/palette/RGB/body/composite/cache/projection/ground/native compressed floor-shadow and erase gates passed, with all actual earned/branch/phase/raster and additional timing counterexamples. Prior observed and pressed cross scenes complete finite12context native cross Tomb rendering/audio coverage, not broader victims, independent stock choreography, all arenas or full-port acceptance. All five original goal groups retained.'
start=run_source.index("  thisGoalTurnClassification='");end=run_source.index("',\n",start)+2
run_source=run_source[:start]+'  thisGoalTurnClassification='+repr(classification)+','+run_source[end:]
next_work='Do not rerun completed mirror or12cross Tomb state/audio/scene matrices for status. Continue broader native Pit/Tomb stock victims, source audio priority/RNG choice and independent stock choreography, full move/arena/CPU/repeated/KO/overlap and other finisher/victim/morph/secret/cinematic integration. Retain all actual natural campaigns/own endings and the complete original five-group goal. Final combined selection/ladder/names/audio regression, dependency-aware obsolete-folder cleanup and refreshed release ZIP remain. Never regenerate permanently retired builds/raw history.'
start=run_source.index("  next='");end=run_source.index("')",start)+1
run_source=run_source[:start]+'  next='+repr(next_work)+run_source[end:]
run_scope=dict(vars(original),__file__=__file__,__doc__=__doc__,runtime=runtime,OUT=OUT,
 INITIAL_IDENTITIES=INITIAL_IDENTITIES,storage=storage)
exec(compile(run_source,__file__+'::whole5850_missing_cross_full_scene_matrix','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 report=run();OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n')
 digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
  'Whole original scope additive journal losslessly compacted')
 print(json.dumps({k:v for k,v in report.items()if k not in ('remaining','newInputHashes','cases')},indent=2),flush=True)
