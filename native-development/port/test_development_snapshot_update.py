import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from export_native_development_source import validate_previous


class SnapshotUpdateTests(unittest.TestCase):
    def test_manifest_checks_before_update(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'source.py').write_bytes(b'original')
            pins = {'source.py': hashlib.sha256(b'original').hexdigest().upper()}
            (root/'FILES.json').write_text(json.dumps(pins))
            self.assertEqual(validate_previous(root), pins)
            (root/'source.py').write_bytes(b'user edit')
            with self.assertRaises(AssertionError): validate_previous(root)

    def test_unrecorded_files_refuse_update(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'FILES.json').write_text('{}')
            (root/'extra.txt').write_text('keep')
            with self.assertRaises(AssertionError): validate_previous(root)


if __name__ == '__main__': unittest.main()
