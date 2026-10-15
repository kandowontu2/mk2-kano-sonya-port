"""Current3172 Friendship visible-scene transfer, full1600fields/both slots.

Compare actual screen pixels, not inferred descriptors or matching state
alone. Prior2753 complete source-bound raster/shadow/erase reference remains
immutable. Only reference PNGs needed for this comparison are revalidated;
no historical raw audio/VRAM graph recreation. Current pixels are streamed
and discarded after exact comparison, with digests retained. This accepts
these visible cross-character scenes, not current hidden VRAM writes,
absolute all-arena shadows, mirror/CPU/other-victim contexts or full port.
"""
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import traceback
from pathlib import Path
import numpy as np
from PIL import Image
import run_current_friendship_ram_audio_v3561 as audio

ROOT, need, sha = audio.ROOT, audio.need, audio.sha
CANDIDATE = audio.collector.CANDIDATE
OUT = ROOT / 'audit_v3576_current_friendship_snapshot_pixels_checked'
SHADOW = ROOT / 'audit_v2783_native_friendship_palette_shadow_rows_checked/report.json'
LUA = ['mk2ks_current_friendship_stream_probe_v3566.lua',
       'mk2ks_current_friendship_stream_audio_v3567.lua',
       'mk2ks_current_friendship_stream_wins_v3568.lua',
       'mk2ks_current_friendship_snapshot_pixels_v3573.lua']
EXPECTED = None


def control_source():
    original = (ROOT / 'mk2ks_native_friendship_probe_v788.lua').read_text()
    for before in (";screen:snapshot('selection_p'..n..'.png')",
                   "  if action_age>=40 and action_age<=198 then screen:snapshot('native_field_'..action_age..'.png')end\n",
                   "  screen:snapshot('friendship_'..age..'.png')\n"):
        need(original.count(before) == 1, 'Exactly declared read-only snapshot omission')
        original = original.replace(before, '')
    need((ROOT / LUA[0]).read_text() == original, 'Whole original extended physical controller retained')
    for old, new, before, after in (
        ('mk2ks_current_friendship_extended_audio_v2687.lua', LUA[1],
         'mk2ks_native_friendship_probe_v788.lua', LUA[0]),
        ('mk2ks_current_friendship_extended_wins_v2688.lua', LUA[2],
         'mk2ks_current_friendship_extended_audio_v2687.lua', LUA[1]),
    ):
        source = (ROOT / old).read_text()
        need(source.count(before) == 1 and (ROOT / new).read_text() == source.replace(before, after),
             'Only declared observer-chain adaptation')
    for name in LUA:
        need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)', (ROOT / name).read_text()),
             'No guest/register/state injection')
    observer = (ROOT / LUA[3]).read_text()
    need(observer.count("dofile('" + LUA[2] + "')") == 1 and
         not re.search(r'set_value|clear_value', observer), 'Read-only pixel observer cannot alter controls')


def reference(fighter, side):
    older = ROOT / 'audit_v3538_current_natural_ending_photo_full_scope_checkpoint/checkpoint.json'
    older_state = json.loads(older.read_text())
    need(sha(SHADOW) == older_state['inputHashes'][str(SHADOW)], 'Already-pinned source-perfect reference lineage')
    shadow = json.loads(SHADOW.read_text())
    key = f'{fighter}_p{side}'
    need(shadow['passed'] and shadow['sourceDerivedNativeShadowRowsAndBlackPenAccepted'] and
         shadow['cases'][key]['sourcePerfectScanouts'] == 1600 and
         shadow['cases'][key]['exactContinuousErasurePasses'] == 1537 and
         not shadow['fullPortAcceptance'], 'Original complete source-bound visible reference only')
    folder = ROOT / (f'audit_v2756_native_kano_friendship_palette_p{side}' if fighter == 'kano'
                     else f'audit_v2760_native_sonya_friendship_palette_p{side}')
    frames, window = [], None
    with (folder / 'run.log').open(encoding='utf-8-sig') as log:
        for line in log:
            if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP '):
                frames.append(dict(re.findall(r'(\w+)=([^\s]+)', line)))
            elif line.startswith('MK2_NAT_CAMPAIGN_FLOOR_WINDOW '):
                row = dict(re.findall(r'(\w+)=([^\s]+)', line))
                need(window is None, 'One source reference finish window')
                window = int(row['window'])
    need(len(frames) == 1600 and [int(r['frame']) for r in frames] == list(range(window + 1, window + 1601)),
         'Every original reference field, no gaps or sparse sampling')
    pins = {str(SHADOW): sha(SHADOW), str(older): sha(older)}
    oldlog = folder / 'run.log'
    need(sha(oldlog) == shadow['inputHashes'][str(oldlog)], 'Exact source-bound physical reference log')
    pins[str(oldlog)] = sha(oldlog)
    for row in frames:
        path = folder / 'snap' / row['file']
        row['path'] = str(path)
        row['wanted'] = shadow['inputHashes'][str(path)]
    return folder, window, frames, pins


def rgb_equal(actual, expected):
    need(actual.shape == expected.shape == (254, 400, 3) and np.array_equal(actual, expected),
         'Every actual current visible RGB pixel equals source-verified original scene')


def pixel_faults(actual, expected):
    faults = []
    yellow = np.argwhere((actual[25:39, :, 0] > 150) &
                         (actual[25:39, :, 1] > 150) & (actual[25:39, :, 2] < 60))
    need(len(yellow), 'Actual highlighted name pixels exist for qualified corruption')
    y, x = yellow[0]
    for name, pos in (('one_actual_visible_pixel_changed', (0, 0)),
                      ('one_actual_lifebar_name_pixel_changed', (int(y) + 25, int(x))),
                      ('one_actual_ground_band_pixel_changed', (235, 150))):
        changed = actual.copy()
        changed[pos][0] ^= 1
        need(not np.array_equal(changed, actual), 'Qualified actual pixel corruption is nonvacuous')
        try:
            rgb_equal(changed, expected)
        except ValueError as error:
            need('Every actual current visible RGB pixel' in str(error), 'Intended exact visible-pixel rejection')
            faults.append(dict(name=name, positionYX=list(pos), beforeRGB=actual[pos].tolist(), rejectedBy=str(error)))
        else:
            raise ValueError('Corrupt actual scene pixel accepted')
    rgb_equal(actual, expected)
    return faults


def capture(case):
    fighter, side = case
    reference_folder, window, refs, pins = reference(fighter, side)
    folder = ROOT / f'audit_v3575_current_{fighter}_friendship_visible_p{side}'
    need(not folder.exists(), 'Fresh immutable current visible capture; never restart into old output')
    candidate = ROOT / CANDIDATE
    build = json.loads((candidate / 'build-info.json').read_text(encoding='utf-8-sig'))
    files = set(map(Path, build['input_hashes'])) | {candidate / 'build-info.json', candidate / 'mkport_candidate.exe',
        candidate / 'roms/mk2ks/mk2ks.mdata', Path(__file__).resolve(), *[ROOT / n for n in LUA],
        ROOT / 'mk2ks_native_friendship_probe_v788.lua', ROOT / 'mk2ks_current_friendship_extended_audio_v2687.lua',
        ROOT / 'mk2ks_current_friendship_extended_wins_v2688.lua', ROOT / 'mame-mkp/src/frontend/mame/luaengine.cpp',
        ROOT / 'mame-mkp/src/emu/screen.cpp', ROOT / 'mame-mkp/src/emu/video.cpp',
        ROOT / 'mk2/mk2-maincpu.bin', ROOT / 'mk3/mk3-maincpu.bin'}
    for relative in ('roms/mk2ks', 'samples/mk2ks', 'artwork'):
        files.update((ROOT / relative).glob('*'))
    files = {p.resolve() for p in files if p.is_file()}
    before = {str(p): sha(p) for p in files}
    need(all(before[str(Path(p).resolve())] == digest for p, digest in build['input_hashes'].items()) and
         before[str((candidate / 'mkport_candidate.exe').resolve())] == audio.collector.state.prior.current.current.EXE and
         before[str((candidate / 'roms/mk2ks/mk2ks.mdata').resolve())] == audio.collector.state.prior.current.current.PAYLOAD,
         'Matched actual executable/payload and every compiled input')
    folder.mkdir()
    compact = subprocess.run(['compact.exe', '/C', '/I', '/Q', '/S:' + str(folder)], capture_output=True, text=True)
    need(compact.returncode == 0, 'Fresh capture inherits lossless compression')
    snapshots = {}
    for path in files:
        need(path.is_relative_to(ROOT), 'Workspace evidence inputs only')
        if path.suffix in ('.lua', '.ps1', '.py', '.json'):
            destination = folder / 'input_sources/tree' / path.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
            need(sha(destination) == before[str(path)], 'Exact collision-free hierarchical source snapshot')
            snapshots[str(path)] = str(destination)
    (folder / 'input_hashes_before.json').write_text(json.dumps(before, indent=2) + '\n')
    (folder / 'source_snapshot_paths.json').write_text(json.dumps(snapshots, indent=2) + '\n')
    env = {k: v for k, v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)', k)}
    env.update(MK2KS_FRIEND_WINNER=fighter, MK2KS_FRIEND_SIDE=str(side), MK2KS_FRIEND_CASE='positive',
               MK2KS_FRIEND_OUT=str(folder), MK2KS_FRIEND_GAP='160', MK2KS_FRIEND_OBSERVATION='1600')
    command = [str(candidate / 'mkport_candidate.exe'), 'mk2ks', '-rompath', str(candidate / 'roms') + ';' + str(ROOT / 'roms'),
        '-samplepath', str(ROOT / 'samples'), '-samples', '-artpath', str(ROOT / 'artwork'), '-skip_gameinfo', '-nocheat',
        '-inipath', str(folder), '-video', 'none', '-sound', 'none', '-samplerate', '48000', '-noautoframeskip',
        '-frameskip', '0', '-nothrottle', '-str', '180', '-snapsize', '400x254', '-cfg_directory', str(folder / 'cfg'),
        '-nvram_directory', str(folder / 'nvram'), '-snapshot_directory', str(folder / 'snap'),
        '-autoboot_script', str(ROOT / LUA[3])]
    verified, mismatches, faults = [], [], []
    with (folder / 'stderr.log').open('wb') as errors, subprocess.Popen(command, cwd=ROOT, env=env,
            stdout=subprocess.PIPE, stderr=errors) as process:
        with (folder / 'run.log').open('w', encoding='utf-8') as log:
            for line in iter(process.stdout.readline, b''):
                if line.startswith(b'MK2_FSTREAM_PIXELS '):
                    header = line.decode('ascii').strip()
                    fields = dict(re.findall(r'(\w+)=([^\s]+)', header))
                    encoded = process.stdout.readline().strip()
                    need(len(encoded) == int(fields['bytes']) * 2 == 400 * 254 * 8 and
                         fields['encoding'] == 'u32le_as_hex_numeric' and
                         int(fields['width']) == 400 and int(fields['height']) == 254 and
                         int(fields['frame']) == window + len(verified) + 1 and fields['writes'] == '0',
                         'Complete actual read-only RGB word payload and consecutive native field framing')
                    raw = bytes.fromhex(encoded.decode('ascii'))
                    words = np.frombuffer(raw, dtype='>u4').reshape(254, 400)
                    actual = np.stack([(words >> shift) & 255 for shift in (16, 8, 0)], axis=2).astype(np.uint8)
                    ref = refs[len(verified)]
                    ref_path = Path(ref['path'])
                    need(sha(ref_path) == ref['wanted'], 'Exact retained source-verified PNG bytes')
                    pins[str(ref_path)] = ref['wanted']
                    expected = np.asarray(Image.open(ref_path).convert('RGB'))
                    differing = int(np.count_nonzero(np.any(actual != expected, axis=2)))
                    if differing:
                        mismatches.append(dict(frame=int(fields['frame']), pixels=differing,
                            firstYX=np.argwhere(np.any(actual != expected, axis=2))[0].tolist()))
                    elif not faults:
                        faults = pixel_faults(actual, expected)
                    row = dict(frame=int(fields['frame']), referencePNG=str(ref_path),
                        referencePNG_SHA256=ref['wanted'], currentRGB_SHA256=hashlib.sha256(actual.tobytes()).hexdigest().upper(),
                        referenceRGB_SHA256=hashlib.sha256(expected.tobytes()).hexdigest().upper(),
                        exactPixels=400 * 254 - differing)
                    verified.append(row)
                    log.write('MK2_FSTREAM_CHECKED ' + ' '.join(f'{k}={v}' for k, v in row.items() if k != 'referencePNG') + '\n')
                    if len(verified) % 400 == 0:
                        print(f'{fighter}_p{side}: {len(verified)}/1600 actual visible fields, mismatching fields={len(mismatches)}', flush=True)
                else:
                    need(not re.search(b'^[A-F0-9]{1000}', line), 'Raw encoded pixels never enter disk logs')
                    log.write(line.decode('utf-8', errors='strict'))
        code = process.wait()
    need(code == 0 and not re.search(r'LUA ERROR|stack traceback|Fatal error|access violation',
        (folder / 'run.log').read_text() + (folder / 'stderr.log').read_text(), re.I), 'Native terminal capture and observer success')
    for path, digest in before.items():
        need(sha(path) == digest, 'Executed inputs unchanged')
    need((folder / 'guest_maincpu.bin').read_bytes() == EXPECTED[0], 'Whole independently assembled actual3172guest')
    rows = audio.scene.previous.parse(folder / 'run.log')
    old_rows = [(tag, row) for tag, row in audio.scene.previous.parse(reference_folder / 'run.log') if not tag.startswith('SHADOW_')]
    need(rows == old_rows, 'Every original physical/native frame/pose/health/owner/WIN/cleanup record retained')
    control = audio.scene.check(rows, fighter, side)
    chronology = audio.native.runtime(rows, fighter, side, 'positive')
    need(len(verified) == 1600 and len(faults) == 3 and not mismatches,
         'All1600current complete visible frames match source-perfect reference, no hidden pixel exclusion')
    (folder / 'visible_frames.json').write_text(json.dumps(verified, indent=2) + '\n')
    result = dict(exit_code=code, candidate=CANDIDATE, winner=fighter, side=side, guest_writes=0, assistance='none',
        cheats_enabled=False, executable_sha256=build['executable_sha256'], payload_sha256=build['payload_sha256'],
        actualCurrentVisibleFrames=1600, exactCurrentVisiblePixels=1600 * 400 * 254,
        currentPixelCounterexamples=faults, nativeScene=control, nativeCueChronology=chronology,
        snapshot_schema=3, rawPixelImageVRAMOrAudioCopiesWritten=0, input_hashes=before,
        passed=True, fullPortAcceptance=False)
    (folder / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    pins.update(before)
    for path in folder.rglob('*'):
        if path.is_file():
            pins[str(path)] = sha(path)
    print(f'{fighter}_p{side}: terminal0, all1600visible frames and native cleanup exact', flush=True)
    return dict(winner=fighter, side=side, capture=folder.name, nativeScene=control,
                actualVisibleFrames=1600, exactVisiblePixels=1600 * 400 * 254,
                currentPixelCounterexamples=faults, samePathOriginalPositive=True), pins


def run():
    global EXPECTED
    need(not OUT.exists(), 'Immutable new current visible transfer proof')
    control_source()
    EXPECTED = audio.current.expected_current()
    need((ROOT / CANDIDATE / 'roms/mk2ks/mk2ks.mdata').read_bytes() == EXPECTED[2], 'Whole independent actual3172payload')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        values = list(pool.map(capture, [(fighter, side) for fighter in ('kano', 'sonya') for side in (1, 2)]))
    cases, pins = [], {}
    for case, inputs in values:
        cases.append(case)
        for path, digest in inputs.items():
            need(path not in pins or pins[path] == digest, 'Consistent source/reference/current capture dependency')
            pins[path] = digest
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file and Path(file).suffix == '.py' and Path(file).resolve().is_relative_to(ROOT / 'tools'):
            pins[str(Path(file).resolve())] = sha(file)
    # Selected references already revalidated while comparing their pixels;
    # no obsolete full historical dependency graph is reread here.
    return dict(passed=True, candidate=CANDIDATE, cases=cases, actualCurrentVisibleFrames=6400,
        exactActualCurrentVisibleRGBPixels=6400 * 400 * 254, actualQualifiedPixelFaults=12,
        currentBothHumanSlotFullVisibleFriendshipSceneAndTransitionAccepted=True,
        completeCurrentHiddenVRAMWriteReplayAccepted=False, allArenaAbsoluteGroundShadowAccepted=False,
        allFriendshipMirrorVictimCPUOrFinisherContextsAccepted=False,
        referenceRawAudioOrVRAMGraphRecreated=False, newExecutableROMWAVOrRawPixelImageCopies=0,
        fullPortAcceptance=False, inputHashes=pins, scope=__doc__)


if __name__ == '__main__':
    try:
        value = run()
    except Exception as error:
        value = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), fullPortAcceptance=False)
    need(not OUT.exists(), 'Never overwrite current visible report')
    OUT.mkdir()
    path = OUT / 'report.json'
    path.write_text(json.dumps(value, indent=2) + '\n')
    digest = sha(path)
    compact = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(path)], capture_output=True, text=True)
    need(compact.returncode == 0 and sha(path) == digest, 'Lossless compact visible report')
    print(json.dumps({k: v for k, v in value.items() if k not in ('inputHashes', 'cases')}, indent=2), flush=True)
    raise SystemExit(0 if value['passed'] else 1)
