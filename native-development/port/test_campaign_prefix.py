import unittest
from compare_campaign_prefix import compare


class PrefixTests(unittest.TestCase):
    def setUp(self):
        self.rows=['mode,p2char,hp\n','2,3,161\n','5,3,0\n','2,1,161\n']

    def test_target_outcome_not_part_of_prefix(self):
        self.assertEqual(compare(self.rows,self.rows[:-1]+['2,1,99\n'],1)['identicalPreMatchupRows'],2)

    def test_earlier_difference_fails(self):
        with self.assertRaises(AssertionError):compare(self.rows,[self.rows[0],'2,3,160\n']+self.rows[2:],1)

    def test_missing_target_fails(self):
        with self.assertRaises(AssertionError):compare(self.rows,self.rows[:-1],1)

    def test_header_difference_fails(self):
        with self.assertRaises(AssertionError):compare(self.rows,['mode,p2char,health\n']+self.rows[1:],1)


if __name__=='__main__':unittest.main()
