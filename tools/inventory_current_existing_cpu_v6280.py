"""Flat current CPU inventory; keep accepted pairs and mixed rejections distinct.

Requalify existing5324 traces only. No capture/build/guest state changes.
Original phase/state/health contracts and their mixed-case rejection remain.
"""
import datetime,json,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_current_existing_cpu_leg_choices_v6274 as source_gate
import inventory_current_cpu_leg_choices_v6276 as qualified
import inventory_current_cpu_leg_choices_v6278 as fault_target
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6281_current_existing_cpu_inventory'
PARENT=ROOT/'audit_v6273_current_native_branch_inventory/report.json'

def main():
 need(not OUT.exists(),'Fresh actual terminal inventory')
 need(not source_gate.census.prior.census(),'Actual native census empty; reuse existing runs')
 guest=current.expected();source_gate.phase_source.phase_contract_source()
 baseline=ROOT/'audit_v2972_native_cpu_ring_checked/report.json';original=json.loads(baseline.read_text())
 for module in(source_gate.pair,source_gate.stream,source_gate.phase_source):
  need(sha(module.__file__)==original['inputHashes'][str(Path(module.__file__).resolve())],'Full original source-qualified native contracts unchanged')
 prior_path=ROOT/'audit_v5325_current_cpu_bicycle_ram_checked/report.json';prior_report=json.loads(prior_path.read_text())
 need(prior_report['passed']and prior_report['candidate']==current.NAME,'Existing actual current native terminal qualification')
 pins=dict(prior_report['inputHashes']);cases=[];faults=[]
 for suffix in('samples','nosamples'):
  folder=ROOT/f'audit_v5324_current_cpu_bicycle_ram_{suffix}';meta=json.loads((folder/'result.json').read_text());proof=json.loads((folder/'guest_memory_proof.json').read_text());text=(folder/'run.log').read_text()
  need(meta['exit_code']==0 and meta['candidate']==current.NAME and meta['wholeActualGuestComparedInRAM']and proof['sha256']==current.GUEST_SHA and proof['bytes']=='1048576'and not(folder/'stderr.log').read_text().strip()and'hex='not in text,'Actual natural native terminal and independently compared full current guest')
  result=qualified.gate(text,guest);cases.append(dict(samplesEnabled=suffix=='samples',folder=str(folder),qualification=result))
  mutate=fault_target.held_mutation
  trials=[('cpu_proxy',mutate(text,'MK2_CPU_PAIR_FIELD','id','1')),
   ('missing_live_state',text.replace(next(line+'\n'for line in text.splitlines()if line.startswith('MK2_CPU_PAIR_FIELD ')),'',1)),
   ('health_write_changed',mutate(text,'MK2_CPU_ROUND_HEALTH','after','0')),
   ('held_leg_pose_changed',mutate(text,'MK2_CPU_PAIR_FIELD','pose','00000000',lambda r:r.get('action')=='272')),
   ('leg_release_damage',mutate(text,'MK2_CPU_PAIR_EVENT','a10','00000022',lambda r:r.get('kind')=='damage')),
   ('leg_handoff_lock',mutate(text,'MK2_CPU_PAIR_OWN_REGAIN','body','0004')),
   ('choice_proxy_owner',mutate(text,'MK2_CPU_CHOICE_EVENT','owner','01000000')),
   ('choice_wrong_opcode',mutate(text,'MK2_CPU_CHOICE_EVENT','opcode','FFFF')),
   ('choice_wrong_threshold',mutate(text,'MK2_CPU_CHOICE_EVENT','a0','000000FB',lambda r:r.get('kind')=='first_call')),
   ('choice_missing_boundary',text.replace(next(line+'\n'for line in text.splitlines()if line.startswith('MK2_CPU_CHOICE_EVENT ')),'',1))]
  for label,bad in trials:
   try:qualified.gate(bad,guest)
   except(ValueError,AssertionError,KeyError)as error:faults.append(dict(case=suffix,fault=label,rejectedBy=str(error)))
   else:raise ValueError('Actual physical CPU fault accepted '+label)
  need(qualified.gate(text,guest)==result,'Entire original positive restored after actual-record faults')
  for p,h in meta['input_hashes'].items():need(sha(p)==h,'Actual existing cold-boot inputs unchanged');pins[p]=h
  for p in folder.glob('*'):
   if p.is_file():pins[str(p.resolve())]=sha(p)
 for p in(PARENT,prior_path,baseline,Path(__file__).resolve(),Path(current.__file__),
          Path(source_gate.__file__),Path(qualified.__file__),Path(fault_target.__file__),
          Path(source_gate.pair.__file__),Path(source_gate.stream.__file__),Path(source_gate.phase_source.__file__)):
  pins[str(p.resolve())]=sha(p)
 failures=[]
 for leaf in('audit_v6275_current_existing_cpu_leg_choices_checked','audit_v6277_current_cpu_leg_choice_inventory','audit_v6279_current_cpu_leg_choice_inventory'):
  p=ROOT/leaf/'failure.json';r=json.loads(p.read_text());need(not r['passed'],'Every original attempted qualification remains rejected');pins[str(p.resolve())]=sha(p);failures.append(dict(path=str(p),error=r['error']))
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,'Entire original scope retained')
 need(all(sha(p)==h for p,h in pins.items()),'Actual immutable whole relevant sources and evidence before final inventory')
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=current.NAME,guestSHA256=current.GUEST_SHA,goalStatus='active',parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],cases=cases,actualFaultsRejected=faults,inputHashes=pins,preservedQualificationFailures=failures,
  actualCurrentAcceptedStandaloneCPULegCycles=4,actualOriginalRejectedMixedLegSquareCycles=2,currentAllThreeSonyaNativeRNGChoicesQualified=True,originalWholePhaseStateHealthGatesRetained=True,compoundLegToSquareAccepted=False,fullRingChildAcceptance=False,fullCPULegArtShadowAudioAcceptance=False,fullPortAcceptance=False,fullGoalComplete=False,newNativeBoots=0,newBuilds=0,newZIPs=0,newRawMedia=0,
  previousGoalTurnClassification='progress: actual canonical CMD sixteen-case move matrix',thisGoalTurnClassification='progress: forty current typed tables, six ladder schedules, eight CPU branches source-bound with127faults; four original full CPU legs and three Sonya RNG branches per existing enabled/disabled trace requalified with20actual faults, retaining both mixed-case rejections',
  nextActions=['Validate existing compound CPU leg-to-Square continuation with exact original standalone rejection retained','Current Kano knife/ball/blade CPU branch fidelity; reuse completed campaigns/UI/endings/Friendships','Complete remaining branch-specific art/audio and matched release handoff'])
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact compact terminal report; no raw media')
 print(json.dumps(dict(passed=True,acceptedStandaloneCPULegCycles=4,rejectedMixedLegSquareCycles=2,actualNativeSonyaChoiceBranches=3,actualFaultsRejected=len(faults),newNativeBoots=0,newBuilds=0,fullPortAcceptance=False)),flush=True)

if __name__=='__main__':
 try:main()
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
