import unittest
from inspect_boss_buyin_delay import transitions


class BuyinDelayTests(unittest.TestCase):
    def test_partial_purchase_not_counted_and_matching_map_required(self):
        rows=[dict(frame='10',attempt='1',map='15',phase='buyin'),
              dict(frame='211',attempt='1',map='15',phase='selection'),
              dict(frame='300',attempt='2',map='15',phase='buyin')]
        self.assertEqual(transitions(rows)[0]['selectionLatency'],201)
        self.assertEqual(len(transitions(rows)),1)
        rows[1]['map']='16'
        with self.assertRaises(AssertionError):transitions(rows)


if __name__=='__main__':unittest.main()
