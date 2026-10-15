"""Current genuine earned Mileena swallowing contexts, bounded RAM native media.

Real physical selection, two collision-earned KOs, native held-HK release,
true victim streams/disappearance/retirement and601-field post-action window.
Original complete state contract retained; bounded PNGs are visual evidence,
not whole-scene replay or audio acceptance. No raw guest/GFX/PCM/RGB sink.
"""
import argparse,hashlib,json,os,re,struct,subprocess,traceback
from pathlib import Path
from PIL import Image
import current_payload_metadata_context_v5229 as current
import verify_mileena_fixed_runtime_v3829 as original
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_current_mileena_native_v6081.lua'

def run(fighter,side):
 folder=ROOT/f'audit_v6083_current_mileena_{fighter}_p{side}'
 need(not folder.exists(),'Fresh exact current native swallowing capture')
 guest=current.expected();build=ROOT/current.NAME;payload=(build/'roms/mk2ks/mk2ks.mdata').read_bytes()
 n0,n1=struct.unpack_from('<I',payload,0x1f6008)[0],struct.unpack_from('<I',payload,0x1f6010)[0]
 expected_gfx=payload[0x122000:0x122000+n0]+payload[0x154000:0x154000+n1]
 need(payload[0x1f6000:0x1f6004]==b'KME1'and 0<len(expected_gfx)<=0x20000,'Current dedicated owned swallowing graphics header')
 pins=dict(json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))['input_hashes'])
 for p in(LUA,ROOT/'mk2ks_mileena_earned_fixed_v3824.lua',ROOT/'mk2ks_cache_provenance_mileena_fixed_v3823.lua',
           Path(__file__).resolve(),Path(current.__file__).resolve(),Path(original.__file__).resolve(),
           build/'build-info.json',build/'mkport_candidate.exe',build/'roms/mk2ks/mk2ks.mdata'):
  pins[str(p.resolve())]=sha(p)
  if p.suffix=='.lua':need(not re.search(r'(write_u|write_i|write_direct|write_logical|\.value\s*=(?!=)|screen:snapshot)',p.read_text()),'Only real controls and read-only nil taps')
 need(all(sha(p)==v for p,v in pins.items()),'All actual compiled and driver inputs unchanged before native boot')
 folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,'Compressed bounded native capture directory')
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_PROVENANCE_MIN_FRAME='0',MK2KS_CURRENT_ROOT=str(ROOT))
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
  '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat',
  '-inipath',str(folder),'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','150',
  '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
 proofs={};scenes=[];errors=[]
 with(folder/'stderr.log').open('w',encoding='utf-8')as stderr,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr,text=True,encoding='utf-8',errors='strict')as process:
  query="Get-CimInstance Win32_Process -Filter 'ProcessId="+str(process.pid)+"' | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
  result=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
  identity=json.loads(result.stdout)if result.returncode==0 and result.stdout.strip()else None
  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command,actualWindowsIdentity=identity),indent=2)+'\n')
  print(f'{fighter} P{side}: current earned Mileena native PID={process.pid}',flush=True)
  with(folder/'run.log').open('w',encoding='utf-8')as log:
   for line in process.stdout:
    if line.startswith(('MK2_CURRENT_MILEENA_GUEST ','MK2_CURRENT_MILEENA_GFX ','MK2_CURRENT_MILEENA_RGB ')):
     try:
      tag=line.split()[0];fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('hex'));digest=hashlib.sha256(raw).hexdigest().upper()
      need(len(raw)==int(fields['bytes']),'Complete native RAM-only transport')
      if tag.endswith(('_GUEST','_GFX')):
       key=tag.rsplit('_',1)[1];expected=guest if key=='GUEST'else expected_gfx
       need(key not in proofs and fields['frame']=='1'and raw==expected,'Every actual initialized guest/owned swallowing GFX byte equals current source')
       proofs[key]=dict(bytes=len(raw),sha256=digest,everyActualByteComparedInRAM=True)
      else:
       need(fields['width']=='400'and fields['height']=='254'and len(raw)==406400,'Whole bounded actual native400x254 screen')
       age=int(fields['age']);image=Image.frombytes('RGB',(400,254),raw,'raw','BGRX');path=folder/f'native_mileena_{age:03d}.png';need(not path.exists(),'One exact bounded native phase image');image.save(path)
       scenes.append(dict(frame=int(fields['frame']),age=age,rgbSHA256=digest,path=str(path),pngSHA256=sha(path)))
      log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in fields.items())+' sha256='+digest+'\n')
     except Exception as error:
      errors.append(repr(error));log.write('MK2_CURRENT_MILEENA_TRANSPORT_ERROR '+repr(error)+'\n')
    else:
     if 'hex='in line:errors.append('Unexpected encoded buffer protocol');log.write('MK2_CURRENT_MILEENA_UNEXPECTED_BUFFER\n')
     else:
      log.write(line)
      if re.match(r'MK2_MILEENA_V3784_(ACTION|FIRST_LIVE|RESULT|HK_RELEASE|HOST_EXIT|WIN) ',line):print(line.strip(),flush=True)
   code=process.wait()
 (folder/'native_terminal.json').write_text(json.dumps(dict(pid=process.pid,nativeExit=code,actualWindowsIdentity=identity),indent=2)+'\n')
 (folder/'memory_proofs.json').write_text(json.dumps(proofs,indent=2)+'\n');(folder/'scene_proofs.json').write_text(json.dumps(scenes,indent=2)+'\n')
 log=(folder/'run.log').read_text();stderr=(folder/'stderr.log').read_text()
 need(code==0 and not errors and set(proofs)=={'GUEST','GFX'}and stderr=='', 'Actual native terminal0, complete source-bound transport and warning-free boot')
 need(identity and identity['ProcessId']==process.pid and identity['Name']=='mkport_candidate.exe'and
      Path(identity['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve()and str(LUA)in identity['CommandLine'],
      'Actual creation/executable/complete command identity bound to native terminal')
 need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|WRONG CHECKSUMS',log,re.I),'No native or observer fault')
 state=original.gate(original.parse(log),fighter,side);need(state['passed'],repr(state))
 need([s['age']for s in scenes]==[0,8,16,24,32,64,128,600]and all(s['frame']==state['actionFrame']+s['age']for s in scenes),
      'All eight exact requested native phase screens; no best-frame search')
 need(all(sha(p)==v for p,v in pins.items()),'All executed inputs immutable after actual native terminal')
 return dict(passed=True,candidate=current.NAME,fighter=fighter,side=side,nativeExit=code,actualWindowsIdentity=identity,
      executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,payloadSHA256=current.PAYLOAD_SHA,
      inputHashes=pins,nativeState=state,memoryProofs=proofs,actualScenes=scenes,
      currentNativeMileenaVictimStreamsAndCleanupAccepted=True,rawMediaFilesWritten=0,
      fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=('kano','sonya'),required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
 out=ROOT/f'audit_v6084_current_mileena_{a.fighter}_p{a.side}_observed';need(not out.exists(),'Fresh immutable current Mileena terminal report')
 try:report=run(a.fighter,a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
