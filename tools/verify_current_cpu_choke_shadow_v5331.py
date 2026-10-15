"""Finite current CPU Kano mirror/cross choke: native phase/body/floor shadows."""
import argparse,copy,inspect,json,re,subprocess,traceback
from collections import defaultdict
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_special_shadow_v5141 as body
import verify_current_kano_physical_p2_cpu_v1941 as cpu
ROOT,need,sha=current.ROOT,current.need,current.sha

def substitute(text,before,after):
 need(text.count(before)==1,'Single source-bound adaptation: '+before[:100])
 return text.replace(before,after,1)

def bindings(human):
 source=inspect.getsource(body.load)
 source=substitute(source,'audit_v5134_special_repeat_{move}_p{side}_kitana',f'audit_v5329_current_cpu_kano_choke_human_{human}')
 source=substitute(source,'audit_v5135_special_repeat_{move}_p{side}_kitana_observed',f'audit_v5330_current_cpu_kano_choke_human_{human}_observed')
 namespace=dict(body.load.__globals__)
 exec(compile(source,__file__+'::entire_original_capture_loader','exec'),namespace)
 load=namespace['load']
 source=inspect.getsource(body.check)
 first=source.index(' # The older physical/ownership/health checker');last=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",first)
 source=substitute(source,source[first:last],
  " state=cpu.verify_log(b['cpuLog'],b['human'],guest)\n entry_frames={r['frame']for r in cpu.original.rows(b['cpuLog'],'ENTRY')}\n")
 source=substitute(source,'ids={side:identity,3-side:4}','ids={2:17,1:cpu.original.HUMANS[b["human"]]}')
 namespace=dict(body.check.__globals__,cpu=cpu)
 exec(compile(source,__file__+'::entire_original_native_body_shadow_with_actual_CPU_physical_gate','exec'),namespace)
 return load,namespace['check']

def run(human):
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in[(0xff801070,0xff8017b0),(0xff804160,0xff804430)]:
  need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==original[(lo-0xff800000)//8:(hi-0xff800000)//8],
       'Entire original body/direct-shadow kernels unchanged')
 baseline_path=ROOT/'audit_v5142_special_shadow_ring_p1_checked/report.json';baseline=json.loads(baseline_path.read_text())
 cpu_path=ROOT/'audit_v2880_native_cpu_start_inventory_checked/report.json';prior=json.loads(cpu_path.read_text())
 need(baseline['passed']and prior['passed'],'Full original accepted body/shadow and natural CPU sources')
 for p in(Path(body.__file__),ROOT/'tools/verify_move_phase_shadow_v5089.py'):
  need(sha(p)==baseline['inputHashes'][str(p.resolve())],'Entire original body/shadow model unchanged')
 for p in(Path(cpu.__file__),Path(cpu.original.__file__)):
  need(sha(p)==prior['inputHashes'][str(p.resolve())],'Entire original CPU native phase/cleanup/ordinary gate unchanged')
 pins={str(Path(__file__).resolve()):sha(__file__),str(baseline_path):sha(baseline_path),str(cpu_path):sha(cpu_path)}
 old=ROOT/'diagnostic_v4992_native_subzero_legs';new=ROOT/current.NAME;rel='input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 def gfx_declaration(text):return text.split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0].split('ROM_REGION( 0x2000000, "gfxrom", ROMREGION_ERASE00 )',1)[1]
 need(gfx_declaration((old/rel).read_text())==gfx_declaration((new/rel).read_text()),'Entire current compiled graphics lane inventory unchanged')
 pins[str(new/rel)]=sha(new/rel);gfx=body.reconstruct(pins)
 load,check=bindings(human);b=load('choke',2);b['human']=human;b['cpuLog']=(b['folder']/'run.log').read_text()
 need(b['report']['passed']and b['report']['nativeExit']==0 and b['report']['candidate']==current.NAME,'Actual current native terminal capture')
 boot=605 if human=='kano'else 606
 previous=ROOT/f'audit_v{2873 if human=="kano"else 2876}_native_cpu_human_{human}_boot{boot}/run.log'
 selected=lambda text:[s for s in text.splitlines()if s.startswith(('MK2_CPU_PAIR_','MK2_P2CPU_'))]
 need(selected(b['cpuLog'])==selected(previous.read_text(encoding='utf-8-sig')),'Entire actual native input/state/health/ordinary continuation exactly matches original accepted cold CPU case')
 case=check(b,guest,payload,gfx)
 need(case['state']['originalContract']['target']=='kano'and case['state']['originalContract']['CPU_slot']==2,
      'Actual true CPU Kano owns complete choke and independent ordinary follow-up')
 need(case['actualRoutineEntryFrames']and all(any(body.num(t,'frame')==f for t in b['rows']['MK2_HPHASE_CANDIDATE'])for f in case['actualRoutineEntryFrames']),
      'Every actual choke entry has unfiltered native body publication')
 faults=[]
 mutations=[('missing_entry_body','MK2_HPHASE_CANDIDATE','source','00000000'),
  ('shadow_owner','MK2_HPHASE_SHADOW_BEGIN','owner','01000000'),('shadow_ineligible','MK2_HPHASE_SHADOW_BEGIN','body','0002'),
  ('projection_shift','MK2_HPHASE_PROJECTION','dx','999'),('wrong_native_camera','MK2_HPHASE_PROJECTION','b4','00000000'),
  ('wrong_native_floor','MK2_HPHASE_PROJECTION','floor','999'),('wrong_shadow_x','MK2_HPHASE_SHADOW_DMA','x','999'),
  ('wrong_shadow_pen','MK2_HPHASE_SHADOW_DMA','color','0101'),('wrong_shadow_source','MK2_HPHASE_SHADOW_DMA','source','00000001')]
 for label,tag,key,value in mutations:
  changed=copy.deepcopy(b)
  index=next(i for i,t in enumerate(changed['rows'][tag])if body.num(t,'frame')in case['actualRoutineEntryFrames'])if label=='missing_entry_body'else 0
  need(changed['rows'][tag][index][key]!=value,'Actual mutation is not no-op');changed['rows'][tag][index][key]=value
  try:check(changed,guest,payload,gfx)
  except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual source/semantic mutation accepted: '+label)
 for label in('actual_rom_stream_wrong','packed_row_start_wrong'):
  changed=copy.deepcopy(b)
  if label=='actual_rom_stream_wrong':changed['streams'][0]['sha256']='0'*64
  else:changed['streams'][0]['actualRowStarts'][1]+=1
  try:check(changed,guest,payload,gfx)
  except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual source-stream mutation accepted: '+label)
 # Real observations mutated while retaining well-formed syntax and present keys.
 physical_faults=[]
 log=b['cpuLog'];lines=log.splitlines()
 step=next(s for s in lines if s.startswith('MK2_CPU_PAIR_EVENT ')and 'kind=step 'in s)
 regain=next(s for s in lines if s.startswith('MK2_CPU_PAIR_OWN_REGAIN '))
 cold=next(s for s in lines if s.startswith('MK2_P2CPU_COLD_LIVE '))
 dose=next(s for s in lines if s.startswith('MK2_CPU_PAIR_HEALTH ')and
           int(re.search(r'before=(\d+)',s)[1])-int(re.search(r'after=(\d+)',s)[1])==8)
 corrupted=[('native_pair_step_missing',log.replace(step+'\n','',1)),
  ('proxy_selected_human',log.replace(cold,re.sub(r'human_id=\d+','human_id=1',cold),1)),
  ('stale_cpu_recovery_body',log.replace(regain,re.sub(r'(?<!\w)body=\w+','body=00000016',regain),1)),
  ('wrong_choke_damage',log.replace(dose,re.sub(r'after=\d+','after=1',dose),1))]
 for label,text in corrupted:
  need(text!=log,'Actual physical mutation changes observed evidence')
  try:cpu.verify_log(text,human,guest)
  except AssertionError as error:physical_faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual native physical fault accepted: '+label)
 for p,h in b['report']['inputHashes'].items():need(sha(p)==h,'Every actual executed input unchanged');pins[p]=h
 for p in[previous,b['report_path'],Path(cpu.__file__),Path(cpu.original.__file__),Path(body.__file__),*(p for p in b['folder'].rglob('*')if p.is_file())]:pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All source/evidence/runtime bytes stable')
 return dict(passed=True,candidate=current.NAME,case=case,physicalHuman=human,actualNativeCPU=17,actualHumanID=cpu.original.HUMANS[human],
  entireOriginalCPUNativePairOrdinaryPhysicalContractRetained=True,entireOriginalBodyShadowSemanticsRetained=True,
  actualSemanticFaultsRejected=faults,actualPhysicalFaultsRejected=physical_faults,actualColdTrajectoryUnchanged=True,
  wholeCurrentGuestIndependentlyReconstructed=True,currentFiniteCPUChokeBodyNativeShadowsAndCleanupVerified=True,
  rawGuestGFXRGBPCMOrWAVFilesWritten=0,newBuilds=0,inputHashes=pins,
  allCPUContextsArenasKOOverlapArtAudioAccepted=False,fullArtAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--human',choices=('kano','sonya'),required=True);a=parser.parse_args()
 out=ROOT/f'audit_v5332_current_cpu_kano_choke_human_{a.human}_checked';need(not out.exists(),'Fresh immutable CPU proof')
 try:report=run(a.human)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True)
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','actualPhysicalFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
