"""Repeated current native morph body/shadow source and actual displayed previews.

Physical actions exactly replay the accepted current three-cycle fixture.
Finite selected transition/handoff windows, not full-scene erasure or art/audio
acceptance. Whole guest and all actual ROM/snapshot bytes remain only in RAM.
"""
import argparse,base64,copy,ctypes,hashlib,inspect,io,json,os,re,subprocess,traceback
from collections import defaultdict
from pathlib import Path
from PIL import Image,ImageDraw
import current_payload_metadata_context_v5229 as current
import verify_morph_adversity_v3235 as physical
import verify_special_shadow_v5141 as native
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_current_morph_shadow_ram_v5407.lua'
BASE=ROOT/'audit_v5408_current_morph_shadow_ram'
OUT=ROOT/'audit_v5409_current_morph_shadow_checked'
PARENT=ROOT/'audit_v5406_current_morph_adversity_progress/progress.json'

def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def prior_case(target,side):return ROOT/'audit_v5404_current_morph_adversity_ram'/f'{target}_p{side}_repeat_morph_added'
def windows(log):
 choices=physical.rows(log,'CHOICE');begins=physical.rows(log,'RESTORE_BEGIN');stores=physical.rows(log,'STORE')
 finish=[r for r in stores if r['id']==6]
 need(len(choices)==len(begins)==len(finish)==3,'Three independent physical native transition cycles')
 ranges=sorted([(r['frame']-2,r['frame']+36)for r in choices]+[(r['frame']-2,s['frame']+30)for r,s in zip(begins,finish)])
 previews=[choices[0]['frame']+i for i in(6,12,22)]+[begins[0]['frame']+i for i in(6,12,22)]
 return ranges,previews

def decode_stream(line,gfx):
 row=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(row.pop('hex'))
 g,m,c=int(row['graphic'],16),int(row['mapped'],16),int(row['command'],16);w,h=int(row['width']),int(row['height'])
 need(len(raw)==int(row['bytes'])and raw==bytes(gfx[m//8:m//8+len(raw)]),'Actual complete unique native sprite stream equals reconstructed compiled ROM')
 need((c>>12)&7==6,'Native fighter six-bit source stream')
 starts=[];headers=[];bit=m%8;origin=bit
 if c&128:
  for y in range(h):
   starts.append(g+bit-origin);need(bit+8<=len(raw)*8,'Complete actual packed row header')
   head=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&255;bit+=8
   pre=(head&15)<<((c>>8)&3);post=(head>>4)<<((c>>10)&3)
   need(pre+post<=w and bit+(w-pre-post)*6<=len(raw)*8,'Complete strictly compressed native row')
   headers.append(dict(row=y,pre=pre,post=post,pixels=w-pre-post));bit+=(w-pre-post)*6
 return dict(**row,sha256=hashlib.sha256(raw).hexdigest().upper(),actualRowStarts=starts,actualRowHeaders=headers,
  usedBits=bit-origin,streamFormat='compressed6'if c&128 else'stockRaw6',compressedRowStreamVerified=bool(c&128))

def bindings():
 # Keep every original descriptor/clip/cache/FIFO, packed-row, native world/
 # camera/floor, copy-pen and source-cadence predicate. Bind dynamic identity
 # and floor only to independent actual pre/post callback publications.
 source=inspect.getsource(native.check_body)
 changes={
  "num(t,'id')==num(t,'roster')==ids[s]":"num(t,'id')==b['pre'][f,s]['id']and num(t,'roster')==b['pre'][f,s]['roster']",
  "set(compositions)=={(f,s)for f in frames for s in(1,2)}":"set(compositions)=={(f,s)for f in b['frames']for s in(1,2)}"}
 for before,after in changes.items():need(source.count(before)==1,'Exact native body publication scope binding');source=source.replace(before,after,1)
 ns=dict(native.check_body.__globals__);exec(compile(source,__file__+'::entire_original_body_dynamic_native_morph_identity','exec'),ns);body=ns['check_body']
 source=inspect.getsource(native.check);start=source.index(" rows=b['rows'];");stop=source.index(" begins=rows[",start)
 source=source[:start]+""" rows=b['rows'];side=b['side'];state=b['physical'];entry_frames=set()
 fields=rows['MK2_HPHASE_POST_FIELD'];by={(num(t,'frame'),num(t,'slot')):t for t in fields};frames=b['frames']
 owners=b['owners'];ids={1:6 if side==1 else 17,2:6 if side==2 else 17};floors={}
 body_parts,published,clipped=check_body(b,guest,payload,frames,owners,ids)
"""+source[stop:]
 changes={"num(t,'id')==ids[s]":"num(t,'id')==b['post'][key]['id']",
  "num(t,'floor')==floors[s]":"num(t,'floor')==b['post'][f,s]['floor']",
  "if ids[s]in(17,18):own_copies+=len(copies)":"if num(t,'id')in(17,18):own_copies+=len(copies)"}
 for before,after in changes.items():need(source.count(before)==1,'Exact native shadow actual publication scope binding');source=source.replace(before,after,1)
 ns=dict(native.check.__globals__,check_body=body);exec(compile(source,__file__+'::entire_original_native_projection_dynamic_morph_floor','exec'),ns)
 return ns['check']

def context(log,streams,target,side,ranges):
 frames={f for a,z in ranges for f in range(a,z+1)};rows=defaultdict(list)
 for line in log.splitlines():
  if line.startswith('MK2_HPHASE_'):rows[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
 physical_result=physical.verify_log(log,target,side,'repeat_morph','added')
 pairs={(r['frame'],r['slot']):r for r in physical.rows(log,'PAIR')}
 pre={};post={}
 for tag,table,delta in(('PRE',pre,0),('POST',post,1)):
  for line in log.splitlines():
   if not line.startswith('MK2_MORPH_SHADOW_'+tag+' '):continue
   t=dict(re.findall(r'(\w+)=([^\s]+)',line));f,s=native.num(t,'frame'),native.num(t,'slot');r={k:native.num(t,k)for k in t if k not in('writes','assistance')}
   need((f,s)not in table and f in frames,'Unique real native callback publication in specified transition window')
   actual=pairs[f+delta,s]
   for k in('mode','actor','main','owner','pose','vx','vy','gravity','flags','body','trail','id','roster','state','hp','x','y','floor','action'):
    need(r[k]==actual[k],'Actual '+tag+' equals independent native morph physical publication: '+k)
   table[f,s]=r
   if tag=='POST':rows['MK2_HPHASE_POST_FIELD'].append(t)
  need(set(table)=={(f,s)for f in frames for s in(1,2)},'Every actual complete '+tag+' field in transition windows')
 owners={s:(pre[min(frames),s]['actor'],pre[min(frames),s]['main'])for s in(1,2)}
 return dict(move='morph',side=side,rows=rows,streams=streams,frames=frames,pre=pre,post=post,owners=owners,physical=physical_result)

def check_context(b,checker,guest,payload,gfx):
 for tag,table in(('MK2_HPHASE_CANDIDATE',b['pre']),('MK2_HPHASE_QUEUE',b['pre']),
  ('MK2_HPHASE_SHADOW_BEGIN',b['post']),('MK2_HPHASE_PROJECTION',b['post'])):
  for t in b['rows'][tag]:
   key=(native.num(t,'frame'),native.num(t,'slot'));need(key in table,'No off-window native body or shadow observation')
   r=table[key]
   for k in('actor','main','owner','id','pose','body'):
    need(native.num(t,k)==r[k],'Actual body/shadow phase binding to independent physical '+k)
   if tag=='MK2_HPHASE_PROJECTION':
    need(native.short(native.num(t,'world'))==r['x']and native.short(native.num(t,'world')>>16)==r['y']and
     native.num(t,'floor')==r['floor'],'Actual shadow world and ground belong to genuine current body')
 result=checker(b,guest,payload,gfx)
 result.update(actualNativeMorphBodyShadowWindowsAccepted=True,fullSceneEraseAndRGBReplayAccepted=False,
  actualObservedWindowFields=len(b['frames']),callbackPhaseIDsAndFloorsIndependentlyBound=True)
 return result

def capture(target,side):
 guest=current.expected();gfx=native.reconstruct({});payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['actualMatrixAccepted'],'Current complete physical morph matrix prerequisite')
 pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
 source_proof=json.loads((ROOT/'audit_v5142_special_shadow_ring_p1_checked/report.json').read_text())
 for file in(ROOT/'mk2ks_special_shadow_v5131.lua',Path(native.__file__),ROOT/'tools/verify_move_phase_shadow_v5089.py'):
  need(sha(file)==source_proof['inputHashes'][str(file.resolve())],'Qualified full original passive native source unchanged')
 for file in(LUA,Path(__file__).resolve(),Path(native.__file__),ROOT/'mk2ks_special_shadow_v5131.lua'):
  pins[str(file.resolve())]=sha(file)
 need(all(sha(p)==h for p,h in pins.items()),'Every authoritative source/evidence/public pin stable before capture')
 key=f'{target}_p{side}';prior=prior_case(target,side);old_log=(prior/'run.log').read_text();ranges,previews=windows(old_log)
 folder=BASE/key;need(not folder.exists(),'Fresh immutable native morph shadow fixture');folder.mkdir(parents=True)
 for name in('cfg','nvram','snap'):(folder/name).mkdir()
 save(folder/'input_hashes_before.json',pins)
 process=json.loads((prior/'process.json').read_text());command=[v.replace(str(prior),str(folder))for v in process['command']]
 command[command.index('-autoboot_script')+1]=str(LUA)
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(process['env']);env['MK2KS_MORPH_CAPTURE_OUT']=str(folder)
 env.update(MK2KS_MORPH_SHADOW_WINDOWS=','.join(f'{a}:{z}'for a,z in ranges),MK2KS_MORPH_SHADOW_PREVIEWS=','.join(map(str,previews)))
 captured=None;streams=[];images=[];rgb=[];errors=[]
 with(folder/'run.log').open('w',encoding='utf-8')as out,(folder/'stderr.log').open('w',encoding='utf-8')as err:
  proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
  save(folder/'process.json',dict(pid=proc.pid,command=command,env={k:v for k,v in env.items()if k.startswith('MK2KS_')}))
  print(key+' actual native body/shadow PID '+str(proc.pid),flush=True)
  for line in proc.stdout:
   try:
    if line.startswith('MK2_CURRENT_MORPH_GUEST '):
     raw=bytes.fromhex(re.search(r'hex=([0-9a-fA-F]+)',line)[1]);need(captured is None and raw==guest,'Whole actual guest equals current reconstructed source')
     captured=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper());out.write('MK2_CURRENT_MORPH_GUEST bytes=1048576 sha256='+captured['sha256']+'\n')
    elif line.startswith('MK2_HPHASE_PART '):
     stream=decode_stream(line,gfx);need(not any(s['stream']==stream['stream']for s in streams),'Unique actual source stream')
     streams.append(stream);out.write('MK2_HPHASE_PART_DIGEST stream='+stream['stream']+' sha256='+stream['sha256']+'\n')
    elif line.startswith('MK2_MORPH_SHADOW_RGB '):
     fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields['hex']);need(len(raw)==406400,'Complete native displayed snapshot in RAM')
     rgb.append(dict(frame=int(fields['frame']),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper()))
     images.append((int(fields['frame']),Image.frombytes('RGB',(400,254),raw,'raw','BGRX')))
     out.write('MK2_MORPH_SHADOW_RGB_DIGEST frame='+fields['frame']+' sha256='+rgb[-1]['sha256']+'\n')
    else:need('hex='not in line,'No unexpected raw media transport');out.write(line)
   except Exception as error:errors.append(repr(error))
  exit_code=proc.wait()
 log=(folder/'run.log').read_text();save(folder/'shadow_stream_memory_proofs.json',streams);save(folder/'displayed_rgb_memory_proofs.json',rgb)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(folder/'run.log')],capture_output=True).returncode==0,'Compress actual text trace')
 need(exit_code==0 and captured and not errors and not(folder/'stderr.log').read_text(),'Warning-free original native terminal with RAM buffers')
 select=lambda text:[s for s in text.splitlines()if s.startswith('MK2_HUMAN_SHANG_')]
 need(select(log)==select(old_log),'Entire genuine physical controller/state/health/choice/morph trajectory unchanged')
 need([r['frame']for r in rgb]==previews,'Every specified actual displayed preview received, no later substitution')
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for a,z in((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
  need(guest[(a-0xff800000)//8:(z-0xff800000)//8]==stock[(a-0xff800000)//8:(z-0xff800000)//8],'Original entire body/shadow instruction kernels unchanged')
 b=context(log,streams,target,side,ranges);checker=bindings();result=check_context(b,checker,guest,payload,gfx)
 faults=[]
 for tag,k,v in(('MK2_HPHASE_CANDIDATE','source','00000000'),('MK2_HPHASE_QUEUE','xy','00000000'),
  ('MK2_HPHASE_SHADOW_BEGIN','body','0002'),('MK2_HPHASE_PROJECTION','floor','999'),
  ('MK2_HPHASE_PROJECTION','world','00000000'),('MK2_HPHASE_PROJECTION','b4','00000000'),
  ('MK2_HPHASE_SHADOW_DMA','color','0101'),('MK2_HPHASE_SHADOW_DMA','source','00000001')):
  changed=copy.deepcopy(b);need(changed['rows'][tag][0][k]!=v,'Effective actual reached semantic fault');changed['rows'][tag][0][k]=v
  try:check_context(changed,checker,guest,payload,gfx)
  except ValueError as error:faults.append(dict(tag=tag,key=k,rejectedBy=str(error)))
  else:raise ValueError('Actual native source fault accepted')
 need(all(sha(p)==h for p,h in pins.items()),'Executed sources and public artifacts unchanged')
 for file in folder.rglob('*'):
  if file.is_file():pins[str(file.resolve())]=sha(file)
 proof=dict(passed=True,candidate=current.NAME,target=target,side=side,nativeExit=exit_code,nativePID=proc.pid,
  wholeGuestRAMProof=captured,ranges=ranges,case=result,actualSemanticFaultsRejected=faults,inputHashes=pins,
  originalEntirePhysicalTrajectoryUnchanged=True,newNativeBoots=1,newBuilds=0,rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,
  actualDisplayedSnapshots=len(rgb),fullSceneEraseAndRGBReplayAccepted=False,canonicalArtisticFidelityAccepted=False,fullPortAcceptance=False)
 report_folder=OUT/key;report_folder.mkdir(parents=True);save(report_folder/'report.json',proof)
 sheet=Image.new('RGB',(450,226));draw=ImageDraw.Draw(sheet)
 for i,(frame,image)in enumerate(images):
  x=(i%3)*150;y=(i//3)*113;sheet.paste(image.resize((150,95),Image.Resampling.NEAREST),(x,y+18));draw.text((x+2,y+2),f'{target} P{side} f{frame}',fill='white')
 png=io.BytesIO();sheet.save(png,format='PNG');print('MK2_NATIVE_MORPH_PREVIEW data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)
 print(json.dumps(dict(passed=True,target=target,side=side,windowFields=result['actualObservedWindowFields'],
  bodyParts=result['actualNativeBodyCandidates'],shadowCopies=result['actualSourceBoundShadowCopies'],actualFaultsRejected=len(faults))),flush=True)
 return proof

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--target',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:capture(args.target,args.side)
 except Exception as error:
  value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  path=OUT/f'{args.target}_p{args.side}';path.mkdir(parents=True,exist_ok=True)
  need(not(path/'report.json').exists(),'Never replace executed result');save(path/'report.json',value)
  print(json.dumps(value,indent=2),flush=True);raise SystemExit(1)
