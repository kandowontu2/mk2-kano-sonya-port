"""Compiled3680 real CSS/ladder/first campaign fight, complete pixel gate in RAM.

Reuse the whole814 independent portrait/cursor/stance/backdrop/teardown/
ladder/name-shadow control and pixel contracts. The original physical probe
changes only its PNG sink. No raster/VRAM/ROM/EXE copies or guest-state writes.
"""
import concurrent.futures,hashlib,json,os,re,shutil,struct,subprocess,traceback
from pathlib import Path
import numpy as np
import verify_native_ui_flow_v814 as model
import run_native_sound_delivery_ram_v3682 as current

ROOT,need,sha,NAME=current.ROOT,current.need,current.sha,current.NAME
OUT=ROOT/'audit_v3731_guarded_native_ui_ram_checked'
LUA='mk2ks_guarded_ui_ram_v3728.lua'
COMPLETED_CASES=[]

def capture(fighter,side):
    folder=ROOT/f'audit_v3730_guarded_ui_{fighter}_p{side}'
    need(not folder.exists(),'Fresh UI leaf, never overwrite/restart executed capture')
    candidate=ROOT/NAME;build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    files=set(map(Path,build['input_hashes']))|{candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'build-info.json',
      Path(__file__).resolve(),Path(model.__file__).resolve(),ROOT/LUA,ROOT/'mk2ks_native_ui_flow_v2_probe.lua',
      ROOT/'mk2/mk2-maincpu.bin',ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp',ROOT/'mame-mkp/src/emu/screen.cpp'}
    for leaf in('roms/mk2ks','artwork','samples/mk2ks'):files.update((ROOT/leaf).glob('*'))
    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}
    need(all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items())and
      pins[str((candidate/'mkport_candidate.exe').resolve())]=='BF5D90F90E6A254C4BCB63B4C0D3974C08DF9F28A817BD35A6F86FE68ABE6A41'and
      pins[str((candidate/'roms/mk2ks/mk2ks.mdata').resolve())]=='ED9023949F73BD719F8BC688C69230C68239D7CC140F814C1A4E54A5BF561BC3','Exact actual compiled3680 source/executable/payload')
    folder.mkdir();compressed=subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True,text=True)
    need(compressed.returncode==0,'New leaf inherited lossless compression')
    snapshots={}
    for p in files:
        need(p.is_relative_to(ROOT),'Workspace inputs only')
        if p.suffix in('.lua','.py','.ps1','.json'):
            dest=folder/'input_sources/tree'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,dest);need(sha(dest)==pins[str(p)],'Exact before-run hierarchy snapshot');snapshots[str(p)]=str(dest)
    (folder/'source_snapshot_paths.json').write_text(json.dumps(snapshots,indent=2)+'\n')
    (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_UI_FIGHTER=fighter,MK2KS_UI_SIDE=str(side),MK2KS_UI_BOOT='604')
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat','-inipath',str(folder),
      '-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0','-nothrottle','-str','65',
      '-snapsize','400x254','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),
      '-autoboot_script',str(ROOT/LUA)]
    headers=[];images={};stream_hash=hashlib.sha256();byte_count=0
    with(folder/'stderr.log').open('w',encoding='utf-8')as errors,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:
        with(folder/'run.log').open('w',encoding='utf-8')as log:
            for line in process.stdout:
                if line.startswith('MK2_UI_RAM_FRAME '):
                    h=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(h.pop('hex'))
                    need(len(raw)==int(h['bytes'])==400*254*4 and h['width']=='400'and h['height']=='254','Whole native400x254 packedRGB32 frame')
                    need(h['filename']==f"ui_{int(h['frame']):04d}.png",'Original exact logical frame key')
                    h['sha256']=hashlib.sha256(raw).hexdigest().upper();headers.append(h);stream_hash.update(raw);byte_count+=len(raw)
                    value=np.frombuffer(raw,dtype=np.uint8).reshape(254,400,4)[:,:,2::-1].copy()
                    need(h['filename']not in images or np.array_equal(images[h['filename']],value),'Duplicate logical PNG sink has identical actual native pixels')
                    images[h['filename']]=value
                    log.write('MK2_UI_RAM_FRAME_DIGEST '+' '.join(f'{k}={v}'for k,v in h.items())+'\n')
                else:
                    need('hex='not in line and 'MK2_UI_RAM_FRAME 'not in line,'No raw/encoded raster or malformed frame enters disk log')
                    log.write(line)
        code=process.wait()
    log=(folder/'run.log').read_text();errors=(folder/'stderr.log').read_text()
    need(code==0 and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|WRONG CHECKSUMS',log+errors,re.I),'Terminal emulator/observer success')
    need(headers and all(float(a['seconds'])<=float(b['seconds'])for a,b in zip(headers,headers[1:])),'Actual native frame callbacks chronological')
    need(all(sha(p)==h for p,h in pins.items()),'Every executed input byte unchanged')
    meta=dict(exit_code=code,candidate=NAME,executable_sha256=build['executable_sha256'],payload_sha256=build['payload_sha256'],
      fighter=fighter,side=side,boot=604,assistance='none',cheats_enabled=False,input_hashes=pins,rawRasterFilesWritten=0,
      actualNativeFrameCallbacks=len(headers),actualUniqueNativeFrames=len(images),nativeFrameBytesVerifiedInRAM=byte_count,
      nativeFrameStreamSHA256=stream_hash.hexdigest().upper(),passed=False,fullPortAcceptance=False)
    (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(f'{fighter} P{side} UI terminal0, {len(images)} complete native frames retained only in RAM',flush=True)
    return folder,log,headers,images

def case(fighter,side):
    folder,log,headers,images=capture(fighter,side)
    guest=current.current.current.expected_current()[0]
    for row in model.records(log,'CODE'):
        first,last=model.h(row,'start'),model.h(row,'stop');raw=b''.join(struct.pack('<H',int(w,16))for w in row['words'].split(','))
        need(raw==guest[(first-0xff800000)//8:(last-0xff800000)//8],'Every observed UI guest-table byte independently reconstructed')
    state=model.verify_log(log,fighter,side)
    snapshots=model.records(log,'SNAP')
    need([r['file']for r in snapshots]==[h['filename']for h in headers],'Every original PNG call captured once in RAM, no omitted/reordered frame')
    pixels=model.render(folder,log,fighter,side,load=lambda name:images[name])
    old=(ROOT/f'audit_v3196_ui_{fighter}_p{side}'/'run.log').read_text(encoding='utf-8-sig')
    select=lambda t:[line for line in t.splitlines()if line.startswith('MK2_UI_')and not line.startswith('MK2_UI_RAM_')]
    need(select(log)==select(old),'All original3196 physical/table/selection/ladder/true-ID/first-match records retained on3680')
    result=dict(passed=True,fighter=fighter,side=side,capture=folder.name,state=state,rendered=pixels,
      actualNativeFrameCallbacks=len(headers),actualUniqueNativeFrames=len(images),rawRasterFilesWritten=0)
    COMPLETED_CASES.append(result)
    print(f'{fighter} P{side} complete independent cursor/number/animation/backdrop/clear/ladder/name-shadow pixels passed',flush=True)
    return result

def run():
    need(not OUT.exists(),'Fresh immutable UI gate')
    wrapper=(ROOT/LUA).read_text();need(wrapper.count('screen:snapshot(name)')==1 and wrapper.count('_ui_emit(name,frame)')==1 and
      not re.search(r':write_|set_value|clear_value|\.value\s*=(?!=)',wrapper),'Only original snapshot sink adaptation, no controls or game writes')
    need(sha(ROOT/'roms/mk2ks/mk2ks.ui')==model.UI_SHA and sha(ROOT/'mk2/mk2-maincpu.bin')==model.ORIGINAL_SHA,'Independent original/UI source assets')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        cases=list(pool.map(lambda pair:case(*pair),[(fighter,side)for fighter in('kano','sonya')for side in(1,2)]))
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for c in cases:
        folder=ROOT/c['capture'];meta=json.loads((folder/'result.json').read_text())
        for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'Consistent actual UI input pins');pins[p]=h
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
        path=ROOT/f"audit_v3196_ui_{c['fighter']}_p{c['side']}"/'run.log';pins[str(path)]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'All executed source/evidence unchanged')
    return dict(passed=True,candidate=NAME,cases=cases,inputHashes=pins,currentBothSlotSelectionLadderFirstMatchPixelsAccepted=True,
      observedUITablesExactlyIndependentGuest=True,wholeActualGuestCapturedByThisUIProbe=False,
      fullLaddersAccepted=False,allCinematicsAccepted=False,audioAccepted=False,fullPortAcceptance=False,rawRasterFilesWritten=0,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED_CASES,fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable result');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes','completedCases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
