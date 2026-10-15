"""Baseline and deliberate corruption tests for the v787 fade verifier."""
import copy
from pathlib import Path
import struct
import unittest
import verify_native_fade_exclusions_v787 as verify

ROOT = Path(__file__).resolve().parents[1]

class FadeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = (ROOT / 'audit_v784_kano_visual_p1/guest_maincpu.bin').read_bytes()
        cls.new = (ROOT / 'audit_v786_kano_visual_p1/guest_maincpu.bin').read_bytes()
        cls.original = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
        cls.rows = verify.parse(ROOT / 'audit_v786_kano_visual_p1/run.log')

    def reject_guest(self, data):
        with self.assertRaises(ValueError):
            verify.guest_check(self.old, data, self.original)

    def reject_rows(self, rows):
        with self.assertRaises(ValueError):
            verify.palette_check(rows, self.new, (17, 18))

    def test_actual_guest_baseline(self):
        self.assertEqual(verify.guest_check(self.old, self.new, self.original)['changed_bytes'], 169)

    def test_actual_palette_baseline(self):
        self.assertEqual(verify.palette_check(self.rows, self.new, (17, 18))['fighter_fields'], 482)

    def test_each_binding_must_route_extended_list(self):
        for address in verify.OPERANDS:
            with self.subTest(address=f'{address:08X}'):
                data = bytearray(self.new)
                struct.pack_into('<I', data, verify.off(address), 0xff908120)
                self.reject_guest(data)

    def test_each_normal_alternate_frozen_record_required(self):
        for index in range(6):
            with self.subTest(index=index):
                data = bytearray(self.new)
                struct.pack_into('<I', data, 0xfa700 + (46 + index) * 4, 0)
                self.reject_guest(data)

    def test_original_list_order_unchanged(self):
        data = bytearray(self.new)
        data[0xfa700:0xfa704], data[0xfa704:0xfa708] = data[0xfa704:0xfa708], data[0xfa700:0xfa704]
        self.reject_guest(data)

    def test_native_terminator_required(self):
        data = bytearray(self.new)
        struct.pack_into('<I', data, 0xfa700 + 52 * 4, 0x01000000)
        self.reject_guest(data)

    def test_unused_reserved_padding_unchanged(self):
        data = bytearray(self.new); data[0xfa7ff] = 0
        self.reject_guest(data)

    def test_native_fader_unchanged(self):
        data = bytearray(self.new); data[verify.off(0xff80fbc0)] ^= 1
        self.reject_guest(data)

    def test_native_colour_converter_unchanged(self):
        data = bytearray(self.new); data[verify.off(0xff8100b0)] ^= 1
        self.reject_guest(data)

    def test_source_palette_unchanged(self):
        data = bytearray(self.new); data[0xfda04] ^= 1
        self.reject_guest(data)

    def test_dimming_any_single_body_field_rejected(self):
        rows = copy.deepcopy(self.rows)
        row = next(r for kind, r in rows if kind == 'VISUAL' and r['age'] == '100' and r['slot'] == '2')
        words = row['colors'].split(','); words[1] = '0000'; row['colors'] = ','.join(words)
        self.reject_rows(rows)

    def test_missing_per_field_palette_rejected(self):
        rows = [(kind, r) for kind, r in self.rows if not(kind == 'VISUAL' and r['age'] == '100' and r['slot'] == '1')]
        self.reject_rows(rows)

    def test_duplicate_per_field_palette_rejected(self):
        rows = copy.deepcopy(self.rows)
        rows.append(next((kind, r) for kind, r in rows if kind == 'VISUAL' and r['age'] == '100'))
        self.reject_rows(rows)

    def test_proxy_identity_rejected(self):
        rows = copy.deepcopy(self.rows)
        next(r for kind, r in rows if kind == 'VISUAL' and r['age'] == '100')['id'] = '1'
        self.reject_rows(rows)

    def test_body_bank_still_faded_rejected(self):
        rows = copy.deepcopy(self.rows)
        next(r for kind, r in rows if kind == 'FADE')['bank'] = '0200'
        self.reject_rows(rows)

    def test_disabled_scenery_fade_rejected(self):
        self.reject_rows([(kind, r) for kind, r in self.rows if kind != 'FADE'])

    def test_wrong_fade_factor_rejected(self):
        rows = copy.deepcopy(self.rows)
        next(r for kind, r in rows if kind == 'FADE')['factor'] = '128'
        self.reject_rows(rows)

    def test_wrong_fade_age_rejected(self):
        rows = copy.deepcopy(self.rows)
        next(r for kind, r in rows if kind == 'FADE')['age'] = '1'
        self.reject_rows(rows)

if __name__ == '__main__':
    unittest.main(verbosity=2)
