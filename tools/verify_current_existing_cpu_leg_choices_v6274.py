"""Requalify existing current CPU leg phases and all three Sonya AI choices.

Reuse the two actual5324 native boots, not another emulator or raw recording.
Keep full original paired choreography/physics/cleanup and independent whole
state/health ledgers. Choice entry is not full ring/child/audio/art acceptance.
"""
import copy,datetime,json,re,struct,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_native_extended_cpu_v2946 as stream
import verify_native_cpu_ring_v2971 as phase_source
import native_extended_cpu_pair_contract_v2939 as pair
import capture_current_cmd_specials_v6263 as census
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6275_current_existing_cpu_leg_choices_checked'
PARENT=ROOT/'audit_v6273_current_native_branch_inventory/report.json'

def choice_rows(text):
 rows=[]
 for line in text.splitlines():
  if line.startswith('MK2_CPU_CHOICE_EVENT '):
   values=re.findall(r'(\w+)=([^\s]+)',line);need(len(values)==len(dict(values)),'Unambiguous actual CPU choice fields');rows.append(dict(values))
 return rows

def choice_gate(rows,guest):
 n=lambda r,k:int(r[k],16 if k in('entry','pc','opcode','mask','actor','main','owner','status','a0','a1','a2','schedule')else 10)
 kinds=dict(entry=0xfffbc200,first_call=0xfffbc220,first_result=0xfffbc250,second_call=0xfffbc280,second_result=0xfffbc2b0,ring=0xfffbc2c0,square=0xfffbc2f0,bicycle=0xfffbc320)
 serials=sorted({n(r,'serial')for r in rows});need(serials==list(range(1,len(serials)+1))and serials,'Contiguous actual native choice serials')
 accepted=[]
 for serial in serials:
  events=[r for r in rows if n(r,'serial')==serial];first=events[0]
  for r in events:
   entry=n(r,'entry');need(r['kind']in kinds and entry==kinds[r['kind']]and n(r,'pc')==entry+16 and n(r,'mask')==65535 and n(r,'opcode')==struct.unpack_from('<H',guest,(entry-0xff800000)//8)[0],'Actual native route opcode/PC/read mask')
   need(n(r,'actor')==n(r,'owner')==n(first,'actor')and n(r,'main')==n(first,'main')and n(r,'frame')==n(first,'frame')and n(r,'id')==n(r,'roster')==18 and(n(r,'state'),n(r,'human_state'),n(r,'mode'),n(r,'stage'))==(0,1,2,0)and n(r,'schedule')==0xfffa3180 and r['writes']=='0'and r['assistance']=='none','Actual true native CPU Sonya branch ownership, input-only scope and same field')
   need(n(r,'carry')==(n(r,'status')>>30)&1,'Actual CPU status carry, not inferred branch label')
  need([r['kind']for r in events[:3]]==['entry','first_call','first_result']and n(events[1],'a0')==250 and 0<=n(events[2],'a0')<1000 and n(events[2],'carry')==int(n(events[2],'a0')<250),'Actual original native first random comparison')
  if n(events[2],'carry'):
   expected=['entry','first_call','first_result','bicycle'];chosen='bicycle';returned=events[2]
  else:
   need(len(events)==6 and events[3]['kind']=='second_call'and events[4]['kind']=='second_result'and n(events[3],'a0')==400 and 0<=n(events[4],'a0')<1000 and n(events[4],'carry')==int(n(events[4],'a0')<400),'Actual original native second random comparison')
   chosen='square'if n(events[4],'carry')else'ring';expected=['entry','first_call','first_result','second_call','second_result',chosen];returned=events[4]
  need([r['kind']for r in events]==expected and all(n(events[-1],k)==n(returned,k)for k in('a0','a1','a2','carry')),'Complete native conditional branch and preserved return registers')
  accepted.append(dict(serial=serial,frame=n(first,'frame'),move=chosen,actor=n(first,'actor'),main=n(first,'main'),actualNativeEvents=len(events),fullMoveOrChildAcceptance=False))
 return accepted

def gate(text,guest):
 health,by=stream.health_ledger(text,guest,'kano');state=stream.state_ledgers(text,guest,'kano',by)
 complete=pair.rows(text,'COMPLETE');need(len(complete)==3,'Three actually completed CPU leg cycles')
 legs=[pair.verify_pair(text,'kano',r['cycle'],guest)for r in complete]
 need(all(r['passed']and r['target']=='sonya'and r['damage']==35 and r['held_fields']==46 for r in legs),'Entire original five-phase leg hold/damage/physics/both-owning cleanup contract')
 choices=choice_gate(choice_rows(text),guest);need({r['move']for r in choices}=={'ring','square','bicycle'},'All three actually naturally chosen Sonya traveling branches present')
 return dict(wholeNativeHealthLedger=health,wholeNativeStateLedger=state,threeOriginalCompleteLegContracts=legs,nativeChoices=choices)

def mutate_field(text,tag,key,value,predicate=lambda r:True):
 lines=text.splitlines()
 for i,line in enumerate(lines):
  if line.startswith(tag+' '):
   row=dict(re.findall(r'(\w+)=([^\s]+)',line))
   if key in row and predicate(row):
    lines[i]=re.sub(r'(?<!\w)'+re.escape(key)+r'=[^\s]+',key+'='+value,line,count=1);return '\n'.join(lines)+'\n'
 raise ValueError('No actual mutation target '+tag+' '+key)

def main():
 need(not OUT.exists(),'Fresh immutable existing-evidence qualification')
 need(not census.prior.census(),'Actual native census empty; do not start another game')
 guest=current.expected();phase_source.phase_contract_source()
 baseline=ROOT/'audit_v2972_native_cpu_ring_checked/report.json';old=json.loads(baseline.read_text())
 for module in(pair,stream,phase_source):need(sha(module.__file__)==old['inputHashes'][str(Path(module.__file__).resolve())],'Entire original phase and state/health ledger source unchanged')
 actual=ROOT/'audit_v5325_current_cpu_bicycle_ram_checked/report.json';prior=json.loads(actual.read_text())
 need(prior['passed']and prior['candidate']==current.NAME,'Actual prior current native terminal/audio qualification')
 pins=dict(prior['inputHashes']);cases=[];faults=[]
 for suffix in('samples','nosamples'):
  folder=ROOT/f'audit_v5324_current_cpu_bicycle_ram_{suffix}';meta=json.loads((folder/'result.json').read_text());proof=json.loads((folder/'guest_memory_proof.json').read_text());text=(folder/'run.log').read_text()
  need(meta['exit_code']==0 and meta['candidate']==current.NAME and meta['wholeActualGuestComparedInRAM']and proof['sha256']==current.GUEST_SHA and proof['bytes']=='1048576'and not(folder/'stderr.log').read_text().strip()and'hex='not in text,'Actual terminal0 current full-guest input-only trace, no raw recordings')
  result=gate(text,guest);cases.append(dict(samplesEnabled=suffix=='samples',folder=str(folder),qualification=result))
  trials=[('cpu_proxy',mutate_field(text,'MK2_CPU_PAIR_FIELD','id','1')),
   ('missing_live_state',text.replace(next(line+'\n'for line in text.splitlines()if line.startswith('MK2_CPU_PAIR_FIELD ')),'',1)),
   ('health_write_changed',mutate_field(text,'MK2_CPU_ROUND_HEALTH','after','0')),
   ('leg_pose_changed',mutate_field(text,'MK2_CPU_PAIR_FIELD','pose','00000000',lambda r:r.get('action')=='272')),
   ('leg_release_damage',mutate_field(text,'MK2_CPU_PAIR_EVENT','a10','00000022',lambda r:r.get('kind')=='damage')),
   ('leg_handoff_lock',mutate_field(text,'MK2_CPU_PAIR_OWN_REGAIN','body','0004')),
   ('choice_proxy_owner',mutate_field(text,'MK2_CPU_CHOICE_EVENT','owner','01000000')),
   ('choice_wrong_opcode',mutate_field(text,'MK2_CPU_CHOICE_EVENT','opcode','FFFF')),
   ('choice_wrong_threshold',mutate_field(text,'MK2_CPU_CHOICE_EVENT','a0','000000FB',lambda r:r.get('kind')=='first_call')),
   ('choice_missing_boundary',text.replace(next(line+'\n'for line in text.splitlines()if line.startswith('MK2_CPU_CHOICE_EVENT ')),'',1))]
  for label,bad in trials:
   try:gate(bad,guest)
   except(ValueError,AssertionError,KeyError)as error:faults.append(dict(case=suffix,fault=label,rejectedBy=str(error)))
   else:raise ValueError('Actual CPU phase/choice fault accepted '+label)
  need(gate(text,guest)==result,'Positive original entire gate restored after actual faults')
  for p,h in meta['input_hashes'].items():need(sha(p)==h,'Actual existing current boot inputs unchanged');pins[p]=h
  for p in folder.glob('*'):
   if p.is_file():pins[str(p.resolve())]=sha(p)
 for p in(PARENT,actual,baseline,Path(__file__).resolve(),Path(pair.__file__),Path(stream.__file__),Path(phase_source.__file__),Path(current.__file__)):
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Full actual source/evidence immutable at final qualification')
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Current full-scope inventory retained')
 report=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=current.NAME,guestSHA256=current.GUEST_SHA,goalStatus='active',parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],cases=cases,actualFaultsRejected=faults,inputHashes=pins,actualCurrentCompletedCPULegCycles=6,originalWholePhaseStateHealthGatesRetained=True,currentAllThreeSonyaTravelingChoicesQualified=True,fullRingChildAcceptance=False,fullCPULegArtShadowAudioAcceptance=False,fullPortAcceptance=False,fullGoalComplete=False,newNativeBoots=0,newBuilds=0,newZIPs=0,newRawMedia=0,
  thisGoalTurnClassification='progress: current frozen table/AI/ladder inventory plus existing current actual CPU leg and all three natural choice branches independently requalified; no repeated native games',nextAction='Current Kano traveling CPU routes and remaining branch-specific fidelity, reusing already complete UI/campaign/ending/Friendship evidence')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Only compact existing-evidence report')
 print(json.dumps(dict(passed=True,actualExistingCPULegCycles=6,nativeChoiceBranches=3,actualFaultsRejected=len(faults),newNativeBoots=0,fullPortAcceptance=False)),flush=True)

if __name__=='__main__':
 try:main()
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
