"""In-memory ending evidence/photo corruptions; retained captures stay unchanged."""
import re
import unittest
import numpy as np
from PIL import Image
from verify_current_ending_presentation_v680_v1 import ROOT, verify


class EndingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=ROOT/'audit_v716_current_ending_kano_p1'
        cls.text=(cls.folder/'run.log').read_text(encoding='utf-8-sig')

    def check(self,text): return verify(self.folder,check_hashes=False,text_override=text)

    def reject(self,pattern,replacement):
        changed,count=re.subn(pattern,replacement,self.text,count=1,flags=re.M)
        self.assertEqual(count,1,'Mutation must hit actual retained evidence')
        self.assertFalse(self.check(changed)['passed'])

    def test_all_four_actual_presentations(self):
        for folder in [self.folder]+sorted(ROOT.glob('audit_v717_current_ending_*')):
            with self.subTest(case=folder.name):
                report=verify(folder,check_hashes=False)
                self.assertTrue(report['passed'],report['errors'])
                self.assertFalse(report['unassisted_clear_proven'])
                self.assertFalse(report['fullPortAcceptance'])
                self.assertFalse(report['audio']['audio_fidelity_accepted'])
                self.assertEqual(sum(p['compared_visible_pixels'] for p in report['rendered_photos']),105460)
                self.assertEqual(sum(p['stock_frame_overpaint_pixels_compared'] for p in report['rendered_photos']),1604)

    def test_stage_fixture_live(self): self.reject(r'(ENDING_FIXTURE_STAGE[^\n]*mode=)4 ',r'\g<1>2 ')
    def test_proxy_selection(self): self.reject(r'(ENDING_FIXTURE_STAGE[^\n]*own_roster=)17 ',r'\g<1>1 ')
    def test_wrong_initial_health_owner(self): self.reject(r'(ENDING_FIXTURE_HEALTH[^\n]*slot=)2 ',r'\g<1>1 ')
    def test_wrong_initial_health_field(self): self.reject(r'(ENDING_FIXTURE_HEALTH[^\n]*field=)01060EC0',r'\g<1>010602F0')
    def test_wrong_true_live_character(self): self.reject(r'(LIVE[^\n]*human=)17:17',r'\g<1>1:1')
    def test_wrong_native_KO_writer(self): self.reject(r'(HEALTH[^\n]*slot=2[^\n]*before=1 after=0 pc=)FF836700',r'\g<1>FF836710')
    def test_missing_final_KO(self): self.reject(r'^MK2_NAT_CAMPAIGN_HEALTH[^\n]*frame=2560[^\n]*slot=2[^\n]*before=1 after=0[^\n]*\n','')
    def test_wrong_first_winner(self): self.reject(r'(WIN[^\n]*slot=)1 ',r'\g<1>2 ')
    def test_wrong_ending_roster(self): self.reject(r'(ENDING_START[^\n]*roster=)17',r'\g<1>1')
    def test_no_actor_retirement(self): self.reject(r'(ENDING_START[^\n]*actors=)00000000,00000000',r'\g<1>01038640,01038850')
    def test_fixture_during_ending(self): self.reject(r'(ENDING_FIXTURE_RESULT[^\n]*last_fixture=)2142',r'\g<1>4000')
    def test_ending_writes_declared(self): self.reject(r'(ENDING_FIXTURE_RESULT[^\n]*ending_writes=)0 ',r'\g<1>1 ')
    def test_wrong_photo_pointer(self): self.reject(r'(PICTURE[^\n]*page=1[^\n]*value=)0000',r'\g<1>0001')
    def test_wrong_photo_table_index(self): self.reject(r'(PICTURE[^\n]*page=1[^\n]*entry=)FFFA4E40',r'\g<1>FFFA4A40')
    def test_wrong_photo_renderer(self): self.reject(r'(PICTURE[^\n]*pc=)FF8447E0',r'\g<1>FF8447F0')
    def test_missing_page2(self): self.reject(r'^MK2_NAT_CAMPAIGN_PICTURE[^\n]*page=2[^\n]*\n','')
    def test_wrong_text_pointer(self): self.reject(r'(TEXT[^\n]*page=1 segment=1[^\n]*value=)6600',r'\g<1>6601')
    def test_wrong_text_roster(self): self.reject(r'(TEXT[^\n]*roster=)17',r'\g<1>1')
    def test_premature_attract(self): self.reject(r'(ENDING_COMPLETED[^\n]*age=)2740 ',r'\g<1>1200 ')
    def test_incomplete_attract_counts(self): self.reject(r'(ENDING_COMPLETED[^\n]*pictures=)1,1',r'\g<1>1,0')
    def test_actual_photo_pixel_corruption(self):
        name='ending_page1_3950.png';image=np.asarray(Image.open(self.folder/'snap'/name).convert('RGB')).copy()
        image[92,80,0]^=1
        self.assertFalse(verify(self.folder,check_hashes=False,image_override={name:image})['passed'])
    def test_actual_stock_frame_edge_corruption(self):
        name='ending_page1_3950.png';image=np.asarray(Image.open(self.folder/'snap'/name).convert('RGB')).copy()
        image[41,30,0]^=1
        self.assertFalse(verify(self.folder,check_hashes=False,image_override={name:image})['passed'])
    def test_runtime_error(self): self.assertFalse(self.check(self.text+'\n[LUA ERROR] failed ending observer\n')['passed'])


if __name__=='__main__':unittest.main()
