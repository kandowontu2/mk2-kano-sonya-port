import unittest
from qualify_movelist_commands import expected_row, table_rows, qualify


class MovelistCommandTests(unittest.TestCase):
    def test_history_reverses_time_and_mirrors_facing(self):
        self.assertEqual(expected_row('B D F', True), ['sw_right', 'sw_down', 'sw_left', '0', '0', '0'])
        self.assertEqual(expected_row('B D F', False), ['sw_left', 'sw_down', 'sw_right', '0', '0', '0'])

    def test_parser_stops_at_next_label(self):
        source = '\nfirst\n .word 038h\n .word sw_down,0\nsecond\n .word 999\n'
        self.assertEqual(table_rows(source, 'first'), [['038h'], ['sw_down', '0']])

    def test_current_document_matches_both_native_facing_tables(self):
        result = qualify()
        self.assertEqual(len(result['cases']), 14)
        self.assertTrue(result['trueIdentityMorphSourceDispatchVerified'])
        self.assertTrue(result['nativeNoPunchSourceGatesVerified'])
        self.assertFalse(result['fullPortVerified'])


if __name__ == '__main__':
    unittest.main()
