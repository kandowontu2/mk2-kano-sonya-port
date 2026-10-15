"""Compiled native CPU air-catch routing, not a full air-throw acceptance gate.

The small interpreter follows the actual dumped TMS instructions. It proves
identity routing for 19 IDs, not that the native AI requests or completes catches.
"""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGINAL_SHA = '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
GATE, END, ROUTER = 0xff9beef0, 0xff9bf2c0, 0xfffc8700
ELIGIBLE, FALLBACK = 0xff9bef40, 0xff9bf050
NAME = 'diagnostic_v388_native_cpu_air_catch'
EXE = '3CFEC2D7AD571CF0FD79D019FC35FF1188ADB4042F5A7AB2994CAD001A117F85'
PAYLOAD = '82FE153FB56B46A6F9D42F493451AC3D59AD61713433714ACA7704E2881F8951'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def rows(log, tag):
    result = []
    for line in log.splitlines():
        if not line.startswith(tag + ' '):
            continue
        pairs = re.findall(r'(\w+)=([^\s]+)', line)
        if len({key for key, _ in pairs}) != len(pairs):
            raise ValueError('Duplicate log field')
        result.append(dict(pairs))
    return result


def route(words, identity):
    """Execute only MOVE ID, CMPI, short JREQ and absolute JA; fail closed."""
    pc, a0, zero = 0, None, False
    for _ in range(12):
        op = words[pc]
        if op == 0xb500 and words[pc + 1] == 0x1f0:
            a0 = identity
            pc += 2
        elif op == 0x0b40:
            zero = a0 == (~words[pc + 1] & 0xffff)
            pc += 2
        elif op & 0xff00 == 0xca00 and op & 255 not in (0, 128):
            displacement = op & 255
            if displacement >= 128:
                displacement -= 256
            pc += 1 + (displacement if zero else 0)
        elif op == 0xc080:
            return words[pc + 1] | words[pc + 2] << 16, a0
        else:
            raise ValueError('Unexpected executed router opcode at word ' + str(pc))
        if not 0 <= pc < len(words):
            raise ValueError('Router branch escapes allocation')
    raise ValueError('Router failed to terminate')


def verify_dump(log, original):
    dumps = rows(log, 'MK2_CPU_AIR_ROM')
    if len(dumps) != 2:
        raise ValueError('Two compiled ROM windows required')
    by_start = {int(r['start'], 16): r for r in dumps}
    gate, router = by_start[GATE], by_start[ROUTER]
    for row in dumps:
        if row['writes'] != '0' or row['assistance'] != 'none':
            raise ValueError('ROM observer is assisted')
    if int(gate['stop'], 16) != END or int(router['stop'], 16) != ROUTER + 256:
        raise ValueError('Wrong compiled ROM range')
    gw = [int(x, 16) for x in gate['words'].split(',')]
    rw = [int(x, 16) for x in router['words'].split(',')]
    if len(gw) != (END - GATE) // 16 or len(rw) != 16:
        raise ValueError('Incomplete ROM dump')
    if gw[:5] != [0xc080, 0x8700, 0xfffc, 0x0300, 0x0300]:
        raise ValueError('Wrong gate trampoline')
    at = (GATE - 0xff800000) // 8
    stock = list(struct.unpack_from('<' + 'H' * len(gw), original, at))
    if stock[:5] != [0xb500, 0x01f0, 0x0b40, 0xfff4, 0xcb11]:
        raise ValueError('Unsupported original identity gate')
    if gw[5:] != stock[5:]:
        raise ValueError('Original eligibility/action/stack-unwind code altered')
    matrix = []
    for identity in range(19):
        target, a0 = route(rw, identity)
        expected = ELIGIBLE if identity in (11, 17) else FALLBACK
        if target != expected or a0 != identity:
            raise ValueError('Wrong or aliased identity route: ' + str(identity))
        matrix.append({'identity': identity, 'target': f'{target:08X}', 'a0': a0})
    if rw[14:] != [0xffff, 0xffff]:
        raise ValueError('Router exceeds allocation')
    return matrix


def matched_launch(folder, observer_name, runner_name):
    folder = Path(folder)
    launch = json.loads((folder / 'result.json').read_text(encoding='utf-8-sig'))
    if launch['exit_code'] != 0 or launch['assistance'] != 'none':
        raise ValueError('Nonterminal/assisted/failed launch')
    if (launch['candidate'], launch['executable_sha256'], launch['payload_sha256']) != (NAME, EXE, PAYLOAD):
        raise ValueError('Exact current candidate required')
    for path, expected in launch['input_hashes'].items():
        if digest(path) != expected:
            raise ValueError('Changed launch input: ' + path)
    build = json.loads((folder / 'input_sources/build-info.json').read_text(encoding='utf-8-sig'))
    for path, expected in build['input_hashes'].items():
        if digest(path) != expected:
            raise ValueError('Changed build input: ' + path)
    observer = (folder / 'input_sources' / observer_name).read_text()
    if re.search(r'write_u\d+|load_state|\.value\s*=(?!=)', observer):
        raise ValueError('Observer writes guest state')
    runner = (folder / 'input_sources' / runner_name).read_text()
    if '-nocheat' not in runner:
        raise ValueError('Cheat-disabled launch missing')
    original = ROOT / 'mk2/mk2-maincpu.bin'
    if digest(original) != ORIGINAL_SHA:
        raise ValueError('Original MKII binary changed')
    log = (folder / 'run.log').read_text(encoding='utf-8-sig')
    if '[LUA ERROR]' in log or 'Fatal error:' in log:
        raise ValueError('Runtime error')
    return launch, log, original.read_bytes()


def verify_case(folder):
    launch, log, original = matched_launch(folder, 'mk2ks_cpu_air_gate_v2_probe.lua', 'run_cpu_air_gate_v2_probe.ps1')
    matrix = verify_dump(log, original)
    select = rows(log, 'MK2_P1CPU_SELECT_RESULT')
    summary = rows(log, 'MK2_CPU_AIR_RESULT')
    if len(select) != 1 or len(summary) != 1 or summary[0]['schema'] != '1':
        raise ValueError('Incomplete selection/terminal evidence')
    if int(select[0]['checks']) != 39 or select[0]['errors'] != '0' or int(select[0]['live']) <= 0:
        raise ValueError('Real P2 selection failed')
    fields = rows(log, 'MK2_CPU_AIR_FIELD')
    if len(fields) < 500:
        raise ValueError('Insufficient native gameplay fields')
    for row in fields + rows(log, 'MK2_CPU_AIR_EVENT') + rows(log, 'MK2_CPU_AIR_HEALTH'):
        if row['writes'] != '0' or row['assistance'] != 'none' or row['cstate'] != '0' or row['hstate'] != '1':
            raise ValueError('Assisted or incorrect actual controllers')
        for prefix in ('c', 'h'):
            if row[prefix + 'id'] != row[prefix + 'roster'] or row[prefix + 'actor'] != row[prefix + 'owner']:
                raise ValueError('Proxy identity or process ownership')
    events = rows(log, 'MK2_CPU_AIR_EVENT')
    for event in events:
        if int(event['pc'], 16) != int(event['entry'], 16) + 16:
            raise ValueError('Not an actual instruction fetch')
    return {'compiled_gate_passed': True, 'identity_routes': matrix,
            'native_fields': len(fields), 'native_gate_entries': sum(e['entry'] == 'FF9BEEF0' for e in events),
            'native_catch_entries': int(summary[0]['actions']),
            'full_CPU_air_throw_acceptance': False, 'scope': 'compiled routing plus input-only scouts, not full catches'}


def verify_recovery_case(folder, player):
    from verify_cpu_recovery import verify_log
    launch, log, _ = matched_launch(folder, 'mk2ks_cpu_recovery_probe.lua', 'run_cpu_recovery_probe.ps1')
    if launch['player'] != player:
        raise ValueError('Wrong recovery player')
    proof = verify_log(log, player)
    if not proof['passed']:
        raise ValueError('Native full-pair recovery failed: ' + str(proof['errors']))
    return proof


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folders', nargs='+')
    args = parser.parse_args()
    for folder in args.folders:
        try:
            print(json.dumps({'folder': folder, **verify_case(folder)}, indent=2))
        except (ValueError, KeyError, IndexError) as error:
            print(json.dumps({'folder': folder, 'passed': False, 'error': str(error)}))
            raise SystemExit(1)
