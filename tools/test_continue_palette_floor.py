"""In-memory adversarial tests of the bounded pixel/record preservation contract."""
import unittest
import numpy as np
import verify_continue_palette_floor as v

class PixelContract(unittest.TestCase):
    def setUp(self):
        self.before = np.full((12,12,3), 90, dtype=np.uint8)
        self.body = np.zeros_like(self.before); self.body[3:8,5:7] = (120,180,50)
        self.opaque = np.any(self.body != 0, axis=2)
        self.shadow = np.zeros((12,12), dtype=bool); self.shadow[2:12,:] = True
        self.before[self.opaque] = self.body[self.opaque]; self.before[7,5] = 0
        self.after = self.before.copy()
        self.after[self.shadow & ~self.opaque] = 0; self.after[7,5] = self.body[7,5]
    def check(self, image):
        return v.check_pixels(self.before, image, self.body, self.opaque, self.shadow)
    def test_valid_shadow_and_restored_foot(self):
        self.assertEqual(self.check(self.after)['restoredBodyPixels'], 1)
    def test_original_bug_rejected(self):
        with self.assertRaises(ValueError): self.check(self.before)
    def test_missing_shadow(self):
        image=self.after.copy(); image[10,2]=90
        with self.assertRaises(ValueError): self.check(image)
    def test_colored_shadow(self):
        image=self.after.copy(); image[10,2]=(0,0,1)
        with self.assertRaises(ValueError): self.check(image)
    def test_erased_body(self):
        image=self.after.copy(); image[3,5]=0
        with self.assertRaises(ValueError): self.check(image)
    def test_recolored_body(self):
        image=self.after.copy(); image[3,5]=200
        with self.assertRaises(ValueError): self.check(image)
    def test_fake_restoration(self):
        image=self.after.copy(); image[7,5]=(119,180,50)
        with self.assertRaises(ValueError): self.check(image)
    def test_outside_ui_overlay(self):
        image=self.after.copy(); image[0,0]=0
        with self.assertRaises(ValueError): self.check(image)

class RecordContract(unittest.TestCase):
    def test_complete_hash_pins(self):
        for pin in (v.EXE, v.OLD_EXE, v.PAYLOAD):
            self.assertEqual(len(pin),64)
            self.assertTrue(all(c in '0123456789ABCDEF' for c in pin))
    def test_identical_native_records(self):
        row='MK2_GROUND_FIELD frame=1 id=17 health=161\n'
        v.preserve_records(row,row,('FIELD',))
    def test_proxy_identity(self):
        with self.assertRaises(ValueError):
            v.preserve_records('MK2_GROUND_FIELD frame=1 id=17\n',
                               'MK2_GROUND_FIELD frame=1 id=0\n',('FIELD',))
    def test_health_override(self):
        with self.assertRaises(ValueError):
            v.preserve_records('MK2_GROUND_HEALTH frame=1 health=161\n',
                               'MK2_GROUND_HEALTH frame=1 health=999\n',('HEALTH',))
    def test_changed_actual_input(self):
        with self.assertRaises(ValueError):
            v.preserve_records('MK2_GROUND_INPUT frame=1 button=Coin\n',
                               'MK2_GROUND_INPUT frame=1 button=Start\n',('INPUT',))

if __name__=='__main__': unittest.main()
