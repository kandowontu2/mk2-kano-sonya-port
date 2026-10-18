import unittest
from inspect_kintaro_variety import validate_decision


class VarietyAuditTests(unittest.TestCase):
    def row(self):
        return dict(history='0200:0200:0000:0000:0000:0000',kicks='2',punches='0',
                    decision='mixpunch',ownAction='771',ownFlags='1',ownHeight='0',ownHP='161')

    def test_request_must_match_native_queue_not_preferred_attack(self):
        self.assertTrue(validate_decision(self.row()))
        with self.assertRaises(AssertionError):validate_decision(dict(self.row(),decision='mixkick'))
        with self.assertRaises(AssertionError):validate_decision(dict(self.row(),kicks='1'))

    def test_unready_request_cannot_pass(self):
        with self.assertRaises(AssertionError):validate_decision(dict(self.row(),ownFlags='4'))
        self.assertFalse(validate_decision(dict(self.row(),decision='wait')))


if __name__=='__main__':unittest.main()
