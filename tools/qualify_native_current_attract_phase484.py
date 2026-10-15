"""Entire actual current demo names/Square/Bicycle PCM and precise source EOF."""
import gzip,hashlib,inspect,json,struct,subprocess
from pathlib import Path
import numpy as np
import qualify_native_attract_early_square as early
import qualify_native_attract_compound_audio as compound
import native_cpu_finisher_spacing_context as current
import native_process_census_v6647 as census
ROOT,need,sha=current.ROOT,current.need,current.sha

def predict(c):
    source=inspect.getsource(early.predict)
    begin=source.index("    sounds=names.runtime.rows(c['text'],'SOUND')")
    end=source.index("    chunks,headers=c['dac'],c['dacHeaders']")
    source=source[:begin]+"    events.extend(compound.launch_events(c))\n    pins.update({e['sourceAsset']:e['sourceSHA256'] for e in events if 'sourceAsset' in e})\n"+source[end:]
    for before,after in [('==769','==811'),('==[256,257,256]','==[257,257,297]'),
        ("(at<len(event['signal']))","(at<event.get('count',len(event['signal'])))")]:
        need(source.count(before)==1,'Exact original full DCS/source/mixer adaptation boundary '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(early),compound=compound)
    exec(compile(source,__file__+'::whole_original_resampler_mixer','exec'),scope)
    predicted,actual,model=scope['predict'](c)
    return predicted,actual,model,source

def qualify(c):
    out=c['folder'];path=out/'current_native_audio_checked.json'
    need(not path.exists() and c['terminal']['nativeExit']==0 and not census.census() and c['guest']==current.expected(),
         'Same actual native child terminal and complete current compiled guest')
    transport=json.loads((out/'report.json').read_text())
    need(transport['passed'] and transport['requestedConfigurationAccepted'] and
         transport['actualPhysicalInputs']==[[f,'1'] for f in range(484,488)]+[[488,'0']] and
         all(sha(p)==h for p,h in transport['inputHashes'].items()),
         'Every actually executed source and ordinary cold input unchanged')
    predicted,actual,model,source=predict(c)
    different=np.argwhere(predicted!=actual)
    report=dict(passed=not len(different),fullPortAcceptance=False,
        candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,
        callbacks=len(c['pcm']),comparedStereoFrames=len(actual),differentChannelSamples=len(different),
        actualSHA256=hashlib.sha256(actual.tobytes()).hexdigest().upper(),
        predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
        firstDifferences=[dict(stereoFrame=int(n),channel=int(ch),expected=int(predicted[n,ch]),actual=int(actual[n,ch])) for n,ch in different[:8]],
        nativeTerminal=c['terminal'],windowCallbackCounts=[len(g) for g in model['windows']],
        actualSourceEvents=[{k:(float(v) if k=='gain' else v) for k,v in e.items() if k not in ('signal','positions')} for e in model['events']],
        nativeDCSSamples=model['nativeSamples'],nonzeroNativeDCSSamples=model['nonzeroNativeSamples'],
        actualPhysicalInputs=transport['actualPhysicalInputs'],audibleKanoDemoLaunchAccepted=False,
        limitation='No actual Kano roll occurred in this finite run; Sonya compound and both biography names are the observed audible paths.',
        comparison='Whole actual DCS floats, native cached resampler and clocks; independent donor sources, actual replacement rule, float32 routing/sum and original signed16 truncation. No fitted onset/gain, omitted first sample or tail.',
        actualVisualReviewPending=True,publicPlayableChanged=False,newBuilds=0,goalStatus='active')
    # Preserve the real comparison, even if it fails; never rewrite an executed oracle.
    with gzip.open(out/'executed_current_audio_sources.json.gz','wt',encoding='utf-8') as f:
        json.dump(dict(predictSource=source,files={str(Path(m.__file__).resolve()):Path(m.__file__).read_text()
            for m in (early,compound,early.names,early.names.audio)}),f)
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','callbacks','comparedStereoFrames','differentChannelSamples','audibleKanoDemoLaunchAccepted')}),flush=True)
    need(not len(different),'Entire current native audible sequence must be bit-exact; failed executed model already preserved')
    channels=compound.channels(c,model)
    faults=[]
    for label,at,ch in [('first actual speaker bit',0,0),('final actual speaker bit',len(actual)-1,1)]:
        bad=actual.copy();bad[at,ch]^=1
        need(not np.array_equal(predicted,bad),'Actual PCM bit counterexample rejected')
        faults.append(dict(fault=label,differentSamples=int(np.count_nonzero(predicted!=bad))))
    for index,field,change in [(0,'position',1.),(-1,'sample',13)]:
        # A separate exact channel gate rejects wrong playback/EOF values through
        # the original model; the positive full callback ledger is preserved.
        text=c['text'];row=early.names.audio.rows(text,'MK2_TOMB_MIX_CHANNEL')[index]
        line=next(s for s in text.splitlines() if s.startswith('MK2_TOMB_MIX_CHANNEL ') and
            f"index={row['index']} " in s and f"channel={row['channel']} " in s)
        value=str(float(row[field])+change) if field=='position' else str(change)
        bad=dict(c,text=text.replace(line,line.replace(f'{field}={row[field]}',f'{field}={value}',1),1))
        try:compound.channels(bad,model)
        except ValueError as e:faults.append(dict(fault='wrong exact source '+field,rejected=str(e)))
        else:raise ValueError('Actual precise source corruption admitted')
    need(compound.channels(c,model)==channels,'Every14-channel positive restored after source counterexamples')
    # Retain only compressed useful source evidence; no raw media or guest dump.
    audio_path,dac_path=out/'captured_native_audio.pcm.gz',out/'captured_native_dac.f32.gz'
    for target,records in ((audio_path,[r['pixels'] for r in c['pcm']]),(dac_path,c['dac'])):
        need(not target.exists(),'Fresh complete compressed native carrier')
        with gzip.open(target,'wb',compresslevel=9) as f:
            for raw in records:f.write(raw)
        with gzip.open(target,'rb') as f:
            need(f.read()==b''.join(records),'Every byte of entire actual carrier conserved')
    pins={**transport['inputHashes'],**model['pins']}
    for module in (early,compound,early.names,early.names.audio):pins[str(Path(module.__file__).resolve())]=sha(module.__file__)
    paths=[Path(__file__),path,out/'executed_current_audio_sources.json.gz',audio_path,dac_path,
        out/'run.log.gz',ROOT/'audit_native_sonya_cpu_finisher_progress/report.json']
    pins.update({str(p.resolve()):sha(p) for p in paths})
    receipt=dict(passed=True,fullPortAcceptance=False,candidate=current.NAME,
        actualNativeTerminal=c['terminal'],finiteCurrentSonyaCompoundAndNamesAudioAccepted=True,
        audibleKanoDemoLaunchAccepted=False,comparedStereoFrames=len(actual),preciseSourceChannels=channels,
        actualCounterexamplesRejected=faults,inputHashes=pins,allOriginalGoalRequirementsStillActive=True,
        byteConservingCompressedNativeCarriers=True,rawMediaFilesWritten=0,newBuilds=0,
        publicPlayableChanged=False,actualVisualReviewPending=True,goalStatus='active')
    receipt_path=out/'current_native_audio_source_eof_checked.json'
    need(not receipt_path.exists(),'Fresh complete actual EOF/source receipt')
    receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
    for p in (path,receipt_path,*[q for q in out.iterdir() if q.is_file()]):
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    need(all(sha(p)==h for p,h in pins.items()),'All selected evidence/source bytes conserved after NTFS compression')
    print(json.dumps(dict(passed=True,preciseSourceChannels=channels,actualCounterexamples=len(faults),
        comparedStereoFrames=len(actual),audibleKanoDemoLaunchAccepted=False)),flush=True)
    return receipt
