"""Current native blocked audio: four bounded captures, PCM only in verifier RAM."""
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import traceback
import wave
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
import verify_current_bicycle_block_push_v3382 as state

ROOT=state.ROOT;CANDIDATE=state.prior.current.current.CANDIDATE
OUT=ROOT/'audit_v3389_current_bicycle_block_audio_checked';need=state.need;sha=state.prior.current.assembly.sha

def capture(side,enabled):
    suffix='samples'if enabled else'nosamples';folder=ROOT/f'audit_v3388_current_bicycle_block_audio_p{side}_{suffix}'
    need(not folder.exists(),'Never overwrite or restart actual audio fixture')
    candidate=ROOT/CANDIDATE;build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    files=set(map(Path,build['input_hashes']))|{candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'build-info.json',Path(__file__).resolve(),
      ROOT/'mk2ks_human_special_negative_v9.lua',ROOT/'mk2ks_human_bicycle_block_trace_v3345.lua',ROOT/'mk2ks_human_bicycle_block_push_v3373.lua',
      ROOT/'mk2ks_human_bicycle_block_audio_v3386.lua',ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin',
      ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp',ROOT/'mame-mkp/src/emu/sound.cpp',ROOT/'mame-mkp/src/devices/sound/samples.cpp'}
    files.update((ROOT/'roms/mk2ks').glob('*'));files.update((ROOT/'artwork').glob('*'));files={p.resolve()for p in files if p.is_file()}
    pins={str(p):sha(p)for p in files}
    need(all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items()) and
         pins[str((candidate/'mkport_candidate.exe').resolve())]==state.prior.current.current.EXE and
         pins[str((candidate/'roms/mk2ks/mk2ks.mdata').resolve())]==state.prior.current.current.PAYLOAD,'Matched actual compiled build/input bytes')
    folder.mkdir();result=subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True,text=True)
    need(result.returncode==0,'Enable inherited lossless capture compression')
    snapshots={}
    for p in files:
        need(p.is_relative_to(ROOT),'Workspace inputs only')
        if p.suffix in ('.lua','.ps1','.json','.py'):
            destination=folder/'input_sources/tree'/p.relative_to(ROOT);destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,destination);need(sha(destination)==pins[str(p)],'Exact full-hierarchy before-run snapshot');snapshots[str(p)]=str(destination)
    (folder/'source_snapshot_paths.json').write_text(json.dumps(snapshots,indent=2)+'\n')
    (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_HUMAN_SPECIAL_MOVE='bicycle',MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_SCENARIO='block',
               MK2KS_HUMAN_SPECIAL_VICTIM='kano',MK2KS_BBLOCK_OUT=str(folder))
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-oslog','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(ROOT/'samples'),'-samples'if enabled else'-nosamples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat',
      '-inipath',str(folder),'-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0','-nothrottle','-str','65',
      '-snapsize','400x254','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),
      '-autoboot_script',str(ROOT/'mk2ks_human_bicycle_block_audio_v3386.lua')]
    chunks=[];headers=[]
    with subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='strict')as process:
        with (folder/'run.log').open('w',encoding='utf-8')as log:
            for line in process.stdout:
                if line.startswith('MK2_BBAUDIO_PCM '):
                    fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('hex'))
                    need(len(raw)==int(fields['bytes']) and len(raw)%4==0,'Exact actual stereo PCM update size')
                    fields.update(sha256=hashlib.sha256(raw).hexdigest().upper());headers.append(fields);chunks.append(raw)
                    # No raw or encoded PCM enters any disk file, even run.log.
                    log.write('MK2_BBAUDIO_PCM_DIGEST '+' '.join(f'{k}={v}'for k,v in fields.items())+'\n')
                else:log.write(line)
        code=process.wait()
    need(code==0 and not re.search(r'LUA ERROR|stack traceback|Fatal error|access violation',(folder/'run.log').read_text(),re.I),'Terminal emulator and observer success')
    need(headers and all(float(a['seconds'])<float(b['seconds'])for a,b in zip(headers,headers[1:])),'Every actual generated sound update chronological')
    for file,digest in pins.items():need(sha(file)==digest,'Executed input bytes unchanged')
    pcm=b''.join(chunks);digest=hashlib.sha256(pcm).hexdigest().upper()
    meta=dict(exit_code=code,candidate=CANDIDATE,executable_sha256=build['executable_sha256'],payload_sha256=build['payload_sha256'],
              move='bicycle',side=side,scenario='block',victim='kano',cheats_enabled=False,assistance='none',snapshot_schema=2,
              samples_enabled=enabled,samplerate=48000,rawAudioFilesWritten=0,mixedPCMBytesVerifiedInRAM=len(pcm),mixedPCMUpdates=len(headers),
              mixedPCMSHA256=digest,input_hashes=pins,passed=False,fullPortAcceptance=False)
    (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(folder.name+' terminal0; mixed PCM retained only in RAM ('+str(len(pcm))+' bytes)',flush=True)
    return folder,headers,np.frombuffer(pcm,dtype='<i2').reshape(-1,2).astype(np.float64)

def pair(side):
    enabled=capture(side,True);disabled=capture(side,False)
    folder,headers,a=enabled;base,oldheaders,b=disabled
    timeline=lambda hs:[{k:v for k,v in h.items()if k!='sha256'}for h in hs]
    need(timeline(headers)==timeline(oldheaders) and a.shape==b.shape,'Every enabled/disabled actual mixed sound update exactly aligned')
    log=(folder/'run.log').read_text();oldlog=(base/'run.log').read_text()
    selected=lambda text:[s for s in text.splitlines()if s.startswith(('MK2_HSPECIAL_','MK2_BBLOCK_','MK2_BBPUSH_'))]
    previous=(ROOT/f'audit_v3375_current_bicycle_block_push_p{side}_kano'/'run.log').read_text(encoding='utf-8-sig')
    need(selected(log)==selected(oldlog)==selected(previous),'Whole native input/state/push events unchanged with and without sample playback')
    guest=state.prior.current.expected_current()[0];typed=state.prior.phase(log,guest,side);movement=state.verify(log,guest,side,typed)
    need((folder/'guest_maincpu.bin').read_bytes()==(base/'guest_maincpu.bin').read_bytes()==guest,'Every independently assembled actual guest byte')
    record=lambda text,tag:[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_BBAUDIO_'+tag+' ')]
    marks=[r for r in record(log,'SOUND')if r['word']in ('6B01','6B02')]
    need([r['word']for r in marks]==['6B01','6B02'] and all(int(r['frame'])==typed['start']for r in marks),'Exactly both original owned startup sound markers')
    need(record(log,'SOUND')==record(oldlog,'SOUND'),'Entire native DCS/marker inventory unchanged; no arbitrary music acceptance')
    names=('sonya_bicycle_launch','sonya_bicycle_cry');voices=[];assets=[]
    for name in names:
        path=ROOT/'samples/mk2ks'/(name+'.wav')
        with wave.open(str(path),'rb')as wav:
            need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate())==(1,2,48000),'Pinned full original cue format')
            voice=np.frombuffer(wav.readframes(wav.getnframes()),'<i2').astype(np.float64)
        voices.append(voice);assets.append(dict(name=name,frames=len(voice),sha256=sha(path)))
    donor=np.zeros(max(map(len,voices)))
    for v in voices:donor[:len(v)]+=v
    delta=a-b;need(np.array_equal(delta[:,0],delta[:,1]),'Actual new cue contribution is original dual mono')
    signal=delta[:,0];product=fftconvolve(signal,donor[::-1],mode='valid');offset=int(np.argmax(product))
    actual=signal[offset:offset+len(donor)];gain=float(np.dot(actual,donor)/np.dot(donor,donor))
    corr=float(np.dot(actual,donor)/(np.linalg.norm(actual)*np.linalg.norm(donor)))
    need(corr>.999 and .699<gain<.701,'Entire actual mixed original launch and cry at compiled native .70 route')
    need(not np.any(signal[:offset]) and not np.any(signal[offset+len(donor)+2:]),'No extra cue contribution before launch or beyond complete native tails')
    start_seconds=float(headers[0]['seconds'])-int(headers[0]['bytes'])/4/48000
    onset=start_seconds+offset/48000;need(abs(onset-float(marks[0]['seconds']))<.0001,'Actual mixed cue onset synchronized with native startup marker')
    channels=record(log,'CHANNEL');owners=record(log,'OWNER');by={(int(r['frame']),int(r['channel'])):r for r in channels}
    ownerby={(int(r['frame']),int(r['slot'])):r for r in owners};final=int(record(log,'RESULT')[0]['frame']);frames=range(1450,final+1)
    need(len(by)==len(channels)==4*len(frames) and len(ownerby)==len(owners)==2*len(frames),'Every original full channel and physical-owner callback')
    first=typed['start']+1;own=next(r for r in state.prior.rows(log,'FIELD')if r['slot']==side)
    basechannel=10+(side-1)*2;completed=[]
    for channel in range(10,14):
        stream=[by[f,channel]for f in frames]
        need(all(r['loop']==r['paused']==r['writes']=='0'for r in stream),'Finite unpaused native channels, no item writes')
        if channel not in (basechannel,basechannel+1):need(all(r['length']=='0'for r in stream),'Opponent physical channels never play')
        else:
            length=assets[channel-basechannel]['frames'];active=[r for r in stream if int(r['length'])>0]
            need(active and int(active[0]['frame'])==first and all(int(r['length'])==length for r in active),'Whole correct cue begins on its actual physical channel')
            positions=[float(r['pos'])for r in active]
            need(all(x<=y for x,y in zip(positions,positions[1:]))and positions[-1]>=length,'Full finite cue reaches its actual final source sample')
            completed.append(next(int(r['frame'])for r in active if float(r['pos'])>=length))
    need(ownerby[first,side]['actor']==f"{own['actor']:08X}"and ownerby[first,side]['main']==f"{own['main']:08X}"and ownerby[first,side]['health']=='161','Own actual Sonya audio owner, not proxy')
    for f in frames:
        for n in(1,2):
            r=ownerby[f,n];need(r['writes']=='0','Read-only owner ledger')
            if n!=side or f<first or f>=max(completed)+3:need(r['actor']==r['main']=='00000000'and r['health']=='0','Other owner clear and own complete finite cleanup')
            elif r['actor']!='00000000':need(r['actor']==f"{own['actor']:08X}"and r['main']==f"{own['main']:08X}"and r['health']=='161','Whole playback remains owned by genuine selected body')
    need(all(r['length']=='0'for r in record(oldlog,'CHANNEL')),'Disabled-sample baseline truly contains no imported launch playback')
    return dict(passed=True,side=side,case=folder.name,baseline=base.name,state=typed,movement=movement,assets=assets,
                mixedPCMUpdates=len(headers),mixedPCMSamples=len(a),fullCueSamples=len(donor),correlation=corr,gain=gain,
                onsetSeconds=onset,markerSeconds=float(marks[0]['seconds']),completedFrames=completed,
                fullCapturedOriginalCuesAndFiniteOwnershipAccepted=True,rawAudioFilesWritten=0,fullPortAcceptance=False)

def run():
    need(not OUT.exists(),'Immutable new audio proof')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:cases=list(pool.map(pair,(1,2)))
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for c in cases:
        for name in(c['case'],c['baseline']):
            folder=ROOT/name;meta=json.loads((folder/'result.json').read_text())
            for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'Consistent actual audio input');pins[p]=h
            for p in folder.rglob('*'):
                if p.is_file():pins[str(p)]=sha(p)
    for p,h in pins.items():need(sha(p)==h,'Captured inputs unchanged after exact in-memory verification')
    return dict(passed=True,candidate=CANDIDATE,physicalSlots=2,cases=cases,inputHashes=pins,
                fullCapturedBlockedBicycleLaunchAudioAndOwnershipAccepted=True,
                rawAudioFilesWritten=0,newBuildsOrROMCopies=0,allMoveOrCPUOrArenaAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite audio results');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in ('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
