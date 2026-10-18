import unittest
from native_lk_poses import LABELS,resolve

def listing():
    return '1 00000000 lk_anitab1\n'+''.join(f'{index+2} {32*(index+1):08x} {name}\n' for index,name in enumerate(LABELS))

class NativeLKPoseTests(unittest.TestCase):
    def test_local_offsets_use_linked_anchor(self):
        values=resolve({'lk_anitab1':0xff900000},listing())
        self.assertEqual(values['a_torso_ripped'],0xff900020)
        self.assertEqual(len(values),len(LABELS))

    def test_missing_duplicate_or_outside_address_rejected(self):
        for text in (listing().replace('LKDEADLEG1','other'),listing()+'99 00000100 LKDEADLEG1\n'):
            with self.assertRaises(AssertionError):resolve({'lk_anitab1':0xff900000},text)
        with self.assertRaises(AssertionError):resolve({'lk_anitab1':0xff700000},listing())
