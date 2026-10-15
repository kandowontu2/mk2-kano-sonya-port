"""Actual natural CPU Bicycle hit audio, RAM-only paired mixed PCM."""
import importlib
import inspect
import json
import re
import subprocess
import traceback
import wave
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
import run_current_bicycle_block_audio_v3390 as base
import verify_current_cpu_square_v3280 as current
import native_cpu_bicycle_hit_contract_v3317 as phase
import verify_native_cpu_mobility_inventory_v3038 as choices

ROOT=base.ROOT;OUT=ROOT/'audit_v3399_current_cpu_bicycle_hit_audio_checked'
need=base.need;sha=base.sha
OLD=ROOT/'audit_v3308_current_cpu_bicycle_launch_jump'

def capture(enabled):
    # Retain the already-executed collector's PCM isolation and input snapshots.
    # Only select the genuine CPU input driver, evidence leaf and run duration.
    source=inspect.getsource(base.capture)
    changes={
      "audit_v3391_current_bicycle_block_audio_p{side}_{suffix}":"audit_v3398_current_cpu_bicycle_hit_audio_p{side}_{suffix}",
      "ROOT/'mk2ks_human_special_negative_v9.lua',ROOT/'mk2ks_human_bicycle_block_trace_v3345.lua',ROOT/'mk2ks_human_bicycle_block_push_v3373.lua',\n      ROOT/'mk2ks_human_bicycle_block_audio_v3386.lua'":
      "*[ROOT/n for n in ('mk2ks_physical_p2_cpu_continuation_v3300.lua','mk2ks_physical_p2_cpu_round_trace_v3301.lua','mk2ks_physical_p2_cpu_overlap_trace_v3302.lua','mk2ks_physical_p2_cpu_choice_trace_v3303.lua','mk2ks_physical_p2_cpu_square_trace_v3304.lua','mk2ks_native_cpu_audio_mobility_v3395.lua','mk2ks_cpu_bicycle_hit_audio_v3396.lua')],Path(base.__file__).resolve()",
      "env.update(MK2KS_HUMAN_SPECIAL_MOVE='bicycle',MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_SCENARIO='block',\n               MK2KS_HUMAN_SPECIAL_VICTIM='kano',MK2KS_BBLOCK_OUT=str(folder))":
      "env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='613',MK2KS_TEST_CONFIRM='hp',MK2KS_TEST_CONFIRM_HOLD='8',MK2KS_TWO_PLAYER='0',MK2KS_CPU_PAIR_APPROACH='guard_until_close',MK2KS_CPU_CONTINUATION_POLICY='jump_on_launch',MK2KS_CPU_PAIR_CONFIRM_AGE='264',MK2KS_FLOOR_OUT=str(folder))",
      "'-str','65'":"'-str','95'",
      "ROOT/'mk2ks_human_bicycle_block_audio_v3386.lua'":"ROOT/'mk2ks_cpu_bicycle_hit_audio_v3396.lua'",
      "move='bicycle',side=side,scenario='block',victim='kano'":"move='bicycle',side=side,scenario='natural_cpu_hit',victim='kano',cpu_slot=2,human_slot=1",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Explicit single collector adaptation: '+before[:70])
        source=source.replace(before,after)
    namespace=dict(vars(base));namespace.update(__file__=__file__,base=base)
    exec(compile(source,__file__+'::unchanged_ram_collector','exec'),namespace)
    return namespace['capture'](2,enabled)

def records(log,tag):
    result=[]
    for line in log.splitlines():
        if line.startswith('MK2_BBAUDIO_'+tag+' '):
            fields=re.findall(r'(\w+)=([^\s]+)',line)
            need(len(fields)==len(dict(fields)),'Unambiguous actual audio fields')
            result.append(dict(fields))
    return result

def run():
    need(not OUT.exists(),'Never overwrite audio proof')
    mobility=(ROOT/'mk2ks_native_cpu_mobility_boundary_v3306.lua').read_text()
    need((ROOT/'mk2ks_native_cpu_audio_mobility_v3395.lua').read_text()==mobility.replace(
        "dofile('mk2ks_native_cpu_bicycle_display_v3305.lua')",
        "dofile('mk2ks_physical_p2_cpu_square_trace_v3304.lua')"),
        'Whole mobility observer retained; omit redundant raster capture only')
    enabled=capture(True);disabled=capture(False)
    folder,headers,a=enabled;baseline,oldheaders,b=disabled
    timeline=lambda hs:[{k:v for k,v in row.items() if k!='sha256'}for row in hs]
    need(timeline(headers)==timeline(oldheaders) and a.shape==b.shape,'All actual enabled/disabled mixed updates exactly aligned')
    log=(folder/'run.log').read_text();oldlog=(baseline/'run.log').read_text()
    select=lambda text:[line for line in text.splitlines() if line.startswith('MK2_') and
                        not line.startswith(('MK2_BBAUDIO_','MK2_CPU_RENDER_'))]
    original=(OLD/'run.log').read_text(encoding='utf-8-sig')
    # Render-only labels are deliberately excluded; exact input/state/RNG/health
    # and original mobility provenance remain the authoritative gameplay oracle.
    need(select(log)==select(oldlog)==select(original),'Every original natural input/CPU choice/state/HP event exactly retained')
    guest=current.expected_current()[0]
    need((folder/'guest_maincpu.bin').read_bytes()==(baseline/'guest_maincpu.bin').read_bytes()==guest,'Whole independently assembled actual guest bytes')
    typed=phase.verify(log,guest);native=choices.native_choices(log,guest,'kano')
    need(typed['start']==2663 and typed['hit']==2680 and typed['damage']==22 and typed['ready']==2742 and
         native[0]['move']=='bicycle' and native[0]['firstRandomResult']==134 and native[0]['nativeContact'],
         'Genuine native CPU branch/contact/recovery, not prescribed CPU or RNG')
    marks=[r for r in records(log,'SOUND')if r['word']in('6B01','6B02')]
    need([r['word']for r in marks]==['6B01','6B02'] and all(int(r['frame'])==2663 and
         r['a8']=='010350A0' and r['a13']=='0106BF30' for r in marks),'Exactly both owned native CPU Bicycle cue writes')
    need(records(log,'SOUND')==records(oldlog,'SOUND'),'Entire actual native DCS/marker command inventory unchanged')
    voices=[];assets=[]
    for name in ('sonya_bicycle_launch','sonya_bicycle_cry'):
        path=ROOT/'samples/mk2ks'/(name+'.wav')
        with wave.open(str(path),'rb')as wav:
            need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate())==(1,2,48000),'Actual retained cue format')
            voice=np.frombuffer(wav.readframes(wav.getnframes()),'<i2').astype(np.float64)
        voices.append(voice);assets.append(dict(name=name,frames=len(voice),sha256=sha(path)))
    donor=np.zeros(max(map(len,voices)))
    for voice in voices:donor[:len(voice)]+=voice
    delta=a-b;need(np.array_equal(delta[:,0],delta[:,1]),'Actual imported cue contribution dual mono')
    signal=delta[:,0];offset=int(np.argmax(fftconvolve(signal,donor[::-1],mode='valid')))
    actual=signal[offset:offset+len(donor)]
    gain=float(np.dot(actual,donor)/np.dot(donor,donor))
    corr=float(np.dot(actual,donor)/(np.linalg.norm(actual)*np.linalg.norm(donor)))
    need(corr>.999 and .699<gain<.701,'Full actual launch/cry playback at compiled .70 route')
    need(not np.any(signal[:offset]) and not np.any(signal[offset+len(donor)+2:]),'No premature or stale mixed cue contribution')
    onset=float(headers[0]['seconds'])-int(headers[0]['bytes'])/4/48000+offset/48000
    need(abs(onset-float(marks[0]['seconds']))<.0001,'Actual sound onset at native CPU launch')
    channels=records(log,'CHANNEL');owners=records(log,'OWNER');frames=range(2600,2931)
    by={(int(r['frame']),int(r['channel'])):r for r in channels}
    ob={(int(r['frame']),int(r['slot'])):r for r in owners}
    need(len(by)==len(channels)==4*len(frames) and len(ob)==len(owners)==2*len(frames),'Complete physical channel/owner ledgers')
    completed=[]
    for channel in range(10,14):
        stream=[by[f,channel]for f in frames]
        need(all(r['loop']==r['paused']==r['writes']=='0'for r in stream),'Unpaused finite channels, read-only observer')
        if channel<12:need(all(r['length']=='0'for r in stream),'Human physical sample channels remain unused')
        else:
            active=[r for r in stream if int(r['length'])>0];length=assets[channel-12]['frames']
            need(active and int(active[0]['frame'])==2664 and all(int(r['length'])==length for r in active),'Correct full cue on genuine CPU physical channel')
            positions=[float(r['pos'])for r in active]
            need(all(x<=y for x,y in zip(positions,positions[1:]))and positions[-1]>=length,'Complete sample reaches its finite end')
            completed.append(next(int(r['frame'])for r in active if float(r['pos'])>=length))
    for f in frames:
        for slot in (1,2):
            row=ob[f,slot];need(row['writes']=='0','Read-only audio owner ledger')
            active=slot==2 and 2664<=f<max(completed)
            if active:need((row['actor'],row['main'],row['health'])==('010350A0','0106BF30','161'),'Whole actual CPU sample lifetime bound to native Sonya body')
            elif slot==1 or f<2664 or f>=max(completed)+3:
                need(row['actor']==row['main']=='00000000'and row['health']=='0','No wrong-slot owner or stale completed owner')
    need(all(r['length']=='0'for r in records(oldlog,'CHANNEL')),'Disabled baseline has no imported playback')
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for leaf in (folder,baseline):
        meta=json.loads((leaf/'result.json').read_text())
        for file,digest in meta['input_hashes'].items():
            need(file not in pins or pins[file]==digest,'Consistent actual input pins');pins[file]=digest
        for path in leaf.rglob('*'):
            if path.is_file():pins[str(path)]=sha(path)
    pins[str(OLD/'run.log')]=sha(OLD/'run.log')
    for module in tuple(__import__('sys').modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).suffix=='.py'and Path(file).resolve().is_relative_to(ROOT/'tools'):
            pins[str(Path(file).resolve())]=sha(file)
    for file,digest in pins.items():need(sha(file)==digest,'All actual source/capture bytes unchanged')
    return dict(passed=True,candidate=base.CANDIDATE,cpuSlot=2,humanSlot=1,
        case=folder.name,baseline=baseline.name,phase=typed,assets=assets,
        mixedPCMUpdates=len(headers),mixedPCMSamples=len(a),correlation=corr,gain=gain,
        onsetSeconds=onset,markerSeconds=float(marks[0]['seconds']),completedFrames=completed,
        fullCapturedNaturalCPUBicycleLaunchCryPlaybackAndOwnershipAccepted=True,
        rawAudioFilesWritten=0,newBuildsOrROMCopies=0,allMoveCPUOrArenaAudioAccepted=False,
        fullNativeContactDCSWaveformAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable audio result');OUT.mkdir()
    path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    compact=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(compact.returncode==0 and sha(path)==digest,'Lossless report compression')
    print(json.dumps({k:v for k,v in value.items()if k not in('inputHashes','assets','phase')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
