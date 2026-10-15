"""Current Babality and four sampled arena gates; full official integration open."""
import json,hashlib,subprocess
from pathlib import Path
import verify_native_ground_throw_source_v1598 as source
import verify_native_stage_performer_v807 as stage
import run_current_stage_matrix_v1713 as matrix
ROOT=source.ROOT;OUT=ROOT/'audit_v1725_current_babality_arena_checkpoint'
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb')as stream:
  for b in iter(lambda:stream.read(1048576),b''):h.update(b)
 return h.hexdigest().upper()
if __name__=='__main__':
 assert not OUT.exists();pins={}
 def pin(p,wanted=None):
  p=Path(p);key=str(p.resolve())
  if key not in pins:pins[key]=sha(p)
  assert wanted is None or pins[key]==wanted.upper(),'Changed evidence '+key
 priorpath=ROOT/'audit_v1701_current_primary_finisher_checkpoint/checkpoint.json';pin(priorpath)
 prior=json.loads(priorpath.read_text());assert prior['goalStatus']=='active'
 for p,h in prior['inputHashes'].items():pin(p,h)
 accepted={};arenas={}
 names=['audit_v1711_current_babality_checked','audit_v1702_current_early_native_counter_campaign_checked','audit_v1718_scaled_raster_units_checked',
  'audit_v1638_current_sonya_p1_arena_checked','audit_v1645_current_kano_p2_arena_checked','audit_v1655_current_sonya_p2_arena_checked',
  'audit_v1717_current_kano_p1_scaled_early_native_counter_arena_checked']
 for name in names:
  path=ROOT/name/'report.json';data=json.loads(path.read_text());assert data['passed'];pin(path)
  for p,h in data['inputHashes'].items():pin(p,h)
  accepted[name]=dict(reportSHA=pins[str(path.resolve())],scope=data.get('scope'),fullPortAcceptance=False)
  if 'allNineRegularArenasSampled'in data:
   assert data['allNineRegularArenasSampled']and data['actualArenaIDs']==list(range(9))
   arenas[data['fighter']+'_p'+str(data['human_slot'])]=dict(exactScanouts=data['exactScanouts'],nativeShadowCopies=data['nativeShadowCopies'],
    fullOwnedPaletteChecks=data['fullOwnedPaletteChecks'],culls=len(data.get('sourceBoundOriginalKintaroLaunchCulls',[])))
 assert set(arenas)=={'kano_p1','kano_p2','sonya_p1','sonya_p2'}
 failed=['audit_v1704_current_kano_p1_early_native_counter_arena_checked','audit_v1715_current_stage_checked']
 for name in failed:
  path=ROOT/name/'report.json';pin(path);assert not json.loads(path.read_text())['passed']
 stage_results={}
 for fighter,side,label,arena,command in matrix.SPECS:
  folder=ROOT/f'audit_v1714_{fighter}_{label}_p{side}'
  for f in ('result.json','inputs_before.json','run.log'):pin(folder/f)
  meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));assert meta['exit_code']==0
  for p,h in meta['input_hashes'].items():pin(p,h)
  try:result=stage.check_log((folder/'run.log').read_text(encoding='utf-8-sig'),fighter,side,arena,command)
  except Exception as error:result=dict(passed=False,error=repr(error))
  stage_results[folder.name]=result
 assert sum(r['passed']for r in stage_results.values())==19
 diagnostic=ROOT/'audit_v1721_sonya_tomb_p2_y_provenance'
 for f in ('result.json','inputs_before.json','run.log'):pin(diagnostic/f)
 meta=json.loads((diagnostic/'result.json').read_text(encoding='utf-8-sig'));assert meta['exit_code']==0
 for p,h in meta['input_hashes'].items():pin(p,h)
 log=(diagnostic/'run.log').read_text(encoding='utf-8-sig')
 original_rows=lambda s:'\n'.join(x for x in s.splitlines()if x.startswith('MK2_STAGE_')and not x.startswith('MK2_STAGE_PROVENANCE_'))
 assert original_rows(log)==original_rows((ROOT/'audit_v1714_sonya_tomb_p2/run.log').read_text(encoding='utf-8-sig'))
 case='audit_v1724_sonya_tomb_p2_branch_provenance';folder=ROOT/case;terminal=(folder/'result.json').exists()
 query="Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'mkport_candidate.exe' -and $_.CommandLine -match 'audit_v1724_sonya_tomb_p2_branch_provenance'} | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 answer=subprocess.run([PWSH,'-NoProfile','-Command',query],capture_output=True,text=True,check=True)
 live=json.loads(answer.stdout)if answer.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 assert live or terminal,'Exact running process or terminal evidence required'
 pin(folder/'inputs_before.json')
 for p,h in json.loads((folder/'inputs_before.json').read_text(encoding='utf-8-sig')).items():pin(p,h)
 if terminal:pin(folder/'result.json');pin(folder/'run.log')
 for name,h in {
  'diagnostic_v1597_native_ground_throw/mkport_candidate.exe':'9D2E9849CA3A98AA06018DB2EF3EE65397A5C9EC95C466CFD999C9091237B695',
  'PLAY_CURRENT_V1597_TEST_BUILD.cmd':'85962962ADA430B706B4052A28A8809D1E53EF3D98FE3C44831D709898375DAB',
  'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
  'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
  'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
  'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}.items():pin(ROOT/name,h)
 pin(__file__)
 report=dict(goalStatus='active',objective=prior['objective'],previousGoalTurnClassification='no progress: status report only; terminal state revalidated and outstanding checks executed this turn',
  thisGoalTurnClassification='progress: current Babality and fourth sampled native arena gate accepted, scaling model source-bound and tested; current stage exception isolated and repeat motion provenance captured',
  currentCandidate=source.NAME,currentCMD=prior['currentCMD'],gameSourceAndPlayableBytesChangedThisTurn=False,
  currentHumanBabalityPerformersVictimsAndRejectionAccepted=True,allFourCharacterSlotNineArenaSampledGatesPassed=True,
  arenaGates=arenas,allMovePhaseFloorAccepted=False,oldFailedArenaCapturesStillUnaccepted=True,
  currentStageOriginalStatePredicates=stage_results,currentFullStageMatrixAccepted=False,
  tombException='Sonya P2 vs Kano Tomb: native ceiling hold/drop variant repeats with byte-exact original input/state chronology. Slow fall set by original FF8EB240; conditional branch provenance capture pending independent analysis. No gameplay patch or predicate waiver.',
  pendingCase=dict(case=case,session=95239,confirmedLiveProcesses=live,terminalResultPresent=terminal,accepted=False),
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,allFinishersVictimsMorphsSecretsCinematicsAccepted=False,
  newReleaseZIPCreated=False,cleanupAllocatedBytesReclaimed=prior['cleanupAllocatedBytesReclaimed'],deletedFilesThisTurn=0,allOldBuildFoldersRemoved=False,
  acceptedReports=accepted,failedEvidencePreserved=True,oldAcceptancePredicatesChanged=False,
  remaining=['Source-bound native Tomb drop/hold branch variants and complete stage scene art/audio',
   'Full move-phase art, grounding, native floor shadows and cleanup; broader CPU, repeated, KO and overlap cases',
   'All other finishers, victims, morphs, secrets and cinematics',
   'Actual natural boss/campaign clear, own endings and return to attract',
   'Final combined selection/ladder/names/audio regression, obsolete-folder cleanup and release ZIP'],inputHashes=pins,fullPortAcceptance=False)
 OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(saved=str(OUT/'checkpoint.json'),pins=len(pins),arenas=arenas,stageCasesMeetingOriginalStatePredicates=19,pending=report['pendingCase'],goalStatus='active'),indent=2))
