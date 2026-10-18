import unittest
from qualify_kintaro_short_search import score


def row(**changes):
    result=dict(p1wins='0',p2wins='0',p1hp='161',p2hp='161',distance='192',map='15')
    result.update(changes);return result


class ShortSearchScoreTests(unittest.TestCase):
    def test_native_round_counters_outrank_hp_and_distance_is_bounded(self):
        self.assertGreater(score(row(p1wins='1',p1hp='1')),score(row(p2hp='0')))
        self.assertLess(score(row(p2wins='1')),score(row(p1hp='1')))
        self.assertEqual(score(row(distance='1000')),score(row(distance='260')))


if __name__=='__main__':unittest.main()
