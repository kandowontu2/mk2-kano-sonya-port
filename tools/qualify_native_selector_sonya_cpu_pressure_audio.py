"""Whole retained real pressure-match source PCM, both Sonya winners and DCS.

All original float32 DAC/resampler/cache, sample interpolation/EOF/route gains,
packet/port/ADSP chronology and all19 channel clocks retained. Native FFF8 is
a genuine low packet byte, not a private fire cue. No waveform or timing fit,
new game, raw media copy, arbitrary channel replacement or heard-quality claim.
"""
import hashlib
import inspect
import json
import re
import struct
import traceback
from pathlib import Path
import numpy as np
import qualify_native_selector_opposite_roles_winner_pcm as winners
import qualify_native_selector_cpu_startup_ring_audio as startup
import qualify_native_selector_sonya_cpu_pressure_round_shadow_scope as geometry
import capture_current_subzero_audio_v6213 as dac_model

ROOT,need,sha=geometry.ROOT,geometry.need,geometry.sha
capture=geometry.previous.capture
model=winners.model
OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_audio_checked'
PARENT=geometry.OUT/'report.json'


def packet_gate(text):
    source=inspect.getsource(startup.packets.packet_gate)
    for before,after in (
        ('identity=17','identity=18'),
        ("need(len(markers)==1 and markers[0]['word']==('FFFE'if identity==17 else'FFFD')and markers[0]['mask']=='FFFF'and",
         "need(len(markers)==2 and all(r['word']==('FFFE'if identity==17 else'FFFD')and r['mask']=='FFFF'for r in markers)and"),
        ('len(all_sounds)==len(sounds)+1','len(all_sounds)==len(sounds)+2')):
        need(source.count(before)==1,'Only actual true-ID/two-winner packet inventory boundary')
        source=source.replace(before,after,1)
    scope=dict(vars(startup.packets),__file__=__file__)
    exec(compile(source,__file__+'::whole_original_all_packets_ADSP_two_Sonya_winners','exec'),scope)
    return scope['packet_gate'](text)


def channel_clocks(text,headers,pins):
    source=inspect.getsource(winners.channel_clocks)
    for before,after in (
        ("('2286','FFFE','FFFEFD10','0106AA60'),('3137','FFFE','FFFEFD10','0106AA60')",
         "('2367','FFFD','FFFEFF20','0106AA60'),('3215','FFFD','FFFEFF20','0106AA60')"),
        ("model.read_winner('kano',pins)","model.read_winner('sonya',pins)"),
        ("ROOT/'samples/mk2ks/sonya_select.wav'","ROOT/'samples/mk2ks/kano_select.wav'"),
        ('return 2 if processed<len(positions)','return 3 if processed<len(positions)')):
        need(source.count(before)==1,'Only actual Sonya producers/source number and completed human selection context')
        source=source.replace(before,after,1)
    scope=dict(vars(winners),__file__=__file__)
    exec(compile(source,__file__+'::whole_original19_channel_clocks_both_Sonya_winners','exec'),scope)
    return scope['channel_clocks'](text,headers,pins)


def routing_source(guest):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    lo,hi=(0xffa12530-0xff800000)//8,(0xffa13ed0-0xff800000)//8
    need(guest[lo:hi]==stock[lo:hi],'Entire original native priority/effect/packet/handshake program unchanged')
    source=(ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
    for fragment in ('bool const native_packet = m_maincpu->pc() == 0xffa13c90U ||',
        'm_maincpu->pc() == 0xffa13d60U;',
        'm_mk2ks_voices && !native_packet && (data == 0xfff8 || data == 0xfff7)',
        'm_mk2ks_voices && !native_packet && data >= 0xfffb && data <= 0xfffe',
        'm_mk2ks_voices->set_volume(0, 0.30f);',
        'm_dcs->data_w(data & 0xff);'):
        need(fragment in source,'Actual compiled native-packet/private-marker routing boundary '+fragment)
    return dict(passed=True,nativePacketStorePCs=['FFA13C90','FFA13D60'],
                actualNativePacketMarkerCannotLaunchPrivateSample=True,
                universalOtherSoundPriorityContextsAccepted=False)


def execute(state):
    need(not OUT.exists(),'Fresh immutable complete pressure source-audio qualification')
    parent=json.loads(PARENT.read_text());pins=dict(parent['inputHashes'])
    folder,text,images=capture.RAM_CASES[capture.KEY];audio=capture.AUDIO[capture.KEY]
    held=capture.NATIVE_HANDLES[capture.KEY];meta=json.loads((folder/'result.json').read_text())
    need(parent['passed']and meta['passed']and held['process'].poll()==meta['nativeExit']==0 and
         held['identity']==parent['actualNativeIdentity']==meta['nativeTerminal']['actualWindowsIdentity']and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (44780,38752,1791769484.6460857)and not meta['nativeTerminal']['hostDecodeErrors']and
         all(sha(p)==h for p,h in pins.items()),
         'Same exact original terminal44780 physical pressure game and every whole source/native input')
    for tag,chunks,headers in (('MK2_BBAUDIO_PCM_DIGEST',audio['pcmChunks'],audio['pcmHeaders']),
                               ('MK2_NATIVE_DAC_RAM_DIGEST',audio['dacChunks'],audio['dacHeaders'])):
        records=model.rows(text,tag)
        need(len(records)==len(chunks)==len(headers)==1646 and
             all(r==dict(h,sha256=hashlib.sha256(raw).hexdigest().upper())for r,h,raw in zip(records,headers,chunks,strict=True)),
             'Every entire actual PCM/DAC callback retained and independently digest-bound')
    need(audio['pcmHeaders'][0]['frame']=='1817'and audio['pcmHeaders'][0]['seconds']=='33.220000000000',
         'Actual opening partial sound callback preserved, no first/tail trimming')
    native_dac,dac_faults,dac_hash=dac_model.dac_models(1646)
    dac=native_dac(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders'])
    raw_faults=list(dac_faults(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders']))
    rom_gate,rom_faults=model.rom_models(audio['expectedROM'])
    rom=[rom_gate(bytes(audio['rom'][phase]),phase)for phase in ('startup','terminal')]
    for phase in ('startup','terminal'):raw_faults.extend(rom_faults(bytes(audio['rom'][phase]),phase))
    need(len(raw_faults)==12,'All original DAC and both whole sound-ROM corruption trials')
    video=model.rows(text,'MK2_MAUDIO_CHANNEL');precise=model.rows(text,'MK2_TOMB_MIX_CHANNEL')
    need([(int(r['frame']),int(r['channel']))for r in video]==[(f,c)for f in range(1818,3619)for c in range(19)]and
         [(r['frame'],r['seconds'],int(r['channel']))for r in precise]==
         [(h['frame'],h['seconds'],c)for h in audio['pcmHeaders']for c in range(19)],
         'All nineteen channels at every independent sound and all-mode video callback')
    for tag in ('MK2_MAUDIO_SOUND','MK2_MAUDIO_ROUTE','MK2_MAUDIO_PACKET','MK2_MAUDIO_DELIVERY',
                'MK2_MAUDIO_CHANNEL','MK2_TOMB_MIX_CHANNEL'):
        need(all(r['writes']=='0'and r['assistance']=='none'for r in model.rows(text,tag)),
             'Every actual source/port/DSP/channel observation passive')
    predict,mix_hash=winners.bindings()
    pcm=np.frombuffer(b''.join(audio['pcmChunks']),dtype='<i2').reshape(-1,2)
    waveform=predict(audio['dacChunks'],audio['dacHeaders'],pcm,text,'sonya',pins)
    OUT.mkdir();dac_model.save(OUT/'waveform.json',waveform)
    need(waveform['passed']and waveform['differentChannelSamples']==0 and
         waveform['comparedStereoFrames']==1580160 and waveform['actualSHA256']==waveform['predictedSHA256'],
         'Whole source-native float/cache/interpolation/two-winner waveform matches, with no fit')
    native_routing=routing_source(state['guest'])
    def gate(value,guest=state['guest']):
        return dict(cue=startup.startup_cue(value,guest),packets=packet_gate(value),
                    channels=channel_clocks(value,audio['pcmHeaders'],pins))
    positive=gate(text)
    need(positive['packets']['packets']==142 and positive['packets']['portWrites']==
         positive['packets']['nativeDSPReads']==284 and positive['packets']['trueWinnerMarkers']==2,
         'Every one of142 actual native packets and both Sonya winner markers accounted')
    special_native=[r for r in model.rows(text,'MK2_MAUDIO_SOUND')if r['word']=='FFF8']
    need(len(special_native)==1 and special_native[0]['frame']=='3599'and special_native[0]['pc']=='FFA13D60',
         'Actual continue-time FFF8 is native low-byte producer, not an imported effect cue')
    faults=[]
    def change(tag,key,value,**where):
        line=next(s for s in text.splitlines()if s.startswith(tag+' ')and
                  all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v)for k,v in where.items()))
        bad,count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(count==1 and bad!=line,'Effective actual source/clock/packet counterexample')
        return text.replace(line,bad,1)
    active=next(r for r in video if r['channel']=='0'and r['sample']=='3'and
                int(r['frame'])>3215 and float(r['pos'])>0)
    full=next(r for r in precise if r['channel']=='0'and r['sample']=='3'and
              int(r['frame'])>3215 and float(r['position'])>0)
    trials=[('late_startup_admission',change('MK2_MAUDIO_BEGIN','origin','1818')),
        ('startup_wrong_actor',change('MK2_FIRST_PROJECTILE_ENTRY','actor','01034E90',serial=1)),
        ('startup_wrong_voice',change('MK2_MAUDIO_ROUTE','a0','00000006',return_pc='FFFC48F0',frame=1817)),
        ('startup_wrong_main',change('MK2_MAUDIO_ROUTE','a13','0106A370',return_pc='FFFC48F0',frame=1817)),
        ('startup_wrong_identity',change('MK2_MAUDIO_ROUTE','id','17',return_pc='FFFC48F0',frame=1817)),
        ('startup_wrong_packet',change('MK2_MAUDIO_PACKET','a3','00000301',frame=1817)),
        ('startup_wrong_port',change('MK2_MAUDIO_SOUND','word','FF04',pc='FFA13C90',frame=1817)),
        ('startup_wrong_DSP',change('MK2_MAUDIO_DELIVERY','word','0004',dsp_pc='03A1',frame=1817)),
        ('private_finisher_leak',change('MK2_TOMB_MIX_CHANNEL','sample','5',frame=1817,channel=14)),
        ('wrong_second_winner_source',change('MK2_MAUDIO_CHANNEL','sample','2',frame=active['frame'],channel=0)),
        ('wrong_second_winner_length',change('MK2_MAUDIO_CHANNEL','length','31999',frame=active['frame'],channel=0)),
        ('second_winner_clock',change('MK2_MAUDIO_CHANNEL','pos',format(float(active['pos'])+1,'.8f'),frame=active['frame'],channel=0)),
        ('second_winner_position_bits',change('MK2_TOMB_MIX_CHANNEL','bits','0000000000000000',seconds=full['seconds'],channel=0)),
        ('unmodelled_other_channel',change('MK2_MAUDIO_CHANNEL','length','1',frame=active['frame'],channel=18)),
        ('channel_assistance',change('MK2_MAUDIO_CHANNEL','writes','1',frame=active['frame'],channel=0)),
        ('native_FFF8_wrong_producer',change('MK2_MAUDIO_SOUND','pc','FFFFB000',frame=3599,word='FFF8')),
        ('native_FFF8_DSP_byte',change('MK2_MAUDIO_DELIVERY','word','0000',frame=3599,dsp_pc='03A8'))]
    for label,bad in trials:
        try:gate(bad)
        except(ValueError,AssertionError,KeyError,IndexError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual pressure source-audio counterexample admitted '+label)
    bad=bytearray(state['guest']);bad[(0xfffc48f0-96-0xff800000)//8]^=1
    try:gate(text,bytes(bad))
    except(ValueError,AssertionError,KeyError)as error:faults.append(dict(fault='actual_startup_voice_opcode',rejectedBy=str(error)))
    else:raise ValueError('Actual Ring sound caller opcode corruption admitted')
    need(len(faults)==18 and gate(text)==positive,'Whole untouched source/cue/packet/clock positive restored after18 effective trials')
    for p in (Path(__file__),PARENT,Path(winners.__file__),Path(model.__file__),Path(startup.__file__),
              Path(startup.packets.__file__),Path(startup.packets.old.__file__),Path(dac_model.__file__),
              ROOT/'samples/mk2ks/kano_select.wav',ROOT/'mame-mkp/src/devices/sound/samples.cpp',
              ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp',OUT/'waveform.json'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'Never replace a prior source/evidence pin');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'All full source/evidence inputs fresh after whole waveform and faults')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        wholeMixedWaveform=waveform,wholeNativeDAC=dac,wholeSoundROM=rom,
        originalDACROMFaultsRejected=raw_faults,wholeActualStartupPacketClocks=positive,
        actualSourceClockPacketFaultsRejected=faults,nativePacketPrivateMarkerRouting=native_routing,
        entireSourceModelSHA256=mix_hash,nativeDACModelSHA256=dac_hash,inputHashes=pins,
        requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],
        finiteWholePressureSourceExactAudioAccepted=True,allHitGruntProducersIndividuallySourceBound=False,
        heardAudioQualityAccepted=False,allOwnerOverlapPriorityContextsAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    dac_model.save(OUT/'report.json',value)
    print('PASS same44780 complete1646 PCM-DAC callbacks, both Sonya winners,142 packets/all19 clocks',flush=True)
    return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        if not OUT.exists():OUT.mkdir()
        need(not(OUT/'failure.json').exists(),'Preserve actual whole pressure source-audio rejection')
        dac_model.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            goalStatus='active',newNativeGames=0,fullPortAcceptance=False))
        raise
