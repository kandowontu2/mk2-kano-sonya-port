import tempfile
import unittest
from pathlib import Path
from recovery_evidence import sha,verify


class RecoveryEvidenceTests(unittest.TestCase):
    def test_all_pins_are_checked_after_valid_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            paths=[folder/name for name in ('execution.json','autoboot.lua','verifier.py','cleanup.csv')]
            for path in paths:path.write_bytes(b'valid baseline')
            proof=dict(verifierSHA256=sha(paths[2]),evidenceSHA256={str(path):sha(path) for path in paths})
            verify(folder,proof,paths[2])
            paths[3].write_bytes(b'altered cleanup')
            with self.assertRaises(AssertionError):verify(folder,proof,paths[2])

    def test_missing_required_pin_and_stale_verifier_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            paths=[folder/name for name in ('execution.json','autoboot.lua','verifier.py')]
            for path in paths:path.write_bytes(b'valid baseline')
            proof=dict(verifierSHA256=sha(paths[2]),evidenceSHA256={str(path):sha(path) for path in paths})
            verify(folder,proof,paths[2])
            with self.assertRaises(AssertionError):verify(folder,dict(proof,verifierSHA256='0'*64),paths[2])
            del proof['evidenceSHA256'][str(paths[0])]
            with self.assertRaises(AssertionError):verify(folder,proof,paths[2])
