import struct
import unittest
from pathlib import Path
from verify_native_pit_assets_v597 import verify

ROOT = Path(__file__).resolve().parents[1]


class PitAssets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = (ROOT/'diagnostic_v597_native_pit_fall/roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.source = (ROOT/'diagnostic_v545_native_roll_edge_clearance/roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.stock = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()

    def reject_word(self, at, value):
        corrupt = bytearray(self.payload)
        struct.pack_into('<I', corrupt, at, value)
        with self.assertRaises(ValueError):
            verify(corrupt, self.source, self.stock)

    def test_actual(self):
        self.assertTrue(verify(self.payload, self.source, self.stock)['passed'])

    def test_kano_missing_entry(self): self.reject_word(0x130100+17*4, 1)
    def test_sonya_kung_lao_proxy(self): self.reject_word(0x130100+18*4, 0xFF85E830)
    def test_sonya_kano_proxy(self): self.reject_word(0x130100+18*4, 0xFF181000)
    def test_stock_row(self): self.reject_word(0x130100+1*4, 0xFF181000)
    def test_kano_phase(self): self.reject_word(0x130200+8, 0xFF182300)
    def test_sonya_phase(self): self.reject_word(0x130240+8, 0xFF182000)
    def test_wrong_loop_target(self): self.reject_word(0x130200+24, 0xFF181200)
    def test_lost_loop_token(self): self.reject_word(0x130240+20, 0)
    def test_missing_phase_separator(self): self.reject_word(0x130200+28, 1)
    def test_missing_final_separator(self): self.reject_word(0x130240+36, 1)
    def test_unbounded_component(self): self.reject_word(0x130404, 0xFF184000)
    def test_component_proxy(self): self.reject_word(0x130430, 0xFF184000)
    def test_wrong_graphics(self): self.reject_word(0x130808, 0x10000000)
    def test_wrong_extent(self): self.reject_word(0x130800, 0x20002000)
    def test_unrelated_payload(self): self.reject_word(0x100000, 0)
    def test_empty_body(self):
        corrupt = bytearray(self.payload);corrupt[0x134000:0x153564] = bytes(0x1F564)
        with self.assertRaises(ValueError): verify(corrupt, self.source, self.stock)


if __name__ == '__main__': unittest.main(verbosity=2)
