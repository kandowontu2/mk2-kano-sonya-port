"""Current3172 human Friendships: paired full audible cues in RAM, both slots.

Unchanged physical controls earn two wins and execute native own-ID actions.
Only read-only PNG output is omitted; mixed PCM is never written to disk.
Retained original-PCM asset evidence is hash-bound, not regenerated. This is
not complete finisher raster/shadows, other victims/arenas or whole-port QA.
"""
import concurrent.futures
import copy
import hashlib
import inspect
import json
import re
import subprocess
import sys
import traceback
from pathlib import Path
import numpy as np
import run_current_bicycle_block_audio_v3390 as collector
import verify_current_cpu_square_v3280 as current
import verify_current_friendship_audio_v2672 as audio

ROOT, need, sha = collector.ROOT, collector.need, collector.sha
OUT = ROOT / 'audit_v3563_current_friendship_ram_audio_checked'
OLD = ROOT / 'audit_v2922_candidate_friendship_audio_checked/report.json'
LUA = ['mk2ks_current_friendship_ram_probe_v3557.lua',
       'mk2ks_current_friendship_ram_audio_v3558.lua',
       'mk2ks_current_friendship_ram_wins_v3559.lua',
       'mk2ks_current_friendship_ram_mix_v3560.lua']
EXPECTED = None


def source_control():
    original = (ROOT / 'mk2ks_native_friendship_probe_v784.lua').read_text()
    changes = {
        ";screen:snapshot('selection_p'..n..'.png')": '',
        "  if action_age>=40 and action_age<=198 then screen:snapshot('native_field_'..action_age..'.png')end\n": '',
        "  screen:snapshot('friendship_'..age..'.png')\n": '',
    }
    for before, after in changes.items():
        need(original.count(before) == 1, 'Only declared read-only snapshot omission')
        original = original.replace(before, after)
    need((ROOT / LUA[0]).read_text() == original, 'Every physical controller and native observation unchanged')
    for old, new, before, after in (
        ('mk2ks_native_friendship_audio_v790.lua', LUA[1],
         'mk2ks_native_friendship_probe_v784.lua', LUA[0]),
        ('mk2ks_current_friendship_wins_v2651.lua', LUA[2],
         'mk2ks_native_friendship_audio_v790.lua', LUA[1]),
    ):
        source = (ROOT / old).read_text()
        need(source.count(before) == 1 and (ROOT / new).read_text() == source.replace(before, after),
             'Only explicit read-only observer chain adaptation')
    for name in LUA:
        need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)', (ROOT / name).read_text()),
             'No guest/register/loaded-state writes')
    need((ROOT / LUA[3]).read_text().count("dofile('" + LUA[2] + "')") == 1 and
         not re.search(r'set_value|clear_value', (ROOT / LUA[3]).read_text()),
         'New RAM observer cannot change physical controls')


def capture(fighter, side, enabled):
    # Keep the already-executed PCM isolation, terminal checks and hierarchical
    # input snapshots. Explicitly replace only controller/case/window metadata.
    source = inspect.getsource(collector.capture)
    changes = {
        'audit_v3391_current_bicycle_block_audio_p{side}_{suffix}':
            'audit_v3562_current_{fighter}_friendship_audio_p{side}_{suffix}',
        "ROOT/'mk2ks_human_special_negative_v9.lua',ROOT/'mk2ks_human_bicycle_block_trace_v3345.lua',ROOT/'mk2ks_human_bicycle_block_push_v3373.lua',\n      ROOT/'mk2ks_human_bicycle_block_audio_v3386.lua'":
            "*[ROOT/n for n in LUA],Path(collector.__file__).resolve(),\n      ROOT/'mk2ks_native_friendship_probe_v784.lua',ROOT/'mk2ks_native_friendship_audio_v790.lua',ROOT/'mk2ks_current_friendship_wins_v2651.lua'",
        "files.update((ROOT/'roms/mk2ks').glob('*'));":
            "files.update((ROOT/'samples/mk2ks').glob('*'));files.update((ROOT/'roms/mk2ks').glob('*'));",
        "env.update(MK2KS_HUMAN_SPECIAL_MOVE='bicycle',MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_SCENARIO='block',\n               MK2KS_HUMAN_SPECIAL_VICTIM='kano',MK2KS_BBLOCK_OUT=str(folder))":
            "env.update(MK2KS_FRIEND_WINNER=fighter,MK2KS_FRIEND_SIDE=str(side),MK2KS_FRIEND_CASE='positive',MK2KS_FRIEND_OUT=str(folder))",
        "'-str','65'": "'-str','180'",
        "ROOT/'mk2ks_human_bicycle_block_audio_v3386.lua'": "ROOT/LUA[3]",
        "move='bicycle',side=side,scenario='block',victim='kano'":
            "move='friendship',side=side,scenario='positive',winner=fighter,victim='sonya'if fighter=='kano'else'kano',guest_writes=0",
    }
    for before, after in changes.items():
        need(source.count(before) == 1, 'Exactly declared RAM collector adaptation: ' + before[:70])
        source = source.replace(before, after)
    namespace = dict(vars(collector))
    namespace.update(__file__=__file__, fighter=fighter, LUA=LUA, collector=collector)
    exec(compile(source, __file__ + '::unchanged_pcm_collector', 'exec'), namespace)
    return namespace['capture'](side, enabled)


def retained_templates():
    proof = json.loads(OLD.read_text())
    need(proof['passed'] and proof['originalPCMAndAudibleOverlapAccepted'] and
         proof['all20OriginalCluckChannelsReconstructed'] and not proof['fullPortAcceptance'],
         'Actual retained original audio evidence; no universal acceptance')
    templates, assets = {}, {}
    for name, metadata in proof['originalAssets'].items():
        path = ROOT / 'samples/mk2ks' / (name + '.wav')
        need(sha(path) == proof['inputHashes'][str(path)], 'Retained exact original asset bytes')
        clip = audio.mono_asset(path)
        need(len(clip) == metadata['frames'], 'Complete original hardware latency/waveform/tail length')
        # Original proof recorded full hardware PCM; retained compensated s16
        # samples recover each integer PCM word by nearest rounding at .70.
        raw = np.rint(clip * .70).astype('<i2').tobytes()
        need(hashlib.sha256(raw).hexdigest().upper() == metadata['sourcePCM_SHA256'],
             'Entire retained original source PCM digest, no screenshot/port-derived oracle')
        templates[metadata['command']] = clip * .70
        assets[name] = dict(**metadata, sha256=sha(path), inheritedOriginalProof=str(OLD),
                            originalRawReferencesRecreated=False)
    return templates, assets


def pair(case, templates):
    fighter, side = case
    folder, headers, a = capture(fighter, side, True)
    baseline, quiet_headers, b = capture(fighter, side, False)
    timeline = lambda hs: [{k: v for k, v in h.items() if k != 'sha256'} for h in hs]
    need(timeline(headers) == timeline(quiet_headers) and a.shape == b.shape,
         'Every actual paired mixed PCM update exactly aligned')
    parse = lambda p: [(tag, row) for tag, row in audio.scene.previous.parse(p)
                       if not tag.startswith('MIX_')]
    rows, quiet = parse(folder / 'run.log'), parse(baseline / 'run.log')
    audio.baselines.exact(rows, quiet)
    control = audio.scene.check(rows, fighter, side)
    need(audio.scene.check(quiet, fighter, side) == control,
         'Enabled/disabled actual native selection/earned wins/poses/ownership/cleanup unchanged')
    for leaf in (folder, baseline):
        need((leaf / 'guest_maincpu.bin').read_bytes() == EXPECTED[0],
             'Entire actual current guest independently assembled, no masked bytes')
    chronology = audio.native.runtime(rows, fighter, side, 'positive')
    # The same controls on2753 are useful as a full chronology cross-check,
    # never a substitute for these actual3172 captures.
    old = ROOT / f'audit_v2920_candidate_{fighter}_friendship_positive_audible_p{side}' / 'run.log'
    need(rows == audio.scene.previous.parse(old), 'All original positive physical/native records retained on3172')
    delta = a - b
    need(np.array_equal(delta[:, 0], delta[:, 1]), 'Imported contribution is genuine dual mono')
    signal = delta[:, 0]
    origin = float(headers[0]['seconds']) - int(headers[0]['bytes']) / 4 / 48000
    cues = audio.scene.previous.select(rows, 'AUDIO')
    others = [(round((float(v['seconds']) - origin) * 48000),
               audio.native.existing_sample(ROOT, int(v['command'], 16)))
              for v in audio.scene.previous.select(rows, 'VOICE')]
    groups, first_data, variants = [], None, set()
    step = 1 if fighter == 'kano' else 3
    for first in range(0, len(cues), step):
        group = cues[first:first + step]
        commands = [0x6e if fighter == 'kano' else
                    (0xa5, 0xaa, 0xaf, 0x96)[(int(c['command'], 16) - 0x6aa0) // 5] for c in group]
        starts = [round((float(c['seconds']) - origin) * 48000) for c in group]
        clips = [templates[c] for c in commands]
        fit = audio.native.fit_overlap(signal, starts, clips, others)
        groups.append(dict(firstCue=first, commands=commands, startsPCM=starts, **fit))
        variants.update(commands)
        if first_data is None:
            first_data = (starts, clips, fit)
    faults = audio.pcm_counterexamples(signal, *first_data[:2], others, first_data[2], templates, fighter)
    changed = copy.deepcopy(rows)
    at = next(i for i, (tag, row) in enumerate(changed) if tag == 'AUDIO')
    changed[at][1]['id'] = '1'
    faults.append(audio.reject(lambda: audio.native.runtime(changed, fighter, side, 'positive'),
                              'proxy_audio_owner', ('Audio belongs to wrong actor/task',)))
    changed = copy.deepcopy(rows)
    if fighter == 'kano':
        changed[at][1]['frame'] = str(int(changed[at][1]['frame']) + 1)
        fault_label = 'Pop is not at the native burst phase'
    else:
        changed[at][1]['command'] = f"{int(changed[at][1]['command'], 16) + 1:04X}"
        fault_label = 'Not original first-free independent voice allocation'
    faults.append(audio.reject(lambda: audio.native.runtime(changed, fighter, side, 'positive'),
                              'wrong_native_cue_or_voice_allocation', (fault_label,)))
    channels = audio.scene.previous.select(audio.scene.previous.parse(folder / 'run.log'), 'MIX_CHANNEL')
    quiet_channels = audio.scene.previous.select(audio.scene.previous.parse(baseline / 'run.log'), 'MIX_CHANNEL')
    need(channels and len(channels) == len(quiet_channels) and
         all(r['loop'] == r['paused'] == r['writes'] == '0' for r in channels) and
         all(r['length'] == '0' for r in quiet_channels),
         'Whole finite unpaused sample ledger and silent disabled control')
    unused = set(range(4, 9)) if fighter == 'kano' else {9}
    need(all(r['length'] == '0' for r in channels if int(r['channel']) in unused),
         'No wrong Friendship channel or bubble/chicken overlap')
    audio.baselines.exact(rows, quiet)
    need(audio.native.runtime(rows, fighter, side, 'positive') == chronology,
         'Unmodified native audio control after qualified faults')
    print(f'{fighter}_p{side}: current native full cues/tails/overlap, owner and physical cleanup passed', flush=True)
    return dict(winner=fighter, side=side, capture=folder.name, baseline=baseline.name,
                nativeScene=control, audioChronology=chronology, groups=groups,
                variants=sorted(variants), actualQualifiedFaults=faults,
                physicalNativeRecords=len(rows), channelRecords=len(channels),
                mixedPCMUpdates=len(headers), mixedPCMFrames=len(signal),
                samplesNeverChangedGameplay=True, samePathUnmodifiedPositive=True)


def run():
    global EXPECTED
    need(not OUT.exists(), 'Fresh immutable current Friendship evidence')
    source_control()
    EXPECTED = current.expected_current()
    need((ROOT / collector.CANDIDATE / 'roms/mk2ks/mk2ks.mdata').read_bytes() == EXPECTED[2],
         'Whole current payload independently assembled')
    templates, assets = retained_templates()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        cases = list(pool.map(lambda c: pair(c, templates),
                              [(fighter, side) for fighter in ('kano', 'sonya') for side in (1, 2)]))
    need(set(v for c in cases for v in c['variants']) == {0x6e, 0xa5, 0xaa, 0xaf, 0x96},
         'All original retained Friendship waveform variants exercised')
    pins = {str(OLD): sha(OLD)}
    for c in cases:
        oldlog = ROOT / f"audit_v2920_candidate_{c['winner']}_friendship_positive_audible_p{c['side']}" / 'run.log'
        pins[str(oldlog)] = sha(oldlog)
        for name in (c['capture'], c['baseline']):
            folder = ROOT / name
            meta = json.loads((folder / 'result.json').read_text())
            for file, digest in meta['input_hashes'].items():
                need(file not in pins or pins[file] == digest, 'Consistent actual capture input pins')
                pins[file] = digest
            for path in folder.rglob('*'):
                if path.is_file():
                    pins[str(path)] = sha(path)
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file and Path(file).suffix == '.py' and Path(file).resolve().is_relative_to(ROOT / 'tools'):
            pins[str(Path(file).resolve())] = sha(file)
    for file, digest in pins.items():
        need(sha(file) == digest, 'All relevant executed source/capture bytes unchanged')
    return dict(passed=True, candidate=collector.CANDIDATE, cases=cases, originalAssets=assets,
                actualPhysicalCaptures=8, actualAudibleCues=sum(c['audioChronology']['cues'] for c in cases),
                actualQualifiedFaults=sum(len(c['actualQualifiedFaults']) for c in cases),
                current3172BothHumanSlotFullRetainedFriendshipCueTailOverlapOwnershipAccepted=True,
                wholeCurrentGuestAndPayloadIndependentlyReconstructed=True,
                originalPhysicalControllerByteExactExceptReadOnlySnapshotOmission=True,
                historicalOriginalRawReferencesRecreated=False, rawAudioFilesWritten=0,
                newExecutableOrROMCopies=0, allFriendshipVictimsArenasCPUOrCompleteRasterAccepted=False,
                allFinisherOrPortAcceptance=False, fullPortAcceptance=False,
                inputHashes=pins, scope=__doc__)


if __name__ == '__main__':
    try:
        value = run()
    except Exception as error:
        value = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), fullPortAcceptance=False)
    need(not OUT.exists(), 'Never overwrite executed result')
    OUT.mkdir()
    path = OUT / 'report.json'
    path.write_text(json.dumps(value, indent=2) + '\n')
    digest = sha(path)
    result = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    need(result.returncode == 0 and sha(path) == digest, 'Lossless report compression')
    print(json.dumps({k: v for k, v in value.items() if k not in ('inputHashes', 'cases', 'originalAssets')}, indent=2), flush=True)
    raise SystemExit(0 if value['passed'] else 1)
