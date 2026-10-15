"""Additive actual Sub-Zero evidence; full native campaign stays live/open."""
import collections,datetime,gzip,hashlib,json,re,subprocess
from pathlib import Path
import run_verified_kitana_jax_sonya_p2_campaign_v5663 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v5681_subzero_sonya_p2_progress'


def run():
 need(not OUT.exists(),'Fresh immutable additive goal receipt')
 parent_path=ROOT/'audit_v5668_verified_jax_sonya_p2_progress/progress.json'
 parent=json.loads(parent_path.read_text())
 first_path=ROOT/'audit_v5670_current_sonya_p2_subzero_prefix_checked/report.json'
 ring_path=ROOT/'audit_v5679_sonya_p2_subzero_ring_record_bound_checked/report.json'
 first=json.loads(first_path.read_text());ring=json.loads(ring_path.read_text())
 need(first['passed']and first['actualCompletePhysicalReplay']['actualCompleteGuardFields']==1737 and
  first['actualCompletePhysicalReplay']['actualNativeLegActivations']==7 and
  first['actualHuman107Stores']==0 and not first['executedNativeHuman107InstructionGateAccepted']and
  len(first['actualRecordFaultsRejected'])==8 and len(first['actualOwnedActionFaultsRejected'])==4,
  'Actual full first Sub-Zero input/ownership/Leg proof; unexecuted HUMAN107 not credited')
 need(ring['passed']and ring['actualContext8PhysicalFields']==2537 and ring['actualContext8RingTasks']>0 and
  len(ring['actualInputStateAndNativeWinnerFaultsRejected'])==11 and
  len(ring['actualContext8TaskAndActionFaultsRejected'])==8 and
  ring['allElevenStateInputWinnerFaultsTargetActualSubZero']and
  not ring['native']['actualSubZeroEncounterWon']and ring['native']['actualOwnSubZeroRoundWins']==1 and
  ring['native']['actualSubZeroRoundWins']==2 and not ring['actualSubZeroAdvanceAccepted'],
  'Whole true Sub-Zero Ring encounter qualified; actual first match loss remains loss')
 for report in(first,ring):need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every qualified source and actual proof remains intact')
 # Bounded streaming observation, not a replacement for the independent first
 # encounter/full campaign replay. No encoded buffers, log copy or guest writes.
 count=0;digest=hashlib.sha256();fields=0;legs=0;uppercuts=0;wins=0;losses=0
 reasons=collections.Counter();cpu_actions=collections.Counter();boundary=None
 with gzip.open(capture.OUT/'run.log.gz','rt',encoding='utf-8',newline='')as reader:
  for line in reader:
   need(line.endswith('\n'),'Complete actual native observation rows only')
   raw=line.encode();count+=len(raw);need(count<=512*1024*1024,'Bounded first80real losses, never unbounded read')
   digest.update(raw)
   if line.startswith(('MK2_NAT_CAMPAIGN_SUBZERO_FIELD ', 'MK2_NAT_CAMPAIGN_SUBZERO_DECISION ',
    'MK2_NAT_CAMPAIGN_SUBZERO_ACTION ', 'MK2_NAT_CAMPAIGN_SPECIAL ',
    'MK2_NAT_CAMPAIGN_WIN ', 'MK2_NAT_CAMPAIGN_LOSS ')):
    row=dict(re.findall(r'(\w+)=([^\s]+)',line))
    if row.get('stage')!='7':continue
    need(row['human_slot']=='2'and row['fighter']=='sonya'and row['writes']=='0'and row['assistance']=='none',
     'Only actual physical true Sonya P2 observations, no guest assistance')
    if line.startswith('MK2_NAT_CAMPAIGN_SUBZERO_FIELD '):
     need(row['human_id']==row['human_roster']=='18'and row['cpu_id']==row['cpu_roster']=='8',
      'Every observed native field retains true added Sonya and true original Sub-Zero')
     fields+=1;cpu_actions[int(row['cpu_action'])]+=1
    elif line.startswith('MK2_NAT_CAMPAIGN_SUBZERO_DECISION '):reasons[row['reason']]+=1
    elif line.startswith('MK2_NAT_CAMPAIGN_SUBZERO_ACTION '):uppercuts+=int(row['after'])==0x107
    elif line.startswith('MK2_NAT_CAMPAIGN_SPECIAL ')and row['move']=='leg':legs+=1
    elif line.startswith('MK2_NAT_CAMPAIGN_WIN '):wins+=row['slot']=='2'
    elif line.startswith('MK2_NAT_CAMPAIGN_LOSS '):
     losses+=1;need(int(row['number'])==losses,'Sequential genuine native loss observations')
     if losses==80:boundary=line.strip();break
  else:raise ValueError('Await known completed80loss boundary; never restart active process')
 need(fields>0 and legs>0 and boundary is not None,'Actual complete bounded observation, no fixture')
 manifest=json.loads((capture.OUT/'process.json').read_text())
 query=f"Get-CimInstance Win32_Process -Filter 'ProcessId={manifest['pid']} OR ProcessId={manifest['hostPID']}' | Select-Object ProcessId,Name,CommandLine,@{{Name='createdUnix';Expression={{([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}}}} | ConvertTo-Json -Compress"
 jobs=json.loads(subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True,check=True).stdout)
 need(isinstance(jobs,list)and len(jobs)==2,'Same native/host processes freshly verified live, not a lock file')
 for expected in parent['observedLiveProcesses']:
  actual=next(p for p in jobs if p['ProcessId']==expected['ProcessId'])
  need(actual==expected,'Same Name/creation/command; no reused PID or observation-timeout restart')
 need(not(capture.OUT/'result.json').exists(),'Current full campaign remains actually nonterminal')
 failure=ROOT/'audit_v5677_sonya_p2_subzero_ring_bound_checked/report.json'
 need(json.loads(failure.read_text())['passed']is False,'Trailing-space record lookup failure preserved')
 probe=ROOT/'audit_v5673_sonya_p2_subzero_ring_probe'
 terminal=json.loads((probe/'result.json').read_text())
 need(terminal['passed']and terminal['nativeExit']==0 and terminal['rawMediaGuestAudioFilesWritten']==0 and
  not any(p.suffix.lower()in('.png','.wav','.bin')for p in probe.rglob('*')if p.is_file()),
  'Ordinary real probe terminal, no automatic timed-stop PNG or raw-buffer files')
 public={ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd':'ADDFB038FCE6EF922358D813E39736B533C570E97D6A043C4A916281A8F1095E',
  ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA'}
 need(all(sha(p)==h for p,h in public.items()),'Public CMD/ZIP not promoted')
 sources=[ROOT/n for n in('tools/verify_current_sonya_p2_subzero_prefix_v5669.py',
  'mk2ks_sonya_p2_subzero_ring_probe_v5671.lua','tools/run_sonya_p2_subzero_ring_probe_v5672.py',
  'tools/verify_sonya_p2_subzero_ring_probe_v5674.py','tools/verify_sonya_p2_subzero_ring_bound_v5676.py',
  'tools/verify_sonya_p2_subzero_ring_record_bound_v5678.py')]+[Path(__file__).resolve()]
 folders=[probe,first_path.parent,ring_path.parent,failure.parent,
  ROOT/'audit_v5675_sonya_p2_subzero_ring_probe_checked']
 sealed=[p for folder in folders for p in folder.rglob('*')if p.is_file()]
 pins={str(p.resolve()):sha(p)for p in[parent_path,*sources,*sealed,*public]}
 journal=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
  remaining=parent['remaining'],parentAdditiveJournal=str(parent_path),
  previousGoalTurnClassification='no progress: courtesy acknowledgment; active goal and exact running jobs revalidated before task actions',
  thisGoalTurnClassification='progress:1737actual Sub-Zero guard fields/7real Leg tasks qualified with12actual faults. Finite Ring comparison completed;2537actual Sub-Zero fields/owned Ring tasks,19context-bound faults and genuine one-own/two-CPU round loss qualified. Original lookup failure retained; first80real loss coverage measured as observation only. Same original native campaign confirmed live; no build/ROM/public mutation.',
  firstGuardEncounterProof=str(first_path),ringEncounterProof=str(ring_path),
  actualFirstGuardFields=1737,actualFirstGuardLegTasks=7,firstGuardActualFaultsRejected=12,
  firstEncounterNativeHuman107Accepted=False,ringActualSubZeroFields=2537,
  ringActualSubZeroTasks=ring['actualContext8RingTasks'],ringActualTargetFaultsRejected=19,
  ringActualOwnRoundWins=1,ringActualCpuRoundWins=2,ringActualMatchWon=False,
  preservedVerifierFailure=str(failure),
  boundedRepeatedSubZeroObservation=dict(actualCompleteLosses=losses,actualFields=fields,actualLegTasksObserved=legs,
   actualHuman107StoresObserved=uppercuts,actualOwnRoundWinsObserved=wins,actualReasons=dict(reasons),
   actualCPUActions=dict(cpu_actions),boundary=boundary,actualPrefixBytes=count,
   actualPrefixSHA256=digest.hexdigest().upper(),observationOnly=True,
   all80CompletePhysicalReplaysAccepted=False,uppercutInstructionFaultGateAccepted=False),
  fullCampaignToolSession=29503,observedLiveProcesses=jobs,newNativeProcessStartsThisTurn=1,
  newBuilds=0,deletedFiles=0,rawGuestRGBPCMFilesWritten=0,publicPlayableChanged=False,publicZIPChanged=False,
  fullSonyaP2TowerAccepted=False,fullEndingPixelsAccepted=False,completeCampaignAudioAccepted=False,
  fullPortAcceptance=False,sourceInputs=pins,
  next='Poll same29503/127684/141652 creation identity. Current controller still naturally loses to Sub-Zero; actual107branch and tower remain unproven. Ring wins one real round but not the match; investigate bounded genuine retry comparison before any replacement, never call first-loss probe a clear. Broader all five scope groups remain unchanged.')
 OUT.mkdir();path=OUT/'progress.json';path.write_text(json.dumps(journal,indent=2)+'\n')
 targets=[p for p in sealed if p.suffix in('.json','.log','.cfg')]+sources+[path]
 before={str(p):sha(p)for p in targets}
 for p in targets:
  need(p.resolve().is_relative_to(ROOT.resolve()),'Exact bounded sealed-file compression targets')
  need(subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True).returncode==0,
   'Lossless static source/evidence compression')
 need(all(sha(p)==h for p,h in before.items())and all(sha(p)==h for p,h in pins.items()),
  'Every actual failure/proof/source/public byte intact; growing campaign log untouched')
 print(json.dumps({k:v for k,v in journal.items()if k not in('sourceInputs','observedLiveProcesses')},indent=2),flush=True)


if __name__=='__main__':run()
