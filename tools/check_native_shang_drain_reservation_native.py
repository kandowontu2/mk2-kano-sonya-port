"""Observe exact native free storage; no build, input or gameplay acceptance.

The whole original source initializer remains pinned, but its limited graphics
provider is explicitly NOT treated as complete GFX. Native read-only observation
covers every byte of BOTH proposed reservations and the exact stock boundaries.
"""
import gzip
import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path

import native_process_census_v6647 as identity

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_shang_drain_reservation_native'
NAME = 'diagnostic_native_paired_stumble_table_ps7'
LUA = ROOT / 'mk2ks_native_shang_drain_reservation.lua'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def need(value, reason):
    if not value:
        raise ValueError(reason)


def main():
    need(not OUT.exists() and not identity.census(), 'Fresh observation; no existing native handle to restart')
    candidate = ROOT / NAME
    meta_path = candidate / 'build-info.json'
    meta = json.loads(meta_path.read_text(encoding='utf-8-sig'))
    need(meta['executable_sha256'] == 'E56DD49DB8B918BC1DF806E3C70C34A557716116DCAADB2F683532DBACAFBD3D' and
         sha(candidate / 'mkport_candidate.exe') == meta['executable_sha256'] and
         sha(candidate / 'roms/mk2ks/mk2ks.mdata') == meta['payload_sha256'] and
         all(sha(p) == h for p, h in meta['input_hashes'].items()), 'Exact existing native executable and immutable compiled inputs')
    observer = LUA.read_text()
    need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|:set_value|:clear_value|machine:exit', observer),
         'Observer contains only passive reads and output')
    paths = [Path(__file__), LUA, meta_path, Path(identity.__file__),
             ROOT / 'mk2/mk2-maincpu.bin', ROOT / 'mk3/mk3-maincpu.bin',
             ROOT / 'audit_native_shang_drain_reservation_provider_failure/report.json',
             ROOT / 'audit_native_shang_drain_reservation_current_initializer/report.json',
             ROOT / 'art_native_shang_drain_encoded_v1/asset-report.json',
             ROOT / 'PLAY_LATEST_KANO_SONYA.cmd']
    pins = {str(p.resolve()): sha(p) for p in paths}
    OUT.mkdir()
    env = {k: v for k, v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)', k)}
    command = [str(candidate / 'mkport_candidate.exe'), 'mk2ks', '-rompath',
               str(candidate / 'roms') + ';' + str(ROOT / 'roms'),
               '-samplepath', str(candidate / 'samples') + ';' + str(ROOT / 'samples'),
               '-skip_gameinfo', '-nocheat', '-video', 'none', '-sound', 'none',
               '-noautoframeskip', '-frameskip', '0', '-throttle', '-str', '3',
               '-inipath', str(OUT), '-cfg_directory', str(OUT / 'cfg'),
               '-nvram_directory', str(OUT / 'nvram'), '-snapshot_directory', str(OUT / 'snap'),
               '-autoboot_delay', '0', '-autoboot_script', str(LUA)]
    born = time.time()
    job = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True, encoding='utf-8', errors='replace', creationflags=subprocess.CREATE_NO_WINDOW)
    actual = None
    # Capture real identity while stdout is deliberately not drained yet.
    # The full passive graphics output also keeps a fast process observable.
    for _ in range(100):
        actual = next((p for p in identity.census() if p['ProcessId'] == job.pid), None)
        if actual or job.poll() is not None:
            break
        time.sleep(.01)
    need(actual and actual['ParentProcessId'] == os.getpid() and actual['createdUnix'] >= born - 1 and
         Path(actual['ExecutablePath']).resolve() == (candidate / 'mkport_candidate.exe').resolve() and
         actual['CommandLine'] == subprocess.list2cmdline(command), 'Actual PID birth/path/parent/full command')
    (OUT / 'process-start.json').write_text(json.dumps(dict(actual=actual, hostPID=os.getpid(), command=command), indent=2) + '\n')
    print(json.dumps(dict(nativePID=job.pid, identityVerified=True, kind='passive cold-boot reservation only')), flush=True)
    # No observation timeout and no restart. Drain this original handle to its
    # native three-second terminal limit; there are no gameplay inputs here.
    stdout, stderr = job.communicate()
    with gzip.open(OUT / 'native-output.txt.gz', 'wt', encoding='utf-8') as target:
        target.write(stdout)
    (OUT / 'stderr.log').write_text(stderr)
    terminal = dict(nativeExit=job.returncode, actualPID=job.pid, sameHandleTerminal=True,
                    exactProcessAbsent=not any(p['ProcessId'] == job.pid and p['createdUnix'] == actual['createdUnix'] for p in identity.census()))
    (OUT / 'terminal.json').write_text(json.dumps(terminal, indent=2) + '\n')
    need(job.returncode == 0 and not stderr and terminal['exactProcessAbsent'], 'Same native handle terminal, clean exit and no live process')
    pattern = re.compile(r'^MK2_DRAIN_RESERVE kind=(\w+) start=([0-9A-F]+) offset=(\d+) bytes=(\d+) writes=0 assistance=none hex=([0-9a-f]+)$', re.M)
    data, starts, counts = {}, {}, {}
    for kind, first, offset, count, hex_data in pattern.findall(stdout):
        first, offset, count = int(first, 16), int(offset), int(count)
        raw = bytes.fromhex(hex_data)
        need(len(raw) == count and offset == len(data.get(kind, b'')) and
             (kind not in starts or starts[kind] == first), 'Every full native chunk ordered, bounded and unaltered')
        starts[kind] = first
        data[kind] = data.get(kind, b'') + raw
        counts[kind] = counts.get(kind, 0) + 1
    lengths = dict(program=4096, graphics=65536, primary=68, secondary=68, helper=18,
                   normal_kano=132, normal_sonya=132, alternate_kano=132, alternate_sonya=132)
    need(set(data) == set(lengths) and all(len(data[k]) == v for k, v in lengths.items()) and
         stdout.count('MK2_DRAIN_RESERVE_COMPLETE writes=0 assistance=none') == 1,
         'All exact whole reservations and original helper/palette/table observations')
    need(starts['program'] == 0xb1000 and starts['graphics'] == 0x1fb0000 and
         data['program'] == b'\xff' * 4096 and data['graphics'] == bytes(65536), 'Actual native reservations completely free')
    stock = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    for kind, address in (('primary', 0xff9d7770), ('secondary', 0xff9d8d70), ('helper', 0xff8cb410)):
        at = (address - 0xff800000) // 8
        need(starts[kind] == at and data[kind] == stock[at:at + lengths[kind]], 'Actual original helper and all17 effective table words untouched')
    donor = (ROOT / 'mk3/mk3-maincpu.bin').read_bytes()
    for kind, at, native in (('normal_kano', 0x92bbc, 0xfda00), ('normal_sonya', 0x92cf2, 0xfdb00),
                             ('alternate_kano', 0x92c3e, 0xf1500), ('alternate_sonya', 0x92d74, 0xf1600)):
        need(starts[kind] == native and data[kind] == bytes.fromhex('41000000') + donor[at + 4:at + 132],
             'Actual owned normal/alternate native palettes retain all64 opaque donor colours')
    need(all(sha(p) == h for p, h in pins.items()), 'Every frozen input and public launcher unchanged')
    result = dict(passed=True, scope=__doc__, nativeReservationAccepted=True,
                  fullGraphicsRegionNotExported=True, limitedOldGraphicsProviderNotUsedAsWhole=True,
                  programReservation=[0xb1000, 0xb2000], graphicsReservation=[0x1fb0000, 0x1fc0000],
                  actualNativeBytesRead=sum(lengths.values()), chunks=counts,
                  nativeSliceHashes={k: hashlib.sha256(v).hexdigest().upper() for k, v in data.items()},
                  actualNativeIdentity=actual, terminal=terminal, inputHashes=pins,
                  originalSecondaryTrailingWordsPreservedWithoutCallingThemPalettes=True,
                  nativeRepairAccepted=False, artworkRuntimeAccepted=False, fullPortAcceptance=False,
                  gameWrites=0, physicalInputs=0, newEmulatorBuilds=0, newROMCopies=0,
                  newRawGameplayMedia=0, newZIPs=0, publicPlayableChanged=False, goalStatus='active')
    (OUT / 'report.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(passed=True, nativeReservationAccepted=True,
                         actualNativeBytesRead=result['actualNativeBytesRead'], nativeRepairAccepted=False)))


if __name__ == '__main__':
    main()
