"""Actual3172 native Tomb held scene and global palette/reset nonmatch path.

Cold physical controls/earned wins only. Full consecutive RGB frames compared
in RAM to retained1836 source-bound native raster/shadow/erase reference.
No new PNG/WAV/VRAM/executable/ROM copies. This is not all stage audio, the
random-drop branch, all slots/arenas/victims, hidden VRAM, or full acceptance.
"""
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
import map_current_native_feature_coverage_v3590 as inventory
import native_stage_variant_checks_v1731 as native

ROOT, need, sha = inventory.ROOT, inventory.need, inventory.sha
NAME = inventory.NAME
OUT = ROOT / 'audit_v3603_current_tomb_palette_pixels_checked'
CASE = ROOT / 'audit_v3598_current_kano_tomb_p1_palette_pixels'
REFERENCE = ROOT / 'audit_v2069_current_kano_p1_tomb_fullscene'
OLD_REPORT = ROOT / 'audit_v2080_current_kano_p1_tomb_matrix_checked/report.json'
LINEAGE = ROOT / 'audit_v3538_current_natural_ending_photo_full_scope_checkpoint/checkpoint.json'
LUA = ('mk2ks_current_stage_ram_driver_v3594.lua',
       'mk2ks_current_stage_provenance_v3595.lua',
       'mk2ks_current_stage_palette_pixels_v3596.lua')


def classic(log):
    return '\n'.join(line for line in log.splitlines()
                     if line.startswith('MK2_STAGE_') and not line.startswith(('MK2_STAGE_PROVENANCE_', 'MK2_STAGE_TRANSFER_')))


def tagged(log, tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in log.splitlines()
            if line.startswith('MK2_STAGE_TRANSFER_' + tag + ' ')]


def equal_state(entry, resumed):
    need(entry['serial'] == resumed['serial'] and entry['regs'] == resumed['regs'] and
         resumed['exact'] == '1', 'Exact actual native status/SP/A0-A14 pass-through')
    words = entry['regs'].split(',')
    need(len(words) == 17 and all(re.fullmatch('[0-9A-F]{8}', word) for word in words),
         'Complete actual status, stack and all caller registers')


def controls():
    source = (ROOT / 'mk2ks_native_stage_performer_v806.lua').read_text()
    for omission in ("    screen:snapshot('selection_match'..(match+1)..'_p'..n..'.png')\n",
                     " if age<=600 and age%20==0 then screen:snapshot('stage_age'..age..'.png')end\n"):
        need(source.count(omission) == 1, 'Only named read-only PNG calls omitted')
        source = source.replace(omission, '')
    need(source == (ROOT / LUA[0]).read_text(), 'Entire original physical controller byte-exact otherwise')
    source = (ROOT / 'mk2ks_stage_branch_provenance_v1722.lua').read_text()
    need(source.count('mk2ks_native_stage_performer_v806.lua') == 1 and
         source.replace('mk2ks_native_stage_performer_v806.lua', LUA[0]).rstrip('\n') == (ROOT / LUA[1]).read_text().rstrip('\n'),
         'Entire original read-only branch/motion observer retained')
    for file in LUA:
        source = (ROOT / file).read_text()
        need(not re.search(r':write_|write_u\d+|load_?state|\.value\s*=(?!=)', source), 'No guest/register injection')
        if file != LUA[0]:
            need(not re.search(r'set_value|clear_value|snapshot\(', source), 'Read-only observer, no disk raster output')


def run():
    need(not OUT.exists() and not CASE.exists(), 'Fresh immutable current capture/report')
    controls()
    guest, _, payload, _, _ = inventory.current.expected_current()
    lineage = json.loads(LINEAGE.read_text())
    need(sha(OLD_REPORT) == lineage['inputHashes'][str(OLD_REPORT)], 'Retained already-pinned native source-perfect reference')
    old = json.loads(OLD_REPORT.read_text())
    need(old['passed'] and old['candidate'] == 'diagnostic_v1836_ball_register_boundary' and
         old['sampledFrames'] == 537 and old['nativeTombBranch']['dropped'] is False and
         not old['fullPortAcceptance'], 'Bounded full held scene, not universal audio or drop gate')
    old_log = (REFERENCE / 'run.log').read_text(encoding='utf-8-sig')
    need(sha(REFERENCE / 'run.log') == old['inputHashes'][str(REFERENCE / 'run.log')], 'Exact native reference trajectory')
    refs = [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in old_log.splitlines()
            if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP ')]
    need([int(row['frame']) for row in refs] == list(range(8174, 8711)), 'Every held-scene field through native pointer teardown plus30')
    candidate = ROOT / NAME
    build = json.loads((candidate / 'build-info.json').read_text(encoding='utf-8-sig'))
    files = {Path(p) for p in build['input_hashes']} | {
        candidate / 'build-info.json', candidate / 'mkport_candidate.exe', candidate / 'roms/mk2ks/mk2ks.mdata',
        Path(__file__).resolve(), OLD_REPORT, LINEAGE, REFERENCE / 'run.log',
        ROOT / 'mk2ks_native_stage_performer_v806.lua', ROOT / 'mk2ks_stage_branch_provenance_v1722.lua',
        ROOT / 'audit_v3591_current_native_feature_coverage/report.json',
        ROOT / 'tools/run_current_stage_palette_pixels_v3597.py',
        ROOT / 'audit_v3599_current_tomb_palette_pixels_checked/report.json',
        ROOT / 'mame-mkp/src/emu/video.cpp', ROOT / 'mame-mkp/src/frontend/mame/luaengine.cpp',
        *[ROOT / name for name in LUA]}
    for directory in ('roms/mk2ks', 'samples/mk2ks', 'artwork'):
        files.update((ROOT / directory).glob('*'))
    files = {p.resolve() for p in files if p.is_file()}
    before = {str(p): sha(p) for p in files}
    need(all(before[str(Path(p).resolve())] == wanted for p, wanted in build['input_hashes'].items()) and
         before[str(candidate / 'mkport_candidate.exe')] == inventory.current.current.EXE and
         (candidate / 'roms/mk2ks/mk2ks.mdata').read_bytes() == payload, 'Actual current matched pair and every manifest input')
    CASE.mkdir()
    compressed = subprocess.run(['compact.exe', '/C', '/I', '/Q', '/S:' + str(CASE)], capture_output=True, text=True)
    need(compressed.returncode == 0, 'Fresh small capture inherits NTFS compression')
    snapshots = {}
    for source in [Path(__file__).resolve(), *[ROOT / file for file in LUA],
                   ROOT / 'mk2ks_native_stage_performer_v806.lua', ROOT / 'mk2ks_stage_branch_provenance_v1722.lua']:
        source = source.resolve()
        target = CASE / 'input_sources/tree' / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        need(sha(target) == before[str(source)], 'Exact executed source snapshot')
        snapshots[str(source)] = str(target)
    (CASE / 'input_hashes_before.json').write_text(json.dumps(before, indent=2) + '\n')
    (CASE / 'source_snapshot_paths.json').write_text(json.dumps(snapshots, indent=2) + '\n')
    env = {k: v for k, v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)', k)}
    env.update(MK2KS_STAGE_SIDE='1', MK2KS_STAGE_WINNER='kano', MK2KS_STAGE_ARENA='1',
               MK2KS_STAGE_CASE='positive', MK2KS_STAGE_OUT=str(CASE))
    command = [str(candidate / 'mkport_candidate.exe'), 'mk2ks', '-rompath', str(candidate / 'roms') + ';' + str(ROOT / 'roms'),
        '-samplepath', str(ROOT / 'samples'), '-samples', '-artpath', str(ROOT / 'artwork'), '-skip_gameinfo', '-nocheat',
        '-inipath', str(CASE), '-video', 'none', '-sound', 'none', '-samplerate', '48000', '-noautoframeskip',
        '-frameskip', '0', '-nothrottle', '-str', '900', '-snapsize', '400x254', '-cfg_directory', str(CASE / 'cfg'),
        '-nvram_directory', str(CASE / 'nvram'), '-snapshot_directory', str(CASE / 'snap'), '-autoboot_script', str(ROOT / LUA[2])]
    verified, mismatches, protocol_errors, pixel_faults = [], [], [], []
    pins = dict(before)
    with (CASE / 'stderr.log').open('wb') as errors, subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=errors) as process:
        print(f'current held Tomb: native PID={process.pid}; no new image/audio/ROM copies', flush=True)
        with (CASE / 'run.log').open('w', encoding='utf-8') as log:
            for line in iter(process.stdout.readline, b''):
                if line.startswith(b'MK2_STAGE_TRANSFER_PIXELS '):
                    header = line.decode('ascii').strip()
                    fields = dict(re.findall(r'(\w+)=([^\s]+)', header))
                    encoded = process.stdout.readline().strip()
                    try:
                        need(len(verified) < len(refs) and len(encoded) == int(fields['bytes']) * 2 == 400 * 254 * 8 and
                             int(fields['frame']) == 8174 + len(verified) and fields['encoding'] == 'u32le_as_hex_numeric',
                             'Complete consecutive actual snapshot-rendered RGB field')
                        words = np.frombuffer(bytes.fromhex(encoded.decode('ascii')), dtype='>u4').reshape(254, 400)
                        actual = np.stack([(words >> shift) & 255 for shift in (16, 8, 0)], axis=2).astype(np.uint8)
                        reference = REFERENCE / 'snap' / refs[len(verified)]['file']
                        wanted = old['inputHashes'][str(reference)]
                        need(sha(reference) == wanted, 'Exact source-bound original visible PNG')
                        pins[str(reference)] = wanted
                        expected = np.asarray(Image.open(reference).convert('RGB'))
                        diff = int(np.count_nonzero(np.any(actual != expected, axis=2)))
                        if diff:
                            mismatches.append(dict(frame=int(fields['frame']), pixels=diff,
                                                   firstYX=np.argwhere(np.any(actual != expected, axis=2))[0].tolist()))
                        elif not pixel_faults:
                            for label, pos in (('full-visible pixel', (0, 0)), ('native floor band', (235, 150)), ('lifebar', (30, 35))):
                                changed = actual.copy(); changed[pos][0] ^= 1
                                need(not np.array_equal(changed, expected), 'Actual qualified one-pixel fault rejected')
                                pixel_faults.append(dict(label=label, positionYX=list(pos), beforeRGB=actual[pos].tolist(),
                                                         afterRGB=changed[pos].tolist(), rejected=True))
                        row = dict(frame=int(fields['frame']), currentRGB_SHA256=hashlib.sha256(actual.tobytes()).hexdigest().upper(),
                                   referenceRGB_SHA256=hashlib.sha256(expected.tobytes()).hexdigest().upper(), referencePNG=str(reference),
                                   referencePNG_SHA256=wanted, exactPixels=101600 - diff)
                        verified.append(row)
                        log.write('MK2_STAGE_TRANSFER_CHECKED ' + ' '.join(f'{k}={v}' for k, v in row.items() if k != 'referencePNG') + '\n')
                        if len(verified) % 150 == 0:
                            print(f'held Tomb: {len(verified)}/537 actual fields, mismatches={len(mismatches)}', flush=True)
                    except Exception as error:
                        # Consume the same live native process to terminal; never restart
                        # because an observation fails, and never save raw RGB payloads.
                        protocol_errors.append(dict(header=header, error=repr(error)))
                else:
                    need(not re.search(b'^[A-F0-9]{1000}', line), 'Raw RGB never enters disk logs')
                    log.write(line.decode('utf-8', errors='strict'))
        code = process.wait()
    log = (CASE / 'run.log').read_text()
    result = dict(exit_code=code, candidate=NAME, executable_sha256=build['executable_sha256'],
                  payload_sha256=build['payload_sha256'], winner='kano', side=1, arena=1,
                  physicalInputsOnly=True, guestWrites=0, assistance='none', cheats_enabled=False,
                  actualVisibleFields=len(verified), mismatches=mismatches, protocolErrors=protocol_errors,
                  rawPixelImageVRAMAudioOrPlayableCopiesWritten=0, passed=False, fullPortAcceptance=False)
    (CASE / 'visible_frames.json').write_text(json.dumps(verified, indent=2) + '\n')
    (CASE / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    need(code == 0 and not re.search(r'LUA ERROR|Lua error|stack traceback|Fatal error|access violation',
                                    log + (CASE / 'stderr.log').read_text(), re.I), 'Native terminal and observer success')
    need(not protocol_errors and not mismatches and len(verified) == 537 and len(pixel_faults) == 3,
         'All full visible held-scene fields exactly source-reference matched')
    need((CASE / 'guest_maincpu.bin').read_bytes() == guest, 'Whole actual initialized current guest independently source-bound')
    need(classic(log) == classic(old_log), 'Entire original input/health/damage/pose/mode/native cleanup trajectory unchanged')
    old_provenance = [line for line in old_log.splitlines() if line.startswith('MK2_STAGE_PROVENANCE_')]
    need([line for line in log.splitlines() if line.startswith('MK2_STAGE_PROVENANCE_')] == old_provenance,
         'Actual original random branch, velocity/gravity, physical owner and native stores exactly retained')
    gameplay = native.check_log(classic(log), 'kano', 1, 1, 'positive', certified_drop_log=classic(old_log))
    begin, retired, terminal = tagged(log, 'BEGIN'), tagged(log, 'RETIRED'), tagged(log, 'RESULT')
    need(len(begin) == len(retired) == len(terminal) == 1 and int(begin[0]['origin']) == 8173 and
         int(retired[0]['retired']) == 8680 and retired[0]['mode'] == '3' and terminal[0]['pixels'] == '537',
         'Actual native actor teardown and complete next-screen plus30fields')
    alloc, resumed = tagged(log, 'ALLOC_ENTRY'), tagged(log, 'ALLOC_RESUME')
    reset, restored = tagged(log, 'RESET_ENTRY'), tagged(log, 'RESET_RESUME')
    need(len(alloc) == len(resumed) == int(terminal[0]['allocations']) > 0 and
         len(reset) == len(restored) == int(terminal[0]['resets']) > 0 and
         terminal[0]['matching_allocations'] == terminal[0]['matching_sprites'] == '0',
         'Real nonmatching palette requests and reset traversal observed, not vacuous')
    for entry, resume in [*zip(alloc, resumed), *zip(reset, restored)]:
        equal_state(entry, resume)
    need(all(row['request'] != 'FECDF710' for row in alloc) and all(row['eligible'] == '0' for row in reset),
         'No typed bubble palette/action path entered')
    register_faults = []
    for label, pair in (('palette caller state', (alloc[0], resumed[0])), ('reset caller state', (reset[0], restored[0]))):
        entry, resume = pair; changed = dict(resume)
        words = changed['regs'].split(','); words[0] = f'{int(words[0],16)^1:08X}'; changed['regs'] = ','.join(words)
        try:
            equal_state(entry, changed)
        except ValueError as error:
            register_faults.append(dict(label=label, beforeST=entry['regs'].split(',')[0],
                                        afterST=words[0], rejectedBy=str(error)))
        else:
            raise ValueError('Changed actual native hook caller state accepted')
        equal_state(entry, resume)
    for file, wanted in before.items():
        need(sha(file) == wanted, 'Actual executed input unchanged')
    result.update(passed=True, nativeScene=gameplay, exactCurrentVisibleRGBPixels=537 * 101600,
                  fullOriginalPhysicalAndBranchRecordsUnchanged=True,
                  actualNonmatchingPaletteRequests=len(alloc), actualNonmatchingNativeResets=len(reset),
                  actualCompleteRegisterStatePairs=len(alloc) + len(reset),
                  qualifiedPixelFaults=pixel_faults, qualifiedRegisterFaults=register_faults)
    (CASE / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    for path in CASE.rglob('*'):
        if path.is_file(): pins[str(path)] = sha(path)
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file and Path(file).suffix == '.py' and Path(file).resolve().is_relative_to(ROOT / 'tools'):
            pins[str(Path(file).resolve())] = sha(file)
    return dict(passed=True, candidate=NAME, currentHeldTombFullVisibleSceneAndNativeHookNonmatchAccepted=True,
                case=result, actualCurrentVisibleFields=537, exactActualCurrentVisibleRGBPixels=54559200,
                actualQualifiedPixelAndRegisterFaults=5, sourceBoundReferenceBuild='diagnostic_v1836_ball_register_boundary',
                historicalUnderlyingVRAMAudioGraphRevalidated=False, currentHiddenVRAMWriteReplayAccepted=False,
                nativeDropBranchOtherSlotsVictimsStagesAndAudioAccepted=False,
                newExecutableROMWAVOrRawPixelImageCopies=0, gameOrPublicBytesChanged=False,
                rejectedPreCaptureVerifierReport=str(ROOT / 'audit_v3599_current_tomb_palette_pixels_checked/report.json'),
                preCaptureVerifierFailure='Trailing blank-line-only copy normalization; no capture was started',
                fullPortAcceptance=False, scope=__doc__, inputHashes=pins)


if __name__ == '__main__':
    need(not OUT.exists(), 'Immutable current report')
    try:
        report = run()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), fullPortAcceptance=False)
    OUT.mkdir()
    saved = OUT / 'report.json'; saved.write_text(json.dumps(report, indent=2) + '\n')
    before = sha(saved)
    compressed = subprocess.run(['compact.exe', '/C', '/I', '/Q', str(saved)], capture_output=True, text=True)
    need(compressed.returncode == 0 and sha(saved) == before, 'Lossless compact report')
    print(json.dumps({k: v for k, v in report.items() if k not in ('case','inputHashes')}, indent=2), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
