"""GSPA lexical regression, not an indexed-access safety proof."""
import unittest
from inventory_character_tables import instruction_code,source_tables,HELPERS
from pathlib import Path

class ScannerTests(unittest.TestCase):
    def test_indirect_character_wrappers_are_inventory_targets(self):
        self.assertIn('adjust_him_tbl',HELPERS)
        self.assertIn('ochar_do_or_rets',HELPERS)
        src=Path(__file__).parent.parent/'baseline/mk2-rebuild-main/srcp'
        utility=(src/'MKUTIL.ASM').read_text()
        adjustment=utility.split('\nadjust_him_tbl\n',1)[1].split('\nadjust_him_a0\n',1)[0]
        self.assertIn('get_his_char_long',adjustment)
        drone=(src/'MKDRONE.ASM').read_text()
        wrapper=drone.split('\nochar_do_or_rets\n',1)[1].split('\nodor9',1)[0]
        self.assertIn('get_char_long',wrapper)

    def test_inline_label_instruction(self):
        self.assertEqual(instruction_code('def2\tmovi\tochar_fatality_distances,a0'),
                         'movi\tochar_fatality_distances,a0')
        self.assertEqual(instruction_code('RST0: MOVI rs_calls,A0 ; comment'),
                         'movi rs_calls,a0')
        self.assertEqual(instruction_code('branch\tcalla get_char_word'),
                         'calla get_char_word')

    def test_indented_instruction_and_operand_preserved(self):
        self.assertEqual(instruction_code('\tMOVI ft_kang,a0'), 'movi ft_kang,a0')
        self.assertEqual(instruction_code('    calla get_char_long'), 'calla get_char_long')

    def test_non_instructions(self):
        for row in ('label_only', '* comment', '\t* comment', '; comment', '\x1a', ''):
            self.assertEqual(instruction_code(row), '')

    def test_inline_table_not_instruction(self):
        text='speeds\t.word 4,4\n\t.word 2\nentry\tmovi speeds,a0\n\tcalla get_char_word\n'
        tables=source_tables(text)
        self.assertEqual(tables['speeds']['rows'][0]['values'],['4','4'])
        self.assertNotIn('entry',tables)

if __name__=='__main__': unittest.main()
