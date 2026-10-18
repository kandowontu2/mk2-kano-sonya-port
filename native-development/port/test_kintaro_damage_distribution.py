import unittest
from inspect_kintaro_damage_distribution import summarize


def row(frame, hp=161, boss=161, attempt=1, round=1, mode=2):
    return {k: str(v) for k, v in dict(frame=frame, p1hp=hp, p2hp=boss,
        attempt=attempt, round=round, mode=mode, p1char=17, p2char=12,
        p1action=0, p2action=0).items()}


class DamageDistributionTests(unittest.TestCase):
    def test_damage_not_health_reset_or_round_transition(self):
        report = summarize(iter([row(2), row(4, 121, 148), row(6),
            row(8, 80, 80, round=2), row(10, 40, 78, round=2)]))
        self.assertEqual([(r['playerDamage'], r['bossDamage']) for r in report['rounds']],
                         [(40, 13), (40, 2)])

    def test_ineligible_gap_breaks_adjacency(self):
        report = summarize(iter([row(2), row(4, mode=5), row(6, 0, 0)]))
        self.assertEqual(report['sampledDamageGroups'], [])
        self.assertEqual(report['rounds'][0]['minimumBossHP'], 0)

    def test_attempt_is_part_of_round_identity(self):
        report = summarize(iter([row(2), row(4, 1, 1, attempt=2)]))
        self.assertEqual(len(report['rounds']), 2)
        self.assertEqual(report['sampledDamageGroups'], [])


if __name__ == '__main__':
    unittest.main()
