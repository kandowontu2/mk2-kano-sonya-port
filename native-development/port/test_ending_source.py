import unittest
import zipfile
from ending_source import winner,story,cast
from prepare_game_candidate import ZIP

class Endings(unittest.TestCase):
    def test_cast_preserves_original_pairs(self):
        with zipfile.ZipFile(ZIP) as archive:
            raw=archive.read('mk2-rebuild-main/src/MKEND.ASM').decode('cp437').replace('\r\n','\n')
        result=cast(raw)
        def table(text):return text.split('\ncast_table\n',1)[1].split('\npf_left_bow\n',1)[0]
        original=table(raw).split('\t.word\t0\n',1)[0]
        self.assertTrue(table(result).startswith(original))
        self.assertIn('.word 17,070H\n\t.word 18,0120H',table(result))
        self.assertEqual(table(result).count('\t.word\t0\n'),1)
        self.assertEqual(raw.split('\npf_left_bow\n',1)[1],result.split('\npf_left_bow\n',1)[1])
        self.assertIn('KERRI HOSKINS\\nAS\\nSONYA',result)
        self.assertIn('RICHARD DIVIZIO\\nAS\\nKANO',result)
        with self.assertRaises(AssertionError):cast(result)

    def test_original_tables_preserved(self):
        with zipfile.ZipFile(ZIP) as archive:
            for name,transform,tables in (
                ('MKEND.ASM',winner,('end_winner_text',)),
                ('UNZIP.ASM',story,('end_text_1','end_text_2'))):
                raw=archive.read('mk2-rebuild-main/src/'+name).decode('cp437').replace('\r\n','\n')
                result=transform(raw)
                for table in tables:
                    original=raw.split('\n'+table+'\n',1)[1]
                    changed=result.split('\n'+table+'\n',1)[1]
                    self.assertEqual(original,changed)
                self.assertIn('cmpi 17,a0',result)
                self.assertIn('cmpi 18,a0',result)
                if name=='UNZIP.ASM':
                    routine=result.split('\nks_story_show\n',1)[1].split('\nks_story_kano\n',1)[0]
                    self.assertIn('jsrp lm_printf',routine)
                    self.assertNotIn('jsrp printf\n',routine)
                    self.assertIn('calla gso_dmawnz_ns',routine)
                    self.assertIn('calla insobj2a8',routine)
                    self.assertEqual(routine.count('calla murder_myoinit_score'),2)
                    self.assertIn('pushp a8\n\tcalla murder_myoinit_score\n\tcalla clr_scrn',routine)
                    self.assertIn('movi dlists_bogus,a0\n\tmove a0,@dlists,l',routine)
                    self.assertIn('calla page_0_setup_no_init\n\tpullp a11',routine)
                    self.assertIn('sleep 4\n\tcalla display_off\n\tcalla sync_wait_dma_q\n\tcalla grab_screen\n\tcalla display_on\n\tsleep 040H*12',routine)
                    self.assertIn('jrne ks_story_page\n\tcalla murder_myoinit_score\n\tcalla clr_scrn\n\tretp',routine)
                    self.assertIn('sleep 040H*12',routine)
                    self.assertEqual(routine.count('pushp '),routine.count('pullp '))
                    for actor in ('kano','sonya'):
                        self.assertIn(f'.long ks_end_{actor}_picture1,0029001eH,ks_story_{actor}_text1',result)
                        self.assertIn(f'.long ks_end_{actor}_picture2,0019003cH,ks_story_{actor}_text2',result)
                with self.assertRaises(AssertionError):transform(result)

if __name__=='__main__':unittest.main()
