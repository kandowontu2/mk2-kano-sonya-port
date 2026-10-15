"""Fresh actual natural CPU Square scene; entire media and native replay stay in RAM."""
import base64,hashlib,io,json,os,re,subprocess,traceback
from pathlib import Path
from PIL import Image,ImageDraw
import current_payload_metadata_context_v5229 as current
import current_cpu_scene_ram_contract_v5357 as scene
import native_cpu_square_hit_contract_v3037 as phase
import verify_native_extended_cpu_v2946 as ledgers
ROOT,need,sha=current.ROOT,current.need,current.sha
FOLDER=ROOT/'audit_v5358_current_cpu_square_scene_ram'
OUT=ROOT/'audit_v5359_current_cpu_square_scene_ram_checked'
LUA=ROOT/'mk2ks_cpu_square_scene_ram_v5357.lua'
CHAIN=('mk2ks_physical_p2_cpu_continuation_v1997.lua','mk2ks_physical_p2_cpu_round_trace_v1998.lua',
 'mk2ks_physical_p2_cpu_overlap_trace_v1999.lua','mk2ks_physical_p2_cpu_choice_trace_v2035.lua',
 'mk2ks_physical_p2_cpu_square_trace_v2038.lua','mk2ks_physical_p2_cpu_square_display_v2039.lua',
 'mk2ks_native_cpu_square_boundary_v2993.lua','mk2ks_native_cpu_square_locks_v3000.lua')
def run():
 guest=current.expected();build=ROOT/current.NAME;meta=json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))
 baseline=ROOT/'audit_v3282_current_cpu_square_render_erase_checked/report.json';qualified=json.loads(baseline.read_text())
 need(qualified['passed'],'Original physical/native full scene sources qualified')
 pins=dict(meta['input_hashes'])
 for name in CHAIN:
  p=ROOT/name;need(sha(p)==qualified['inputHashes'][str(p.resolve())],'Whole original physical/native scene source unchanged')
  need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',p.read_text()),'No game/CPU/health/RNG injection');pins[str(p)]=sha(p)
 for p in(LUA,Path(__file__),Path(scene.__file__),Path(current.__file__),baseline,build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata',
  *(ROOT/'mame-mkp/src/devices/cpu/tms34010'/name for name in('34010gfx.hxx','34010ops.hxx'))):pins[str(p.resolve())]=sha(p)
 need(not FOLDER.exists(),'Fresh immutable native capture');FOLDER.mkdir()
 need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(FOLDER)],capture_output=True).returncode==0,'Compress trace before native execution')
 (FOLDER/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='613',MK2KS_CPU_PAIR_APPROACH='guard_until_close',MK2KS_CPU_CONTINUATION_POLICY='jump_guard',MK2KS_CPU_PAIR_CONFIRM_AGE='264',MK2KS_FLOOR_OUT=str(FOLDER))
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(ROOT/'samples'),
  '-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat','-inipath',str(FOLDER),'-video','none','-sound','none',
  '-noautoframeskip','-frameskip','0','-nothrottle','-str','100','-cfg_directory',str(FOLDER/'cfg'),'-nvram_directory',str(FOLDER/'nvram'),'-snapshot_directory',str(FOLDER/'snap'),'-autoboot_script',str(LUA)]
 ram={};rawproofs=[];memory_log=[]
 with(FOLDER/'stderr.log').open('w',encoding='utf-8')as err,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='strict')as process:
  (FOLDER/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n');print('Actual native scene CPU PID='+str(process.pid),flush=True)
  with(FOLDER/'run.log').open('w',encoding='utf-8')as log:
   for line in process.stdout:
    if line.startswith('MK2_SCENE_RAM '):
     fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('hex'));label=fields['label']
     need(label not in ram and len(raw)==int(fields['bytes']),'Complete unique native RAM buffer');ram[label]=raw
     if label=='guest_maincpu.bin':need(raw==guest,'Every actual current guest byte independently reconstructed in RAM')
     if label.endswith('.rgb'):need(len(raw)==406400,'Entire actual native 400x254 BGRX field')
     proof=dict(label=label,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper());rawproofs.append(proof)
     log.write('MK2_SCENE_RAM_DIGEST '+' '.join(str(k)+'='+str(v)for k,v in proof.items())+'\n')
    elif line.startswith('MK2_NAT_CAMPAIGN_FLOOR_GFX '):
     memory_log.append(line);fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('data'))
     need(len(raw)==int(fields['bytes']),'Complete actual scene ROM stream')
     fields['sha256']=hashlib.sha256(raw).hexdigest().upper();log.write('MK2_SCENE_GFX_DIGEST '+' '.join(k+'='+v for k,v in fields.items())+'\n')
    else:
     need('hex='not in line,'No raw ROM/VRAM/RGB persisted');memory_log.append(line);log.write(line)
     if line.startswith(('MK2_P2CPU_COLD_LIVE ','MK2_CPU_PAIR_RESULT ','MK2_CPU_ROUND_RESULT ','MK2_NAT_CAMPAIGN_FLOOR_RESULT ')):print(line.strip(),flush=True)
  code=process.wait()
 log=''.join(memory_log)
 need(code==0 and ram.get('guest_maincpu.bin')==guest and (FOLDER/'stderr.log').read_text()==''and not re.search(r'LUA ERROR|stack traceback|fatal error',log,re.I),'Actual terminal0, complete guest and warning-free native execution')
 need(all(sha(p)==h for p,h in pins.items()),'All actual compiled/observer sources unchanged')
 (FOLDER/'ram_buffer_proofs.json').write_text(json.dumps(rawproofs,indent=2)+'\n')
 physical=dict(exit_code=code,candidate=current.NAME,assistance='none',cheats_enabled=False,input_hashes=pins,
  mediaTransport='native RAM only; all old file names are observation labels, not filesystem media',rawMediaFilesWritten=0)
 (FOLDER/'result.json').write_text(json.dumps(physical,indent=2)+'\n')
 prefixes=('MK2_CPU_PAIR_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_CPU_CHOICE_','MK2_SQUARE_NATIVE_','MK2_P2CPU_','MK2_SQUARE_BOUNDARY_','MK2_SQUARE_LOCK_')
 prior=ROOT/'audit_v5351_current_cpu_sonya_square_human_kano/run.log'
 need([s for s in log.splitlines()if s.startswith(prefixes)]==[s for s in prior.read_text().splitlines()if s.startswith(prefixes)],'Entire accepted current physical/native trajectory unchanged')
 pins[str(prior)]=sha(prior)
 typed=phase.verify(log,guest,'kano');health,by=ledgers.health_ledger(log,guest,'kano');state=ledgers.state_ledgers(log,guest,'kano',by)
 proof=scene.verify(FOLDER,ram,log,guest,pins)
 pictures=[]
 for frame in(2279,2287,2288,2297,2313,2317,2345,2348):pictures.append((str(frame),Image.frombytes('RGB',(400,254),ram[f'display_{frame}.rgb'],'raw','BGRX')))
 sheet=Image.new('RGB',(800,284),'black');draw=ImageDraw.Draw(sheet)
 for i,(label,picture)in enumerate(pictures):
  x=i%4*200;y=i//4*142;draw.text((x+2,y),label,fill='white');sheet.paste(picture.resize((200,127),Image.Resampling.NEAREST),(x,y+15))
 png=io.BytesIO();sheet.save(png,format='PNG');print('MK2_SCENE_PREVIEW_DATAURL data:image/png;base64,'+base64.b64encode(png.getvalue()).decode(),flush=True)
 for p in FOLDER.rglob('*'):
  if p.is_file():pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every final source/evidence pin stable')
 proof.update(candidate=current.NAME,phase=typed,wholeNativeHealth=health,wholeNativeState=state,
  originalWholePhysicalTrajectoryUnchanged=True,actualNativeTerminal=code,actualRAMBuffers=len(ram),
  actualRawBufferBytesInRAM=sum(len(v)for v in ram.values()),rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,newBuilds=0,inputHashes=pins)
 return proof
if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable current native scene proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','continuous','fullRAMRGBBindings')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
