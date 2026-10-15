"""Compiled3680 real mirror selection/earned individual finishers and direct cues.

Original1166 physical controller, only PNG sink omitted. Preserve1674's entire
physical damage/parser/owner/alternate/fullpalette/FIFO/continue contract.
Complete audible cues are modeled with original MAME interpolation, native
channel preemption and independent concurrent kiss/fire/victim/winner voices.
No new executable/ROM/raster/VRAM/WAV copies or injected game state.
"""
import hashlib
import inspect
import json
import re
import textwrap
import traceback
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
import run_current_bicycle_block_audio_v3390 as audio
import run_native_sound_delivery_ram_v3682 as current
import verify_current_natural_mirror_finish_v1674 as physical
from verify_native_friendship_audio_v791 import existing_sample

ROOT,need,sha=current.ROOT,current.need,current.sha
NAME=current.NAME
OUT=ROOT/'audit_v3702_natural_mirror_audio_ram_checked'
LUA='mk2ks_natural_mirror_audio_ram_v3699.lua'
CHANNELS={0xfffc:0,0xfffb:0,0xfffe:0,0xfffd:0,0xfffa:1,0xfff9:1,0xfff8:2,0xfff7:3}

def collector(fighter):
    source=inspect.getsource(audio.capture)
    edits={
      "folder=ROOT/f'audit_v3391_current_bicycle_block_audio_p{side}_{suffix}'":f"folder=ROOT/f'audit_v3701_{fighter}_mirror_audio_p{{side}}_{{suffix}}'",
      "ROOT/'mk2ks_human_special_negative_v9.lua',ROOT/'mk2ks_human_bicycle_block_trace_v3345.lua',":
        "ROOT/'mk2ks_natural_mirror_finish_v1166.lua',ROOT/'mk2ks_natural_mirror_no_raster_v3698.lua',",
      "ROOT/'mk2ks_human_bicycle_block_push_v3373.lua',":
        "ROOT/'tools/verify_current_natural_mirror_finish_v1674.py',ROOT/'tools/verify_native_friendship_audio_v791.py',",
      'mk2ks_human_bicycle_block_audio_v3386.lua':LUA,
      "files.update((ROOT/'roms/mk2ks').glob('*'));":"files.update((ROOT/'samples/mk2ks').glob('*'));files.update((ROOT/'roms/mk2ks').glob('*'));",
      "env.update(MK2KS_HUMAN_SPECIAL_MOVE='bicycle',MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_SCENARIO='block',\n               MK2KS_HUMAN_SPECIAL_VICTIM='kano',MK2KS_BBLOCK_OUT=str(folder))":
        f"env.update(MK2KS_TEST_FIGHTER='{fighter}',MK2KS_MIRROR_WINNER=str(side),MK2KS_MIRROR_CONFIRM_FIRST='1',MK2KS_REPTILE_AUDIT_DIR=str(folder))",
      "'-str','65'":"'-str','95'",
      "move='bicycle',side=side,scenario='block',victim='kano'":f"move='individual_fatality',side=side,scenario='natural_mirror',fighter='{fighter}'",
      'state.prior.current.current.EXE':'NEW_EXE','state.prior.current.current.PAYLOAD':'NEW_PAYLOAD',
    }
    for old,new in edits.items():
        need(source.count(old)==(2 if old=='mk2ks_human_bicycle_block_audio_v3386.lua'else 1),'Exact RAM collector adaptation '+old)
        source=source.replace(old,new)
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    scope=dict(audio.__dict__);scope.update(__file__=__file__,CANDIDATE=NAME,NEW_EXE=build['executable_sha256'],NEW_PAYLOAD=build['payload_sha256'])
    exec(compile(source,'<whole3390RAMcollector_physicalmirror_only>','exec'),scope)
    return scope['capture'],hashlib.sha256(source.encode()).hexdigest().upper()

def physical_contract():
    source=inspect.getsource(physical.verify)
    first='  data=rows(log);items=lambda tag:[r for t,r in data if t==tag]'
    last="  captures=[r for r in items('SNAPSHOT') if r['file'].startswith('mirror_finish_')]"
    need(source.count(first)==source.count(last)==1,'Exact original whole runtime/state/palette contract boundaries')
    block=textwrap.dedent(source[source.index(first):source.index(last)])
    continuation='if not all(len(x)==1 for x in (starts,actions,wraps,stops)):continue'
    need(block.count(continuation)==1,'Original multi-case error continuation identified')
    block=block.replace(continuation,"need(all(len(x)==1 for x in (starts,actions,wraps,stops)),'Invalid single-case chronology cannot continue')")
    function='def contract(log,name,side,folder,guest):\n    identity=17 if name=="kano"else 18\n    victim=3-side;label=" current3680mirror";pins={}\n'
    function+=textwrap.indent(block,'    ')
    function+='    return dict(passed=True,nativeDamage=total,nativeKOs=chains,action=start,wrap=int(wrap["frame"]),fullHardwarePaletteSamples=palette_samples,inputHashes=pins)\n'
    scope=dict(physical.__dict__);scope['need']=need
    exec(compile(function,'<whole1674physical_fullpalette_FIFO_contract_no_raster_scope>','exec'),scope)
    return scope['contract'],hashlib.sha256(function.encode()).hexdigest().upper()

def rows(log,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_MAUDIO_'+tag+' ')]

def fit_all(signal,headers,events):
    start=float(headers[0]['seconds'])-int(headers[0]['bytes'])/4/48000
    theoretical=[round((float(e['seconds'])-start)*48000)for e in events]
    clips=[existing_sample(ROOT,int(e['word'],16))for e in events]
    channels=[CHANNELS[int(e['word'],16)]for e in events]
    offsets=[0]*len(clips)
    audible=np.zeros(len(signal),dtype=bool)
    for first,clip in zip(theoretical,clips):
        need(first>=8 and first+len(clip)+8<=len(signal),'Complete original cue and rounding margins captured')
        audible[first-8:first+len(clip)+8]=True
    need(not np.any(signal[~audible]),'No unmodeled imported audio during silent gaps, before selection or after full tails')
    indices=np.flatnonzero(audible);observed=signal[audible]
    def columns(offsets):
        matrix=np.zeros((len(indices),len(clips)))
        for j,clip in enumerate(clips):
            first=theoretical[j]+offsets[j]
            end=first+len(clip)
            later=next((k for k in range(j+1,len(clips))if channels[k]==channels[j]),None)
            if later is not None:end=min(end,theoretical[later]+offsets[later])
            need(0<=first<end<=len(signal),'Full actual cue or native same-channel preemption lies within captured PCM')
            positions=indices-first;used=(positions>=0)&(positions<end-first)
            matrix[used,j]=clip[positions[used]]
        return matrix
    # PCM onsets can round by <=4 samples, never by fields or seconds.
    for _ in range(2):
        for j in range(len(clips)):
            best=None
            for shift in range(-4,5):
                test=list(offsets);test[j]=shift;matrix=columns(test)
                gain=np.linalg.lstsq(matrix.T@matrix,matrix.T@observed,rcond=None)[0]
                mse=float(np.mean((matrix@gain-observed)**2))
                if best is None or mse<best[0]:best=(mse,shift)
            offsets[j]=best[1]
    matrix=columns(offsets);gains=np.linalg.lstsq(matrix.T@matrix,matrix.T@observed,rcond=None)[0];pred=matrix@gains
    rms=float(np.sqrt(np.mean((observed-pred)**2)));corr=float(np.dot(observed,pred)/(np.linalg.norm(observed)*np.linalg.norm(pred)))
    need(np.all((gains>.98)&(gains<1.02))and rms<2 and corr>.9995,'Every original direct cue/full audible tail/independent overlap/gain, no extra native-packet alias: '+str((gains.tolist(),rms,corr,offsets)))
    return dict(cues=len(events),gains=gains.tolist(),residualRMS=rms,correlation=corr,offsetOutputSamples=offsets,
      fullCapturedOutputSamples=len(signal),audibleCueUnionSamples=len(indices),exactSilentGapSamples=int(np.count_nonzero(~audible)),
      nativeSameChannelPreemptions=sum(next((True for k in range(j+1,len(clips))if channels[k]==channels[j]and theoretical[k]<theoretical[j]+len(clips[j])),False)for j in range(len(clips))))

def pair(fighter,side):
    capture,collector_sha=collector(fighter)
    folder,headers,a=capture(side,True);base,oldheaders,b=capture(side,False)
    log=(folder/'run.log').read_text();oldlog=(base/'run.log').read_text()
    selected=lambda s:[line for line in s.splitlines()if line.startswith('MK2_NATURAL_MIRROR_FINISH_V1166_')]
    need(selected(log)==selected(oldlog),'Every original physical input/state/palette/FIFO/continuation row equal with/without samples')
    guest=current.current.current.expected_current()[0]
    need((folder/'guest_maincpu.bin').read_bytes()==(base/'guest_maincpu.bin').read_bytes()==guest,'Entire independently reconstructed current guest')
    contract,contract_sha=physical_contract();state=contract(log,fighter,side,folder,guest)
    timeline=lambda hs:[{k:v for k,v in h.items()if k!='sha256'}for h in hs]
    need(timeline(headers)==timeline(oldheaders)and a.shape==b.shape,'Every actual complete mixed update timeline aligned')
    need(rows(log,'SOUND')==rows(oldlog,'SOUND'),'All native commands and direct markers unchanged by sample playback')
    events=[r for r in rows(log,'SOUND')if int(r['word'],16)in CHANNELS and r['pc']not in('FFA13C90','FFA13D60')]
    words=[int(e['word'],16)for e in events]
    select=0xfffc if fighter=='kano'else 0xfffb;win=0xfffe if fighter=='kano'else 0xfffd
    effects=[0xfff9]if fighter=='kano'else[0xfffa,0xfff8,0xfff7]
    need(words==[select,select,win,*effects,win],'Exactly both genuine selection cues, first win, physical own effect cues and final win')
    action=state['action']
    for e in events:
        if int(e['word'],16)in effects:need(action<=int(e['frame'])<=state['wrap'],'Effect belongs to actual native individual choreography')
    delta=a-b;need(np.array_equal(delta[:,0],delta[:,1]),'Actual imported contribution dual mono')
    mix=fit_all(delta[:,0],headers,events)
    # Source number is the authoritative inactive sentinel; source_len remains
    # cached after finishing and is not treated as an active orphaned sound.
    ending=max(int(r['frame'])for r in rows(log,'CHANNEL'))
    final=[r for r in rows(log,'CHANNEL')if int(r['frame'])==ending]
    need(len(final)==14 and all(int(r['sample'])==0xffffffff for r in final),'All individual effect/name channels finish before terminal return')
    need(all(int(r['sample'])==0xffffffff for r in rows(oldlog,'CHANNEL')),'No imported cue in DCS-only baseline')
    return dict(passed=True,fighter=fighter,side=side,capture=folder.name,baseline=base.name,
      physical=state,physicalContractSHA256=contract_sha,collectorSHA256=collector_sha,events=events,mixedOriginalDirectCueFidelity=mix,
      rawAudioFilesWritten=0,fullFinisherRasterOrAllVictimAcceptance=False)

def run():
    need(not OUT.exists(),'Fresh actual mirror audio gate')
    wrapper=(ROOT/'mk2ks_natural_mirror_no_raster_v3698.lua').read_text()
    need(wrapper.count('screen:snapshot(file)')==1 and wrapper.count("log('OMITTED_SNAPSHOT'")==1 and
         not re.search(r':write_|set_value|clear_value|\.value\s*=(?!=)',wrapper),'Only declared original PNG sink omission')
    observer=(ROOT/LUA).read_text();need(not re.search(r'io\.open|:write_|set_value|clear_value|snapshot\(|\.value\s*=(?!=)',observer),'Read-only RAM-only audio observer')
    cases=[pair(fighter,side)for fighter in('kano','sonya')for side in(1,2)]
    pins={str(Path(__file__).resolve()):sha(__file__),str(ROOT/LUA):sha(ROOT/LUA)}
    for case in cases:
        pins.update(case['physical']['inputHashes'])
        for leaf in(case['capture'],case['baseline']):
            folder=ROOT/leaf;meta=json.loads((folder/'result.json').read_text())
            for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'Consistent actual input bindings');pins[p]=h
            for p in folder.rglob('*'):
                if p.is_file():pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Executed source/evidence unchanged')
    return dict(passed=True,candidate=NAME,cases=cases,inputHashes=pins,
      naturalMirrorBothCharactersBothSlotsSelectionIndividualDirectCueMixAccepted=True,
      allVictimFinisherOrNativeDCSWaveformAcceptance=False,fullPortAcceptance=False,rawAudioFilesWritten=0,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable result');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
