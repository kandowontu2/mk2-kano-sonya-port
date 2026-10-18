import unittest
import numpy as np
from shadow_pixel_regression import verify

class ShadowPixelTests(unittest.TestCase):
    def test_current_fix_must_match_not_merely_have_dark_pixels(self):
        before=np.full((254,400,3),120,dtype=np.uint8)
        corrected=before.copy();corrected[210:215,260:280]=0
        self.assertEqual(int(verify(before,corrected,corrected.copy()).sum()),100)
        current=corrected.copy();current[212,270]=1
        with self.assertRaises(AssertionError):verify(before,corrected,current)

    def test_unbounded_or_empty_historical_delta_rejected(self):
        before=np.full((254,400,3),120,dtype=np.uint8)
        with self.assertRaises(AssertionError):verify(before,before,before)
        corrected=before.copy();corrected[30,270]=0
        with self.assertRaises(AssertionError):verify(before,corrected,corrected)
