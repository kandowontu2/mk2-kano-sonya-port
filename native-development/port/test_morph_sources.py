import json
from pathlib import Path
import unittest
import re
import struct
import zipfile
from build_inflation_assets import unpack6
from PIL import Image
from build_arm_rip_assets import read_pgm,sha

PORT=Path(__file__).resolve().parent
class MorphSources(unittest.TestCase):
    def test_rejoin_requires_selected_and_actual_shang_in_fresh_match(self):
        source=(PORT/'qualify_finisher_rejoin.py').read_text()
        wrapper=(PORT.parent/'baseline/test_wolf_baseline.py').read_text()
        self.assertIn("if '--finisher-rejoin' in sys.argv:",wrapper)
        self.assertIn('selected_actor=6 if morphed else actor',source)
        self.assertIn("identities[r['frame']]['selected']==identities[r['frame']]['actual']=='6'",source)
        self.assertIn('assert len(fresh)==600',source)

    def test_finisher_morph_selects_shang_and_logs_actual_identity(self):
        wrapper=(PORT.parent/'baseline/test_wolf_baseline.py').read_text()
        probe=(PORT/'diagnostics/extract_probe.lua').read_text()
        self.assertIn("if '--finisher-morph' in sys.argv:",wrapper)
        self.assertIn("local selectedActor=morphFinisher and 6 or actor",probe)
        self.assertIn('frame,selected,actual,winner,death,action',probe)
        self.assertIn('morphFinisher and fd==0 and u16(ko+0x1f0)~=actor',probe)
        self.assertIn('not morphCommandAge and u16(ownProcess+0x1f0)==0x303',probe)
        self.assertNotIn(':write_u',probe)

    def test_square_profile_jumps_opponent_with_physical_input(self):
        wrapper=(PORT.parent/'baseline/test_wolf_baseline.py').read_text()
        probe=(PORT/'diagnostics/morph_probe.lua').read_text()
        self.assertIn("if '--morph-square' in sys.argv:",wrapper)
        self.assertIn("fight>=1230 and fight<1234 then hi['P2 Up']:set_value(1)",probe)
        self.assertIn("fight>=1112 and fight<1116 or fight>=1246 and fight<1250",probe)
        self.assertNotIn(':write_u',probe)

    def test_grapples_observe_victim_and_use_only_physical_commands(self):
        wrapper=(PORT.parent/'baseline/test_wolf_baseline.py').read_text()
        probe=(PORT/'diagnostics/morph_probe.lua').read_text()
        self.assertIn("if '--morph-grapples' in sys.argv:",wrapper)
        self.assertIn('victimHP,victimAction',probe)
        self.assertIn("fight>=1150 and fight<1164 then hi['P1 Down']:set_value(1);hi['P1 Block']:set_value(1)",probe)
        self.assertIn("fight>=1154 and fight<1164 then hi['P1 Low Punch']:set_value(1)",probe)
        self.assertNotIn(':write_u',probe)

    def test_melee_profile_uses_physical_commands_without_guest_writes(self):
        wrapper=(PORT.parent/'baseline/test_wolf_baseline.py').read_text()
        probe=(PORT/'diagnostics/morph_probe.lua').read_text()
        self.assertIn("if '--morph-melee' in sys.argv:",wrapper)
        self.assertIn("('--morph-specials','--morph-throws','--morph-ball')",wrapper)
        self.assertIn("local melee=os.getenv('KS_MORPH_MELEE')=='1'",probe)
        self.assertIn('math.abs(u16(a+0x90)-u16(b+0x90))>84',probe)
        self.assertIn("fight>=1126 and fight<1130 then hi['P1 High Kick']:set_value(1)",probe)
        self.assertNotIn(':write_u',probe)

    def test_ball_controller_is_opt_in_and_charges_through_physical_input(self):
        wrapper=(PORT.parent/'baseline/test_wolf_baseline.py').read_text()
        probe=(PORT/'diagnostics/morph_probe.lua').read_text()
        self.assertIn("if '--morph-ball' in sys.argv:\n        assert game_candidate and '--morph' in sys.argv",wrapper)
        self.assertIn("assert '--morph-specials' not in sys.argv and '--morph-throws' not in sys.argv",wrapper)
        self.assertIn("local ball=os.getenv('KS_MORPH_BALL')=='1'",probe)
        self.assertIn("if ball and fight>=250 and fight<350 then hi['P1 Low Kick']:set_value(1) end",probe)
        self.assertNotIn(':write_u',probe)

    def test_original_morph_scripts_unchanged(self):
        from inventory_character_tables import source_tables
        src=PORT.parent/'baseline/mk2-rebuild-main/srcp'
        with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as archive:
            original=archive.read('mk2-rebuild-main/src/MKST.ASM').decode('cp437').replace('\r\n','\n')
        before=source_tables(original)
        after=source_tables((src/'MKST.ASM').read_text())
        names=[name for name in before if name.startswith('a_st_2_')]
        self.assertEqual(len(names),11)
        for name in names:
            values=lambda table:[(row['type'],row['values']) for row in table['rows']]
            self.assertEqual(values(before[name]),values(after[name]),name)

    def test_entry_only_grounding_source(self):
        from morph_source import MORPH_ROWS,MORPH_ENTRY_HELPERS
        text=(PORT.parent/'baseline/mk2-rebuild-main/srcp/MKST.ASM').read_text()
        self.assertIn(MORPH_ENTRY_HELPERS.strip(),text)
        self.assertIn('ani_calla,ks_morph_kano_pal',MORPH_ROWS)
        self.assertIn('ani_calla,ks_morph_sonya_pal',MORPH_ROWS)
        self.assertEqual(MORPH_ENTRY_HELPERS.count('callr morph_swpal'),2)
        self.assertNotIn('sleep',MORPH_ENTRY_HELPERS)
        self.assertNotIn('ochar)',MORPH_ENTRY_HELPERS)

    def test_compiled_headers_palettes_and_packed_pixels(self):
        src=PORT.parent/'baseline/mk2-rebuild-main/srcp'
        symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(src/'MK2P.MAP').read_text())}
        program=bytearray(1048576)
        for lane in range(2):program[lane::2]=b''.join((src/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
        report=json.loads((PORT/'generated_morph/MORPH_DATA.json').read_text())
        packed=(PORT/'generated_morph/fighter_ui_finish_morph_graphics.bin').read_bytes()
        self.assertEqual(sha(packed),report['packedSHA256'])
        for actor,colors in report['palettes'].items():
            at=(symbols[f'ks_{actor}_morph_palette']-0xff800000)//8
            self.assertEqual(list(struct.unpack_from('<66H',program,at)),[65]+colors+[0])
        for frame in report['frames']:
            header=struct.unpack_from('<HHhhIHI',program,(symbols[frame['imageLabel']]-0xff800000)//8)
            self.assertEqual(header,(frame['width'],frame['height'],frame['xOffset'],frame['yOffset'],
                (0xc00000+frame['packedByteOffset'])*8,0x6000,symbols[frame['paletteLabel']]))
            w,h,pixels=read_pgm(PORT/'assets/morph'/frame['file'])
            at=frame['packedByteOffset']
            self.assertEqual(unpack6(packed[at:at+frame['packedBytes']],w*h),pixels)

    def test_six_native_frames(self):
        data=json.loads((PORT/'assets/morph/MORPH_SOURCES.json').read_text())
        self.assertEqual(len(data['frames']),6)
        for actor,ground in (('kano',131),('sonya',132)):
            frames=[f for f in data['frames'] if f['actor']==actor]
            self.assertEqual(len(frames),3)
            self.assertEqual(len({f['sourceScale'] for f in frames}),1)
            self.assertEqual(len(data['palettes'][actor]),64)
            self.assertEqual(data['palettes'][actor][0],0)
            for f in frames:
                path=PORT/'assets/morph'/f['file']
                self.assertEqual(sha(path.read_bytes()),f['SHA256'])
                w,h,indices=read_pgm(path)
                self.assertEqual((w,h),(f['width'],f['height']))
                self.assertEqual(h-f['yOffset'],ground)
                self.assertTrue(all(0<=i<64 for i in indices))
                source=PORT/f['sourceAsset']
                self.assertEqual(sha(source.read_bytes()),f['sourceAssetSHA256'])
                self.assertEqual('v2' in source.name,f['phase']==0)
                with Image.open(source) as image:
                    self.assertEqual(sha(image.crop(f['cellRectangle']).tobytes()),f['sourceRGBA_SHA256'])

if __name__=='__main__':unittest.main()
