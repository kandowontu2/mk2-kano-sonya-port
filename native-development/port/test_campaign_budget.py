import unittest
from campaign_budget import budget

class CampaignBudgetTests(unittest.TestCase):
    def test_defaults_unchanged(self):
        self.assertEqual(budget([]),dict(continueLimit=0,fieldLimit=30000,endurance=False))
        self.assertEqual(budget(['--campaign-full','--campaign-extra-continues','--campaign-continues=32'])['fieldLimit'],90000)

    def test_endurance_requires_all_explicit_prerequisites(self):
        args=['--game','--campaign','--campaign-full','--campaign-extra-continues','--campaign-ending-window','--campaign-finale-window','--campaign-background-margin','--campaign-boss-endurance','--campaign-continues=64']
        self.assertEqual(budget(args),dict(continueLimit=64,fieldLimit=300000,endurance=True))
        for required in args[:7]:
            with self.assertRaises(AssertionError):budget([arg for arg in args if arg!=required])

    def test_unflagged_excess_negative_and_duplicate_limits_rejected(self):
        for args in (['--campaign-full','--campaign-extra-continues','--campaign-continues=64'],
                     ['--campaign-continues=-1'],['--campaign-continues=0','--campaign-continues=1']):
            with self.assertRaises(AssertionError):budget(args)
