import re
import unittest
from pathlib import Path
from verify_p2_tower import verify

ROOT=Path(__file__).resolve().parents[1]


class NativeP2TowerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logs={fighter:(ROOT/f'audit_v274_verified_p2_tower_{fighter}/run.log').read_text(encoding='utf-8-sig')
                  for fighter in ('kano','sonya')}

    def test_actual_both_complete_native_towers(self):
        for fighter,log in self.logs.items():
            result=verify(log,fighter)
            self.assertTrue(result['passed'],result['errors'])
            self.assertEqual(result['assistance'],'health_only')
            self.assertFalse(result['unassisted_clear_proven'])
            self.assertEqual(result['own_ending_pages'],{'PICTURE':[1,1],'TEXT':[3,3]})

    def test_actual_incomplete_pilot_and_uncorrected_base_rejected(self):
        for folder in ('audit_v274_p2_tower_kano','audit_v274_p2_tower_native_kano'):
            self.assertFalse(verify((ROOT/f'{folder}/run.log').read_text(encoding='utf-8-sig'),'kano')['passed'])

    def test_wrong_human_identity_rejected(self):
        log=re.sub(r'(MK2_P2_TOWER_LIVE[^\r\n]* human=17:)17',r'\g<1>1',self.logs['kano'],count=1)
        self.assertNotEqual(log,self.logs['kano'])
        self.assertFalse(verify(log,'kano')['passed'])

    def test_wrong_cpu_identity_rejected(self):
        log=re.sub(r'(MK2_P2_TOWER_LIVE[^\r\n]* cpu=18:)18',r'\g<1>1',self.logs['kano'],count=1)
        self.assertNotEqual(log,self.logs['kano'])
        self.assertFalse(verify(log,'kano')['passed'])

    def test_morph_without_native_store_rejected(self):
        log=re.sub(r'^MK2_NATIVE_SHANG_ID[^\r\n]*\r?\n','',self.logs['kano'],flags=re.M)
        self.assertNotEqual(log,self.logs['kano'])
        self.assertFalse(verify(log,'kano')['passed'])

    def test_morph_wrong_writer_rejected(self):
        log=self.logs['kano'].replace('pc=FF86E670 a9=','pc=FF86E680 a9=',1)
        self.assertNotEqual(log,self.logs['kano'])
        self.assertFalse(verify(log,'kano')['passed'])

    def test_morph_wrong_source_register_rejected(self):
        log=re.sub(r'(MK2_NATIVE_SHANG_ID[^\r\n]* pc=FF86E670 a9=)[0-9A-F]+',r'\g<1>0000000C',self.logs['kano'],count=1)
        self.assertNotEqual(log,self.logs['kano'])
        self.assertFalse(verify(log,'kano')['passed'])

    def test_missing_native_win_rejected(self):
        log=re.sub(r'^MK2_P2_TOWER_WIN[^\r\n]*\r?\n','',self.logs['kano'],count=1,flags=re.M)
        self.assertFalse(verify(log,'kano')['passed'])

    def test_timeout_requires_real_native_winner_scene(self):
        win=re.search(r'MK2_P2_TOWER_WIN frame=(\d+)[^\r\n]* health=1,161',self.logs['kano'])
        self.assertIsNotNone(win)
        frame=int(win[1])+1
        log=re.sub(rf'(MK2_P2_TOWER_STATE frame={frame}[^\r\n]* winner=)2',r'\g<1>1',self.logs['kano'])
        self.assertNotEqual(log,self.logs['kano'])
        self.assertFalse(verify(log,'kano')['passed'])

    def test_missing_last_boss_stage_rejected(self):
        log=re.sub(r'^MK2_P2_TOWER_STAGE[^\r\n]* stage=16[^\r\n]*\r?\n','',self.logs['kano'],flags=re.M)
        self.assertFalse(verify(log,'kano')['passed'])

    def test_wrong_ending_picture_owner_rejected(self):
        log=re.sub(r'(MK2_P2_TOWER_PICTURE[^\r\n]* roster=)17',r'\g<1>1',self.logs['kano'],count=1)
        self.assertFalse(verify(log,'kano')['passed'])

    def test_missing_second_story_page_rejected(self):
        log=re.sub(r'^MK2_P2_TOWER_TEXT[^\r\n]* page=2[^\r\n]*\r?\n','',self.logs['kano'],flags=re.M)
        self.assertFalse(verify(log,'kano')['passed'])

    def test_false_ending_completion_rejected(self):
        log=re.sub(r'(MK2_P2_TOWER_COMPLETED[^\r\n]* mode=)11',r'\g<1>2',self.logs['kano'])
        self.assertFalse(verify(log,'kano')['passed'])

    def test_undeclared_health_assistance_rejected(self):
        self.assertFalse(verify(self.logs['kano'].replace('assistance=health_only','assistance=none'),'kano')['passed'])

    def test_position_assistance_rejected(self):
        self.assertFalse(verify(self.logs['kano']+'\nMK2_FINISH_POSITION_ASSIST applied','kano')['passed'])

    def test_duplicate_native_schedule_rejected(self):
        row=re.search(r'^MK2_P2_TOWER_ROM[^\r\n]*',self.logs['kano'],re.M)[0]
        self.assertFalse(verify(self.logs['kano']+'\n'+row,'kano')['passed'])


if __name__=='__main__': unittest.main()
