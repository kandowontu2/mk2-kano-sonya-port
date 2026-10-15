import unittest
from pathlib import Path
import numpy as np
from PIL import Image
from verify_native_floor_display_v602 import check_latch,verify_display,verify_coverage

ROOT=Path(__file__).resolve().parents[1]


class NativeDisplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=ROOT/'audit_v621_floor_latch_sonya_p2'
        cls.image=np.asarray(Image.open(cls.folder/'snap/floor_epoch1_1912.png').convert('RGB'))
        cls.raw=(cls.folder/'floor_vram_snap1912_flip1912_4.bin').read_bytes()
        cls.palette=(cls.folder/'floor_palette_1912.bin').read_bytes()

    def test_all_actual_latched_frames(self):self.assertEqual(verify_display(self.folder,ROOT/'audit_v620_floor_sonya_p2')['pixels'],15*101600)
    def test_kano_nine_regular_arenas(self):self.assertEqual(verify_coverage(ROOT/'audit_v620_floor_kano_p2','kano',ROOT/'audit_v610_native_pit_kano_p2')['arenas'],list(range(9)))
    def test_sonya_nine_regular_arenas(self):self.assertEqual(verify_coverage(ROOT/'audit_v620_floor_sonya_p2','sonya',ROOT/'audit_v610_native_pit_sonya_p2')['arenas'],list(range(9)))
    def test_wrong_back_buffer(self):
        with self.assertRaises(ValueError):check_latch(self.image,self.raw,self.palette,0xFFFC,0xF010,0x001C)
    def test_wrong_column(self):
        with self.assertRaises(ValueError):check_latch(self.image,self.raw,self.palette,0xEFFC,0xF010,0x001D)
    def test_wrong_display_polarity(self):
        with self.assertRaises(ValueError):check_latch(self.image,self.raw,self.palette,0xEFFC,0xF410,0x001C)
    def test_previous_flip(self):
        raw=(self.folder/'floor_vram_snap1912_flip1911_3.bin').read_bytes()
        with self.assertRaises(ValueError):check_latch(self.image,raw,self.palette,0xEFFC,0xF010,0x001C)
    def test_one_corrupted_vram_pixel(self):
        words=np.frombuffer(self.raw,dtype='<u2').copy();palette=np.frombuffer(self.palette,dtype='<u4')
        at=256*512+56;original=words[at]&0x7fff
        words[at]=np.flatnonzero(palette!=palette[original])[0]
        self.assertNotEqual(words[at],original)
        with self.assertRaises(ValueError):check_latch(self.image,words.tobytes(),self.palette,0xEFFC,0xF010,0x001C)
    def test_one_corrupted_png_pixel(self):
        image=self.image.copy();image[100,100,0]^=1
        with self.assertRaises(ValueError):check_latch(image,self.raw,self.palette,0xEFFC,0xF010,0x001C)
    def test_wrong_palette(self):
        palette=np.frombuffer(self.palette,dtype='<u4').copy();words=np.frombuffer(self.raw,dtype='<u2')
        pen=words[256*512+56]&0x7fff;palette[pen]^=1
        with self.assertRaises(ValueError):check_latch(self.image,self.raw,palette.tobytes(),0xEFFC,0xF010,0x001C)
    def test_truncated_vram(self):
        with self.assertRaises(ValueError):check_latch(self.image,self.raw[:-2],self.palette,0xEFFC,0xF010,0x001C)


if __name__=='__main__':unittest.main(verbosity=2)
