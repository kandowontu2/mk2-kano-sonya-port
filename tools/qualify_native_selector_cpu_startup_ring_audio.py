"""Whole original startup ring PCM/DAC/ROM, cue caller and DCS delivery.

This actual guard policy has no imported battle markers. Require every one
of nineteen channels to prove that absence; retain the complete original
native float/cache plus winner waveform, all packet and clock rules/faults.
"""
import hashlib,inspect,json,re,struct,traceback,wave
from pathlib import Path
import numpy as np
import capture_native_selector_cpu_projectile_pcm_startup_direct as capture
import current_tomb_winner_mix_fault_model_v5789 as model
import capture_current_subzero_audio_v6213 as dac_model
import verify_current_cpu_blade_knife_audio_v6370 as packets

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_startup_ring_audio_checked'

def packet_gate(text):
    source=inspect.getsource(packets.packet_gate)
    need(source.count('identity=17')==1, 'Whole unchanged original packet/port/ADSP chronology')
    source=source.replace('identity=17','identity=18',1)
    scope=dict(vars(packets),__file__=__file__)
    exec(compile(source,__file__+'::entire_original_packet_gate_true_Sonya','exec'),scope)
    return scope['packet_gate'](text)

def channel_gate(text,headers,waveform):
    source=inspect.getsource(packets.old.channel_gate)
    with wave.open(str(ROOT/'samples/mk2ks/sonya_select.wav'),'rb')as clip:
        need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==(1,2,16000,18400), 'Complete native selection source dimensions')
        values=np.frombuffer(clip.readframes(18400),'<i2').copy()
    _,positions=model.sample_values(values,16000)
    for before,after in (('14*len(pcm)','19*len(pcm)'),('range(14)','range(19)'),
        ('return 0xffffffff,32000,endpoint','return 0xffffffff,18400,selection_endpoint')):
        need(source.count(before)==1, 'Only current19 channels and completed source-derived selection differ')
        source=source.replace(before,after,1)
    scope=dict(packets.old.channel_gate.__globals__,selection_endpoint=positions[-1],__file__=__file__)
    exec(compile(source,__file__+'::entire_original_exact_channel_clock_gate','exec'),scope)
    records=packets.old.inventory(text)
    need([(r['frame'],int(r['channel']))for r in records['MK2_MAUDIO_CHANNEL']]==
         [(str(f),c)for f in range(1818,3619)for c in range(19)], 'Every actual video callback on all19 channels')
    return scope['channel_gate'](records,headers,dict(waveform=waveform),'sonya')

def startup_cue(text,guest):
    rows=model.rows
    begin=rows(text,'MK2_MAUDIO_BEGIN');first=rows(text,'MK2_FIRST_PROJECTILE_ENTRY')
    need(len(begin)==1 and begin[0]['frame']==begin[0]['origin']=='1817' and begin[0]['id']=='18', 'Sound armed at actual owned first-round ring, not next live callback')
    need(first and first[0]['frame']=='1817' and first[0]['kind']=='ring' and first[0]['id']=='18' and first[0]['opcode']=='574A' and first[0]['mask']=='FFFF', 'Actual source ring entry, no prescribed AI choice')
    actor,main='010350A0','0106BF30'
    need(first[0]['actor']==first[0]['owner']==begin[0]['a8']==actor and first[0]['main']==begin[0]['a13']==main, 'Real native actor/Main owns startup admission')
    live=rows(text,'MK2_P2CPU_COLD_LIVE');need(len(live)==1 and live[0]['frame']=='1818' and live[0]['human_id']=='17' and live[0]['cpu_id']=='18', 'Opening cue genuinely before original live callback in real17/18 match')
    route=[r for r in rows(text,'MK2_MAUDIO_ROUTE')if r['return_pc']=='FFFC48F0']
    need(len(route)==3 and route[0]['frame']=='1817' and all(r['entry']=='FFA12530' and r['a0']=='00000005' and r['a8']==r['owner']==actor and r['a13']==main and r['id']=='18'for r in route), 'All three actual ring release voice callers own their real18 actor/Main')
    at=(0xfffc48f0-0xff800000)//8
    need(guest[at-12:at]==struct.pack('<6H',0x09e0,5,0,0x0d5f,0x2530,0xffa1), 'Entire original native MOVI5/call sound-route instructions')
    events=rows(text,'MK2_MAUDIO_PACKET');first_packet=events[0]
    need(first_packet['frame']=='1817' and first_packet['a3']=='00000300' and first_packet['a8']==actor and first_packet['a13']==main, 'Actual initial packet binds executing ring owner, before live')
    sound=rows(text,'MK2_MAUDIO_SOUND');stores=sound[:2];reads=rows(text,'MK2_MAUDIO_DELIVERY')[:2]
    need([(r['word'],r['pc'],r['frame'])for r in stores]==[('FF03','FFA13C90','1817'),('FF00','FFA13D60','1817')] and
         [(r['word'],r['dsp_pc'],r['frame'])for r in reads]==[('0003','03A1','1817'),('0000','03A8','1817')], 'Both startup bytes actually reach original ADSP firmware')
    off=lambda address:(address-0xff800000)//8
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(guest[off(0xffa12530):off(0xffa13ed0)]==stock[off(0xffa12530):off(0xffa13ed0)], 'Complete stock effect/priority/packet/handshake source untouched')
    return dict(passed=True,actualRingVoiceCalls=3,initialFrame=1817,firstLiveFrame=1818,actor=actor,main=main,initialPacket='0300',startupDCSReadBytes=['03','00'])

def execute(state):
    need(not OUT.exists(), 'Fresh immutable qualification of original terminal game')
    folder,text,images=capture.RAM_CASES[capture.KEY];audio=capture.AUDIO[capture.KEY];held=capture.NATIVE_HANDLES[capture.KEY]
    path=capture.OUT/'report.json';receipt=json.loads(path.read_text());meta=json.loads((folder/'result.json').read_text())
    need(receipt['passed'] and meta['passed'] and held['process'].poll()==meta['nativeExit']==0 and held['identity']==receipt['actualNativeIdentity']==meta['nativeTerminal']['actualWindowsIdentity'] and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==(46264,38752,1791748793.1740513) and not meta['nativeTerminal']['hostDecodeErrors'], 'Exact original real guard-policy game terminal0')
    pins=dict(receipt['inputHashes']);need(all(sha(p)==h for p,h in pins.items()), 'Whole current capture/source/compiled input provenance unchanged')
    for tag,chunks,headers in (('MK2_BBAUDIO_PCM_DIGEST',audio['pcmChunks'],audio['pcmHeaders']),('MK2_NATIVE_DAC_RAM_DIGEST',audio['dacChunks'],audio['dacHeaders'])):
        records=model.rows(text,tag)
        need(len(chunks)==len(headers)==len(records)==1646, 'Entire actual startup-to-terminal sound callback inventory')
        need(all(r==dict(h,sha256=hashlib.sha256(raw).hexdigest().upper())for r,h,raw in zip(records,headers,chunks,strict=True)), 'Every whole original RAM block matches its original header/digest')
    need(audio['pcmHeaders'][0]['frame']=='1817' and audio['pcmHeaders'][0]['seconds']=='33.220000000000', 'Opening partial sound callback retained, not trimmed')
    native_gate,native_faults,dac_sha=dac_model.dac_models(1646)
    dac=native_gate(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders']);dac_faults=native_faults(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders'])
    rom_gate,rom_faults=model.rom_models(audio['expectedROM'])
    rom=[rom_gate(bytes(audio['rom'][p]),p)for p in ('startup','terminal')]
    rom_bad=[f for p in ('startup','terminal')for f in rom_faults(bytes(audio['rom'][p]),p)]
    pcm=np.frombuffer(b''.join(audio['pcmChunks']),'<i2').reshape(-1,2)
    waveform=model.predict_mix(audio['dacChunks'],audio['dacHeaders'],pcm,text,'sonya',pins)
    need(waveform['passed'] and waveform['differentChannelSamples']==0 and waveform['comparedStereoFrames']==1580160 and waveform['actualSHA256']==waveform['predictedSHA256'], 'Entire native unquantized resampler/cache plus actual winner mix, including first callback and all tail samples')
    def gate(value,guest=state['guest']):
        return dict(cue=startup_cue(value,guest),packets=packet_gate(value),channels=channel_gate(value,audio['pcmHeaders'],waveform))
    positive=gate(text);faults=[]
    def alter(tag,key,value,**where):
        line=next(s for s in text.splitlines()if s.startswith(tag+' ') and all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v)for k,v in where.items()))
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and changed!=line, 'Effective counterexample alters one real observed field')
        return text.replace(line,changed,1)
    for label,bad in (
        ('late_startup_admission',alter('MK2_MAUDIO_BEGIN','origin','1818')),
        ('startup_wrong_actor',alter('MK2_FIRST_PROJECTILE_ENTRY','actor','01034E90',serial=1)),
        ('startup_wrong_voice',alter('MK2_MAUDIO_ROUTE','a0','00000006',return_pc='FFFC48F0',frame=1817)),
        ('startup_wrong_main',alter('MK2_MAUDIO_ROUTE','a13','0106A370',return_pc='FFFC48F0',frame=1817)),
        ('startup_wrong_identity',alter('MK2_MAUDIO_ROUTE','id','17',return_pc='FFFC48F0',frame=1817)),
        ('startup_wrong_packet',alter('MK2_MAUDIO_PACKET','a3','00000301',frame=1817)),
        ('startup_wrong_port_byte',alter('MK2_MAUDIO_SOUND','word','FF04',pc='FFA13C90',frame=1817)),
        ('startup_wrong_DSP_byte',alter('MK2_MAUDIO_DELIVERY','word','0004',dsp_pc='03A1',frame=1817)),
        ('private_finisher_leak',alter('MK2_TOMB_MIX_CHANNEL','sample','5',frame=1817,channel=14))):
        try:gate(bad)
        except(AssertionError,ValueError,KeyError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual startup audio counterexample admitted '+label)
    bad=bytearray(state['guest']);bad[(0xfffc48f0-96-0xff800000)//8]^=1
    try:gate(text,bytes(bad))
    except(AssertionError,ValueError,KeyError)as error:faults.append(dict(fault='actual_startup_voice_opcode',rejectedBy=str(error)))
    else:raise ValueError('Actual startup caller corruption admitted')
    need(gate(text)==positive, 'Complete original source/packet/clock positive restored after faults')
    for p in (Path(__file__).resolve(),Path(model.__file__).resolve(),Path(dac_model.__file__).resolve(),Path(packets.__file__).resolve(),Path(packets.old.__file__).resolve(),path,ROOT/'samples/mk2ks/sonya_select.wav',ROOT/'audit_native_selector_cpu_projectile_pcm_startup_prelaunch_binding.json',*(p for p in folder.rglob('*')if p.is_file())):
        pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'Every executed/read whole input remains intact')
    OUT.mkdir();dac_model.save(OUT/'waveform.json',waveform)
    report=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],completePCMCallbacks=1646,completeStereoFrames=1580160,
        firstRoundRingCueBeforeLiveCallbackAccepted=True,wholeStartupAudio=positive,wholeMixedWaveform=waveform,nativeDAC=dac,nativeDACFaultsRejected=dac_faults,nativeDACModelSHA256=dac_sha,
        wholeSoundROM=rom,soundROMFaultsRejected=rom_bad,actualStartupSourceFaultsRejected=faults,originalNativeStateContract=receipt['originalNativeStateContract'],
        requirements=receipt['requirements'],remainingGroups=receipt['remainingGroups'],inputHashes=pins,fullNaturalOpponentStateHealthAcceptance=False,
        allStartupContextsAccepted=False,heardAudioQualityAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    dac_model.save(OUT/'report.json',report)
    print('PASS actual startup Ring voice/DCS/full1646 PCM-DAC/all19 exact clocks and source faults; wider goal active',flush=True)
    return report

def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(), 'Preserve actual qualifier failure')
        OUT.mkdir();dac_model.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),newNativeGames=0,fullPortAcceptance=False))
        raise
