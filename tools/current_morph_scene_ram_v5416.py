"""Complete current three-cycle morph scene operation sequence; RAM comparisons.

One actual initial VRAM base only. Every native operation between first morph
and final return is retained, including the full 512-field timers. Dense actual
targets at all six transition/handoff windows; no later target seeds replay.
Not universal artistic, arena, audio, finisher or full-port acceptance.
"""
import argparse,collections,hashlib,inspect,json,os,re,subprocess,traceback
from pathlib import Path
import numpy as np
import current_payload_metadata_context_v5229 as current
import current_morph_shadow_ram_v5407 as morph
import current_cpu_scene_ram_contract_v5357 as original
import current_cpu_scene_ram_contract_v5363 as hud
import current_cpu_ko_round_scene_contract_v5382 as replay
import current_tomb_ram_model_v3642 as transport
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_current_morph_scene_ram_v5416.lua'
BASE=ROOT/'audit_v5417_current_morph_scene_ram'
OUT=ROOT/'audit_v5418_current_morph_scene_checked'
PARENT=ROOT/'audit_v5415_current_morph_shadow_progress/progress.json'

def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')

def scene_verify(folder,ram,log,guest,pins,targets):
 source=inspect.getsource(original.verify)
 changes={
  'image=graphics.reconstruct(pins);payload=':'image=patch_hud(graphics.reconstruct(pins),pins);payload=',
  "len(snaps)==70 and [r['frame']for r in snaps]==list(range(2279,2349))":
   "len(snaps)==len(expected_targets)and [r['frame']for r in snaps]==expected_targets"}
 for before,after in changes.items():need(source.count(before)==1,'Exact whole source-bound replay plus actual morph target scope');source=source.replace(before,after,1)
 ns=dict(original.verify.__globals__,patch_hud=hud.patch_hud,replay_binding=replay.replay_binding,expected_targets=targets,__file__=__file__)
 exec(compile(source,__file__+'::entire_original_native_graphics_ops_shift_and_actual_RGB','exec'),ns)
 return ns['verify'](folder,ram,log,guest,pins)

def publication_bindings(log,prior,ranges):
 groups,_,_,_,_=original.parser(log);number=morph.native.num
 sample_set={f for a,z in ranges for f in range(a,z+1)}
 def selected(text,prefix):
  records=[]
  for line in text.splitlines():
   if line.startswith(prefix):
    r=dict(re.findall(r'(\w+)=([^\s]+)',line))
    if int(r['frame'])in sample_set:records.append(r)
  return records
 # This complementary actual native run must retain the complete previously
 # proven actor/cache/FIFO and shadow hardware stream, not only buttons/HP.
 old=(prior/'run.log').read_text()
 fields=('frame','slot','actor','main','owner','id','roster','pose','facing','body','cache','part','row','source','size','xy','command')
 for current_tag,old_tag in(('MK2_NAT_CAMPAIGN_FLOOR_CANDIDATE ','MK2_HPHASE_CANDIDATE '),('MK2_NAT_CAMPAIGN_FLOOR_QUEUE ','MK2_HPHASE_QUEUE ')):
  fresh=selected(log,current_tag);known=selected(old,old_tag)
  keys=lambda rows:[tuple(number(r,k)for k in fields)for r in rows]
  need(keys(fresh)==keys(known),'Entire actual previously proven native composite/cache/FIFO chronology unchanged')
 # Every observed eligible native shadow row copy was already independently
 # source/geometry/cadence qualified; bind it to actual full-scene hardware.
 keys=('frame','source','command','x','y','width','height','pc')
 old_shadow=selected(old,'MK2_HPHASE_SHADOW_DMA ')
 shadow=collections.Counter(tuple(number(r,k)for k in keys)for r in old_shadow)
 scene=collections.Counter(tuple(r[k]for k in keys)for r in groups['FLOOR_DMA']if r['frame']in sample_set and r['pc']in(0xff8015a0,0xff801610))
 need(shadow==scene,'Every original actual native floor-shadow row copy equals full-scene hardware')
 return dict(completeNativeBodyFIFOChronologyMatchesPrior=True,entireNativeShadowHardwareStreamMatchesPrior=True,actualShadowHardwareCopies=sum(shadow.values()))

def run(target,side):
 guest=current.expected();parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Completed repeated morph body/source/native shadow prerequisite')
 pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
 qualified_path=ROOT/'audit_v3282_current_cpu_square_render_erase_checked/report.json';qualified=json.loads(qualified_path.read_text())
 source=ROOT/'mk2ks_physical_p2_cpu_square_display_v2039.lua'
 need(qualified['passed']and sha(source)==qualified['inputHashes'][str(source.resolve())],'Original full native scene observer previously qualified unchanged')
 for p in(LUA,Path(__file__).resolve(),source,ROOT/'mk2ks_native_tomb_ram_v3624.lua',qualified_path,
  Path(original.__file__),Path(hud.__file__),Path(replay.__file__),Path(transport.__file__),
  *(ROOT/'mame-mkp/src/devices/cpu/tms34010'/name for name in('34010gfx.hxx','34010ops.hxx'))):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All retained authoritative native/source/public evidence stable before capture')
 prior=morph.prior_case(target,side);old_log=(prior/'run.log').read_text();ranges,_=morph.windows(old_log)
 targets=sorted({f for a,z in ranges for f in range(a,z+1)});first,last=targets[0]-1,targets[-1]
 key=f'{target}_p{side}';folder=BASE/key;need(not folder.exists(),'Fresh immutable full native morph scene');folder.mkdir(parents=True)
 for name in('cfg','nvram','snap'):(folder/name).mkdir()
 save(folder/'input_hashes_before.json',pins)
 process=json.loads((prior/'process.json').read_text());command=[value.replace(str(prior),str(folder))for value in process['command']]
 command[command.index('-autoboot_script')+1]=str(LUA);command[command.index('-snapsize')+1]='400x254'
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(process['env']);env['MK2KS_MORPH_CAPTURE_OUT']=str(folder)
 env.update(MK2KS_FLOOR_OUT=str(folder),MK2KS_MORPH_SCENE_FIRST=str(first),MK2KS_MORPH_SCENE_LAST=str(last),
  MK2KS_MORPH_SCENE_TARGETS=','.join(f'{a}:{z}'for a,z in ranges))
 ram={};proofs=[];memory_log=[];decoder=transport.Transport();errors=[];primary_guest=False
 with(folder/'stderr.log').open('w',encoding='utf-8')as err,(folder/'run.log').open('w',encoding='utf-8')as out:
  proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
  save(folder/'process.json',dict(pid=proc.pid,command=command,env={k:v for k,v in env.items()if k.startswith('MK2KS_')}))
  print(key+' actual complete native scene PID '+str(proc.pid),flush=True)
  for line in proc.stdout:
   try:
    if line.startswith(('MK2_TOMB_RAM_BUFFER ','MK2_TOMB_RAM_PIXELS ')):
     row=dict(re.findall(r'(\w+)=([^\s]+)',line));encoded=next(proc.stdout).strip();label=row['file']
     if line.startswith('MK2_TOMB_RAM_BUFFER '):raw=decoder.decode(row,encoded)
     else:
      need(row['encoding']=='u32le_numeric_hex'and row['width']=='400'and row['height']=='254'and len(encoded)==406400*2,'Whole original native displayed snapshot')
      raw=np.frombuffer(bytes.fromhex(encoded),dtype='>u4').astype('<u4').tobytes()
     need(label not in ram and len(raw)==int(row['bytes']),'Unique complete actual RAM buffer')
     if label=='guest_maincpu.bin':need(raw==guest,'Entire initialized actual guest equals independent current source')
     ram[label]=raw;proof=dict(file=label,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper());proofs.append(proof)
     out.write('MK2_MORPH_SCENE_RAM_DIGEST '+' '.join(k+'='+str(v)for k,v in proof.items())+'\n')
    elif line.startswith('MK2_CURRENT_MORPH_GUEST '):
     raw=bytes.fromhex(re.search(r'hex=([0-9a-fA-F]+)',line)[1]);need(not primary_guest and raw==guest,'Entire original physical observer guest identical');primary_guest=True
     out.write('MK2_CURRENT_MORPH_GUEST bytes=1048576 sha256='+current.GUEST_SHA+'\n')
    elif line.startswith('MK2_NAT_CAMPAIGN_FLOOR_GFX '):
     memory_log.append(line);row=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(row.pop('data'))
     need(len(raw)==int(row['bytes']),'Complete actual native scene ROM stream');row['sha256']=hashlib.sha256(raw).hexdigest().upper()
     out.write('MK2_MORPH_SCENE_GFX_DIGEST '+' '.join(k+'='+v for k,v in row.items())+'\n')
    else:
     need('hex='not in line,'Never persist raw guest or media');memory_log.append(line);out.write(line)
     if line.startswith(('MK2_HUMAN_SHANG_RESULT ','MK2_NAT_CAMPAIGN_FLOOR_RESULT ')):print(line.strip(),flush=True)
   except Exception as error:errors.append(repr(error))
  code=proc.wait()
 save(folder/'ram_buffer_proofs.json',proofs)
 before=sha(folder/'run.log');need(subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(folder/'run.log')],capture_output=True).returncode==0 and sha(folder/'run.log')==before,'Exact native text LZX compressed')
 log=''.join(memory_log)
 manifest=dict(exit_code=code,candidate=current.NAME,assistance='none',cheats_enabled=False,input_hashes=pins,
  mediaTransport='Original names label RAM buffers only; no raw media files',rawMediaFilesWritten=0)
 save(folder/'result.json',manifest)
 need(code==0 and primary_guest and ram.get('guest_maincpu.bin')==guest and not errors and not(folder/'stderr.log').read_text(),
  'Warning-free terminal native capture and every complete actual buffer')
 select=lambda text:[s for s in text.splitlines()if s.startswith('MK2_HUMAN_SHANG_')]
 need(select(log)==select(old_log),'Entire current actual physical inputs/state/health/ID stores and choices unchanged')
 state=morph.physical.verify_log(log,target,side,'repeat_morph','added')
 print(key+' native terminal; verifying every operation and '+str(len(targets))+' full displayed frames',flush=True)
 proof=scene_verify(folder,ram,log,guest,pins,targets)
 groups,_,_,_,_=original.parser(log);pairs={(r['frame'],r['slot']):r for r in morph.physical.rows(log,'PAIR')}
 states=groups['FLOOR_STATE'];need([r['frame']for r in states]==list(range(first,last+1)),'Every intervening native timer field observed, including unsampled scanout periods')
 for r in states:
  f=r['frame']
  for slot in(1,2):
   actual=pairs[f+1,slot]
   for key0,field in(('p','actor'),('main','main'),('roster','roster'),('state','state'),('health','hp')):
    need(r[f'{key0}{slot}']==actual[field],'Every frame_done native identity/controller/health field equals independent next pre-CPU publication')
   need(r['mode']==actual['mode']==2,'Every actual repeated morph timer remains playable')
 binding=publication_bindings(log,ROOT/'audit_v5412_current_morph_shadow_ram'/key,ranges)
 for p in folder.rglob('*'):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actual source/evidence/native public bytes stable at completed replay')
 proof.update(candidate=current.NAME,target=target,side=side,nativePID=proc.pid,nativeExit=code,physical=state,
  fullInterveningNativeTimerFields=len(states),denseActualDisplayedTargets=len(targets),actualRAMBuffers=len(ram),
  actualRawBufferBytesOnlyInRAM=sum(len(raw)for raw in ram.values()),nativeBodyShadowHardwareBinding=binding,
  oneActualInitialBaseAcrossAllThreeMorphCycles=True,wholeSceneOperationSequenceAcrossThreeTimersAccepted=True,
  actualPhysicalTrajectoryUnchanged=True,newNativeBoots=1,newBuilds=0,rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,inputHashes=pins)
 return proof

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--target',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);a=parser.parse_args()
 path=OUT/f'{a.target}_p{a.side}';need(not path.exists(),'Fresh immutable whole scene proof')
 try:report=run(a.target,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 path.mkdir(parents=True);save(path/'report.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','continuous','fullRAMRGBBindings','physical')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
