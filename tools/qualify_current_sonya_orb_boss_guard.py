"""Current-source bridge and true-opponent boss-guard units; never gameplay.

The preserved dispatch proof actually compiled and decoded the guard. Its
whole dispatch source remains identical in the current compiled source.
Exercise those decoded instructions with opponent/performer identities
deliberately different. All memory here is a local unit model, not a guest.
"""
import hashlib
import json
import struct
import traceback
from pathlib import Path

import verify_native_source_sync as sync

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'audit_current_sonya_orb_boss_guard'
PRIOR = ROOT / 'audit_native_sonya_orb_dispatch_source/report.json'
PRIOR_SHA = '2BC5A604BF8F1CA9BFCAB31B6CB9ACEB3CFA8F3276D4E50BE1BCDF1866FCB139'
ENTRY = 0xffd7b000
ACTION = 0xffd78000
RETIRE = 0xffa14860
need, sha = sync.need, sync.sha


def block(text):
    begin, end = '// SONYA_ORB_DISPATCH_BEGIN', '// SONYA_ORB_DISPATCH_END'
    need(text.count(begin) == text.count(end) == 1, 'Unique complete dispatch block')
    return text[text.index(begin):text.index(end) + len(end)]


def guard_bytes():
    # Independently encoded from the preserved actual native disassembly.
    return struct.pack('<18H', 0xb7a0, 0x140, 0xb404, 0x1f0, 0x0b44,
                       (~12) & 65535, 0xca80, RETIRE & 65535, RETIRE >> 16,
                       0x0b44, (~13) & 65535, 0xca80, RETIRE & 65535,
                       RETIRE >> 16, 0xc080, ACTION & 65535, ACTION >> 16,
                       0xffff)


def execute(program, side, victim_id, performer_id):
    # Independent slots, actual bit-addressed Main/actor field layout.
    mains = (0x01060000, 0x01070000)
    actors = (0x01030000, 0x01040000)
    own, other = side - 1, 2 - side
    regs = [0] * 16
    regs[13], regs[8] = mains[own], actors[own]
    memory = {mains[own] + 0x140: actors[other],
              actors[own] + 0x1f0: performer_id,
              actors[other] + 0x1f0: victim_id}
    original_memory = dict(memory)
    pc, zero, reads = ENTRY, False, []
    for _ in range(20):
        if pc in (ACTION, RETIRE):
            need(memory == original_memory, 'Guard never writes actor/Main/identity')
            return dict(target=pc, reads=reads)
        need(ENTRY <= pc < ENTRY + len(program) * 8, 'Guard stays inside its finite body')
        op = struct.unpack_from('<H', program, (pc - ENTRY) // 8)[0]
        pc += 16

        def word():
            nonlocal pc
            value = struct.unpack_from('<H', program, (pc - ENTRY) // 8)[0]
            pc += 16
            return value

        if op & 0xfc00 == 0xb400:
            src, dst, field = (op >> 5) & 15, op & 15, (op >> 9) & 1
            at = regs[src] + word()
            need(at in memory, 'Every guard read addresses a real local Main/actor field')
            regs[dst] = memory[at] & (0xffffffff if field else 0xffff)
            zero = regs[dst] == 0
            reads.append(dict(address=at, field=field, value=regs[dst]))
        elif op & 0xfff0 == 0x0b40:
            immediate = (~word()) & 0xffff
            if immediate & 0x8000:
                immediate -= 0x10000
            zero = regs[op & 15] == immediate
        elif op in (0xca80, 0xc080):
            target = word() | (word() << 16)
            if op == 0xc080 or zero:
                pc = target
        else:
            raise AssertionError(f'Unexpected guard instruction {op:04X}')
    raise AssertionError('Guard did not return a native route')


def cases(program):
    count = 0
    for side in (1, 2):
        for victim in range(19):
            for performer in range(19):
                got = execute(program, side, victim, performer)
                need(got['target'] == (RETIRE if victim in (12, 13) else ACTION),
                     'Boss immunity follows true opponent, independently of performer identity')
                own, other = side - 1, 2 - side
                need(got['reads'] == [
                    dict(address=(0x01060000, 0x01070000)[own] + 0x140,
                         field=1, value=(0x01030000, 0x01040000)[other]),
                    dict(address=(0x01030000, 0x01040000)[other] + 0x1f0,
                         field=0, value=victim)],
                     'Only opponent pointer then opponent 16-bit ID are consumed')
                count += 1
    return count


def main():
    need(not OUT.exists(), 'Fresh evidence; preserve every earlier report')
    OUT.mkdir()
    try:
        receipt = json.loads(PRIOR.read_text())
        need(sha(PRIOR) == PRIOR_SHA and receipt['passed'] and receipt['sourceOnlyAccepted']
             and not receipt['nativeRuntimeAccepted'], 'Exact actual compiled/decoded prior proof')
        need(all(sha(p) == h for p, h in receipt['inputHashes'].items()),
             'All nine preserved dispatch proof inputs unchanged')
        source = ROOT / 'mame-mkp/src/mame/midway/midtunit_m.cpp'
        staged = ROOT / 'source_native_sonya_orb_dispatch/midtunit_m.cpp'
        need(block(source.read_text()) == block(staged.read_text()),
             'Complete current dispatch block equals actually qualified staged source')
        source_sync = sync.verify()
        expected = {
            'FFD7B000': 'MOVE   *A13(140h),A0,1',
            'FFD7B020': 'MOVE   *A0(1F0h),A4,0',
            'FFD7B040': 'CMPI   Ch,A4', 'FFD7B060': 'JAEQ   FFA14860h',
            'FFD7B090': 'CMPI   Dh,A4', 'FFD7B0B0': 'JAEQ   FFA14860h',
            'FFD7B0E0': 'JA     FFD78000h',
        }
        need(all(receipt['actualNativeDisassembly'].get(p) == v for p, v in expected.items()),
             'Every independently modeled instruction matches actual compiled disassembly')
        cpu = ROOT / 'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp'
        ops = ROOT / 'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx'
        need('#define SRCREG(O)       (((O) >> 5) & 0x0f)' in cpu.read_text()
             and '*rd = RFIELD##F(R##REG(SRCREG(op))+o);' in ops.read_text()
             and 'int32_t t = (int16_t)~PARAM_WORD();' in ops.read_text()
             and 'j_xx_0(Z_FLAG());' in ops.read_text(),
             'Current native CPU defines source register, offset load, complemented compare and EQ')
        good = guard_bytes()
        count = cases(good)
        faults = []
        for label, at, value in (
            ('performer_instead_of_opponent', 0, 0xb700),
            ('wrong_opponent_link', 2, 0x170),
            ('wrong_identity_field', 6, 0x1e0),
            ('wrong_id_width', 4, 0xb604),
            ('missing_Kintaro_immunity', 10, (~11) & 65535),
            ('missing_Shao_Kahn_immunity', 20, (~14) & 65535),
            ('inverted_first_boss_branch', 12, 0xc080),
            ('wrong_normal_victim_action', 30, 0x8008),
        ):
            bad = bytearray(good)
            struct.pack_into('<H', bad, at, value)
            try:
                cases(bytes(bad))
            except (AssertionError, struct.error) as error:
                faults.append(dict(name=label, rejectedBy=str(error)))
            else:
                raise AssertionError('Effective guard fault admitted: ' + label)
        need(cases(good) == count, 'Whole positive restored after every effective fault')
        paths = [Path(__file__), PRIOR, source, staged, cpu, ops,
                 ROOT / 'tools/verify_native_source_sync.py', *map(Path, receipt['inputHashes'])]
        pins = {str(p.resolve()): sha(p) for p in paths}
        report = dict(passed=True, sourceOnlyAccepted=True, nativeRuntimeAccepted=False,
                      fullPortAcceptance=False, goalStatus='active', classification='progress',
                      currentCompileInputsVerified=15, priorProofInputsVerified=9,
                      exactCurrentDispatchSourceConserved=True, localGuardCases=count,
                      protectedVictimIDs=[12, 13], ordinarySecretAddedVictimIDs=[i for i in range(19) if i not in (12, 13)],
                      guardReadOnly=True, effectiveFaultRejections=faults,
                      actualCompiledPriorInstructions=expected, inputHashes=pins,
                      currentSourceSync=source_sync,
                      originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
                      originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],
                      gameBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                      latestPlayableChanged=False,
                      limitations=['Current source bridge and local guard units only; no current gameplay or new runtime evidence.',
                                   'Live worker handoff, entire victim/effect choreography, audio and cleanup remain open.',
                                   'Corrected ordinary IN2 interruption capture remains unexecuted because retained terminal input is denied.'],
                      nextAction='When test access is restored, execute the prepared corrected physical-input interruption capture; preserve broad finisher/victim/stage/campaign runtime requirements.')
        need(all(sha(p) == h for p, h in pins.items()), 'Final fresh whole-file provenance census')
        (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(dict(passed=True, sourceOnlyAccepted=True, nativeRuntimeAccepted=False,
                              cases=count, faults=len(faults), report=str(OUT / 'report.json'))))
    except Exception:
        (OUT / 'failure.json').write_text(json.dumps(dict(passed=False, failure=traceback.format_exc(),
                                                        nativeRuntimeAccepted=False), indent=2) + '\n')
        raise


if __name__ == '__main__':
    main()
