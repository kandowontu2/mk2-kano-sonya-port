import unittest
from pathlib import Path
from verify_cpu_air_gate import ROOT, route, verify_dump, verify_case, verify_recovery_case, rows, ELIGIBLE, FALLBACK


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.words = [0xb500, 0x1f0, 0x0b40, 0xfff4, 0xca06,
                      0x0b40, 0xffee, 0xca03, 0xc080, 0xf050, 0xff9b,
                      0xc080, 0xef40, 0xff9b, 0xffff, 0xffff]

    def test_all_real_id_routes(self):
        for identity in range(19):
            with self.subTest(identity=identity):
                self.assertEqual(route(self.words, identity),
                                 (ELIGIBLE if identity in (11, 17) else FALLBACK, identity))

    def test_old_off_by_one_short_branch_rejected(self):
        for identity, index in ((11, 4), (17, 7)):
            words = self.words.copy()
            words[index] -= 1
            with self.assertRaises(ValueError):
                route(words, identity)

    def test_escaped_branch_rejected(self):
        self.words[7] = 0xca7f
        with self.assertRaises(ValueError):
            route(self.words, 17)

    def test_sonya_not_granted_kano_catch(self):
        self.assertEqual(route(self.words, 18), (FALLBACK, 18))

    def test_no_identity_substitution_instruction(self):
        self.words[:2] = [0x09c0, 11]
        with self.assertRaises(ValueError):
            route(self.words, 17)

    def test_unknown_instruction_rejected(self):
        self.words[0] = 0x0300
        with self.assertRaises(ValueError):
            route(self.words, 17)

    def test_duplicate_fields_rejected(self):
        with self.assertRaises(ValueError):
            rows('TAG pc=1234 pc=4321', 'TAG')

    def test_real_rejected_candidate_dump(self):
        log = (ROOT / 'audit_v387_cpu_air_kano_wait604/run.log').read_text(encoding='utf-8-sig')
        with self.assertRaisesRegex(ValueError, 'Unexpected executed router opcode'):
            verify_dump(log, (ROOT / 'mk2/mk2-maincpu.bin').read_bytes())

    def test_missing_rom_window_rejected(self):
        with self.assertRaises(ValueError):
            verify_dump('', b'')

    def test_both_current_compiled_native_dumps(self):
        for name in ('sonya_jump604', 'kano_wait604'):
            proof = verify_case(ROOT / ('audit_v389_cpu_air_' + name))
            self.assertTrue(proof['compiled_gate_passed'])
            self.assertFalse(proof['full_CPU_air_throw_acceptance'])
            self.assertEqual(proof['native_catch_entries'], 0)

    def test_both_current_full_close_recoveries(self):
        for player, boot in (('kano', 604), ('cage', 605)):
            proof = verify_recovery_case(ROOT / f'audit_v389_cpu_recovery_{player}_boot{boot}', player)
            self.assertTrue(proof['passed'])
            self.assertEqual(proof['held_fields'], 70 if player == 'kano' else 46)

    def current_log(self):
        return (ROOT / 'audit_v389_cpu_air_kano_wait604/run.log').read_text(encoding='utf-8-sig')

    def test_native_range_check_mutation_rejected(self):
        log = self.current_log().replace('0B43,FF9F', '0B43,FF8F', 1)
        with self.assertRaisesRegex(ValueError, 'Original eligibility'):
            verify_dump(log, (ROOT / 'mk2/mk2-maincpu.bin').read_bytes())

    def test_native_stack_unwind_mutation_rejected(self):
        log = self.current_log().replace('09AF,0001', '0300,0001', 1)
        with self.assertRaisesRegex(ValueError, 'Original eligibility'):
            verify_dump(log, (ROOT / 'mk2/mk2-maincpu.bin').read_bytes())

    def test_compiled_router_branch_mutation_rejected(self):
        log = self.current_log().replace('CA06', 'CA05', 1)
        with self.assertRaisesRegex(ValueError, 'Unexpected executed'):
            verify_dump(log, (ROOT / 'mk2/mk2-maincpu.bin').read_bytes())

    def test_proxy_compare_mutation_rejected(self):
        log = self.current_log().replace('0B40,FFEE,CA03', '0B40,FFED,CA03', 1)
        with self.assertRaisesRegex(ValueError, 'Wrong or aliased'):
            verify_dump(log, (ROOT / 'mk2/mk2-maincpu.bin').read_bytes())


if __name__ == '__main__':
    unittest.main()
