"""Native victim table bounds and ground anchor arithmetic; not visual QA."""
import unittest
import zipfile
from pathlib import Path
from inventory_character_tables import source_tables

PORT=Path(__file__).parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'

class ClappedLineups(unittest.TestCase):
    def test_physical_clap_probe_matches_native_release_command(self):
        controller=(PORT/'diagnostics/extract_probe.lua').read_text()
        self.assertIn("if clap then actor=11 end",controller)
        self.assertIn("if ws~=3 then lo[player..' Low Punch']:set_value(1) end",controller)
        command=controller.split('elseif clap then',1)[1].split('elseif tongue then',1)[0]
        self.assertIn("lo[player..' Low Punch']:set_value(t<30 and 1 or 0)",command)
        for pulse in ('t>=6 and t<10','t>=14 and t<18','t>=22 and t<26'):
            self.assertIn(pulse,command)
        native=(SRC/'MOVES.ASM').read_text()
        release=native.split('\njx_lp_open\n',1)[1].split('\njc_lp_open\n',1)[0]
        self.assertIn('040H,a1',release)
        self.assertIn('scom_jx_db1,a11',release)
        self.assertIn('do_fatality_1,a7',release)
        self.assertNotIn('write_u',controller)

    def test_preserve_original_and_bound_all_native_ids(self):
        table=source_tables((SRC/'MKDEATH.ASM').read_text())['clapped_lineups']
        values=[v.lower() for row in table['rows'] for v in row['values']]
        self.assertTrue(all(row['type']=='word' for row in table['rows']))
        with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as archive:
            original=source_tables(archive.read('mk2-rebuild-main/src/MKDEATH.ASM').decode('cp437'))['clapped_lineups']
        prior=[v.lower() for row in original['rows'] for v in row['values']]
        self.assertEqual(len(prior),32)
        self.assertEqual(values[:32],prior)
        self.assertEqual(len(values),38)
        self.assertEqual(values[32:],['-060h','0','-060h','8','-060h','7'])

    def test_own_ground_compensation_uses_performer_anchor(self):
        util=(SRC/'MKUTIL.ASM').read_text()
        matching=util.split('\nmatch_ani_points\n',1)[1].split('\nmap9',1)[0]
        self.assertIn('move\t*a8(oyval),*a0(oyval),l',matching)
        table=source_tables((SRC/'MKGUYS.ASM').read_text())['ochar_ground_offsets']
        raw=[v for row in table['rows'] for v in row['values']]
        number=lambda value:int(value[:-1],16) if value.lower().endswith('h') else int(value)
        ground=list(map(number,raw))
        self.assertEqual([ground[11]-ground[i] for i in (17,18)],[8,7])
        for floor in (240,254,300):
            self.assertEqual(floor-ground[11]+8+ground[17],floor)
            self.assertEqual(floor-ground[11]+7+ground[18],floor)

if __name__=='__main__': unittest.main()
