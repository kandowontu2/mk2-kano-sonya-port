import unittest
from qualify_normal_contact import contact_spec

class NormalContactSpecTests(unittest.TestCase):
    def test_jumping_damage_matches_native_tables_for_both_characters(self):
        import re
        from pathlib import Path
        source=(Path(__file__).parent.parent/'baseline/mk2-rebuild-main/srcp/MKSTK.ASM').read_text()
        for actor in ('kano','sonya'):
            for move,gap,label in (('jumpkick',70,'lkjumpupk'),('jumppunch',70,'lkjumpupp'),
                                   ('flyingkick',180,'lkflipk'),('flyingpunch',180,'lkflipp')):
                record=re.search(r'^ks_'+actor+'_stk_'+label+r'\n(.*?)(?=^ks_|\Z)',source,re.M|re.S).group(1)
                packed=int(re.search(r'\.word\s+([0-9a-f]+)h\s*; damage',record,re.I).group(1),16)
                self.assertEqual(contact_spec(move,gap,False)[1],packed>>8)
                self.assertEqual(contact_spec(move,gap,True)[1],packed&255)
    def test_ground_damage_matches_native_tables_not_measured_whiffs(self):
        import re
        from pathlib import Path
        source=(Path(__file__).parent.parent/'baseline/mk2-rebuild-main/srcp/MKSTK.ASM').read_text()
        for actor in ('kano','sonya'):
            for move,gap,label in (('roundhouse',90,'lkroundh'),('sweep',90,'lksweepk'),
                ('uppercut',70,'lkuppercut'),('duckpunch',70,'lkduckpunch'),
                ('duckhighkick',70,'lkduckkickh'),('ducklowkick',70,'lkduckkickl')):
                record=re.search(r'^ks_'+actor+'_stk_'+label+r'\n(.*?)(?=^ks_|\Z)',source,re.M|re.S).group(1)
                packed=int(re.search(r'\.word\s+([0-9a-f]+)h\s*; damage',record,re.I).group(1),16)
                self.assertEqual(contact_spec(move,gap,False)[1],packed>>8)
                self.assertEqual(contact_spec(move,gap,True)[1],packed&255)
    def test_punch_damage_matches_both_native_character_tables(self):
        import re
        from pathlib import Path
        source=(Path(__file__).parent.parent/'baseline/mk2-rebuild-main/srcp/MKSTK.ASM').read_text()
        for actor in ('kano','sonya'):
            for move,label in (('hp','lkhipunch'),('lp','lklopunch')):
                record=source.split(f'ks_{actor}_stk_{label}\n',1)[1].split('\n\n',1)[0]
                packed=int(re.search(r'\.word\s+([0-9a-fA-F]+)H\s*; damage',record).group(1),16)
                self.assertEqual(contact_spec(move,90,False)[1],packed>>8)
                self.assertEqual(contact_spec(move,90,True)[1],packed&255)
    def test_proximity_attacks_are_not_mislabeled_as_standing_punches(self):
        self.assertEqual(contact_spec('hp',70,False),(0x114,24,0x503))
        self.assertEqual(contact_spec('lp',70,True),(0x507,34,0x226))
        self.assertEqual(contact_spec('lp',100,False),(0x102,8,None))

    def test_native_punch_chip_does_not_accept_a_zero_damage_whiff(self):
        self.assertEqual(contact_spec('hp',100,True),(0x101,3,None))
        self.assertEqual(contact_spec('hp',100,False),(0x101,11,None))
        self.assertEqual(contact_spec('hp',90,True),(0x101,3,None))
        self.assertEqual(contact_spec('lp',90,True),(0x102,2,None))
        with self.assertRaises(KeyError):contact_spec('lk',70,False)
