"""Source-only repair of a reproduced native packed-victim table overread.

The actual failing guest remains in its original RAM parent. No game writes,
replays, cache caps, identity aliases, or synthetic gameplay acceptance.
"""
import copy
import gzip
import hashlib
import json
import os
import re
import struct
import traceback
from pathlib import Path

import capture_native_sonya_raiden_cache_cause as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
STAGE = ROOT / 'source_native_paired_stumble_table'
OUT = ROOT / 'audit_native_paired_stumble_table_source'
BEGIN, END = '// PAIRED_STUMBLE_TABLE_BEGIN', '// PAIRED_STUMBLE_TABLE_END'
TABLE, OPERAND, SOURCE, ROW = 0xfd7a0, 0xff8752a0, 0xff875bd0, 0x2303bce0


def offset(address):
    return (address - 0xff800000) // 8


def read32(guest, address):
    return struct.unpack_from('<I', guest, offset(address))[0]


def source_contract():
    original = ROOT / 'source_native_kano_laser_audio'
    for name in ('midtunit.cpp', 'midtunit.h'):
        need((STAGE / name).read_bytes() == (original / name).read_bytes(),
             'Entire audio configuration and header unchanged')
    before = (original / 'midtunit_m.cpp').read_text()
    after = (STAGE / 'midtunit_m.cpp').read_text()
    first = after.index('\n\t' + BEGIN)
    last = after.index('\n', after.index(END, first))
    block = after[first:last]
    need(after[:first] + after[last:] == before, 'Whole driver differs only by new packed table')
    need(block.count('std::copy_n(') == 1 and block.count('write32(') == 3 and
         '17 * 4, rom + paired_stumble_table' in block and
         'paired_stumble_table = 0xfd7a0;' in block and
         'paired_stumble_row = 0x2303bce0;' in block and
         'read32(rom_offset(0xff8752a0)) != 0xff875bd0' in block and
         'native_address(paired_stumble_table)' in block,
         'Exact original operand, unused storage, 17 preserved rows, two own rows')
    return block


def cause_contract(rows, guest, payload):
    actual = [r for r in rows if r['frame'] == '54865']
    lookup = next(r for r in actual if r['kind'] == 'main_lookup')
    result = next(r for r in actual if r['kind'] == 'lookup_result')
    cache = next(r for r in actual if r['kind'] == 'cache_begin')
    bad = next(r for r in actual if r['kind'] == 'first_global_write')
    need(lookup['actor'] == cache['actor'] == bad['actor'] == '01033C00' and
         lookup['main'] == lookup['victim_main'] == '0106F6B0' and
         cache['main'] == cache['cpu_main'] == '0106A370' and
         cache['main_owner'] == cache['cpu_actor'] == '01033E10' and
         all(r['id'] == r['roster'] == '18' and r['cpu_roster'] == '7' and
             r['writes'] == '0' and r['assistance'] == 'none' for r in actual),
         'Actual true Sonya victim and Raiden owner context, no identity substitution')
    packed = read32(guest, SOURCE + 18 * 32)
    need(read32(guest, OPERAND) == SOURCE and packed == 0x0230b02d and
         lookup['a0'] == f'{packed:08X}' and lookup['a9'] == f'{packed >> 24:08X}' and
         lookup['a1'] == f'{((packed >> 16) & 255) * 32:08X}' and
         lookup['stack0'] == 'FF842E20',
         'Original unextended victim row is actual executable code and actual packed input')
    stream = int(result['a9'], 16)
    cell = stream + ((packed >> 16) & 255) * 32
    fetch = struct.unpack_from('<I', payload, (cell - 0xfe800000) // 8)[0]
    descriptor = struct.unpack_from('<I', payload, (fetch - 0xfe800000) // 8)[0]
    need(result['a9'] == 'FF0210C0' and cache['a9'] == f'{cell + 32:08X}' and
         cache['a0'] == f'{fetch:08X}' and descriptor == 0x00170039 and
         cache['a0_rom'] == f'{descriptor:08X}' and cache['stack0'] == 'FFFC1370' and
         cache['stack1'] == 'FF842330' and bad['pc'] == 'FF838860' and
         bad['health'] == '0,115' and bad['stage'] == '2',
         'Full observed packed48-pose offset -> descriptor-as-group -> real global decoder store')
    return dict(packedVictimRow=f'{packed:08X}', erroneousAnimation=packed >> 24,
                erroneousPoseIndex=(packed >> 16) & 255, actualStream=f'{stream:08X}',
                actualWrongCell=f'{cell:08X}', actualDescriptor=f'{fetch:08X}',
                actualDescriptorDimensions=f'{descriptor:08X}')


def guest_contract(previous, proposed, payload):
    need(len(previous) == len(proposed) == 1048576, 'Whole original native guest')
    expected = bytearray(previous)
    need(all(x == 255 for x in expected[TABLE:TABLE + 0x50]), 'Actual free storage, no overwritten allocation')
    expected[TABLE:TABLE + 17 * 4] = previous[offset(SOURCE):offset(SOURCE) + 17 * 4]
    struct.pack_into('<II', expected, TABLE + 17 * 4, ROW, ROW)
    struct.pack_into('<I', expected, offset(OPERAND), 0xff800000 + TABLE * 8)
    need(proposed == expected, 'Every other code/data/identity/audio/cache byte unchanged')
    outer = read32(previous, 0xff9060a0)
    own = []
    for ident in (17, 18):
        root = read32(previous, outer + ident * 32)
        stream = struct.unpack_from('<I', payload, (root - 0xfe800000) // 8 + 35 * 4)[0]
        values = struct.unpack_from('<6I', payload, (stream - 0xfe800000) // 8)
        need(values[5] == 0 and all(v > 0xfe800000 for v in values[:5]),
             'Complete actual five-pose owned main35 native stumble grammar')
        group = values[3]
        parts = []
        at = (group - 0xfe800000) // 8
        while True:
            pointer = struct.unpack_from('<I', payload, at)[0]
            if not pointer:
                break
            need(0xfe800000 <= pointer < 0xff800000 and len(parts) < 8, 'Owned composite terminates')
            descriptor = struct.unpack_from('<7H', payload, (pointer - 0xfe800000) // 8)
            need(0 < descriptor[0] < 512 and 0 < descriptor[1] < 512, 'Actual descriptor dimensions')
            parts.append(dict(pointer=f'{pointer:08X}', words=list(descriptor)))
            at += 4
        need(parts, 'Actual character-owned stumble pose, not stock proxy or descriptor')
        own.append(dict(identity=ident, root=f'{root:08X}', animation=35, pose=3,
                        stream=f'{stream:08X}', group=f'{group:08X}', parts=parts,
                        signedAlignment=[-68, -32], nativeTimingDamageCleanupUnchanged=True))
    return expected, own


def qualify(ram):
    need(os.getpid() == 145372 and not OUT.exists(), 'Exact retained failed native parent, fresh qualification')
    folder = capture.OUT
    proof = json.loads((folder / 'guest_memory_proof.json').read_text())
    metadata = json.loads((folder / 'result.json').read_text())
    terminal = json.loads((folder / 'native_terminal.json').read_text())
    failure = json.loads((folder / 'current_capture_failure.json').read_text())
    pins = json.loads((folder / 'input_hashes_before.json').read_text())
    need(terminal['nativeExit'] == 0 and terminal['identity']['ProcessId'] == 190268 and
         terminal['identity']['ParentProcessId'] == 145372 and not failure['passed'] and
         metadata['nativeCacheOverrunObserved'] and proof['everyActualByteComparedInRAM'] and
         hashlib.sha256(ram['guest']).hexdigest().upper() == proof['sha256'] and
         all(sha(p) == h for p, h in pins.items()), 'Original failed native guest and every executed source bound')
    payload_path = ROOT / 'diagnostic_native_kano_laser_audio/roms/mk2ks/mk2ks.mdata'
    payload = payload_path.read_bytes()
    need(sha(payload_path) == ram['build']['payload_sha256'], 'Entire original unchanged donor payload')
    text = gzip.open(folder / 'run.log.gz', 'rt', encoding='utf-8').read()
    parse = lambda tag: [dict(re.findall(r'(\w+)=([^\s]+)', line))
                         for line in text.splitlines() if line.startswith(tag + ' ')]
    rows = parse('MK2_SONYA_RAIDEN_CACHE_CAUSE')
    stores = parse('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE')
    legacy = parse('MK2_MILEENA_CAMPAIGN_OVERRUN')
    need(len(rows) == 1800 and len(stores) == len(legacy) == 146 and
         all(all(a[k] == b[k] for k in ('pc', 'at', 'data', 'mask', 'a8', 'a13'))
             for a, b in zip(stores, legacy)), 'Whole bounded provenance and independent real corruption taps')
    block = source_contract()
    cause = cause_contract(rows, ram['guest'], payload)
    proposed = bytearray(ram['guest'])
    proposed[TABLE:TABLE + 17 * 4] = ram['guest'][offset(SOURCE):offset(SOURCE) + 17 * 4]
    struct.pack_into('<II', proposed, TABLE + 17 * 4, ROW, ROW)
    struct.pack_into('<I', proposed, offset(OPERAND), 0xff800000 + TABLE * 8)
    _, own = guest_contract(ram['guest'], proposed, payload)
    rejected = []
    for ident in range(19):
        fault = proposed.copy()
        fault[TABLE + ident * 4] ^= 1
        try:
            guest_contract(ram['guest'], fault, payload)
        except ValueError:
            rejected.append('wrong_packed_victim_row_' + str(ident))
        else:
            raise ValueError('Invalid actual table row admitted')
    for index, (kind, key, wrong) in enumerate([
        ('main_lookup', 'a0', '0230B02C'), ('main_lookup', 'a1', '00000060'),
        ('main_lookup', 'a9', '00000023'), ('lookup_result', 'a9', 'FF0210E0'),
        ('cache_begin', 'a0', 'FF031A80'), ('cache_begin', 'a9', 'FF021100'),
        ('cache_begin', 'main_owner', '01033C00'), ('cache_begin', 'stack1', 'FF842E20'),
        ('first_global_write', 'health', '115,115'), ('first_global_write', 'cpu_roster', '18')]):
        fault = copy.deepcopy(rows)
        next(r for r in fault if r['frame'] == '54865' and r['kind'] == kind)[key] = wrong
        try:
            cause_contract(fault, ram['guest'], payload)
        except ValueError:
            rejected.append('wrong_actual_cause_field_' + str(index))
        else:
            raise ValueError('False native causal chain admitted')
    parent = json.loads((capture.SOURCE / 'report.json').read_text())
    paths = [Path(__file__), *STAGE.iterdir(), payload_path,
             ROOT / 'diagnostic_native_kano_laser_audio/build-info.json',
             ROOT / 'audit_native_kano_laser_audio_call_frame_source/report.json',
             ROOT / 'PLAY_LATEST_KANO_SONYA.cmd', *folder.rglob('*'), *capture.SOURCE.rglob('*')]
    pins.update({str(p.resolve()): sha(p) for p in paths if p.is_file()})
    delta = sum(a != b for a, b in zip(ram['guest'], proposed))
    staged = {p.name: sha(p) for p in STAGE.iterdir()}
    report = dict(passed=True, sourceOnlyAccepted=True, nativeRuntimeAccepted=False,
        actualRootCauseSourceMatched=True, originalGameDefectPreserved=True,
        exactNativeGame=190268, exactRAMParent=145372, nativeExit=0,
        actualGlobalDecoderStores=146, completeProvenanceRows=1800, actualCause=cause,
        stagedSourceHashes=staged, proposedGuestSHA256=hashlib.sha256(proposed).hexdigest().upper(),
        initializedGuestByteDelta=delta, originalAll17PackedVictimRowsConserved=True,
        newOwnRows=own, negativeFaultsRejected=rejected, sourceAddition=block,
        originalNaturalIntegrationRequirements=parent['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=parent['originalRemainingWorkGroups'], inputHashes=pins,
        newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
        publicPlayableChanged=False, fullPortAcceptance=False, goalStatus='active')
    need(len(report['originalNaturalIntegrationRequirements']) == 14 and
         len(report['originalRemainingWorkGroups']) == 6, 'Full original objective retained')
    OUT.mkdir()
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(sourceOnlyAccepted=True, changedGuestBytes=delta,
                         negativeFaultsRejected=len(rejected), proposedGuestSHA256=report['proposedGuestSHA256'])), flush=True)
    return proposed


def run(ram):
    try:
        return qualify(ram)
    except Exception as error:
        need(not OUT.exists(), 'Never rewrite original qualification failure')
        OUT.mkdir()
        (OUT / 'failure.json').write_text(json.dumps(dict(passed=False, error=repr(error),
            traceback=traceback.format_exc(), fullPortAcceptance=False, goalStatus='active'), indent=2) + '\n')
        raise
