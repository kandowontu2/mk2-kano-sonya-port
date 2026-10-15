"""Earned current Tomb victim routing and complete imported winner PCM.

Native DCS stage/victim waveform fidelity remains explicitly unaccepted.
No audio/raster/VRAM/build copies. Exact samples-on/off native timelines and
all physical control/true-ID/full-health input gates precede waveform checks.
"""
import hashlib
import inspect
import json
import re
import subprocess
import traceback
import wave
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
import run_current_bicycle_block_audio_v3390 as audio
import map_current_native_feature_coverage_v3590 as current
import native_tomb_drop_qualification_v3643 as native

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3663_current_tomb_audio_routing_checked'
LUA='mk2ks_current_tomb_audio_ram_v3660.lua'

def collector(fighter):
    source=inspect.getsource(audio.capture)
    edits={
      "folder=ROOT/f'audit_v3391_current_bicycle_block_audio_p{side}_{suffix}'":
        f"folder=ROOT/f'audit_v3662_current_{fighter}_tomb_audio_p{{side}}_{{suffix}}'",
      "ROOT/'mk2ks_human_special_negative_v9.lua',ROOT/'mk2ks_human_bicycle_block_trace_v3345.lua',":
        "ROOT/'mk2ks_native_stage_performer_v806.lua',ROOT/'mk2ks_stage_branch_provenance_v1722.lua',",
      "ROOT/'mk2ks_human_bicycle_block_push_v3373.lua',":
        "ROOT/'mk2ks_current_stage_ram_driver_v3594.lua',ROOT/'mk2ks_current_stage_provenance_v3595.lua',",
      "mk2ks_human_bicycle_block_audio_v3386.lua":LUA,
      "env.update(MK2KS_HUMAN_SPECIAL_MOVE='bicycle',MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_SCENARIO='block',\n               MK2KS_HUMAN_SPECIAL_VICTIM='kano',MK2KS_BBLOCK_OUT=str(folder))":
        f"env.update(MK2KS_STAGE_SIDE=str(side),MK2KS_STAGE_WINNER='{fighter}',MK2KS_STAGE_ARENA='1',MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(folder))",
      "'-str','65'":"'-str','900'",
      "move='bicycle',side=side,scenario='block',victim='kano'":
        f"move='native_tomb',side=side,scenario='earned',winner='{fighter}'",
    }
    for old,new in edits.items():
        expected=2 if old=='mk2ks_human_bicycle_block_audio_v3386.lua' else 1
        need(source.count(old)==expected,'Exact declared original collector adaptation: '+old)
        source=source.replace(old,new)
    scope=dict(audio.__dict__);scope['__file__']=str(Path(__file__).resolve())
    exec(compile(source,'<entire3390RAMcollector_stage_only_adaptations>','exec'),scope)
    return scope['capture'],hashlib.sha256(source.encode()).hexdigest().upper()

def rows(log,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_TAUDIO_'+tag+' ')]

def pair(fighter,side):
    capture,collector_hash=collector(fighter)
    folder,headers,a=capture(side,True);base,oldheaders,b=capture(side,False)
    log=(folder/'run.log').read_text();oldlog=(base/'run.log').read_text()
    selected=lambda s:[line for line in s.splitlines()if line.startswith('MK2_STAGE_')]
    need(selected(log)==selected(oldlog),'Every physical input, health, parser, native branch/field unchanged by sample playback')
    guest=current.current.expected_current()[0]
    need((folder/'guest_maincpu.bin').read_bytes()==(base/'guest_maincpu.bin').read_bytes()==guest,'Actual compiled whole guest independently reconstructed')
    contract=native.check_log(log,fighter,side,1,guest=guest)
    timeline=lambda hs:[{k:v for k,v in row.items()if k!='sha256'}for row in hs]
    need(timeline(headers)==timeline(oldheaders)and a.shape==b.shape,'Entire actual mixed audio update timeline aligned')
    need(rows(log,'SOUND')==rows(oldlog,'SOUND')and rows(log,'ROUTE')==rows(oldlog,'ROUTE'),'Native voice/DCS routes unchanged with imported samples disabled')
    beginning=rows(log,'BEGIN');need(len(beginning)==1,'One native Tomb audio origin')
    origin=int(beginning[0]['origin']);need(int(headers[0]['frame'])==origin and int(headers[-1]['frame'])==origin+650,'Complete native scene audio window')
    routes=rows(log,'ROUTE');screams=[r for r in routes if r['entry']=='FFA11FD0']
    victim=18 if fighter=='kano'else 17
    for scream in screams:
        need(int(scream['id'])==victim and scream['owner']==scream['a8'],'True owned victim scream, no identity proxy')
        frame=scream['frame'];dispatch=[r for r in routes if r['frame']==frame and r['a8']==scream['a8']]
        branch='FFA123B0'if victim==18 else'FFA122D0'
        need(any(r['entry']==branch for r in dispatch),'Actual own female/male native victim predicate branch')
        chosen=[int(r['a0'],16)for r in dispatch if r['entry']=='FFA12530']
        permitted=(0x32,0x33)if victim==18 else(0x34,0x35)
        need(any(index in permitted for index in chosen),'Original MK2 packed scream selects the proper gender range')
    # Only the native random-drop branch calls this late victim scream.
    drops=[r for r in native.records(log,'BRANCH')if r['entry']=='FF8EB290']
    need(len(screams)==len(drops),'Exactly native conditional late scream, no injected or omitted calls')
    marker='FFFE'if fighter=='kano'else'FFFD'
    marks=[r for r in rows(log,'SOUND')if r['word']==marker]
    need(len(marks)==1 and marks[0]['pc']=='FFFB7140','One true-ID winner announcement from native router')
    name=fighter+'_wins';asset=ROOT/'samples/mk2ks'/(name+'.wav')
    with wave.open(str(asset),'rb')as wav:
        need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate())==(1,2,48000),'Pinned original full winner cue format')
        donor=np.frombuffer(wav.readframes(wav.getnframes()),'<i2').astype(np.float64)
    delta=a-b;need(np.array_equal(delta[:,0],delta[:,1]),'Isolated imported contribution is dual mono')
    signal=delta[:,0];offset=int(np.argmax(fftconvolve(signal,donor[::-1],mode='valid')))
    actual=signal[offset:offset+len(donor)];gain=float(np.dot(actual,donor)/np.dot(donor,donor))
    correlation=float(np.dot(actual,donor)/(np.linalg.norm(actual)*np.linalg.norm(donor)))
    need(correlation>.999 and .209<gain<.211,'Complete original winner waveform at .30 times .70 route')
    need(not np.any(signal[:offset])and not np.any(signal[offset+len(donor)+2:]),'No imported residue outside the complete winner clip')
    start=float(headers[0]['seconds'])-int(headers[0]['bytes'])/4/48000
    onset=start+offset/48000;need(abs(onset-float(marks[0]['seconds']))<.0001,'Winner mixed onset synchronized to native marker')
    channels=rows(log,'CHANNEL');by={(int(r['frame']),int(r['channel'])):r for r in channels}
    frames=range(origin+1,origin+651)
    need(len(by)==len(channels)==14*len(frames),'Every physical sample channel in complete native scene window')
    need(all(r['loop']==r['paused']=='0'for r in channels),'All clips finite and unpaused')
    playing=[r for r in channels if int(r['length'])]
    need(playing and all(r['channel']=='0'and int(r['length'])==len(donor)for r in playing),'Only full winner source plays, no unrelated sample channels')
    need(max(float(r['pos'])for r in playing)>=len(donor)and all(by[origin+650,n]['length']=='0'for n in range(14)),'Complete clip and native channel cleanup')
    need(all(r['length']=='0'for r in rows(oldlog,'CHANNEL')),'Native DCS-only baseline has no imported playback')
    return dict(passed=True,fighter=fighter,side=side,capture=folder.name,baseline=base.name,
      collectorSHA256=collector_hash,inputContract=contract,origin=origin,lateVictimScreamCalls=len(screams),
      trueVictim=victim,winnerCue=dict(source=str(asset),sha256=sha(asset),samples=len(donor),gain=gain,correlation=correlation,onsetSeconds=onset),
      nativeDCSWaveformFidelityAccepted=False,rawAudioFilesWritten=0)

def run():
    need(not OUT.exists(),'Fresh immutable audio gate')
    source=(ROOT/LUA).read_text()
    need(not re.search(r':write_|set_value|clear_value|io\.open|snapshot\(|\.value\s*=(?!=)',source),'Read-only observer with RAM-only PCM transport')
    cases=[pair(fighter,1)for fighter in('kano','sonya')]
    pins={str(Path(__file__).resolve()):sha(__file__),str(ROOT/LUA):sha(ROOT/LUA)}
    for case in cases:
        for name in(case['capture'],case['baseline']):
            folder=ROOT/name;meta=json.loads((folder/'result.json').read_text())
            for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'Consistent actual source bindings');pins[p]=h
            for file in folder.rglob('*'):
                if file.is_file():pins[str(file)]=sha(file)
    need(all(sha(p)==h for p,h in pins.items()),'All captured inputs remain unchanged')
    return dict(passed=True,candidate=current.NAME,cases=cases,inputHashes=pins,
      currentTombP1NativeVictimRoutingAndCompleteWinnerMixAccepted=True,
      completeStageEffectOrVictimAudioFidelityAccepted=False,bothPlayerSlotsAccepted=False,
      fullPortAcceptance=False,rawAudioFilesWritten=0,newBuildsOrPlayableCopies=0,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite executed audio result');OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
