import unittest
from inspect_kintaro_ball_charge import release_windows


class ChargeAuditTests(unittest.TestCase):
    def fixture(self):
        held = [dict(frame=str(n), lk='1', phase='charge') for n in range(1, 89)]
        release = dict(frame='89', lk='0', phase='release', age='88', height='0',
                       action='771', flags='1', ownHP='161')
        return held + [release]

    def test_contiguous_physical_charge(self):
        result = release_windows(self.fixture())
        self.assertEqual(result[0]['consecutiveHeldFields'], 88)
        self.assertTrue(result[0]['heldLongerThanNative80FieldGate'])

    def test_skipped_callback_or_released_button_breaks_charge(self):
        for gap in (True, False):
            rows = self.fixture()
            if gap:
                del rows[30]
            else:
                rows[30] = dict(rows[30], lk='0')
            self.assertFalse(release_windows(rows)[0]['heldLongerThanNative80FieldGate'])

    def test_no_release_is_not_an_activation(self):
        self.assertEqual(release_windows(self.fixture()[:-1]), [])

    def test_early_or_unready_release_rejected(self):
        for key, value in (('age', '70'), ('height', '1'), ('action', '0'), ('flags', '4')):
            rows = self.fixture()
            rows[-1] = dict(rows[-1], **{key: value})
            with self.subTest(key=key), self.assertRaises(AssertionError):
                release_windows(rows)


if __name__ == '__main__':
    unittest.main()
