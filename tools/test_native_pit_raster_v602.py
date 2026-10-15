import unittest
from pathlib import Path
import numpy as np
from PIL import Image
from inspect_native_pit_pixels_v602 import poses
from verify_native_pit_raster_v602 import check_frame,verify

ROOT=Path(__file__).resolve().parents[1]


class NativeFallingRaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body=poses('kano');cls.path=ROOT/'audit_v610_native_pit_kano_p2/snap/campaign_pit_37440.png'
        cls.image=np.asarray(Image.open(cls.path).convert('RGB'))

    def test_actual_p1_kano(self):self.assertEqual(verify(ROOT/'audit_v603_native_pit_kano_p1','kano',[{'pit_enter':16784}])['checked_frames'],19)
    def test_actual_p1_sonya(self):self.assertEqual(verify(ROOT/'audit_v603_native_pit_sonya_p1','sonya',[{'pit_enter':17027}])['checked_frames'],19)
    def test_actual_p2_kano(self):self.assertEqual(verify(ROOT/'audit_v610_native_pit_kano_p2','kano',[{'pit_enter':37435}])['checked_frames'],19)
    def test_actual_p2_sonya(self):self.assertEqual(verify(ROOT/'audit_v610_native_pit_sonya_p2','sonya',[{'pit_enter':37468}])['checked_frames'],19)
    def test_actual_mirror_kano_both_episodes(self):self.assertEqual(verify(ROOT/'audit_v615_kano_p2_mirror_palette','kano',[{'pit_enter':17636,'episode':1},{'pit_enter':39024,'episode':2}])['checked_frames'],38)
    def test_actual_mirror_sonya(self):self.assertEqual(verify(ROOT/'audit_v615_sonya_p2_mirror_palette','sonya',[{'pit_enter':39788}])['checked_frames'],19)
    def test_wrong_timed_phase(self):
        with self.assertRaises(ValueError):check_frame(self.image,self.body[1])
    def test_shifted_one_pixel(self):
        with self.assertRaises(ValueError):check_frame(np.roll(self.image,1,axis=1),self.body[0])
    def test_one_pixel_wrong_color(self):
        image=self.image.copy();pose=self.body[0];y,x=np.argwhere(pose['indices']!=0)[0]
        image[y+pose['top'],x+pose['left'],0]^=1
        with self.assertRaises(ValueError):check_frame(image,pose)
    def test_wrong_costume_palette(self):
        image=self.image.copy();pose=self.body[0];mask=pose['indices']!=0;h,w=mask.shape
        image[pose['top']:pose['top']+h,pose['left']:pose['left']+w][mask]=pose['alternate'][mask]
        self.assertFalse(np.array_equal(image,self.image))
        with self.assertRaises(ValueError):check_frame(image,pose)
    def test_clipped_raster(self):
        with self.assertRaises(ValueError):check_frame(self.image[:-1],self.body[0])
    def test_missing_body(self):
        image=self.image.copy();pose=self.body[0];h,w=pose['indices'].shape
        image[pose['top']:pose['top']+h,pose['left']:pose['left']+w]=0
        with self.assertRaises(ValueError):check_frame(image,pose)


if __name__=='__main__':unittest.main(verbosity=2)
