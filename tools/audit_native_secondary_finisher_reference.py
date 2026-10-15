"""Original-ROM secondary-finisher map, not runtime or release acceptance.

Keeps disassembly and reconstructed guest in memory. Proves the current
missing dispatch distinction and checks every already imported component
needed by the unused donor performer scripts. Never edits game/source/ROM.
"""
import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path

import build_mk2ks_mk3 as art
import native_cpu_finisher_spacing_context as current
import native_process_census_v6647 as native

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_secondary_finisher_reference'
SOURCE = ROOT / 'source_native_cpu_finisher_spacing/midtunit_m.cpp'
MK3 = ROOT / 'mk3/mk3-maincpu.bin'
MK2 = ROOT / 'mk2/mk2-maincpu.bin'
PAYLOAD = ROOT / current.NAME / 'roms/mk2ks/mk2ks.mdata'
TABLES = (0xf4320, 0xf436c)
ORIGINAL_TABLES = (0xff8ba210, 0xff8ba390)
ACTION_RANGES = ((0xff9b5cd0, 0xff9b6200),
                 (0xff9b62c0, 0xff9b6970),
                 (0xff9ae0b0, 0xff9af2e0))


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def pointer(data, address):
    return art.u32(data, art.stock_file(address))


def inspect_dispatch(guest, original):
    rows = []
    for ident in range(12):
        choices = [pointer(original, table + ident * 32) for table in ORIGINAL_TABLES]
        need(choices[0] != choices[1], 'Every original playable MKII row has distinct fatality choices')
        need(all(art.u32(guest, table + ident * 4) == action
                 for table, action in zip(TABLES, choices)), 'Both original stock choices conserved')
        rows.append(dict(identity=ident, first=f'{choices[0]:08X}', second=f'{choices[1]:08X}'))
    added = []
    for ident, expected in ((17, 0xfffaae00), (18, 0xfffab200)):
        choices = [art.u32(guest, table + ident * 4) for table in TABLES]
        need(choices == [expected, expected], 'Current added CPU variants alias the one installed owned action')
        added.append(dict(identity=ident, first=f'{choices[0]:08X}', second=f'{choices[1]:08X}',
                          distinctChoices=False))
    return dict(stock=rows, added=added)


def inspect_groups(program, payload):
    result = []
    for name, main, special, block, index in (
        ('kano_unused_performer', art.KANO_MAIN, art.KANO_SPECIAL, art.KANO_BLOCK, 3),
        ('sonya_shared_kiss_performer', art.SONYA_MAIN, art.SONYA_SPECIAL, art.SONYA_BLOCK, 2),
        ('sonya_unused_effect', art.SONYA_MAIN, art.SONYA_SPECIAL, art.SONYA_BLOCK, 4),
    ):
        entry = art.stock_file(special) + index * 4
        start, end = art.sequence_spans(program, special, block, (main, special))[index]
        need(art.u32(payload, entry) == art.relocate_pointer(start), 'Original secondary animation entry already relocated')
        references = art.group_references(program, start, end, *block)
        need(references, 'Original unused sequence contains actual valid composites')
        groups = []
        for at, group, components in references:
            need(art.u32(payload, at) == art.relocate_pointer(group), 'Every original sequence reference already relocated')
            descriptors = []
            for offset, frame in enumerate(components):
                component = art.stock_file(frame)
                need(art.u32(payload, art.stock_file(group) + offset * 4) == art.relocate_pointer(frame),
                     'Every original composite component already relocated')
                expected = bytearray(program[component:component + 14])
                struct.pack_into('<I', expected, 8, art.u32(program, component + 8) + art.GFX_REBASE)
                need(payload[component:component + 14] == expected,
                     'All width/height/origin/DMA command fields conserved, only graphics address rebased')
                tail = art.u32(program, component + 14)
                palette = None
                if art.TMS_ROM_BASE <= tail <= 0xffffffff and not tail & 15:
                    need(art.u32(payload, component + 14) == art.relocate_pointer(tail),
                         'Actual descriptor palette pointer already relocated')
                    palette = f'{tail:08X}'
                descriptors.append(dict(frame=f'{frame:08X}', descriptorSHA256=hashlib.sha256(expected).hexdigest().upper(),
                                        palette=palette))
            need(art.u32(payload, art.stock_file(group) + len(components) * 4) == 0,
                 'Original composite terminator conserved')
            groups.append(dict(sequenceByteOffset=at, group=f'{group:08X}', components=descriptors))
        result.append(dict(name=name, animationIndex=index, script=f'{start:08X}',
                           spanEnd=f'{end:08X}', references=groups,
                           uniqueGroups=len({r['group'] for r in groups}), alreadyImported=True))
    return result


def inspect_original_actions(program, instructions):
    # Original MK3 selects these by its genuine roster table, not by names
    # inferred from an old assisted trace or from an unverified move guide.
    tables = (0xff998870, 0xff998a50)
    expected = ((0xff9b5cd0, 0xff9b12e0), (0xff9af2e0, 0xff9ae0b0))
    need(instructions[0xff998780] == 'MOVI   FF998870h,A0' and
         instructions[0xff998810] == 'MOVI   FF998A50h,A0', 'Original first/second native performer table operands')
    need(instructions[0xff9b5d80] == 'MOVK   3h,A9' and
         instructions[0xff9b5d90] == 'CALLA  FFA5EF10h', 'Unused Kano performer selects original special3')
    need(instructions[0xff9ae120] == 'MOVK   2h,A9' and
         instructions[0xff9ae130] == 'CALLA  FFA5EF10h' and
         instructions[0xff9ae1f0] == 'MOVK   4h,A9' and
         instructions[0xff9ae200] == 'CALLA  FFA5EF10h', 'Unused Sonya performer selects shared special2 and independent special4 effect')
    result = []
    for ident, choices in enumerate(expected):
        actual = tuple(pointer(program, table + ident * 32) for table in tables)
        need(actual == choices and actual[0] != actual[1], 'Original Kano/Sonya native choices are genuinely distinct')
        result.append(dict(originalIdentity=ident, first=f'{actual[0]:08X}', second=f'{actual[1]:08X}',
                           unusedVariant=1 if ident == 0 else 2))
    return result


def main():
    need(not OUT.exists(), 'Fresh immutable secondary reference evidence')
    need(not native.census(), 'No live port process while taking immutable source reference')
    guest = current.expected()
    original = MK2.read_bytes()
    program, payload = MK3.read_bytes(), PAYLOAD.read_bytes()
    need(sha(MK3) == '1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651',
         'Independent original donor program used for all action/animation facts')
    source = SOURCE.read_text()
    need(source.count('write32(table+17*4,native_address(kano_finish_action));') == 1 and
         source.count('write32(table+18*4,native_address(sonya_finish_action));') == 1 and
         'for (unsigned variant=0;variant<2;variant++)' in source, 'Both current variants unconditionally bind the same owned actions')
    dispatch = inspect_dispatch(guest, original)
    groups = inspect_groups(program, payload)
    tool = ROOT / 'mame-mkp/unidasm.exe'
    run = subprocess.run([str(tool), str(MK3), '-arch', 'tms34010', '-basepc', '0xff800000', '-norawbytes'],
                         capture_output=True, text=True, check=True)
    instructions = {int(line.split(':', 1)[0], 16): line.split(':', 1)[1].strip()
                    for line in run.stdout.splitlines()}
    actions = inspect_original_actions(program, instructions)
    faults = []
    for label, data, at, check in (
        ('added_first_dispatch', guest, TABLES[0]+17*4, lambda value: inspect_dispatch(value, original)),
        ('added_second_dispatch', guest, TABLES[1]+18*4, lambda value: inspect_dispatch(value, original)),
        ('stock_first_dispatch', guest, TABLES[0], lambda value: inspect_dispatch(value, original)),
        ('stock_second_dispatch', guest, TABLES[1], lambda value: inspect_dispatch(value, original)),
        ('Kano_unused_sequence_pointer', payload, art.stock_file(art.KANO_SPECIAL)+3*4,
         lambda value: inspect_groups(program, value)),
        ('Sonya_unused_effect_pointer', payload, art.stock_file(art.SONYA_SPECIAL)+4*4,
         lambda value: inspect_groups(program, value)),
    ):
        wrong = bytearray(data)
        wrong[at] ^= 1
        try:
            check(bytes(wrong))
        except ValueError as error:
            faults.append(dict(name=label, rejected=str(error)))
        else:
            raise ValueError('Reference fault admitted: '+label)
    for label, entry in (('native_Kano_first_roster_action', 0xff998870),
                         ('native_Sonya_second_roster_action', 0xff998a70)):
        wrong = bytearray(program)
        wrong[art.stock_file(entry)] ^= 1
        try:
            inspect_original_actions(bytes(wrong), instructions)
        except ValueError as error:
            faults.append(dict(name=label, rejected=str(error)))
        else:
            raise ValueError('Original action fault admitted: '+label)
    scope_path = ROOT/'audit_native_guard_campaign_progress/report.json'
    scope = json.loads(scope_path.read_text(encoding='utf-8-sig'))
    paths = [Path(__file__), Path(art.__file__), Path(current.__file__), Path(native.__file__), SOURCE,
             MK3, MK2, PAYLOAD, tool, scope_path, ROOT/current.NAME/'build-info.json',
             ROOT/current.NAME/'mkport_candidate.exe', ROOT/'audit_latest_native_launcher/report.json']
    pins = {str(path.resolve()): sha(path) for path in paths}
    report = dict(passed=True, sourceReferenceAccepted=True, runtimeAccepted=False, fullPortAcceptance=False,
                  previousGoalTurnClassification='no progress: requested status restatement only; revalidated current source and native process absence here',
                  thisGoalTurnClassification='progress: independent original native dispatch/action map and all existing unused composite assets verified; no duplicate asset build required',
                  candidate=current.NAME, guestSHA256=hashlib.sha256(guest).hexdigest().upper(),
                  dispatch=dispatch, originalDonorChoices=actions, originalUnusedAssets=groups,
                  originalNativeActionDisassembly=[f'{at:08X}: {text}' for at, text in instructions.items()
                      if any(first <= at < last for first, last in ACTION_RANGES)],
                  originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],
                  limitations=['No second human command or second native action installed yet.',
                               'Original native selector/animation mappings are source facts, not observed finisher timing or sound.',
                               'Victim choreography, effect ownership, input grammar, palette and cleanup must be independently mapped before implementation.'],
                  nextAction='Trace the unused original native actions through physically earned finish windows; port their distinct typed animation/victim/effect routines and commands without executing MK3 code or borrowing another MKII fatality.',
                  faultRejections=faults, inputHashes=pins, newBuilds=0, newROMCopies=0, newRawMedia=0,
                  newZIPs=0, gameSourceChanged=False, latestPlayableChanged=False, goalStatus='active')
    need(len(report['originalNaturalIntegrationRequirements']) == 14 and len(report['originalRemainingWorkGroups']) == 6,
         'Full original scope remains intact')
    need(all(sha(path) == digest for path, digest in pins.items()), 'Actual source/assets/playable hashes conserved')
    OUT.mkdir()
    with gzip.open(OUT/'executed_reference_sources.json.gz', 'wt', encoding='utf-8') as stream:
        json.dump({str(path): dict(sha256=pins[str(path.resolve())], text=path.read_text())
                   for path in paths if path.suffix in ('.py', '.cpp')}, stream)
    (OUT/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(passed=True, unusedGroupsAlreadyImported=[r['uniqueGroups'] for r in groups],
                          rejectedFaults=len(faults), gameSourceChanged=False, nextAction=report['nextAction'])))


if __name__ == '__main__':
    main()
