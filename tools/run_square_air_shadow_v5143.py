"""Two physical signature-move cycles and ordinary follow-up; RAM-only native media."""
import argparse,base64,hashlib,io,json,os,re,subprocess,traceback
from pathlib import Path
from PIL import Image,ImageDraw
import native_subzero_legs_context_v4993 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
LUA=ROOT/'mk2ks_special_shadow_v5131.lua'
MOVES=('square',)

def capture(move,side,victim):
 folder=ROOT/f'audit_v5144_special_repeat_{move}_p{side}_{victim}'
 need(not folder.exists(),'Fresh physical repeated-special capture')
 guest=native.expected();gfx=native.expected_gfx();build=ROOT/native.NAME
 pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])
 for p in(LUA,Path(__file__),Path(native.__file__),build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata'):
  pins[str(p.resolve())]=sha(p)
 need(not re.search(r'(?:write_u|write_i|write_direct|write_logical|\.value\s*=(?!=)|screen:snapshot)',LUA.read_text()),'Only real physical inputs/read-only observations, no guest/media files')
 need(all(sha(p)==h for p,h in pins.items()),'Exact current isolated input set')
 folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,'Compress trace before capture')
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='1',MK2KS_HUMAN_SPECIAL_VICTIM=victim)
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(ROOT/'samples'),
  '-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none',
  '-noautoframeskip','-frameskip','0','-nothrottle','-str','100','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),
  '-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
 proof_guest=proof_gfx=None;scenes=[];preview=[];streams=[]
 with(folder/'stderr.log').open('w',encoding='utf-8')as err,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='strict')as process:
  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n')
  print(f'{move} P{side} versus {victim}:actual physical native pid={process.pid}',flush=True)
  with(folder/'run.log').open('w',encoding='utf-8')as log:
   for line in process.stdout:
    if line.startswith('MK2_HPHASE_PART '):

     f=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(f.pop('hex'))
     need(len(raw)==int(f['bytes']),'Complete actual unique shadow ROM stream')
     source,mapped,cmd=int(f['graphic'],16),int(f['mapped'],16),int(f['command'],16)
     width,height=int(f['width']),int(f['height'])
     need(mapped==(source-0x0a000000 if 0x10000000<=source<0x1a000000 else source),'Exact compiled imported-source rebasing')
     need((cmd>>12)&7==6 and (not 0x10000000<=source<0x1a000000 or cmd&128),'Strict six-bit source stream; all imported parts compressed')
     bit=mapped%8;origin=bit;starts=[];headers=[]
     if cmd&128:
      for y in range(height):
       starts.append(source+bit-origin)
       need(bit+8<=len(raw)*8,'Actual row header complete')
       header=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&255;bit+=8
       pre=(header&15)<<((cmd>>8)&3);post=(header>>4)<<((cmd>>10)&3)
       need(pre+post<=width and bit+(width-pre-post)*6<=len(raw)*8,'Actual compressed shadow row complete')
       headers.append(dict(row=y,pre=pre,post=post,pixels=width-pre-post));bit+=(width-pre-post)*6
     proof=dict(**f,sha256=hashlib.sha256(raw).hexdigest().upper(),actualRowStarts=starts,actualRowHeaders=headers,usedBits=bit-origin,
      streamFormat='compressed6'if cmd&128 else'stockRaw6',compressedRowStreamVerified=bool(cmd&128),rawGFXFilesWritten=0)
     need(not any(p['stream']==proof['stream']for p in streams),'Actual unique immutable GFXROM stream captured once')
     streams.append(proof);log.write('MK2_HPHASE_PART_DIGEST '+' '.join(k+'='+str(v)for k,v in f.items())+' sha256='+proof['sha256']+'\n')
    elif line.startswith(('MK2_HPHASE_GUEST ','MK2_HPHASE_GFX ','MK2_HPHASE_RGB ')):
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
      if f['attempt']=='1'and f['stage']=='phase_16': # One native full frame plus compact sheet.
       png=io.BytesIO();frame_image.save(png,format='PNG');print('MK2_SPECIAL_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)
      (folder/'rgb_memory_proofs.json').write_text(json.dumps(scenes,indent=2)+'\n')
     log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in f.items())+' sha256='+digest+'\n');log.flush()
    else:
     need('hex='not in line,'Never persist raw guest/GFX/RGB/audio buffers')
     log.write(line)
     if re.search(r'_(SELECT|LIVE|READY|COMMAND|RECOVERED|REPEAT_READY|FINAL|FAILED|RESULT) ',line):print(line.strip(),flush=True)
  native_exit=process.wait()
 (folder/'shadow_stream_memory_proofs.json').write_text(json.dumps(streams,indent=2)+'\n')
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
  actualUniqueShadowStreams=len(streams),bothPhysicalSpecialCyclesTransportPassed=True,rawGuestGFXRGBPCMOrWAVFilesWritten=0,fullPortAcceptance=False,
  completeSignatureMoveCoverageAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False)
 (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n');return meta

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=MOVES,required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True)
 parser.add_argument('--victim',choices=('kitana','sub_zero','kano','sonya'),default='kitana');args=parser.parse_args()
 out=ROOT/f'audit_v5145_special_repeat_{args.move}_p{args.side}_{args.victim}_observed';need(not out.exists(),'Fresh actual terminal report')
 try:report=capture(args.move,args.side,args.victim)
 except Exception as e:report=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compress compact terminal report')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)



