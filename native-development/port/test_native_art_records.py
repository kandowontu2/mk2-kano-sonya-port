"""Synthetic bounds/record tests; no copyrighted ROM input required."""
import struct
import unittest
import native_art_records as art

class NativeArtRecordsTests(unittest.TestCase):
    def fixture(self,control=0x6000):
        data=bytearray(256)
        struct.pack_into('<HHhhIH',data,128,8,10,-2,3,0x12340,control)
        frame=art.TMS_ROM_BASE+128*8
        group=art.TMS_ROM_BASE+32*8
        struct.pack_into('<I',data,0,group)
        struct.pack_into('<II',data,32,frame,0)
        return data,frame,group

    def test_address_alignment(self):
        self.assertEqual(art.stock_file(art.TMS_ROM_BASE+16),2)
        for address in (0,art.TMS_ROM_BASE-16,art.TMS_ROM_BASE+8,0x100000000):
            with self.assertRaises(ValueError):art.stock_file(address)

    def test_signed_coordinates(self):
        self.assertEqual([art.signed(x) for x in (0,32767,32768,65535)],[0,32767,-32768,-1])

    def test_full_and_skip_records(self):
        for control in (0x6000,0x6080):
            data,_,_=self.fixture(control)
            self.assertTrue(art.looks_like_frame(data,128))

    def test_invalid_records(self):
        for control in (0x6001,0x2000,0x8000):
            data,_,_=self.fixture(control)
            self.assertFalse(art.looks_like_frame(data,128))
        self.assertFalse(art.looks_like_frame(bytes(13),0))
        self.assertFalse(art.looks_like_frame(bytes(20),-1))

    def test_composite_reference(self):
        data,frame,group=self.fixture()
        base=art.TMS_ROM_BASE
        self.assertEqual(art.frame_group(data,group,base,base+96*8),[frame])
        self.assertEqual(art.group_references(data,base,base+96*8),[(0,group,[frame])])

    def test_unterminated_and_out_of_bounds_group(self):
        data,frame,group=self.fixture()
        for i in range(16):struct.pack_into('<I',data,32+i*4,frame)
        self.assertIsNone(art.frame_group(data,group,art.TMS_ROM_BASE,art.TMS_ROM_BASE+96*8))
        self.assertIsNone(art.frame_group(bytes(35),group,art.TMS_ROM_BASE,art.TMS_ROM_BASE+96*8))

if __name__=='__main__':unittest.main()
