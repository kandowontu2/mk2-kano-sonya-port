"""Actual earned finisher native branches and RAM-only scenes; no full-port claim."""
import argparse,base64,hashlib,io,json,os,re,subprocess,traceback
from pathlib import Path
from PIL import Image
import native_subzero_legs_context_v4993 as native

ROOT,need,sha=native.ROOT,native.need,native.sha
LUA='mk2ks_native_subzero_legs_nextmatch_v5000.lua'

def capture(fighter,side):
 folder=ROOT/f'audit_v5008_subzero_{fighter}_p{side}_lifecycle'
 need(not folder.exists(),'Fresh actual lifecycle leaf')
 guest=native.expected();gfx=native.expected_gfx()
 build=ROOT/native.NAME
 pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])
 controllers=[ROOT/name for name in(LUA,'mk2ks_native_subzero_legs_lifecycle_v4999.lua',
  'mk2ks_native_subzero_legs_shatter_v4998.lua','mk2ks_native_subzero_legs_body_v4997.lua','mk2ks_stock_fatality_v1021.lua')]
 for path in[*controllers,Path(__file__),Path(native.__file__),build/'build-info.json',build/'mkport_candidate.exe',build/'roms/mk2ks/mk2ks.mdata']:
  pins[str(path.resolve())]=sha(path)
 text='\n'.join(path.read_text()for path in controllers)
 need(not re.search(r'(?:write_u|write_i|write_direct|write_logical|\.value\s*=(?!=))',text),'Only physical buttons; every loaded controller reviewed')
 need(sha(build/'mkport_candidate.exe')==native.EXE_SHA and all(sha(p)==h for p,h in pins.items()),'Immutable actual compiled inputs')
 folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,'Compress before evidence')
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_STOCK_KILLER='subzero',MK2KS_STOCK_COMMAND='ffd_hk',MK2KS_STOCK_GAP='168')
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
  '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000',
  '-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none','-noautoframeskip','-frameskip','0',
  '-nothrottle','-str','130','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),
  '-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(ROOT/LUA)]
 guestproof=gfxproof=None;scenes=[]
 with(folder/'stderr.log').open('w',encoding='utf-8')as err,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='strict')as process:
  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n')
  print(f'{fighter} P{side} actual shatter lifecycle started pid={process.pid}',flush=True)
  with(folder/'run.log').open('w',encoding='utf-8')as log:
   for line in process.stdout:
    if line.startswith(('MK2_EARNED_SUBZERO_GUEST ','MK2_EARNED_SUBZERO_GFX ','MK2_EARNED_SUBZERO_RGB ')):
     fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('hex'))
     digest=hashlib.sha256(raw).hexdigest().upper();tag=line.split()[0]
     if tag.endswith('_GUEST'):
      need(guestproof is None and fields==dict(frame='1',bytes='1048576')and raw==guest,'Every actual guest byte in RAM')
      guestproof=dict(bytes=len(raw),sha256=digest,executableSHA256=native.EXE_SHA,everyActualByteComparedInRAM=True,rawGuestFilesWritten=0)
      (folder/'guest_memory_proof.json').write_text(json.dumps(guestproof,indent=2)+'\n')
     elif tag.endswith('_GFX'):
      need(gfxproof is None and fields==dict(frame='1',bytes='18976')and raw==gfx,'Every actual own GFX byte in RAM')
      gfxproof=dict(bytes=len(raw),sha256=digest,everyActualByteComparedInRAM=True)
      (folder/'gfx_memory_proof.json').write_text(json.dumps(gfxproof,indent=2)+'\n')
     else:
      need(len(raw)==406400 and fields['width']=='400'and fields['height']=='254'and fields['bytes']=='406400','Actual complete RGB field')
      need(not any(r['frame']==int(fields['frame'])for r in scenes),'Distinct actual RGB times')
      scene=dict(frame=int(fields['frame']),width=400,height=254,bytes=len(raw),sha256=digest,rawMediaFilesWritten=0)
      scenes.append(scene)
      png=io.BytesIO();Image.frombytes('RGB',(400,254),raw,'raw','BGRX').save(png,format='PNG')
      print('MK2_NATIVE_SUBZERO_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)
      (folder/'rgb_memory_proofs.json').write_text(json.dumps(scenes,indent=2)+'\n')
     log.write(tag+'_DIGEST frame='+fields['frame']+' sha256='+digest+'\n');log.flush()
    else:
     need('hex='not in line,'Never persist guest, GFX, RGB or raw audio')
     log.write(line)
     if re.search(r'_(SHATTER_ENTRY|FRACTURE_ENTRY|LEGS_LOOKUP|WIN_WRAP|LIFECYCLE_END|RESULT) ',line):
      print(line.strip(),flush=True);log.flush()
  code=process.wait()
 log=(folder/'run.log').read_text();err=(folder/'stderr.log').read_text()
 need(all(sha(p)==h for p,h in pins.items()),'All executed source/native inputs unchanged')
 rows=[dict(re.findall(r'(\w+)=([^\s]+)',line),tag=line.split()[0])for line in log.splitlines()if line.startswith(('MK2_EARNED_SUBZERO_','MK2_STOCK_HEAD_V921_'))and '_DIGEST 'not in line]
 summary=dict(nativeExit=code,candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,
  actionRows=[r for r in rows if r['tag'].endswith(('DEEP_TASK','BODY_LOOKUP','SHATTER_ENTRY','HUMAN_PUNCH','FRACTURE_ENTRY','LEGS_LOOKUP','WIN_WRAP','LIFECYCLE_END','RESULT'))],
  actualScenes=scenes,inputHashes=pins,fullPortAcceptance=False,fullArtAcceptance=False,fullAudioAcceptance=False,
  nativeCacheOverrunObserved='CACHE_OVERWRITE 'in log,rawGuestMediaAudioFilesWritten=0)
 (folder/'result.json').write_text(json.dumps(summary,indent=2)+'\n')
 need(code==0 and guestproof and gfxproof and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log+err,re.I),'Actual successful transport/callbacks')
 need(not summary['nativeCacheOverrunObserved'],'No native cache global overwrite')
 for tag in('DEEP_TASK','BODY_LOOKUP','SHATTER_ENTRY','HUMAN_PUNCH','FRACTURE_ENTRY','LEGS_LOOKUP','WIN_WRAP','LIFECYCLE_END'):
  need(any(r['tag']=='MK2_EARNED_SUBZERO_'+tag for r in rows),'Actual required native branch '+tag)
 need(len(scenes)==4,'Actual freeze, fracture, victory and subsequent scene')
 summary['passed']=True
 return summary

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));parser.add_argument('--side',required=True,type=int,choices=(1,2));args=parser.parse_args()
 out=ROOT/f'audit_v5009_subzero_{args.fighter}_p{args.side}_lifecycle_observed'
 need(not out.exists(),'Fresh actual terminal report')
 try:report=capture(args.fighter,args.side)
 except Exception as e:report=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compress actual report')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
