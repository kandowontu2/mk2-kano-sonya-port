"""Reject corrupted genuine native victim-table evidence; never simulate play."""
import argparse
import io
import json
import re
import unittest
from pathlib import Path
import verify_native_gore_victim_tables_v924 as proof


class NativeGoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {case: (proof.ROOT / case / 'run.log').read_text(encoding='utf-8-sig') for case in proof.CASES}

    def report(self, texts=None, guests=None):
        return proof.verify(self.texts if texts is None else texts, check_files=False, guests=guests)

    def reject(self, label, edit):
        texts = dict(self.texts)
        case = proof.CASES[0]
        texts[case] = edit(texts[case])
        self.assertNotEqual(texts[case], self.texts[case])
        report = self.report(texts)
        self.assertFalse(report['passed'])
        self.assertTrue(any(label in error for error in report['errors']), report['errors'])

    def test_baseline_proves_only_four_native_stability_cases(self):
        report = self.report()
        self.assertTrue(report['passed'], report['errors'])
        self.assertTrue(report['fiveNativeVictimTablesAcceptance'])
        self.assertEqual(len(report['cases']), 4)
        self.assertEqual(sum(case['snapshots'] for case in report['cases'].values()), 244)
        for flag in ('fullPortAcceptance', 'ownedInflationArtworkAcceptance', 'cageTorsoArtworkAcceptance',
                     'alternatePaletteRuntimeAcceptance', 'allStockFatalitiesAcceptance'):
            self.assertFalse(report[flag])

    def test_missing_physical_case(self):
        texts = dict(self.texts)
        texts.pop(proof.CASES[0])
        report = self.report(texts)
        self.assertFalse(report['passed'])
        self.assertIn('All four real-ID/physical-slot cases required', report['errors'])

    def test_proxy_identity(self):
        self.reject('true Kitana and victim', lambda text: text.replace('ids=4,17', 'ids=4,1', 1))

    def test_foreign_action_owner(self):
        self.reject('true Kitana and victim', lambda text: re.sub(r'(^MK2_STOCK_HEAD_V921_ACTION .*?actor=)[0-9A-F]+', r'\g<1>01000000', text, count=1, flags=re.M))

    def test_illegal_health_writer(self):
        self.reject('original physical health writers', lambda text: text.replace('pc=FF836700', 'pc=FF838860', 1))

    def test_missing_real_collision(self):
        self.reject('independently observed 322 damage', lambda text: re.sub(r'^MK2_STOCK_HEAD_V921_HEALTH .*pc=FF836700\n', '', text, count=1, flags=re.M))

    def test_missing_actual_action(self):
        self.reject('one original action', lambda text: re.sub(r'^MK2_STOCK_HEAD_V921_ACTION .*\n', '', text, flags=re.M))

    def test_missing_native_completion(self):
        self.reject('one original action', lambda text: re.sub(r'^MK2_STOCK_HEAD_V921_WRAP .*\n', '', text, flags=re.M))

    def test_wrong_native_completion_age(self):
        self.reject('exact native winner completion', lambda text: text.replace('age=276', 'age=277', 1))

    def test_body_cache_overrun(self):
        self.reject('no body-cache', lambda text: text + '\nMK2_STOCK_HEAD_V921_CACHE_OVERWRITE frame=3500 victim=kano side=1 killer=kitana writes=0 assistance=none at=01060220\n')

    def test_native_reset(self):
        self.reject('no native reset', lambda text: text + '\nMK2_STOCK_HEAD_V921_MODE frame=3500 victim=kano side=1 killer=kitana writes=0 assistance=none mode=0 states=65535,65535\n')

    def test_missing_physical_direction(self):
        self.reject('genuine Forward Forward', lambda text: re.sub(r'^MK2_STOCK_HEAD_V921_INPUT .*button=Down\n', '', text, flags=re.M))

    def test_missing_physical_hold(self):
        self.reject('actual continuous hold', lambda text: re.sub(r'^MK2_STOCK_HEAD_V921_INPUT .*button=Low_Kick\n', '', text, flags=re.M))

    def test_command_parser_mismatch(self):
        self.reject('native command parser', lambda text: re.sub(r'(COMPARE .*?wanted=)[78]', r'\g<1>6', text, count=1))

    def test_bad_timing_table_value(self):
        self.reject('exact own-ID timing', lambda text: text.replace('value=0040', 'value=6050', 1))

    def test_bad_position_table_value(self):
        self.reject('exact own-ID timing', lambda text: text.replace('value=FFB7', 'value=00C0', 1))

    def test_wrong_native_parameter_consumer(self):
        self.reject('exact own-ID timing', lambda text: text.replace('pc=FF82EE10', 'pc=FF83B850', 1))

    def test_wrong_native_gore_consumer(self):
        self.reject('genuine independent inflation', lambda text: text.replace('pc=FF83B850', 'pc=FF82EE10', 1))

    def test_missing_pointer_bus_half(self):
        self.reject('all three native pointer reads', lambda text: re.sub(r'^MK2_STOCK_HEAD_V921_GORE_ROW .*half=1 .*\n', '', text, count=1, flags=re.M))

    def test_invalid_pointer_high_half(self):
        self.reject('genuine independent inflation', lambda text: text.replace('half=1 value=FFFD', 'half=1 value=0000', 1))

    def test_gore_uses_wrong_physical_actor(self):
        self.reject('genuine independent inflation', lambda text: re.sub(r'(GORE_ROW .*?actor=)[0-9A-F]+', r'\g<1>01000000', text, count=1))

    def test_missing_continue_screen(self):
        self.reject('real terminal continue', lambda text: re.sub(r'^MK2_STOCK_HEAD_V921_MODE .*mode=3 .*\n', '', text, flags=re.M))

    def test_missing_snapshot_record(self):
        self.reject('full snapshot chronology', lambda text: re.sub(r'^MK2_STOCK_HEAD_V921_DISPLAY .*age=600\n', '', text, flags=re.M))

    def test_original_stock_table_mutation(self):
        guests = {case: (proof.ROOT / case / 'guest_maincpu.bin').read_bytes() for case in proof.CASES}
        guest = bytearray(guests[proof.CASES[0]])
        guest[proof.offset(0xff9ed0f0)] ^= 1
        guests[proof.CASES[0]] = bytes(guest)
        report = self.report(guests=guests)
        self.assertFalse(report['passed'])
        self.assertTrue(any('whole guest equals' in error for error in report['errors']))

    def test_private_palette_mutation(self):
        guests = {case: (proof.ROOT / case / 'guest_maincpu.bin').read_bytes() for case in proof.CASES}
        guest = bytearray(guests[proof.CASES[0]])
        guest[0xfae04] ^= 1
        guests[proof.CASES[0]] = bytes(guest)
        report = self.report(guests=guests)
        self.assertFalse(report['passed'])
        self.assertTrue(any('whole guest equals' in error for error in report['errors']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Preserve evidence')
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NativeGoreTests))
    args.output.mkdir(parents=True)
    (args.output / 'unit-tests.txt').write_text(log.getvalue())
    report = {'passed': result.wasSuccessful(), 'tests': result.testsRun,
              'failures': len(result.failures), 'errors': len(result.errors),
              'runtimeNotSimulated': True, 'artAndFullPortAcceptance': False}
    (args.output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))
    raise SystemExit(0 if result.wasSuccessful() else 1)
