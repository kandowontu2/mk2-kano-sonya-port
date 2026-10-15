"""Actual current stock reaction fixtures and fail-closed evidence mutations."""
import json
import re
import unittest

import verify_stock_reaction as check


class StockReaction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={}
        for folder in check.ROOT.glob('audit_v364_stock_reaction_*'):
            meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            cls.logs[(meta['victim'],meta['effect'],meta['side'])]=(folder/'run.log').read_text(encoding='utf-8-sig')

    def rejects(self,log):
        proof=check.verify_log(log,'sonya','shock',2)
        self.assertFalse(proof['passed'],proof)

    def change(self,tag,old,new,age=None,remove=False):
        lines=self.logs[('sonya','shock',2)].splitlines(keepends=True)
        for i,line in enumerate(lines):
            if line.startswith('MK2_STOCK_REACTION_'+tag+' ') and old in line and (age is None or f'age={age} ' in line):
                lines[i]='' if remove else line.replace(old,new)
                return ''.join(lines)
        self.fail('Mutation must change actual captured evidence')

    def test_all_eight_current_owned_reactions(self):
        for victim in ('kano','sonya'):
            for effect in ('freeze','shock'):
                for side in (1,2):
                    with self.subTest(victim=victim,effect=effect,side=side):
                        proof=check.verify_log(self.logs[(victim,effect,side)],victim,effect,side)
                        self.assertTrue(proof['passed'],proof)
                        self.assertEqual(proof['fields'],1301)
                        self.assertEqual(proof['contacts'],4)

    def test_two_original_cage_controls_without_custom_name_claim(self):
        for effect in ('freeze','shock'):
            proof=check.verify_log(self.logs[('cage',effect,1)],'cage',effect,1)
            self.assertTrue(proof['passed'],proof)
            self.assertEqual(proof['stock_control_custom_name_checks'],'inapplicable_zero_checks')

    def test_scope_not_whole_goal_or_every_pixel(self):
        proof=check.verify_log(self.logs[('sonya','shock',2)],'sonya','shock',2)
        self.assertFalse(proof['whole_character_integration_complete'])
        self.assertIn('not_all_projectiles_bitmap_audio',proof['scope'])

    def test_missing_field(self):self.rejects(self.change('FIELD','age=1160 ','',remove=True))
    def test_proxy_identity(self):self.rejects(self.change('FIELD','id=18 attack_state','id=1 attack_state'))
    def test_proxy_roster(self):self.rejects(self.change('FIELD','own_roster=18','own_roster=1'))
    def test_other_controller(self):self.rejects(self.change('FIELD','attack_state=1','attack_state=0'))
    def test_actor_replaced(self):self.rejects(self.change('FIELD','published=010350A0','published=010352B0'))
    def test_main_replaced(self):self.rejects(self.change('FIELD','published_main=0106B840','published_main=0106A370'))
    def test_no_guest_writes(self):self.rejects(self.change('FIELD','writes=0','writes=1'))
    def test_no_undeclared_health_assistance(self):self.rejects(self.change('FIELD','hp=73 attack_hp','hp=161 attack_hp',age=1160))
    def test_damage_native_pc(self):self.rejects(self.change('DAMAGE','pc=FF836700','pc=00000000'))
    def test_correct_health_slot(self):self.rejects(self.change('DAMAGE','address=01060EC0','address=010602F0'))
    def test_stock_damage_not_reduced(self):self.rejects(self.change('DAMAGE','new=139','new=140'))
    def test_four_contacts_required(self):self.rejects(self.change('DAMAGE','new=73','',remove=True))
    def test_four_lookups_required(self):self.rejects(self.logs[('sonya','shock',2)].replace('MK2_BLUE_LOOKUP frame=2179','REMOVED frame=2179'))
    def test_original_queue_source(self):self.rejects(self.logs[('sonya','shock',2)].replace('source=FFFAD210','source=FFFACD10'))
    def test_palette_queue_cannot_overrun(self):self.rejects(self.logs[('sonya','shock',2)].replace('count=64','count=4096'))
    def test_no_palette_restoration_is_rejected(self):
        log=self.logs[('sonya','shock',2)]
        blue,_normal,_record=check.references('sonya')
        color_text=','.join(f'{v:04X}' for v in blue)
        self.rejects(re.sub(r'colors=[0-9A-F,]+',lambda m:'colors='+color_text,log))
    def test_missing_original_blue_colors(self):
        log=self.logs[('sonya','shock',2)]
        _blue,normal,_record=check.references('sonya')
        color_text=','.join(f'{v:04X}' for v in normal)
        self.rejects(re.sub(r'colors=[0-9A-F,]+',lambda m:'colors='+color_text,log))
    def test_normal_palette_one_opaque_color_corrupt(self):self.rejects(self.change('FIELD','colors=0000,7F99','colors=0000,0001',age=1290))
    def test_native_ready_returns_required(self):self.rejects(self.logs[('sonya','shock',2)].replace('pc=FF861360','pc=00000000'))
    def test_jump_control_required(self):self.rejects(self.change('INPUT','buttons=Up','buttons=Down'))
    def test_punch_activation_required(self):self.rejects(self.logs[('sonya','shock',2)].replace('action=0101','action=0000'))
    def test_final_child_not_left_attached(self):self.rejects(self.change('FIELD','trail=00000000','trail=010352B0',age=1290))
    def test_final_grounded_return(self):self.rejects(self.change('FIELD','y=81','y=40',age=1290))
    def test_name_shadow_failure_cannot_be_waived_for_new_characters(self):self.rejects(self.logs[('sonya','shock',2)].replace('MK2KS_HUD_SHADOW_RESULT pass=true','MK2KS_HUD_SHADOW_RESULT pass=false'))
    def test_lua_error_not_hidden_by_exit_zero(self):self.rejects(self.logs[('sonya','shock',2)]+'\n[LUA ERROR] bogus\n')


if __name__=='__main__':unittest.main()
