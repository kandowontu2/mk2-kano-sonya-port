import unittest
from native_roster import verified_names

class NativeRoster(unittest.TestCase):
    def test_full_actor_names_do_not_expand_selectable_roster(self):
        names=verified_names(include_nonselectable=True)
        self.assertEqual(set(names),set(range(19)))
        self.assertEqual([names[i] for i in range(12,17)],
                         ['KINTARO','SHAO KAHN','SMOKE','NOOB SAIBOT','JADE'])
        self.assertEqual(len(verified_names()),14)

    def test_own_identity_equate_mismatch_is_rejected(self):
        from unittest.mock import patch,Mock
        from native_roster import SOURCE
        source=SOURCE.read_text()
        import re
        for symbol in ('ft_kano','ft_sonya'):
            changed=re.sub(r'(?m)^('+symbol+r'\s+\.set\s+)\d+',r'\g<1>16',source)
            self.assertNotEqual(changed,source)
            with patch('native_roster.SOURCE',Mock(read_text=lambda:changed)):
                with self.assertRaises(AssertionError): verified_names()

    def test_actual_native_ids_not_visual_positions(self):
        names=verified_names()
        self.assertEqual(names[5],'MILEENA')
        self.assertEqual(names[7],'RAIDEN')
        self.assertEqual(names[4],'KITANA')
        self.assertEqual(names[17],'KANO')
        self.assertEqual(names[18],'SONYA')
        self.assertEqual(len(names),14)

    def test_controller_uses_correct_matchups(self):
        from pathlib import Path
        source=(Path(__file__).parent/'diagnostics/campaign_probe.lua').read_text()
        self.assertNotIn('mileenaKnife',source)
        self.assertNotIn('(c2==4 or c2==7)',source)
        self.assertIn('raidenKnife and c2==7',source)
        self.assertIn('(c2==4 or c2==5)',source)

    def test_native_throw_away_uses_relative_position(self):
        from native_roster import SOURCE
        source=(SOURCE.parent/'JOY.ASM').read_text()
        helper=source.split('\nis_stick_away\n',1)[1].split('\nis_stick_down\n',1)[0]
        self.assertIn('calla\tis_he_right',helper)
        self.assertNotIn('m_fliph',helper)

    def test_guard_action_ids_match_native_equates(self):
        import re
        from native_roster import SOURCE
        source=SOURCE.read_text()
        for name,value in {'act_throw_fans':8,'act_air_fans':9,
                           'act_lkzap_lo':2,'act_lkzap_hi':3,'act_lkzap_air':4,
                           'act_superkang':0x203,'act_bike':0x204,
                           'act_throw_bolt':0x0f,'act_dive':0x209,
                           'pm_reacting':4,'pm_sitduck':8,'pm_special':0x10}.items():
            match=re.search(r'^'+name+r'\s+\.set\s+([0-9a-fA-F]+)H',source,re.M|re.I)
            self.assertIsNotNone(match,name)
            self.assertEqual(int(match.group(1),16),value,name)

if __name__=='__main__':unittest.main()
