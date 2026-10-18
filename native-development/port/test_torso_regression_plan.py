import unittest
from pathlib import Path
from refresh_torso_regression import plan

class TorsoPlanTests(unittest.TestCase):
    def test_both_families_preserve_complete_roles_and_rejoin(self):
        for swipe in (False,True):
            cases=plan('current_torso',swipe)
            self.assertEqual(len({name for name,_ in cases}),4)
            self.assertEqual({(18 if '--sonya' in args else 17,1 if '--mirror' in args else 2) for _,args in cases},
                             {(actor,side) for actor in (17,18) for side in (1,2)})
            flag='--swipe-victim' if swipe else '--torso-victim'
            self.assertTrue(all(flag in args and '--finisher-rejoin' in args and '--freeze-victim' not in args for _,args in cases))

    def test_path_prefix_rejected(self):
        with self.assertRaises(AssertionError):plan('../outside')

    def test_swipe_fresh_counter_has_separate_duck_entry_interval(self):
        source=(Path(__file__).resolve().parent/'diagnostics/extract_probe.lua').read_text()
        branch=source.split('elseif swipe and freshFriendCombat%180>=48',1)[1].split('elseif freshFriendCombat%180>=60',1)[0]
        self.assertIn("hi[player..' Down']:set_value(1)",branch)
        self.assertIn("if freshFriendCombat%180>=60 then hi[player..' High Punch']:set_value(1) end",branch)
