"""Freeze wide current regression, real interruption and lossless space savings."""
import ctypes,hashlib,json,subprocess,sys
from pathlib import Path
import verify_native_ground_throw_source_v1598 as source
ROOT=source.ROOT
OUT=ROOT/'audit_v1653_wide_current_regression_checkpoint'
PWSH=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb')as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest().upper()
def freeze():
 pins={};accepted={}
 def pin(p,wanted=None):
  p=Path(p);key=str(p.resolve())
  if key not in pins:pins[key]=sha(p)
  assert wanted is None or wanted==pins[key],'Changed authoritative input '+key
 priorpath=ROOT/'audit_v1618_native_ground_throw_checkpoint/checkpoint.json'
 pin(priorpath,'56EE4A30D499E3D9581768C19199A0E3BE380E5EFDD5046776B8666E07BA48CD')
 prior=json.loads(priorpath.read_text())
 for p,h in prior['inputHashes'].items():pin(p,h)
 for name in('audit_v1623_ground_throw_special_matrix_checked','audit_v1624_ground_throw_opponents_checked',
  'audit_v1637_current_sonya_p1_campaign_checked','audit_v1638_current_sonya_p1_arena_checked',
  'audit_v1644_current_kano_p2_campaign_checked','audit_v1645_current_kano_p2_arena_checked',
  'audit_v1652_p2_square_jumpkick_audio_checked'):
  p=ROOT/name/'report.json';r=json.loads(p.read_text());assert r['passed']
  if 'candidate'in r:assert r['candidate']==source.NAME
  pin(p)
  for path,h in r['inputHashes'].items():pin(path,h)
  accepted[name]=dict(reportSHA=pins[str(p.resolve())],scope=r.get('scope'),fullPortAcceptance=False)
 special=json.loads((ROOT/'audit_v1623_ground_throw_special_matrix_checked/report.json').read_text())
 throw=json.loads((ROOT/'audit_v1624_ground_throw_opponents_checked/report.json').read_text())
 assert special['current52CaseHumanStateMatrixAccepted'] and len(special['cases'])==52 and special['exactPriorActualFullScreensMatched']==156
 assert throw['all14SelectableVictimsInBothSlots'] and len(throw['cases'])==56
 audio=json.loads((ROOT/'audit_v1652_p2_square_jumpkick_audio_checked/report.json').read_text())
 assert audio['p2SquareActualIncomingHitAudioCleanupAccepted'] and audio['readOnlyObserverReplayExact']
 arenas={}
 for name in('audit_v1638_current_sonya_p1_arena_checked','audit_v1645_current_kano_p2_arena_checked'):
  r=json.loads((ROOT/name/'report.json').read_text());assert r['allNineRegularArenasSampled']
  arenas[r['fighter']+'_p'+str(r['human_slot'])]=dict(arenas=r['actualArenaIDs'],exactFullScanouts=r['exactScanouts'],nativeShadowCopies=r['nativeShadowCopies'],sourceBoundCoordinates=r['nativeCoordinatePublicationsChecked'])
 # These are actual allocated bytes, not logical EXE size or a noisy disk-free delta.
 kernel=ctypes.WinDLL('kernel32',use_last_error=True)
 allocation=kernel.GetCompressedFileSizeW
 allocation.argtypes=(ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32));allocation.restype=ctypes.c_uint32
 total_saved=0;compressed=0
 for name in('audit_v1631_immutable_build_compression_pilot','audit_v1632_immutable_old_build_compression'):
  folder=ROOT/name;p=folder/'report.json';r=json.loads(p.read_text(encoding='utf-8-sig'));assert r['passed'] and r['deletedFiles']==0
  records=r.get('files',[r])
  for row in records:
   pin(row['path'],row['shaBefore']);assert row['shaBefore']==row['shaAfter']
   high=ctypes.c_uint32();low=allocation(row['path'],ctypes.byref(high))
   assert low!=0xffffffff or not ctypes.get_last_error()
   allocated=(high.value<<32)+low;assert allocated==row['allocatedAfter']
   assert row['allocatedBefore']-allocated==row['reclaimedBytes']>=0
   total_saved+=row['reclaimedBytes'];compressed+=1
  for path,h in r.get('keptHashes',{}).items():pin(path,h)
  for path in folder.rglob('*'):
   if path.is_file():pin(path)
 assert total_saved==1457885184 and compressed==82
 for name in('audit_v1619_ground_throw_special_matrix_dispatch','audit_v1621_ground_throw_opponents_dispatch',
  'audit_v1628_square_early_uppercut_p2','audit_v1630_square_ready_uppercut_p2',
  'audit_v1634_square_dash_uppercut_p2','audit_v1635_square_later_dash_uppercut_p2',
  'audit_v1640_square_jax_uppercut_p2','audit_v1641_square_cage_uppercut_p2',
  'audit_v1647_square_jumpkick_interruption_p2'):
  for p in(ROOT/name).rglob('*'):
   if p.is_file():pin(p)
 for name in('run_ground_throw_special_matrix_v1619.py','run_ground_throw_opponents_v1621.py',
  'verify_ground_throw_special_matrix_v1623.py','verify_ground_throw_opponents_v1624.py',
  'run_sonya_launch_interruption_v1627.ps1','run_sonya_launch_interruption_v1629.ps1',
  'run_sonya_launch_interruption_v1633.ps1','run_sonya_launch_interruption_v1639.ps1',
  'run_sonya_launch_interruption_v1646.ps1','run_sonya_launch_interruption_v1648.ps1',
  'run_sonya_launch_interruption_v1650.ps1','verify_p2_square_jumpkick_audio_v1652.py',
  'compress_immutable_build_pilot_v1631.ps1','compress_immutable_old_builds_v1632.ps1'):
  pin(ROOT/'tools'/name)
 for name in('mk2ks_launch_interruption_v1627.lua','mk2ks_launch_interruption_v1629.lua',
  'mk2ks_launch_interruption_v1633.lua','mk2ks_launch_interruption_v1646.lua',
  'mk2ks_launch_interruption_v1648.lua','mk2ks_launch_interruption_v1650.lua'):
  pin(ROOT/name)
 # Confirm live handles against the actual running executable and exact output
 # directories. Never infer a verified wait from an unfinished log alone.
 query="Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'mkport_candidate.exe' -and $_.ExecutablePath -like '*\\mk2port\\diagnostic_v1597_native_ground_throw\\*'} | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
 proc=subprocess.run([PWSH,'-NoProfile','-Command',query],capture_output=True,text=True,check=True)
 live=json.loads(proc.stdout)if proc.stdout.strip()else[]
 if isinstance(live,dict):live=[live]
 pending=[]
 for name,session in(('audit_v1642_current_kano_p1_campaign',41111),('audit_v1643_current_sonya_p2_campaign',93979)):
  folder=ROOT/name;pin(folder/'input_hashes_before.json')
  before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
  for p,h in before.items():pin(p,h)
  running=[p['ProcessId']for p in live if name in p['CommandLine']]
  terminal=(folder/'result.json').exists()
  assert running or terminal,'No authoritative live or terminal state; re-poll same handle'
  pending.append(dict(case=name,session=session,confirmedLivePIDs=running,terminalResultPresent=terminal,accepted=False))
 pin(ROOT/'PLAY_CURRENT_V1597_TEST_BUILD.cmd')
 pin(ROOT/source.NAME/'mkport_candidate.exe','9D2E9849CA3A98AA06018DB2EF3EE65397A5C9EC95C466CFD999C9091237B695')
 pin(__file__)
 return dict(goalStatus='active',objective='Once again, the goal is clear: THey need to appear as a natural part of the game in all aspects.',
  previousStatusTurnClassification='no progress beyond status reporting; terminal captures revalidated and strict independent checkers executed this turn',
  thisGoalTurnClassification='progress: accepted 52 special cases, 56 selectable-victim throws, two current nine-arena rasters, actual P2 square incoming-hit audio stop and 1.36 GiB lossless cleanup',
  currentCandidate=source.NAME,currentCMD='PLAY_CURRENT_V1597_TEST_BUILD.cmd',currentGameSourceOrPayloadEditedThisTurn=False,
  current52SpecialCasesAccepted=True,current56SelectableVictimThrowsAccepted=True,
  currentNineArenaAccepted=arenas,allNineBothCharactersBothSlots=False,
  actualP2SquareJumpKickInterruptionAccepted=True,p2SquareUppercutStillUnexercised=True,
  cleanupAllocatedBytesReclaimed=total_saved,immutableBuildExecutablesCompressed=compressed,deletedFiles=0,allOldBuildFoldersRemoved=False,
  actualKanoP2LadderReachedKintaro=True,actualFullLadderClearAccepted=False,actualEndingsAccepted=False,
  pendingCaptures=pending,failedAndUnexercisedCapturesRetained=True,oldCapturedEvidenceChanged=False,
  newReleaseZIPCreated=False,acceptedReports=accepted,inputHashes=pins,fullPortAcceptance=False,
  remaining=['Finish and strictly verify live current Kano P1/Sonya P2 all-nine-arena captures',
   'Full move-phase art/ground/shadow choreography; more CPU repertoire, repeated/KO/overlap and interruption coverage',
   'All finishers, victims, morphs, boss/campaign clears, endings, secrets and cinematics',
   'Remaining obsolete-folder cleanup while retaining required inputs; final release ZIP'])
if __name__=='__main__':
 assert not OUT.exists(),'Never overwrite checkpoint'
 r=freeze();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(dict(saved=str(OUT/'checkpoint.json'),candidate=r['currentCandidate'],pins=len(r['inputHashes']),pending=r['pendingCaptures'],reclaimedBytes=r['cleanupAllocatedBytesReclaimed'],goalStatus='active',fullPortAcceptance=False),indent=2))
