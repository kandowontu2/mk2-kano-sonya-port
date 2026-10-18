"""Independent checks of the actual minimal local player artifact."""
import hashlib
import json
import unittest
import zipfile
from build_native_player_playtest import digest_stream
from inspect_normal_runtime import PORT


class PlayerBundleTests(unittest.TestCase):
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
        folder = PORT / 'development_patches'
        proof = json.loads((folder / 'PLAYER_PLAYTEST_QUALIFICATION.json').read_text())
        path = folder / 'MK2KS_NATIVE_PLAYTEST_WITH_STOCK_MAME.zip'
        with path.open('rb') as stream:
            self.assertEqual(digest_stream(stream), proof['SHA256'])
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            self.assertEqual(len(names), 33)
            self.assertEqual(len(names), len(set(names)))
            pins = json.loads(archive.read('FILES.json'))
            self.assertEqual(set(names), set(pins) | {'FILES.json'})
            self.assertEqual(len([name for name in names if name.endswith('.ips')]), 14)
            self.assertFalse(any(name.startswith(('roms/', 'source/')) for name in names))
            for name, expected in pins.items():
                with archive.open(name) as stream:
                    self.assertEqual(digest_stream(stream), expected, name)
            readme = archive.read('README_PATCHING.txt').decode('ascii')
            self.assertIn('UNFINISHED NATIVE PLAYTEST', readme)
            self.assertIn('SEPARATE', readme)
        self.assertTrue(proof['isolatedPatcherReproducedExactTestedROM'])
        self.assertFalse(proof['releaseApproved'])
        self.assertFalse(proof['fullPortVerified'])


if __name__ == '__main__':
    unittest.main()
