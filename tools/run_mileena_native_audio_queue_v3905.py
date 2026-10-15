"""3836 swallowing full PCM/DCS delivery with actual native queue branches.

Actual added-character contexts retain original3824 controls and real17/18.
No stock identity is substituted or labelled as an added-character run.
All waveform samples and initialized guests remain only in verifier RAM.
"""
import hashlib,json,os,re,shutil,subprocess,traceback
from pathlib import Path
import numpy as np
import verify_native_mileena_victim_data_v3819 as data
import verify_mileena_identity_runtime_v3842 as state
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
NAME='diagnostic_v3836_native_mileena_rom_identity'
OUT=ROOT/'audit_v3907_mileena_native_audio_queue_observed'
COMPLETED=[]

def rows(text,tag):
    return[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_MAUDIO_'+tag+' ')]

def expected():
    base,_,payload,_,_=data.old.expected_current()
    return data.check(payload,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes(),base,json.loads((ROOT/'art_reference_mileena_v3801/reference.json').read_text()))[0]

def capture(fighter,side,enabled,guest):
    suffix='samples'if enabled else'nosamples';folder=ROOT/f'audit_v3906_mileena_{fighter}_p{side}_audio_queue_{suffix}'
    need(not folder.exists(),'Fresh immutable actual capture')
    need(fighter in('kano','sonya'),'Only real added-character contexts')
    reference=False;lua='mk2ks_mileena_audio_queue_ram_v3904.lua'
    controller='mk2ks_mileena_stock_reference_v3896.lua'if reference else'mk2ks_mileena_earned_fixed_v3824.lua'
    candidate=ROOT/NAME;build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    files={Path(p)for p in build['input_hashes']}|{candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'build-info.json',
        Path(__file__).resolve(),ROOT/lua,ROOT/controller,ROOT/'mk2ks_cache_provenance_mileena_fixed_v3823.lua',ROOT/'mame-mkp/src/mame/shared/dcs.cpp',
        ROOT/'mame-mkp/src/emu/sound.cpp',ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp',ROOT/'mame-mkp/src/devices/sound/samples.cpp',Path(state.__file__),Path(data.__file__)}
    for leaf in('roms/mk2ks','samples/mk2ks','artwork'):files.update((ROOT/leaf).glob('*'))
    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}
    need(all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items())and
         sha(candidate/'mkport_candidate.exe')==build['executable_sha256']=='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'and
         sha(candidate/'roms/mk2ks/mk2ks.mdata')==build['payload_sha256']=='91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24','Actual3836 compiled executable/payload/all source bytes')
    folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,'Capture compressed before writes')
    frozen={}
    for p in files:
        if p.suffix in('.lua','.py','.ps1','.json'):
            dest=folder/'input_sources/tree'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);need(sha(dest)==pins[str(p)],'Exact executed hierarchy snapshot');frozen[str(p)]=str(dest)
    (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n');(folder/'source_snapshot_paths.json').write_text(json.dumps(frozen,indent=2)+'\n')
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_TEST_BOOT_FRAME='600',MK2KS_TEST_CONFIRM='hp',MK2KS_TEST_CONFIRM_HOLD='8',
        MK2KS_TWO_PLAYER='1',MK2KS_CAMPAIGN_OUT=str(folder),MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_PROVENANCE_MIN_FRAME='0')
    cmd=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(ROOT/'samples'),
        '-samples'if enabled else'-nosamples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat','-inipath',str(folder),
        '-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0','-nothrottle','-str','150',
        '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(ROOT/lua)]
    chunks=[];headers=[];guest_sha=None
    with(folder/'stderr.log').open('w',encoding='utf-8')as errors,subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:
        (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=cmd),indent=2)+'\n');print(f'{fighter}P{side} {suffix} actual native audio pid={process.pid}',flush=True)
        with(folder/'run.log').open('w',encoding='utf-8')as log:
            for line in process.stdout:
                if line.startswith('MK2_BBAUDIO_PCM '):
                    h=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(h.pop('hex'))
                    need(len(raw)==int(h['bytes'])and len(raw)%4==0,'Whole native stereo PCM update')
                    h['sha256']=hashlib.sha256(raw).hexdigest().upper();chunks.append(raw);headers.append(h)
                    log.write('MK2_BBAUDIO_PCM_DIGEST '+' '.join(f'{k}={v}'for k,v in h.items())+'\n')
                elif line.startswith('MK2_MAUDIO_GUEST '):
                    h=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(h.pop('hex'));need(guest_sha is None and raw==guest and len(raw)==1048576,'Every initialized actual guest byte in RAM')
                    guest_sha=hashlib.sha256(raw).hexdigest().upper();log.write('MK2_MAUDIO_GUEST_DIGEST sha256='+guest_sha+'\n')
                else:
                    need('hex='not in line,'No raw audio or ROM encoded data written to disk');log.write(line)
                    if re.match(r'^MK2_MAUDIO_(BEGIN|RESULT) ',line):log.flush();print(line.strip(),flush=True)
        code=process.wait()
    text=(folder/'run.log').read_text();errors=(folder/'stderr.log').read_text()
    need(all(sha(p)==h for p,h in pins.items()),'All executed inputs unchanged')
    pcm=b''.join(chunks)
    meta=dict(exit_code=code,candidate=NAME,fighter=fighter,side=side,samples_enabled=enabled,stockReferenceOnly=reference,
        executable_sha256=build['executable_sha256'],payload_sha256=build['payload_sha256'],input_hashes=pins,guestSHA256=guest_sha,
        mixedPCMBytesVerifiedInRAM=len(pcm),mixedPCMUpdates=len(headers),mixedPCMSHA256=hashlib.sha256(pcm).hexdigest().upper(),
        rawAudioRasterVRAMROMCopiesWritten=0,assistance='none',guest_writes=0,fullPortAcceptance=False)
    (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n')
    need(code==0 and guest_sha and headers and not re.search(r'LUA ERROR|stack traceback|fatal error|WRONG CHECKSUMS|might not run correctly',text+errors,re.I),'Actual native terminal/observer/whole guest success')
    need(all(float(a['seconds'])<float(b['seconds'])for a,b in zip(headers,headers[1:])),'Every actual sound update chronological')
    need(not list(folder.rglob('*.png'))and not list(folder.rglob('*.wav'))and not list(folder.rglob('guest*.bin')),'No ordinary runtime raster/audio/ROM copies')
    return folder,headers,np.frombuffer(pcm,dtype='<i2').reshape(-1,2).copy()

def pair(fighter,side,guest):
    folder,headers,a=capture(fighter,side,True,guest);baseline,oldheaders,b=capture(fighter,side,False,guest)
    text=(folder/'run.log').read_text();oldtext=(baseline/'run.log').read_text()
    original=lambda t:[s for s in t.splitlines()if s.startswith(('MK2_MILEENA_V3784_','MK2_CACHE_V3823_'))]
    need(original(text)==original(oldtext),'All actual physical inputs/native health/finisher/group/removal state identical samples on/off')
    timeline=lambda hs:[{k:v for k,v in h.items()if k!='sha256'}for h in hs]
    need(timeline(headers)==timeline(oldheaders)and a.shape==b.shape and np.array_equal(a,b),'Every complete native PCM sample unchanged by imported samples; no phantom FFF7..FFFE playback')
    for tag in('BEGIN','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','RESULT'):need(rows(text,tag)==rows(oldtext,tag),'Actual native '+tag+' inventory unchanged')
    begin=rows(text,'BEGIN');end=rows(text,'RESULT');need(len(begin)==len(end)==1,'One actual audio origin and terminal')
    origin=int(begin[0]['origin']);need(end[0]['origin']==str(origin)and int(end[0]['frame'])==origin+601 and
        int(headers[0]['frame'])in(origin,origin+1)and int(headers[-1]['frame'])==origin+600,'Complete native fatality through600 sound fields and original601 exit')
    if fighter in('kano','sonya'):
        typed=state.gate(state.parse(text),fighter,side);need(typed['passed'],'Full original true-ID/earned/native swallowing state gate '+repr(typed))
    else:
        typed=dict(stockReferenceOnly=True,fighter=fighter,identity=1 if fighter=='liu'else 4)
        action=[r for r in state.parse(text)if r['tag']=='ACTION'];need(len(action)==1 and action[0]['damage']==322 and action[0]['gap']<=69,'Separate stock reference also earns two actual KOs and native fatality')
    channels=rows(text,'CHANNEL');need(len(channels)==14*600 and len({(r['frame'],r['channel'])for r in channels})==len(channels)and
        all(int(r['sample'])==0xffffffff and r['paused']==r['loop']=='0'for r in channels),'All14sample channels genuinely idle through600callbacks')
    writes=rows(text,'SOUND');deliveries=rows(text,'DELIVERY');native=[r for r in writes if r['pc']in('FFA13C90','FFA13D60')]
    matched=[]
    for i,write in enumerate(native):
        first=float(write['seconds']);last=float(native[i+1]['seconds'])if i+1<len(native)else first+.1
        hits=[r for r in deliveries if first<=float(r['seconds'])<last and int(r['word'],16)==int(write['word'],16)&255]
        need(hits,'Every genuine DCS byte actually read before following write');matched.append(dict(write=write,dspRead=hits[0]))
    need(native and np.any(a!=0),'Native packet delivery and non-silent actual native waveform, not a disabled sound engine')
    routes=rows(text,'ROUTE');codes=[int(r['a0'],16)for r in routes if r['entry']=='FFA12530']
    need(all(code in codes for code in(0x60,0xc9,0xc3)),'All original native swallowing/music-stop/effect codes actually dispatch')
    summary=dict(passed=True,fighter=fighter,side=side,capture=folder.name,baseline=baseline.name,origin=origin,terminalFrame=origin+601,
        state=typed,nativeDeliveredBytes=len(matched),nativeDispatchCodes=codes,nonzeroNativePCMSamples=int(np.count_nonzero(a)),
        fullNativeMixedSamples=len(a),samplesOnOffNativePCMExactlyEqual=True,rawAudioFilesWritten=0,
        sourceQualifiedNativeDCSWaveformReferencePending=True,fullPortAcceptance=False)
    COMPLETED.append(summary);print(json.dumps({k:v for k,v in summary.items()if k!='state'}),flush=True)
    return summary,headers,a,text,matched

def run():
    need(not OUT.exists(),'Fresh matrix observation');guest=expected();collected=[]
    for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
        collected.append(pair(fighter,side,guest))
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for c in COMPLETED:
        for name in(c['capture'],c['baseline']):
            folder=ROOT/name;meta=json.loads((folder/'result.json').read_text())
            for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'Consistent exact actual matrix inputs');pins[p]=h
            for p in folder.rglob('*'):
                if p.is_file():pins[str(p)]=sha(p)
    return dict(passed=True,candidate=NAME,cases=COMPLETED,inputHashes=pins,
        actualOwnedContexts=4,separateStockAudioReferences=0,actualPairedCaptures=8,
        currentSwallowingDCSByteDeliveryAndNoPhantomImportedWaveformAccepted=True,
        originalStockWaveformFidelityAccepted=False,allFinisherAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=COMPLETED,fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable observation');OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compression')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','completed')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
