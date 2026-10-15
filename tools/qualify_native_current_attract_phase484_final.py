"""Direct source/EOF qualification of the same retained native job; no replay."""
import copy,gzip,hashlib,json,subprocess
from pathlib import Path
import numpy as np
import qualify_native_current_attract_phase484 as pcm
import qualify_native_current_attract_phase484_v2 as context
ROOT,need,sha=pcm.ROOT,pcm.need,pcm.sha

def preserve_wrapper(c):
    out=c['folder'];path=out/'replacement_wrapper_local_binding_failure.json'
    script=Path(context.__file__).resolve()
    need(not path.exists() and not (out/'current_native_audio_source_eof_checked.json').exists(),
         'Fresh conservation of actual executed local-binding failure')
    report=json.loads((out/'current_native_audio_checked_v2.json').read_text())
    need(report['passed'] and report['differentChannelSamples']==0 and c['terminal']['nativeExit']==0,
         'Whole native PCM remained exact and game terminal before host wrapper local binding failed')
    with gzip.open(out/'replacement_wrapper_local_binding_executed_source.json.gz','wt',encoding='utf-8') as f:
        json.dump(dict(path=str(script),sha256=sha(script),text=script.read_text()),f)
    path.write_text(json.dumps(dict(passed=False,checkerFailure=True,nativeGameFailure=False,
        error="UnboundLocalError: cannot access local variable 'channels' where it is not associated with a value",
        cause='Mechanical wrapper replaced a module-qualified function with a name also assigned to a local result.',
        failedExecutedSourceSHA256=sha(script),newNativeRuns=0,fullPortAcceptance=False),indent=2)+'\n')

def qualify(c):
    out=c['folder'];path=out/'current_native_audio_source_eof_checked.json'
    need(not path.exists() and c['terminal']['nativeExit']==0 and not pcm.census.census() and
         c['guest']==pcm.current.expected(),'Same original terminal native run; full initialized guest, never a replay')
    wrapper=json.loads((out/'replacement_wrapper_local_binding_failure.json').read_text())
    failed=json.loads((out/'first_source_EOF_checker_failure.json').read_text())
    need(wrapper['failedExecutedSourceSHA256']==sha(context.__file__) and
         failed['failedCheckerSourceSHA256']==sha(pcm.__file__),
         'Both actual failed executed checker sources remain intact')
    transport=json.loads((out/'report.json').read_text())
    need(transport['passed'] and transport['requestedConfigurationAccepted'] and
         all(sha(p)==h for p,h in transport['inputHashes'].items()),'All originally executed game/host/controller inputs conserved')
    predicted,actual,model,_=pcm.predict(c)
    need(np.array_equal(predicted,actual),'Entire actual stereo output matches independent native DCS/source-clock model')
    state=context.channels(c,model)
    faults=[]
    for label,at,ch in [('first actual speaker bit',0,0),('final actual speaker bit',len(actual)-1,1)]:
        bad=actual.copy();bad[at,ch]^=1
        count=int(np.count_nonzero(predicted!=bad));need(count==1,'Actual PCM bit fault rejected')
        faults.append(dict(fault=label,differentSamples=count))
    precise=pcm.early.names.audio.rows(c['text'],'MK2_TOMB_MIX_CHANNEL')
    for label,index,field,value in [('wrong initial source position',0,'position','1'),
        ('stale final source',-1,'sample','13'),('wrong actual replacement source',
        next(i for i,r in enumerate(precise) if r['index']=='555' and r['channel']=='10'),'sample','13')]:
        row=precise[index]
        line=next(s for s in c['text'].splitlines() if s.startswith('MK2_TOMB_MIX_CHANNEL ') and
            f"index={row['index']} " in s and f"channel={row['channel']} " in s)
        bad=dict(c,text=c['text'].replace(line,line.replace(f'{field}={row[field]}',f'{field}={value}',1),1))
        try:context.channels(bad,model)
        except ValueError as e:faults.append(dict(fault=label,rejected=str(e)))
        else:raise ValueError('Actual precise source fault admitted '+label)
    square=next(e for e in model['events'] if e['marker']['word']=='6B00')
    extend=pcm.compound.contribution(c,square,True)-pcm.compound.contribution(c,square,False)
    convert=lambda signal:(np.clip(signal,-1,1).astype(np.float64)*32767).astype('<i2')
    for label,wrong in [('native DCS source omitted',convert(model['voice'])),
        ('Square wrongly continues after Bicycle replaces it',convert(np.float32(model['dcs']+np.float32(model['voice']+extend))))]:
        count=int(np.count_nonzero(wrong!=actual));need(count>0,'Effective independent native source fault '+label)
        faults.append(dict(fault=label,differentSamples=count))
    need(context.channels(c,model)==state and np.array_equal(predicted,actual),'Complete actual positive restored after all seven faults')
    carriers=[]
    for leaf,records in [('captured_native_audio.pcm.gz',[r['pixels'] for r in c['pcm']]),
        ('captured_native_dac.f32.gz',c['dac'])]:
        target=out/leaf;need(not target.exists(),'Fresh compact full native carrier')
        with gzip.open(target,'wb',compresslevel=9) as f:
            for raw in records:f.write(raw)
        with gzip.open(target,'rb') as f:need(f.read()==b''.join(records),'Every original native carrier byte retained losslessly')
        carriers.append(target)
    pins={**transport['inputHashes'],**model['pins']}
    files=[Path(__file__),Path(pcm.__file__),Path(context.__file__),Path(pcm.early.__file__),
        Path(pcm.compound.__file__),Path(pcm.early.names.__file__),Path(pcm.early.names.audio.__file__)]
    with gzip.open(out/'executed_final_audio_qualification_sources.json.gz','wt',encoding='utf-8') as f:
        json.dump({str(p.resolve()):dict(sha256=sha(p),text=p.read_text()) for p in files},f)
    files += [*carriers,out/'report.json',out/'run.log.gz',out/'current_native_audio_checked.json',
        out/'current_native_audio_checked_v2.json',out/'first_source_EOF_checker_failure.json',
        out/'replacement_wrapper_preflight_failure.json',out/'replacement_wrapper_local_binding_failure.json',
        out/'executed_final_audio_qualification_sources.json.gz']
    pins.update({str(p.resolve()):sha(p) for p in files})
    report=dict(passed=True,fullPortAcceptance=False,candidate=pcm.current.NAME,
        executableSHA256=pcm.current.EXE_SHA,guestSHA256=pcm.current.GUEST_SHA,
        actualNativeTerminal=c['terminal'],finiteCurrentSonyaCompoundAndNamesAudioAccepted=True,
        audibleKanoDemoLaunchAccepted=False,comparedStereoFrames=len(actual),differentChannelSamples=0,
        wholeActualPCM_SHA256=hashlib.sha256(actual.tobytes()).hexdigest().upper(),
        preciseSourceChannels=state,actualCounterexamplesRejected=faults,inputHashes=pins,
        actualSourceEvents=[{k:(float(v) if k=='gain' else v) for k,v in e.items() if k not in ('signal','positions')} for e in model['events']],
        actualPCMHeaders=[r['header'] for r in c['pcm']],actualDACHeaders=c['dacHeaders'],
        actualRGBHeaders=[r['header'] for r in c['rgbFrames']],
        byteConservingCompressedNativeCarriers=True,rawMediaFilesWritten=0,newNativeRunsForCheckerRepairs=0,
        gameSourceChanged=False,newBuilds=0,publicPlayableChanged=False,goalStatus='active',
        allOriginalGoalRequirementsStillActive=True,actualVisualReviewPending=True,
        audioStopObservation='The exact native timer flushed Square at417.82792384 between speaker snapshots417.82 and417.84; actual Bicycle source14 appeared in the next callback. All14 source IDs/lengths/positions/EOF bits remain checked.',
        failedOriginalCheckersPreserved=True)
    path.write_text(json.dumps(report,indent=2)+'\n')
    for p in out.iterdir():
        if p.is_file():subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    need(all(sha(p)==h for p,h in pins.items()),'Every compressed source/evidence byte conserved')
    print(json.dumps(dict(passed=True,comparedStereoFrames=len(actual),differentChannelSamples=0,
        actualFaultsRejected=len(faults),preciseSourceChannels=state,audibleKanoDemoLaunchAccepted=False)),flush=True)
    return report
