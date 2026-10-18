import unittest
from collect_native_videos import plan

class NativeVideoCatalogTests(unittest.TestCase):
    def test_complete_finite_set_excludes_rejected_pit_captures(self):
        cases=plan()
        self.assertEqual(len(cases),24)
        self.assertEqual(sum(key.startswith('special/') for key,_ in cases),8)
        self.assertEqual(sum(key.startswith('lethal/') for key,_ in cases),4)
        for key,name in cases:
            if key.startswith('pit/'):
                self.assertIn('pit_video_filtered',name)
                self.assertNotIn('stage_video_pit',name)
