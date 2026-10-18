import subprocess
import sys
import unittest
from pathlib import Path

class OwnThrowInputTests(unittest.TestCase):
    def invoke(self,*args):
        flags=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0
        return subprocess.run([sys.executable,str(Path(__file__).with_name('qualify_own_throw.py')),*args],
            capture_output=True,text=True,creationflags=flags,timeout=10)

    def test_empty_invocation_cannot_report_success(self):
        result=self.invoke()
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Supply distinct completed throw fixtures',result.stderr)

    def test_duplicate_and_outside_names_rejected(self):
        duplicate=self.invoke('same','same')
        self.assertNotEqual(duplicate.returncode,0)
        self.assertIn('Supply distinct completed throw fixtures',duplicate.stderr)
        outside=self.invoke('../outside')
        self.assertNotEqual(outside.returncode,0)
        self.assertIn('AssertionError',outside.stderr)
        self.assertNotIn('FileNotFoundError',outside.stderr)
