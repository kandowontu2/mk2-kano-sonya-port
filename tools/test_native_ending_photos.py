"""Exact original ROM comparison against the compiled production C++ decoder."""
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from decode_native_picture import Bits,codebook,decode
from build_native_ending_reference import reference
from upgrade_ksui_previews import load_gfx

ROOT=Path(__file__).resolve().parents[1]
BOOKS=bytes.fromhex('0f0012032415362738396a7b4c9d6e1f0906011334e5f696f7')

class NativeEndingPhotoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='mk2ks_native_picture_')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.exe=Path(cls.temp.name)/'decoder.exe'
        subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-Wall','-Wextra','-Werror',
                        str(ROOT/'tools/native_picture_reference.cpp'),'-o',str(cls.exe)],check=True)
        cls.gfx=load_gfx(ROOT/'mk3')

    def run_decoder(self,record):
        return subprocess.run([str(self.exe)],input=record,capture_output=True)

    def exact_original(self,offset):
        image,report=decode(self.gfx,offset)
        count=report['palette_count']
        palette=self.gfx[offset+8:offset+8+count*2]
        pixels=image.tobytes()
        bottom=b''.join(pixels[y*image.width:(y+1)*image.width] for y in reversed(range(image.height)))
        actual=self.run_decoder(self.gfx[offset:(report['stream_end_bit']+7)//8])
        self.assertEqual(actual.returncode,0,actual.stderr)
        self.assertEqual(actual.stdout,struct.pack('<3I',image.width,image.height,count)+palette+bottom)

    def test_kano_original_palette_and_all_pixels(self): self.exact_original(0x103599a)
    def test_sonya_original_palette_and_all_pixels(self): self.exact_original(0x1000000)
    def test_liu_biography_original_palette_and_all_pixels(self): self.exact_original(0xfaa73c)
    def test_truncated_original(self):
        result=self.run_decoder(self.gfx[0x1000000:0x1000500])
        self.assertEqual(result.returncode,2);self.assertIn(b'truncated',result.stderr)
    def test_empty_record(self):
        self.assertEqual(self.run_decoder(b'').returncode,2)
    def test_invalid_header(self):
        self.assertIn(b'header',self.run_decoder(struct.pack('<4H',0,128,1,255)).stderr)
    def test_codebook_count_overflow(self):
        record=struct.pack('<5H',1,1,1,1,0)+bytes([4,0xf0,0xf0,0xf0,0xf0,0xf0])
        self.assertIn(b'too many symbols',self.run_decoder(record).stderr)
    def test_codebook_count_underflow(self):
        record=struct.pack('<5H',1,1,1,1,0)+bytes([0,0])
        self.assertIn(b'64 symbols',self.run_decoder(record).stderr)
    def test_literal_palette_bound(self):
        record=struct.pack('<5H',1,1,1,1,0)+BOOKS+bytes([3,0]) # literal palette index 1, count 1
        self.assertIn(b'exceeds palette',self.run_decoder(record).stderr)
    def test_one_black_literal(self):
        record=struct.pack('<5H',1,1,1,1,0)+BOOKS+bytes([1,0])
        result=self.run_decoder(record)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(result.stdout,struct.pack('<3I',1,1,1)+bytes(3))

    def copy_record(self,width,height,distance,run,literal=None):
        bits=Bits(BOOKS,0)
        lengths,distances=codebook(bits),codebook(bits)
        fields=[]
        if literal is not None: fields.extend(((1,1),(literal,8)))
        fields.extend(((0,1),((distance-1)&63,6)))
        def symbol_fields(codes,value):
            key=next(key for key,symbol in codes.items() if symbol==value)
            fields.append((key[1],key[0]))
        symbol_fields(distances,(distance-1)>>6)
        symbol_fields(lengths,min(run-2,63))
        if run>=65:fields.append((run-65,8))
        value=0;position=0
        for word,count in fields:value|=word<<position;position+=count
        stream=value.to_bytes((position+7)//8,'little')
        return struct.pack('<4H2H',width,height,1,2,0,0x7fff)+BOOKS+stream

    def test_overlapping_back_reference(self):
        result=self.run_decoder(self.copy_record(20,1,1,19,literal=1))
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(result.stdout[-20:],bytes([1])*20)
    def test_initial_zero_ring_reference(self):
        result=self.run_decoder(self.copy_record(20,1,1,20))
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(result.stdout[-20:],bytes(20))
    def test_extended_copy_length(self):
        result=self.run_decoder(self.copy_record(321,1,1,320,literal=1))
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(result.stdout[-321:],bytes([1])*321)
    def test_copy_overflow(self):
        result=self.run_decoder(self.copy_record(10,1,1,11))
        self.assertEqual(result.returncode,2)
        self.assertIn(b'exceeds picture dimensions',result.stderr)
    def test_original_kano_zero_is_not_black(self):
        self.assertNotEqual(struct.unpack_from('<H',self.gfx,0x10359a2)[0],0)
    def test_wide_pages_preserve_all_original_palette_and_black_margins(self):
        for fighter in (0,1):
            data,image,report=reference(self.gfx,fighter,1)
            source=report['source_offset']
            self.assertEqual(data[10:520],self.gfx[source+8:source+518])
            words=struct.unpack_from('<256H',data,8)
            pixels=image.tobytes()
            for y in range(119):
                for x in (*range(21),*range(259,280)):
                    self.assertEqual(words[pixels[y*280+x]],0)
            self.assertTrue(all(pixels)) # No literal index-zero escape accidentally emitted.

if __name__=='__main__': unittest.main()
