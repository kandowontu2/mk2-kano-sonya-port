"""Finite source-photo and append-only ending art contracts; no runtime claim."""
import hashlib
import json
from pathlib import Path
import unittest

PORT=Path(__file__).resolve().parent
sha=lambda data:hashlib.sha256(data).hexdigest().upper()

class EndingArt(unittest.TestCase):
    def test_preserves_all_existing_graphics(self):
        report=json.loads((PORT/'generated_ending/ENDING_ART.json').read_text())
        prefix=(PORT/'generated_morph/fighter_ui_finish_morph_graphics.bin').read_bytes()
        packed=(PORT/'generated_ending/fighter_ui_finish_ending_graphics.bin').read_bytes()
        self.assertEqual(packed[:len(prefix)],prefix)
        self.assertEqual(report['prefixSHA256'],sha(prefix))
        self.assertEqual(report['packedSHA256'],sha(packed))
        self.assertEqual(len(packed)-len(prefix),107064)
        self.assertLess(len(packed),0x600000)

    def test_own_photos_and_typed_records(self):
        report=json.loads((PORT/'generated_ending/ENDING_ART.json').read_text())
        source=(PORT/'generated_ending/KSENDART.ASM').read_bytes()
        self.assertEqual(sha(source),report['sourceSHA256'])
        expected=[
            '1D61987975AE3F8FA1D2E93060DC5FBBFFD3F8C9FD837976D9C79C878D9E72BC',
            '2942FFFAC03FBE124BD459A8F18C2432885969431D930607719D15424ECB95F8',
            'DF60746CC30E5D23EAC8B16481891441BB963B6A6E3362F3D55FF94F07BF5051',
            '4719686805D33ABDB780EA87F92783D895FC2C7F8CF7001D8FE9B4688DA8207E']
        self.assertEqual([image['independentReferenceSHA256'] for image in report['images']],expected)
        packed=(PORT/'generated_ending/fighter_ui_finish_ending_graphics.bin').read_bytes()
        for image in report['images']:
            pixels=packed[image['packedOffset']:image['packedOffset']+image['bytes']]
            self.assertEqual(sha(pixels),image['pixelsSHA256'])
            self.assertEqual(len(pixels),image['width']*image['height'])
            self.assertGreater(min(pixels),0)
            self.assertIn((image['label']+'\n        .word ').encode(),source)
        self.assertEqual(source.count(b'.word 256'),4)
        self.assertNotIn(b'.text',source)
        self.assertFalse(report['linkedIntoGame'])
        self.assertFalse(report['runtimeVerified'])

if __name__=='__main__': unittest.main()
