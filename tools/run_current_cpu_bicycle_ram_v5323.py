"""Current natural CPU Bicycle contact/audio, original full gates, RAM-only media."""
import base64,hashlib,inspect,io,json,os,re,subprocess,traceback,types
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import current_payload_metadata_context_v5229 as current
import run_current_cpu_bicycle_hit_audio_v3400 as original
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5325_current_cpu_bicycle_ram_checked'
LUA=ROOT/'mk2ks_cpu_ram_transport_v5323.lua'
CHAIN=('mk2ks_physical_p2_cpu_continuation_v3300.lua','mk2ks_physical_p2_cpu_round_trace_v3301.lua',
 'mk2ks_physical_p2_cpu_overlap_trace_v3302.lua','mk2ks_physical_p2_cpu_choice_trace_v3303.lua',
 'mk2ks_physical_p2_cpu_square_trace_v3304.lua','mk2ks_native_cpu_audio_mobility_v3395.lua',
 'mk2ks_cpu_bicycle_hit_audio_v3396.lua')
GUEST=None

def capture(enabled):
 folder=ROOT/f'audit_v5324_current_cpu_bicycle_ram_{"samples"if enabled else"nosamples"}'
 need(not folder.exists(),'Fresh immutable physical CPU capture')
 build=ROOT/current.NAME;meta=json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))
 baseline=ROOT/'audit_v3402_current_cpu_bicycle_hit_audio_checked/report.json'
 qualified=json.loads(baseline.read_text());need(qualified['passed'],'Actual original CPU hit/audio acceptance')
 pins=dict(meta['input_hashes'])
 for name in CHAIN:
  path=ROOT/name;need(sha(path)==qualified['inputHashes'][str(path)],'Entire original input/observer source unchanged')
  need(not re.search(r'write_u\d+|write_i\d+|\.value\s*=(?!=)|load_?state|:reset\(',path.read_text()),'No guest/register state injection')
 for path in [*(ROOT/n for n in CHAIN),LUA,Path(__file__),Path(current.__file__),Path(original.__file__),baseline,
              build/'mkport_candidate.exe',build/'roms/mk2ks/mk2ks.mdata',build/'build-info.json',
              ROOT/'samples/mk2ks/sonya_bicycle_launch.wav',ROOT/'samples/mk2ks/sonya_bicycle_cry.wav']:
  pins[str(path.resolve())]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'All actual compiled and observer inputs pinned')
 folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,'Compressed trace folder')
 (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='613',MK2KS_CPU_PAIR_APPROACH='guard_until_close',
            MK2KS_CPU_CONTINUATION_POLICY='jump_on_launch',MK2KS_CPU_PAIR_CONFIRM_AGE='264')
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
  '-samplepath',str(ROOT/'samples'),'-samples'if enabled else'-nosamples','-artpath',str(ROOT/'artwork'),
  '-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none','-samplerate','48000',
  '-noautoframeskip','-frameskip','0','-nothrottle','-str','95','-cfg_directory',str(folder/'cfg'),
  '-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
 chunks=[];headers=[];scenes=[];preview=[];guest_seen=False
 with(folder/'stderr.log').open('w',encoding='utf-8')as err,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='strict')as process:
  (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n')
  print(f'{folder.name}: actual native pid={process.pid}',flush=True)
  with(folder/'run.log').open('w',encoding='utf-8')as log:
   for line in process.stdout:
    if line.startswith(('MK2_BBAUDIO_PCM ','MK2_CPU_RAM_RGB ','MK2_CPU_RAM_GUEST ')):
     fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('hex'))
     need(len(raw)==int(fields['bytes']),'Complete native RAM buffer')
     fields['sha256']=hashlib.sha256(raw).hexdigest().upper()
     if line.startswith('MK2_BBAUDIO_PCM '):
      need(len(raw)%4==0,'Whole stereo PCM frames');chunks.append(raw);headers.append(fields)
     elif line.startswith('MK2_CPU_RAM_GUEST '):
      need(not guest_seen and fields['frame']=='1'and raw==GUEST,'Entire initialized current guest independently compared')
      guest_seen=True;(folder/'guest_memory_proof.json').write_text(json.dumps(fields,indent=2)+'\n')
     else:
      need(len(raw)==406400 and fields['width']=='400'and fields['height']=='254','Entire native rendered RGB field')
      scenes.append(fields)
      if enabled:preview.append((fields['label'],Image.frombytes('RGB',(400,254),raw,'raw','BGRX')))
     log.write(line.split()[0]+'_DIGEST '+' '.join(f'{k}={v}'for k,v in fields.items())+'\n')
    else:
     need('hex='not in line,'No raw PCM/ROM/RGB in files');log.write(line)
     if line.startswith(('MK2_P2CPU_COLD_LIVE ','MK2_CPU_PAIR_COMPLETE ','MK2_CPU_PAIR_RESULT ','MK2_BBAUDIO_RESULT ')):print(line.strip(),flush=True)
  code=process.wait()
 text=(folder/'run.log').read_text();errors=(folder/'stderr.log').read_text()
 need(code==0 and guest_seen and errors==''and not re.search(r'LUA ERROR|stack traceback|Fatal error|access violation',text,re.I),'Native terminal0, no warning/error waiver')
 need(headers and all(float(a['seconds'])<float(b['seconds'])for a,b in zip(headers,headers[1:])),'Every native audio callback chronological')
 need(scenes and all(sha(p)==h for p,h in pins.items()),'All actual inputs unchanged and original snapshots transported')
 pcm=b''.join(chunks)
 (folder/'rgb_memory_proofs.json').write_text(json.dumps(scenes,indent=2)+'\n')
 (folder/'result.json').write_text(json.dumps(dict(exit_code=code,candidate=current.NAME,input_hashes=pins,
  wholeActualGuestComparedInRAM=True,rawAudioRGBGuestFilesWritten=0,mixedPCMBytes=len(pcm),mixedPCMSHA256=hashlib.sha256(pcm).hexdigest().upper(),
  actualRGBFields=len(scenes),samples_enabled=enabled,fullPortAcceptance=False),indent=2)+'\n')
 if enabled:
  sheet=Image.new('RGB',(600,115*((len(preview)+3)//4)),'black');draw=ImageDraw.Draw(sheet)
  for i,(label,picture)in enumerate(preview):
   x=i%4*150;y=i//4*115;draw.text((x,y),label[:24],fill='white');sheet.paste(picture.resize((150,95),Image.Resampling.NEAREST),(x,y+18))
  png=io.BytesIO();sheet.save(png,format='PNG');print('MK2_CPU_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)
 return folder,headers,np.frombuffer(pcm,dtype='<i2').reshape(-1,2).astype(np.float64)

def run():
 global GUEST
 GUEST=current.expected()
 source=inspect.getsource(original.run)
 changes={
  "guest=current.expected_current()[0]":"guest=GUEST",
  "need((folder/'guest_maincpu.bin').read_bytes()==(baseline/'guest_maincpu.bin').read_bytes()==guest,'Whole independently assembled actual guest bytes')":
   "need(all(json.loads((p/'guest_memory_proof.json').read_text())['sha256']==current.GUEST_SHA for p in(folder,baseline)),'Whole actual current guests independently compared in RAM')",
  "not line.startswith(('MK2_BBAUDIO_','MK2_NAT_CAMPAIGN_'))":"not line.startswith(('MK2_BBAUDIO_','MK2_NAT_CAMPAIGN_','MK2_CPU_RAM_'))",
  "candidate=base.CANDIDATE":"candidate=current.NAME"}
 for before,after in changes.items():
  need(source.count(before)==1,'Single exact whole original audio-contract adaptation: '+before[:90]);source=source.replace(before,after,1)
 namespace=dict(original.run.__globals__,OUT=OUT,capture=capture,current=current,GUEST=GUEST)
 exec(compile(source,__file__+'::entire_original_cpu_hit_audio_contract','exec'),namespace)
 result=namespace['run']()
 result.update(currentMetadataCorrectedCandidate=True,originalEntireNativeCPUHitAudioContractRetained=True,
  transportOnlyChanges=['snapshot to native RAM RGB','guest file to RAM byte comparison'],newBuilds=0,
  rawGuestGFXRGBPCMOrWAVFilesWritten=0)
 return result

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable current CPU proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','assets')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
