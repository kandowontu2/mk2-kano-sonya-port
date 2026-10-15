"""Full-scope additive journal: four real earned offset cases, not port completion."""
import hashlib, json, subprocess
from pathlib import Path
import run_native_subzero_offset_regression_v4856 as native

ROOT,need,sha=native.ROOT,native.need,native.sha
PARENT=ROOT/'audit_v4869_native_subzero_repair_progress/progress.json'
OUT=ROOT/'audit_v4916_earned_subzero_matrix_progress'

def main():
 need(not OUT.exists(),'Fresh additive full-scope journal')
 parent=json.loads(PARENT.read_text());need(parent['goalStatus']=='active'and len(parent['remaining'])==5,'All original five groups retained')
 checked=ROOT/'audit_v4914_earned_subzero_offset_matrix_checked/report.json'
 matrix=json.loads(checked.read_text())
 need(matrix['passed']and len(matrix['cases'])==4 and len(matrix['actualFaultsRejected'])==36
      and not matrix['fullPortAcceptance']and not matrix['fullShatterAccepted']and not matrix['ownFrozenBodyAccepted'],
      'Only actual finite four-case offset regression accepted')
 pins={}
 def pin(path,wanted=None):
  path=Path(path).resolve();digest=sha(path)
  need(wanted is None or wanted==digest,'Exact current evidence bytes')
  need(str(path)not in pins or pins[str(path)]==digest,'Consistent source pins')
  pins[str(path)]=digest
 for path in (PARENT,checked,Path(__file__).resolve(),ROOT/'tools/verify_earned_subzero_offset_matrix_v4913.py'):pin(path)
 for p,h in matrix['inputHashes'].items():pin(p,h)
 for number in (4870,4875,4880,4884,4889,4893,4897,4901,4905):pin(ROOT/f'mk2ks_earned_subzero_victims_v{number}.lua')
 pin(ROOT/'mk2ks_earned_subzero_offset_v4909.lua')
 for number in (4871,4876,4881,4885,4890,4894,4898,4902,4906):pin(ROOT/f'tools/run_earned_subzero_victims_v{number}.py')
 pin(ROOT/'tools/run_earned_subzero_offset_v4910.py')
 failures=[]
 for capture,observed in ((4872,4873),(4877,4878),(4882,4883),(4886,4887),(4891,4892),(4895,4896),(4899,4900),(4903,4904),(4907,4908)):
  folder=ROOT/f'audit_v{capture}_subzero_kano_p1_earned'
  report_path=ROOT/f'audit_v{observed}_subzero_kano_p1_earned_observed/report.json'
  report=json.loads(report_path.read_text());meta=json.loads((folder/'result.json').read_text())
  need(not report['passed'] and not report['fullPortAcceptance'],'Every executed failed case retained as failed')
  for p,h in meta['inputHashes'].items():pin(p,h)
  for p in (report_path,*[p for p in folder.rglob('*')if p.is_file()]):pin(p)
  failures.append(dict(capture=str(folder),report=str(report_path),error=report['error'],nativeExit=meta['nativeExit'],
                       fullFinisherAccepted=False))
 for p in (ROOT/'art_native_subzero_v4888').rglob('*'):
  if p.is_file():pin(p)
 master=ROOT/'art_native_subzero_v4888/kano-sonya-frozen-bodies.png'
 need(sha(master)=='13F3938BED3E1337E8847FAAE7A6646DFF227CF02D943AF097C217A63D6F1E2F','Exact selected AI master, still not native accepted')
 public={
  'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
  'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
  'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
 }
 for p,h in public.items():pin(ROOT/p,h)
 guest=native.expected();program=ROOT/'mk2/mk2-maincpu.bin';pin(program,'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23')
 prompts=json.loads((ROOT/'art_native_subzero_v4888/generation-prompts.json').read_text())
 report=dict(schema=1,baseFullScopeCheckpoint=parent['baseFullScopeCheckpoint'],
  parentAdditiveJournals=parent['parentAdditiveJournals']+[str(PARENT)],
  mergeRule='Additive to4557 and every parent; preserve original full scope and finite successes. Four new actual physical earned0616 cases extend only native offset-repair coverage. Own body, shatter, normal-health freeze, all other full-port requirements remain mandatory and unaccepted.',
  remaining=parent['remaining'],newInputHashes=pins,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
  previousGoalTurnClassification='no progress: acknowledgement only. Revalidated current source, failed cases, exact native candidate and active full goal before further action.',
  thisGoalTurnClassification='progress: original native dispatch/history parsed; actual Forward Forward Down High Kick reaches real0616 after two earned rounds. Four cold boots on4850 independently compare every initialized1MB guest byte in RAM. True17/18 in both slots now use dedicated zero-offset rows and own main40/dizzy groups without global-cache overrun for401 consecutive fields each. Independent4913 binds20 native opcode/PC/mask records,1604 consecutive native fields,12 mirrored history comparisons and rejects36 actual-row/field faults. Full attempted shatter4907 honestly fails host callback and approach; not accepted. No gameplay build/source changes or public promotion this turn.',
  actualOffsetRepairMatrix=str(checked),actualCases=matrix['cases'],actualWholeColdGuestComparisons=4,
  initializedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),actualNativeFaultsRejected=36,
  normalHealthFreezeAccepted=False,ownFrozenBodyAccepted=False,fullShatterAccepted=False,
  correctedSourceUnderstanding=dict(
   deepFreezePhysicalCommand=['Forward','Forward','Down','High Kick'],
   reverseHistorySide1=[6,7,7],reverseHistorySide2=[6,8,8],historyTable='FF8785C0',
   highKickDispatchTable='FF862D20',trueSubZeroRow='FF862E20',nativeHumanConsumer='FF865B00',
   nativeFreezeEntry='FF8C1490',nativeVictimEntry='FF8C2320',
   actualRuntimeHistoryProof='Every comparison matches original ROM at table-16; HK parser actualA0=33/A1=300C.',
   shatterPhysicalCommand=['Forward','Down','Forward','Forward','High Punch'],shatterRequiresVictimAction='0616',
   priorOrdinaryIceballClaim='Not proven; retracted. Shared victim0616 inference fromFF8C1490 caller did not establish normal-health iceball routing. New positive cases explicitly earned zero-health deep-freeze only.'),
  preservedExecutedFailures=failures,
  actualIncompleteShatter=dict(case='audit_v4907_subzero_kano_p1_earned',
   actualFreezeFrame=3152,actualBodyLookupFrame=3208,actualFrozenBodyGroup='FF8C2E10',
   physicalWalkApproachStoppedAtCenterGap=85,desiredCenterGap=55,shatterInputNeverIssued=True,
   callbackFailure='Readonly assert real identity became invalid after natural later mode/roster transition; cannot accept run or hide callback errors.',
   collisionRootCauseQualified=False,
   next='Integrate dedicated own frozen body then diagnose native close-range collision/distance as needed, and actually issue/verify full shatter/parts/cleanup/audio in both slots. Do not lower native distance gate, alter coordinates, force victim state or accept the bounded freeze-only probe as this finisher.'),
  frozenBodyMaster=dict(path=str(master),sha256=sha(master),prompts=str(ROOT/'art_native_subzero_v4888/generation-prompts.json'),
   builtInImageGeneration=True,selectedMasterOnly=True,nativeEncoded=False,nativeAccepted=False),
  publicCMDExecutableZIPAndHistoricalInstalledEXEUnchanged=True,newBuilds=0,newGameplaySourceEdits=0,
  newPayloadCopies=0,rawGuestMediaOrPCMFilesWritten=0,newDeletions=0,
  cleanupAccounting='Only compressed physical-controller sources, small native logs and digest reports. No new build/payload copies or raw screenshots/audio/guest dumps. Preserve prior32.49GiB cleanup; do not resurrect retired historical leaves.',
  nextAction='Inspect actual current native dizzy/composite geometry and unused ROM/payload/GFX spans; encode selected own Kano/Sonya ice master into original3-component groups and extend native body ID lookup with stock semantics retained. Compile isolated candidate preserving dirty checkout/installed EXE; verify actual full shatter, close-range behavior, parts, cleanup and audio in both slots. Continue every original Pit/Tomb/move-art/grounding/floor-shadow/CPU/KO/overlap/finishers/victims/morphs/secrets/cinematics/natural endings/selection/ladder/names/dependency-aware cleanup/refreshed ZIP requirement.')
 need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Exact current pins and full scope preserved')
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before journal')
 (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),actualOffsetCases=4,
                      fullShatterAccepted=False,fullPortAcceptance=False,goalStatus='active'),indent=2),flush=True)

if __name__=='__main__':main()
