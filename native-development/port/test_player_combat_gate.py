import unittest
from qualify_player_headless_boot import combat_acceptance


def row(**changes):
    r=dict(mode='2',p1state='1',p2state='1',p1char='17',p2char='18',locked='1',
           p1hp='150',p2hp='140',missing='0')
    r.update(changes);return r


class PlayerCombatGateTests(unittest.TestCase):
    def test_exact_minimum_and_both_sides(self):
        self.assertTrue(combat_acceptance([row() for _ in range(600)])['passed'])
        self.assertFalse(combat_acceptance([row() for _ in range(599)])['passed'])
        self.assertTrue(combat_acceptance([row(p1char='18',p2char='17') for _ in range(600)],True)['passed'])

    def test_cpu_proxy_unlocked_missing_and_no_damage_do_not_pass(self):
        for invalid in (dict(p1state='2'),dict(p2state='2'),dict(p1char='1'),dict(locked='0'),
                        dict(missing='1'),dict(p1hp='161'),dict(p2hp='161')):
            self.assertFalse(combat_acceptance([row(**invalid) for _ in range(600)])['passed'],invalid)


if __name__=='__main__':unittest.main()
