"""Finish the actual audible Square run: complete source clocks and finite EOF.

This does not claim all attract interruptions or the complete character port.
The game receives only ordinary factory-screen High Punch. Faults below alter
copies of evidence/model output, never emulated memory, AI or audio.
"""
import gzip
import hashlib
import json
import struct
import subprocess
import sys
import wave
from decimal import Decimal
from pathlib import Path
import numpy as np
import qualify_native_attract_early_square as mix
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=mix.ROOT,mix.need,mix.sha

def channels(c,model):
    headers=[r['header'] for r in c['pcm']]
    rows=mix.names.audio.rows(c['text'],'MK2_TOMB_MIX_CHANNEL')
    need(len(rows)==len(headers)*14 and {(int(r['index']),int(r['channel'])) for r in rows}==
         {(i,ch) for i in range(1,len(headers)+1) for ch in range(14)},'Every precise source channel on every actual callback')
    events=[]
    for event in model['events']:
        ch=event.get('channel',0)
        filename='sonya_square_launch.wav' if ch==10 else ('kano_select.wav' if event['identity']==17 else 'sonya_select.wav')
        with wave.open(str(ROOT/'samples/mk2ks'/filename),'rb') as wav:
            length,freq=wav.getnframes(),wav.getframerate()
            _,positions=mix.names.audio.sample_values(np.frombuffer(wav.readframes(length),'<i2').copy(),freq)
        events.append(dict(event,channel=ch,length=length,positions=positions,sample_id=13 if ch==10 else (0 if event['identity']==17 else 1)))
    active={0:0,10:0};tails={0:0,10:0}
    played_events=set();ended_events=set()
    for row in rows:
        index,ch=int(row['index']),int(row['channel']);h=headers[index-1]
        need(all(row[k]==h[k] for k in ('frame','seconds')) and row['loop']==row['paused']=='0' and
             row['writes']=='0' and row['assistance']=='none','Actual non-looping passive source callback association')
        tick=int(Decimal(h['seconds'])*50)
        sec,frac=divmod(tick*960*(mix.names.audio.ATTO//48000),mix.names.audio.ATTO)
        end=sec*48000+(frac+mix.names.audio.PERIOD-1)//mix.names.audio.PERIOD
        launches=[e for e in events if e['channel']==ch and e['start']<=end]
        number,length,position=0xffffffff,0,0.0
        if launches:
            event=launches[-1]
            count=min(len(event['positions']),max(0,end-event['start']))
            length=event['length'];position=event['positions'][count-1] if count else 0.0
            playing=0<count<len(event['positions'])
            # Stock samples.cpp sets source_num from the PREVIOUS source_len.
            # Both biography announcements share channel0. Sonya's later
            # start therefore sees Kano's completed length18400, not zero.
            prior_length=0 if len(launches)==1 else launches[-2]['length']
            if playing:
                active[ch]+=1;played_events.add(event['marker']['word'])
                if prior_length:number=event['sample_id']
            if count==len(event['positions']):
                tails[ch]+=1;ended_events.add(event['marker']['word'])
        need(int(row['sample'])==number and int(row['length'])==length and float(row['position'])==position and
             row['bits']==struct.pack('<d',position).hex().upper(),'Exact native source ID, full length and every repeated-double playback/EOF bit')
    need(all(active.values()) and all(tails.values()) and played_events==ended_events=={'FFFC','FFFB','6B00'},
         'All three real sources cover playback and complete EOF tails')
    sample_source=ROOT/'mame-mkp/src/devices/sound/samples.cpp'
    need(sha(sample_source)=='8BF4BB350F40B309A5CECB4591DF8EE32A3563C3E061F2D2338C8CBA76B5353F',
         'Compiled original sample interpolation, previous-length source ID and finite EOF behavior conserved')
    return dict(passed=True,preciseChannelStates=len(rows),activeCallbacks=active,finiteEOFTailCallbacks=tails,
                sourceNumberUsesPreviousLength=True,allRepeatedDoubleBitsExact=True,allFourteenChannelsChecked=True)

def policy(c):
    rows=lambda tag:mix.names.runtime.rows(c['text'],tag)
    inputs=rows('INPUT');dip=rows('DIP');switch=rows('SWITCH_POLICY');mute=rows('MUTE_POLICY')
    need([(int(r['frame']),r['value'],r['button']) for r in inputs]==
         [(f,'1','HighPunch') for f in range(360,364)]+[(364,'0','HighPunch')], 'Only actual ordinary cold-boot acknowledgement and release')
    need(len(dip)==1 and all(dip[0][k]=='1000' for k in ('mask','default','configured')) and dip[0]['actual']=='FC7D',
         'Actual default Attract Sound On DIP, never a forced native sound flag')
    need(len(switch)==1 and switch[0]['pc']=='FF8474B0' and switch[0]['a0']=='000041C0' and switch[0]['dsw']=='FC7D',
         'Actual original native initial policy return has disable bit8 clear')
    launch=next(e['marker'] for e in mix.predict(c)[2]['events'] if e.get('channel')==10)
    prior=[r for r in mute if Decimal(r['seconds'])<=Decimal(launch['seconds'])]
    need(prior[-1]['pc']=='FF8278D0' and prior[-1]['value']=='0', 'Natural demo startup restored the original unmuted flag')
    late=[r for r in mute if r['pc']=='FF843960' and r['value']=='1']
    need(late and int(late[0]['frame'])>int(launch['frame']), 'Original later attract sequence mute policy still executes naturally')
    script=ROOT/'mk2ks_native_attract_early_launch.lua'
    text=script.read_text()
    need(text.count(':set_value(')==1 and 'frame>=360 and frame<364' in text and ':write_' not in text,
         'Executed observer exposes only ordinary button input and passive native reads/taps')
    return dict(passed=True,physicalInputs=inputs,actualDIP=dip,actualInitialStockPolicy=switch,
                lastMuteWriteBeforeLaunch=prior[-1],actualLaterStockMute=late[0],fullMuteInterruptionAcceptance=False)

def finish(c):
    out=c['folder'];receipt=out/'verified_progress.json'
    need(not receipt.exists() and c['terminal']['nativeExit']==0 and not native.census() and c['guest']==mix.current.expected(),
         'Original native job terminal, no replacement run, and full compiled guest exact')
    passed=json.loads((out/'native_early_square_mix.json').read_text())
    need(passed['passed'] and passed['differentChannelSamples']==0,'Preserved original complete PCM equality')
    predicted,actual,model=mix.predict(c)
    need(np.array_equal(predicted,actual),'Full actual source-positive before effective counterexamples')
    precise=channels(c,model);sound_policy=policy(c)
    faults=[]
    convert=lambda x:(np.clip(x,-1,1).astype(np.float64)*32767).astype('<i2')
    for label,i,ch in [('first actual speaker bit',0,0),('final actual speaker bit',len(actual)-1,1)]:
        bad=actual.copy();bad[i,ch]^=1
        need(not np.array_equal(predicted,bad),'Actual PCM bit fault rejected')
        faults.append(dict(fault=label,differentSamples=int(np.count_nonzero(predicted!=bad))))
    need(actual[:-1].shape!=predicted.shape,'Missing complete final stereo frame rejected')
    faults.append(dict(fault='omitted final stereo frame',rejectedBy='whole shape'))
    start=model['windows'][2][0]*960;stop=(model['windows'][2][-1]+1)*960
    square=model['voice'].copy();square[:start]=0;square[stop:]=0
    late=np.zeros_like(square);late[1:]=square[:-1]
    for label,bad in [('actual DCS omitted',convert(model['voice'])),
                      ('actual Square omitted',convert(np.float32(model['dcs']+model['voice']-square))),
                      ('Square starts one sample late',convert(np.float32(model['dcs']+model['voice']-square+late))),
                      ('Square native .70 gain omitted',convert(np.float32(model['dcs']+model['voice']-square+square/np.float32(.70))))]:
        need(not np.array_equal(bad,actual),'Effective native source-operation fault rejected')
        faults.append(dict(fault=label,differentSamples=int(np.count_nonzero(bad!=actual))))
    for key,value in [('p1_id','17'),('mute','1'),('p1_owner','00000000')]:
        row=next(e['marker'] for e in model['events'] if e.get('channel')==10)
        changed=dict(row,**{key:value})
        original=' '.join(k+'='+v for k,v in row.items())
        need(original in c['text'],'Exact whole actual launch row located')
        bad=dict(c,text=c['text'].replace(original,' '.join(k+'='+v for k,v in changed.items()),1))
        try:mix.predict(bad)
        except ValueError as error:faults.append(dict(fault='actual launch '+key+' altered',rejectedBy=str(error)))
        else:raise ValueError('Invalid actual source owner admitted')
    for carrier,headers in [('pcm',[r['header'] for r in c['pcm']]),('dac',c['dacHeaders'])]:
        path=out/('captured_native_audio.pcm.gz' if carrier=='pcm' else 'captured_native_dac.f32.gz')
        need(not path.exists(),'One compact original evidence carrier, no duplicate build/assets')
        buffers=[r['pixels'] for r in c['pcm']] if carrier=='pcm' else c['dac']
        with gzip.open(path,'wb') as f:
            for raw in buffers:f.write(raw)
        with gzip.open(path,'rb') as f:
            need(all(f.read(len(raw))==raw for raw in buffers) and not f.read(),'Every archived actual byte preserved')
    sources={}
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):
            path=Path(file).resolve();sources[str(path)]=dict(sha256=sha(path),text=path.read_text())
    with gzip.open(out/'executed_qualification_sources.json.gz','wt',encoding='utf-8') as f:json.dump(sources,f)
    result=dict(goalStatus='active',fullPortAcceptance=False,fullAttractAudioAccepted=False,publicBuildPromoted=False,
        previousGoalTurnClassification='no progress: acknowledgement only; revalidated same retained live host and terminal native job',
        thisGoalTurnClassification='progress: actual audible true Sonya18 CPU Square demo, complete DCS/clip speaker equality, precise all-channel playback/EOF and original native sound policy verified',
        nativeTerminal=c['terminal'],finiteAudibleSonyaSquare=passed,preciseSources=precise,originalSoundPolicy=sound_policy,
        faultsRejected=faults,wholePCMHeaders=[r['header'] for r in c['pcm']],wholeDACHeaders=c['dacHeaders'],
        originalRemainingScope=json.loads((ROOT/'audit_native_dual_roll_progress_storage/report.json').read_text())['remaining'],
        nextAction='Audible native Kano attract startup and broader launch interruption/scene/mute cleanup; broader actual-ID CPU/arena and current campaign/finisher/UI/reset/morph integration; matching public CMD and finished portable ZIP.',
        newBuilds=0,newROMCopies=0,newZIPs=0,compilerCacheAbsent=not (ROOT/'mame-mkp/build/mingw-gcc').exists())
    receipt.write_text(json.dumps(result,indent=2)+'\n')
    paths=[p for p in out.rglob('*') if p.is_file()]+[Path(__file__).resolve(),Path(mix.__file__).resolve()]
    storage=[]
    for path in paths:
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(),'Exact in-workspace evidence target')
        digest=sha(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],check=True,capture_output=True)
        need(sha(path)==digest,'Compression preserves actual original evidence bytes')
        storage.append(dict(path=str(path),allocatedBytes=allocated(path),sha256=digest))
    (out/'storage_receipt.json').write_text(json.dumps(dict(passed=True,exactFiles=storage,newBuilds=0,newROMCopies=0,newZIPs=0),indent=2)+'\n')
    print(json.dumps(dict(passed=True,comparedStereoFrames=len(actual),preciseChannelStates=precise['preciseChannelStates'],
                         effectiveFaults=len(faults),allocatedEvidenceBytes=sum(r['allocatedBytes'] for r in storage),fullPortAcceptance=False)),flush=True)
    return result
