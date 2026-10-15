"""Source-exact whole native sound for actual paired/Knife overlap27520.

This actual sequence has one Kano winner and no imported6B00..6B03 battle
sample. Keep the original whole float32 DCS/cache/resampler and winner mixer;
bind the existing exact channel-clock model to this one actual winner marker.
No sample/time/gain fitting or imported cue borrowed from another game.
"""
import ast
import hashlib
import inspect
import json
import re
import sys
import traceback
from pathlib import Path
import numpy as np
import capture_native_selector_sonya_walkin_kano_cpu as capture
import qualify_native_selector_sonya_walkin_body_shadow as geometry
import qualify_native_selector_opposite_roles_winner_pcm as original

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
model = original.model
OUT = ROOT/'audit_native_selector_sonya_walkin_winner_pcm_checked'
PARENT = geometry.OUT/'report.json'


def channel_binding():
    source = inspect.getsource(original.channel_clocks)
    parsed = ast.parse(source)
    comparisons = [n for n in ast.walk(parsed) if isinstance(n, ast.Compare) and
        isinstance(n.left, ast.ListComp) and len(n.comparators) == 1 and
        isinstance(n.comparators[0], ast.List) and len(n.comparators[0].elts) == 2]
    need(len(comparisons) == 1, 'Only exact finite winner-marker inventory changes')
    before = ast.get_source_segment(source, comparisons[0].comparators[0])
    need(ast.literal_eval(before) == [('2286', 'FFFE', 'FFFEFD10', '0106AA60'),
                                    ('3137', 'FFFE', 'FFFEFD10', '0106AA60')],
         'Original two-marker context, all channel/source-clock equations retained')
    after = "[('2553', 'FFFE', 'FFFEFD10', '0106AA60')]"
    need(source.count(before) == 1, 'Exact whole original marker predicate')
    source = source.replace(before, after, 1)
    scope = dict(vars(original), __file__=__file__)
    exec(compile(source, __file__+'::unchanged_clocks_single_actual_winner', 'exec'), scope)
    return scope['channel_clocks'], hashlib.sha256(source.encode()).hexdigest().upper()


def execute(state):
    need(not OUT.exists(), 'New immutable full actual walk-in waveform proof')
    parent = json.loads(PARENT.read_text()); pins = dict(parent['inputHashes'])
    folder, text, images = capture.RAM_CASES[capture.KEY]
    held = capture.NATIVE_HANDLES[capture.KEY]
    meta = json.loads((folder/'result.json').read_text())
    audio = capture.AUDIO[capture.KEY]
    need(parent['passed'] and meta['passed'] and
         held['process'].poll() == meta['nativeExit'] == 0 and
         held['identity'] == parent['actualNativeIdentity'] == meta['nativeTerminal']['actualWindowsIdentity'] and
         (held['identity']['ProcessId'], held['identity']['ParentProcessId'], held['identity']['createdUnix']) ==
         (27520, 38752, 1791760361.8604069) and
         all(sha(p) == h for p, h in pins.items()), 'Same original terminal27520 and entire geometry/source inventory')
    for tag, chunks, headers in (
            ('MK2_BBAUDIO_PCM_DIGEST', audio['pcmChunks'], audio['pcmHeaders']),
            ('MK2_NATIVE_DAC_RAM_DIGEST', audio['dacChunks'], audio['dacHeaders'])):
        records = model.rows(text, tag)
        need(len(records) == len(chunks) == len(headers) == 1645 and
             all(r == dict(h, sha256=hashlib.sha256(raw).hexdigest().upper())
                 for r, h, raw in zip(records, headers, chunks, strict=True)),
             'Every full actual native PCM/DAC chunk and callback digest')
    video = model.rows(text, 'MK2_MAUDIO_CHANNEL')
    precise = model.rows(text, 'MK2_TOMB_MIX_CHANNEL')
    need([(int(r['frame']), int(r['channel'])) for r in video] ==
         [(f, c) for f in range(1815, 3616) for c in range(19)] and
         [(r['frame'], r['seconds'], int(r['channel'])) for r in precise] ==
         [(h['frame'], h['seconds'], c) for h in audio['pcmHeaders'] for c in range(19)],
         'All nineteen native channels at every independent video/sound callback')
    clocks, clock_hash = channel_binding()
    clock_result = clocks(text, audio['pcmHeaders'], pins)
    pcm = np.frombuffer(b''.join(audio['pcmChunks']), dtype='<i2').reshape(-1, 2)
    waveform = model.predict_mix(audio['dacChunks'], audio['dacHeaders'], pcm, text, 'kano', pins)
    OUT.mkdir()
    (OUT/'waveform.json').write_text(json.dumps(waveform, indent=2)+'\n')
    need(waveform['passed'] and waveform['differentChannelSamples'] == 0 and
         waveform['comparedStereoFrames'] == 1579200 and
         len(waveform['actualRawMixedPCMFaultsRejected']) == 4 and
         len(waveform['actualMixedSourceOperationFaultsRejected']) == 4,
         'Whole unchanged native source model exactly predicts every actual mixed PCM sample')
    def change(tag, key, value, **where):
        line = next(s for s in text.splitlines() if s.startswith(tag+' ') and
                    all(dict(re.findall(r'(\w+)=([^\s]+)', s)).get(k) == str(v) for k, v in where.items()))
        bad, count = re.subn(r'\b'+key+r'=\S+', key+'='+value, line, count=1)
        need(count == 1 and bad != line, 'Effective actual channel-clock mutation')
        return text.replace(line, bad, 1)
    active = next(r for r in video if r['channel'] == '0' and r['sample'] == '2' and
                  int(r['frame']) > 2553 and float(r['pos']) > 0)
    full = next(r for r in precise if r['channel'] == '0' and r['sample'] == '2' and
                int(r['frame']) > 2553 and float(r['position']) > 0)
    trials = [
        ('winner_source', change('MK2_MAUDIO_CHANNEL', 'sample', '3', frame=active['frame'], channel=0)),
        ('winner_length', change('MK2_MAUDIO_CHANNEL', 'length', '31999', frame=active['frame'], channel=0)),
        ('winner_video_clock', change('MK2_MAUDIO_CHANNEL', 'pos', format(float(active['pos'])+1, '.8f'), frame=active['frame'], channel=0)),
        ('winner_precise_bits', change('MK2_TOMB_MIX_CHANNEL', 'bits', '0000000000000000', seconds=full['seconds'], channel=0)),
        ('inactive_channel', change('MK2_MAUDIO_CHANNEL', 'length', '1', frame=active['frame'], channel=18)),
        ('channel_assistance', change('MK2_MAUDIO_CHANNEL', 'writes', '1', frame=active['frame'], channel=0)),
    ]
    faults = []
    for label, bad in trials:
        try:
            clocks(bad, audio['pcmHeaders'], pins)
        except (ValueError, AssertionError) as error:
            faults.append(dict(fault=label, rejectedBy=str(error)))
        else:
            raise ValueError('Actual source-clock corruption admitted '+label)
    need(len(faults) == 6 and clocks(text, audio['pcmHeaders'], pins) == clock_result,
         'Every six actual clock faults rejects and complete source-clock positive restored')
    paths = {Path(__file__).resolve(), PARENT.resolve(), (OUT/'waveform.json').resolve()}
    for module in tuple(sys.modules.values()):
        name = getattr(module, '__file__', None)
        if name:
            path = Path(name).resolve()
            if path.is_relative_to(ROOT) and path.is_file(): paths.add(path)
    for path in paths:
        key = str(path); digest = sha(path)
        need(key not in pins or pins[key] == digest, 'No executed/source/evidence byte replaced')
        pins[key] = digest
    need(all(sha(p) == h for p, h in pins.items()), 'Whole complete source inventory after waveform and faults')
    value = dict(passed=True, goalStatus='active', actualNativeIdentity=held['identity'],
        wholeMixedWaveform=waveform, wholeSourceChannelClocks=clock_result,
        actualChannelClockFaultsRejected=faults, entireClockModelSHA256=clock_hash,
        entireSourceModelSHA256=sha(model.__file__), inputHashes=pins,
        requirements=parent['requirements'], remainingGroups=parent['remainingGroups'],
        finiteActualPairKnifeSourceExactAudioAccepted=True, importedBattleCuesInActualGame=0,
        allAudioOwnerPriorityContextsAccepted=False, heardAudioQualityAccepted=False,
        fullPortAcceptance=False, publicPlayableChanged=False,
        newNativeGames=0, newBuilds=0, newROMCopies=0, newRawMediaFiles=0, newZIPs=0)
    (OUT/'report.json').write_text(json.dumps(value, indent=2)+'\n')
    print('PASS whole1579200 native mixed stereo frames, all19 channel clocks and14 waveform/clock faults', flush=True)
    return value


def safe_execute(state):
    try:
        return execute(state)
    except Exception as error:
        if not OUT.exists(): OUT.mkdir()
        need(not (OUT/'failure.json').exists(), 'Preserve original exact audio rejection')
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False, error=repr(error),
            traceback=traceback.format_exc(), goalStatus='active', newNativeGames=0,
            fullPortAcceptance=False), indent=2)+'\n')
        raise
