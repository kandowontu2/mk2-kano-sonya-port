import unittest
from stage_sides import performer_first,signed_word,tomb_command


class StageSides(unittest.TestCase):
    def test_swap_and_roundtrip_without_mutation(self):
        rows=[dict(p1char='17',p2char='18',p1hp='161',p2hp='0',winner='3')]
        swapped=performer_first(rows,True)
        self.assertEqual(swapped[0],dict(p1char='18',p2char='17',p1hp='0',p2hp='161',winner='3'))
        self.assertEqual(rows[0]['p1char'],'17')
        self.assertEqual(performer_first(swapped,True),rows)
        self.assertIs(performer_first(rows,False),rows)

    def test_both_commands_both_facings(self):
        self.assertEqual(tomb_command(17,100,160),[7,5,5])
        self.assertEqual(tomb_command(17,160,100),[8,5,5])
        self.assertEqual(tomb_command(18,100,160),[6,8,8])
        self.assertEqual(tomb_command(18,160,100),[6,7,7])

    def test_negative_coordinates(self):
        self.assertEqual(signed_word(65530),-6)
        self.assertEqual(tomb_command(17,65530,10),[7,5,5])
        self.assertEqual(tomb_command(18,10,65530),[6,7,7])


if __name__=='__main__':unittest.main()
