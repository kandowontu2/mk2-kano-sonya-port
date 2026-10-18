import struct
import unittest
from qualify_all_roster_roots import pointers,read_long

class AllRootChecks(unittest.TestCase):
    def test_exact_table_length_and_missing_rejected(self):
        source='table\n    .long own_a ; main 00\n    .long own_b ; main 01\nnext\n'
        self.assertEqual(pointers(source,'table',2),['own_a','own_b'])
        with self.assertRaises(AssertionError):pointers(source,'table',3)
        with self.assertRaises(AssertionError):pointers(source.replace('own_b','ks_missing_main_01'),'table',2)
        with self.assertRaises(AssertionError):pointers(source.replace('own_b','own_b+32'),'table',2)

    def test_bit_address_bounds_prevent_negative_or_short_reads(self):
        program=struct.pack('<II',123,456)
        self.assertEqual(read_long(program,0xff800000),123)
        self.assertEqual(read_long(program,0xff800020),456)
        for address in (0xff7ffff8,0xff800001,0xff800040,0x100000000):
            with self.assertRaises(AssertionError):read_long(program,address)
