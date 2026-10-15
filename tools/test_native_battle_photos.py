"""Original-photo crop and native BATTLE storage invariants."""
from pathlib import Path
import struct
import unittest
from build_native_ending_reference import reference
from decode_native_picture import decode
from upgrade_ksui_previews import load_gfx

class NativeBattlePhotoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.gfx=load_gfx(Path(__file__).resolve().parents[1]/'mk3')
    def test_both_native_headers_palettes_and_no_escape_pixels(self):
        for fighter in (0,1):
            data,image,report=reference(self.gfx,fighter,2)
            self.assertEqual(struct.unpack_from('<4H',data),(138,158,1,256))
            at=report['source_offset']
            self.assertEqual(data[8:520],bytes(2)+self.gfx[at+8:at+518])
            self.assertTrue(all(image.tobytes()))
            self.assertGreater(len(set(image.tobytes())),64) # Not a resized 64-color roster icon.
    def test_crop_corners_and_face_center_are_original_pixels(self):
        for fighter in (0,1):
            _,image,report=reference(self.gfx,fighter,2)
            source,_=decode(self.gfx,report['source_offset'])
            for x,y in ((0,0),(137,0),(0,157),(137,157),(69,60),(69,79)):
                sx=(0 if fighter else 143)+x*108//138
                sy=4+y*124//158
                self.assertEqual(image.getpixel((x,y)),source.getpixel((sx,sy))+1)
    def test_crop_preserves_native_aspect(self):
        self.assertLess(abs((108/124)/(138/158)-1),0.005)
    def test_both_literal_records_fit_reserved_window(self):
        length=8+256*2+25+(138*158*9+7)//8
        self.assertLessEqual(length+(length+1)//2*2,0x10000)
    def test_invalid_fighter_or_picture_kind(self):
        for fighter,page in ((2,2),(0,3),(-1,0)):
            with self.assertRaises(ValueError):reference(self.gfx,fighter,page)

if __name__=='__main__':unittest.main()
