"""Same retained native run: true CPU Sonya P2, full DCS + Square waveform.

This is a finite source/ownership/EOF proof, not full-port acceptance. Nothing
here writes guest memory or adjusts actual audio. Faults modify copies only.
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
import qualify_native_attract_early_square as prior
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated

ROOT, need, sha = prior.ROOT, prior.need, prior.sha
audio, rows = prior.names.audio, prior.names.runtime.rows


def predict(c):
    sounds = rows(c['text'], 'SOUND')
    need(len(sounds) == 1, 'One complete actual imported-source marker; no omitted announcements')
    launch = sounds[0]
    need(launch['word'] == '6B00' and launch['pc'] == 'FFFFCAC0' and
         launch['mode'] == '1' and launch['mute'] == '0' and
         launch['a8'] == launch['p2_actor'] == launch['p2_owner'] and
         launch['a13'] == launch['p2_main'] and
         launch['p2_id'] == launch['p2_roster'] == '18' and
         launch['p2_action'] == '519' and launch['p2_hp'] == '158' and
         launch['p1_id'] == launch['p1_roster'] == '8',
         'Actual unmuted true Sonya18 P2 vs Subzero8 with live, already-damaged owner')
    path = ROOT / 'samples/mk2ks/sonya_square_launch.wav'
    with wave.open(str(path), 'rb') as reader:
        need((reader.getnchannels(), reader.getsampwidth(), reader.getframerate(),
              reader.getnframes(), reader.getcomptype()) == (1, 2, 48000, 45512, 'NONE'),
             'Whole finite original Square clip')
        signal, positions = audio.sample_values(np.frombuffer(reader.readframes(45512), '<i2').copy(), 48000)
    headers = [r['header'] for r in c['pcm']]
    need(len(headers) == len(c['dac']) == len(c['dacHeaders']) == 256 and
         [len(g) for g in prior.groups(headers)] == [256], 'Entire one contiguous real captured window')
    actual = []
    nonzero = 0
    for i, (record, raw, dac) in enumerate(zip(c['pcm'], c['dac'], c['dacHeaders'])):
        h, pcm = record['header'], record['pixels']
        need(len(pcm) == 3840 and sha_bytes(pcm) == h['sha256'], 'Every whole unchanged stereo PCM buffer')
        need(all(dac[k] == h[k] for k in ('frame', 'seconds')) and int(dac['index']) == i + 1 and
             dac['writes'] == '0' and dac['assistance'] == 'none' and dac['prefix'] == '4' and
             dac['ring'] == '32768' and dac['element_bytes'] == '4', 'Every passive native DAC/PCM association')
        need(len(raw) == 629 * 4 and sha_bytes(raw) == dac['sha256'] and dac['consumed'] == '625' and
             (int(dac['current_out']) - int(dac['previous_out'])) % 32768 == 625 and
             Decimal(dac['seconds']) - Decimal(dac['previous_seconds']) == Decimal('.02'),
             'Exact native 31250Hz serial interval, prefix and complete ring traversal')
        if i:
            need(dac['previous_out'] == c['dacHeaders'][i-1]['current_out'], 'Continuous native DAC cursor')
        need(dac['enabled'] == dac['channels'] == dac['incs'] == '1' and dac['volume'] == '3F800000' and
             int(dac['autobuffer'], 16) & 2 and int(dac['syscontrol'], 16) & 0x0800,
             'Original enabled unit-gain mono serial hardware')
        values = np.frombuffer(raw, '<f4')
        need(np.isfinite(values).all(), 'All native hardware float samples finite')
        integers = np.rint(values.astype(np.float64) * 32767)
        need(np.all((integers >= -32768) & (integers <= 32767)) and
             np.array_equal((integers.astype(np.float32) * np.float32(1 / 32767)).view('<u4'), values.view('<u4')),
             'Every original signed16 DCS normalization bit exact')
        nonzero += int(np.count_nonzero(values[4:]))
        actual.append(np.frombuffer(pcm, '<i2').reshape(960, 2))
    actual = np.concatenate(actual)
    need(nonzero > 1000, 'Actual non-silent native DCS carrier, not inferred from mixed PCM')
    dcs, clocks = audio.float_model()(c['dac'], c['dacHeaders'])
    need(dcs.shape == actual.shape, 'Complete original float32 native cached resampler, no trimmed edges')
    start = audio.sample_clock(launch['seconds'], True)
    voice = np.zeros_like(dcs)
    for i, h in enumerate(headers):
        tick = int(Decimal(h['seconds']) * 50)
        sec, fraction = divmod((tick - 1) * 960 * (audio.ATTO // 48000), audio.ATTO)
        view = sec * 48000 + fraction // audio.PERIOD
        at = np.arange(view, view + 960, dtype=np.int64) - start
        valid = (at >= 0) & (at < len(signal))
        segment = np.zeros(960, '<f4')
        segment[valid] = np.float32(signal[at[valid]] * np.float32(.70))
        voice[i*960:(i+1)*960, 0] = segment
        voice[i*960:(i+1)*960, 1] = segment
    predicted = convert(np.float32(dcs + voice))
    return predicted, actual, dict(launch=launch, start=start, positions=positions, dcs=dcs, voice=voice,
                                  clocks=clocks, nonzeroNativeSamples=nonzero, clipSHA256=sha(path))


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest().upper()


def convert(value):
    return (np.clip(value, -1, 1).astype(np.float64) * 32767).astype('<i2')


def source_gate(c, model):
    headers = [r['header'] for r in c['pcm']]
    channels = audio.rows(c['text'], 'MK2_TOMB_MIX_CHANNEL')
    need(len(channels) == 256 * 14 and {(int(r['index']), int(r['channel'])) for r in channels} ==
         {(i, ch) for i in range(1, 257) for ch in range(14)}, 'All fourteen channels at every real sound callback')
    active = tails = 0
    for r in channels:
        h = headers[int(r['index'])-1]
        need(all(r[k] == h[k] for k in ('frame', 'seconds')) and r['loop'] == r['paused'] == r['writes'] == '0' and
             r['assistance'] == 'none', 'Every exact source-clock callback is passive and non-looping')
        length, position = 0, 0.0
        if r['channel'] == '12':
            tick = int(Decimal(h['seconds']) * 50)
            sec, frac = divmod(tick * 960 * (audio.ATTO // 48000), audio.ATTO)
            end = sec * 48000 + (frac + audio.PERIOD - 1) // audio.PERIOD
            count = min(45512, max(0, end - model['start']))
            length = 45512
            position = model['positions'][count-1] if count else 0.0
            active += int(0 < count < 45512)
            tails += int(count == 45512)
        # Original samples.cpp uses the previous length: first launch's num=-1.
        need(r['sample'] == '4294967295' and int(r['length']) == length and
             float(r['position']) == position and r['bits'] == struct.pack('<d', position).hex().upper(),
             'Every precise native source ID/length/repeated-double position and finite EOF bit')
    need(active and tails and sha(ROOT/'mame-mkp/src/devices/sound/samples.cpp') ==
         '8BF4BB350F40B309A5CECB4591DF8EE32A3563C3E061F2D2338C8CBA76B5353F',
         'Actual complete playback and EOF through conserved original sample implementation')
    owners = rows(c['text'], 'AUDIO_OWNER')
    playing = [r for r in owners if audio.sample_clock(r['seconds'], False) < model['start'] + 45512]
    need(playing and all(r['mode'] == '1' and r['mute'] == '0' and r['p2_actor'] == r['p2_owner'] == model['launch']['a8'] and
         r['p2_main'] == model['launch']['a13'] and r['p2_id'] == r['p2_roster'] == '18' and r['p2_hp'] == '158'
         for r in playing), 'Every observed live P2 owner keeps launch HP until complete source EOF')
    inputs = rows(c['text'], 'INPUT')
    need([(int(r['frame']), r['value'], r['button']) for r in inputs] ==
         [(f, '1', 'HighPunch') for f in range(482, 486)] + [(486, '0', 'HighPunch')], 'Ordinary acknowledgement only')
    config, dip, switches = rows(c['text'], 'CONFIG'), rows(c['text'], 'DIP'), rows(c['text'], 'SWITCH_POLICY')
    need(len(config) == 1 and config[0]['boot_start'] == '482' and config[0]['capture_winners'] == '1', 'Actual wrapper configuration')
    need(len(dip) == 1 and all(dip[0][k] == '1000' for k in ('mask', 'default', 'configured')) and dip[0]['actual'] == 'FC7D',
         'Original physical Attract Sound On switch, never guest flag assistance')
    need(len(switches) == 1 and switches[0]['pc'] == 'FF8474B0' and switches[0]['a0'] == '000041C0', 'Actual stock switch-policy return')
    mutes = rows(c['text'], 'MUTE_POLICY')
    before = [r for r in mutes if Decimal(r['seconds']) <= Decimal(model['launch']['seconds'])]
    need(before[-1]['pc'] == 'FF8278D0' and before[-1]['value'] == '0', 'Original demo startup enables sound')
    need(any(r['pc'] == 'FF843960' and r['value'] == '1' and Decimal(r['seconds']) > Decimal(model['launch']['seconds']) for r in mutes),
         'Original later attract mute still executes')
    need(not rows(c['text'], 'ERROR_ENTRY') and rows(c['text'], 'RESULT')[-1]['boots'] == '0', 'No executed native error or soft reset')
    return dict(preciseChannelStates=len(channels), activeCallbacks=active, finiteEOFTailCallbacks=tails,
                physicalInputs=inputs, actualDIP=dip, lastMuteBeforeLaunch=before[-1], observedOwnerHP=158)


def finish(c):
    out = c['folder'] / 'native_audible_square_p2.json'
    need(not out.exists() and c['terminal']['nativeExit'] == 0 and not native.census() and
         c['guest'] == prior.current.expected(), 'Same terminal native run and independent whole current source/compiled guest')
    predicted, actual, model = predict(c)
    different = np.argwhere(predicted != actual)
    comparison = dict(passed=not len(different), differentChannelSamples=len(different), comparedStereoFrames=len(actual),
                      actualSHA256=sha_bytes(actual.tobytes()), predictedSHA256=sha_bytes(predicted.tobytes()),
                      firstDifferences=[dict(frame=int(i), channel=int(ch), expected=int(predicted[i,ch]), actual=int(actual[i,ch]))
                                        for i,ch in different[:8]])
    # Preserve actual failures before any repair to a checker or game source.
    if len(different):
        (c['folder']/'square_p2_initial_comparison_failure.json').write_text(json.dumps(comparison, indent=2)+'\n')
        raise ValueError('Entire actual mixed PCM differs; preserved initial failure')
    sources = source_gate(c, model)
    faults = []
    for label, i, ch in [('first PCM bit', 0, 0), ('last PCM bit', len(actual)-1, 1)]:
        bad = actual.copy(); bad[i,ch] ^= 1
        need(not np.array_equal(predicted, bad), 'Whole actual PCM bit fault rejected')
        faults.append(dict(fault=label, rejected=True))
    need(predicted.shape != actual[:-1].shape, 'Last stereo frame cannot be omitted')
    faults.append(dict(fault='omitted final stereo frame', rejected=True))
    late = np.zeros_like(model['voice']); late[1:] = model['voice'][:-1]
    for label, bad in [('Square omitted', convert(model['dcs'])), ('DCS omitted', convert(model['voice'])),
                       ('Square one sample late', convert(np.float32(model['dcs']+late))),
                       ('Square .70 route omitted', convert(np.float32(model['dcs']+model['voice']/np.float32(.70))))]:
        need(not np.array_equal(actual, bad), 'Effective source-operation fault rejected')
        faults.append(dict(fault=label, differentChannelSamples=int(np.count_nonzero(actual != bad))))
    row = model['launch']; original = ' '.join(k+'='+v for k,v in row.items())
    need(original in c['text'], 'Whole actual source marker located')
    for key, value in [('p2_id', '17'), ('p2_owner', '00000000'), ('mute', '1')]:
        altered = dict(row, **{key:value})
        bad = dict(c, text=c['text'].replace(original, ' '.join(k+'='+v for k,v in altered.items()), 1))
        try:
            predict(bad)
        except ValueError as error:
            faults.append(dict(fault='launch '+key+' corrupted', rejectedBy=str(error)))
        else:
            raise ValueError('Bad launch owner admitted')
    need(np.array_equal(predicted, actual), 'Complete source-positive restored')
    for name, buffers in [('captured_native_audio.pcm.gz', [r['pixels'] for r in c['pcm']]),
                          ('captured_native_dac.f32.gz', c['dac'])]:
        path = c['folder']/name
        need(not path.exists(), 'Single compact evidence carrier, never duplicate ROM/build/raw media')
        with gzip.open(path, 'wb') as stream:
            for raw in buffers: stream.write(raw)
        with gzip.open(path, 'rb') as stream:
            need(all(stream.read(len(raw)) == raw for raw in buffers) and not stream.read(), 'Every archived byte exact')
    executed = {}
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):
            path = Path(file).resolve()
            executed[str(path)] = dict(sha256=sha(path), text=path.read_text())
    with gzip.open(c['folder']/'executed_square_p2_qualification_sources.json.gz', 'wt', encoding='utf-8') as stream:
        json.dump(executed, stream)
    result = dict(passed=True, goalStatus='active', fullPortAcceptance=False, audibleKanoAccepted=False,
                  finiteAudibleSonyaP2SquareAccepted=True, fullAttractAudioAccepted=False, nativeTerminal=c['terminal'],
                  comparison=comparison, exactSources=sources, marker=row, nonzeroNativeDCSSamples=model['nonzeroNativeSamples'],
                  nativeClocks=model['clocks'], clipSHA256=model['clipSHA256'], faultsRejected=faults,
                  wholePCMHeaders=[r['header'] for r in c['pcm']], wholeDACHeaders=c['dacHeaders'],
                  previousGoalTurnClassification='no progress: status only; retained live RAM handle revalidated',
                  thisGoalTurnClassification='progress: exact true-player-two audible CPU Square full DCS/source playback and EOF proof',
                  remaining=json.loads((ROOT/'audit_native_dual_roll_progress_storage/report.json').read_text())['remaining'],
                  publicBuildPromoted=False, newBuilds=0, newROMCopies=0, newZIPs=0)
    out.write_text(json.dumps(result, indent=2)+'\n')
    paths = [p for p in c['folder'].rglob('*') if p.is_file()] + [Path(__file__).resolve()]
    storage = []
    for path in paths:
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(), 'Exact in-workspace compact evidence target')
        digest = sha(path)
        subprocess.run(['compact.exe', '/C', '/EXE:LZX', '/F', '/I', '/Q', str(path)], check=True, capture_output=True)
        need(sha(path) == digest, 'Compression preserves bytes')
        storage.append(dict(path=str(path), allocatedBytes=allocated(path), sha256=digest))
    (c['folder']/'square_p2_storage_receipt.json').write_text(json.dumps(dict(passed=True, files=storage), indent=2)+'\n')
    print(json.dumps(dict(passed=True, comparedStereoFrames=len(actual), preciseChannelStates=sources['preciseChannelStates'],
                         faults=len(faults), allocatedEvidenceBytes=sum(r['allocatedBytes'] for r in storage))), flush=True)
    return result
