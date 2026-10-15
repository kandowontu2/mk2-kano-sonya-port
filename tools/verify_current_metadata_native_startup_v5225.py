"""Current metadata-only native cold boots; RAM guest/RGB and exact prior chronology."""
import gzip,hashlib,json,os,re,subprocess,time
from pathlib import Path
import native_subzero_legs_context_v4993 as old
import run_current_kano_p1_campaign_v5195 as kano
import run_extended_sonya_p1_campaign_v5207 as sonya
ROOT,need,sha=old.ROOT,old.need,old.sha
NAME='diagnostic_v5219_current_payload_rom_metadata'
EXE_SHA='A6BC32F526C78A5BD72ED1960EAE56AB40701D7FE881D70A93E031AEB87AB944'
OUT=ROOT/'audit_v5226_current_metadata_native_startup_checked'
LUA='mk2ks_current_metadata_smoke_ram_v5220.lua'

def row_kind(line):
 return line.startswith(('MK2_NAT_CAMPAIGN_','MK2_MILEENA_CAMPAIGN_','MK2_BOSS_KNIFE_','MK2_CAMPAIGN_RAM_FRAME_DIGEST ','MK2_CAMPAIGN_GUEST_RAM_DIGEST '))and not line.startswith(
  ('MK2_NAT_CAMPAIGN_RESULT ','MK2_NAT_CAMPAIGN_FLOOR_RESULT ','MK2_MILEENA_CAMPAIGN_RESULT ','MK2_BOSS_KNIFE_RESULT '))

def main():
 need(not OUT.exists(),'Fresh immutable actual current metadata startup')
 guest=old.expected();candidate=ROOT/NAME
 build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
 prior=json.loads((ROOT/old.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 need(build['executable_sha256']==EXE_SHA==sha(candidate/'mkport_candidate.exe')and
  build['payload_sha256']==old.PAYLOAD_SHA==sha(candidate/'roms/mk2ks/mk2ks.mdata')and
  build['expected_guest_sha256']==old.GUEST_SHA and not build['game_data_changed']and
  not build['initialized_native_table_changed']and build['initialized_guest_byte_delta']==0,
  'Actual rebuilt executable, same immutable payload/initialized guest')
 changes={p:(prior['canonical_source_hashes_at_compile'][p],h)for p,h in build['canonical_source_hashes_at_compile'].items()
  if prior['canonical_source_hashes_at_compile'][p]!=h}
 need(len(changes)==1 and next(iter(changes)).endswith('/midtunit.cpp')and
  list(changes.values())==[('0094EAE7DC9D3AF85474F720A16054BCFA5DF654751E8DA9C3D105588E674363',
   '17FCD9D7C5D862FEB03487828364AC4126D9B0C7AB437DAEBD94F760DA11C0DE')],
  'Exactly one compiled-source CRC/SHA1 metadata change; every gameplay/render/audio source unchanged')
 restore=json.loads((candidate/'restoration.json').read_text(encoding='utf-8-sig'))
 need(restore['passed']and all(sha(p)==h for p,h in restore['restored_actual_preexisting_files'].items()),
  'Dirty preexisting sources and installed executable exactly restored')
 pins=dict(build['input_hashes'])
 for p in[Path(__file__).resolve(),ROOT/LUA,candidate/'build-info.json',candidate/'restoration.json',
  candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata']:
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every actual compilation/input byte intact')
 OUT.mkdir()
 command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-verifyroms','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms')]
 verify=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
 need(verify.returncode==0 and verify.stdout.replace('\r\n','\n')=='romset mk2ks [mk2] is good\n1 romsets found, 1 were OK.\n'and not verify.stderr and
  not re.search(r'wrong|warning|error',verify.stdout+verify.stderr,re.I),
  'Actual new native ROM verification, no checksum warning waiver')
 (OUT/'rom_verification.txt').write_text(verify.stdout+verify.stderr)
 cases=[]
 for fighter,reference in [('kano',kano),('sonya',sonya)]:
  folder=OUT/fighter;folder.mkdir()
  controls=[LUA,*reference.CONTROLLERS]
  for p in controls:pins[str((ROOT/p).resolve())]=sha(ROOT/p)
  for p in [Path(reference.__file__),reference.OUT/'result.json',reference.OUT/'run.log.gz']:
   pins[str(p.resolve())]=sha(p)
  env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
  env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE='1',MK2KS_CAMPAIGN_STRATEGY='zoning'if fighter=='kano'else'guard_punish',
   MK2KS_BOSS_PHYSICAL_POLICY='shao_knife_retreat'if fighter=='kano'else'shao_ring_retreat',
   MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900'if fighter=='kano'else'18000',MK2KS_TEST_BOOT_FRAME='600',
   MK2KS_CAMPAIGN_OUT=str(folder),MK2KS_TWO_PLAYER='0')
  command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
   '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000',
   '-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none','-noautoframeskip','-frameskip','0',
   '-nothrottle','-str','200','-snapsize','400x254','-cfg_directory',str(folder/'cfg'),
   '-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),
   '-autoboot_script',str(ROOT/LUA)]
  initialized=None;scenes=[];lines=[]
  with(folder/'stderr.log').open('w')as errors,subprocess.Popen(command,cwd=ROOT,env=env,
   stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8')as process:
   (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,hostPID=os.getpid(),command=command),indent=2)+'\n')
   print(f'{fighter}: actual new nativePID={process.pid}',flush=True)
   with gzip.open(folder/'run.log.gz','wt',encoding='utf-8',compresslevel=6)as log:
    for line in process.stdout:
     if line.startswith('MK2_CAMPAIGN_GUEST_RAM '):
      r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r.pop('hex'))
      need(initialized is None and r==dict(frame='1',bytes='1048576')and raw==guest,
       'Every actually initialized new native guest byte equals independently reconstructed tested guest')
      initialized=hashlib.sha256(raw).hexdigest().upper()
      line=f'MK2_CAMPAIGN_GUEST_RAM_DIGEST frame=1 bytes=1048576 sha256={initialized}\n'
     elif line.startswith('MK2_CAMPAIGN_RAM_FRAME '):
      r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r.pop('hex'))
      need(len(raw)==406400 and r['width']=='400'and r['height']=='254','Actual complete native RGB field in RAM')
      r['sha256']=hashlib.sha256(raw).hexdigest().upper();scenes.append(r)
      line='MK2_CAMPAIGN_RAM_FRAME_DIGEST '+' '.join(f'{k}={v}'for k,v in r.items())+'\n'
     need('hex='not in line,'No raw guest/raster/audio persisted')
     log.write(line);lines.append(line.rstrip())
   code=process.wait()
  text='\n'.join(lines)+'\n';stderr=(folder/'stderr.log').read_text()
  need(code==0 and initialized==old.GUEST_SHA and not stderr and
   not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I),
   'Actual new native startup and6000fields, with entirely empty stderr/no ignored warning')
  need(text.count('MK2_METADATA_SMOKE_STOP observed_fields=6000 writes=0 assistance=none')==1,'Actual read-only early-play stop')
  actual=[line for line in lines if row_kind(line)]
  with gzip.open(reference.OUT/'run.log.gz','rt')as reader:
   prior_lines=[line.rstrip()for line in reader if row_kind(line.rstrip())]
  need(actual==prior_lines[:len(actual)]and len(actual)>1000,'Every actual cold selection/ladder/gameplay/native guest/RGB event is exact tested chronology prefix')
  identity=17 if fighter=='kano'else 18
  need(any(line.startswith('MK2_NAT_CAMPAIGN_SELECT_ID ')and f'roster={identity} state=3'in line for line in actual)and
   any(line.startswith('MK2_NAT_CAMPAIGN_LIVE ')and f'human={identity}:{identity}'in line for line in actual),
   'Actual own selected/live identity, no proxy')
  need(scenes and not any(p.suffix.lower()in('.png','.wav','.bin')for p in folder.rglob('*')if p.is_file()),
   'Complete native RAM visual chronology and no guest/raster/audio dumps')
  cases.append(dict(fighter=fighter,physicalSlot=1,trueIdentity=identity,nativeExit=code,actualGuestSHA256=initialized,
   actualGuestBytesComparedInRAM=1048576,actualExactNativeChronologyRows=len(actual),actualNativeRGBFields=len(scenes),
   exactPriorCompleteChronologyPrefix=True,stderrEmpty=True,nativeChecksumWarningAbsent=True,actualObservedFields=6000,
   actualNativeSceneDigests=scenes))
  print(json.dumps({k:v for k,v in cases[-1].items()if k!='actualNativeSceneDigests'}),flush=True)
 for p in OUT.rglob('*'):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actual current/prior sources and terminal native records intact')
 report=dict(passed=True,candidate=NAME,executableSHA256=EXE_SHA,payloadSHA256=old.PAYLOAD_SHA,guestSHA256=old.GUEST_SHA,
  compiledSourceChanges=changes,actualNativeROMVerificationPassedWithoutWarnings=True,cases=cases,inputHashes=pins,
  actualPreexistingFilesExactlyRestored=True,metadataOnlyFixCompiledAndNativeStartupAccepted=True,
  actualNewCandidateTowerClearsAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
  rawGuestRasterAudioFilesWritten=0)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)

if __name__=='__main__':main()
