from pathlib import Path
import unittest


class CampaignStreamSourceTests(unittest.TestCase):
    def test_capture_only_reads_pixels_and_uses_bounded_stream(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_stream_capture.lua').read_text()
        self.assertIn(';(function()',source)
        self.assertTrue(source.rstrip().endswith('end)()'))
        self.assertIn('count<=maximum',source)
        self.assertIn('frame==last+1',source)
        self.assertIn('screen:pixels()',source)
        self.assertIn("io.open(endpoint,'wb')",source)
        self.assertNotIn(':write_u',source)
        self.assertNotIn(':set_value',source)

    def test_termination_closes_capture_before_native_process_exit(self):
        here=Path(__file__).parent
        source=(here/'diagnostics/campaign_probe.lua').read_text()
        self.assertLess(source.index('ks_stream_capture_close(n)'),source.index('continueLog:close();log:close();m:exit()'))


if __name__=='__main__':unittest.main()
