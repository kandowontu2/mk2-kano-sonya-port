"""Two physical signature-move cycles and ordinary follow-up; RAM-only native media."""
import argparse,base64,hashlib,io,json,os,re,subprocess,traceback
from pathlib import Path
from PIL import Image,ImageDraw
import native_subzero_legs_context_v4993 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
LUA=ROOT/'mk2ks_special_repeat_v5099.lua'
MOVES=('knife','ball','blade','choke','ring','square','bicycle','leg')

def capture(move,side,victim):
 folder=ROOT/f'audit_v5102_special_repeat_{move}_p{side}_{victim}'
 need(not folder.exists(),'Fresh physical repeated-special capture')
 guest=native.expected();gfx=native.expected_gfx();build=ROOT/native.NAME
 pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])
 for p in(LUA,Path(__file__),Path(native.__file__),build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata'):
  pins[str(p.resolve())]=sha(p)
 need(not re.search(r'(?:write_u|write_i|write_direct|write_logical|\.value\s*=(?!=)|screen:snapshot)',LUA.read_text()),'Only real physical inputs/read-only observations, no guest/media files')
 need(all(sha(p)==h for p,h in pins.items()),'Exact current isolated input set')
 folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,'Compress trace before capture')
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM=victim)
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(ROOT/'samples'),
  '-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none',
  '-noautoframeskip','-frameskip','0','-nothrottle','-str','100','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),
  '-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
 proof_guest=proof_gfx=None;scenes=[];preview=[]
 with(folder/'stderr.log').open('w',encoding='utf-8')as err,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='strict')as process:
  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n')
  print(f'{move} P{side} versus {victim}:actual physical native pid={process.pid}',flush=True)
  with(folder/'run.log').open('w',encoding='utf-8')as log:
   for line in process.stdout:
    if line.startswith(('MK2_HPHASE_GUEST ','MK2_HPHASE_GFX ','MK2_HPHASE_RGB ')):
     f=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(f.pop('hex'));digest=hashlib.sha256(raw).hexdigest().upper();tag=line.split()[0]
     if tag.endswith('_GUEST'):
      need(proof_guest is None and f==dict(frame='1',bytes='1048576')and raw==guest,'Every actual initialized guest byte matches independent reconstruction')
      proof_guest=dict(bytes=len(raw),sha256=digest,executableSHA256=native.EXE_SHA,everyActualByteComparedInRAM=True,rawGuestFilesWritten=0)
      (folder/'guest_memory_proof.json').write_text(json.dumps(proof_guest,indent=2)+'\n')
     elif tag.endswith('_GFX'):
      need(proof_gfx is None and f==dict(frame='1',bytes='18976')and raw==gfx,'Every actual owned appended GFX byte matches current constructor data')
      proof_gfx=dict(bytes=len(raw),sha256=digest,everyActualByteComparedInRAM=True)
      (folder/'gfx_memory_proof.json').write_text(json.dumps(proof_gfx,indent=2)+'\n')
     else:
      need(len(raw)==406400 and f['width']=='400'and f['height']=='254'and f['bytes']=='406400','Actual entire400x254native RGB field')
      scene=dict(stage=f['stage'],attempt=int(f['attempt']),frame=int(f['frame']),width=400,height=254,bytes=len(raw),sha256=digest,rawMediaFilesWritten=0)
      scenes.append(scene);frame_image=Image.frombytes('RGB',(400,254),raw,'raw','BGRX');preview.append((f['attempt']+'_'+f['stage'],frame_image))
      if False: # Contact sheet only; avoid redundant full-frame transport previews.
       png=io.BytesIO();frame_image.save(png,format='PNG');print('MK2_SPECIAL_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)
      (folder/'rgb_memory_proofs.json').write_text(json.dumps(scenes,indent=2)+'\n')
     log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in f.items())+' sha256='+digest+'\n');log.flush()
    else:
     need('hex='not in line,'Never persist raw guest/GFX/RGB/audio buffers')
     log.write(line)
     if re.search(r'_(SELECT|LIVE|READY|COMMAND|RECOVERED|REPEAT_READY|FINAL|FAILED|RESULT) ',line):print(line.strip(),flush=True)
  native_exit=process.wait()
 log=(folder/'run.log').read_text();err=(folder/'stderr.log').read_text()
 need(native_exit==0 and proof_guest and proof_gfx and all(sha(p)==h for p,h in pins.items()),'Actual successful terminal native boot and immutable inputs')
 need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|MK2_HSPECIAL_FAILED',log+err,re.I),'No native/observer/action/recovery failure')
 results=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_HSPECIAL_RESULT ')]
 need(len(results)==1 and results[0]['completed']=='2'and results[0]['attempt']=='2','Both true physical move activations and complete recovery/follow-up')
 need(len(scenes)>=9 and all(any(s['attempt']==i and s['stage']==stage for s in scenes)for i in(1,2)for stage in('special_before','entry','special_recovered')),
      'Actual own before/entry/recovery RGB captured for both cycles')
 sheet=Image.new('RGB',(600,113*((len(preview)+3)//4)),'black');draw=ImageDraw.Draw(sheet)
 for i,(label,frame_image)in enumerate(preview):
  x=(i%4)*150;y=(i//4)*113;draw.text((x+2,y+2),label,fill='white');sheet.paste(frame_image.resize((150,95),Image.Resampling.NEAREST),(x,y+18))
 png=io.BytesIO();sheet.save(png,format='PNG');print('MK2_SPECIAL_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)
 meta=dict(passed=True,nativeExit=native_exit,move=move,side=side,victim=victim,candidate=native.NAME,executableSHA256=native.EXE_SHA,
  guestSHA256=native.GUEST_SHA,payloadSHA256=native.PAYLOAD_SHA,inputHashes=pins,actualScenes=scenes,terminalResult=results[0],
  bothPhysicalSpecialCyclesTransportPassed=True,rawGuestGFXRGBPCMOrWAVFilesWritten=0,fullPortAcceptance=False,
  completeSignatureMoveCoverageAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False)
 (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n');return meta

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=MOVES,required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True)
 parser.add_argument('--victim',choices=('kitana','sub_zero','kano','sonya'),default='kitana');args=parser.parse_args()
 out=ROOT/f'audit_v5103_special_repeat_{args.move}_p{args.side}_{args.victim}_observed';need(not out.exists(),'Fresh actual terminal report')
 try:report=capture(args.move,args.side,args.victim)
 except Exception as e:report=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compress compact terminal report')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)

