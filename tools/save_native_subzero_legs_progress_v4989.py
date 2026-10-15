"""Additive entire-scope checkpoint: stock shatter counterexample, paired PCM, staged semantic legs."""
import json,subprocess
from pathlib import Path
import native_subzero_body_context_v4932 as native

ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v4960_native_subzero_body_shatter_progress/progress.json'
OUT=ROOT/'audit_v4990_native_subzero_legs_progress'

def main():
 need(not OUT.exists(),'Fresh additive full-scope journal')
 parent=json.loads(PARENT.read_text());need(parent['goalStatus']=='active'and len(parent['remaining'])==5,'All original groups preserved')
 paths=[ROOT/'audit_v4982_native_subzero_reference_pcm_checked/report.json',
        ROOT/'asset_v4984_native_subzero_legs/report.json',ROOT/'audit_v4988_native_subzero_legs_source_checked/report.json']
 pcm,asset,stage=[json.loads(p.read_text())for p in paths]
 need(all(r['passed']for r in(pcm,asset,stage))and pcm['actualPairedPCMContexts']==3
      and len(pcm['alteredRecordFaultsRejected'])==15 and not pcm['fullPortAcceptance'],'Actual finite paired PCM/DMA evidence only')
 need(len(stage['sourceNegativeFaults'])==5 and len(stage['dataNegativeFaults'])==9
      and not stage['compiledFixAccepted']and not stage['runtimeAccepted']and not stage['artAccepted'],
      'New semantic art data/source staging, not unearned native acceptance')
 pins={}
 def pin(p,wanted=None):
  p=Path(p).resolve();h=sha(p);need(wanted is None or wanted==h,'Current immutable source/evidence hash')
  need(str(p)not in pins or pins[str(p)]==h,'Consistent actual input');pins[str(p)]=h
 for p in(PARENT,Path(__file__),Path(native.__file__),*paths):pin(p)
 for report in(pcm,asset,stage):
  for p,h in report['inputHashes'].items():pin(p,h)
 stock=[]
 for fighter in('kitana','liu_kang'):
  folder=ROOT/f'audit_v4963_subzero_{fighter}_p1_samples_reference'
  report_path=ROOT/f'audit_v4964_subzero_{fighter}_p1_samples_reference_observed/report.json'
  report=json.loads(report_path.read_text());meta=json.loads((folder/'result.json').read_text())
  need(report['passed']and report['nativeExit']==0 and not report['fullPortAcceptance'],'Actual physical-input stock terminal reference')
  for p in[report_path,*[p for p in folder.rglob('*')if p.is_file()]]:pin(p)
  for p,h in meta['inputHashes'].items():pin(p,h)
  stock.append(dict(fighter=fighter,side=1,report=str(report_path),nativeExit=0,fullPortAcceptance=False))
 failed=[]
 for fighter in('kitana','kano','sonya'):
  p=ROOT/f'audit_v4974_subzero_{fighter}_p1_nosamples_reference_observed/report.json'
  report=json.loads(p.read_text());need(not report['passed']and 'prior'in report['error'],'Actual preboot observer failure retained')
  pin(p);failed.append(dict(report=str(p),passed=False,scope='Undefined source-pin variable prior, before native boot'))
 for name in('run_native_subzero_reference_pcm_v4962.py','run_native_subzero_dma_pcm_v4966.py',
              'run_native_subzero_dma_pcm_detail_v4969.py','run_native_subzero_dma_pcm_detail_v4972.py',
              'run_native_subzero_dma_pcm_detail_v4975.py','verify_native_subzero_reference_pcm_v4979.py',
              'verify_native_subzero_reference_pcm_v4981.py','build_native_subzero_legs_v4983.py',
              'qualify_native_subzero_legs_v4987.py'):pin(ROOT/'tools'/name)
 for name in('mk2ks_native_subzero_reference_pcm_v4961.lua','mk2ks_native_subzero_dma_pcm_v4965.lua'):pin(ROOT/name)
 for folder in('art_native_subzero_legs_v4978','asset_v4984_native_subzero_legs','source_v4985_native_subzero_legs'):
  for p in(ROOT/folder).rglob('*'):
   if p.is_file():pin(p)
 public={
  'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
  'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
  'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
  'mame-mkp/src/mame/midway/midtunit_v.cpp':'8912181C8D7560BFD4974CECFEADD0532A9588A60D8D3FC399D58433EDB37611',
  'mk2/mk2-maincpu.bin':'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'}
 for p,h in public.items():pin(ROOT/p,h)
 native.expected()
 need(all(sha(p)==h for p,h in pins.items()),'Every current exact input still unchanged')
 result=dict(schema=1,baseFullScopeCheckpoint=parent['baseFullScopeCheckpoint'],
  parentAdditiveJournals=parent['parentAdditiveJournals']+[str(PARENT)],remaining=parent['remaining'],
  mergeRule='Additive to4557 and all parents. Stock-reference, finite PCM/DMA and semantic legs staging add evidence only. No original requirement is removed or narrowed.',
  goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
  previousGoalTurnClassification='progress: four real true17/18 native deep-freeze/shatter instances, natural subsequent CPU matches and independent finite checks (4960).',
  thisGoalTurnClassification='progress: actual stock Kitana/Liu controls, six paired samples-on/off native captures, entire actual mixed PCM update equality and transparency DMA source binding independently verified. Native zoom disproves an opaque/black-alpha band: rectangular partition leaves floating hands and a flat cutline. Built-in transparent semantic legs-only master inspected/saved, encoded into original six-bit palette, staged data-only native initializer and independent14-fault qualification. No new native build/public changes; anchors/GFX storage/runtime fidelity remain unaccepted.',
  newInputHashes=pins,actualStockReferences=stock,pairedPCMMatrix=str(paths[0]),semanticLegsEncoding=str(paths[1]),semanticLegsSourceQualification=str(paths[2]),
  actualPairedPCMContexts=3,pairedSubjects=['stock Kitana P1','true Kano17 P1','true Sonya18 P1'],
  actualPCMSampleRate=48000,actualPCMChannels=2,actualPCMUpdatesPerContext=354,actualCompletePCMBytesPerContext=1359360,
  allPCMCallbacksCadenceSeconds=.02,actualNonzeroUpdatesPerContext=353,pcmRecordNegativeFaultsRejected=15,
  audioScope='Entire deep-freeze through win+180 mixed stereo PCM byte-identical with samples on/off in these three actual P1 windows. No stem separation, all-four-slot, other-finisher/stage/victim or full audio acceptance inferred.',
  actualArtCounterexample=pcm['actualArtCounterexample'],
  correctedSourceUnderstanding=dict(zeroPixels='Actual native E002 commands skip zero pixels; do not change compression to fix a semantic crop.',
    stockPartSemantics='Original stock whole body and retained legs overlap and have shaped ice waist edges, unlike the prior fixed48% vertical crop. Current frozen whole body is retained unchanged; only post-shatter17/18 legs data are staged separately.',
    femaleVocal='Original source FFA122A0 female predicate is already redirected through FFFF0200 by initialized port; Sonya18 extension is present. Original unpatched ROM disassembly alone cannot establish her runtime vocal branch. Actual per-subject PCM differs, but gender branch/delivery/full fidelity remain unqualified.'),
  newBuiltInProjectAsset=str(ROOT/'art_native_subzero_legs_v4978/kano-sonya-frozen-legs.png'),
  finalBuiltInPrompt=str(ROOT/'art_native_subzero_legs_v4978/generation-prompts.json'),
  masterSHA256='D9E7CA72B91479803E84E15E6C7CE48F2CAE9906F1ABF548DE3CC7BB86B1E0C3',
  stagedSourceSHA256=stage['stagedSourceSHA256'],stagedPayloadSHA256=stage['payloadSHA256'],stagedGuestSHA256=stage['expectedGuestSHA256'],
  stagedGuestChangedBytes=92,additionalOwnGFXBytes=7032,
  sourceNegativeFaultsRejected=5,dataNegativeFaultsRejected=9,
  originalWholeBodiesStockLegRowsNativeTasksAudioAndCleanupUnchanged=True,
  compiledCandidateStill=native.NAME,executableSHA256=native.EXE_SHA,initializedGuestSHA256=native.GUEST_SHA,
  newLegsCompiled=False,newLegsActualGFXStorageGuardObserved=False,newLegsNativeAnchorAccepted=False,newLegsRuntimeAccepted=False,
  fullShatterArtAndAudioAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,
  normalHealthFreezeAccepted=False,nativeFloorShadowCoverageAccepted=False,
  preservedPrebootFailures=failed,preservedSourceCorrections=[
   '4969 source-export expansion assertion failed before any boot; executed source preserved.',
   '4972 source-pin prior variable was undefined; three failed preboot reports preserved. Fresh4975 produced the actual qualified4976/4977 native observations.',
   '4979 missing space else2 is an actual parse error, confirmed with ast.parse. Fresh4981 preserves failed source and independently qualifies4982; no evidence inferred from failed verifier.'],
  publicCMDExecutableZIPAndHistoricalInstalledEXEUnchanged=True,dirtyCheckoutUnchanged=True,
  newBuildsThisContinuation=0,newPayloadCopiesThisContinuation=1,rawGuestGFXRGBPCMOrWAVFilesWritten=0,
  newDeletionsThisContinuation=0,cleanupAccounting='Prior32.49GiB reclamation retained. One reused4926 native executable; no new build folders. Actual media/guest/GFX/PCM buffers stayed RAM-only; small logs/digest proofs compressed. One generated project PNG and one compressed2MiB native payload are required new implementation inputs, not duplicate build trees.',
  nextAction='One isolated semantic-legs candidate build with preservation/restoration guards, actual freeGFX guard/wholeguest/dedicatedGFX comparisons, real human shatter all four true17/18 slots and direct stock-relative RGB/grounding/cleanup/PCM inspection. Continue all five original groups, including ordinary freeze, move phases/floor shadows, broader CPU/repeated/KO/overlap, Pit/Tomb/victim audio, every other finisher/morph/secret/cinematic, genuine Kintaro/Shao campaign clears/own endings/attract, combined selection/ladder/names/audio and dependency-aware cleanup/finalZIP. No public promotion until full gates pass.')
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress full-scope journal')
 (OUT/'progress.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(journal=str(OUT/'progress.json'),pins=len(pins),pairedPCMContexts=3,stagedLegsNativeCompiled=False,
                       remainingGroups=len(result['remaining']),fullPortAcceptance=False,goalStatus='active'),indent=2),flush=True)

if __name__=='__main__':main()
