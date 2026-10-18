import unittest
from build_move_showcases import plan
from collect_native_videos import plan as catalog_plan

class ShowcasePlanTests(unittest.TestCase):
    def test_two_showcases_cover_all_fifty_eight_current_clips_once(self):
        keys=[key for actor in (17,18) for key,_ in plan(actor)]
        self.assertEqual(len(keys),58)
        self.assertEqual(len(set(keys)),58)
        self.assertEqual(set(keys),{key for key,_ in catalog_plan(True)})
        self.assertTrue(all('pit_video_filtered' in name for key,name in catalog_plan(True) if key.startswith('pit/')))
        with self.assertRaises(AssertionError):plan(1)
