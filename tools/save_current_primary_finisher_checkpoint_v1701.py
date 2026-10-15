"""Current primary mirrors proven; boss clipping frontier remains explicitly open."""
import hashlib,json,subprocess
from pathlib import Path
import verify_native_ground_throw_source_v1598 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1701_current_primary_finisher_checkpoint'
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb')as stream:
  for block in iter(lambda:stream.read(1048576),b''):h.update(block)
 return h.hexdigest().upper()
if __name__=='__main__':
 assert not OUT.exists()
 pins={}
 def pin(path,wanted=None):
  path=Path(path);key=str(path.resolve())
  if key not in pins:pins[key]=sha(path)
  assert wanted is None or pins[key]==wanted,'Changed accepted evidence '+key
 priorpath=ROOT/'audit_v1665_current_native_frontier_checkpoint/checkpoint.json';pin(priorpath)
 prior=json.loads(priorpath.read_text());assert prior['goalStatus']=='active'
 accepted={};renders={}
 names=['audit_v1674_current_natural_mirror_finish_checked','audit_v1681_current_mirror_finish_negative_checks',
  'audit_v1678_current_native_counter_campaign_checked','audit_v1693_native_kintaro_causal_probe_checked','audit_v1695_native_kintaro_negative_checked']
 names += [f'audit_v1677_{f}_mirror_finish_p{s}_render_checked'for f in('kano','sonya')for s in(1,2)]
 for name in names:
  path=ROOT/name/'report.json';data=json.loads(path.read_text());assert data['passed'];pin(path)
  for p,h in data['inputHashes'].items():pin(p,h)
  accepted[name]=dict(reportSHA=pins[str(path.resolve())],scope=data.get('scope'),fullPortAcceptance=False)
  if 'naturalMirrorSampledRenderAccepted'in data:
   assert data['naturalMirrorSampledRenderAccepted']
   renders[data['fighter']+'_p'+str(data['winner'])]=dict(exactReplayedFrames=data['replayed']['frames'],
    heldScanoutSamples=len(data['heldScanout']),nativeTeardown=data['nativeTeardown'],
    postRetirementReplayedSamples=data['postTransitionReplayedSamples'])
 for name in ('audit_v1668_current_mirror_finish_dispatch','audit_v1680_current_kano_p1_native_counter_arena_checked',
  'audit_v1684_native_kintaro_causal_probe_checked','audit_v1686_native_kintaro_causal_probe_checked',
  'audit_v1688_native_kintaro_causal_probe_checked','audit_v1691_native_kintaro_causal_probe_checked',
  'audit_v1694_current_kano_p1_native_counter_arena_checked',
  'audit_v1696_native_counter_cull_predicate_diagnostic','audit_v1697_native_counter_cull_predicate_diagnostic'):
  pin(ROOT/name/'report.json')
 for name in ('audit_v1673_current_mirror_finish_dispatch','audit_v1676_current_mirror_finish_dispatch'):
  path=ROOT/name/'report.json';data=json.loads(path.read_text());assert data['allRunnerExitsZero'];pin(path)
 case='audit_v1700_current_kano_p1_early_native_counter';folder=ROOT/case
 pin(folder/'input_hashes_before.json')
 for p,h in json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig')).items():pin(p,h)
 wrapper=ROOT/'mk2ks_native_counter_cull_v1699.lua';driver=ROOT/'mk2ks_natural_campaign_floor_v1698.lua'
 pin(wrapper);pin(driver);pin(ROOT/'tools/run_native_counter_cull_v1699.ps1')
 text=driver.read_text()
 restored=text.replace('local floor_origin,floor_pending=nil,nil\n-- Earlier read-only observation for the actual native Kintaro stage only.\n-- Gameplay controls, schedules, health, CPU and all other arena windows stay unchanged.\nlocal function floor_min_age()return p:read_u16(0x01061b30)==15 and 0 or 208 end','local floor_origin,floor_pending=nil,nil')
 restored=restored.replace('frame-floor_origin<floor_min_age()','frame-floor_origin<208').replace('age<floor_min_age()','age<208').replace('frame-floor_origin>=(floor_min_age()==0 and 8 or 216)','frame-floor_origin>=216')
 assert restored==(ROOT/'mk2ks_natural_campaign_floor_v1566.lua').read_text()
 query="Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'mkport_candidate.exe' -and $_.CommandLine -match 'audit_v1700_current_kano_p1_early_native_counter'} | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 answer=subprocess.run([PWSH,'-NoProfile','-Command',query],capture_output=True,text=True,check=True)
 live=json.loads(answer.stdout)if answer.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 terminal=(folder/'result.json').exists();assert live or terminal,'Re-poll exact existing handle, never restart from timeout'
 for name,h in {
  'diagnostic_v1597_native_ground_throw/mkport_candidate.exe':'9D2E9849CA3A98AA06018DB2EF3EE65397A5C9EC95C466CFD999C9091237B695',
  'PLAY_CURRENT_V1597_TEST_BUILD.cmd':'85962962ADA430B706B4052A28A8809D1E53EF3D98FE3C44831D709898375DAB',
  'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
  'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
  'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
  'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}.items():pin(ROOT/name,h)
 pin(__file__)
 report=dict(goalStatus='active',objective=prior['objective'],previousGoalTurnClassification='verified wait: exact existing PID98720 confirmed live during status inspection',
  thisGoalTurnClassification='progress: current primary mirror state/palette/render/retirement acceptance in both slots, source-bound native boss flights, fresh earlier boss capture',
  currentCandidate=source.NAME,currentCMD=prior['currentCMD'],gameSourceAndPlayableBytesChangedThisTurn=False,
  allFourPrimaryMirrorFinisherStatePaletteAccepted=True,allFourPrimaryMirrorSampledRenderAndRetirementAccepted=True,
  currentPrimaryMirrorRendering=renders,twoActualNativeKintaroLaunchesAndNormalRecoveryAccepted=True,
  allCurrentKanoP1ArenaCullsAccepted=False,currentKanoP1ArenaGatePassed=False,
  bossCullCause='Original Kintaro 40-point hit selects native FF8D8330: -19 Y speed, 0.5 gravity; complete launch/landing/recovery accepted. First five saved culls still lack a retained pre-hit native draw; fresh earlier observation required.',
  pendingCapture=dict(case=case,session=97338,confirmedLiveProcesses=live,terminalResultPresent=terminal,accepted=False),
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,allMovePhaseFloorAccepted=False,
  allFinishersVictimsMorphsSecretsCinematicsAccepted=False,newReleaseZIPCreated=False,
  cleanupAllocatedBytesReclaimed=prior['cleanupAllocatedBytesReclaimed'],deletedFilesThisTurn=0,allOldBuildFoldersRemoved=False,
  acceptedReports=accepted,failedSourcesReportsAndActualCapturesPreserved=True,oldAcceptancePredicatesChanged=False,
  remaining=['Source-bound pre-hit native drawing and seven Kintaro culls from the fresh earlier capture',
   'Full move-phase art, grounding, native floor shadows and cleanup; broader CPU, repeated, KO and overlap cases',
   'All other finishers, victims, morphs, secrets and cinematics; primary mirror proof is not all-character proof',
   'Actual natural boss/campaign clear, own endings and return to attract',
   'Remaining obsolete-folder cleanup and final release ZIP'],inputHashes=pins,fullPortAcceptance=False)
 OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(saved=str(OUT/'checkpoint.json'),pins=len(pins),renders=renders,pending=report['pendingCapture'],goalStatus='active',fullPortAcceptance=False),indent=2))
