import re
import unittest
from pathlib import Path
from kiss_setup_source import OLD, NEW, integrate

PORT = Path(__file__).resolve().parent
BASE = PORT.parent/'baseline/mk2-rebuild-main/srcp'


class KissSetupTests(unittest.TestCase):
    def test_own_stop_is_real_pose_boundary(self):
        for actor in ('kano', 'sonya'):
            text = (BASE/f'{actor.upper()}ANI.ASM').read_text()
            label = f'ks_{actor}_main_28'
            body = text.split('\n'+label+'\n', 1)[1].split('        .def', 1)[0]
            poses = re.findall(r'\.long (ks_\w+_pose_[a-f0-9]+)', body)
            self.assertEqual(len(poses), 7)
            self.assertIn(f'.long ani_jump,{label}', body)
            # Native pa9 advances one 32-bit pointer per displayed pose.
            self.assertLess(32*5, 32*len(poses))
            self.assertTrue(poses[4].startswith(f'ks_{actor}_pose_'))

    def test_transform_preserves_every_other_byte(self):
        source = 'before\n'+OLD+'\nafter'
        result = integrate(source)
        self.assertEqual(result.replace(NEW, OLD), source)
        self.assertIn('\tpull a1\n\tcalla\tget_his_char_word', result)
        self.assertEqual(result.count('push a1'), 1)
        self.assertEqual(result.count('pull a1'), 2)  # mutually exclusive paths

    def test_duplicate_or_missing_anchor_rejected(self):
        for text in ('', OLD+OLD, NEW):
            with self.assertRaises(AssertionError):
                integrate(text)


if __name__ == '__main__':
    unittest.main()
