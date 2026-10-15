"""3680 true mirror finishers plus all subsequent owned launch PCM.

Preserve the whole1674 physical/palette/FIFO gate, minimum5198fields and exact
zero unexplained-audio gate. Extend the host capture through complete actual
cue tails, including genuine CPU Sonya launches in the subsequent fight.
No new ROM/EXE/raster/VRAM/WAV, state injections or modified game sources.
"""
import hashlib,inspect,json,re,textwrap,traceback,wave
from pathlib import Path
import numpy as np
import run_natural_mirror_audio_ram_v3700 as prior

ROOT,need,sha,NAME=prior.ROOT,prior.need,prior.sha,prior.NAME
OUT=ROOT/'audit_v3711_natural_mirror_complete_audio_checked'
LUA='mk2ks_natural_mirror_audio_ram_v3708.lua'
BATTLE={0x6b00:'sonya_square_launch',0x6b01:'sonya_bicycle_launch',0x6b02:'sonya_bicycle_cry'}

def collector(fighter):
    source=inspect.getsource(prior.collector)
    for old,new in {
      'audit_v3701_':'audit_v3710_',
      'mk2ks_natural_mirror_no_raster_v3698.lua':'mk2ks_natural_mirror_no_raster_v3712.lua',
      '"\'-str\',\'95\'"':'"\'-str\',\'110\'"',
      "MK2KS_TEST_FIGHTER='{fighter}',":"MK2KS_PORT_ROOT=str(ROOT),MK2KS_TEST_FIGHTER='{fighter}',",
    }.items():
        need(source.count(old)==1,'Exact fresh complete capture adaptation '+old)
        source=source.replace(old,new)
    where='    for old,new in edits.items():'
    extra="    edits.update({\"subprocess.Popen(command,cwd=ROOT\":\"subprocess.Popen(command,cwd=folder\",\"'-skip_gameinfo','-nocheat'\":\"'-skip_gameinfo','-nocheat','-log'\"})\n"
    need(source.count(where)==1,'Capture cwd/log isolation only')
    source=source.replace(where,extra+where)
    scope=dict(prior.__dict__);scope.update(__file__=__file__,LUA=LUA)
    exec(compile(source,'<whole3390collector_complete_mirror_host_capture>','exec'),scope)
    return scope['collector'](fighter)

def physical_contract():
    source=inspect.getsource(prior.physical.verify)
    first='  data=rows(log);items=lambda tag:[r for t,r in data if t==tag]'
    last="  captures=[r for r in items('SNAPSHOT') if r['file'].startswith('mirror_finish_')]"
    need(source.count(first)==source.count(last)==1,'Whole original physical/fullpalette contract boundaries')
    block=textwrap.dedent(source[source.index(first):source.index(last)])
    old='if not all(len(x)==1 for x in (starts,actions,wraps,stops)):continue'
    need(block.count(old)==1,'Original multi-case continuation')
    block=block.replace(old,"need(all(len(x)==1 for x in (starts,actions,wraps,stops)),'Invalid single-case chronology')")
    old="stop['frame']=='5198'"
    need(block.count(old)==1,'Original full-length terminal field bound')
    block=block.replace(old,"int(stop['frame'])>=5198")
    function='def contract(log,name,side,folder,guest):\n    identity=17 if name=="kano"else 18\n    victim=3-side;label=" current3680completeMirror";pins={}\n'+textwrap.indent(block,'    ')
    function+='    return dict(passed=True,nativeDamage=total,nativeKOs=chains,action=start,wrap=int(wrap["frame"]),terminalFrame=int(stop["frame"]),fullHardwarePaletteSamples=palette_samples,inputHashes=pins)\n'
    scope=dict(prior.physical.__dict__);scope['need']=need
    exec(compile(function,'<whole1674physical_FIFO_palette_minimum5198>','exec'),scope)
    return scope['contract'],hashlib.sha256(function.encode()).hexdigest().upper()

def error_rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2KS_BATTLE_'+tag+' ')]

def cue_model(log,errors):
    events=[r for r in prior.rows(log,'SOUND')if int(r['word'],16)in prior.CHANNELS and r['pc']not in('FFA13C90','FFA13D60')]
    model=[]
    for e in events:
        word=int(e['word'],16)
        model.append(dict(event=e,channel=prior.CHANNELS[word],clip=prior.existing_sample(ROOT,word),stop=None))
    requests=prior.rows(log,'REQUEST');marks=error_rows(errors,'MARKER');stops=error_rows(errors,'CLEANUP')
    ports=[r for r in prior.rows(log,'SOUND')if int(r['word'],16)in BATTLE]
    need(len(ports)==len(requests)==len(marks),'Every subsequent actual launch is source-owned, not a phantom cue')
    for request,mark,port in zip(requests,marks,ports):
        word=int(port['word'],16);slot=int(request['slot']);channel=10+(slot-1)*2+(word==0x6b02)
        need(request['word']==mark['command']==port['word']and request['seconds']==mark['seconds']==port['seconds']and
          request['actor']==request['owner']==mark['actor']==port['a8']and request['main']==mark['main']==port['a13']and
          int(mark['channel'])==channel and int(mark['sample'])==13+word-0x6b00 and mark['slot']==request['slot']and
          request['id']=='18'and request['mode']=='2'and request['state']==('0207'if word==0x6b00 else'0204')and
          mark['pc']==port['pc'],'Exact genuine native Sonya launch/physical actor/Main/marker/channel')
        asset=ROOT/'samples/mk2ks'/(BATTLE[word]+'.wav')
        with wave.open(str(asset),'rb')as wav:
            need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate())==(1,2,48000),'Original native48k launch source')
            clip=np.frombuffer(wav.readframes(wav.getnframes()),'<i2').astype(float)*.70
        clip[-1]=0 # same-rate non-loop samples.cpp final-sample fill
        cleanup=next((r for r in stops if r['slot']==request['slot']and r['actor']==request['actor']and r['main']==request['main']and float(r['seconds'])>float(port['seconds'])),None)
        need(cleanup is not None and cleanup['reason']in('finished','health_changed','owner_changed','noncombat','new_launch','reset'),'Actual finite owned launch cleanup observed')
        model.append(dict(event=port,channel=channel,clip=clip,stop=float(cleanup['seconds']),assetSHA256=sha(asset),request=request,cleanup=cleanup))
    model.sort(key=lambda r:float(r['event']['seconds']))
    return model,events

def fit_all(signal,headers,model):
    start=float(headers[0]['seconds'])-int(headers[0]['bytes'])/4/48000
    theoretical=[round((float(m['event']['seconds'])-start)*48000)for m in model]
    clips=[m['clip']for m in model];channels=[m['channel']for m in model];offsets=[0]*len(clips)
    stop=[round((m['stop']-start)*48000)if m['stop']is not None else len(signal)for m in model]
    audible=np.zeros(len(signal),bool)
    for first,clip in zip(theoretical,clips):
        need(first>=8 and first+len(clip)+8<=len(signal),'Complete original cue and source rounding margins captured, including subsequent launches')
        audible[first-8:first+len(clip)+8]=True
    need(not np.any(signal[~audible]),'Exactly zero unexplained imported audio before/between/after all original cues')
    indices=np.flatnonzero(audible);observed=signal[audible]
    def columns(offsets):
        matrix=np.zeros((len(indices),len(clips)))
        for j,clip in enumerate(clips):
            first=theoretical[j]+offsets[j];end=min(first+len(clip),stop[j])
            later=next((k for k in range(j+1,len(clips))if channels[k]==channels[j]),None)
            if later is not None:end=min(end,theoretical[later]+offsets[later])
            need(0<=first<end<=len(signal),'Actual complete cue or native channel/owner cancellation within captured PCM')
            pos=indices-first;used=(pos>=0)&(pos<end-first);matrix[used,j]=clip[pos[used]]
        return matrix
    for _ in range(2):
        for j in range(len(clips)):
            best=None
            for shift in range(-4,5):
                test=list(offsets);test[j]=shift;matrix=columns(test)
                gain=np.linalg.lstsq(matrix.T@matrix,matrix.T@observed,rcond=None)[0]
                mse=float(np.mean((matrix@gain-observed)**2))
                if best is None or mse<best[0]:best=(mse,shift)
            offsets[j]=best[1]
    matrix=columns(offsets);gain=np.linalg.lstsq(matrix.T@matrix,matrix.T@observed,rcond=None)[0];pred=matrix@gain
    rms=float(np.sqrt(np.mean((observed-pred)**2)));corr=float(np.dot(observed,pred)/(np.linalg.norm(observed)*np.linalg.norm(pred)))
    need(np.all((gain>.98)&(gain<1.02))and rms<2 and corr>.9995,'All original direct cues/full tails/owned launches gain and overlap: '+str((gain.tolist(),rms,corr,offsets)))
    return dict(cues=len(model),gains=gain.tolist(),residualRMS=rms,correlation=corr,offsetOutputSamples=offsets,
      fullCapturedOutputSamples=len(signal),exactSilentGapSamples=int(np.count_nonzero(~audible)),
      modeledSourceOutputSamples=[len(c)for c in clips],rawAudioFilesWritten=0)

def pair(fighter,side):
    capture,collector_sha=collector(fighter)
    folder,headers,a=capture(side,True);base,oldheaders,b=capture(side,False)
    log=(folder/'run.log').read_text();oldlog=(base/'run.log').read_text();errors=(folder/'error.log').read_text()
    selected=lambda s:[l for l in s.splitlines()if l.startswith('MK2_NATURAL_MIRROR_FINISH_V1166_')]
    need(selected(log)==selected(oldlog),'Every original physical/state/palette/FIFO/continue observation unchanged with playback')
    guest=prior.current.current.current.expected_current()[0]
    need((folder/'guest_maincpu.bin').read_bytes()==(base/'guest_maincpu.bin').read_bytes()==guest,'Complete independently reconstructed current guest')
    contract,contract_sha=physical_contract();state=contract(log,fighter,side,folder,guest)
    timeline=lambda hs:[{k:v for k,v in h.items()if k!='sha256'}for h in hs]
    need(timeline(headers)==timeline(oldheaders)and a.shape==b.shape,'Every actual complete mixed update aligned')
    need(prior.rows(log,'SOUND')==prior.rows(oldlog,'SOUND')and prior.rows(log,'REQUEST')==prior.rows(oldlog,'REQUEST'),'All genuine native command/physical request chronology unchanged')
    ends=prior.rows(log,'CAPTURE_END');need(len(ends)==1 and ends==prior.rows(oldlog,'CAPTURE_END')and
      int(ends[0]['frame'])==state['terminalFrame']>=5198 and float(ends[0]['seconds'])>=float(ends[0]['not_before']),'Actual common minimum95s and complete cue-tail capture deadline')
    model,events=cue_model(log,errors)
    select,win=(0xfffc,0xfffe)if fighter=='kano'else(0xfffb,0xfffd)
    effects=[0xfff9]if fighter=='kano'else[0xfffa,0xfff8,0xfff7]
    need([int(e['word'],16)for e in events]==[select,select,win,*effects,win],'All and only genuine selected character announcements and own individual effect markers')
    need(all(state['action']<=int(e['frame'])<=state['wrap']for e in events if int(e['word'],16)in effects),'Own effect cues remain inside true native individual choreography')
    delta=a-b;need(np.array_equal(delta[:,0],delta[:,1]),'Original imported contribution dual mono')
    mix=fit_all(delta[:,0],headers,model)
    channels=prior.rows(log,'CHANNEL');final=[r for r in channels if int(r['frame'])==state['terminalFrame']]
    need(len(final)==14 and all(int(r['sample'])==0xffffffff for r in final),'All actual sample channels inactive after complete final cue lifetime')
    need(all(r['loop']==r['paused']==r['writes']=='0'for r in channels),'All14 finite unpaused read-only voices')
    need(all(r['length']=='0'for r in channels if 4<=int(r['channel'])<=9),'No unrelated Friendship/orphaned sample channel')
    need(all(int(r['sample'])==0xffffffff and r['length']=='0'for r in prior.rows(oldlog,'CHANNEL')),'Disabled baseline has no imported source')
    owner=prior.rows(log,'OWNER');terminal=[r for r in owner if int(r['frame'])==state['terminalFrame']]
    need(len(terminal)==2 and all(r['actor']==r['main']=='00000000'and r['health']=='0'for r in terminal),'Both actual launch owners cleared at terminal')
    for r in owner:
        if r['actor']=='00000000':need(r['main']=='00000000'and r['health']=='0','Complete cleared owner tuple')
        else:need(any(m.get('request',{}).get('slot')==r['slot']and m['request']['actor']==r['actor']and
          m['request']['main']==r['main']and m['request']['health']==r['health']and int(m['event']['frame'])<int(r['frame'])for m in model),'Every active launch owner comes from actual native Sonya marker/request')
    cues=[{k:v for k,v in m.items()if k!='clip'}for m in model]
    return dict(passed=True,fighter=fighter,side=side,capture=folder.name,baseline=base.name,physical=state,
      collectorSHA256=collector_sha,physicalContractSHA256=contract_sha,cues=cues,mixedOriginalCueFidelity=mix,
      subsequentOwnedLaunchCues=sum('request'in m for m in model),rawAudioFilesWritten=0)

def run():
    need(not OUT.exists(),'Fresh complete mirror audio gate')
    observer=(ROOT/LUA).read_text();need(not re.search(r'io\.open|:write_|set_value|clear_value|snapshot\(|\.value\s*=(?!=)',observer),'Read-only observer, host exit only')
    cases=[]
    for fighter in('kano','sonya'):
        for side in(1,2):
            case=pair(fighter,side);cases.append(case)
            print(json.dumps(dict(case=f'{fighter} P{side}',passed=True,fit=case['mixedOriginalCueFidelity'],subsequentOwnedLaunchCues=case['subsequentOwnedLaunchCues'])),flush=True)
    pins={str(Path(__file__).resolve()):sha(__file__),str(Path(prior.__file__).resolve()):sha(prior.__file__),str(ROOT/LUA):sha(ROOT/LUA),str(ROOT/'mk2ks_natural_mirror_no_raster_v3712.lua'):sha(ROOT/'mk2ks_natural_mirror_no_raster_v3712.lua')}
    for case in cases:
        pins.update(case['physical']['inputHashes'])
        for leaf in(case['capture'],case['baseline']):
            folder=ROOT/leaf;meta=json.loads((folder/'result.json').read_text())
            for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'Consistent executed input bindings');pins[p]=h
            for p in folder.rglob('*'):
                if p.is_file():pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All executed source and evidence unchanged')
    return dict(passed=True,candidate=NAME,cases=cases,inputHashes=pins,
      naturalMirrorBothCharactersBothSlotsSelectionIndividualDirectCueMixAccepted=True,
      allVictimFinisherOrNativeDCSWaveformAcceptance=False,fullPortAcceptance=False,rawAudioFilesWritten=0,scope=__doc__)

if __name__=='__main__':
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable result');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
