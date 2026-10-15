"""Map the unused original Kano fatality input from the actual donor ROM.

This is source evidence, not proof that the move executed. Keeps the complete
disassembly in memory and conserves the existing candidate and frozen trials.
"""
import gzip
import hashlib
import json
import struct
import subprocess
from pathlib import Path
import audit_native_secondary_finisher_reference as reference
import capture_native_secondary_kano_reference as transport

ROOT = reference.ROOT
OUT = ROOT / 'audit_native_kano_secondary_input'


def inspect(program, instructions):
    need = reference.need
    pointer = lambda a: reference.pointer(program, a)
    word = lambda a: struct.unpack_from('<H', program, reference.art.stock_file(a))[0]
    table = pointer(0xff977bd0 + 3 * 32)
    need(table == 0xff978490 and pointer(table) == 0xff979ff0,
         'Actual original event3 and Kano0 press dispatch')
    expected = {
        0xff818be0: 'MOVI   FF977BD0h,A4',
        0xff818c70: 'SLL    5h,A1',
        0xff818ca0: 'MOVE   *A8(1F0h),A4,0',
        0xff818cc0: 'SLL    5h,A4',
        0xff979ff0: 'MOVI   FF991AF0h,A14',
        0xff97a020: 'JR     FF991F70h',
        0xff991fe0: 'CALLR  FF982880h',
        0xff992010: 'MOVE   *A14(50h),A7,1',
        0xff992090: 'MOVE   *A14(70h),A7,1',
        0xff992ee0: 'MOVI   80h,A5',
        0xff992f00: 'MOVI   B0h,A6',
        0xff992f20: 'JR     FF993160h',
        0xff993160: 'CALLA  FF822890h',
        0xff993190: 'CMP    A5,A3',
        0xff9931a0: 'JRC    FF993B00h',
        0xff9931c0: 'CMP    A6,A3',
        0xff9931d0: 'JRHI   FF993B00h',
        0xff9931f0: 'JR     FF993760h',
        0xff993760: 'MOVE   @1062250h,A4,0',
        0xff993790: 'CMPI   3h,A4',
        0xff9937b0: 'JRNE   FF993B00h',
        0xff998780: 'MOVI   FF998870h,A0',
        0xff9b5d80: 'MOVK   3h,A9',
        0xff9b5d90: 'CALLA  FFA5EF10h',
    }
    for at, opcode in expected.items():
        need(instructions.get(at) == opcode, f'Actual original input instruction {at:08X}')
    record = 0xff991af0
    need(pointer(record) == 0x40 and pointer(record + 0x20) == 0x4000,
         'High Kick allowed held masks for both original physical players')
    need(word(record + 0x40) == 2 and pointer(record + 0x50) == 0xff992ee0 and
         pointer(record + 0x70) == 0xff998750, 'Actual typed native fatality gate and first selector')
    need(word(record + 0x90) == 40, 'Actual history timeout40 native ticks')
    sequences = [[word(record + 0xa0 + facing * 0x60 + token * 16)
                  for token in range(6)] for facing in range(2)]
    need(sequences == [[3, 2, 2, 1, 0, 0]] * 2,
         'Both actual facing histories: most-recent HK, Block, Block, LP')
    need(pointer(0xff998870) == 0xff9b5cd0,
         'Actual Kano0 first performer, not a recalled command guide')
    return dict(pressEvent=3, pressTable=f'{table:08X}', handler='FF979FF0',
                record=f'{record:08X}', requiredFinishFlag=3,
                commandChronological=['Low Punch', 'Block', 'Block', 'High Kick'],
                timeoutNativeTicks=40, bodySeparationMinimum=128,
                bodySeparationMaximum=176, bothFacingHistories=sequences,
                action='FF9B5CD0', specialAnimationIndex=3,
                verifiedInstructions={f'{at:08X}': text for at, text in expected.items()})


def main():
    reference.need(not OUT.exists() and not transport.census() and not reference.native.census(),
                   'Fresh source audit with no live native games')
    original = reference.MK3.read_bytes()
    reference.need(reference.sha(reference.MK3) ==
                   '1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651',
                   'Exact authoritative original program')
    program = reference.current.expected()
    run = subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'), str(reference.MK3),
                          '-arch', 'tms34010', '-basepc', '0xff800000', '-norawbytes'],
                         capture_output=True, text=True, check=True)
    instructions = {int(line.split(':', 1)[0], 16): line.split(':', 1)[1].strip()
                    for line in run.stdout.splitlines()}
    mapping = inspect(original, instructions)
    faults = []
    for name, at in [('press_table', 0xff977bd0+3*32), ('Kano_handler', 0xff978490),
                     ('held_mask', 0xff991af0), ('range_gate', 0xff991b40),
                     ('selector', 0xff991b60), ('timeout', 0xff991b80),
                     ('right_history', 0xff991b90), ('left_history', 0xff991bf0),
                     ('actual_performer', 0xff998870)]:
        wrong = bytearray(original)
        wrong[reference.art.stock_file(at)] ^= 1
        try:
            inspect(bytes(wrong), instructions)
        except ValueError as error:
            faults.append(dict(name=name, rejected=str(error)))
        else:
            raise ValueError('Original input fault admitted: '+name)
    before = ROOT/'audit_native_secondary_kano_guarded_command/report.json'
    record = json.loads(before.read_text())
    reference.need(record['passed'] and record['nativeExit'] == 0 and
                   not record['finisherAccepted'] and
                   all(reference.sha(p) == h for p, h in record['inputHashes'].items()),
                   'Actually executed unsuccessful guarded attempt remains immutable')
    with gzip.open(before.parent/'run.log.gz', 'rt') as stream:
        prior = stream.read()
    reference.need('frame=5266 ' in prior and 'x=835,901' in prior,
                   'Observed guarded attempt had66 pixel gap, below original128 minimum')
    scope = json.loads((ROOT/'audit_native_guard_campaign_progress/report.json').read_text(encoding='utf-8-sig'))
    paths = [Path(__file__), Path(reference.__file__), Path(transport.__file__), reference.MK3,
             ROOT/'mame-mkp/unidasm.exe', before, before.parent/'run.log.gz',
             ROOT/'audit_native_secondary_finisher_reference/report.json', reference.SOURCE,
             ROOT/reference.current.NAME/'mkport_candidate.exe', reference.PAYLOAD,
             ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
    pins = {str(p.resolve()): reference.sha(p) for p in paths}
    report = dict(passed=True, sourceInputAccepted=True, runtimeAccepted=False,
                  fullPortAcceptance=False, originalInput=mapping, faultRejections=faults,
                  previousGoalTurnClassification='no progress: requested status restatement only',
                  thisGoalTurnClassification='progress: original input record and128..176 separation gate verified; prior66pixel command was outside the actual gate',
                  candidateGuestSHA256=hashlib.sha256(program).hexdigest().upper(),
                  originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],
                  inputHashes=pins, newBuilds=0, newROMCopies=0, newRawMedia=0,
                  newZIPs=0, gameSourceChanged=False, latestPlayableChanged=False,
                  goalStatus='active',
                  nextAction='Physically earn the same original finish window, walk backward to144pixel separation, send LP/Block/Block/HK and passively observe the actual native first performer.')
    reference.need(len(report['originalNaturalIntegrationRequirements']) == 14 and
                   len(report['originalRemainingWorkGroups']) == 6, 'Full14+6 scope preserved')
    reference.need(all(reference.sha(p) == h for p, h in pins.items()), 'Actual source and candidate conserved')
    OUT.mkdir()
    with gzip.open(OUT/'executed_sources.json.gz', 'wt', encoding='utf-8') as stream:
        json.dump({str(p.resolve()): dict(sha256=pins[str(p.resolve())], text=p.read_text())
                   for p in paths if p.suffix == '.py'}, stream)
    (OUT/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(passed=True, input=mapping, rejectedFaults=len(faults),
                          gameSourceChanged=False, runtimeAccepted=False)))


if __name__ == '__main__':
    main()
