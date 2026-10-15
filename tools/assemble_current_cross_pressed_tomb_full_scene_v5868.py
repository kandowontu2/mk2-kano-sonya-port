"""Full actual cross pressed Tomb scene matrix, retaining the original full goal.

Entire5831 scene acceptance and real negative gates remain. Only current cross
IDs/palettes, independent actual audio reference and process identities change;
the complete seven physical-input faults are also checked for each scene.
"""
import datetime,gzip,hashlib,inspect,json,re,subprocess
from pathlib import Path
import assemble_current_pressed_tomb_full_scene_v5831 as original
import run_current_cross_pressed_tomb_render_ram_v5865 as runtime
from record_current_cross_tomb_audio_v5844 import allocated
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
OUT=ROOT/'audit_v5869_current_cross_pressed_tomb_full_scene_matrix_progress'
INITIAL_IDENTITIES={
 'kano1':dict(hostPID=135220,hostCreated='2026-10-08T04:12:19.078227-04:00',pid=145312,created='2026-10-08T04:12:31.147189-04:00'),
 'kano2':dict(hostPID=19952,hostCreated='2026-10-08T04:12:19.088594-04:00',pid=152924,created='2026-10-08T04:12:31.154111-04:00'),
 'sonya1':dict(hostPID=147484,hostCreated='2026-10-08T04:12:19.069008-04:00',pid=150668,created='2026-10-08T04:12:31.139523-04:00'),
 'sonya2':dict(hostPID=130012,hostCreated='2026-10-08T04:12:19.083972-04:00',pid=144060,created='2026-10-08T04:12:31.123245-04:00'),
}
records=original.records
fault_source=inspect.getsource(original.actual_pressed_source_faults)
fault_scope=dict(vars(original),runtime=runtime)
exec(compile(fault_source,__file__+'::whole5831_actual_owned_source_writer_faults','exec'),fault_scope)
actual_pressed_source_faults=fault_scope['actual_pressed_source_faults']

def once(code,before,after):
 need(code.count(before)==1,'Exactly declared full scene matrix adaptation: '+before)
 return code.replace(before,after,1)

run_source=inspect.getsource(original.run)
changes=(
 ('audit_v5826_current_requested_cleanup_progress/progress.json','audit_v5863_current_cross_pressed_tomb_enabled_audio_progress/progress.json'),
 ("parent['actualCurrentHeldAndRandomMirrorFullScenesRetained']", "parent['allPriorMirrorHeldPressedRandomAndObservedCrossScenesRetained']and parent['actualCurrentBothCharactersBothSlotsCrossPressedTombEnabledWinnerMixAccepted']"),
 ('audit_v5796_current_pressed_tomb_enabled_winner_mix_checked/report.json','audit_v5861_current_cross_pressed_tomb_enabled_audio_checked/report.json'),
 ('actualCurrentPressedMirrorNativeTombWholeRenderPaletteShadowEraseAccepted','actualCurrentCrossPressedNativeTombWholeRenderPaletteShadowEraseAccepted'),
 ("report['truePhysicalIDs']==[identity,identity]", "report['truePhysicalIDs']==[identity if s==side else 35-identity for s in(1,2)]"),
 ("need(branch==ref['sourceQualifiedNativeBranch']and", "need(branch==ref['sourceQualifiedNativeBranch']and branch['trueVictim']==35-identity and"),
 ("report['nativeMirrorPaletteSelectors']=={'1':[False],'2':[True]}", "report['nativeCrossPaletteSelectors']=={'1':[False],'2':[False]}"),
 ("nativeMirrorPaletteSelectors=report['nativeMirrorPaletteSelectors']", "nativeCrossPaletteSelectors=report['nativeCrossPaletteSelectors']"),
 ('mk2ks_current_pressed_tomb_display_ram_v5828.lua','mk2ks_current_cross_pressed_tomb_display_ram_v5864.lua'),
 ('run_current_pressed_tomb_render_ram_v5827.py','run_current_cross_pressed_tomb_render_ram_v5865.py'),
 ('source/mirror palette','source/cross palette'),
 ("'MK2_STAGE_SELECT ','MK2_STAGE_SELECT_ID ','MK2_STAGE_WINDOW ','MK2_STAGE_COMMAND ','MK2_STAGE_RESULT ')",
  "'MK2_STAGE_SELECT ','MK2_STAGE_SELECT_ID ','MK2_STAGE_WINDOW ','MK2_STAGE_COMMAND ','MK2_STAGE_RESULT ','MK2_STAGE_DROP_INPUT ','MK2_STAGE_DROP_RESULT ')"),
 ("  process=json.loads((folder/'process.json').read_text());processes.append(process)",
  "  process=json.loads((folder/'process.json').read_text());processes.append(process)\n  initial=INITIAL_IDENTITIES[fighter+str(side)]\n  need(process['pid']==initial['pid']and process['hostPID']==initial['hostPID']and\n   abs(process['startedUnix']-datetime.datetime.fromisoformat(initial['created']).timestamp())<.05,\n   'Exact native and host names, full commands and creation times independently inspected live')"),
 ("  need(len(source_faults)==6,'All actual owned pressed source/writer counterexamples rejected')",
  "  need(len(source_faults)==6 and report['actualPressedSourceWriterFaultsRejected']==source_faults,\n   'All actual owned pressed source/writer counterexamples rejected')\n  input_faults=runtime.audio_proof.input_faults(text,guest,fighter,side)\n  need(len(input_faults)==7 and report['actualPhysicalInputFaultsRejected']==input_faults and\n   len(report['actualEarnedFaultsRejected'])==12 and len(report['actualPressedPhaseFaultsRejected'])==4,\n   'Every complete earned/phase and actual physical input, callback, role and NOT operand fault retained')"),
 ('actualPressedSourceFaultsRejected=source_faults,actualRasterFaultsRejected=2',
  'actualPressedSourceFaultsRejected=source_faults,actualPhysicalInputFaultsRejected=input_faults,actualRasterFaultsRejected=2'),
 (" sealed=list(dict.fromkeys(p.resolve()for p in sealed));before={str(p):sha(p)for p in sealed}",
  " sealed=list(dict.fromkeys(p.resolve()for p in sealed));before={str(p):sha(p)for p in sealed}\n before_allocated=sum(allocated(p)for p in sealed)"),
 (" need(all(sha(p)==h for p,h in before.items()),'Every sealed full evidence/source byte unchanged')",
  " need(all(sha(p)==h for p,h in before.items()),'Every sealed full evidence/source byte unchanged')\n after_allocated=sum(allocated(p)for p in sealed)"),
 ('actualCurrentBothCharactersBothSlotsPressedMirrorTombFullSceneGroundShadowEraseAccepted=True',
  'actualCurrentBothCharactersBothSlotsCrossPressedTombFullSceneGroundShadowEraseAccepted=True,priorObservedCrossFullScenesAndAllMirrorBranchesRetained=True'),
 ('currentPressedMirrorFullSceneAccepted=True,broaderPitTombVictimsAccepted=False',
  'currentPressedCrossFullSceneAccepted=True,allCurrentCrossHeldPressedRandomFullScenesAccepted=False,broaderPitTombVictimsAccepted=False'),
 ('actualPressedSourceWriterFaultsRejected=24,actualRasterFaultsRejected=8',
  'actualPressedSourceWriterFaultsRejected=24,actualPhysicalInputFaultsRejected=28,actualRasterFaultsRejected=8'),
 ('consumedCaptureToolSessions=[67586,55245,78952,28597]',
  'consumedCaptureToolSessions=[20243,22783,98787,39934],initialLiveProcessIdentities=INITIAL_IDENTITIES'),
 ('sealedTextSourcesLosslesslyCompacted=len(sealed),',
  'sealedTextSourcesLosslesslyCompacted=len(sealed),sealedAllocatedBytesBefore=before_allocated,sealedAllocatedBytesAfter=after_allocated,sealedAllocatedBytesReclaimed=before_allocated-after_allocated,'),
)
for before,after in changes:run_source=once(run_source,before,after)
classification='progress: four actual current opposite-character physical both-Down Tomb full scenes completed. Whole one-base native CPU/DMA/shift/VRAM/palette/RGB, original body/composite/cache/projection/ground/compressed native floor-shadow and retirement+30 gates pass with genuine target faults. Full earned/PC/IO/owned ceiling-writer/269motion, all six source/writer and seven input/role faults per case pass and agree with independent actual enabled audio. Wider original five-group scope remains active.'
start=run_source.index("  thisGoalTurnClassification='")
end=run_source.index("',\n",start)+2
run_source=run_source[:start]+'  thisGoalTurnClassification='+repr(classification)+','+run_source[end:]
next_work='Do not rerun these completed four cross pressed or prior mirror/unpressed scenes for status. Continue missing cross held/random slots and broader native Pit/Tomb stock victims, exact source audio priority/RNG choice and independent stock choreography. Retain all original move/arena/CPU/repeated/KO/overlap, other finisher/victim/morph/secret/cinematic, natural campaign/endings and final combined selection/ladder/names/audio regression, dependency-aware cleanup and refreshed release ZIP. No regeneration of permanently retired raw recordings/builds.'
start=run_source.index("  next='")
end=run_source.index("')",start)+1
run_source=run_source[:start]+'  next='+repr(next_work)+run_source[end:]
run_scope=dict(vars(original),__file__=__file__,__doc__=__doc__,runtime=runtime,OUT=OUT,
 actual_pressed_source_faults=actual_pressed_source_faults,INITIAL_IDENTITIES=INITIAL_IDENTITIES,allocated=allocated)
exec(compile(run_source,__file__+'::whole5831_actual_cross_pressed_matrix','exec'),run_scope)
run=run_scope['run'];run.source=run_source

if __name__=='__main__':
 report=run();OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(report,indent=2)+'\n')
 digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
  'New full-scope actual evidence journal losslessly compacted')
 print(json.dumps({k:v for k,v in report.items()if k not in('remaining','newInputHashes','cases')},indent=2),flush=True)
