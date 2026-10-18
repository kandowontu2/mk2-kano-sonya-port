"""Synthetic archive fixtures only; no emulator or game-state manipulation."""
from pathlib import Path
import os
import tempfile
import unittest
import zipfile
from test_rom_cache import prepare_archive

class CacheTests(unittest.TestCase):
    def test_reuse_and_payload_isolation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);base=root/'base.zip'
            with zipfile.ZipFile(base,'x') as archive:
                archive.writestr('program',b'original');archive.writestr('art',b'preserved')
            first=prepare_archive(base,{'program':b'changed'},root/'cache',root/'one/mk3.zip')
            second=prepare_archive(base,{'program':b'changed'},root/'cache',root/'two/mk3.zip')
            self.assertFalse(first['cacheReused']);self.assertTrue(second['cacheReused'])
            self.assertEqual(first['archiveSHA256'],second['archiveSHA256'])
            if first['hardLinked'] and second['hardLinked']:
                self.assertTrue(os.path.samefile(root/'one/mk3.zip',root/'two/mk3.zip'))
            with zipfile.ZipFile(root/'two/mk3.zip') as archive:
                self.assertEqual(archive.read('program'),b'changed')
                self.assertEqual(archive.read('art'),b'preserved')
            third=prepare_archive(base,{'program':b'next'},root/'cache',root/'three/mk3.zip')
            self.assertNotEqual(first['key'],third['key'])
            with zipfile.ZipFile(base) as archive:self.assertEqual(archive.read('program'),b'original')

    def test_corruption_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);base=root/'base.zip'
            with zipfile.ZipFile(base,'x') as archive:archive.writestr('program',b'original')
            first=prepare_archive(base,{},root/'cache',root/'one.zip')
            with (root/'cache'/first['key']/'mk3.zip').open('ab') as stream:stream.write(b'corruption')
            with self.assertRaises(ValueError):prepare_archive(base,{},root/'cache',root/'two.zip')
            self.assertFalse((root/'two.zip').exists())

if __name__=='__main__':unittest.main()
