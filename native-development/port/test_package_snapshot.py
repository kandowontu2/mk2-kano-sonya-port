import tempfile
from pathlib import Path
import unittest
import zipfile
from package_native_patches import README,write_package_zip

class PackageSnapshotTests(unittest.TestCase):
    def test_current_finite_scope_is_not_a_finished_release_claim(self):
        self.assertIn('136 finite cases',README)
        self.assertIn('all14 human opponents',README)
        self.assertIn('NOT A FINISHED RELEASE',README)
        self.assertNotIn('advances to\n  Mileena',README)

    def test_failed_candidate_preserves_existing_zip_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'snapshot.zip';target.write_bytes(b'previous')
            with self.assertRaises(AssertionError):write_package_zip(target,{'forbidden.exe':b'x'})
            self.assertEqual(target.read_bytes(),b'previous')
            self.assertTrue(target.with_name('snapshot.candidate.zip').exists())

    def test_success_replaces_with_verified_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'snapshot.zip';target.write_bytes(b'previous')
            write_package_zip(target,{'README.txt':b'development'})
            with zipfile.ZipFile(target) as archive:
                self.assertEqual(archive.read('MK2KS_NATIVE_DEVELOPMENT/README.txt'),b'development')
            self.assertFalse(target.with_name('snapshot.candidate.zip').exists())
