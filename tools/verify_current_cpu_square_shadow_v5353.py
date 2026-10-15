"""Current natural CPU Square hit: full finite phase/body/shadow, whole match state/HP."""
import copy,inspect,json,re,traceback
from collections import defaultdict
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_special_shadow_v5141 as body
import native_cpu_square_hit_contract_v3037 as phase
import verify_native_extended_cpu_v2946 as ledgers
ROOT,need,sha=current.ROOT,current.need,current.sha
FOLDER=ROOT/'audit_v5351_current_cpu_sonya_square_human_kano'
OBSERVED=ROOT/'audit_v5352_current_cpu_sonya_square_observed/report.json'
OUT=ROOT/'audit_v5354_current_cpu_sonya_square_shadow_checked'
def run():
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 observed=json.loads(OBSERVED.read_text());need(observed['passed']and observed['nativeExit']==0 and
  observed['originalWholePhysicalTrajectoryUnchanged']and observed['originalCPUExitNotReplaced'],'Actual unchanged natural input/RNG/state/health timeline and native terminal0')
 baseline=ROOT/'audit_v3282_current_cpu_square_render_erase_checked/report.json'
 old=json.loads(baseline.read_text());need(old['passed'],'Original full physical Square source qualification')
 for module in(phase,ledgers):need(sha(module.__file__)==old['inputHashes'][str(Path(module.__file__).resolve())],'Entire original native phase/state/health checker unchanged')
 qualified=ROOT/'audit_v5142_special_shadow_ring_p1_checked/report.json'
 accepted=json.loads(qualified.read_text())
 for p in(Path(body.__file__),ROOT/'tools/verify_move_phase_shadow_v5089.py'):
  need(sha(p)==accepted['inputHashes'][str(p.resolve())],'Entire original body/shadow model unchanged')
 pins={str(p):sha(p)for p in(OBSERVED,baseline,qualified,Path(__file__),Path(phase.__file__),Path(ledgers.__file__),Path(body.__file__))}
 for p,h in observed['inputHashes'].items():need(sha(p)==h,'Every executed/compiled source stable');pins[p]=h
 log=(FOLDER/'run.log').read_text();typed=phase.verify(log,guest,'kano')
 health,round_by=ledgers.health_ledger(log,guest,'kano');state=ledgers.state_ledgers(log,guest,'kano',round_by)
 rows=defaultdict(list)
 lo,hi=typed['start']-30,max(typed['lastScene'],typed['victimReady']+2)
 for line in log.splitlines():
  if line.startswith('MK2_HPHASE_'):
   pairs=re.findall(r'(\w+)=([^\s]+)',line);need(len(pairs)==len(dict(pairs)),'Unique actual phase fields');row=dict(pairs)
   if lo<=int(row['frame'])<=hi:rows[line.split()[0]].append(row)
 posts=rows['MK2_HPHASE_POST_FIELD']
 need({(int(r['frame']),int(r['slot']))for r in posts}=={(f,s)for f in range(lo,hi+1)for s in(1,2)},'Every actual body/shadow field from pre-entry through both true recoveries')
 streams=json.loads((FOLDER/'shadow_stream_memory_proofs.json').read_text())
 used={f'{r["graphic"]}_{r["width"]}_{r["height"]}_{r["command"]}'for r in rows['MK2_HPHASE_PROJECTION']}
 selected=[r for r in streams if r['stream']in used];need({r['stream']for r in selected}==used,'All complete actual unique finite-window ROM streams retained')
 b=dict(move='square',side=2,rows=rows,streams=selected,cpuLog=log)
 source=inspect.getsource(body.check)
 start=source.index(' # The older physical/ownership/health checker');end=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",start)
 before=source[start:end];need(source.count(before)==1,'One physical scope binding')
 source=source.replace(before," state=phase.verify(b['cpuLog'],guest,'kano')\n entry_frames={state['start']}\n",1)
 before='ids={side:identity,3-side:4}';need(source.count(before)==1,'Exact real CPU/human identity binding')
 source=source.replace(before,'ids={2:18,1:17}',1)
 namespace=dict(body.check.__globals__,phase=phase)
 exec(compile(source,__file__+'::entire_original_body_shadow_with_original_native_CPU_phase','exec'),namespace)
 check=namespace['check'];gfx=body.reconstruct(pins)
 actual=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo_code,hi_code in((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
  a,z=(lo_code-0xff800000)//8,(hi_code-0xff800000)//8
  need(guest[a:z]==actual[a:z],'Whole original native body/shadow kernels unchanged')
 case=check(b,guest,payload,gfx)
 faults=[]
 mutations=[('missing_entry_body','MK2_HPHASE_CANDIDATE','source','00000000'),
  ('shadow_owner','MK2_HPHASE_SHADOW_BEGIN','owner','01000000'),('shadow_ineligible','MK2_HPHASE_SHADOW_BEGIN','body','0002'),
  ('projection_shift','MK2_HPHASE_PROJECTION','dx','999'),('wrong_native_camera','MK2_HPHASE_PROJECTION','b4','00000000'),
  ('wrong_native_floor','MK2_HPHASE_PROJECTION','floor','999'),('wrong_shadow_x','MK2_HPHASE_SHADOW_DMA','x','999'),
  ('wrong_shadow_pen','MK2_HPHASE_SHADOW_DMA','color','0101'),('wrong_shadow_source','MK2_HPHASE_SHADOW_DMA','source','00000001')]
 for label,tag,key,value in mutations:
  changed=copy.deepcopy(b)
  index=next(i for i,r in enumerate(changed['rows'][tag])if int(r['frame'])==typed['start'])if label=='missing_entry_body'else 0
  need(changed['rows'][tag][index][key]!=value,'Actual fault changes a real observation');changed['rows'][tag][index][key]=value
  try:check(changed,guest,payload,gfx)
  except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual body/shadow corruption accepted: '+label)
 for label in('actual_rom_stream_wrong','packed_row_start_wrong'):
  changed=copy.deepcopy(b)
  if label=='actual_rom_stream_wrong':changed['streams'][0]['sha256']='0'*64
  else:changed['streams'][0]['actualRowStarts'][1]+=1
  try:check(changed,guest,payload,gfx)
  except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual ROM source corruption accepted: '+label)
 physical=[]
 dose=next(s for s in log.splitlines()if s.startswith('MK2_SQUARE_LOCK_HEALTH ')and 'before='in s)
 contact=next(s for s in log.splitlines()if s.startswith('MK2_SQUARE_BOUNDARY_EVENT ')and 'kind=hit_entry 'in s)
 cold=next(s for s in log.splitlines()if s.startswith('MK2_P2CPU_COLD_LIVE '))
 tests=[('wrong_actual_contact_damage',log.replace(dose,re.sub(r'after=\d+','after=1',dose),1)),
  ('missing_native_hit_entry',log.replace(contact+'\n','',1)),
  ('proxy_actual_cpu',log.replace(cold,re.sub(r'cpu_id=\d+','cpu_id=1',cold),1))]
 for label,text in tests:
  need(text!=log,'Physical corruption is a real change')
  try:
   phase.verify(text,guest,'kano');ledgers.health_ledger(text,guest,'kano');ledgers.state_ledgers(text,guest,'kano',round_by)
   cold_rows=ledgers.pair.rows_prefix(text,'MK2_P2CPU_COLD_LIVE ')
   need(len(cold_rows)==1 and cold_rows[0]['cpu_id']==18,'Actual natural CPU identity')
  except(AssertionError,ValueError)as error:physical.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual physical corruption accepted: '+label)
 for p in FOLDER.rglob('*'):
  if p.is_file():pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every final source/evidence pin unchanged')
 return dict(passed=True,candidate=current.NAME,phase=typed,health=health,stateLedger=state,case=case,
  finiteBodyShadowWindow=dict(first=lo,last=hi,fields=hi-lo+1,allFieldsFromPreEntryThroughBothRecoveries=True),
  actualSemanticFaultsRejected=faults,actualPhysicalFaultsRejected=physical,originalWholePhysicalTrajectoryUnchanged=True,
  fullNativeSquareHitPhaseBodyShadowAccepted=True,whole1800FieldNativeMatchStateHealthAccepted=True,
  currentWholeSceneEraseAccepted=False,allCPUContextsArenasKOOverlapArtAudioAccepted=False,fullPortAcceptance=False,
  rawGuestGFXRGBPCMOrWAVFilesWritten=0,newBuilds=0,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable current CPU acceptance')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','actualPhysicalFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
