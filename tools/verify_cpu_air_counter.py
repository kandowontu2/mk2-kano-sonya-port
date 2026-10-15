"""Decode the actual compiled counter/guard words, not native catch acceptance.

Models only their TMS instructions. Native helper outcomes are test parameters,
not values injected into the game. MMTM/MMFM masks follow 34010ops.hxx.
"""
import re
from verify_cpu_air_gate import ROOT, rows


def execute(words, base, identity, airborne, gap=78, chance=False, guard=False):
    initial = [identity if guard and i == 0 else 0x12340000 + i for i in range(7)]
    regs, stack, calls = initial.copy(), [], []
    pc, zero, carry, high = 0, False, False, False
    for _ in range(60):
        op = words[pc]
        if op == 0x098f:
            mask = words[pc + 1]
            for index in range(16):
                if mask & (0x8000 >> index):
                    if index >= len(regs):
                        raise ValueError('Unsupported save register')
                    stack.append(regs[index])
            pc += 2
        elif op == 0x09af:
            mask = words[pc + 1]
            for index in range(15, -1, -1):
                if mask & (1 << index):
                    if index >= len(regs) or not stack:
                        raise ValueError('Unbalanced restore')
                    regs[index] = stack.pop()
            pc += 2
        elif op == 0xb500 and words[pc + 1] == 0x1f0:
            regs[0] = identity
            pc += 2
        elif op in (0x0b40, 0x0b43):
            value, constant = regs[op & 15], ~words[pc + 1] & 0xffff
            zero, carry, high = value == constant, value < constant, value > constant
            pc += 2
        elif op == 0x09c0:
            regs[0] = words[pc + 1]
            pc += 2
        elif op == 0x09e6:
            regs[6] = words[pc + 1] | words[pc + 2] << 16
            pc += 3
        elif op == 0x0d5f:
            target = words[pc + 1] | words[pc + 2] << 16
            calls.append(target)
            if target == 0xff80ec20 and regs[0] != 250:
                raise ValueError('Native chance threshold changed')
            for index in range(4):
                regs[index] = 0xdead0000 + index
            if target == 0xff837bf0:
                carry = airborne
            elif target == 0xff834cc0:
                regs[3] = gap
            elif target == 0xff80ec20:
                carry = chance
            else:
                raise ValueError('Unknown native helper')
            pc += 3
        elif op in (0xc080, 0xcb80, 0xc980, 0xc380):
            target = words[pc + 1] | words[pc + 2] << 16
            taken = op == 0xc080 or op == 0xcb80 and not zero or op == 0xc980 and not carry or op == 0xc380 and high
            if taken:
                if base <= target < base + len(words) * 16:
                    if (target - base) % 16:
                        raise ValueError('Unaligned branch')
                    pc = (target - base) // 16
                    continue
                if stack:
                    raise ValueError('Counter leaves saved registers on native stack')
                expected = initial.copy()
                if target == 0xff9c8180:
                    expected[6] = 0xff9beef0
                if regs != expected:
                    raise ValueError('Original arguments/identity not preserved')
                return target, calls
            pc += 3
        elif op == 0x0300:
            pc += 1
        else:
            raise ValueError(f'Unexpected executed counter opcode {op:04X} at word {pc}')
        if not 0 <= pc < len(words):
            raise ValueError('Counter escaped allocation')
    raise ValueError('Counter did not terminate')


def words_from_log(log):
    found = [r for r in rows(log, 'MK2_CPU_AIR_ROM') if r['start'] == 'FFFCA000']
    if len(found) != 1:
        raise ValueError('Actual compiled counter ROM dump missing')
    return [int(word, 16) for word in found[0]['words'].split(',')]


def verify_compiled(log):
    words = words_from_log(log)
    if len(words) != 256:
        raise ValueError('Both compiled counter variants and guard required')
    count = 0
    for offset, base, fallback in ((0, 0xfffca000, 0xff8704e0), (128, 0xfffca800, 0xff870620)):
        for identity in range(19):
            for airborne in (False, True):
                for gap in (95, 96, 97):
                    for chance in (False, True):
                        target, calls = execute(words[offset:offset + 64], base, identity, airborne, gap, chance)
                        wanted = 0xff9c8180 if identity == 17 and airborne and gap <= 96 and chance else fallback
                        if target != wanted:
                            raise ValueError('Wrong native counter choice/fallback')
                        if 0xff80ec20 in calls and not (identity == 17 and airborne and gap <= 96):
                            raise ValueError('Stock/grounded/out-of-range RNG consumed')
                        count += 1
    for identity in (11, 17):
        for airborne in (False, True):
            target, _ = execute(words[64:96], 0xfffca400, identity, airborne, guard=True)
            wanted = 0xff9bf050 if identity == 17 and not airborne else 0xff9bef40
            if target != wanted:
                raise ValueError('Grounded victim caught or Jax callback altered')
            count += 1
    return {'compiled_branches': count, 'CPU_catch_runtime_acceptance': False}


if __name__ == '__main__':
    import sys
    from pathlib import Path
    import json
    for name in sys.argv[1:]:
        try:
            print(json.dumps(verify_compiled((Path(name) / 'run.log').read_text(encoding='utf-8-sig'))))
        except ValueError as error:
            print(json.dumps({'passed': False, 'error': str(error)}))
            raise SystemExit(1)
