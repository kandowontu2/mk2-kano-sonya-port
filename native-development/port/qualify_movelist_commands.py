"""Finite documentation/table agreement; not runtime or complete movelist approval."""
import json
import re
from inspect_normal_runtime import PORT, BASE, sha

SPECS = (
    ('ks_knife_command', 'D B', 'Knife:            D, B + HP.'),
    ('ks_blade_command', 'D F', 'Blade:            D, F + HP.'),
    ('ks_ring_command', 'D F', 'Ring:             D, F + LP.'),
    ('ks_square_command', 'F B', 'Square wave:      F, B + HP'),
    ('ks_bike_command', 'B B D', 'Bicycle kick:     B, B, D + HK.'),
    ('ks_extract_command', 'B D F', 'Skeleton extract: B, D, F + HK'),
    ('ks_kiss_command', 'B F D D', 'Flame kiss:       B, F, D, D + LP.'),
    ('ks_bubble_command', 'U U B D', 'Death orb:        Hold BL before starting U, U, B, D + HK'),
    ('ks_kano_stage_command', 'U U B', 'Tomb/Pit II:      U, U, B + LK'),
    ('ks_sonya_stage_command', 'F F D', 'Tomb/Pit II:      F, F, D + HP'),
    ('ks_kano_baby_combo', 'F F D D', 'Babality:         F, F, D, D + LK'),
    ('ks_sonya_baby_combo', 'D D F', 'Babality:         D, D, F + LK'),
    ('ks_fs_sonya_directions', 'B F B D', 'Friendship:       B, F, B, D + BL'),
    ('ks_scom_st_kano', 'B D B', 'Kano:             B, D, B + LK.'),
)


def table_rows(source, label):
    tail = source.split('\n' + label + '\n', 1)[1]
    block = re.split(r'\n(?=[A-Za-z_])', tail, maxsplit=1)[0]
    return [[v.strip().lower() for v in row.split(',')]
            for row in re.findall(r'(?im)^\s*\.word\s+([^;\n]+)', block)]


def expected_row(command, facing_right):
    direction = dict(D='sw_down', U='sw_up',
                     F='sw_right' if facing_right else 'sw_left',
                     B='sw_left' if facing_right else 'sw_right')
    switches = [direction[v] for v in command.split()][::-1]
    return switches + ['0'] * (6 - len(switches))


def qualify():
    src = BASE / 'mk2-rebuild-main/srcp'
    command = (src / 'KSCMD.ASM').read_text()
    baby = (src / 'MKBABY.ASM').read_text()
    friend = (src / 'MKFRIEND.ASM').read_text()
    moves = (src / 'MOVES.ASM').read_text()
    document = (PORT / 'MOVELIST_NATIVE.txt').read_text()
    cases = []
    for label, inputs, line in SPECS:
        assert line in document, ('Document changed; review command wording', label)
        source = (baby if 'baby_combo' in label else friend if label.startswith('ks_fs_')
                  else moves if label.startswith('ks_scom_') else command)
        rows = table_rows(source, label)
        assert rows[1:3] == [expected_row(inputs, True), expected_row(inputs, False)], label
        cases.append(dict(label=label, writtenDirections=inputs, bothFacingTablesMatched=True))
    laser = table_rows(command, 'ks_laser_command')
    assert laser[1] == ['sw_hi_kick', 'sw_block', 'sw_block', 'sw_lo_punch', '0', '0']
    assert 'Eye laser:        LP, BL, BL, HK' in document
    friendship = table_rows(friend, 'ks_fs_kano_buttons')
    assert friendship[1] == ['sw_hi_kick', 'sw_block', 'sw_block', 'sw_lo_kick', '0', '0']
    assert 'Friendship:       LK, BL, BL, HK' in document
    for text, label, end in ((friend, 'fs_check', 'ks_fs_kano'), (baby, 'bb_check', 'bbno')):
        block = text.split('\n' + label + '\n', 1)[1].split('\n' + end, 1)[0]
        assert re.search(r'movi\s+l_hp,a0\s+callr\s+\w+\s+jrne', block)
        assert re.search(r'movi\s+l_lp,a0\s+callr\s+\w+\s+jrne', block)
    for label, actor in (('do_st_2_kano', 17), ('do_st_2_sonya', 18)):
        block = moves.split('\n' + label + '\n', 1)[1]
        assert re.match(r'\s*movi\s+' + str(actor) + r',a9\s+jruc\s+shang_morph', block)
    for label, end in (('st_block', 'ks_st_block_original'), ('st_lo_punch', 'ks_st_lp_original')):
        block = moves.split('\n' + label + '\n', 1)[1].split('\n' + end, 1)[0]
        assert 'calla ks_leg_chord' in block and 'movi do_st_2_sonya,a7' in block
    assert "Sonya:            D + LP + BL" in document
    return dict(scope='14 directional tables in both facings, two button histories, no-punch gates and true-ID morph dispatch match documented entries',
                cases=cases, laserButtonHistoryMatched=True,
                friendshipButtonHistoryMatched=True, nativeNoPunchSourceGatesVerified=True,
                trueIdentityMorphSourceDispatchVerified=True,
                allRuntimeEligibilityAndChordGatesVerified=False, fullPortVerified=False,
                pins={str(p): sha(p) for p in (src / 'KSCMD.ASM', src / 'MKBABY.ASM',
                    src / 'MKFRIEND.ASM', src / 'MOVES.ASM', PORT / 'MOVELIST_NATIVE.txt')})


if __name__ == '__main__':
    report = qualify()
    (PORT / 'MOVELIST_COMMAND_QUALIFICATION.json').write_text(json.dumps(report, indent=2) + '\n')
    print(report['scope'])
