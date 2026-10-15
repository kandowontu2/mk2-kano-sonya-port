"""Qualify an intact native precombat interval in an otherwise failed recorder.

The original full-cold report stays false. No replacement clock, synthesized
DAC chunk, game write, native replay or boot-waveform acceptance is permitted.
"""
import hashlib, inspect, json, re, wave
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from pathlib import Path
import numpy as np
import qualify_launch_challenger_transition as original
import qualify_launch_challenger_transition_remaining_v2 as health
import qualify_launch_challenger_transition_v2 as packets

ROOT, need, sha = original.ROOT, original.need, original.sha
rows, clock = original.rows, original.clock


def interval(c):
    need(c['terminal']['nativeExit'] == 0 and not c['decodeErrors'], 'Actual same normal native terminal and lossless transport')
    need(not c['report']['passed'], 'Original full-cold recorder rejection remains false')
    fields = rows(c['text'], 'MK2_KO_FIELD')
    by = {(int(r['frame']), int(r['slot'])): r for r in fields}
    first = next(f for f in sorted({f for f, s in by}) if all(
        by[f, s]['mode'] == '7' and by[f, s]['hp'] == '161' and
        by[f, s]['id'] == by[f, s]['roster'] == str({1: 18, 2: 17}[s]) and
        by[f, s]['actor'] == by[f, s]['owner'] != '00000000' for s in (1, 2)))
    begin = by[first, 1]
    missing = [h for h in c['pcmHeaders'] if h['seconds'] not in {d['seconds'] for d in c['dacHeaders']}]
    need(len(missing) == 1 and missing[0]['frame'] == '301' and missing[0]['seconds'] == '5.520000000000', 'Only actual early boot DAC reset callback is missing')
    need(first == 1477 and Decimal(begin['seconds']) > Decimal(missing[0]['seconds']), 'First original full-health published precombat, not PCM-selected cutoff')
    retained = []
    for line in c['text'].splitlines():
        match = re.search(r'\bframe=(\d+)', line)
        if match and int(match[1]) >= first and not line.startswith('MK2_MAUDIO_BEGIN'):
            retained.append(line)
    # This is explicitly derived admission metadata; the captured log stays intact.
    retained.insert(0, f"MK2_MAUDIO_BEGIN frame={first} seconds={begin['seconds']} writes=0 assistance=none origin={first} scope=derived_native_full_health_precombat")
    scoped = dict(c, text='\n'.join(retained) + '\n')
    for chunks, headers in (('pcm', 'pcmHeaders'), ('dac', 'dacHeaders')):
        indices = [i for i, h in enumerate(c[headers]) if Decimal(h['seconds']) >= Decimal(begin['seconds'])]
        scoped[chunks] = [c[chunks][i] for i in indices]
        scoped[headers] = [c[headers][i] for i in indices]
    need(scoped['pcmHeaders'][0]['seconds'] == scoped['dacHeaders'][0]['seconds'] == '27.000000000000', 'Actual first sound callback after native admission')
    need(all(r['actor'] == r['main'] == '00000000' and r['health'] == r['id'] == '0'
             for r in rows(scoped['text'], 'MK2_INTERRUPT_OWNER') if int(r['frame']) == first), 'No imported-source carry-in at native precombat admission')
    return scoped, dict(firstNativeFrame=first, actualNativeAdmission=begin,
        derivedMetadataNotCapturedAdmission=True, bootRejectedCallback=missing,
        wholeColdBootAudioAccepted=False, originalReportSHA256=sha(c['folder'] / 'report.json'))


def source_events(c, pins, by):
    markers = [r for r in rows(c['text'], 'MK2_MAUDIO_SOUND') if r['word'] in ('6B01', '6B02', '6B03')]
    need([r['word'] for r in markers] == ['6B01', '6B02', '6B03'], 'Both actual CPU Bicycle cues and human Kano launch retained')
    events = []
    for marker, name, sid, slot, channel, pc, length in zip(markers,
        ('sonya_bicycle_launch', 'sonya_bicycle_cry', 'kano_ball_launch'),
        (14, 15, 16), (1, 1, 2), (10, 11, 12),
        ('FFF9A4C0', 'FFF9A520', 'FFFFDEC0'), (40720, 66523, 55465), strict=True):
        field = by[int(marker['frame']), slot]
        need(marker['mask'] == 'FFFF' and marker['pc'] == pc and marker['a8'] == field['actor'] == field['owner'] and
             marker['a13'] == field['main'] and field['id'] == field['roster'] == str(18 if slot == 1 else 17), 'Each actual source marker binds native CPU/human actor, Main and real identity')
        path = ROOT / (original.prior.mirror.old.current.NAME + '/samples/mk2ks' if sid == 16 else 'samples/mk2ks') / (name + '.wav')
        pins[str(path)] = sha(path)
        with wave.open(str(path), 'rb') as clip:
            need((clip.getnchannels(), clip.getsampwidth(), clip.getframerate(), clip.getnframes()) == (1, 2, 48000, length), 'Entire original native battle sample')
            sample, positions = clock.sample_values(np.frombuffer(clip.readframes(length), '<i2'), 48000)
        events.append(dict(marker=marker, slot=slot, channel=channel, sample_id=sid,
            start=clock.sample_clock(marker['seconds'], True), sample=sample, positions=positions,
            length=length, generatedBeforeStop=len(sample), gain=np.float32(.70)))
    # Human noncombat retirement uses the unchanged complete original timer model.
    own = dict(c, text='\n'.join(line for line in c['text'].splitlines() if not
        (line.startswith('MK2_MAUDIO_SOUND') and ('word=6B01 ' in line or 'word=6B02 ' in line))) + '\n')
    e = original.source_events(own, pins)[0]
    events[2].update({k: v for k, v in e.items() if k not in ('sample', 'positions')})
    origin = int(Decimal(markers[0]['seconds']) * clock.ATTO)
    period = clock.ATTO // 60
    n = 1
    while any(clock.sample_clock(str(Decimal(origin + n * period) / clock.ATTO), True) - e['start'] < len(e['sample']) for e in events[:2]):
        n += 1
    stop = origin + n * period
    for e in events[:2]:
        e.update(stopAttoseconds=stop, sharedTimerOrigin=origin, incoming=None)
    return events


def owners(c, events, by):
    first = int(original.prior.one(c['text'], 'MK2_MAUDIO_BEGIN')['frame'])
    last = int(original.prior.one(c['text'], 'MK2_JR_RESULT')['frame'])
    owned, channels = rows(c['text'], 'MK2_INTERRUPT_OWNER'), rows(c['text'], 'MK2_INTERRUPT_CHANNEL')
    need(len(owned) == 2 * (last-first+1) and len({(r['frame'], r['slot']) for r in owned}) == len(owned), 'Every continuous both-slot owner field')
    need(len(channels) == 4 * (last-first+1) and len({(r['frame'], r['channel']) for r in channels}) == len(channels), 'Every continuous battle-channel field')
    for r in owned:
        t = int(Decimal(r['seconds']) * clock.ATTO)
        active = [e for e in events if e['channel'] in (10, 12) and e['slot'] == int(r['slot']) and int(Decimal(e['marker']['seconds']) * clock.ATTO) < t < e['stopAttoseconds']]
        need(len(active) <= 1 and r['writes'] == '0' and r['assistance'] == 'none', 'Source-owned finite read-only lifetime')
        if active:
            e = active[0]; p = by[int(e['marker']['frame']), e['slot']]
            need(r['actor'] == p['actor'] and r['main'] == p['main'] and r['id'] == p['id'] and r['health'] == p['hp'], 'CPU and human owners remain exact until original guard retirement')
        else:
            need(r['actor'] == r['main'] == '00000000' and r['id'] == r['health'] == '0', 'All-slot owner retirement, including CPU Bicycle EOF')
    for r in channels:
        need(r['loop'] == r['paused'] == r['writes'] == '0' and r['assistance'] == 'none', 'Every source finite, unpaused and read-only')
        for e in events:
            if int(r['channel']) != e['channel']: continue
            t = int(Decimal(r['seconds']) * clock.ATTO)
            if t <= int(Decimal(e['marker']['seconds']) * clock.ATTO):
                need(r['length'] == '0' and float(r['position']) == 0 and r['sample'] == '4294967295', 'No unobserved source carry-in')
            elif t > e['stopAttoseconds']:
                need(int(r['length']) == e['length'] and float(r['position']) == e['positions'][e['generatedBeforeStop']-1] and r['sample'] == '4294967295', 'Entire EOF/interrupted channel position frozen at native source cutoff')
        if r['channel'] == '13':
            need(r['length'] == '0' and float(r['position']) == 0 and r['sample'] == '4294967295', 'Unused fourth battle channel stays idle')
    return dict(passed=True, continuousOwnerFields=len(owned), continuousChannelFields=len(channels), actualCPUEOFAccepted=True)


def predict(c, events, pins):
    headers = c['pcmHeaders']; text = c['text']
    begin, end = (original.prior.one(text, 'MK2_MAUDIO_' + tag) for tag in ('BEGIN', 'RESULT'))
    first = int((Decimal(begin['seconds']) * 50).to_integral_value(rounding=ROUND_CEILING))
    last = int((Decimal(end['seconds']) * 50).to_integral_value(rounding=ROUND_FLOOR))
    need([Decimal(h['seconds']) for h in headers] == [Decimal(n)/50 for n in range(first, last+1)] and
         headers == rows(text, 'MK2_BBAUDIO_PCM_DIGEST') and c['dacHeaders'] == rows(text, 'MK2_NATIVE_DAC_RAM_DIGEST'), 'Every scheduled actual callback from native precombat through original terminal')
    pcm = np.frombuffer(b''.join(c['pcm']), '<i2').reshape(-1, 2)
    dcs, clocks = clock.float_model()(c['dac'], c['dacHeaders'])
    need(dcs.shape == pcm.shape, 'Whole original native DAC/cache/float-resampler output')
    speech = [r for r in rows(text, 'MK2_MAUDIO_SOUND') if r['pc'] in ('FFFF3DA0', 'FFFB7140')]
    need([r['word'] for r in speech] == ['FFFD', 'FFFC', 'FFFB'], 'Actual CPU Sonya winner and both new selection announcements')
    names = []
    for i, m in enumerate(speech):
        stem = {'FFFD': 'sonya_wins', 'FFFC': 'kano_select', 'FFFB': 'sonya_select'}[m['word']]
        path = ROOT / 'samples/mk2ks' / (stem + '.wav'); pins[str(path)] = sha(path)
        with wave.open(str(path), 'rb') as clip:
            length = 32000 if m['word'] == 'FFFD' else 18400
            need((clip.getnchannels(), clip.getsampwidth(), clip.getframerate(), clip.getnframes()) == (1, 2, 16000, length), 'Complete original native announcer clip')
            sample, positions = clock.sample_values(np.frombuffer(clip.readframes(length), '<i2'), 16000)
        start = clock.sample_clock(m['seconds'], True)
        limit = len(sample) if i+1 == len(speech) else min(len(sample), clock.sample_clock(speech[i+1]['seconds'], True)-start)
        names.append(dict(marker=m, channel=0, start=start, sample=sample, positions=positions, generatedBeforeStop=limit, gain=np.float32(np.float32(.70)*np.float32(.30))))
    voices = {i: np.zeros_like(dcs) for i in (0, 10, 11, 12)}
    for e in events + names:
        for i, h in enumerate(headers):
            tick = int(Decimal(h['seconds'])*50); at0 = (tick-1)*960*(clock.ATTO//48000); s, f = divmod(at0, clock.ATTO)
            at = np.arange(s*48000+f//clock.PERIOD, s*48000+f//clock.PERIOD+960, dtype=np.int64)-e['start']
            valid = (at >= 0) & (at < e['generatedBeforeStop']); segment = np.zeros(960, dtype='<f4')
            segment[valid] = np.float32(e['sample'][at[valid]]*e['gain'])
            voices[e['channel']][i*960:(i+1)*960] += segment[:, None]
    mix = lambda v: np.float32(np.float32(np.float32(v[0]+v[10])+v[11])+v[12])
    convert = lambda v: (np.clip(v, -1, 1).astype(np.float64)*32767.0).astype('<i2')
    predicted = convert(np.float32(dcs+mix(voices)))
    differences = np.argwhere(predicted != pcm)
    proof = dict(passed=not len(differences), comparedStereoFrames=len(pcm), differentChannelSamples=len(differences), firstDifferences=differences[:12].tolist(), actualSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper(), predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(), completeNativeClocks=clocks)
    need(proof['passed'], 'Whole scoped native CPU/Bicycle/human/Kano/announcer/DCS waveform source-exact: ' + str(proof))
    rejected = []
    for channel in voices:
        v = dict(voices); v[channel] = np.zeros_like(dcs)
        need(not np.array_equal(convert(np.float32(dcs+mix(v))), pcm), 'Nonvacuous omission of actual channel ' + str(channel)); rejected.append('channel' + str(channel) + ' omitted')
    for label, i in (('first PCM bit', 0), ('last PCM bit', len(pcm)-1)):
        bad = pcm.copy(); bad[i, 0] ^= 1; need(not np.array_equal(predicted, bad), 'Actual boundary PCM bit rejected'); rejected.append(label)
    proof['actualFaultsRejected'] = rejected
    return proof, names


def qualify(c):
    out = ROOT / 'audit_challenger_retained_precombat_checked'
    need(not out.exists(), 'Fresh immutable same-terminal evidence')
    pins = dict(c['pins']); need(all(sha(p) == h for p, h in pins.items()), 'All actual executed inputs remain intact')
    scoped, admission = interval(c)
    state, by = health.physical_inventory(scoped)
    game = original.gameplay_gate(c['text'], 'kano', 2)
    events = source_events(scoped, pins, by); owned = owners(scoped, events, by)
    waveform, names = predict(scoped, events, pins)
    gate, fault = original.prior.mirror.qualifier.source_audio.dac_models(len(scoped['pcmHeaders']))
    dac = dict(positive=gate(scoped['dac'], scoped['dacHeaders'], scoped['pcmHeaders']), faults=fault(scoped['dac'], scoped['dacHeaders'], scoped['pcmHeaders']))
    rg, rf = original.prior.mirror.qualifier.source_audio.host.models.rom_models(c['expectedROM'])
    rom = dict(positive=[rg(bytes(c['rom'][p]), p) for p in c['rom']], faults=[f for p in c['rom'] for f in rf(bytes(c['rom'][p]), p)])
    # Keep complete original packet/port/ADSP grammar; only inventory sizes vary.
    src = inspect.getsource(packets.packet_gate)
    src = src.replace("not markers and len(selection)==2", "len(markers)==1 and markers[0]['word']=='FFFD' and len(selection)==2")
    src = src.replace('len(launches)==1', 'len(launches)==3').replace('len(sounds)+len(selection)+len(launches)', 'len(sounds)+len(selection)+len(launches)+len(markers)')
    scope = dict(vars(packets)); exec(compile(src, str(Path(__file__))+'::whole_original_packet_delivery', 'exec'), scope)
    delivery = scope['packet_gate'](scoped['text'])
    for p in (Path(__file__), Path(original.__file__), Path(health.__file__), Path(packets.__file__), ROOT/'mame-mkp/src/devices/sound/samples.cpp', *c['folder'].rglob('*')):
        if p.is_file(): pins[str(p.resolve())] = sha(p)
    need(all(sha(p) == h for p, h in pins.items()), 'Whole actual sources and original rejection are unchanged')
    public = lambda e: {k: v for k, v in e.items() if k not in ('sample', 'positions', 'gain')}
    report = dict(passed=True, nativeTerminal=c['terminal'], admission=admission, completePhysicalAndHealthInventory=state, wholeOriginalJoinedGameplay=game, completeIndependentOwnership=owned, completeSourceWaveform=waveform, sourceDAC=dac, wholeSoundROM=rom, completeNativeDCSDelivery=delivery, sourceEvents=[public(e) for e in events], announcerEvents=[public(e) for e in names], inputHashes=pins, originalColdRecorderStillRejected=True, bootAudioAccepted=False, fullPortAcceptance=False, goalStatus='active', newNativeBoots=0, newBuilds=0, newRawMedia=0)
    out.mkdir(); (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(passed=True, report=str(out/'report.json'), fields=state['continuousPhysicalFields'], stereoFrames=waveform['comparedStereoFrames'])), flush=True)
    return report
