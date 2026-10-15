"""Source-clock CPU Square/Bicycle, winners, selection and complete native mix.

No PCM-derived stop/onset/gain, trimmed callback or synthesized DAC chunk.
The original timer, resampler and repeated-double sample implementation apply.
"""
import hashlib
import inspect
import wave
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from pathlib import Path
import numpy as np
import launch_stage_advance_contract_v2 as stage
import current_tomb_winner_mix_fault_model_v5789 as clock
import qualify_launch_challenger_transition_v2 as packet_source

ROOT, need, sha = stage.ROOT, stage.need, stage.sha


def values(name, rate, length, pins):
    path = ROOT/'samples/mk2ks'/(name+'.wav')
    pins[str(path)] = sha(path)
    with wave.open(str(path), 'rb') as clip:
        need((clip.getnchannels(), clip.getsampwidth(), clip.getframerate(), clip.getnframes(), clip.getcomptype()) ==
             (1, 2, rate, length, 'NONE'), 'Entire actual original sample '+name)
        sample, positions = clock.sample_values(np.frombuffer(clip.readframes(length), '<i2'), rate)
    return sample, positions


def source_events(c, by, pins):
    rows = stage.inventory(c['text'])
    get = lambda tag: rows.get(tag, [])
    markers = [r for r in get('MK2_MAUDIO_SOUND') if r['word'] in ('6B00', '6B01', '6B02', '6B03')]
    need([r['word'] for r in markers] == ['6B00', '6B00', '6B01', '6B02'], 'Every actual CPU cue; no invented human roll or omitted auxiliary cry')
    health = get('MK2_INTERRUPT_HEALTH')
    events = []
    period = clock.ATTO//60
    for marker, name, sid, channel, pc, length in zip(markers,
         ('sonya_square_launch', 'sonya_square_launch', 'sonya_bicycle_launch', 'sonya_bicycle_cry'),
         (13, 13, 14, 15), (10, 10, 10, 11), ('FFFFCAC0', 'FFFFCAC0', 'FFF9A4C0', 'FFF9A520'),
         (45512, 45512, 40720, 66523), strict=True):
        frame = int(marker['frame']); physical = by[frame, 1]
        need(marker['pc'] == pc and marker['mask'] == 'FFFF' and
             marker['a8'] == physical['actor'] == physical['owner'] and marker['a13'] == physical['main'] and
             physical['state'] == '0' and physical['id'] == physical['roster'] == '18', 'Actual original CPU actor/Main/ID and marker-PC ownership')
        sample, positions = values(name, 48000, length, pins)
        start = clock.sample_clock(marker['seconds'], True)
        main = markers[2] if sid == 15 else marker
        timer = int(Decimal(main['seconds'])*clock.ATTO)
        # Each main start is separated from the previous independent EOF/stop.
        incoming = [r for r in health if r['slot'] == '1' and r['pc'] == 'FF836700' and
                    Decimal(r['seconds']) > Decimal(main['seconds']) and
                    Decimal(r['seconds']) < Decimal(main['seconds']) + Decimal('1.5') and
                    int(r['before']) > int(r['after'])]
        if sid in (14, 15):
            need(len(incoming) == 1 and incoming[0]['before'] == physical['hp'], 'One real CPU incoming collision interrupts Bicycle/cry')
            damage = int(Decimal(incoming[0]['seconds'])*clock.ATTO)
            n = (damage-timer+period-1)//period
            stop = timer+n*period
            updates = [int(Decimal(h['seconds'])*clock.ATTO) for h in c['pcmHeaders'] if int(Decimal(h['seconds'])*clock.ATTO) < stop]
            update = max(max(updates), stop-period)
            generated = clock.sample_clock(str(Decimal(update)/clock.ATTO), True)-start
            need(0 < generated < len(sample), 'Original timer/previous-playing-update interrupted source prefix')
            reason = 'health_changed'; hit = incoming[0]
        else:
            need(not incoming, 'Both genuine Square clips reach original unhit EOF')
            n = 1
            while clock.sample_clock(str(Decimal(timer+n*period)/clock.ATTO), True)-start < len(sample): n += 1
            stop = timer+n*period
            generated = len(sample); update = None; reason = 'finished'; hit = None
        events.append(dict(marker=marker, slot=1, channel=channel, sample_id=sid, length=length,
                           start=start, sample=sample, positions=positions, generatedBeforeStop=generated,
                           sharedTimerOrigin=timer, stopAttoseconds=stop, lastStreamUpdateAttoseconds=update,
                           stopReason=reason, incoming=hit, gain=np.float32(.70)))
    need(events[0]['stopAttoseconds'] < events[1]['sharedTimerOrigin'] and
         events[1]['stopAttoseconds'] < events[2]['sharedTimerOrigin'] and
         events[2]['stopAttoseconds'] == events[3]['stopAttoseconds'], 'Source timer disables between independent launches; Bicycle auxiliary shares its owner timer')
    owners = get('MK2_INTERRUPT_OWNER')
    for row in owners:
        time = int(Decimal(row['seconds'])*clock.ATTO)
        active = [e for e in events if e['channel'] == 10 and
                  int(Decimal(e['marker']['seconds'])*clock.ATTO) < time < e['stopAttoseconds']]
        need(len(active) <= 1 and row['writes'] == '0' and row['assistance'] == 'none', 'Every passive finite source ownership snapshot')
        if row['slot'] == '1' and active:
            event = active[0]; field = by[int(event['marker']['frame']), 1]
            need(row['actor'] == event['marker']['a8'] and row['main'] == event['marker']['a13'] and
                 row['id'] == '18' and row['health'] == field['hp'], 'Exact CPU actor/Main/health/ID until independently computed guard tick')
        else:
            need(row['actor'] == row['main'] == '00000000' and row['id'] == row['health'] == '0', 'Both-slot retirement throughout KO/reset/paid selection/next arena/next opponent')
    last = int(get('MK2_NAT_CAMPAIGN_STAGE_RESULT')[0]['frame'])
    first = int(get('MK2_MAUDIO_BEGIN')[0]['frame'])
    need(len(owners) == 2*(last-first+1) and len({(r['frame'], r['slot']) for r in owners}) == len(owners), 'Every ownership field through the actual terminal')
    return events, rows


def predict(c, by, pins):
    events, records = source_events(c, by, pins)
    get = lambda tag: records.get(tag, [])
    headers = c['pcmHeaders']; begin, end = get('MK2_MAUDIO_BEGIN')[0], get('MK2_MAUDIO_RESULT')[0]
    first = int((Decimal(begin['seconds'])*50).to_integral_value(rounding=ROUND_CEILING))
    last = int((Decimal(end['seconds'])*50).to_integral_value(rounding=ROUND_FLOOR))
    need([Decimal(h['seconds']) for h in headers] == [Decimal(n)/50 for n in range(first, last+1)] and
         headers == get('MK2_BBAUDIO_PCM_DIGEST') and c['dacHeaders'] == get('MK2_NATIVE_DAC_RAM_DIGEST'), 'Every initial/interior/cache/final native 50Hz callback')
    announcements = [r for r in get('MK2_MAUDIO_SOUND') if r['pc'] in ('FFFF3DA0', 'FFFB7140')]
    need([r['word'] for r in announcements] == ['FFFD', 'FFFD', 'FFFC', 'FFFE', 'FFFE'], 'Actual two CPU winners, paid Kano selection and two own winners')
    names = []
    for i, marker in enumerate(announcements):
        name, sid, length = {'FFFD': ('sonya_wins', 3, 32000), 'FFFE': ('kano_wins', 2, 32000), 'FFFC': ('kano_select', 0, 18400)}[marker['word']]
        need(marker['mask'] == 'FFFF', 'Whole original announcer port word')
        sample, positions = values(name, 16000, length, pins)
        start = clock.sample_clock(marker['seconds'], True)
        limit = len(sample) if i+1 == len(announcements) else min(len(sample), clock.sample_clock(announcements[i+1]['seconds'], True)-start)
        need(limit == len(sample), 'All actual announcers keep complete source tails, no fitted truncation')
        names.append(dict(marker=marker, channel=0, sample_id=sid, length=length, start=start, sample=sample,
                          positions=positions, generatedBeforeStop=limit, gain=np.float32(np.float32(.70)*np.float32(.30))))
    pcm = np.frombuffer(b''.join(c['pcm']), '<i2').reshape(-1, 2)
    dcs, clocks = clock.float_model()(c['dac'], c['dacHeaders'])
    need(dcs.shape == pcm.shape and len(headers)*960 == len(pcm), 'Complete original native float DAC/cache/resampler')
    voices = {channel: np.zeros_like(dcs) for channel in (0, 10, 11)}
    for event in events+names:
        for i, header in enumerate(headers):
            tick = int(Decimal(header['seconds'])*50)
            at0 = (tick-1)*960*(clock.ATTO//48000); sec, fraction = divmod(at0, clock.ATTO)
            at = np.arange(sec*48000+fraction//clock.PERIOD, sec*48000+fraction//clock.PERIOD+960, dtype=np.int64)-event['start']
            valid = (at >= 0) & (at < event['generatedBeforeStop'])
            segment = np.zeros(960, dtype='<f4')
            segment[valid] = np.float32(event['sample'][at[valid]]*event['gain'])
            voices[event['channel']][i*960:(i+1)*960] += segment[:, None]
    mix = lambda voice: np.float32(np.float32(voice[0]+voice[10])+voice[11])
    convert = lambda value: (np.clip(value, -1, 1).astype(np.float64)*32767.0).astype('<i2')
    predicted = convert(np.float32(dcs+mix(voices)))
    different = np.argwhere(predicted != pcm)
    need(not len(different), 'Complete native CPU/announcer/stage-advance waveform source equality: '+str(different[:12].tolist()))
    faults = []
    for channel in voices:
        changed = dict(voices); changed[channel] = np.zeros_like(dcs)
        need(not np.array_equal(convert(np.float32(dcs+mix(changed))), pcm), 'Actual audible source omission '+str(channel))
        faults.append('channel'+str(channel)+' omitted')
    for label, index in [('first PCM bit', 0), ('last PCM bit', len(pcm)-1)]:
        changed = pcm.copy(); changed[index, 0] ^= 1
        need(not np.array_equal(predicted, changed), 'Actual complete waveform boundary bit fault')
        faults.append(label)
    need(predicted.shape != pcm[1:].shape and predicted.shape != pcm[:-1].shape, 'Whole window rejects first/last stereo frame omission')
    faults.extend(['first PCM frame omitted', 'last PCM frame omitted'])
    return dict(passed=True, comparedStereoFrames=len(pcm), differentChannelSamples=0,
                actualSHA256=hashlib.sha256(pcm.tobytes()).hexdigest().upper(),
                predictedSHA256=hashlib.sha256(predicted.tobytes()).hexdigest().upper(),
                completeSourceClocks=clocks, actualWaveformFaultsRejected=faults,
                mainLaunches=3, auxiliaryCues=1, completeAnnouncements=5), events, names


def packet_gate(text):
    source = inspect.getsource(packet_source.packet_gate)
    before = "not markers and len(selection)==2 and {r['word']for r in selection}=={'FFFB','FFFC'}and"
    after = "len(markers)==4 and [r['word']for r in markers]==['FFFD','FFFD','FFFE','FFFE'] and len(selection)==1 and selection[0]['word']=='FFFC'and"
    need(source.count(before) == 1, 'Whole original packet grammar, actual announcer inventory only')
    source = source.replace(before, after, 1)
    need(source.count('len(launches)==1') == 1, 'All actual complete launch markers')
    source = source.replace('len(launches)==1', 'len(launches)==4', 1)
    need(source.count('len(all_sounds)==len(sounds)+len(selection)+len(launches)') == 1, 'Complete port inventory includes original winner markers')
    source = source.replace('len(all_sounds)==len(sounds)+len(selection)+len(launches)', 'len(all_sounds)==len(sounds)+len(selection)+len(launches)+len(markers)', 1)
    scope = dict(vars(packet_source))
    exec(compile(source, __file__+'::whole_original_packet_ADSP_delivery_actual_stage_inventory', 'exec'), scope)
    return scope['packet_gate'](text)
