import unittest
from campaign_rounds import require_clean_runtime_log


class CampaignLogTests(unittest.TestCase):
    def test_checksum_warning_is_not_a_runtime_crash(self):
        require_clean_runtime_log('WRONG CHECKSUMS:\nWARNING: the machine might not run correctly.\nAverage speed: 1400%')

    def test_fatal_failure_rejected_even_after_valid_gameplay(self):
        for marker in ('Fatal error:', 'FATAL ERROR:', 'fatal error:'):
            with self.subTest(marker=marker), self.assertRaises(AssertionError):
                require_clean_runtime_log('Average speed: 1400%\n' + marker + ' callback failed')

    def test_lua_failure_rejected(self):
        with self.assertRaises(AssertionError):
            require_clean_runtime_log('[LUA ERROR] in frame callback')


if __name__ == '__main__':
    unittest.main()
