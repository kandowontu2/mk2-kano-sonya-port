"""Pre-link checks: original dispatch retained, own halves distinct, assets pinned."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile

from lao_split_source import integrate, LOOKUP_NATIVE, LOOKUP_NEW, SECOND_NEW
from build_inflation_assets import unpack6
from build_arm_rip_assets import read_pgm

PORT = Path(__file__).resolve().parent


class LaoSplitSourceTests(unittest.TestCase):
    def test_canonical_source_integration(self):
        with zipfile.ZipFile(Path('C:/Users/kando/Downloads/mk2-rebuild-main.zip')) as archive:
            names = [n for n in archive.namelist() if n.lower().endswith('/src/mkdeath.asm')]
            self.assertEqual(len(names), 1)
            original = archive.read(names[0]).decode('cp437').replace('\r\n', '\n')
        result = integrate(original)
        self.assertEqual(result.count(LOOKUP_NEW), 1)
        self.assertEqual(result.count(SECOND_NEW), 1)
        self.assertIn(LOOKUP_NATIVE, LOOKUP_NEW)
        # No original table, animation cadence, stance construction or physics edit.
        self.assertEqual(result.replace(LOOKUP_NEW, LOOKUP_NATIVE).replace(
            SECOND_NEW, __import__('lao_split_source').SECOND_OLD).replace(
            '\n\t.ref ks_kano_split,ks_sonya_split,ks_kano_split_other,ks_sonya_split_other\nr_split_in_2\n',
            '\nr_split_in_2\n'), original)

    def test_packed_images_and_prefix(self):
        folder = PORT/'generated_split'
        report = json.loads((folder/'SPLIT_DATA.json').read_text())
        packed = (folder/'fighter_ui_finish_split_graphics.bin').read_bytes()
        sha = lambda data: hashlib.sha256(data).hexdigest().upper()
        self.assertEqual(sha(packed), report['packedSHA256'])
        self.assertEqual(sha((folder/'KSPLART.ASM').read_bytes()), report['assemblySHA256'])
        prefix = (PORT/'generated_ingestion/fighter_ui_finish_ingest_graphics.bin').read_bytes()
        self.assertTrue(packed.startswith(prefix))
        self.assertEqual(sha(prefix), report['prefixSHA256'])
        self.assertEqual(len(report['frames']), 34)
        for frame in report['frames']:
            w, h, pixels = read_pgm(PORT/'assets/split_v2'/frame['file'])
            offset = frame['packedByteOffset']
            self.assertEqual(unpack6(packed[offset:offset+frame['packedBytes']], w*h), pixels)
        for name, digest in report['sockets'].items():
            self.assertEqual(sha((folder/name).read_bytes()), digest)


if __name__ == '__main__':
    unittest.main()
