"""Actual3836 cold Sonya P2; native-grounded Ring/jump inputs versus Mileena and Shang.

Full campaign-state and actual boss-input replay are retained. A bounded
observation is never called a tower clear. Ending pixel/audio fidelity remains
separate; no new EXE, ROM, WAV, PNG or VRAM copies are written.
"""
import concurrent.futures,hashlib,json,os,re,shutil,subprocess,sys,traceback
from pathlib import Path
import numpy as np
import verify_current_campaign_shao_knife_retreat_v3515 as knife
import verify_current_campaign_shao_ring_retreat_v3491 as ring
import run_native_sound_delivery_ram_v3682 as current
import verify_native_mileena_victim_data_v3819 as data
import qualify_shang_jump_retry_source_v4301 as source

ROOT,need,sha,NAME=current.ROOT,current.need,current.sha,'diagnostic_v3836_native_mileena_rom_identity'
LUA='mk2ks_shang_jump_retry_campaign_ram_v4300.lua'
OUT=ROOT/'audit_v4305_shang_jump_retry_campaign_observed'
COMPLETED=[]

def expected():
    base_guest,_,base_payload,_,_=data.old.expected_current()
    return data.check(base_payload,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes(),base_guest,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))[0]

def capture(fighter):
    need(fighter=='sonya','Actual unfinished Sonya P2 context only')
    source.source_boundary()
    preflight=json.loads((ROOT/'audit_v4302_shang_jump_retry_source_preflight/report.json').read_text())
    need(preflight['passed'] and all(sha(p)==h for p,h in preflight['inputHashes'].items()),'Actual passed source preflight and unchanged executed policy before boot')
    guest=expected()
    policy=knife if fighter=='kano'else ring
    policy.source_boundary()
    folder=ROOT/f'audit_v4304_{fighter}_shang_jump_retry_p2_campaign'
    need(not folder.exists(),'Fresh leaf; do not restart or overwrite an executed run')
    candidate=ROOT/NAME;build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    files=set(map(Path,build['input_hashes']))|{candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'build-info.json',
      Path(__file__).resolve(),ROOT/LUA,ROOT/'mk2ks_mileena_campaign_trace_v3848.lua',ROOT/policy.DRIVER,ROOT/policy.BASELINE,ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',ROOT/'art_reference_mileena_v3801/reference.json'}
    if fighter=='kano':files.add(ROOT/knife.policy.OBSERVER)
    for module in(knife,ring,knife.old,knife.policy,ring.policy,current):files.add(Path(module.__file__))
    for module in tuple(sys.modules.values()):
        p=getattr(module,'__file__',None)
        if p and Path(p).suffix=='.py'and Path(p).resolve().is_relative_to(ROOT/'tools'):files.add(Path(p))
    for leaf in('roms/mk2ks','artwork','samples/mk2ks'):files.update((ROOT/leaf).glob('*'))
    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}
    need(all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items()),'Every actual compiled source bound')
    need(sha(candidate/'mkport_candidate.exe')=='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'and
      sha(candidate/'roms/mk2ks/mk2ks.mdata')=='91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24','Exact compiled3836 executable and immutable owned-victim payload')
    folder.mkdir();compressed=subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True,text=True)
    need(compressed.returncode==0,'Compression inherited before capture writes')
    snapshots={}
    for p in files:
        need(p.is_relative_to(ROOT),'Workspace input only')
        if p.suffix in('.lua','.py','.ps1','.json'):
            dest=folder/'input_sources/tree'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,dest);need(sha(dest)==pins[str(p)],'Exact hierarchy snapshot');snapshots[str(p)]=str(dest)
    (folder/'source_snapshot_paths.json').write_text(json.dumps(snapshots,indent=2)+'\n')
    (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_CAMPAIGN_OBSERVER_LIMIT='1500',MK2KS_TEST_FIGHTER=fighter,MK2KS_TEST_BOOT_FRAME='600',MK2KS_TEST_CONFIRM='hp',MK2KS_TEST_CONFIRM_HOLD='8',
      MK2KS_TWO_PLAYER='0',MK2KS_CAMPAIGN_OUT=str(folder),MK2KS_CAMPAIGN_SIDE='2',
      MK2KS_CAMPAIGN_STRATEGY='guard_punish',
      MK2KS_BOSS_PHYSICAL_POLICY='shao_knife_retreat'if fighter=='kano'else'shao_ring_retreat')
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat',
      '-inipath',str(folder),'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','1600',
      '-snapsize','400x254','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),
      '-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(ROOT/LUA)]
    headers=[];images={};stream=hashlib.sha256();byte_count=0;guest_sha=None
    with(folder/'stderr.log').open('w',encoding='utf-8')as errors,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:
        (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n')
        print(f'{fighter} P2 actual3836 campaign started pid={process.pid}',flush=True)
        with(folder/'run.log').open('w',encoding='utf-8')as log:
            for line in process.stdout:
                if line.startswith('MK2_CAMPAIGN_GUEST_RAM '):
                    h=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(h.pop('hex'))
                    need(guest_sha is None and h==dict(frame='1',bytes='1048576')and raw==guest,'Every byte of actual first-frame initialized guest independently reconstructed in RAM')
                    guest_sha=hashlib.sha256(raw).hexdigest().upper()
                    proof=dict(schema=1,frame=1,bytes=len(raw),sha256=guest_sha,everyActualByteComparedInRAM=True,
                      executableSHA256=pins[str((candidate/'mkport_candidate.exe').resolve())],payloadSHA256=pins[str((candidate/'roms/mk2ks/mk2ks.mdata').resolve())],
                      captureSourceSHA256=sha(__file__),transportSourceSHA256=sha(ROOT/LUA),guestDumpFilesWritten=0)
                    (folder/'guest_memory_proof.json').write_text(json.dumps(proof,indent=2)+'\n')
                    log.write('MK2_CAMPAIGN_GUEST_RAM_DIGEST frame=1 bytes=1048576 sha256='+guest_sha+'\n');log.flush()
                elif line.startswith('MK2_CAMPAIGN_RAM_FRAME '):
                    h=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(h.pop('hex'))
                    need(len(raw)==int(h['bytes'])==400*254*4 and h['width']=='400'and h['height']=='254','Complete actual native RGB32 frame')
                    h['sha256']=hashlib.sha256(raw).hexdigest().upper();stream.update(raw);byte_count+=len(raw)
                    rgb=np.frombuffer(raw,dtype=np.uint8).reshape(254,400,4)[:,:,2::-1].copy()
                    h['rgbSHA256']=hashlib.sha256(rgb.tobytes()).hexdigest().upper();headers.append(h)
                    images[h['filename']]=rgb
                    log.write('MK2_CAMPAIGN_RAM_FRAME_DIGEST '+' '.join(f'{k}={v}'for k,v in h.items())+'\n')
                else:
                    need('hex='not in line,'Never persist encoded raster')
                    log.write(line)
                    if re.match(r'^MK2_NAT_CAMPAIGN_(STAGE|LOSS|ENDING_START|ENDING_COMPLETED|RESULT) ',line)or re.match(r'^MK2_MILEENA_CAMPAIGN_(EATEN_TASK|DISAPPEAR|OVERRUN|RESULT) ',line):
                        print(line.strip(),flush=True);log.flush()
        code=process.wait()
    need(all(sha(p)==h for p,h in pins.items()),'Every executed input unchanged')
    meta=dict(exit_code=code,candidate=NAME,executable_sha256=build['executable_sha256'],payload_sha256=build['payload_sha256'],
      player=fighter,human_slot=2,cpu_slot=1,boot_frame=600,seconds=1600,observer_limit_seconds=1500,strategy=env['MK2KS_CAMPAIGN_STRATEGY'],boss_policy=env['MK2KS_BOSS_PHYSICAL_POLICY'],
      ramGuestSHA256=guest_sha,nativeGuestBytesVerifiedInRAM=1048576 if guest_sha else 0,guestDumpFilesWritten=0,
      assistance='none',cheats_enabled=False,snapshot_schema=2,raw_audio_files_written=0,new_builds_or_rom_copies=0,input_hashes=pins,
      rawRasterFilesWritten=0,actualNativeFrameCallbacks=len(headers),nativeFrameBytesVerifiedInRAM=byte_count,
      nativeFrameStreamSHA256=stream.hexdigest().upper(),passed=False,unassisted_clear_proven=False,fullPortAcceptance=False)
    (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n')
    need(guest_sha and not list(folder.rglob('guest*.bin')),'One full-byte-verified actual RAM guest and no guest dump')
    need(code==0 and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|WRONG CHECKSUMS',
      (folder/'run.log').read_text()+(folder/'stderr.log').read_text(),re.I),'Terminal emulator/observer success')
    print(f'{fighter} P2 terminal0; {len(headers)} native frames only in RAM',flush=True)
    return folder,headers,images

def run():
    need(not OUT.exists(),'Fresh immutable observation report')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        results=list(pool.map(capture,('sonya',)))
    for folder,headers,images in results:
        rows=knife.old.parse((folder/'run.log').read_text(),2,json.loads((folder/'result.json').read_text())['player'])
        need(json.loads((folder/'guest_memory_proof.json').read_text())['sha256']==hashlib.sha256(expected()).hexdigest().upper(),'Actual full-byte RAM comparison proof matches independently assembled guest')
        COMPLETED.append(dict(capture=folder.name,terminal0=True,stages=[r['stage']for r in rows if r['tag']=='STAGE'],
          endingStarts=sum(r['tag']=='ENDING_START'for r in rows),endingCompletions=sum(r['tag']=='ENDING_COMPLETED'for r in rows),
          actualNativeFrameCallbacks=len(headers),fullIndependentCampaignVerificationPending=True))
    return dict(passed=True,observations=COMPLETED,candidate=NAME,rawRasterFilesWritten=0,rawAudioFilesWritten=0,
      newBuildsOrROMCopies=0,independentCampaignAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=COMPLETED,fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writes');(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
