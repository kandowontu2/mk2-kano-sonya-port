import unittest
from run_kano_finish_stomp_refresh import combined_arguments
from run_kano_finishing_uppercut13 import trial_arguments


class CombinedInputTests(unittest.TestCase):
    def test_only_refresh_is_added_without_extra_budget(self):
        prior = ['--game', '--campaign', '--campaign-continues=32']
        args = combined_arguments(prior)
        self.assertEqual(args[:-1], trial_arguments(prior))
        self.assertEqual(args[-1], '--campaign-kano-kintaro-stomp-refresh')
        self.assertNotIn('--campaign-boss-endurance', args)
        self.assertNotIn('--campaign-kano-kintaro-stomp-momentum', args)
        self.assertIn('--campaign-continues=32', args)


if __name__ == '__main__':
    unittest.main()
