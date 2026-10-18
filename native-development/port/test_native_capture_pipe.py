import os
from pathlib import Path
import shutil
import tempfile
import unittest

if os.name == 'nt':
    from native_capture_pipe import CapturePipe


@unittest.skipUnless(os.name == 'nt' and shutil.which('ffmpeg'), 'Windows/ffmpeg pipe checks')
class NativePipeTests(unittest.TestCase):
    def fixture(self):
        root = Path(__file__).parent
        temporary = tempfile.TemporaryDirectory(prefix='pipe-unit-', dir=root)
        self.addCleanup(temporary.cleanup)
        work = Path(temporary.name).resolve()
        self.assertTrue(work.is_relative_to(root.resolve()))
        return CapturePipe(work / 'test.mp4', 55, 2, 5)

    def test_cancel_before_writer_connects_leaves_no_encoder(self):
        capture = self.fixture()
        capture.abort()
        self.assertFalse(capture.thread.is_alive())
        self.assertIsNotNone(capture.process.poll())
        self.assertIsNone(capture.result)

    def test_partial_frame_cannot_qualify(self):
        capture = self.fixture()
        try:
            with open(capture.address, 'wb', buffering=0) as stream:
                stream.write(b'bad!')
            with self.assertRaises(AssertionError):
                capture.finish()
        finally:
            if capture.thread.is_alive():
                capture.abort()
        self.assertIsNone(capture.result)


if __name__ == '__main__':
    unittest.main()
