"""Verify original MK3's human-input skeleton reference, not port acceptance."""
import argparse
import json
import re
import struct
from pathlib import Path

from verify_kano_victim_sync import normalize_mk3_sonya_reference, verify as verify_phases


def verify_rom(program):
    def words(address, count):
        return struct.unpack_from('<' + 'H' * count, program, (address - 0xff800000) // 8)
    # Independent original ROM, not constants read from the candidate driver.
    assert words(0xff986380, 5) == (0x30, 9, 7, 7, 9), 'Native F,D,D,F record changed'
    assert words(0xff992d50, 4) == (0x0b41, 0xffbf, 0xc800, 0x00d7), 'Native >=64 charge gate changed'
    assert words(0xff992da0, 4) == (0x09c5, 0x20, 0x09c6, 0x50), 'Native 32..80 distance bounds changed'
    assert words(0xff993190, 3) == (0x48a3, 0xc800, 0x0094), 'Native lower-bound comparison changed'
    assert words(0xff9931c0, 3) == (0x48c3, 0xc300, 0x0091), 'Native upper-bound comparison changed'


def verify(log):
    errors = []
    selection = re.search(r'MK3_FATALITY_SELECTION frame=\d+ ids=0,1 own=([0-9A-F]{8}) victim=([0-9A-F]{8})', log)
    if not selection:
        errors.append('Missing selected P1 Kano/P2 Sonya actor pointers')
    owners = re.search(r'MK3_FATALITY_FINISH_OWNERS frame=\d+ own=([0-9A-F]{8}) victim=([0-9A-F]{8})', log)
    if not owners:
        errors.append('Missing final-round actor owners; actor pointers are rebuilt between rounds')
    own = int(owners[1], 16) if owners else None
    gates = []
    pattern = (r'MK3_FATALITY_INPUT_GATE frame=(\d+) age=\d+ at=([0-9A-F]{8}) '
               r'a0=([0-9A-F]{8}) a1=([0-9A-F]{8}) a5=([0-9A-F]{8}) '
               r'a6=([0-9A-F]{8}) a8=([0-9A-F]{8}) a11=([0-9A-F]{8}) x=(-?\d+),(-?\d+)')
    for match in re.finditer(pattern, log):
        values = match.groups()
        gates.append({'frame': int(values[0]), 'at': int(values[1], 16),
                      'a1': int(values[3], 16), 'a5': int(values[4], 16),
                      'a6': int(values[5], 16), 'own': int(values[6], 16),
                      'record': int(values[7], 16), 'gap': abs(int(values[8]) - int(values[9]))})
    commands = [gate for gate in gates if gate['at'] == 0xff982880 and
                gate['record'] == 0xff986380 and gate['own'] == own]
    accepted = None
    for command in commands:
        frame_gates = [gate for gate in gates if gate['frame'] == command['frame'] and gate['own'] == own]
        charge = next((gate for gate in frame_gates if gate['at'] == 0xff992d50 and gate['a1'] >= 64), None)
        distance = next((gate for gate in frame_gates if gate['at'] == 0xff993160 and
                         gate['a5'] == 32 and gate['a6'] == 80 and 32 <= gate['gap'] <= 80), None)
        dispatch = next((gate for gate in frame_gates if gate['at'] == 0xff9987e0), None)
        action = next((gate for gate in frame_gates if gate['at'] == 0xff9b12e0), None)
        if charge and distance and dispatch and action:
            ordered = [command, charge, distance, dispatch, action]
            if [gates.index(gate) for gate in ordered] == sorted(gates.index(gate) for gate in ordered):
                accepted = {'frame': command['frame'], 'charge_fields': charge['a1'], 'gap': distance['gap']}
                break
    if not accepted:
        errors.append('Missing ordered human command, charge, distance, dispatch and native action gates')
    result = re.search(r'MK3_FATALITY_INPUT_RESULT pass=true fighter=kano round_health_writes=(\d+) '
                       r'position_writes=0 auto_cheat=false action_frame=(\d+) command_gap=(\d+)', log)
    if not result:
        errors.append('Missing input-only result with explicit assistance accounting')
    elif accepted and int(result[2]) <= accepted['frame']:
        errors.append('Fatality pose must follow the native input dispatch')
    if re.search(r'MK3_FATALITY_(?:CLOSE_ASSIST|ORIENTATION_ASSIST|AUTO_CHEAT|STAGE_ASSIST)', log):
        errors.append('Forbidden position/action/stage assistance in the reference')
    if re.search(r'\[LUA ERROR\]|fatal error|access violation', log, re.I):
        errors.append('Emulator or Lua error')
    phases = verify_phases(normalize_mk3_sonya_reference(log), 1, 'sonya')
    errors.extend(phases['errors'])
    return {'passed': not errors, 'scope': 'original_input_and_choreography_reference_not_port_acceptance',
            'assistance': 'round_health_only', 'native_distance_bounds': [32, 80],
            'native_minimum_charge_fields': 64, 'accepted_input': accepted,
            'paired_phases': phases['phases'], 'errors': errors}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log', type=Path)
    parser.add_argument('--program', type=Path, default=Path(__file__).resolve().parent.parent / 'mk3/mk3-maincpu.bin')
    args = parser.parse_args()
    verify_rom(args.program.read_bytes())
    result = verify(args.log.read_text(encoding='utf-8-sig'))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
