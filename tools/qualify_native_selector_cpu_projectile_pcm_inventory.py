"""Same current Kano/Sonya game: full native DAC/PCM/ROM/source inventory.

Keep original whole DAC and ROM fault models, not a winner-only waveform
substitute. Actual Square/bicycle launch/cry must be included in the next
full mixer proof. First-load source_num=-1 does NOT mean an empty pointer.
"""
import hashlib,json,struct,wave
from pathlib import Path
import capture_native_selector_cpu_projectile_pcm_natural as capture
import capture_current_subzero_audio_v6213 as dac_model

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_selector_cpu_projectile_pcm_inventory_checked'


def execute(state):
    need(not OUT.exists()and not capture.prior.current.prior.identity.census(),'Same original terminal game; no native replay')
    folder,text,images=capture.RAM_CASES[capture.KEY];audio=capture.AUDIO[capture.KEY]
    held=capture.NATIVE_HANDLES[capture.KEY];meta=json.loads((folder/'result.json').read_text())
    receipt_path=capture.OUT/'report.json';receipt=json.loads(receipt_path.read_text())
    need(receipt['passed']and meta['passed']and meta['nativeExit']==held['process'].poll()==0 and
         held['identity']==meta['nativeTerminal']['actualWindowsIdentity']==receipt['actualNativeIdentity']and
         (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix'])==
         (47172,38752,1791745912.9231853)and not meta['nativeTerminal']['hostDecodeErrors']and
         all(sha(p)==h for p,h in receipt['inputHashes'].items()),'Exact original natural CPU native terminal0 and whole current inputs')
    rows=capture.prior.audio_model.rows
    pcm_records=rows(text,'MK2_BBAUDIO_PCM_DIGEST');dac_records=rows(text,'MK2_NATIVE_DAC_RAM_DIGEST')
    for label,chunks,headers,records in(('PCM',audio['pcmChunks'],audio['pcmHeaders'],pcm_records),
                                      ('DAC',audio['dacChunks'],audio['dacHeaders'],dac_records)):
        need(len(chunks)==len(headers)==len(records)==1645,'Every actual full-match '+label+' callback')
        for raw,head,record in zip(chunks,headers,records,strict=True):
            need(record==dict(head,sha256=hashlib.sha256(raw).hexdigest().upper()),
                 'Every whole retained '+label+' block reproduces original callback digest/header')
    gate,fault,source_hash=dac_model.dac_models(1645)
    dac=gate(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders'])
    dac_faults=fault(audio['dacChunks'],audio['dacHeaders'],audio['pcmHeaders'])
    region_gate,region_fault=capture.prior.audio_model.rom_models(audio['expectedROM'])
    rom=[region_gate(bytes(audio['rom'][phase]),phase)for phase in('startup','terminal')]
    rom_faults=[f for phase in('startup','terminal')for f in region_fault(bytes(audio['rom'][phase]),phase)]
    channels=rows(text,'MK2_MAUDIO_CHANNEL');precise=rows(text,'MK2_TOMB_MIX_CHANNEL')
    heads=audio['pcmHeaders'];begin=rows(text,'MK2_MAUDIO_BEGIN');end=rows(text,'MK2_MAUDIO_RESULT')
    need(len(begin)==len(end)==1 and begin[0]['frame']==begin[0]['origin']=='1818'and
         begin[0]['id']=='18'and end[0]['origin']=='1818'and end[0]['frame']=='3618'and
         begin[0]['a8']=='010350A0'and begin[0]['a13']=='0106BF30',
         'Actual Sonya CPU sound origin inside human Kano17/Sonya18 full native match')
    need([(int(r['frame']),int(r['channel']))for r in channels]==
         [(f,c)for f in range(1818,3619)for c in range(19)],'All19 sample channels at every actual video callback')
    need(len(precise)==1645*19 and [(r['frame'],r['seconds'],int(r['channel']))for r in precise]==
         [(h['frame'],h['seconds'],c)for h in heads for c in range(19)],'All19 exact source positions on every sound callback')
    for r in channels+precise:
        need(r['loop']==r['paused']==r['writes']=='0'and r['assistance']=='none','Every channel is passive/nonlooping/unpaused')
        if int(r['channel'])>=14:
            need(r['sample']=='4294967295'and r['length']=='0'and float(r.get('position',r.get('pos')))==0,
                 'All five private finisher channels remain entirely inactive')
        if 'bits'in r:
            need(struct.pack('<d',float(r['position'])).hex().upper()==r['bits'],'Every exact native source-position bit retained')
    markers=[r for r in rows(text,'MK2_MAUDIO_SOUND')if 0x6b00<=int(r['word'],16)<=0x6b03]
    need([(r['word'],r['frame'],r['pc'])for r in markers]==
         [('6B00','1966','FFFFCAC0'),('6B01','2766','FFF9A4C0'),('6B02','2766','FFF9A520')]and
         all(r['a8']=='010350A0'and r['a13']=='0106BF30'and r['mask']=='FFFF'for r in markers),
         'Actual source-owned Sonya Square/bicycle launch/cry markers; no inferred choices or forced launch')
    pins=dict(receipt['inputHashes']);assets=[]
    for name,frequency,length,channel,sample in(
        ('sonya_square_launch.wav',48000,45512,12,13),('sonya_bicycle_launch.wav',48000,40720,12,14),
        ('sonya_bicycle_cry.wav',48000,66523,13,15),('sonya_wins.wav',16000,32000,0,3)):
        path=ROOT/'samples/mk2ks'/name;need(str(path)in pins and sha(path)==pins[str(path)],'Complete original source clip pinned by actual current build/capture')
        with wave.open(str(path),'rb')as clip:
            need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==
                 (1,2,frequency,length),'Whole original source clip dimensions')
        need(any(int(r['channel'])==channel and int(r['length'])==length for r in precise),'Actual native loaded source pointer/length even when source_num is -1')
        assets.append(dict(name=name,frequency=frequency,sourceFrames=length,channel=channel,sampleIndex=sample,sha256=sha(path)))
    compiled=ROOT/'diagnostic_native_selector_layers_long/input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    source=compiled.read_text()
    need('set_channels(19)'in source and '"sonya_square_launch", "sonya_bicycle_launch", "sonya_bicycle_cry", "kano_ball_launch"'in source,
         'Actual compiled19-channel source declarations, not older dirty checkout')
    for path in(Path(__file__),Path(dac_model.__file__),receipt_path,compiled,
                ROOT/'diagnostic_native_selector_layers_long/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp',
                ROOT/'mame-mkp/src/devices/sound/samples.cpp',*(p for p in folder.rglob('*')if p.is_file())):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Entire executed/read inventory remains unchanged')
    report=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],completePCMCallbacks=1645,
        completeStereoFrames=1645*960,wholePCMSHA256=hashlib.sha256(b''.join(audio['pcmChunks'])).hexdigest().upper(),
        nativeDAC=dac,nativeDACFaultsRejected=dac_faults,nativeDACModelSHA256=source_hash,
        wholeOriginalSoundROM=rom,originalSoundROMFaultsRejected=rom_faults,
        complete19ChannelVideoRows=len(channels),complete19ChannelSoundRows=len(precise),actualBattleMarkers=markers,
        actualLoadedSources=assets,originalMirrorStateContract=receipt['originalNativeStateContract'],
        fullNaturalOpponentStateHealthAcceptance=False,allMixedPCMSourceSamplesAccepted=False,heardAudioQualityAccepted=False,
        firstLoadMinusOneSourceIsNotAssumedSilent=True,requirements=receipt['requirements'],remainingGroups=receipt['remainingGroups'],
        nextAction='Full current source-clock/gain/stop mixture: Square launch, both simultaneous bicycle launch/cry channels, Sonya winner and native DCS; then other contexts and remaining original goal groups',
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,inputHashes=pins)
    OUT.mkdir();capture.prior.current.prior.save(OUT/'report.json',report)
    print('PASS same current Kano/Sonya1645 PCM/DAC callbacks/all19 channels/source inventory; whole mixed waveform still open',flush=True)
    return report
