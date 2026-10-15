"""Current physical freeze/shatter to next CPU, complete source audio in RAM.

No copied builds, raw media, guest writes or fitted audio. Native DCS-only
stage first; enabled imported-victim mixing is explicitly not accepted.
"""
import argparse,gzip,hashlib,inspect,json,os,re,subprocess,traceback
from pathlib import Path
import numpy as np
import current_payload_metadata_context_v5229 as current
import current_ending_audio_model_v5733 as model

ROOT,need,sha=current.ROOT,current.need,current.sha
LUA='mk2ks_current_subzero_audio_v6212.lua'
PARENT=ROOT/'audit_v6211_current_normal_subzero_freeze_progress/progress.json'

def digest(raw):return hashlib.sha256(raw).hexdigest().upper()
def fields(line):
 pairs=re.findall(r'(\w+)=([^\s]+)',line);r=dict(pairs)
 need(len(pairs)==len(r),'Unique actual transport header keys');return r
def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')

def dac_models(callbacks):
 need(1600<callbacks<2100,'Whole earned next-CPU audio window')
 source=inspect.getsource(model.original_dac.dac_gate)
 before='len(chunks)==len(headers)==len(pcm_headers)==685'
 need(source.count(before)==1,'Only complete native duration parameter changes')
 source=source.replace(before,'len(chunks)==len(headers)==len(pcm_headers)==callbacks',1)
 scope=dict(vars(model.original_dac),callbacks=callbacks)
 exec(compile(source,__file__+'::whole_original_DAC_gate','exec'),scope)
 exec(compile(inspect.getsource(model.original_dac.dac_faults),__file__+'::whole_original_DAC_faults','exec'),scope)
 need(scope['dac_faults'].__globals__['dac_gate']is scope['dac_gate'],'Faults bind entire unchanged gate')
 return scope['dac_gate'],scope['dac_faults'],digest(source.encode())

def run(fighter,side):
 folder=ROOT/f'audit_v6214_current_subzero_{fighter}_p{side}_native_audio'
 need(not folder.exists(),'Fresh native evidence folder')
 guest=current.expected();gfx=current.expected_gfx();build=ROOT/current.NAME
 parent=json.loads(PARENT.read_text());need(parent['passed']and len(parent['remaining'])==5,'Full current scope preserved')
 files=[ROOT/leaf for leaf in (LUA,'mk2ks_native_subzero_legs_nextmatch_v5000.lua',
  'mk2ks_native_subzero_legs_lifecycle_v4999.lua','mk2ks_native_subzero_legs_shatter_v4998.lua',
  'mk2ks_native_subzero_legs_body_v4997.lua','mk2ks_stock_fatality_v1021.lua',
  'mk2ks_current_tomb_winner_mix_observer_v5779.lua')]
 controller='\n'.join(p.read_text()for p in files)
 need(not re.search(r'write_u\d|write_i\d|write_direct|write_logical|\.value\s*=(?!=)|load_?state|force_update|flush\(',controller),
      'Only original physical inputs and passive native audio observers')
 pins={str(p):sha(p)for p in files+[Path(__file__),Path(current.__file__),Path(model.__file__),
  ROOT/'tools/current_native_dac_clock_v5596.py',ROOT/'tools/current_native_dac_capture_v5593.py',
  ROOT/'tools/current_dcs_rom_source_capture_v5586.py',PARENT,build/'build-info.json',build/'mkport_candidate.exe']}
 expected,_=model.expected_region(pins)
 folder.mkdir();save(folder/'inputs.json',pins)
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_STOCK_KILLER='subzero',
            MK2KS_STOCK_COMMAND='ffd_hk',MK2KS_STOCK_GAP='168')
 cmd=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
  '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-nosamples','-samplerate','48000',
  '-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none',
  '-noautoframeskip','-frameskip','0','-nothrottle','-str','130',
  '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),
  '-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(ROOT/LUA)]
 pcm_chunks=[];pcm_headers=[];dac_chunks=[];dac_headers=[];rom={p:bytearray()for p in ('startup','terminal')}
 raw_proofs=[];seen_guest=0;seen_gfx=0;decode_errors=[]
 with (folder/'stderr.log').open('w',encoding='utf-8')as err,subprocess.Popen(cmd,cwd=ROOT,env=env,
      stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='strict',creationflags=subprocess.CREATE_NO_WINDOW)as process:
  query="Get-CimInstance Win32_Process -Filter 'ProcessId="+str(process.pid)+"' | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
  wi_result=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
  wi=json.loads(wi_result.stdout)if wi_result.returncode==0 and wi_result.stdout.strip()else None
  save(folder/'process.json',dict(pid=process.pid,command=cmd,actualWindowsIdentity=wi))
  print(f'Current {fighter} P{side} native audio PID={process.pid}',flush=True)
  with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:
   for line in process.stdout:
    try:
     if ' hex='in line:
      tag=line.split()[0];h=fields(line);raw=bytes.fromhex(h.pop('hex'))
      need(len(raw)==int(h['bytes']),'All actual transported bytes retained')
      h['sha256']=digest(raw)
      if tag=='MK2_BBAUDIO_PCM':pcm_chunks.append(raw);pcm_headers.append(h)
      elif tag=='MK2_NATIVE_DAC_RAM':dac_chunks.append(raw);dac_headers.append(h)
      elif tag=='MK2_NATIVE_DCS_ROM':
       phase=h['phase'];need(phase in rom and int(h['offset'])==len(rom[phase])and h['size']=='12582912'and h['bytes']=='65536'and h['bytewidth']=='2'and h['bitwidth']=='16'and h['writes']=='0'and h['assistance']=='none','Whole consecutive original ROM inventory')
       at=int(h['offset']);need(raw==expected[at:at+len(raw)],'Every actual original DCS ROM byte')
       rom[phase].extend(raw)
      elif tag in ('MK2_MAUDIO_GUEST','MK2_EARNED_SUBZERO_GUEST'):
       need(raw==guest,'Every independently reconstructed current guest byte');seen_guest+=1
      elif tag=='MK2_EARNED_SUBZERO_GFX':need(raw==gfx,'Every own frozen GFX byte');seen_gfx+=1
      elif tag=='MK2_EARNED_SUBZERO_RGB':
       need(len(raw)==406400 and h['width']=='400'and h['height']=='254','Whole native stage RGB transport')
       raw_proofs.append(h)
      else:raise AssertionError('Unexpected raw transport '+tag)
      log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in h.items())+'\n')
     else:log.write(line)
    except Exception as error:
     # Native execution is authoritative. Drain this same process to terminal
     # after a host parsing failure; do not restart or preserve raw transport.
     decode_errors.append(dict(error=repr(error),tag=line.split()[0]if line.strip()else'empty'))
   code=process.wait()
  save(folder/'native_terminal.json',dict(pid=process.pid,nativeExit=code,actualWindowsIdentity=wi,hostDecodeErrors=decode_errors))
 with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
 need(wi and wi['ProcessId']==process.pid and wi['Name']=='mkport_candidate.exe'and
      Path(wi['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve()and str(ROOT/LUA)in wi['CommandLine'],
      'Actual CIM native creation/executable/full command')
 need(code==0 and not decode_errors and (folder/'stderr.log').read_text()==''and
      not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|CACHE_OVERWRITE',text,re.I),
      'Actual warning-free native terminal, not observation timeout')
 need(seen_guest==2 and seen_gfx==1 and len(raw_proofs)==4,'Whole driver plus audio guest and four native transitions')
 rows=[dict(fields(line),tag=line.split()[0])for line in text.splitlines()if line.startswith('MK2_EARNED_SUBZERO_')and '_DIGEST 'not in line]
 for tag in ('DEEP_TASK','BODY_LOOKUP','SHATTER_ENTRY','HUMAN_PUNCH','FRACTURE_ENTRY','LEGS_LOOKUP','WIN_WRAP','LIFECYCLE_END'):
  need(any(r['tag']=='MK2_EARNED_SUBZERO_'+tag for r in rows),'Actual native branch '+tag)
 end=[r for r in rows if r['tag']=='MK2_EARNED_SUBZERO_LIFECYCLE_END'];need(len(end)==1,'One genuine next CPU terminal')
 need(end[0]['winner_id']=='8'and end[0]['winner_state']=='1'and end[0]['enemy_state']=='0'and end[0]['mode']=='2',
      'Actual new stock CPU match, no abandoned finisher')
 gate,fault,gate_sha=dac_models(len(pcm_headers));dac=gate(dac_chunks,dac_headers,pcm_headers)
 dac_faults=fault(dac_chunks,dac_headers,pcm_headers)
 pcm=np.frombuffer(b''.join(pcm_chunks),dtype='<i2').reshape(-1,2)
 waveform=model.predict_waveform(dac_chunks,dac_headers,pcm)
 save(folder/'waveform.json',waveform)
 need(waveform['passed'],'Every actual native PCM sample, no timing/gain fit or trimmed tail')
 rg,rf=model.rom_models(expected)
 rom_proof=[rg(bytes(rom[p]),p)for p in rom]
 rom_faults=[f for p in rom for f in rf(bytes(rom[p]),p)]
 need(all(sha(p)==h for p,h in pins.items()),'All original executed and current compiled inputs unchanged')
 report=dict(passed=True,fighter=fighter,physicalSlot=side,candidate=current.NAME,executableSHA256=current.EXE_SHA,
  guestSHA256=current.GUEST_SHA,parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],inputHashes=pins,
  nativeTerminal=json.loads((folder/'native_terminal.json').read_text()),nativeNextCPUMatch=end[0],
  sourceDACGateSHA256=gate_sha,dacProof=dac,dacFaultsRejected=dac_faults,wholeOriginalSoundROM=rom_proof,
  originalSoundROMFaultsRejected=rom_faults,pcmHeaders=pcm_headers,dacHeaders=dac_headers,
  waveformReport=str(folder/'waveform.json'),comparedStereoFrames=waveform['comparedStereoFrames'],
  nativeDCSWaveformAccepted=True,samplesEnabled=False,importedVictimMixAccepted=False,
  fullStageArtAccepted=False,fullPortAcceptance=False,newBuilds=0,rawMediaFilesWritten=0,
  actualDriverNativeRGBTransport=raw_proofs)
 save(folder/'report.json',report)
 print(json.dumps({k:report[k]for k in ('passed','fighter','physicalSlot','comparedStereoFrames','nativeDCSWaveformAccepted','samplesEnabled','fullPortAcceptance')},indent=2),flush=True)
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:run(args.fighter,args.side)
 except Exception as error:
  folder=ROOT/f'audit_v6214_current_subzero_{args.fighter}_p{args.side}_native_audio'
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():save(folder/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
