"""Independent checks of the actual minimal local player artifact."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
from build_native_player_playtest import digest_stream, isolated_launcher
from inspect_normal_runtime import PORT


class PlayerBundleTests(unittest.TestCase):
    def test_launcher_blocks_external_ini_without_changing_paths(self):
        original=b'"%MK2KS_MAME%" mk3 -rompath "%~dp0roms" -cfg_directory "%~dp0config\\cfg"\r\n'
        changed=isolated_launcher(original)
        self.assertEqual(changed.replace(b' -noreadconfig',b''),original)
        with self.assertRaises(AssertionError):isolated_launcher(changed)
        with self.assertRaises(AssertionError):isolated_launcher(b'unknown')

    def test_stream_hash_uses_bounded_reads(self):
        class BoundedStream:
            remaining = 200000
            def read(self, size):
                self.assert_size(size)
                count = min(size, self.remaining)
                self.remaining -= count
                return b'x' * count
            def assert_size(self, size):
                if size != 65536:
                    raise AssertionError('Unbounded hashing read')
        self.assertEqual(digest_stream(BoundedStream()), hashlib.sha256(b'x' * 200000).hexdigest().upper())

    def test_actual_bundle_manifest_and_payload(self):
        folder = PORT / 'native_release'
        release = json.loads((folder / 'RELEASE_QUALIFICATION.json').read_text())
        proof = next(item for item in release['artifacts'] if item['file'] == 'MK2KS_NATIVE_WITH_STOCK_MAME.zip')
        path = folder / proof['file']
        with path.open('rb') as stream:
            self.assertEqual(digest_stream(stream), proof['SHA256'])
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            self.assertEqual(len(names), 34)
            self.assertEqual(len(names), len(set(names)))
            pins = json.loads(archive.read('FILES.json'))
            self.assertEqual(set(names), set(pins) | {'FILES.json'})
            self.assertEqual(len([name for name in names if name.endswith('.ips')]), 14)
            self.assertFalse(any(name.startswith(('roms/', 'source/')) for name in names))
            for name, expected in pins.items():
                with archive.open(name) as stream:
                    self.assertEqual(digest_stream(stream), expected, name)
            readme = archive.read('README_PATCHING.txt').decode('ascii')
            self.assertIn('NATIVE ROM PORT', readme)
            self.assertIn('separate MK2KS_NATIVE_SOURCE_AND_IPS.zip', readme)
            self.assertIn('FIRST BOOT', readme)
            self.assertIn('P1 High Punch', readme)
            self.assertIn(b' -noreadconfig ',archive.read('PLAY.cmd'))
        self.assertTrue(proof['isolatedPatcherReproducedExactTestedROM'])
        self.assertTrue(release['releaseApproved'])
        self.assertFalse(release['customDriver'])
        self.assertFalse(release['gameROMsIncluded'])


if __name__ == '__main__':
    unittest.main()
