import unittest
from qualify_normal_soak import summarize


class SoakResultTests(unittest.TestCase):
    def fixture(self):
        rows = [dict(frame=str(n), mode='2', locked='1', missing='0', p1selected='17', p2selected='18',
            p1char='17', p2char='18', p1hp='120', p2hp='130', p1wins='0', p2wins='0', winner='0', p1state='1', p2state='1')
            for n in range(1, 51)]
        for index in (0, 11):
            rows[index].update(p1hp='161', p2hp='161')
        rows[9].update(mode='5', p1hp='0', p2wins='2', winner='2')
        rows[10]['mode'] = '7'
        return rows

    def test_native_result_then_fresh_match(self):
        result = summarize(self.fixture(), (17, 18), 50, 30)
        self.assertEqual(result['freshMatchEntryFrames'], [1, 12])
        self.assertEqual(result['nativeTwoWinResultEntryFrames'], [10])

    def test_wrong_identity_or_missing_field_cannot_pass(self):
        rows = self.fixture(); rows[20]['p1char'] = '1'
        with self.assertRaises(AssertionError):
            summarize(rows, (17, 18), 50, 30)
        with self.assertRaises(AssertionError):
            summarize(self.fixture()[:-1], (17, 18), 50, 30)

    def test_health_drop_without_native_match_result_is_insufficient(self):
        rows = self.fixture(); rows[9]['p2wins'] = '0'
        with self.assertRaises(AssertionError):
            summarize(rows, (17, 18), 50, 30)

    def test_cpu_opponent_cannot_count_as_two_player_stress(self):
        rows = self.fixture(); rows[20]['p1state'] = '0'
        with self.assertRaises(AssertionError):
            summarize(rows, (17, 18), 50, 30)

    def test_a_result_after_leaving_human_match_context_is_not_proof(self):
        rows = self.fixture()
        rows[4].update(mode='4', locked='0')
        for index in range(5, 9):
            rows[index].update(mode='7', locked='0')
        rows[9]['locked'] = '0'
        with self.assertRaises(AssertionError):
            summarize(rows, (17, 18), 50, 30)


if __name__ == '__main__':
    unittest.main()
