"""Actual four-slot UI captures and rejection of the user's reported failures."""
import re
import unittest
import numpy as np
from PIL import Image
import verify_native_ui_flow_v814 as v

CASES = [('kano', 1), ('sonya', 1), ('kano', 2), ('sonya', 2)]


def change(log, tag, frame, key=None, value=None, contains=None, remove=False):
    lines = log.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith('MK2_UI_'+tag+' ') and f'frame={frame} ' in line and (contains is None or contains in line):
            if remove:lines[i] = ''
            else:
                lines[i], count = re.subn(r'\b'+key+r'=[^\s]+', key+'='+value, line)
                assert count == 1
            return ''.join(lines)
    raise AssertionError('Mutation must touch actual evidence')


MUTATIONS = [
 (0, 'Kano_highlight_proxy', 'SELECT', 991, 'roster', '1', None, False),
 (1, 'Sonya_not_reached', 'SELECT', 992, 'roster', '9', None, False),
 (0, 'horizontal_skip', 'SELECT', 1015, 'roster', '0', None, False),
 (1, 'Sonya_vertical_down_skip', 'SELECT', 1112, 'roster', '9', None, False),
 (0, 'Kano_up_rebound_wrong', 'SELECT', 1135, 'roster', '17', None, False),
 (0, 'committed_ID_changed', 'SELECT', 1171, 'roster', '1', None, False),
 (0, 'selection_field_missing', 'SELECT', 1040, None, None, None, True),
 (0, 'portraits_linger', 'OUTSIDE', 1290, 'kano_matches', '192', None, False),
 (1, 'Sonya_portrait_lingers', 'OUTSIDE', 1290, 'sonya_matches', '192', None, False),
 (0, 'post_selection_field_missing', 'OUTSIDE', 1330, None, None, None, True),
 (0, 'native_ladder_fake_consumer', 'LADDER', 1283, 'pc', 'FF8A0BF0', 'id=17', False),
 (0, 'native_ladder_wrong_ID', 'LADDER', 1283, 'id', '1', 'id=17', False),
 (0, 'native_ladder_proxy_descriptor', 'LADDER', 1283, 'descriptor', '00002B00', 'id=17', False),
 (0, 'native_ladder_wrong_table', 'LADDER', 1283, 'at', 'FFFF3040', 'id=17', False),
 (0, 'native_schedule_changed', 'LIVE', 1814, 'schedule', 'FFFA3000', None, False),
 (0, 'wrong_underlying_Kano', 'FIELD', 1840, 'id', '1', 'slot=1', False),
 (1, 'wrong_underlying_Sonya', 'FIELD', 1840, 'id', '1', 'slot=1', False),
 (2, 'wrong_P2_Kano', 'FIELD', 1840, 'roster', '1', 'slot=2', False),
 (3, 'wrong_P2_Sonya', 'FIELD', 1840, 'roster', '9', 'slot=2', False),
 (0, 'CPU_identity_changed', 'FIELD', 1840, 'id', '1', 'slot=2', False),
 (0, 'wrong_actor_owner', 'FIELD', 1840, 'owner', '010350A0', 'slot=1', False),
 (0, 'wrong_Main_owner', 'FIELD', 1840, 'main', '0106BF30', 'slot=1', False),
 (0, 'CPU_not_human_campaign', 'FIELD', 1840, 'state', '0', 'slot=1', False),
 (0, 'initial_match_field_missing', 'FIELD', 1840, None, None, 'slot=1', True),
 (0, 'terminal_misreported', 'RESULT', 1994, 'frame', '1900', None, False),
 (0, 'snapshot_path_traversal', 'SNAP', 986, 'file', '../ui_0986.png', None, False),
 (0, 'snapshot_wrong_native_roster', 'SNAP', 986, 'roster', '1', None, False),
 (0, 'fake_input_field', 'INPUT', 1195, 'button', 'High Kick', None, False),
 (0, 'actual_confirm_missing', 'INPUT', 1195, None, None, None, True),
 (0, 'actual_match_input_missing', 'INPUT', 1840, None, None, None, True),
 (0, 'duplicate_ambiguous_ID', 'FIELD', 1840, 'id', '17 id=17', 'slot=1', False),
 (0, 'guest_write_assistance', 'FIELD', 1840, 'writes', '1', 'slot=1', False),
]


class NativeUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs = []
        for fighter, side in CASES:
            cls.logs.append(v.launch(v.ROOT/f'audit_v813_ui_{fighter}_p{side}', fighter, side))
        cls.folder = v.ROOT/'audit_v813_ui_kano_p1'
        cls.snapshots = v.records(cls.logs[0], 'SNAP')
        cls.images = {r['file']: np.asarray(Image.open(cls.folder/'snap'/r['file']).convert('RGB')) for r in cls.snapshots}
        cls.ui = (v.ROOT/'roms/mk2ks/mk2ks.ui').read_bytes()

    def test_four_actual_current_native_cases(self):
        for fighter, side in CASES:
            proof = v.verify(v.ROOT/f'audit_v813_ui_{fighter}_p{side}', fighter, side)
            self.assertTrue(proof['passed'])
            self.assertFalse(proof['whole_character_integration_complete'])
            self.assertEqual(proof['first_match_participant_fields'], 362)
            self.assertGreaterEqual(proof['rendered']['native_name_shadow_checks'], 4)

    def visual_reject(self, altered):
        with self.assertRaises(ValueError):
            v.render(self.folder, self.logs[0], 'kano', 1, load=lambda name: altered.get(name, self.images[name]))

    def test_border_shift_one_pixel(self):
        name = next(r['file'] for r in self.snapshots if r['scene'] == 'select' and n(r, 'age') == 55)
        a = self.images[name].copy();a[20:98, 19:23] = a[20:98, 20:24]
        self.visual_reject({name: a})

    def test_border_too_thin(self):
        name = next(r['file'] for r in self.snapshots if r['scene'] == 'select' and n(r, 'age') == 55)
        a = self.images[name].copy();a[24:94, 21:23] = 0
        self.visual_reject({name: a})

    def test_player_number_missing(self):
        name = next(r['file'] for r in self.snapshots if r['scene'] == 'select' and n(r, 'age') == 55)
        a = self.images[name].copy();a[30:56, 43:59] = 0
        self.visual_reject({name: a})

    def test_stance_animation_frozen(self):
        source = next(r['file'] for r in self.snapshots if r['scene'] == 'select' and n(r, 'age') == 55)
        altered = {}
        for r in self.snapshots:
            if r['scene'] == 'select' and 54 <= n(r, 'age') <= 70:
                a = self.images[r['file']].copy();a[110:241, 5:74] = self.images[source][110:241, 5:74]
                altered[r['file']] = a
        self.visual_reject(altered)

    def test_native_backdrop_shifted(self):
        source = next(r['file'] for r in self.snapshots if r['scene'] == 'select' and n(r, 'age') == 55)
        a = self.images[source].copy();a[106:244, 5:75] = a[106:244, 6:76].copy()
        self.visual_reject({source: a})

    def test_dimmed_full_size_avatar_lingers_on_ladder(self):
        target = next(r['file'] for r in self.snapshots if r['scene'] == 'transition' and n(r, 'age') == 2)
        a = self.images[target].copy();a[24:94, 23:78] = v.portrait(self.ui, 0, 55, 70)//2
        self.visual_reject({target: a})

    def test_locked_character_pose_lingers_on_ladder(self):
        target = next(r['file'] for r in self.snapshots if r['scene'] == 'transition' and n(r, 'age') == 2)
        source = max((r for r in self.snapshots if r['scene'] == 'select' and n(r, 'frame') < 1286), key=lambda r:n(r, 'frame'))['file']
        a = self.images[target].copy();a[106:242, 5:75] = self.images[source][106:242, 5:75]
        self.visual_reject({target: a})

    def test_dimmed_character_pose_lingers_on_ladder(self):
        target = next(r['file'] for r in self.snapshots if r['scene'] == 'transition' and n(r, 'age') == 2)
        source = next(r['file'] for r in self.snapshots if r['scene'] == 'select' and n(r, 'age') == 55)
        a = self.images[target].copy();a[106:242, 5:75] = self.images[source][106:242, 5:75]//2
        self.visual_reject({target: a})

    def test_Sonya_ladder_icons_removed(self):
        altered = {};template = v.portrait(self.ui, 1, 35, 45)
        for r in self.snapshots:
            if r['scene'] != 'transition':continue
            a = self.images[r['file']].copy()
            position = v.find_portrait(a, template)
            if position is not None:
                x, y = position;a[y:y+45, x:x+35] = 0;altered[r['file']] = a
        self.assertTrue(altered)
        self.visual_reject(altered)

    def test_name_black_shadow_removed(self):
        target = next(r['file'] for r in self.snapshots if r['scene'] == 'fight' and n(r, 'age') == 60)
        a = self.images[target].copy();face, edge, x = v.shadow(self.ui, 17, 1)
        a[30:40, x:x+face.shape[1]][edge] = [0, 255, 0]
        self.visual_reject({target: a})

    def test_unchosen_avatar_has_persistent_player_number(self):
        target = next(r['file'] for r in self.snapshots if r['scene'] == 'select' and n(r, 'age') == 79)
        a = self.images[target].copy();a[30:56, 43:59] = [0, 123, 0]
        self.visual_reject({target: a})

    def test_failed_observer_not_accepted(self):
        folder = v.ROOT/'audit_v423_native_ui_kano_p1'
        with self.assertRaises(ValueError):v.verify_log((folder/'run.log').read_text(encoding='utf-8-sig'), 'kano', 1)

    def test_compiled_coordinate_and_neighbor_mutations(self):
        dump = next(r for r in v.records(self.logs[0], 'CODE') if r['start'] == 'FFFF0800')
        for address in (0xffff2220, 0xffff1710, 0xffff3220):
            words = dump['words'].split(',');index = (address-0xffff0800)//16
            words[index] = f'{int(words[index],16)^1:04X}'
            log = change(self.logs[0], 'CODE', 1, 'words', ','.join(words), 'start=FFFF0800')
            with self.subTest(address=f'{address:08X}'):
                with self.assertRaises(ValueError):v.verify_log(log, 'kano', 1)


n = v.n


def mutation_test(case, tag, frame, key, value, contains, remove):
    def test(self):
        altered = change(self.logs[case], tag, frame, key, value, contains, remove)
        with self.assertRaises(ValueError):v.verify_log(altered, *CASES[case])
    return test


for case, label, tag, frame, key, value, contains, remove in MUTATIONS:
    setattr(NativeUI, 'test_reject_'+label, mutation_test(case, tag, frame, key, value, contains, remove))


if __name__ == '__main__':
    import hashlib,io,json,sys
    from pathlib import Path
    out=v.ROOT/'audit_v817_current_native_ui_units'
    if out.exists():raise ValueError('Do not overwrite evidence')
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NativeUI))
    out.mkdir();(out/'unit-tests.log').write_text(stream.getvalue())
    paths=[Path(__file__),Path(v.__file__)]+[v.ROOT/f'audit_v813_ui_{fighter}_p{side}'/'run.log'for fighter,side in CASES]
    (out/'verification.json').write_text(json.dumps({'passed':result.wasSuccessful(),'methods':result.testsRun,
        'scope':'Four current UI baseline cases and actual state/pixel corruptions for reported selection/ladder/name failures',
        'fullPortAcceptance':False,'checked_inputs':{str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest().upper()for p in paths}},indent=2)+'\n')
    print(stream.getvalue());sys.exit(0 if result.wasSuccessful()else 1)
