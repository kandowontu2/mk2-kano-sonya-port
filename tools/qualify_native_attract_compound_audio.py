"""Whole actual native Square-to-Bicycle attract mix; no fitted source stops.

Reuse the entire independently checked DCS resampler/mixer. Derive Square's
replacement from the actual next launch, native ownership timer and preceding
stream callback, not from speaker samples or an assumed move duration.
"""
import gzip
import hashlib
import inspect
import json
import struct
import subprocess
import sys
import wave
from decimal import Decimal
from pathlib import Path
import numpy as np
import qualify_native_attract_early_square as original
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=original.ROOT,original.need,original.sha

def launch_events(c):
    sounds=original.names.runtime.rows(c['text'],'SOUND')
    rows=[r for r in sounds if r['word'] in ('6B00','6B01','6B02','6B03') and r['mute']=='0']
    need([r['word'] for r in rows]==['6B00','6B01','6B02'],'Actual complete natural Square then dual Bicycle cues')
    files=('sonya_square_launch.wav','sonya_bicycle_launch.wav','sonya_bicycle_cry.wav')
    lengths=(45512,40720,66523);pcs=('FFFFCAC0','FFF9A4C0','FFF9A520')
    events=[]
    headers=[r['header'] for r in c['pcm']]
    for i,(row,file,length,pc) in enumerate(zip(rows,files,lengths,pcs)):
        need(row['pc']==pc and row['mode']=='1' and row['p1_id']==row['p1_roster']=='18' and
             row['a8']==row['p1_actor']==row['p1_owner'] and row['a13']==row['p1_main'] and row['p1_hp']=='161' and
             row['p1_action']==('519' if i==0 else '516') and row['p2_id']==row['p2_roster']=='9',
             'True CPU Sonya18 versus Reptile9, original actor/Main ownership and signature action')
        path=ROOT/'samples/mk2ks'/file
        with wave.open(str(path),'rb') as wav:
            need((wav.getnchannels(),wav.getsampwidth(),wav.getframerate(),wav.getnframes(),wav.getcomptype())==(1,2,48000,length,'NONE'),
                 'Complete original native donor launch waveform')
            values=np.frombuffer(wav.readframes(length),'<i2').copy()
        signal,positions=original.names.audio.sample_values(values,48000)
        start=original.names.audio.sample_clock(row['seconds'],True)
        count=len(signal);stop_details=None
        if i==0:
            onset=int(Decimal(row['seconds'])*original.names.audio.ATTO)
            replacement=int(Decimal(rows[1]['seconds'])*original.names.audio.ATTO)
            period=original.names.audio.ATTO//60
            previous=onset+((replacement-onset-1)//period)*period
            earlier=[int(Decimal(h['seconds'])*original.names.audio.ATTO) for h in headers if Decimal(h['seconds'])<Decimal(rows[1]['seconds'])]
            need(earlier and onset<previous<replacement,'Original preceding60Hz playback tick and actual stream callback before replacement')
            last_update=max(max(earlier),previous)
            cutoff=original.names.audio.sample_clock(str(Decimal(last_update)/original.names.audio.ATTO),True)
            count=cutoff-start
            need(0<count<len(signal),'Real mid-source replacement, not an EOF or silence-only case')
            stop_details=dict(nextNativeLaunch=rows[1],previousNativeOwnershipTick=previous,lastStreamUpdate=last_update,
                              cutoff=cutoff,generatedBeforeReplacement=count)
        events.append(dict(identity=18,marker=row,start=start,signal=signal,positions=positions,count=count,
                           channel=11 if i==2 else 10,sample_id=13+i,length=length,gain=np.float32(.70),
                           sourceAsset=str(path),sourceSHA256=sha(path),replacement=stop_details))
    owners=original.names.runtime.rows(c['text'],'AUDIO_OWNER')
    until=Decimal(rows[2]['seconds'])+Decimal(lengths[2])/48000
    owners=[r for r in owners if Decimal(rows[0]['seconds'])<=Decimal(r['seconds'])<=until]
    need(owners and all(r['mode']=='1' and r['mute']=='0' and r['p1_id']=='18' and r['p1_hp']=='161' and
         r['p1_actor']==r['p1_owner']==rows[0]['p1_actor'] and r['p1_main']==rows[0]['p1_main'] for r in owners),
         'No hidden health/owner/mute transition during the actual complete compound launch')
    return events

def predict(c):
    source=inspect.getsource(original.predict)
    begin=source.index("    sounds=names.runtime.rows(c['text'],'SOUND')")
    end=source.index("    chunks,headers=c['dac'],c['dacHeaders']")
    source=source[:begin]+"    events.extend(launch_events(c))\n    pins.update({e['sourceAsset']:e['sourceSHA256'] for e in events if 'sourceAsset' in e})\n"+source[end:]
    for before,after in [("==769","==1067"),("==[256,257,256]","==[257,257,297,256]"),
                         ("(at<len(event['signal']))","(at<event.get('count',len(event['signal'])))")]:
        need(source.count(before)==1,'Whole original DCS/mixer adaptation boundary '+before)
        source=source.replace(before,after,1)
    scope=dict(original.__dict__,launch_events=launch_events)
    exec(compile(source,str(Path(original.__file__).resolve())+'::actual_compound_launch', 'exec'),scope)
    return scope['predict'](c)

def channels(c,model):
    headers=[r['header'] for r in c['pcm']]
    precise=original.names.audio.rows(c['text'],'MK2_TOMB_MIX_CHANNEL')
    need(len(precise)==len(headers)*14 and {(int(r['index']),int(r['channel'])) for r in precise}==
         {(i,ch) for i in range(1,len(headers)+1) for ch in range(14)},'Every precise native channel at every full speaker callback')
    events=[]
    for event in model['events']:
        if 'positions' not in event:
            file='kano_select.wav' if event['identity']==17 else 'sonya_select.wav'
            with wave.open(str(ROOT/'samples/mk2ks'/file),'rb') as wav:
                _,positions=original.names.audio.sample_values(np.frombuffer(wav.readframes(18400),'<i2').copy(),16000)
            event=dict(event,positions=positions,channel=0,length=18400,sample_id=0 if event['identity']==17 else 1,count=len(positions))
        events.append(event)
    playing=set();ended=set();replaced=False
    for row in precise:
        index,ch=int(row['index']),int(row['channel']);h=headers[index-1]
        need(row['frame']==h['frame'] and row['seconds']==h['seconds'] and row['loop']==row['paused']=='0' and
             row['writes']=='0' and row['assistance']=='none','Actual passive precise source callback association')
        tick=int(Decimal(h['seconds'])*50)
        sec,frac=divmod(tick*960*(original.names.audio.ATTO//48000),original.names.audio.ATTO)
        end=sec*48000+(frac+original.names.audio.PERIOD-1)//original.names.audio.PERIOD
        launches=[e for e in events if e['channel']==ch and e['start']<=end]
        number,length,position=0xffffffff,0,0.0
        if launches:
            event=launches[-1];count=min(event['count'],max(0,end-event['start']))
            length=event['length'];position=event['positions'][count-1] if count else 0.0
            active=0<count<len(event['positions']) and count<event['count']
            if active:
                playing.add(event['marker']['word'])
                if len(launches)>1:number=event['sample_id']
            if count==len(event['positions']):ended.add(event['marker']['word'])
            if event['marker']['word']=='6B00' and count==event['count']:
                # This precise callback is the original final update before
                # replacement, hence pointer remains live until next marker.
                replaced=True
        need(int(row['sample'])==number and int(row['length'])==length and float(row['position'])==position and
             row['bits']==struct.pack('<d',position).hex().upper(),'All source IDs, retained lengths and exact native playback/EOF bits')
    need(playing=={'FFFC','FFFB','6B00','6B01','6B02'} and ended=={'FFFC','FFFB','6B01','6B02'} and replaced,
         'Actual Square replacement and both complete Bicycle EOFs, with all unused/muted channels idle')
    return dict(passed=True,preciseChannelStates=len(precise),SquareReplacedBeforeEOF=True,BicycleBothCompleteEOF=True,
                allFourteenChannelsChecked=True,allRepeatedDoubleBitsExact=True)

def qualify(c):
    out=c['folder']/'native_compound_attract_mix.json'
    need(not out.exists() and c['terminal']['nativeExit']==0 and not native.census() and c['guest']==original.current.expected(),
         'Same actual terminal native process and complete compiled guest')
    transport=json.loads((c['folder']/'report.json').read_text())
    need(transport['passed'] and transport['requestedConfigurationAccepted'],'Actual corrected physical timing, not the failed private-environment wrapper')
    predicted,actual,model=predict(c)
    different=np.argwhere(predicted!=actual)
    result=dict(passed=not len(different),comparedStereoFrames=len(actual),differentChannelSamples=len(different),
        firstDifferences=[dict(stereoFrame=int(n),channel=int(ch),expected=int(predicted[n,ch]),actual=int(actual[n,ch])) for n,ch in different[:8]],
        actualSHA256=hashlib.sha256(actual.tobytes()).hexdigest().upper(),predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
        sourceEvents=[{k:(float(v) if k=='gain' else v) for k,v in e.items() if k not in ('signal','positions')} for e in model['events']],
        nativeTerminal=c['terminal'],actualWinnerCallRows=original.names.runtime.rows(c['text'],'WINNER_CALL'),
        nativeDCSSamples=model['nativeSamples'],nonzeroNativeDCSSamples=model['nonzeroNativeSamples'],
        physicalInputs=transport['actualPhysicalInputs'],fullAttractAudioAccepted=False,fullPortAcceptance=False,
        audibleKanoDemoLaunchAccepted=False,goalStatus='active',sourceHashes={**model['pins'],str(Path(__file__).resolve()):sha(__file__),str(Path(original.__file__).resolve()):sha(original.__file__)})
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','comparedStereoFrames','differentChannelSamples','audibleKanoDemoLaunchAccepted')}),flush=True)
    return result

def contribution(c,event,full=False):
    pieces=[]
    for record in c['pcm']:
        h=record['header'];tick=int(Decimal(h['seconds'])*50)
        sec,frac=divmod((tick-1)*960*(original.names.audio.ATTO//48000),original.names.audio.ATTO)
        view=sec*48000+frac//original.names.audio.PERIOD
        at=np.arange(view,view+960,dtype=np.int64)-event['start']
        limit=len(event['signal']) if full else event['count']
        valid=(at>=0)&(at<limit)
        mono=np.zeros(960,dtype='<f4');mono[valid]=np.float32(event['signal'][at[valid]]*event['gain'])
        pieces.append(np.column_stack((mono,mono)))
    return np.concatenate(pieces)

def finish(c):
    out=c['folder'];receipt=out/'verified_progress.json'
    need(not receipt.exists() and c['terminal']['nativeExit']==0 and not native.census(),'Original native process terminal and fresh finite receipt')
    passed=json.loads((out/'native_compound_attract_mix.json').read_text())
    need(passed['passed'] and passed['differentChannelSamples']==0,'Preserve complete original audio comparison')
    predicted,actual,model=predict(c)
    need(np.array_equal(predicted,actual),'Whole actual positive before source counterexamples')
    channel_result=channels(c,model)
    inputs=original.names.runtime.rows(c['text'],'INPUT')
    need([(int(r['frame']),r['value'],r['button']) for r in inputs]==
         [(f,'1','HighPunch') for f in range(420,424)]+[(424,'0','HighPunch')],'Every actual configured physical input and release')
    config=original.names.runtime.rows(c['text'],'CONFIG')
    need(len(config)==1 and config[0]['boot_start']=='420' and config[0]['capture_winners']=='1','Actual corrected observer configuration')
    need(not original.names.runtime.rows(c['text'],'RESET') and not original.names.runtime.rows(c['text'],'ERROR_ENTRY'),
         'No reset or executed native error throughout the whole87531-field attract run')
    faults=[]
    for label,i,ch in [('first actual speaker bit',0,0),('final actual speaker bit',len(actual)-1,1)]:
        bad=actual.copy();bad[i,ch]^=1
        need(not np.array_equal(predicted,bad),'Actual whole PCM corruption rejected')
        faults.append(dict(fault=label,differentSamples=int(np.count_nonzero(predicted!=bad))))
    need(predicted.shape!=actual[:-1].shape,'Actual whole final stereo frame cannot be omitted')
    faults.append(dict(fault='omitted final stereo frame',rejectedBy='whole shape'))
    convert=lambda x:(np.clip(x,-1,1).astype(np.float64)*32767).astype('<i2')
    square=next(e for e in model['events'] if e['marker']['word']=='6B00')
    for label,bad in [('Square incorrectly continues through next launch',convert(np.float32(model['dcs']+model['voice']-contribution(c,square)+contribution(c,square,True)))),
                      ('original native DCS omitted',convert(model['voice']))]:
        need(not np.array_equal(bad,actual),'Nonvacuous whole original source operation fault')
        faults.append(dict(fault=label,differentSamples=int(np.count_nonzero(bad!=actual))))
    for event in [e for e in model['events'] if e['marker']['word'] in ('6B01','6B02')]:
        bad=convert(np.float32(model['dcs']+model['voice']-contribution(c,event)))
        need(not np.array_equal(bad,actual),'Each real overlapping Bicycle source contributes actual audible samples')
        faults.append(dict(fault=event['marker']['word']+' actual source omitted',differentSamples=int(np.count_nonzero(bad!=actual))))
    exact=original.names.audio.rows(c['text'],'MK2_TOMB_MIX_CHANNEL')[0]
    before=' '.join(k+'='+v for k,v in exact.items())
    need(before in c['text'],'Whole actual precise row located')
    wrong=dict(exact,bits='0000000000000000')
    need(wrong['bits']!=exact['bits'],'Effective native playback bit corruption')
    altered=dict(c,text=c['text'].replace(before,' '.join(k+'='+v for k,v in wrong.items()),1))
    try:channels(altered,model)
    except ValueError as error:faults.append(dict(fault='actual precise source-position bits altered',rejectedBy=str(error)))
    else:raise ValueError('Actual precise channel corruption admitted')
    for name,buffers in [('captured_native_audio.pcm.gz',[r['pixels'] for r in c['pcm']]),('captured_native_dac.f32.gz',c['dac'])]:
        path=out/name;need(not path.exists(),'One original compact proof carrier, not an asset/build duplicate')
        with gzip.open(path,'wb') as f:
            for raw in buffers:f.write(raw)
        with gzip.open(path,'rb') as f:
            need(all(f.read(len(raw))==raw for raw in buffers) and not f.read(),'Complete archived original bytes match')
    sources={}
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):
            path=Path(file).resolve();sources[str(path)]=dict(sha256=sha(path),text=path.read_text())
    with gzip.open(out/'executed_qualification_sources.json.gz','wt',encoding='utf-8') as f:json.dump(sources,f)
    result=dict(goalStatus='active',fullPortAcceptance=False,fullAttractAudioAccepted=False,publicBuildPromoted=False,
        thisGoalTurnClassification='progress: audible Sonya mirror EOF, corrected real alternate-button timing, native Sonya/Reptile Square-to-Bicycle replacement and overlapping voices, complete DCS/mixer PCM and all-channel clocks verified',
        nativeTerminal=c['terminal'],finiteCompoundAttractAudio=passed,preciseSources=channel_result,faultsRejected=faults,
        wholePCMHeaders=[r['header'] for r in c['pcm']],wholeDACHeaders=c['dacHeaders'],
        audibleKanoAttractLaunchAccepted=False,winnerMuteReachabilityAcceptance=False,
        winnerCallObservation='Actual native opcode observer enabled for the entire run; no winner announcement call observed. Do not claim that this verifies all winner mute behavior.',
        originalRemainingScope=json.loads((ROOT/'audit_native_dual_roll_progress_storage/report.json').read_text())['remaining'],
        nextAction='Reconcile the complete natural-character requirement list against current accepted evidence and exact changed-source conservation. Run the actual remaining current-build campaign/finisher/UI/reset/morph integration gaps, not already accepted unchanged cases. Audible Kano attract and full native mute/scene-owner interruption remain unproven. Final matching public CMD and portable ZIP still required.',
        newBuilds=0,newROMCopies=0,newZIPs=0,compilerCacheAbsent=not (ROOT/'mame-mkp/build/mingw-gcc').exists())
    receipt.write_text(json.dumps(result,indent=2)+'\n')
    storage=[]
    for path in [p for p in out.rglob('*') if p.is_file()]+[Path(__file__).resolve()]:
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(),'Exact in-workspace original proof target')
        digest=sha(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],check=True,capture_output=True)
        need(sha(path)==digest,'Original actual evidence unchanged by compression')
        storage.append(dict(path=str(path),allocatedBytes=allocated(path),sha256=digest))
    (out/'storage_receipt.json').write_text(json.dumps(dict(passed=True,exactFiles=storage,newBuilds=0,newROMCopies=0,newZIPs=0),indent=2)+'\n')
    print(json.dumps(dict(passed=True,comparedStereoFrames=len(actual),preciseChannelStates=channel_result['preciseChannelStates'],
                         effectiveFaults=len(faults),allocatedEvidenceBytes=sum(r['allocatedBytes'] for r in storage),fullPortAcceptance=False)),flush=True)
    return result
