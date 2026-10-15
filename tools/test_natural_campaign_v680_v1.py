"""In-memory corruption checks for current genuine campaign progression proof."""
import re
import unittest
from verify_natural_campaign_v680_v2 import ROOT,verify

FOLDER=ROOT/'audit_v706_native_tower_kano_p1'


class NativeCampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log=(FOLDER/'run.log').read_text(encoding='utf-8-sig')

    def check(self,text):
        return verify(FOLDER,check_hashes=False,text_override=text)

    def reject(self,pattern,replacement):
        changed,count=re.subn(pattern,replacement,self.log,count=1,flags=re.M)
        self.assertEqual(count,1,'Mutation must hit its exact retained evidence')
        self.assertFalse(self.check(changed)['passed'])

    def test_baseline_is_progress_not_clear(self):
        report=self.check(self.log)
        self.assertTrue(report['passed'],report['errors'])
        self.assertFalse(report['unassisted_clear_proven'])
        self.assertFalse(report['fullPortAcceptance'])
        self.assertEqual(report['stages_reached'],list(range(13))+[14,15])
        self.assertEqual(report['native_own_round_wins'],31)

    def test_proxy_human(self):self.reject(r'(MK2_NAT_CAMPAIGN_LIVE[^\n]*human=)17:17',r'\g<1>1:1')
    def test_wrong_cpu(self):self.reject(r'(MK2_NAT_CAMPAIGN_LIVE[^\n]*cpu=)18:18',r'\g<1>8:8')
    def test_changed_schedule(self):self.reject(r'(MK2_NAT_CAMPAIGN_LIVE[^\n]*schedule=)FFFA3180',r'\g<1>FFFA3000')
    def test_invalid_Main(self):self.reject(r'(MK2_NAT_CAMPAIGN_LIVE[^\n]*human_main=)[0-9A-F]+',r'\g<1>00000000')
    def test_missing_winner(self):self.reject(r'^MK2_NAT_CAMPAIGN_WIN[^\n]*\n','')
    def test_wrong_winner_instruction(self):self.reject(r'(MK2_NAT_CAMPAIGN_WIN[^\n]*pc=)FF8296B0',r'\g<1>FF8296C0')
    def test_wrong_win_entry(self):self.reject(r'(MK2_NAT_CAMPAIGN_WIN[^\n]*entry=)FFFEFA40',r'\g<1>FFFEFA20')
    def test_wrong_health_writer(self):self.reject(r'(MK2_NAT_CAMPAIGN_HEALTH[^\n]*before=161 after=139 pc=)FF836700',r'\g<1>FF836710')
    def test_premature_stage_advance(self):self.reject(r'(MK2_NAT_CAMPAIGN_STAGE[^\n]*stage=)1 ',r'\g<1>2 ')
    def test_continue_to_wrong_stage(self):self.reject(r'(MK2_NAT_CAMPAIGN_SELECT[^\n]*number=2[^\n]*stage=)1 ',r'\g<1>0 ')
    def test_wrong_continue_ancestry(self):self.reject(r'(MK2_NAT_CAMPAIGN_SELECT[^\n]*number=2[^\n]*continue=)9957',r'\g<1>1')
    def test_wrong_selection_identity(self):self.reject(r'(MK2_NAT_CAMPAIGN_SELECT_ID[^\n]*roster=)17 ',r'\g<1>1 ')
    def test_runtime_error(self):self.assertFalse(self.check(self.log+'\n[LUA ERROR] test driver failure\n')['passed'])
    def test_declared_assistance(self):self.reject(r'(MK2_NAT_CAMPAIGN_LIVE[^\n]*assistance=)none ',r'\g<1>health_only ')
    def test_duplicate_boot(self):
        line=next(line for line in self.log.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_BOOT '))
        self.assertFalse(self.check(self.log+'\n'+line+'\n')['passed'])


if __name__=='__main__':unittest.main()
