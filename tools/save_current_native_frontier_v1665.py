"""Preserve accepted broad checks and the still-unaccepted native boss cull."""
import hashlib,json,subprocess
from pathlib import Path
import verify_native_ground_throw_source_v1598 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1665_current_native_frontier_checkpoint'
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest().upper()
def freeze():
 pins={}
 def pin(p,wanted=None):
  p=Path(p);key=str(p.resolve())
  if key not in pins:pins[key]=sha(p)
  assert wanted is None or wanted==pins[key],'Changed actual input '+key
 priorpath=ROOT/'audit_v1653_wide_current_regression_checkpoint/checkpoint.json'
 pin(priorpath,'5156FFCAF43C345F8FE745D36691D8D9E8C1CC72EEAA27B7D44A804337967D21')
 prior=json.loads(priorpath.read_text())
 # The prior checkpoint remains an immutable hash-chain input. New actual
 # report inputs are independently rehashed below, not merely trusted green.
 accepted={};arenas={}
 for name in('audit_v1654_current_sonya_p2_campaign_checked','audit_v1655_current_sonya_p2_arena_checked','audit_v1656_current_kano_p1_campaign_checked'):
  p=ROOT/name/'report.json';r=json.loads(p.read_text());assert r['passed'];pin(p)
  if 'candidate'in r:assert r['candidate']==source.NAME
  for path,h in r['inputHashes'].items():pin(path,h)
  accepted[name]=dict(reportSHA=pins[str(p.resolve())],scope=r.get('scope'),fullPortAcceptance=False)
 for name in('audit_v1638_current_sonya_p1_arena_checked','audit_v1645_current_kano_p2_arena_checked','audit_v1655_current_sonya_p2_arena_checked'):
  p=ROOT/name/'report.json';r=json.loads(p.read_text());assert r['passed'] and r['candidate']==source.NAME and r['allNineRegularArenasSampled'];pin(p)
  arenas[r['fighter']+'_p'+str(r['human_slot'])]=dict(arenas=r['actualArenaIDs'],exactFullScanouts=r['exactScanouts'],nativeShadowCopies=r['nativeShadowCopies'])
 failed=ROOT/'audit_v1657_current_kano_p1_arena_checked/report.json';r=json.loads(failed.read_text());assert not r['passed'];pin(failed)
 diagnostic=ROOT/'audit_v1661_current_kano_p1_visibility_diagnostic/report.json';d=json.loads(diagnostic.read_text());pin(diagnostic)
 assert d['diagnosticCompleted'] and d['exactSavedFrames']==285 and len(d['visibilityFailures'])==7
 for path,h in d['inputHashes'].items():pin(path,h)
 for q in d['visibilityFailures']:
  assert q['body']['pixels']==0 and q['wholeVRAMMismatches']==q['displayedMismatches']==q['shadowMismatches']==0
  assert q['actualOwnShadowComponents']
  for p in q['actualOwnShadowComponents']:
   assert p['id']==17 and p['owner']==p['actor'] and p['y']<p['floor']
  pin(ROOT/'audit_v1642_current_kano_p1_campaign/snap'/q['file'])
 for module in('tools/inspect_current_native_visibility_v1660.py','tools/run_native_counter_cull_v1663.ps1','mk2ks_native_counter_cull_v1663.lua'):
  pin(ROOT/module)
 wrapper=(ROOT/'mk2ks_native_counter_cull_v1663.lua').read_text()
 assert wrapper.count("dofile('mk2ks_natural_campaign_floor_v1566.lua')")==1
 assert ':write_'not in wrapper and 'write_u'not in wrapper and '.value ='not in wrapper and 'loadstate'not in wrapper
 case='audit_v1664_current_kano_p1_native_counter';folder=ROOT/case
 pin(folder/'input_hashes_before.json')
 for path,h in json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig')).items():pin(path,h)
 query="Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'mkport_candidate.exe' -and $_.ExecutablePath -like '*\\mk2port\\diagnostic_v1597_native_ground_throw\\*'} | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 response=subprocess.run([PWSH,'-NoProfile','-Command',query],capture_output=True,text=True,check=True)
 live=json.loads(response.stdout)if response.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 running=[p for p in live if case in p['CommandLine']]
 terminal=(folder/'result.json').exists()
 assert running or terminal,'Re-poll existing handle; no authoritative terminal/live state'
 pin(ROOT/'PLAY_CURRENT_V1597_TEST_BUILD.cmd','85962962ADA430B706B4052A28A8809D1E53EF3D98FE3C44831D709898375DAB')
 pin(ROOT/source.NAME/'mkport_candidate.exe','9D2E9849CA3A98AA06018DB2EF3EE65397A5C9EC95C466CFD999C9091237B695')
 for p,h in {'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34','mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85','mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}.items():pin(ROOT/p,h)
 pin(__file__)
 return dict(goalStatus='active',objective=prior['objective'],thisGoalTurnClassification='progress: broad current matrices, three current nine-arena geometry/raster proofs, source-bound P2 audio interruption and lossless cleanup; native boss cull remains unaccepted',
  currentCandidate=source.NAME,currentCMD='PLAY_CURRENT_V1597_TEST_BUILD.cmd',gameSourceAndPlayableBytesChangedThisTurn=False,
  current52SpecialCasesAccepted=True,current56SelectableVictimThrowsAccepted=True,currentP2SquareJumpKickAudioInterruptionAccepted=True,
  currentNineArenaAccepted=arenas,allNineBothCharactersBothSlots=False,
  currentKanoP1ExactSavedScanoutDiagnosticFrames=285,currentKanoP1UnacceptedOffTopFrames=[q['frame']for q in d['visibilityFailures']],
  currentKanoP1ArenaGatePassed=False,confirmedGameRenderingDefect=False,bossCullCauseStillNeedsNativeProvenance=True,
  bossCullObservation='Actual owned cached body parts lie above viewport; original uppercut-only proof lacks preceding rendered samples. Do not waive visibility or claim a native boss counter without source/trajectory evidence.',
  actualFullLadderClearAccepted=False,actualEndingsAccepted=False,allMovePhaseFloorAccepted=False,
  cleanupAllocatedBytesReclaimed=prior['cleanupAllocatedBytesReclaimed'],immutableBuildExecutablesCompressed=82,deletedFiles=0,allOldBuildFoldersRemoved=False,
  acceptedReports=accepted,failedReport=str(failed),visibilityDiagnostic=str(diagnostic),
  pendingCapture=dict(case=case,session=47808,confirmedLiveProcesses=running,terminalResultPresent=terminal,accepted=False),
  oldCapturesAndAcceptancePredicatesChanged=False,newReleaseZIPCreated=False,inputHashes=pins,fullPortAcceptance=False,
  remaining=['Complete actual native Kintaro descriptor/hurt/cull diagnosis and fix any demonstrated game defect',
   'Full move-phase art, grounding and shadow choreography; broader CPU, repeated, KO and overlap cases',
   'Full boss/campaign clear, endings, finishers, victims, morphs, secrets and cinematics',
   'Remaining obsolete-folder cleanup and final release ZIP'])
if __name__=='__main__':
 assert not OUT.exists(),'Preserve prior checkpoints'
 r=freeze();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(saved=str(OUT/'checkpoint.json'),pins=len(r['inputHashes']),currentCandidate=r['currentCandidate'],pending=r['pendingCapture'],goalStatus='active',fullPortAcceptance=False),indent=2))
