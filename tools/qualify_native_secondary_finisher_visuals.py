"""Compile the staged initializer in a small harness, not a playable game.

All ROM buffers stay in RAM. A tiny generated opcode slice is disassembled
and removed after checking. Original traces are passive frozen evidence.
This cannot accept victim/audio/input/CPU/physics or an entire finisher.
"""
import gzip
import hashlib
import json
import re
import struct
import subprocess
import traceback
from pathlib import Path

import native_cpu_finisher_spacing_context as prior
import native_process_census_v6647 as native

ROOT = prior.ROOT
STAGE = ROOT/'source_native_secondary_finisher_visuals'
OUT = ROOT/'audit_native_secondary_finisher_visuals_source'
FIRST, LAST = 0xad000, 0xad800
BEGIN, END = '// SECONDARY_FINISHER_VISUALS_BEGIN', '// SECONDARY_FINISHER_VISUALS_END'
TABLES = (0xad000, 0xad200, 0xad300, 0xad340)
ENTRIES = (0xad400, 0xad440, 0xad480, 0xad4c0)
SOURCE_PINS = {
    'midtunit_m.cpp': 'DF2A57916147482AF17BCC560293C2F32173CE8699E0BBD22A5D2E997B9ABA0B',
    'midtunit.h': '43CF38B7D12B9161E3274F2D21C5258534C3DA2C68DD137B331EAFC458D925E5',
    'midtunit.cpp': '30FEDAD4216D86217E6A69111FD16E907DF63D0CAB3B99AE33C82C53C6B1DD61',
}
REFERENCE_PINS = {
    'audit_native_kano_laser_reference_checked/report.json': 'C5625D1D812AF001288909F6F7EF8BCF3266D36805E900C0206FBC7F3CB36392',
    'audit_native_sonya_orb_reference_checked/report.json': 'C5C273214E603826A7FBB59762FDF6368EC68831D22F6F80E2CF585689A40BDA',
    'audit_native_secondary_finisher_reference/report.json': '1D753C449B10DA8BEE0E41CA6795CBCDC694608A226CD2E377608B7E4B18A67C',
}


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def address(byte):
    return 0xff800000 + byte*8


def u32(data, at):
    return struct.unpack_from('<I', data, at)[0]


def source_block():
    old = (ROOT/'source_native_cpu_finisher_spacing/midtunit_m.cpp').read_text()
    proposed = (STAGE/'midtunit_m.cpp').read_text()
    need(proposed.count(BEGIN) == proposed.count(END) == 1, 'Unique staged implementation markers')
    start, end = proposed.index('\t'+BEGIN), proposed.index(END)+len(END)
    need(proposed[:start-1]+proposed[end+1:] == old,
         'Exactly one appended initializer block; every prior game/source byte conserved')
    for leaf, expected in SOURCE_PINS.items():
        need(sha(ROOT/'source_native_cpu_finisher_spacing'/leaf) == expected, 'Frozen prior source '+leaf)
        if leaf != 'midtunit_m.cpp':
            need(sha(STAGE/leaf) == expected, 'Unchanged staged platform '+leaf)
    for leaf, expected in REFERENCE_PINS.items():
        need(sha(ROOT/leaf) == expected, 'Frozen accepted original reference '+leaf)
        receipt = json.loads((ROOT/leaf).read_text())
        need(receipt['passed'] and all(sha(p) == h for p, h in receipt['inputHashes'].items()),
             'Actual accepted reference and every dependency unchanged')
    return proposed[start:end], old


def original_rows():
    """Expand source grammar independently, using actual ROM tokens/loops."""
    donor = (ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    need(hashlib.sha256(donor).hexdigest().upper() ==
         '1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651',
         'Actual original donor ROM')
    stream = struct.unpack_from('<48I', donor, (0xff830f00-0xff800000)//8)
    rows, segment, i = [], 0, 0
    while i < len(stream):
        own = effect = 0
        token = stream[i]
        i += 1
        if token == 0:
            segment += 1
            if segment == 3:
                break
            continue
        if token == 11:
            need(stream[i] == 0xff831640, 'Original bootstrap precedes first actual effect step')
            i += 1
            continue  # allocation proceeds directly into the next real step
        if token in (12, 14):
            effect = stream[i]-0x01000000
            i += 1
            if token == 12:
                own = stream[i]-0x01000000
                i += 1
        else:
            need(token >= 0xff800000, 'No donor control token admitted as a composite')
            own = token-0x01000000
        rows.append((segment, own, effect, 6 if segment == 1 else 4))
    parts = [[(own, effect, ticks) for seg, own, effect, ticks in rows if seg == s] for s in range(3)]
    laser = parts[0]+parts[1]*4+parts[2]
    need(len(laser) == 36 and sum(r[2] for r in laser) == 176, 'Original four sustain repetitions and arm return')
    intro = [0xfe8402c0, 0xfe840340, 0xfe8403c0, 0xfe840440, 0xfe8404c0,
             0xfe840540, 0xfe8405c0, 0xfe840640, 0xfe8406c0, 0xfe840740, 0xfe8407a0]
    orb = struct.unpack_from('<21I', donor, (0xff83f3c0-0xff800000)//8)
    need(orb[7] == orb[14] == orb[18] == orb[20] == 0 and
         orb[12:14] == (1, 0xff83f4c0), 'Original growth, looping travel, retirement and separate unused tail')
    grow = [(g, 0, 3) for g in intro]+[(0, g-0x01000000, 3) for g in orb[:7]]
    travel = [(0, g-0x01000000, 3) for g in orb[8:12]]
    retire = [(0, g-0x01000000, 4) for g in orb[15:18]]
    return (laser, grow, travel, retire)


def expected_tables(base):
    guest = bytearray(base)
    need(all(b == 255 for b in base[FIRST:LAST]), 'Actual initialized program allocation is unused FF')
    original = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(all(b == 255 for b in original[FIRST:LAST]), 'Original stock program allocation is unused FF')
    for at, rows in zip(TABLES, original_rows()):
        for row in rows+[(0, 0, 0)]:
            struct.pack_into('<III', guest, at, *row)
            at += 12
    struct.pack_into('<II', guest, 0xad380, 0xfe831640, 0)
    struct.pack_into('<II', guest, 0xad390, 0xfe83fda0, 0)
    return guest


HARNESS_HEADER = r'''
#include <cstdint>
#include <cstdio>
#include <iostream>
#include <initializer_list>
#include <iterator>
#include <stdexcept>
#include <io.h>
#include <fcntl.h>
template<class... Args> void fatalerror(const char *message, Args...) { throw std::runtime_error(message); }
int main() {
    _setmode(_fileno(stdin), _O_BINARY); _setmode(_fileno(stdout), _O_BINARY);
    uint8_t memory[0x100000]; uint8_t *rom=memory;
    std::cin.read(reinterpret_cast<char *>(rom), sizeof(memory));
    if (std::cin.gcount()!=sizeof(memory)) return 2;
    auto write16=[&](unsigned at,uint16_t value) { rom[at]=value; rom[at+1]=value>>8; };
    auto write32=[&](unsigned at,uint32_t value) { for(unsigned b=0;b<4;b++) rom[at+b]=value>>(b*8); };
    auto native_address=[](unsigned at) { return 0xff800000U+at*8; };
    constexpr unsigned leg_parser=0xf0000,leg_action=0xf0100;
'''


def harness_code(block, old):
    start = old.index('\tunsigned leg_cursor = leg_parser, leg_limit = leg_action;')
    end = old.index('\n\t// LP and Block events', start)
    start_poses = old.index('\tconstexpr uint32_t sonya_pose_groups[]={')
    end_poses = old.index('};', start_poses)+2
    return HARNESS_HEADER+old[start:end]+'\n(void)leg_cooperate;\n'+old[start_poses:end_poses]+'\n'+block+r'''
    std::cout.write(reinterpret_cast<char *>(rom), sizeof(memory));
    return std::cout ? 0 : 3;
}
'''


def compile_initializer(code, base):
    probe = OUT/'initializer_probe.exe'
    compile_run = subprocess.run([r'C:\Strawberry\c\bin\g++.exe', '-std=c++17', '-O1',
                                  '-Wall', '-Wextra', '-Werror', '-x', 'c++', '-', '-o', str(probe)],
                                 input=code, text=True, capture_output=True)
    (OUT/'compiler.log').write_text(compile_run.stdout+compile_run.stderr)
    need(compile_run.returncode == 0, 'Actual C++ initializer compiled without warnings')
    run = subprocess.run([str(probe)], input=base, capture_output=True)
    (OUT/'initializer.stderr').write_bytes(run.stderr)
    need(run.returncode == 0 and len(run.stdout) == len(base), 'Actual emitted C++ initializer returned the whole buffer')
    return run.stdout, probe


def disassemble_helpers(guest):
    # 1 KiB of generated new code only. Never write a duplicated whole ROM.
    binary = OUT/'generated_helpers.bin'
    binary.write_bytes(guest[0xad400:0xad800])
    run = subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'), str(binary), '-arch', 'tms34010',
                          '-basepc', hex(address(0xad400)), '-norawbytes'],
                         text=True, capture_output=True, check=True)
    instructions = {int(line.split(':', 1)[0], 16):line.split(':', 1)[1].strip()
                    for line in run.stdout.splitlines()}
    return instructions, binary


def inspect_helpers(guest, instructions):
    # Reviewed actual unidasm output: all entries, row reader, conditional
    # allocator, paired renderer, task-stack exit, both short allocators,
    # native group registration and the facing-relative positioning helper.
    need(hashlib.sha256(guest[0xad400:0xad800]).hexdigest().upper() ==
         'A664D041A7D5EC01B607B4A3CFD0666080C36DA8CEBB6DCAE79F55CAF3C5321E',
         'Every reviewed helper instruction, target, immediate and reserved padding conserved')
    expected_starts = {
        0xad500: 'MOVE   *A9+,A0,1',
        0xad502: 'ADDI   20h,A9',
        0xad506: 'MOVE   *A9+,A10,1',
        0xad508: 'MOVE   A10,A10',
        0xad680: 'MMTM   SP,A10,A11',
        0xad684: 'MOVE   A8,-*SP,1',
        0xad780: 'MOVE   *A13(190h),A0,1',
    }
    for at, text in expected_starts.items():
        need(instructions[address(at)] == text, 'Actual native helper instruction '+text)
    pair = [text for pc, text in instructions.items() if address(0xad500)<=pc<address(0xad600)]
    need('CALL   A11' in pair and 'CALLA  FF80DCC0h' in pair and
         'MMFM   A12,A7' in pair and 'EXGPC  A7' in pair,
         'Actual native allocator callback, scheduler and coroutine return')
    need(pair.count('CALLA  FF838790h') == 2,
         'Separate ordinary renderer calls for own actor and child')
    create = [text for pc, text in instructions.items() if address(0xad680)<=pc<address(0xad780)]
    need('CALLA  FF83AE20h' in create and 'CALLA  FF83F610h' in create and
         'MMFM   SP,A10,A11' in create and 'MOVE   A10,*A13(190h),1' in create,
         'Native group allocation/list registration, cadence/callback preservation and child ownership')
    need(not any('(140h)' in t or '(170h)' in t or t.startswith('MOVE') and ',@' in t
                 for pc, t in instructions.items() if address(0xad400)<=pc<address(0xad800)),
         'No true opponent/process/global identity/HP/AI pointer replacement')
    for at, table in zip(ENTRIES, TABLES):
        need(instructions[address(at)] == f'MOVI   {address(table):08X}h,A9' and
             instructions[address(at+6)] == f'MOVI   {address(0xad600 if table==TABLES[0] else 0xad640):08X}h,A11' and
             instructions[address(at+12)] == f'JA     {address(0xad500):08X}h',
             'Every entry selects its typed stream and native allocator')


def pair_cpu_model(guest, entry):
    """Unit model of emitted TMS words, not emulator/runtime evidence.

    Deliberately poison renderer/sleep-clobbered registers. Check that only
    task-stack state survives a yield and no global return remains live.
    """
    registers = [0]*16
    registers[8], registers[13] = 0x1000, 0x2000
    registers[12] = 0x3000
    pc, zero, fields, child = address(entry), False, 21, 0
    system_stack, task_stack = [], [0x12345678]
    events, sleeps, allocations = [], [], 0
    memory = {}
    def load(at):
        if at >= 0xff800000:
            return u32(guest, (at-0xff800000)//8)
        return memory.get(at, 0)
    def poison():
        for reg in range(7):
            registers[reg] = 0xfade0000+reg
    for steps in range(5000):
        need(pc & 15 == 0, 'Native instruction fetch is word-aligned, never rounded to a byte offset')
        offset = (pc-0xff800000)//8
        op = struct.unpack_from('<H', guest, offset)[0]
        pc += 16
        if 0x09e0<=op<=0x09ef:
            registers[op-0x09e0] = u32(guest, offset+2)
            pc += 32
        elif op in (0xc080, 0xca80, 0xcb80):
            target = u32(guest, offset+2)
            if op == 0xc080 or (op == 0xca80 and zero) or (op == 0xcb80 and not zero):
                pc = target
            else:
                pc += 32
        elif op in (0x9720, 0x972a):
            reg = 0 if op == 0x9720 else 10
            registers[reg] = load(registers[9])
            registers[9] += 32
            zero = registers[reg] == 0
        elif op == 0x0b09:
            registers[9] += struct.unpack_from('<H', guest, offset+2)[0]
            pc += 16
        elif op in (0x4d4a, 0x4c00, 0x4c21):
            zero = registers[{0x4d4a:10, 0x4c00:0, 0x4c21:1}[op]] == 0
        elif op == 0xb720:
            displacement = struct.unpack_from('<h', guest, offset+2)[0]
            registers[0] = load(registers[9]+displacement)
            zero = registers[0] == 0
            pc += 16
        elif op in (0xb7a1, 0xb7a8):
            reg = 1 if op == 0xb7a1 else 8
            displacement = struct.unpack_from('<H', guest, offset+2)[0]
            registers[reg] = load(registers[13]+displacement)
            zero = registers[reg] == 0
            pc += 16
        elif op == 0x092b:
            need(registers[11] in (address(0xad600), address(0xad640)), 'Typed allocator callback remains intact')
            child, allocations = 0x4000, allocations+1
            memory[registers[13]+0x190] = child
            poison()
        elif op == 0xa30f:
            system_stack.append(registers[8])
        elif op == 0x09af:
            need(struct.unpack_from('<H', guest, offset+2)[0] == 0x100 and system_stack,
                 'Native short child draw restores only its own saved actor')
            registers[8] = system_stack.pop()
            pc += 16
        elif op == 0x4d40:
            registers[0] = registers[10]
        elif op == 0x0d5f:
            target = u32(guest, offset+2)
            pc += 32
            if target == 0xff838790:
                need(registers[8] in (0x1000, child) and registers[0]>=0xfe800000,
                     'Composite is drawn on actual owned actor or its distinct child')
                events.append((fields, 'own' if registers[8]==0x1000 else 'child', registers[0]))
                poison()
            elif target == 0xff80dcc0:
                need(not system_stack and registers[8]==0x1000 and 0<registers[0]<=6,
                     'No global stack return or changed actor across the cooperative sleep')
                sleeps.append((fields, registers[0]))
                fields += registers[0]
                poison()
            else:
                raise ValueError('Unexpected pair-model native call')
        elif op == 0x09ac:
            need(struct.unpack_from('<H', guest, offset+2)[0] == 0x80 and len(task_stack)==1,
                 'Exactly the task-local continuation is popped')
            registers[7] = task_stack.pop()
            pc += 16
        elif op == 0x0127:
            need(registers[7]==0x12345678 and not task_stack and not system_stack and registers[8]==0x1000,
                 'Coroutine returns to its native caller with both stacks and actor intact')
            return dict(events=events, sleeps=sleeps, endpoint=fields, allocations=allocations)
        else:
            raise ValueError(f'Unexpected pair-model opcode {op:04X} at {pc-16:08X}')
    raise ValueError('Typed animation does not terminate')


def inspect(guest, base, instructions):
    expected = expected_tables(base)
    need(guest[:FIRST] == base[:FIRST] and guest[LAST:] == base[LAST:],
         'Whole native program outside allocated visuals unchanged, including all dispatch/input/AI/audio')
    need(guest[FIRST:0xad400] == expected[FIRST:0xad400],
         'All actual C++ typed rows/bootstrap/padding match original grammar independently')
    inspect_helpers(guest, instructions)
    assets = json.loads((ROOT/'audit_native_secondary_finisher_reference/report.json').read_text())['originalUnusedAssets']
    owned = [{int(r['group'],16)-0x01000000 for r in a['references']} for a in assets]
    for index, rows in enumerate(original_rows()):
        for own, effect, ticks in rows:
            need((not own or own in owned[0 if index==0 else 1]) and
                 (not effect or effect in owned[0 if index==0 else 2]),
                 'Every typed composite is already imported from the proper original character/effect')
    results = []
    for entry, rows in zip(ENTRIES, original_rows()):
        result = pair_cpu_model(guest, entry)
        age, expected_events, expected_sleeps = 21, [], []
        for own, effect, ticks in rows:
            if own:
                expected_events.append((age, 'own', own))
            if effect:
                expected_events.append((age, 'child', effect))
            expected_sleeps.append((age, ticks))
            age += ticks
        need(result['events'] == expected_events and result['sleeps'] == expected_sleeps and
             result['endpoint'] == age and result['allocations'] == 1,
             'Actual emitted pair code matches complete typed schedule and exactly one effect allocation')
        results.append(result)
    # Recheck every observed original child/own state in the finite early
    # action interval, rather than selecting just convenient phase markers.
    for name, index, actor, end in (('kano',0,'01032970',197), ('sonya',1,'01034A70',75)):
        text = gzip.open(ROOT/f'audit_native_secondary_{name}_source_distance/run.log.gz','rt').read()
        observations = [dict(re.findall(r'(\w+)=([^\s]+)', line), tag=line.split()[0])
                        for line in text.splitlines() if line.startswith('MK3_SECONDARY_')]
        events = results[index]['events']
        for observation in observations:
            age = int(observation.get('age', 0))
            if not 21<=age<end:
                continue
            side = ('child' if observation['tag']=='MK3_SECONDARY_OBJECT' and observation['actor']==actor
                    else 'own' if observation['tag']=='MK3_SECONDARY_FIELD' else None)
            if side:
                history = [e for e in events if e[0]<=age and e[1]==side]
                if not history:  # child not allocated during intro
                    continue
                actual = int(observation['pose'] if side=='child' else observation['poses'].split(',')[0],16)-0x01000000
                need(history[-1][2] == actual, 'Every covered actual original actor/child observation matches staged timing')
    return results


def main():
    need(not OUT.exists() and not native.census(), 'Fresh finite stage evidence and no live port process')
    OUT.mkdir()
    code = ''
    try:
        block, old = source_block()
        base = prior.expected()
        code = harness_code(block, old)
        guest, probe = compile_initializer(code, base)
        instructions, binary = disassemble_helpers(guest)
        results = inspect(guest, base, instructions)
        faults = []
        for name, at in (('Kano_effect_composite',0xad028), ('Kano_cadence',0xad008),
                         ('Sonya_grow_composite',0xad288), ('Sonya_travel_composite',0xad304),
                         ('Sonya_retire_composite',0xad344), ('Kano_bootstrap',0xad380),
                         ('Sonya_bootstrap',0xad390), ('Stock_dispatch',0xf4320),
                         ('Pair_cadence_register',0xad506), ('Pair_allocator_callback',0xad536),
                         ('Pair_native_renderer',0xad542)):
            wrong = bytearray(guest)
            wrong[at] ^= 1
            try:
                inspect(bytes(wrong), base, instructions)
            except ValueError as error:
                faults.append(dict(name=name, rejected=str(error)))
            else:
                raise ValueError('Source fault admitted: '+name)
        scope = json.loads((ROOT/'audit_native_secondary_finisher_reference_progress/report.json').read_text())
        pins = {str((STAGE/leaf).resolve()):sha(STAGE/leaf) for leaf in SOURCE_PINS}
        for leaf in REFERENCE_PINS:
            pins[str((ROOT/leaf).resolve())] = sha(ROOT/leaf)
        pins[str(Path(__file__).resolve())] = sha(__file__)
        pins[str((ROOT/'tools/native_cpu_finisher_spacing_context.py').resolve())] = sha(ROOT/'tools/native_cpu_finisher_spacing_context.py')
        pins[str((ROOT/'audit_native_secondary_finisher_reference_progress/report.json').resolve())] = sha(ROOT/'audit_native_secondary_finisher_reference_progress/report.json')
        report = dict(passed=True, sourceOnlyAccepted=True, nativeRuntimeAccepted=False,
                      completeSecondFatalitiesImplemented=False, fullPortAcceptance=False,
                      previousGoalTurnClassification='no progress: requested status restatement only',
                      thisGoalTurnClassification='progress: staged native owned paired choreography compiled in initializer harness; emitted TMS timing checked independently against original grammar and passive traces',
                      allocatedRange=dict(byteStart=f'{FIRST:X}', byteEndExclusive=f'{LAST:X}', bytes=LAST-FIRST),
                      emittedInitializedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
                      initializedByteDelta=sum(a!=b for a,b in zip(base,guest)),
                      finiteUnitModel=[dict(entry=f'{address(e):08X}', rows=len(r['sleeps']),
                           nativeFields=sum(t for _,t in r['sleeps']), endpoint=r['endpoint'],
                           effectAllocations=r['allocations']) for e,r in zip(ENTRIES,results)],
                      actualHelperDisassembly={f'{pc:08X}':text for pc,text in instructions.items()
                                               if text!='DW     FFFFh'},
                      faultRejections=faults, inputHashes=pins,
                      originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
                      originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],
                      currentPlayableChanged=False, payloadChanged=False, gameBuilds=0, newROMCopies=0,
                      newRawMedia=0, newZIPs=0, goalStatus='active',
                      limitations=['C++ initializer harness and deliberately scoped TMS unit model, not native gameplay.',
                                   'Kano attacker/independent beam stream complete; victim red fade and bones not connected.',
                                   'Sonya attacker/growth/cycle/retirement streams; travel and wrap physics still need implementation.',
                                   'Neither human input nor CPU choice/approach is rebound.',
                                   'Sound and native win/rematch/ladder cleanup remain required.',
                                   'Private staged source only; latest playable and launcher preserved.'],
                      nextAction='Add independent victim/effect physics, palettes, sounds and complete normal finish/cleanup; then wire distinct human and CPU actions in a private compiled game and perform genuine earned-input tests.')
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,
             'Full original objective retained')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        # These are generated tiny test outputs, not a game build or source.
        need(probe.parent.resolve()==OUT.resolve() and binary.parent.resolve()==OUT.resolve(), 'Exact finite generated test files')
        probe.unlink()
        binary.unlink()
        print(json.dumps(dict(passed=True, sourceOnlyAccepted=True,
                              unitModels=report['finiteUnitModel'], rejectedFaults=len(faults),
                              completeSecondFatalitiesImplemented=False)))
    except Exception:
        (OUT/'report.json').write_text(json.dumps(dict(passed=False, failure=traceback.format_exc(),
                            sourceOnlyAccepted=False, nativeRuntimeAccepted=False),indent=2)+'\n')
        raise
    finally:
        paths = [Path(__file__), *(STAGE/leaf for leaf in SOURCE_PINS)]
        with gzip.open(OUT/'executed_sources.json.gz','wt',encoding='utf-8') as stream:
            json.dump(dict(files={str(p.resolve()):dict(sha256=sha(p),text=p.read_text()) for p in paths},
                           actualCompiledInitializerHarness=code),stream)


if __name__ == '__main__':
    main()
