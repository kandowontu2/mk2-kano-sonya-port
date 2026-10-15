"""Both actual Kano winner cues, whole same38692 native source-exact PCM.

Original float32 DCS/cache/resampler and complete winner source operations
retained. Actual channel0 sources are disjoint; not arbitrary replacement,
all owner/priority interruption contexts or heard-quality acceptance.
"""
import hashlib
import inspect
import json
import re
import struct
import traceback
import wave
from bisect import bisect_right
from decimal import Decimal
from pathlib import Path
import numpy as np
import capture_native_selector_sonya_human_kano_cpu as capture
import qualify_native_selector_opposite_roles_checkpoint as checkpoint
import current_tomb_winner_mix_fault_model_v5789 as model

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_opposite_roles_winner_pcm_checked'
PARENT=checkpoint.OUT/'report.json'


def bindings():
    source=inspect.getsource(model.predict_mix)
    before="need(len(markers)==1 and markers[0]['word']==('FFFE'if fighter=='kano'else'FFFD'),"
    after="need(len(markers)==2 and all(m['word']==('FFFE'if fighter=='kano'else'FFFD') for m in markers),"
    need(source.count(before)==1,'Whole original true-character winner source gate')
    source=source.replace(before,after,1)
    a,z=source.index(' marker=markers[0]'),source.index(' mixed=np.float32(dcs+voice)')
    body=source[a:z]
    need(body.count('marker=markers[0]')==1,'One entire original source/stream-clock/interpolation block')
    body=body.replace('marker=markers[0]','marker=current_marker',1)
    multiple=""" winner_parts=[];winner_sources=[]
 for current_marker in markers:
"""+'\n'.join(' '+line for line in body.splitlines())+"""
  winner_parts.append(voice)
  winner_sources.append(dict(marker=marker,startStreamIndex=start,outputSamples=len(sample),
   firstWindowSample=first_offset,expectedCallbackStates=callback_states))
 need(all(a['startStreamIndex']+a['outputSamples']<b['startStreamIndex'] for a,b in zip(winner_sources,winner_sources[1:])),
  'Actual native channel0 winner sources finish before each later launch')
 voice=np.zeros_like(dcs)
 for part in winner_parts:voice=np.float32(voice+part)
"""
    source=source[:a]+multiple+source[z:]
    before=' return dict(passed=not len(different),actualRawMixedPCMFaultsRejected=raw_faults,'
    after=""" repeated_faults=[]
 if not len(different):
  for index,part in enumerate(winner_parts):
   wrong=convert(np.float32(dcs+np.float32(voice-part)))
   need(not np.array_equal(wrong,pcm),'Each actual winner announcement omission is effective')
   repeated_faults.append(dict(fault='omit actual winner '+str(index+1),differentChannelSamples=int(np.count_nonzero(wrong!=pcm))))
 return dict(completeActualWinnerSources=winner_sources,actualRepeatedWinnerFaultsRejected=repeated_faults,
  passed=not len(different),actualRawMixedPCMFaultsRejected=raw_faults,"""
    need(source.count(before)==1,'All original PCM and source-operation fault suites remain')
    source=source.replace(before,after,1)
    scope=dict(vars(model),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_mixer_both_actual_winners','exec'),scope)
    return scope['predict_mix'],hashlib.sha256(source.encode()).hexdigest().upper()


def channel_clocks(text,headers,pins):
    markers=[r for r in model.rows(text,'MK2_MAUDIO_SOUND') if r['pc']=='FFFB7140']
    need([(r['frame'],r['word'],r['a8'],r['a13']) for r in markers]==[
        ('2286','FFFE','FFFEFD10','0106AA60'),('3137','FFFE','FFFEFD10','0106AA60')],
        'Both actual true Kano winner producers')
    need(all(r['mask']=='FFFF' and r['writes']=='0' and r['assistance']=='none' for r in markers),
         'Every actual native winner port store and passive observer')
    need(not [r for r in model.rows(text,'MK2_MAUDIO_SOUND') if 0x6b00<=int(r['word'],16)<=0x6b03],
         'No unmodelled imported battle cue in this actual game')
    values,freq=model.read_winner('kano',pins)
    _,positions=model.sample_values(values,freq)
    selection_path=ROOT/'samples/mk2ks/sonya_select.wav'
    need(str(selection_path) in pins and sha(selection_path)==pins[str(selection_path)],'Whole original actual Sonya selection source')
    with wave.open(str(selection_path),'rb') as clip:
        need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==(1,2,16000,18400),
             'Complete original selection pointer/frequency/length')
        selection=np.frombuffer(clip.readframes(clip.getnframes()),'<i2').copy()
    _,selection_positions=model.sample_values(selection,16000)
    ticks=[Decimal(h['seconds']) for h in headers]
    def expected(channel,clock):
        if channel!=0:return 0xffffffff,0,0.0
        actual=[r for r in markers if Decimal(r['seconds'])<=Decimal(clock)]
        if not actual:return 0xffffffff,18400,selection_positions[-1]
        source=actual[-1];i=bisect_right(ticks,Decimal(clock))-1
        last=headers[i]['seconds'] if i>=0 else str(Decimal(headers[0]['seconds'])-Decimal('.02'))
        processed=max(0,model.sample_clock(last,True)-model.sample_clock(source['seconds'],True))
        position=positions[min(processed,len(positions))-1] if processed else 0.0
        return 2 if processed<len(positions) else 0xffffffff,32000,position
    counts={}
    for tag,video in [('MK2_MAUDIO_CHANNEL',True),('MK2_TOMB_MIX_CHANNEL',False)]:
        records=model.rows(text,tag);counts[tag]=len(records)
        for r in records:
            want=expected(int(r['channel']),r['seconds'])
            actual=(int(r['sample']),int(r['length']),float(r['pos'] if video else r['position']))
            need(actual[:2]==want[:2] and (r['pos']==format(want[2],'.8f') if video else actual[2]==want[2]),
                 'Every original source-derived channel/length/position '+str((tag,r['frame'],r['channel'],actual,want)))
            if not video:need(r['bits']==struct.pack('<d',want[2]).hex().upper(),'Every full64-bit native source position')
            need(r['loop']==r['paused']==r['writes']=='0' and r['assistance']=='none','Whole passive nonlooping source history')
    return dict(passed=True,completeVideoRows=counts['MK2_MAUDIO_CHANNEL'],completeSoundRows=counts['MK2_TOMB_MIX_CHANNEL'],
        sourceStarts=[dict(marker=r,startStreamIndex=model.sample_clock(r['seconds'],True)) for r in markers],
        completeSourceChannelOrder=[0],initialSelectionPointerNotAssumedEmpty=True,noPositionOrWaveformFit=True)


def execute(state):
    need(not OUT.exists(),'Fresh immutable two-winner waveform qualification')
    parent=json.loads(PARENT.read_text());pins=dict(parent['inputHashes'])
    folder,text,images=capture.RAM_CASES[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    meta=json.loads((folder/'result.json').read_text());audio=capture.AUDIO[capture.KEY]
    need(parent['passed'] and meta['passed'] and held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==parent['actualNativeIdentity']==meta['nativeTerminal']['actualWindowsIdentity'] and
         all(sha(p)==h for p,h in pins.items()),'Same original terminal38692 and full1253 inputs, no replay')
    for tag,chunks,headers in [('MK2_BBAUDIO_PCM_DIGEST',audio['pcmChunks'],audio['pcmHeaders']),
                               ('MK2_NATIVE_DAC_RAM_DIGEST',audio['dacChunks'],audio['dacHeaders'])]:
        records=model.rows(text,tag)
        need(len(records)==len(chunks)==len(headers)==1645 and
             all(r==dict(h,sha256=hashlib.sha256(raw).hexdigest().upper()) for r,h,raw in zip(records,headers,chunks,strict=True)),
             'Every original entire sound block/header independently digest-bound')
    video=model.rows(text,'MK2_MAUDIO_CHANNEL');precise=model.rows(text,'MK2_TOMB_MIX_CHANNEL')
    need([(int(r['frame']),int(r['channel'])) for r in video]==[(f,c) for f in range(1815,3616) for c in range(19)] and
         [(r['frame'],r['seconds'],int(r['channel'])) for r in precise]==
         [(h['frame'],h['seconds'],c) for h in audio['pcmHeaders'] for c in range(19)],
         'Every independent actual video/sound callback retains all19 channels')
    predict,source_hash=bindings();pcm=np.frombuffer(b''.join(audio['pcmChunks']),dtype='<i2').reshape(-1,2)
    waveform=predict(audio['dacChunks'],audio['dacHeaders'],pcm,text,'kano',pins)
    OUT.mkdir();capture.previous.choices.current.prior.save(OUT/'waveform.json',waveform)
    need(waveform['passed'],'Entire two-winner native PCM must match without fitting')
    positive=channel_clocks(text,audio['pcmHeaders'],pins)
    def change(tag,key,value,**where):
        line=next(s for s in text.splitlines() if s.startswith(tag+' ') and
                  all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v) for k,v in where.items()))
        bad,count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(count==1 and bad!=line,'Effective real native source-clock counterexample')
        return text.replace(line,bad,1)
    active=next(r for r in video if r['channel']=='0' and r['sample']=='2' and int(r['frame'])>3137 and float(r['pos'])>0)
    full=next(r for r in precise if r['channel']=='0' and r['sample']=='2' and int(r['frame'])>3137 and float(r['position'])>0)
    trials=[('wrong_winner_source',change('MK2_MAUDIO_CHANNEL','sample','3',frame=active['frame'],channel=0)),
            ('wrong_winner_length',change('MK2_MAUDIO_CHANNEL','length','31999',frame=active['frame'],channel=0)),
            ('second_winner_clock',change('MK2_MAUDIO_CHANNEL','pos',format(float(active['pos'])+1,'.8f'),frame=active['frame'],channel=0)),
            ('second_winner_position_bits',change('MK2_TOMB_MIX_CHANNEL','bits','0000000000000000',seconds=full['seconds'],channel=0)),
            ('unmodelled_other_channel',change('MK2_MAUDIO_CHANNEL','length','1',frame=active['frame'],channel=18)),
            ('channel_assistance',change('MK2_MAUDIO_CHANNEL','writes','1',frame=active['frame'],channel=0))]
    faults=[]
    for label,bad in trials:
        try:channel_clocks(bad,audio['pcmHeaders'],pins)
        except (ValueError,AssertionError,KeyError,IndexError) as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native source-clock corruption admitted '+label)
    need(channel_clocks(text,audio['pcmHeaders'],pins)==positive,'Whole source-clock positive restored')
    for path in (Path(__file__),PARENT,Path(model.__file__),ROOT/'mame-mkp/src/devices/sound/samples.cpp',
                 ROOT/'samples/mk2ks/sonya_select.wav',OUT/'waveform.json'):
        key=str(path.resolve());digest=sha(path)
        need(key not in pins or pins[key]==digest,'Never replace a historical input pin');pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'All source/evidence unchanged after whole prediction and faults')
    report=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],wholeMixedWaveform=waveform,
        wholeSourceChannelClocks=positive,actualChannelClockFaultsRejected=faults,entireSourceModelSHA256=source_hash,
        originalWholeDACROMReceipt=str(PARENT),inputHashes=pins,requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        finiteBothKanoWinnerSourceExactAudioAccepted=True,allOwnerOverlapPriorityContextsAccepted=False,
        heardAudioQualityAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    capture.previous.choices.current.prior.save(OUT/'report.json',report)
    print('PASS same38692 both Kano winners whole PCM/all19 channel clocks',flush=True)
    return report


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        if not OUT.exists():OUT.mkdir()
        need(not (OUT/'failure.json').exists(),'Preserve exact original two-winner rejection')
        capture.previous.choices.current.prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',newNativeGames=0,fullPortAcceptance=False))
        raise
