"""Cold current4992 Sonya P1; only ordinary Sub-Zero guard controls change.

No guest writes, save states, proxy IDs or gameplay assistance. Full guest and
native RGB buffers stay in RAM. Complete textual chronology is gzip-streamed
to avoid another large uncompressed build/test folder. A terminal transport
success is not campaign, artwork, audio or full-port acceptance.
"""
import base64,gzip,hashlib,io,json,os,re,subprocess,sys,time,traceback,zlib
from pathlib import Path
from PIL import Image
import native_subzero_legs_context_v4993 as native

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5208_extended_sonya_p1_campaign'
LUA='mk2ks_sonya_extended_tested_ram_v5206.lua'
CONTROLLERS=[LUA,'mk2ks_sonya_extended_prime_ram_v5205.lua','mk2ks_sonya_extended_subzero_ram_v5204.lua','mk2ks_sonya_extended_jax_ram_v5203.lua','mk2ks_sonya_extended_kitana_ram_v5202.lua',
 'mk2ks_sonya_extended_guard_base_ram_v5201.lua',
 'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua',
 'mk2ks_mileena_campaign_trace_v3848.lua']

def qualify_payload_metadata_warning(errors,guestproof):
 # Only this isolated candidate's exact source-bound mdata warning is allowed.
 # It remains a release defect; every other warning/error is retained/rejected.
 candidate=ROOT/native.NAME
 source=candidate/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 need(sha(source)=='0094EAE7DC9D3AF85474F720A16054BCFA5DF654751E8DA9C3D105588E674363',
  'Exact actual compiled ROM declaration source')
 declaration=re.findall(r'ROM_LOAD\( "mk2ks\.mdata", 0x000000, 0x200000, CRC\(([a-f0-9]+)\) SHA1\(([a-f0-9]+)\) \)',source.read_text())
 need(len(declaration)==1,'One exact compiled payload metadata declaration')
 payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()
 need(len(payload)==0x200000 and sha(candidate/'roms/mk2ks/mk2ks.mdata')==native.PAYLOAD_SHA and
  guestproof and guestproof['sha256']==native.GUEST_SHA and guestproof['everyActualByteComparedInRAM'],
  'Actual payload and complete initialized guest independently qualified, not a generic checksum waiver')
 expected_crc,expected_sha=declaration[0]
 found_crc=f'{zlib.crc32(payload):08x}';found_sha=hashlib.sha1(payload).hexdigest()
 warning=('mk2ks.mdata WRONG CHECKSUMS:\n'
  f'    EXPECTED: CRC({expected_crc}) SHA1({expected_sha})\n'
  f'       FOUND: CRC({found_crc}) SHA1({found_sha})\n'
  'WARNING: the machine might not run correctly.\n')
 need(errors.replace('\r\n','\n')==warning,'Only exact source/payload-bound startup metadata warning, no other error')
 return dict(compiledCRC=expected_crc,compiledSHA1=expected_sha,payloadCRC=found_crc,payloadSHA1=found_sha,
  exactSourceAndFullGuestBound=True,testCandidateWarningQualified=True,releaseMetadataCorrectionStillRequired=True)

def capture():
 need(not OUT.exists(),'Fresh immutable campaign; never restart a live run')
 guest=native.expected()
 candidate=ROOT/native.NAME
 build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
 pins=dict(build['input_hashes'])
 paths=[ROOT/p for p in CONTROLLERS]+[Path(__file__).resolve(),candidate/'build-info.json',
  candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'restoration.json']
 for module in tuple(sys.modules.values()):
  path=getattr(module,'__file__',None)
  if path and Path(path).suffix=='.py' and Path(path).resolve().is_relative_to(ROOT/'tools'):
   paths.append(Path(path))
 for path in paths:
  key=str(path.resolve());actual=sha(path)
  need(key not in pins or pins[key]==actual,'Compiled input unchanged '+key)
  pins[key]=actual
 text='\n'.join((ROOT/p).read_text()for p in CONTROLLERS)
 need(not re.search(r'(?:write_u|write_i|write_direct|write_logical|\.value\s*=(?!=))',text),
  'All eight loaded controllers inspected; buttons and readonly taps only')
 need(sha(candidate/'mkport_candidate.exe')==native.EXE_SHA and
  sha(candidate/'roms/mk2ks/mk2ks.mdata')==native.PAYLOAD_SHA and
  all(sha(p)==h for p,h in pins.items()),'Actual current compiled source and payload')
 OUT.mkdir()
 (OUT/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1',
  MK2KS_CAMPAIGN_STRATEGY='guard_punish',MK2KS_BOSS_PHYSICAL_POLICY='shao_ring_retreat',
  MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000',MK2KS_TEST_BOOT_FRAME='600',
  MK2KS_CAMPAIGN_OUT=str(OUT),MK2KS_TWO_PLAYER='0')
 command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
  '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000',
  '-skip_gameinfo','-nocheat','-inipath',str(OUT),'-video','none','-sound','none',
  '-noautoframeskip','-frameskip','0','-nothrottle','-str','18100','-snapsize','400x254',
  '-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),
  '-snapshot_directory',str(OUT/'snap'),'-autoboot_script',str(ROOT/LUA)]
 guestproof=None;scenes=[];events=[];images={};preview_seen=set();overruns=[];stream=hashlib.sha256();rawbytes=0
 started=time.time()
 with(OUT/'stderr.log').open('w',encoding='utf-8')as errors,subprocess.Popen(command,cwd=ROOT,env=env,
  stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:
  (OUT/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command,
   startedUnix=started,hostPID=os.getpid(),hostSource=str(Path(__file__).resolve())),indent=2)+'\n')
  print(f'Current4992 exact-tested-prime Sonya P1 campaign started nativePID={process.pid} hostPID={os.getpid()}',flush=True)
  with gzip.open(OUT/'run.log.gz','wt',encoding='utf-8',compresslevel=6)as log:
   for line in process.stdout:
    if line.startswith('MK2_CAMPAIGN_GUEST_RAM '):
     fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('hex'))
     need(guestproof is None and fields==dict(frame='1',bytes='1048576')and raw==guest,
      'Every initialized current guest byte compared independently in RAM')
     guestproof=dict(frame=1,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),
      executableSHA256=native.EXE_SHA,payloadSHA256=native.PAYLOAD_SHA,
      captureSourceSHA256=sha(__file__),transportSourceSHA256=sha(ROOT/LUA),
      everyActualByteComparedInRAM=True,guestDumpFilesWritten=0)
     (OUT/'guest_memory_proof.json').write_text(json.dumps(guestproof,indent=2)+'\n')
     log.write('MK2_CAMPAIGN_GUEST_RAM_DIGEST frame=1 bytes=1048576 sha256='+guestproof['sha256']+'\n')
     print('Actual initialized guest qualified: '+guestproof['sha256'],flush=True)
    elif line.startswith('MK2_CAMPAIGN_RAM_FRAME '):
     fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('hex'))
     need(len(raw)==406400 and fields['width']=='400'and fields['height']=='254'and fields['bytes']=='406400',
      'Complete actual native RGB field in RAM')
     fields['sha256']=hashlib.sha256(raw).hexdigest().upper();stream.update(raw);rawbytes+=len(raw)
     scenes.append(fields)
     name=fields['filename'];image=Image.frombytes('RGB',(400,254),raw,'raw','BGRX')
     # Retain just critical scenes for live visual inspection, not all losses.
     selected=(name=='campaign_selection_1_146.png' or
      bool(re.fullmatch(r'campaign_fight_selection\d+_stage(?:7|8|15|16)\.png',name)) or
      name.startswith('ending_page') or name=='ending_return_to_attract.png')
     if selected and fields['sha256']not in preview_seen:
      preview_seen.add(fields['sha256']);images[name]=image
      preview=io.BytesIO();image.save(preview,format='PNG')
      print('MK2_CURRENT_CAMPAIGN_PREVIEW_DATAURL data:image/png;base64,'+
       base64.b64encode(preview.getvalue()).decode(),flush=True)
      print('Native scene '+name+' sha256='+fields['sha256'],flush=True)
     log.write('MK2_CAMPAIGN_RAM_FRAME_DIGEST '+' '.join(f'{k}={v}'for k,v in fields.items())+'\n')
    else:
     need('hex='not in line,'Never persist encoded guest/raster/audio')
     log.write(line)
     if re.match(r'^MK2_NAT_CAMPAIGN_(SELECT_ID|STAGE|LOSS|ENDING_START|ENDING_COMPLETED|RESULT) ',line) or \
      re.match(r'^MK2_MILEENA_CAMPAIGN_(OVERRUN|RESULT) ',line) or line.startswith('MK2_CAMPAIGN_HOST_DEADLINE '):
      events.append(line.strip());print(line.strip(),flush=True);log.flush()
      if 'MK2_MILEENA_CAMPAIGN_OVERRUN 'in line:overruns.append(line.strip())
     elif re.search(r'LUA ERROR|stack traceback|fatal error|access violation',line,re.I):
      print(line.strip(),flush=True)
  code=process.wait()
 # Gzip member is complete now; authoritative verification can read all rows.
 need(all(sha(p)==h for p,h in pins.items()),'Every actually executed input remains unchanged')
 with gzip.open(OUT/'run.log.gz','rt',encoding='utf-8')as reader:chronology=reader.read()
 errors=(OUT/'stderr.log').read_text()
 metadata=qualify_payload_metadata_warning(errors,guestproof)
 transport=bool(code==0 and guestproof and not re.search(
  r'LUA ERROR|stack traceback|fatal error|access violation',chronology+errors,re.I))
 stages=[int(re.search(r' stage=(\d+)',line).group(1))for line in events if line.startswith('MK2_NAT_CAMPAIGN_STAGE ')]
 result=dict(schema=1,passed=transport,nativeExit=code,candidate=native.NAME,
  executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,fighter='sonya',physicalSlot=1,
  identity=18,actualStages=stages,nativeEvents=events,nativeCacheOverrunObserved=bool(overruns),
  actualNativeRGBFrameCallbacks=len(scenes),nativeRGBBytesComparedInRAM=rawbytes,
  nativeRGBStreamSHA256=stream.hexdigest().upper(),actualScenes=scenes,inputHashes=pins,
  elapsedSeconds=time.time()-started,rawMediaGuestAudioFilesWritten=0,newBuilds=0,
  publicPlayableChanged=False,actualNaturalTowerClearAccepted=False,
  independentWholeCampaignVerificationPending=True,fullArtAcceptance=False,
  fullAudioAcceptance=False,fullPortAcceptance=False,
  logCompression='lossless streaming gzip; complete rows preserved',qualifiedTestCandidateMetadataWarning=metadata)
 (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items()if k not in('inputHashes','actualScenes','nativeEvents')},indent=2),flush=True)
 need(transport,'Actual terminal current4992 transport and native callbacks; inspect immutable failure')
 need(not overruns,'No original cache writes into global state')
 return result

if __name__=='__main__':
 try:capture()
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():
   path=OUT/'capture_failure.json';need(not path.exists(),'Immutable failure');path.write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise



