import unittest
from campaign_continuity import require_no_state_load


class CampaignContinuityTests(unittest.TestCase):
    def test_save_only_is_not_a_load(self):
        require_no_state_load('m:save(path)', ['--campaign-boss-checkpoint'])

    def test_loaded_state_cannot_pass_as_continuous(self):
        for source in ('m:load(path)','m : load (path)','m.load(m,path)'):
            with self.assertRaises(AssertionError):require_no_state_load(source,[])
        for flag in ('--planning-state=x','--campaign-state-load=x','-state','-autosave'):
            with self.assertRaises(AssertionError):require_no_state_load('',[flag])


if __name__=='__main__':unittest.main()
