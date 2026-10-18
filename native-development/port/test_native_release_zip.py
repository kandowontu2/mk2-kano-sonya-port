import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from build_native_release import write_checked
from prepare_native_release_evidence import digest


class NativeReleaseZipTests(unittest.TestCase):
    def test_streamed_and_memory_members_are_exact_and_pinned(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            disk = root/'input.txt'
            disk.write_bytes(b'from disk')
            output = root/'release.zip'
            report = write_checked(output, {'memory.txt': b'from memory', 'disk.txt': disk})
            self.assertEqual(report['SHA256'], digest(output))
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(archive.read('memory.txt'), b'from memory')
                self.assertEqual(archive.read('disk.txt'), b'from disk')
                self.assertEqual(json.loads(archive.read('FILES.json'))['disk.txt'], digest(disk))
            self.assertFalse(output.with_suffix('.zip.partial').exists())
            before = output.read_bytes()
            with self.assertRaises(AssertionError):
                write_checked(output, {'other.txt': b'replacement'})
            self.assertEqual(output.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
