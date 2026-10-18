import unittest
from campaign_budget import budget
from run_kano_finishing_uppercut13 import trial_arguments


class FinishingEnduranceTests(unittest.TestCase):
    def prior(self):
        return ['--game','--campaign','--campaign-full','--campaign-extra-continues',
                '--campaign-ending-window','--campaign-finale-window','--campaign-background-margin',
                '--campaign-continues=32']

    def test_endurance_only_extends_declared_continue_and_field_budgets(self):
        ordinary=trial_arguments(self.prior())
        extended=trial_arguments(self.prior(),True)
        self.assertEqual(budget(ordinary)['continueLimit'],32)
        self.assertEqual(budget(extended),dict(continueLimit=64,fieldLimit=300000,endurance=True))
        self.assertEqual([a for a in ordinary if not a.startswith('--campaign-continues=')],
                         [a for a in extended if not a.startswith('--campaign-continues=') and a!='--campaign-boss-endurance'])


if __name__=='__main__':unittest.main()
