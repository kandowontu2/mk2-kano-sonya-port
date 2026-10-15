"""Actual3680 cold Sonya P2 campaign with the original throw input strategy.

Full campaign-state and actual boss-input replay are retained. A bounded
observation is never called a tower clear. Ending pixel/audio fidelity remains
separate; no new EXE, ROM, WAV, PNG or VRAM copies are written.
"""
import concurrent.futures,hashlib,json,os,re,shutil,subprocess,traceback
from pathlib import Path
import numpy as np
import verify_current_campaign_shao_knife_retreat_v3515 as knife
import verify_current_campaign_shao_ring_retreat_v3491 as ring
import run_native_sound_delivery_ram_v3682 as current

ROOT,need,sha,NAME=current.ROOT,current.need,current.sha,current.NAME
LUA='mk2ks_guarded_campaign_ram_v3743.lua'
OUT=ROOT/'audit_v3757_guarded_sonya_p2_throw_ram_observed'
COMPLETED=[]

def capture(fighter):
    policy=knife if fighter=='kano'else ring
    policy.source_boundary()
    folder=ROOT/f'audit_v3756_guarded_{fighter}_throw_p2_campaign'
    need(not folder.exists(),'Fresh leaf; do not restart or overwrite an executed run')
    candidate=ROOT/NAME;build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    files=set(map(Path,build['input_hashes']))|{candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'build-info.json',
      Path(__file__).resolve(),ROOT/LUA,ROOT/policy.DRIVER,ROOT/policy.BASELINE,ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin'}
    if fighter=='kano':files.add(ROOT/knife.policy.OBSERVER)
    for module in(knife,ring,knife.old,knife.policy,ring.policy,current):files.add(Path(module.__file__))
    for leaf in('roms/mk2ks','artwork','samples/mk2ks'):files.update((ROOT/leaf).glob('*'))
    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}
    need(all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items()),'Every actual compiled source bound')
    need(sha(candidate/'mkport_candidate.exe')=='BF5D90F90E6A254C4BCB63B4C0D3974C08DF9F28A817BD35A6F86FE68ABE6A41'and
      sha(candidate/'roms/mk2ks/mk2ks.mdata')=='ED9023949F73BD719F8BC688C69230C68239D7CC140F814C1A4E54A5BF561BC3','Exact compiled3680 executable and immutable payload')
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
    env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_TEST_BOOT_FRAME='600',MK2KS_TEST_CONFIRM='hp',MK2KS_TEST_CONFIRM_HOLD='8',
      MK2KS_TWO_PLAYER='0',MK2KS_CAMPAIGN_OUT=str(folder),MK2KS_CAMPAIGN_SIDE='2',
      MK2KS_CAMPAIGN_STRATEGY='throw',
      MK2KS_BOSS_PHYSICAL_POLICY='shao_knife_retreat'if fighter=='kano'else'shao_ring_retreat')
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat',
      '-inipath',str(folder),'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','3900',
      '-snapsize','400x254','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),
      '-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(ROOT/LUA)]
    headers=[];images={};stream=hashlib.sha256();byte_count=0
    with(folder/'stderr.log').open('w',encoding='utf-8')as errors,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:
        print(f'{fighter} P2 actual3680 campaign started pid={process.pid}',flush=True)
        with(folder/'run.log').open('w',encoding='utf-8')as log:
            for line in process.stdout:
                if line.startswith('MK2_CAMPAIGN_RAM_FRAME '):
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
                    if re.match(r'^MK2_NAT_CAMPAIGN_(STAGE|LOSS|ENDING_START|ENDING_COMPLETED|RESULT) ',line):
                        print(line.strip(),flush=True);log.flush()
        code=process.wait()
    need(all(sha(p)==h for p,h in pins.items()),'Every executed input unchanged')
    meta=dict(exit_code=code,candidate=NAME,executable_sha256=build['executable_sha256'],payload_sha256=build['payload_sha256'],
      player=fighter,human_slot=2,cpu_slot=1,boot_frame=600,seconds=3900,strategy=env['MK2KS_CAMPAIGN_STRATEGY'],boss_policy=env['MK2KS_BOSS_PHYSICAL_POLICY'],
      assistance='none',cheats_enabled=False,snapshot_schema=2,raw_audio_files_written=0,new_builds_or_rom_copies=0,input_hashes=pins,
      rawRasterFilesWritten=0,actualNativeFrameCallbacks=len(headers),nativeFrameBytesVerifiedInRAM=byte_count,
      nativeFrameStreamSHA256=stream.hexdigest().upper(),passed=False,unassisted_clear_proven=False,fullPortAcceptance=False)
    (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n')
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
        need((folder/'guest_maincpu.bin').read_bytes()==current.current.current.expected_current()[0],'Whole actual initialized guest independently reconstructed')
        COMPLETED.append(dict(capture=folder.name,terminal0=True,stages=[r['stage']for r in rows if r['tag']=='STAGE'],
          endingStarts=sum(r['tag']=='ENDING_START'for r in rows),endingCompletions=sum(r['tag']=='ENDING_COMPLETED'for r in rows),
          actualNativeFrameCallbacks=len(headers),fullIndependentCampaignVerificationPending=True))
    return dict(passed=True,observations=COMPLETED,candidate=NAME,rawRasterFilesWritten=0,rawAudioFilesWritten=0,
      newBuildsOrROMCopies=0,independentCampaignAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=COMPLETED,fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
