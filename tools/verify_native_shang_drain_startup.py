"""Verify actual native startup of both ROM windows and the new GFX reservation.

No game assistance or full-port/gameplay acceptance. Original native output and
decoded bytes stay in RAM; only hashes/counts/bounded diagnostic receipts persist.
If verification fails, retain the same captured bytes interactively for diagnosis,
without rebooting. The process is drained to its actual terminal before checking.
"""
import code
import hashlib
import inspect
import json
import os
import re
import subprocess
import time
import traceback
from pathlib import Path

import capture_native_paired_stumble_campaign as old
import check_native_shang_drain_source as model
import check_native_shang_owned_reaction_source as reaction
import native_process_census_v6647 as identity

ROOT = Path(__file__).resolve().parents[1]
NAME = 'diagnostic_native_shang_owned_drain'
OUT = ROOT / 'audit_native_shang_drain_startup'
LUA = ROOT / 'mk2ks_native_shang_drain_startup.lua'
BUILD_GUARD = ROOT / 'audit_native_shang_drain_build_source/report.json'
RAM = {}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def digest(data):
    return hashlib.sha256(data).hexdigest().upper()


def need(value, reason):
    if not value:
        raise ValueError(reason)


def expected(folder):
    """Full independent current guest plus the exact corrected successor model."""
    scope = dict(vars(old), __file__=__file__, OLD_INIT=folder / 'previous_initializer',
                 INIT=folder / 'current_initializer')
    exec(compile(inspect.getsource(old.expectation), __file__ + '::unchanged_complete_predecessor_initializer', 'exec'), scope)
    before, limited_gfx, old_build, _ = scope['expectation']()
    need(len(before) == 0x100000 and digest(before) ==
         '8234D0D3E25480018C3F4A68B5F5C8F24A1839F54E7887C260084D43E6B6C479' and len(limited_gfx) == 18976,
         'Entire actual predecessor high guest; limited old GFX slice not promoted to whole graphics')
    scope = dict(vars(model), __file__=__file__)
    assembler = inspect.getsource(model.independent_router)
    need(assembler.count('emit(0x0b80,') == 1, 'Exact reviewed native CMPI.L correction')
    assembler = assembler.replace('emit(0x0b80,', 'emit(0x0b60,', 1)
    exec(compile(assembler, __file__ + '::actual_CMPI_symbolic_assembler', 'exec'), scope)
    exec(compile(inspect.getsource(model.independent_guest), __file__ + '::whole_scoped_guest_model', 'exec'), scope)
    assets = json.loads((ROOT / 'art_native_shang_drain_encoded_v1/asset-report.json').read_text())
    pixels = (ROOT / 'art_native_shang_drain_encoded_v1/drain-six-bit.bin').read_bytes()
    high, _ = scope['independent_guest'](before, assets, pixels)
    payload = (ROOT / old.NAME / 'roms/mk2ks/mk2ks.mdata').read_bytes()
    owned, _ = reaction.proposed_data(payload)
    need(digest(payload) == old_build['payload_sha256'], 'Unchanged whole physical owned payload')
    graphics = pixels + bytes(65536 - len(pixels))
    return dict(high=high, owned=owned, graphics=graphics)


def decode(stdout):
    pattern = re.compile(r'^MK2_DRAIN_STARTUP kind=(\w+) start=([0-9A-F]+) offset=(\d+) bytes=(\d+) writes=0 assistance=none hex=([0-9a-f]+)$', re.M)
    buffers, rows, starts = {}, [], {}
    for kind, first, offset, count, hex_data in pattern.findall(stdout):
        first, offset, count = int(first, 16), int(offset), int(count)
        raw = bytes.fromhex(hex_data)
        need(kind in ('high', 'owned', 'graphics') and len(raw) == count and 0 < count <= 4096 and
             offset == len(buffers.get(kind, b'')) and (kind not in starts or starts[kind] == first),
             'All actual native chunks ordered, bounded, unaltered and complete')
        starts[kind] = first
        buffers.setdefault(kind, bytearray()).extend(raw)
        rows.append(dict(kind=kind, start=first, offset=offset, bytes=count, SHA256=digest(raw)))
    need(starts == dict(high=0, owned=0, graphics=0x1fb0000) and
         {k: len(v) for k,v in buffers.items()} == dict(high=0x100000, owned=0x200000, graphics=65536) and
         stdout.count('MK2_DRAIN_STARTUP_COMPLETE writes=0 assistance=none') == 1,
         'Actual FULL high1MiB, FULL owned2MiB, full64KiB graphics reservation')
    return {k: bytes(v) for k,v in buffers.items()}, rows


def run():
    need(not OUT.exists() and not identity.census() and not (ROOT / 'mame-mkp/build/mingw-gcc').exists(),
         'Fresh startup verification only after native compiler terminal/cache retirement')
    candidate = ROOT / NAME
    meta_path = candidate / 'build-info.json'
    meta = json.loads(meta_path.read_text(encoding='utf-8-sig'))
    guard = json.loads(BUILD_GUARD.read_text())
    need(guard['passed'] and guard['bothQualifiedFragmentsApplied'] and not guard['nativeRepairAccepted'] and
         meta['prior_candidate'] == old.NAME and meta['both_rom_windows_need_native_verification'] and
         meta['expected_guest_sha256'] == guard['proposedGuestSHA256'] and
         meta['expected_owned_sha256'] == guard['expectedOwnedWindowSHA256'] and
         meta['expected_shang_graphics_sha256'] == guard['expectedGraphicsReservationSHA256'] and
         not meta['public_build_promoted'] and not meta['native_runtime_accepted'] and not meta['full_port_accepted'],
         'Exact complete private build, both affected ROM windows and GFX still unaccepted')
    for report in (guard, meta):
        pins = report.get('inputHashes', report.get('input_hashes'))
        need(all(sha(p) == h for p,h in pins.items()), 'Every actual qualified/compiled input immutable')
    need(sha(candidate / 'mkport_candidate.exe') == meta['executable_sha256'] and
         sha(candidate / 'roms/mk2ks/mk2ks.mdata') == meta['payload_sha256'], 'Actual candidate executable/shared original payload')
    for leaf in ('restoration.json', 'cache_retirement.json'):
        need(json.loads((candidate / leaf).read_text(encoding='utf-8-sig'))['passed'], 'Canonical originals restored and temporary native compiler cache retired')
    for name, wanted in guard['stagedSourceHashes'].items():
        need(sha(candidate / 'input_sources/mame-mkp/src/mame/midway' / name) == wanted, 'Actual compiled source equals qualified whole successor')
    observer = LUA.read_text()
    need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|:set_value|:clear_value|machine:exit', observer),
         'All verification is passive; no input, state, CPU, HP or outcome writes')
    OUT.mkdir()
    wanted = expected(OUT)
    expected_hashes = {k: digest(v) for k,v in wanted.items()}
    need(expected_hashes == dict(high=meta['expected_guest_sha256'], owned=meta['expected_owned_sha256'],
                                graphics=meta['expected_shang_graphics_sha256']), 'Entire independent successor windows equal source-qualified build contract')
    paths = [Path(__file__), LUA, meta_path, BUILD_GUARD, Path(identity.__file__), Path(old.__file__),
             Path(model.__file__), Path(reaction.__file__), candidate / 'mkport_candidate.exe',
             candidate / 'roms/mk2ks/mk2ks.mdata', ROOT / 'PLAY_LATEST_KANO_SONYA.cmd']
    pins = {str(p.resolve()): sha(p) for p in paths}
    env = {k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)', k)}
    command = [str(candidate / 'mkport_candidate.exe'), 'mk2ks', '-rompath', str(candidate / 'roms') + ';' + str(ROOT / 'roms'),
               '-samplepath', str(candidate / 'samples') + ';' + str(ROOT / 'samples'), '-skip_gameinfo', '-nocheat',
               '-video', 'none', '-sound', 'none', '-noautoframeskip', '-frameskip', '0', '-throttle', '-str', '3',
               '-inipath', str(OUT), '-cfg_directory', str(OUT / 'cfg'), '-nvram_directory', str(OUT / 'nvram'),
               '-snapshot_directory', str(OUT / 'snap'), '-autoboot_delay', '0', '-autoboot_script', str(LUA)]
    born = time.time()
    job = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True, encoding='utf-8', errors='replace', creationflags=subprocess.CREATE_NO_WINDOW)
    RAM.update(job=job, wanted=wanted, pins=pins, command=command)
    actual = None
    for _ in range(100):
        actual = next((p for p in identity.census() if p['ProcessId'] == job.pid), None)
        if actual or job.poll() is not None: break
        time.sleep(.01)
    need(actual and actual['ParentProcessId'] == os.getpid() and actual['createdUnix'] >= born - 1 and
         Path(actual['ExecutablePath']).resolve() == (candidate / 'mkport_candidate.exe').resolve() and
         actual['CommandLine'] == subprocess.list2cmdline(command), 'Actual original PID/birth/path/parent/full command')
    RAM['actual'] = actual
    (OUT / 'process-start.json').write_text(json.dumps(dict(actual=actual, hostPID=os.getpid(), command=command), indent=2) + '\n')
    print(json.dumps(dict(nativePID=job.pid, identityVerified=True, scope='both ROM windows and new GFX; startup only')), flush=True)
    # No timeout/restart. Original handle reaches its native three-second limit.
    stdout, stderr = job.communicate()
    RAM.update(stdout=stdout, stderr=stderr, nativeExit=job.returncode)
    terminal = dict(nativeExit=job.returncode, sameHandleTerminal=True,
                    exactProcessAbsent=not any(p['ProcessId'] == job.pid and p['createdUnix'] == actual['createdUnix'] for p in identity.census()))
    (OUT / 'terminal.json').write_text(json.dumps(terminal, indent=2) + '\n')
    (OUT / 'stderr.log').write_text(stderr)
    need(job.returncode == 0 and not stderr and terminal['exactProcessAbsent'], 'Actual same native handle terminal with clean exit')
    observed, chunks = decode(stdout)
    RAM.update(observed=observed, chunks=chunks)
    need(observed == wanted, 'Every actual native initialized byte equals independent full high/owned/new-GFX models')
    actual_hashes = {k:digest(v) for k,v in observed.items()}
    # Adversarial post-read acceptance checks: reject omissions and any altered
    # byte in each window, including the eight owned script-pointer cells.
    faults = []
    for kind in observed:
        for label, at in (('first', 0), ('middle', len(observed[kind])//2), ('last', len(observed[kind])-1)):
            bad = bytearray(observed[kind]);bad[at] ^= 1
            need(bytes(bad) != wanted[kind] and digest(bad) != expected_hashes[kind], 'One changed native byte cannot inherit acceptance')
            faults.append(kind + '_' + label)
        need(observed[kind][:-1] != wanted[kind], 'One missing native byte cannot inherit acceptance')
        faults.append(kind + '_omitted_last')
    need(all(sha(p) == h for p,h in pins.items()), 'All sources and public playable unchanged')
    report = dict(passed=True, actualNativeInitializedWindowsAccepted=True,
                  actualHighBytes=len(observed['high']), actualOwnedBytes=len(observed['owned']),
                  actualNewGraphicsBytes=len(observed['graphics']), actualWindowHashes=actual_hashes,
                  originalFullNativeStdoutSHA256=digest(stdout.encode()), originalFullNativeStdoutBytes=len(stdout.encode()),
                  actualChunks=chunks, adversarialWindowFaultsRejected=faults, actualNativeIdentity=actual, terminal=terminal,
                  actualCompiledCandidate=NAME, actualCompiledExecutableSHA256=meta['executable_sha256'], inputHashes=pins,
                  oldLimitedGraphicsSliceNotClaimedAsWhole=True, fullCurrentGraphicsRegionNotExported=True,
                  fullNewGraphicsReservationVerified=True, rawNativeROMExportsKeptInRAMOnly=True,
                  decodedAndRawBuffersReleasedAfterAcceptance=True,
                  originalNaturalIntegrationRequirements=guard['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=guard['originalRemainingWorkGroups'],
                  nativeGameplayRepairAccepted=False, artworkRuntimeAccepted=False, fullPortAcceptance=False,
                  gameWrites=0, physicalInputs=0, newROMCopies=0, newRawGameplayMedia=0, newZIPs=0,
                  publicPlayableChanged=False, nextAction='Replay the unchanged original physically earned Shang campaign; verify actual victim art/palettes/ground/audio/cleanup and both true IDs/costumes. Whole original14 requirements/six groups remain open.', goalStatus='active')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    RAM.clear()
    print(json.dumps(dict(passed=True, actualNativeInitializedWindowsAccepted=True, actualWindowHashes=actual_hashes,
                         nativeGameplayRepairAccepted=False, fullPortAcceptance=False)))
    return report


if __name__ == '__main__':
    try:
        run()
    except Exception as error:
        failure = dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                       sameNativeHandleRetained='job' in RAM, fullPortAcceptance=False, goalStatus='active')
        if OUT.exists():
            path = OUT / 'failure.json'; need(not path.exists(), 'Never overwrite original native/source failure')
            path.write_text(json.dumps(failure, indent=2) + '\n')
        print(json.dumps(failure, indent=2), flush=True)
        code.interact(banner='Original startup handle and full actual bytes retained; inspect/re-poll, never timeout-reboot.', local=dict(RAM=RAM))
