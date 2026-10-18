import unittest
from inspect_chicken_isolated import held_out_bounds


class HeldOutBoundsTests(unittest.TestCase):
    def test_entire_alignment_search_excluded(self):
        self.assertEqual(held_out_bounds(20000,1200,8895),(7695,20000))

    def test_command_before_validation_gives_no_samples(self):
        self.assertEqual(held_out_bounds(20000,1200,8895,5000),(7695,7695))

    def test_later_command_cuts_tail(self):
        self.assertEqual(held_out_bounds(20000,1200,8895,12000),(7695,10800))

    def test_no_validation_when_reference_shorter_than_search(self):
        self.assertEqual(held_out_bounds(6000,1200,8895),(6000,6000))
