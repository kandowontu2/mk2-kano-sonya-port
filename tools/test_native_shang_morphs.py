"""Original transition art, palette, native grammar and transactional scope."""
import hashlib
import json
import struct
import unittest
from pathlib import Path

import build_native_shang_morphs as morph
import build_mk2ks_mk3 as animation
import build_native_projectile_impacts as pixels
import upgrade_ksui_previews as decoder

ROOT=Path(__file__).resolve().parents[1]


class MorphAssets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/'diagnostic_v300_native_projectile_choreography/roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.payload=(ROOT/'diagnostic_v323_native_shang_morph_payload/roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.report=json.loads((ROOT/'diagnostic_v323_native_shang_morph_payload/roms/mk2ks/mk2ks.morph.json').read_text())
        cls.program=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
        cls.gfx=decoder.load_gfx(ROOT/'mk3')

    def test_exact_source_and_generated_asset_identity(self):
        self.assertEqual(hashlib.sha256(self.source).hexdigest(),morph.SOURCE_SHA)
        self.assertEqual(hashlib.sha256(self.payload).hexdigest(),self.report['payload_sha256'])

    def test_existing_full_payload_unchanged_outside_reserved_import(self):
        self.assertEqual(self.payload[:morph.HEADER],self.source[:morph.HEADER])
        self.assertEqual(self.payload[morph.END:],self.source[morph.END:])

    def test_native_header_exact_inventory(self):
        self.assertEqual(struct.unpack_from('<4s6I',self.payload,morph.HEADER),
            (b'KSM1',morph.PIXELS,34212,morph.GFX_DEST,morph.address(morph.SEQUENCES[0]),morph.address(morph.SEQUENCES[1]),12))

    def test_original_six_complete_composites_not_stance_substitutes(self):
        for fighter,data in self.report['fighters'].items():
            self.assertEqual(tuple(int(g['source'],16) for g in data['groups']),morph.SOURCE_GROUPS[fighter])
            self.assertEqual(len(data['components']),6)
            for group in data['groups']:
                at=(int(group['native'],16)-morph.BASE)//8
                self.assertEqual(struct.unpack_from('<3I',self.payload,at),(*group['components'],0))

    def test_every_original_component_pixel_and_pivot_preserved(self):
        for data in self.report['fighters'].values():
            for component in data['components']:
                spec=decoder.component_spec(self.program,int(component['source'],16))
                original=pixels.decode_indices(self.gfx,spec)
                at=(int(component['native'],16)-morph.BASE)//8
                w,h,xo,yo,source,cmd,pal=struct.unpack_from('<4hIHI',self.payload,at)
                self.assertEqual((w,h,xo,yo),spec[2:])
                self.assertEqual((cmd,pal),(0x6000,int(data['palette'],16)))
                bit=source-morph.GFX_DEST*8+morph.PIXELS*8
                actual=bytes(decoder.extract_bits(self.payload,bit+i*6,63) for i in range(w*h))
                self.assertEqual(actual,original)
                self.assertEqual(hashlib.sha256(actual).hexdigest(),component['pixel_sha256'])

    def test_every_original_opaque_palette_index_preserved(self):
        for data in self.report['fighters'].values():
            at=(int(data['palette_source'],16)-animation.TMS_ROM_BASE)//8
            count=animation.u16(self.program,at)
            native=(int(data['palette'],16)-morph.BASE)//8
            self.assertEqual(animation.u16(self.payload,native),64)
            original=struct.unpack_from(f'<{count}H',self.program,at+2)
            actual=struct.unpack_from('<64H',self.payload,native+2)
            self.assertEqual(actual[1:count],original[1:])
            self.assertEqual(actual[0],0)

    def test_stock_native_tokens_callback_and_own_target_stance(self):
        for index,fighter in enumerate(('kano','sonya')):
            data=self.report['fighters'][fighter]
            seq=struct.unpack_from('<9I',self.payload,morph.SEQUENCES[index])
            self.assertEqual(seq,(0xff959cb0,6,0xff9645e0,*(int(g['native'],16) for g in data['groups']),5,int(data['target_stance'],16),0))
            self.assertEqual(data['target_id'],17+index)

    def test_wrong_source_rejected_without_mutation(self):
        data=bytearray(self.source);data[0]^=1;before=bytes(data)
        with self.assertRaises(ValueError):morph.build(data,self.program,ROOT/'mk3')
        self.assertEqual(data,before)

    def test_wrong_original_palette_rejected_without_mutation(self):
        data=bytearray(self.source);program=bytearray(self.program)
        struct.pack_into('<H',program,animation.stock_file(0xffca1600),65)
        with self.assertRaises(ValueError):morph.build(data,program,ROOT/'mk3')
        self.assertEqual(data,self.source)

    def test_asset_preparation_cannot_claim_runtime_or_whole_goal(self):
        self.assertEqual(self.report['scope'],'original_morph_assets_only_native_runtime_not_yet_verified')


if __name__=='__main__':unittest.main()
