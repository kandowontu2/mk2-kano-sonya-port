import unittest
from inspect_normal_runtime import PORT


class ShortRouteInputTests(unittest.TestCase):
    def test_physical_input_body_matches_search_and_preserves_final_release(self):
        search=(PORT/'diagnostics/kintaro_short_search.lua').read_text()
        replay=(PORT/'diagnostics/campaign_probe.lua').read_text()
        search=search.split('local function input(action,age)',1)[1].split('local function finish',1)[0]
        replay=replay.split('subBallRecovery.applyShortRoute=function(action,age,toward,away)',1)[1].split('if subBallRecovery.kintaroVertical then',1)[0]
        self.assertIn('if age==120 then return end',replay)
        search=search[search.index('local phase='):].rsplit('\nend',1)[0]
        replay=replay[replay.index('local phase='):].rsplit('\n end',1)[0]
        normalize=lambda text:[line.strip() for line in text.splitlines() if line.strip()]
        self.assertEqual(normalize(search),normalize(replay))


if __name__=='__main__':unittest.main()
