"""Same terminal44988: whole native mixed PCM with both real Square launches.

Retain the original float32 DCS cache/resampler, sample interpolation, mixer,
EOF semantics, exact callback clocks and all original corruption trials.
Repeated launches are admitted only when their native channel intervals are
disjoint; this is not a generic overlap/replacement or other-context claim.
"""
import hashlib
import inspect
import json
import re
import struct
import traceback
import wave
from decimal import Decimal
from pathlib import Path
import numpy as np
import qualify_native_selector_cpu_projectile_pcm_mix as prior
import capture_native_selector_sonya_choice_shadow_bound_loader as capture
import qualify_native_selector_sonya_shadow_geometry as geometry
import capture_current_subzero_audio_v6213 as dac_model

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
model=prior.model
OUT=ROOT/'audit_native_selector_sonya_repeated_cue_pcm_checked'
PARENT=geometry.OUT/'report.json'


def sources(text,pins):
    commands=model.rows(text,'MK2_MAUDIO_SOUND');result=[]
    observed=[r for r in commands if 0x6b00<=int(r['word'],16)<=0x6b03]
    need([(r['word'],r['frame'],r['pc']) for r in observed]==[
        ('6B00','1966','FFFFCAC0'),('6B00','3011','FFFFCAC0'),
        ('6B01','3191','FFF9A4C0'),('6B02','3191','FFF9A520')],
        'All actual owned repeated Square/bicycle cues, no inferred activation')
    need(all(r['a8']=='010350A0' and r['a13']=='0106BF30' and r['mask']=='FFFF' and
             r['writes']=='0' and r['assistance']=='none' for r in observed),
         'Every executing cue true Sonya actor/Main and full physical store')
    for word,sample,channel,name,length in prior.SPECS:
        selected=[r for r in observed if r['word']==word]
        need(len(selected)==(2 if word=='6B00' else 1),'Complete repeated source inventory')
        path=ROOT/'samples/mk2ks'/name
        need(str(path) in pins and sha(path)==pins[str(path)],'Whole original source clip '+name)
        with wave.open(str(path),'rb') as clip:
            need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==
                 (1,2,48000,length),'Whole original source dimensions')
            values=np.frombuffer(clip.readframes(length),dtype='<i2').copy()
        for marker in selected:
            result.append(dict(word=word,sample=sample,channel=channel,name=name,length=length,
                marker=marker,start=model.sample_clock(marker['seconds'],True),values=values))
    for channel in (12,13):
        owned=[s for s in result if s['channel']==channel]
        need(all(a['start']+a['length']<b['start'] for a,b in zip(owned,owned[1:])),
             'Actual same-channel sources finish before each later native launch')
    return result


def bindings():
    source=inspect.getsource(prior.mixer)
    old='source_contributions[1]'
    need(source.count(old)==3,'Whole original bicycle volume fault remains present')
    source=source.replace(old,"source_contributions[next(i for i,s in enumerate(extra) if s['word']=='6B01')]")
    scope=dict(vars(prior),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_mixer_repeated_cues','exec'),scope)
    predict,model_hash=scope['mixer']()
    clocks=inspect.getsource(prior.channel_clocks)
    changes=[
        ("parent=extra[0]if spec['word']=='6B00'else extra[1]",
         "parent=spec if spec['word']=='6B00' else next(s for s in extra if s['word']=='6B01')"),
        ("n*800>=extra[1]['length']","n*800>=parent['length']"),
        ("need(actual==want,'Every source-derived native channel/length/position ",
         "need(actual[:2]==want[:2] and (r['pos']==format(want[2],'.8f') if video else actual[2]==want[2]),'Every source-derived native channel/length/position ")]
    for old,new in changes:
        need(clocks.count(old)==1,'Exact original timer/serialization binding '+old)
        clocks=clocks.replace(old,new,1)
    exec(compile(clocks,__file__+'::whole_original_clocks_each_actual_launch','exec'),scope)
    return predict,scope['channel_clocks'],model_hash,hashlib.sha256(clocks.encode()).hexdigest().upper()


def execute(state):
    need(not OUT.exists(),'Fresh immutable repeated-cue qualification')
    parent=json.loads(PARENT.read_text());pins=dict(parent['inputHashes'])
    need(parent['passed'] and all(sha(p)==h for p,h in pins.items()),'Whole current geometry/source/evidence inventory unchanged')
    folder,text,images=capture.RAM_CASES[capture.KEY];audio=capture.AUDIO[capture.KEY]
    held=capture.NATIVE_HANDLES[capture.KEY];meta=json.loads((folder/'result.json').read_text())
    need(meta['passed'] and held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==meta['nativeTerminal']['actualWindowsIdentity']==parent['actualNativeIdentity'] and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (44988,38752,1791753882.5997791) and not meta['nativeTerminal']['hostDecodeErrors'],
         'Same original terminal44988 physical-input game and exact retained handle')
    for tag,chunks,headers in [('MK2_BBAUDIO_PCM_DIGEST',audio['pcmChunks'],audio['pcmHeaders']),
                               ('MK2_NATIVE_DAC_RAM_DIGEST',audio['dacChunks'],audio['dacHeaders'])]:
        records=model.rows(text,tag)
        need(len(records)==len(chunks)==len(headers)==1646 and
             all(r==dict(h,sha256=hashlib.sha256(raw).hexdigest().upper()) for r,h,raw in zip(records,headers,chunks,strict=True)),
             'Every entire actual PCM/DAC callback and independent digest')
    native_dac,dac_faults,dac_hash=dac_model.dac_models(1646)
    dac=native_dac(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders'])
    raw_faults=list(dac_faults(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders']))
    rom_gate,rom_faults=model.rom_models(audio['expectedROM'])
    rom=[rom_gate(bytes(audio['rom'][phase]),phase) for phase in ('startup','terminal')]
    for phase in ('startup','terminal'):raw_faults.extend(rom_faults(bytes(audio['rom'][phase]),phase))
    need(len(raw_faults)==12,'All original DAC and both whole sound-ROM fault suites')
    video=model.rows(text,'MK2_MAUDIO_CHANNEL');precise=model.rows(text,'MK2_TOMB_MIX_CHANNEL')
    need([(int(r['frame']),int(r['channel'])) for r in video]==[(f,c) for f in range(1818,3619) for c in range(19)] and
         [(r['frame'],r['seconds'],int(r['channel'])) for r in precise]==
         [(h['frame'],h['seconds'],c) for h in audio['pcmHeaders'] for c in range(19)],
         'All nineteen channels at every independent native video/sound callback')
    extra=sources(text,pins);predict,clocks,mix_hash,clock_hash=bindings()
    pcm=np.frombuffer(b''.join(audio['pcmChunks']),dtype='<i2').reshape(-1,2)
    waveform=predict(audio['dacChunks'],audio['dacHeaders'],pcm,text,'sonya',pins,extra)
    # Preserve a complete actual disagreement even when subsequent clocks fail.
    OUT.mkdir();geometry.coverage.original.phases.original.capture.choices.current.prior.save(OUT/'waveform.json',waveform)
    need(waveform['passed'],'Entire source-predicted repeated-cue native PCM must match without a fit')
    clock_result=clocks(text,audio['pcmHeaders'],extra,waveform)
    clock_faults=[]
    def change(tag,key,value,**where):
        line=next(s for s in text.splitlines() if s.startswith(tag+' ') and
                  all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v) for k,v in where.items()))
        bad,count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(count==1 and bad!=line,'Effective actual channel counterexample')
        return text.replace(line,bad,1)
    for label,bad in [
        ('second Square source length',change('MK2_MAUDIO_CHANNEL','length','45513',frame=3012,channel=12)),
        ('second Square precise clock',change('MK2_TOMB_MIX_CHANNEL','position','0',channel=12,seconds='55.060000000000')),
        ('bicycle source channel',change('MK2_MAUDIO_CHANNEL','sample','4294967295',frame=3192,channel=12)),
        ('cry position bits',change('MK2_TOMB_MIX_CHANNEL','bits','0000000000000000',channel=13,seconds='58.340000000000')),
        ('inactive private channel',change('MK2_MAUDIO_CHANNEL','length','1',frame=3200,channel=18)),
        ('passive channel assistance',change('MK2_MAUDIO_CHANNEL','writes','1',frame=3200,channel=12))]:
        try:clocks(bad,audio['pcmHeaders'],extra,waveform)
        except (ValueError,AssertionError,KeyError,IndexError) as error:clock_faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual source-clock corruption accepted '+label)
    need(clocks(text,audio['pcmHeaders'],extra,waveform)==clock_result,'Whole original clock positive restored')
    paths=(Path(__file__),PARENT,Path(prior.__file__),Path(model.__file__),Path(dac_model.__file__),
           ROOT/'mame-mkp/src/devices/sound/samples.cpp',ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp',
           ROOT/'diagnostic_native_selector_layers_long/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp',
           ROOT/'samples/mk2ks/sonya_select.wav',OUT/'waveform.json')
    for path in paths:
        key=str(path.resolve());digest=sha(path)
        need(key not in pins or pins[key]==digest,'No historical input hash silently replaced');pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'Complete immutable inputs after full waveform and faults')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],wholeMixedWaveform=waveform,
        wholeSourceChannelClocks=clock_result,wholeNativeDAC=dac,wholeSoundROM=rom,
        originalDACROMFaultsRejected=raw_faults,actualChannelClockFaultsRejected=clock_faults,
        entireSourceModelSHA256=mix_hash,entireClockModelSHA256=clock_hash,nativeDACModelSHA256=dac_hash,
        inputHashes=pins,requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        finiteRepeatedCueSourceExactAudioAccepted=True,allOverlapHitOwnerContextsAccepted=False,
        heardAudioQualityAccepted=False,fullArtAudioAllContextsAcceptance=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    geometry.coverage.original.phases.original.capture.choices.current.prior.save(OUT/'report.json',value)
    print('PASS same44988 whole repeated-cue native PCM/channel clocks/DAC-ROM',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        if not OUT.exists():OUT.mkdir()
        need(not (OUT/'failure.json').exists(),'Preserve original repeated-cue rejection')
        geometry.coverage.original.phases.original.capture.choices.current.prior.save(OUT/'failure.json',
            dict(passed=False,goalStatus='active',error=repr(error),traceback=traceback.format_exc(),
                 newNativeGames=0,fullPortAcceptance=False))
        raise
