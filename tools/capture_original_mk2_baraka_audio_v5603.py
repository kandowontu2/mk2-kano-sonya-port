"""Physical original-game reference; never substitute it for port acceptance.

One stock mk2 boot, original Cage2 victim and original Baraka3 winner. The
whole physical921 controller is retained except original roster names and
snapshot sink. Native guest, DCS ROM, DAC and mixed PCM remain in RAM. Only
metadata/digests and MAME's single automatic timed-exit PNG persist.
"""
import ctypes
import datetime
import hashlib
import json
import os
import re
import subprocess
import traceback
from pathlib import Path

import numpy as np
from PIL import Image
import current_native_dac_clock_v5596 as clock
import current_dcs_rom_source_capture_v5586 as rom
import qualify_current_baraka_direct_packets_v5580 as direct

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'audit_v5601_current_native_dac_matrix_progress/progress.json'
FOLDER = ROOT / 'audit_v5604_original_mk2_baraka_audio_ram/cage_p1'
OUT = ROOT / 'audit_v5605_original_mk2_baraka_audio_progress'
LUA = ROOT / 'mk2_stock_baraka_audio_reference_v5602.lua'
BUILD = ROOT / 'diagnostic_v5219_current_payload_rom_metadata'
EXE = BUILD / 'mkport_candidate.exe'
STOCK = ROOT / 'mk2/mk2-maincpu.bin'
need = clock.need


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for raw in iter(lambda: f.read(1048576), b''):
            h.update(raw)
    return h.hexdigest().upper()


def digest(raw):
    return hashlib.sha256(raw).hexdigest().upper()


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def rows(log, prefix):
    return [dict(re.findall(r'(\w+)=([^\s]+)', line))
            for line in log.splitlines() if line.startswith(prefix + ' ')]


def physical(log):
    records = lambda tag: rows(log, 'MK2_STOCK_HEAD_V921_' + tag)
    result, action, live, wrap = (records(t) for t in ('RESULT', 'ACTION', 'FIRST_LIVE', 'WRAP'))
    need(all(len(r) == 1 for r in (result, action, live, wrap)),
         'Exactly one original live fight, physically earned fatality, completion and terminal')
    result, action, live, wrap = (r[0] for r in (result, action, live, wrap))
    need(result['frame'] == '5198' and result['damage'] == action['damage'] == '322'
         and result['wins'] == '2' and live['ids'] == '3,2'
         and wrap['age'] == '174' and wrap['actor'] == action['actor']
         and wrap['main'] == action['main'] and int(result['action']) == int(action['frame'])
         and int(result['wrap']) == int(wrap['frame']),
         'Original Cage2/Baraka3 true identities, two earned wins,322 collision damage,174-field completion')
    health = [r for r in records('HEALTH') if r['pc'] == 'FF836700'
              and int(r['after']) < int(r['before']) <= 161]
    need(len(health) == 10 and sum(int(r['before']) - int(r['after']) for r in health) == 322,
         'All ten real original collision-health stores account for both earned rounds')
    inputs = records('INPUT'); start = int(action['frame'])
    need(any(r['button'] == 'High_Punch' and int(r['slot']) == 2 and start-15 <= int(r['frame']) <= start for r in inputs)
         and any(r['button'] == 'Block' and int(r['slot']) == 2 and start-40 <= int(r['frame']) <= start for r in inputs)
         and any(r['table'] == 'FF87A9A0' for r in records('PARSER')),
         'Original P2 Baraka physical Block/BBBB/HP native parser, never injected action')
    need(not records('CACHE_OVERWRITE') and all(r['victim'] == 'cage' and r['side'] == '1'
         and r['killer'] == 'baraka' and r['writes'] == '0' and r['assistance'] == 'none'
         for tag in ('RESULT', 'ACTION', 'FIRST_LIVE', 'WRAP', 'HEALTH', 'INPUT') for r in records(tag)),
         'All original-reference records honest identity and passive provenance, no cache overrun')
    states = [r for r in records('STATE') if int(r['frame']) >= start]
    need(states and all(r['own'].endswith(':3') and r['victim'].endswith(':2') for r in states),
         'Actual original actor/main identities stay original throughout finishing sequence')
    return dict(passed=True, action=action, wrap=wrap, result=result,
                originalVictim='cage', originalVictimID=2, originalWinnerID=3,
                genuineHealthStores=len(health), physicalInputs=len(inputs), importedCharacterProxy=False)


def run():
    need(not FOLDER.exists() and not OUT.exists(), 'Fresh immutable original-game capture')
    parent = json.loads(PARENT.read_text())
    need(parent['passed'] and parent['goalStatus'] == 'active', 'Keep qualified four-context port proof and full original scope')
    pins = dict(parent['newInputHashes'])
    for p in (PARENT, Path(__file__), LUA, STOCK, EXE, Path(clock.__file__), Path(rom.__file__),
              ROOT / 'mk2ks_stock_head_victim_v921.lua', ROOT / 'mk2ks_kitana_audio_queue_ram_v3939.lua',
              ROOT / 'mk2ks_current_baraka_priority_ram_v5554.lua', ROOT / 'mk2ks_current_baraka_announcer_ram_v5565.lua',
              ROOT / 'mk2ks_current_baraka_packet_origin_v5576.lua', ROOT / 'mk2ks_current_native_dac_ram_v5592.lua',
              ROOT / 'mk2ks_current_dcs_rom_source_v5585.lua'):
        pins[str(p.resolve())] = sha(p)
    need(sha(EXE) == 'A6BC32F526C78A5BD72ED1960EAE56AB40701D7FE881D70A93E031AEB87AB944'
         and sha(STOCK) == '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
         'Exact current binary with genuine original stock main CPU source')
    stock = STOCK.read_bytes()
    expected, source_roms = rom.expected_region(pins)
    rom.EXPECTED = expected  # Functions bind their defining module, not this caller.
    need(all(sha(p) == h for p, h in pins.items()), 'All source/current/public and prior evidence unchanged before stock boot')
    FOLDER.mkdir(parents=True)
    for name in ('cfg', 'nvram', 'snap'):
        (FOLDER / name).mkdir()
    save(FOLDER / 'input_hashes_before.json', pins)
    env = {k: v for k, v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)', k)}
    env.update(MK2KS_PORT_ROOT=str(ROOT), MK2KS_TEST_FIGHTER='cage', MK2KS_CAMPAIGN_SIDE='1',
               MK2KS_STOCK_KILLER='baraka', MK2KS_STOCK_COMMAND='bbbb_hp', MK2KS_STOCK_GAP='64')
    command = [str(EXE), 'mk2', '-rompath', str(ROOT / 'roms'), '-nosamples', '-skip_gameinfo', '-nocheat',
               '-inipath', str(FOLDER), '-video', 'none', '-sound', 'none', '-samplerate', '48000',
               '-noautoframeskip', '-frameskip', '0', '-nothrottle', '-str', '95', '-snapsize', '400x254',
               '-cfg_directory', str(FOLDER / 'cfg'), '-nvram_directory', str(FOLDER / 'nvram'),
               '-snapshot_directory', str(FOLDER / 'snap'), '-autoboot_script', str(LUA)]
    pcm_chunks, pcm_headers, dac_chunks, dac_headers, guest = [], [], [], [], None
    regions = {'startup': bytearray(), 'terminal': bytearray()}
    region_headers, transport_errors = [], []
    with (FOLDER / 'stderr.log').open('w', encoding='utf-8') as err:
        proc = subprocess.Popen(command, cwd=FOLDER, env=env, stdout=subprocess.PIPE, stderr=err,
                                text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
        save(FOLDER / 'process.json', dict(pid=proc.pid, command=command,
             env={k: v for k, v in env.items() if k.startswith('MK2KS_')}, startedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat()))
        print('Original mk2 Cage-P1/Baraka-P2 native PID=' + str(proc.pid), flush=True)
        with (FOLDER / 'run.log').open('w', encoding='utf-8') as out:
            for line in proc.stdout:
                if line.startswith(('MK2_MAUDIO_GUEST ', 'MK2_BBAUDIO_PCM ', 'MK2_NATIVE_DAC_RAM ', 'MK2_NATIVE_DCS_ROM ')):
                    tag = line.split()[0]
                    try:
                        r = dict(re.findall(r'(\w+)=([^\s]+)', line))
                        raw = bytes.fromhex(r.pop('hex'))
                        need(len(raw) == int(r['bytes']), 'Whole RAM-only stock source/audio transport')
                        r['sha256'] = digest(raw)
                        if tag == 'MK2_MAUDIO_GUEST':
                            need(guest is None and raw == stock, 'Every initialized original guest byte equals original stock ROM, not port ROM')
                            guest = raw
                        elif tag == 'MK2_BBAUDIO_PCM':
                            need(len(raw) == 3840, 'Whole960-stereo-frame actual48kHz PCM callback')
                            pcm_chunks.append(raw); pcm_headers.append(r)
                        elif tag == 'MK2_NATIVE_DAC_RAM':
                            dac_chunks.append(raw); dac_headers.append(r)
                        else:
                            phase = r['phase']; offset = int(r['offset'])
                            need(phase in regions and offset == len(regions[phase]) and len(raw) == 65536
                                 and raw == expected[offset:offset+len(raw)] and r['writes'] == '0'
                                 and r['assistance'] == 'none' and r['frame'] == ('1' if phase == 'startup' else '5198'),
                                 'Complete original sound ROM bytes and native checkpoint bound to original lanes/mirrors')
                            regions[phase].extend(raw); region_headers.append(r)
                        out.write(tag + '_DIGEST ' + ' '.join(k+'='+str(v) for k, v in r.items()) + '\n')
                    except Exception as error:
                        # Always drain the same process. Never log raw transport or restart a timed-out observation.
                        transport_errors.append(dict(tag=tag, error=repr(error)))
                        out.write(tag + '_TRANSPORT_ERROR error=' + repr(error) + '\n')
                else:
                    need('hex=' not in line, 'No unrecognized raw buffer sink')
                    out.write(line)
            exit_code = proc.wait()
    terminal = dict(nativePID=proc.pid, exit_code=exit_code, completedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    driver='mk2', victim='cage', victimID=2, winner='baraka', winnerID=3, cheats=False, assistance='none')
    save(FOLDER / 'terminal.json', terminal)
    print('Original native terminal exit=' + str(exit_code), flush=True)
    log = (FOLDER / 'run.log').read_text()
    need(exit_code == 0 and not (FOLDER / 'stderr.log').read_text() and 'Average speed:' in log
         and not transport_errors, 'Actual stock process terminal0, no script/transport errors')
    state = physical(log)
    need('MK2_ORIGINAL_REFERENCE_SETUP driver=mk2 victim=cage victim_id=2 winner=baraka winner_id=3 imported_voice_device=absent writes=0 assistance=none' in log
         and not rows(log, 'MK2_MAUDIO_CHANNEL') and guest == stock,
         'Genuine original driver/guest with absent added-character voice device and no fabricated channel ledger')
    dcs_proof = [rom.region_gate(bytes(regions[phase]), phase) for phase in ('startup', 'terminal')]
    dcs_faults = [fault for phase in ('startup', 'terminal') for fault in rom.region_faults(bytes(regions[phase]), phase)]
    need(len(region_headers) == 384 and len(dcs_faults) == 8, 'Entire original sound ROM at both native checkpoints with effective byte faults')
    dac = clock.original.dac_gate(dac_chunks, dac_headers, pcm_headers)
    dac_faults = clock.original.dac_faults(dac_chunks, dac_headers, pcm_headers)
    pcm = np.frombuffer(b''.join(pcm_chunks), '<i2').reshape(-1, 2)
    waveform = clock.predict_waveform(dac_chunks, dac_headers, pcm)
    need(waveform['passed'] and waveform['differentChannelSamples'] == 0
         and len(waveform['effectiveActualWholeWaveformFaults']) == 4,
         'Every actual stock native DAC-to-mixer sample equals original source-clock prediction')
    # The current packet gate may expose stock-specific callers. Retain that
    # result honestly; original waveform transport acceptance does not hide it.
    try:
        packets = dict(passed=True, proof=direct.gate(log, stock), effectiveFaults=direct.faults(log, stock))
    except Exception as error:
        packets = dict(passed=False, error=repr(error), traceback=traceback.format_exc())
    need(all(sha(p) == h for p, h in pins.items()), 'All existing current/public/source/evidence bytes unchanged after original boot')
    waveform.pop('actualCallbackSourceClocks')  # Derived685 rows available from retained timestamps/source; no redundant journal bulk.
    return dict(passed=True, observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), goalStatus='active',
        remaining=parent['remaining'], parentAdditiveJournal=str(PARENT), previousGoalTurnClassification='no progress: acknowledgement and read-only cleanup status did not change implementation or qualification',
        thisGoalTurnClassification='progress: genuine original mk2 Cage2-versus-Baraka3 physical control, entire stock guest and sound ROM source, native DAC-to-mixer waveform and source/transport faults; no proxy, guest/audio writes, added voice channels or new build',
        nativeCaptureResult=str(FOLDER / 'result.json'), nativeTerminal=terminal, originalPhysicalProof=state,
        originalGuestSHA256=digest(guest), originalSourceROMs=source_roms, actualOriginalDCSROMProof=dcs_proof,
        effectiveActualDCSROMByteFaults=dcs_faults, originalDACProof=dac, effectiveOriginalDACFaults=dac_faults,
        originalDACToMixedPCMProof=waveform, originalPacketQualification=packets,
        originalPCMCallbacks=len(pcm_headers), originalPCMBytes=sum(len(r) for r in pcm_chunks),
        originalPCMHeaders=pcm_headers, originalDACHeaders=dac_headers,
        genuineOriginalMK2WaveformReferenceCaptured=True, portWaveformEqualsOriginalGameplayReferenceAccepted=False,
        allNativeBranchCombinationsAccepted=False, completeBarakaFinisherAudioAccepted=False, fullPortAcceptance=False,
        newNativeBoots=1, newBuilds=0, newDeletedFiles=0, publicPlayableChanged=False, refreshedReleaseZIP=False,
        requestedRawGuestGFXVRAMRGBPCMFilesWritten=0, newInputHashes=pins,
        nextAction='Qualify stock-specific original packet/caller observations if needed and compare source-owned corresponding original/port audio phases without whole-scene or timing/gain fits; continue every original stage/move/finisher/CPU/campaign/UI/cleanup/release requirement.')


def seal(report):
    pngs = []
    if FOLDER.exists():
        for p in sorted(FOLDER.rglob('*')):
            if p.is_file():
                need(p.suffix.lower() not in ('.wav', '.pcm', '.bin', '.rgb'), 'No requested raw evidence files')
                if p.suffix.lower() == '.png':
                    with Image.open(p) as image:
                        need(p == FOLDER / 'snap/mk2/0000.png' and image.size == (400, 254), 'Only stock-driver automatic native timed-exit PNG')
                    pngs.append(dict(path=str(p), bytes=p.stat().st_size, sha256=sha(p)))
    report.update(persistentNativeAutomaticExitPNGs=pngs, persistentNativeAutomaticPNGBytes=sum(p['bytes'] for p in pngs))
    if report['passed']:
        need(len(pngs) == 1, 'Exactly one automatic stock timed-exit PNG accounted')
        save(FOLDER / 'result.json', report)
    OUT.mkdir()
    save(OUT / 'progress.json', report)
    api = ctypes.WinDLL('kernel32', use_last_error=True).GetCompressedFileSizeW
    api.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_uint32)]
    api.restype = ctypes.c_uint32
    def allocated(p):
        high = ctypes.c_uint32(); ctypes.set_last_error(0)
        low = api(str(p), ctypes.byref(high))
        need(low != 0xffffffff or not ctypes.get_last_error(), 'Actual allocated NTFS size')
        return (high.value << 32) | low
    measures = []
    for p in [Path(__file__), LUA, *FOLDER.rglob('*'), *OUT.rglob('*')]:
        if p.is_file() and p.suffix.lower() in ('.py', '.lua', '.log', '.json', '.cfg', '.txt'):
            before_hash, before = sha(p), allocated(p)
            done = subprocess.run(['compact.exe', '/C', '/F', '/EXE:LZX', '/Q', str(p)], capture_output=True)
            need(done.returncode == 0 and sha(p) == before_hash, 'Force-LZX preserves every sealed source/metadata/log byte')
            measures.append(dict(path=str(p), sha256=before_hash, allocatedBefore=before, allocatedAfter=allocated(p)))
    save(OUT / 'storage.json', dict(passed=True, files=len(measures), measurements=measures,
         measuredAllocatedBytesReclaimed=sum(r['allocatedBefore']-r['allocatedAfter'] for r in measures), deletedFiles=0))
    done = subprocess.run(['compact.exe', '/C', '/F', '/EXE:LZX', '/Q', str(OUT / 'storage.json')], capture_output=True)
    need(done.returncode == 0, 'New storage receipt compressed')


if __name__ == '__main__':
    need(not FOLDER.exists() and not OUT.exists(), 'Never overwrite original capture or failure')
    try:
        report = run()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), goalStatus='active',
                      fullPortAcceptance=False, parentAdditiveJournal=str(PARENT))
    seal(report)
    print(json.dumps({k: report[k] for k in ('passed', 'error', 'nativeTerminal', 'originalPCMCallbacks',
        'originalPCMBytes', 'originalPacketQualification', 'persistentNativeAutomaticPNGBytes') if k in report
        and k != 'originalPacketQualification'}, indent=2), flush=True)
    if report.get('originalPacketQualification'):
        print('Original packet gate passed=' + str(report['originalPacketQualification']['passed']), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
