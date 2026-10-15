"""Actual old/new native RNG hardware reads/results; no altered RNG or AI choices."""
import json,re
from pathlib import Path
import verify_active_launch_timer_v1520 as source
import verify_repeated_sonya_cpu_v1463 as state
ROOT=source.ROOT;OUT=ROOT/'audit_v1545_native_rng_checked';need=source.need
HEX={'pc','mask','seed','a0','expected','actor','main','caller','value'}
def rows(log,tag):
 result=[]
 for line in log.splitlines():
  if not line.startswith('MK2_NATIVE_RNG_'+tag+' '):continue
  pairs=re.findall(r'(\w+)=([^\s]+)',line)
  need(len(pairs)==len({k for k,v in pairs}),'Unambiguous original RNG observation')
  result.append({k:v if k in ('seconds','assistance')else int(v,16 if k in HEX else 10)for k,v in pairs})
 return result
def verify_rng_log(log):
 reads,results,terminal=[rows(log,t)for t in('READ','RESULT','TERMINAL')]
 need(len(terminal)==1 and terminal[0]['calls']==len(reads)==len(results)>1000 and terminal[0]['pending']==0,'Complete native read/result/terminal pairs')
 need([q['index']for q in reads]==[q['index']for q in results]==list(range(1,len(reads)+1)),'Every original RNG call is independently paired')
 for a,b in zip(reads,results):
  need(a['pc']==0xff80ea90 and a['mask']==0xffff and b['pc']==0xff80eac0,'Actual original HCOUNT read and post-rotate native instruction')
  need(a['writes']==b['writes']==0 and a['assistance']==b['assistance']=='none','No observer guest/item writes or RNG assistance')
  need((a['frame'],a['actor'],a['main'])==(b['frame'],b['actor'],b['main'])and 0<=float(b['seconds'])-float(a['seconds'])<.001,'Same executing original actor/Main and native call')
  need(0<=a['hcount']<1024 and a['rotation']==(a['hcount']&31),'Actual hardware horizontal count and original modulo-32 shift')
  value=a['a0'];count=a['rotation']
  expected=((value<<count)|(value>>(32-count)))&0xffffffff if count else value
  need(a['expected']==b['value']==expected,'Every actual original RNG result exactly recomputes from its live operand and hardware HCOUNT')
 need(terminal[0]['writes']==0 and terminal[0]['assistance']=='none','Read-only terminal')
 return reads,results
def verify():
 pins={}
 def pin(p,wanted=None):
  p=Path(p);key=str(p.resolve())
  if key not in pins:pins[key]=source.sha(p)
  need(wanted is None or pins[key]==wanted,'Changed executed source/evidence '+key)
 proofpath=ROOT/'audit_v1542_native_rng_timing/report.json';proof=json.loads(proofpath.read_text());need(proof['passed']and proof['rngRotatesByNativeBeamPosition'],'Bound original RNG instruction and actual CPU IO mapping');pin(proofpath)
 for p,h in proof['inputHashes'].items():pin(p,h)
 cases={};all_reads={};all_results={};logs={}
 for key,candidate,baseline in [('previous','diagnostic_v1411_native_grab_audio','audit_v1539_previous_cpu_repeated_kano_p1'),('current',source.NAME,'audit_v1519_cpu_repeated_p1_human_kano')]:
  folder=ROOT/f'audit_v1544_native_rng_{key}';meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'));build=json.loads((ROOT/candidate/'build-info.json').read_text(encoding='utf-8-sig'))
  need(meta['exit_code']==0 and meta['candidate']==candidate and meta['executable_sha256']==build['executable_sha256']and meta['payload_sha256']==build['payload_sha256']and meta['player']=='kano'and meta['boot_frame']==605 and meta['confirm_age']==264 and meta['approach']=='guard_until_close'and not meta['cheats_enabled']and meta['assistance']=='none','Same real physical native cold inputs')
  need(before==meta['input_hashes']and all(before.get(p)==h for p,h in build['input_hashes'].items()),'Whole executed build/observer manifest')
  for p,h in before.items():pin(p,h)
  observer=(folder/'input_sources/mk2ks_cpu_native_rng_v1543.lua').read_text()
  need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|set_value\(',observer),'Observer adds no physical inputs, native writes or forced RNG')
  need(observer.count("dofile('mk2ks_cpu_pair_display_probe_v1459.lua')")==1,'Unchanged actual human scenario')
  guest=source.sound.prior.expected_guest()[0]if key=='previous'else source.expected_guest()[0]
  need((folder/'guest_maincpu.bin').read_bytes()==guest,'Every actual guest byte independently exact')
  log=(folder/'run.log').read_text(encoding='utf-8-sig');need(not re.search('LUA ERROR|fatal error|access violation|stack traceback',log,re.I),'No emulator/observer failure');logs[key]=log
  all_reads[key],all_results[key]=verify_rng_log(log)
  old=(ROOT/baseline/'run.log').read_text(encoding='utf-8-sig');pin(ROOT/baseline/'run.log')
  events=lambda text:[q for q in text.splitlines()if q.startswith('MK2_CPU_PAIR_')or q.startswith('MK2_P1CPU_')]
  need(events(log)==events(old),'Every actual CPU/control field matches the original capture: observer cannot change native behavior')
  result=state.rows(log,'RESULT')[0]
  cases[key]=dict(candidate=candidate,nativeRNGCalls=len(all_reads[key]),everyActualRotationRecomputed=True,priorWholeNativeCPUEventStreamExact=True,completePairCount=result['complete_count'])
  for p in folder.rglob('*'):
   if p.is_file():pin(p)
 a,b=all_reads['previous'],all_reads['current'];ra,rb=all_results['previous'],all_results['current']
 common=min(len(a),len(b));different=None
 for i in range(common):
  keys=set(a[i])-{'seconds','expected','rotation','hcount'}
  if any(a[i][k]!=b[i][k]for k in keys)or a[i]['hcount']!=b[i]['hcount']:
   different=i;break
 need(different is not None,'Actually locate first old/new RNG input divergence')
 i=different;keys=set(a[i])-{'seconds','expected','rotation','hcount'}
 same_operand=all(a[i][k]==b[i][k]for k in keys)
 hardware_changed=a[i]['hcount']!=b[i]['hcount'];result_changed=ra[i]['value']!=rb[i]['value']
 pin(__file__)
 corruptions=[]
 original=logs['current']
 for label,text in [('wrong_mask',original.replace('mask=FFFF seed=','mask=00FF seed=')),('missing_reads','\n'.join(q for q in original.splitlines()if not q.startswith('MK2_NATIVE_RNG_READ '))),('missing_results','\n'.join(q for q in original.splitlines()if not q.startswith('MK2_NATIVE_RNG_RESULT '))),('wrong_result',re.sub(r'(MK2_NATIVE_RNG_RESULT[^\n]*value=)[0-9A-F]+',r'\g<1>00000000',original)),('observer_writes',original.replace('writes=0 assistance=none','writes=1 assistance=none'))]:
  need(text!=original,'Effective in-memory corruption')
  try:verify_rng_log(text)
  except ValueError as error:corruptions.append(dict(mutation=label,rejected=True,reason=str(error)))
  else:raise ValueError('Accepted RNG corruption '+label)
 return dict(passed=True,cases=cases,firstRNGDivergence=dict(index=a[i]['index'],previous=a[i],current=b[i],previousActualResult=ra[i],currentActualResult=rb[i]),sameFirstDivergentNativeOperandAndContext=same_operand,firstDivergentHardwareCountChanged=hardware_changed,firstDivergentActualResultChanged=result_changed,actualNativeRNGTimingDifferenceObserved=same_operand and hardware_changed and result_changed,inputHashes=pins,counterexamples=corruptions,allLaterAIChangesCausallyProven=False,repeatedCurrentCPUAccepted=False,fullAIRepertoireAccepted=False,fullPortAccepted=False,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Never overwrite evidence')
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report.get(k)for k in ('passed','error','cases','firstRNGDivergence','actualNativeRNGTimingDifferenceObserved')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
