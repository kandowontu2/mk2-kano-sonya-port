"""Ensure current user-facing launchers cannot silently run the withdrawn driver."""
from pathlib import Path
import json
import unittest

PORT=Path(__file__).resolve().parent
ROOT=PORT.parents[1]

class NativeLauncher(unittest.TestCase):
    def test_checked_workspace_entry_uses_only_native_rom_launcher(self):
        route=(ROOT/'PLAY_CURRENT_NATIVE_CHECKED.cmd').read_text()
        self.assertIn('romhack\\port\\PLAY_CURRENT_NATIVE.cmd',route)
        self.assertIn('call "%MK2KS_NATIVE_CMD%" %*',route)
        self.assertNotIn('mkport_candidate.exe',route)
        self.assertNotIn(' mk2ks ',route)

    def test_check_mode_exits_before_opening_stock_mame(self):
        launch=(PORT/'PLAY_CURRENT_NATIVE.cmd').read_text()
        self.assertLess(launch.index('check_native_launcher.ps1'),launch.index('if /I "%~1"=="--check"'))
        self.assertLess(launch.index('if /I "%~1"=="--check"'),launch.index('"%MK2KS_MAME%" mk3'))
        self.assertIn('-nocheat %*',launch)
        checker=(PORT/'check_native_launcher.ps1').read_text()
        self.assertIn('AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3',checker)
        packaging=json.loads((PORT/'development_patches/PACKAGING_VERIFICATION.json').read_text())
        self.assertIn(packaging['roundtrip']['SHA256'],checker)

if __name__=='__main__':unittest.main()
