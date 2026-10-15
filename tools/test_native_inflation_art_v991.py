"""Reject corrupted genuine native victim-table evidence; never simulate play."""
import argparse
import io
import json
import re
import unittest
from pathlib import Path
import verify_native_inflation_art_v989 as proof


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

    def test_baseline_proves_owned_six_pose_runtime_but_not_full_port(self):
        report = self.report()
        self.assertTrue(report['passed'], report['errors'])
        self.assertTrue(report['fiveNativeVictimTablesAcceptance'])
        self.assertEqual(len(report['cases']), 4)
        self.assertEqual(sum(case['snapshots'] for case in report['cases'].values()), 244)
        self.assertTrue(report['ownedSixPoseInflationNativeRuntimeAcceptance'])
        self.assertEqual(sum(case['nativeOwnedDMAs'] for case in report['cases'].values()), 700)
        self.assertEqual(sum(case['poseSnapshots'] for case in report['cases'].values()), 24)
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

    def test_missing_sixth_pose(self):
        self.reject('all six genuine', lambda t: re.sub(r'^MK2_INFLATION_ART_V938_QUEUE .*source=0F783480 .*\n', '', t, flags=re.M))

    def test_stock_liu_graphics_substitute(self):
        self.reject('victim own art', lambda t: re.sub(r'(MK2_INFLATION_ART_V938_QUEUE .*?source=)0F700000', r'\g<1>043A1000', t, count=1))

    def test_proxy_body(self):
        self.reject('physical body/owner/ID', lambda t: re.sub(r'(MK2_INFLATION_ART_V938_QUEUE .*?id=)17', r'\g<1>1', t, count=1))

    def test_foreign_body_owner(self):
        self.reject('physical body/owner/ID', lambda t: re.sub(r'(MK2_INFLATION_ART_V938_QUEUE .*?owner=)[0-9A-F]+', r'\g<1>01000000', t, count=1))

    def test_bad_actual_dimensions(self):
        self.reject('native dimensions', lambda t: re.sub(r'(MK2_INFLATION_ART_V938_DMA .*?width=)134', r'\g<1>135', t, count=1))

    def test_floating_inflation_feet(self):
        self.reject('native raster floor', lambda t: re.sub(r'(MK2_INFLATION_ART_V938_DMA .*? y=)355', r'\g<1>354', t, count=1))

    def test_wrong_body_floor(self):
        self.reject('own floor stays fixed', lambda t: re.sub(r'(MK2_INFLATION_ART_V938_QUEUE .*?floor=)82', r'\g<1>81', t, count=1))

    def test_wrong_actual_palette_bank(self):
        self.reject('actual palette bank', lambda t: re.sub(r'(MK2_INFLATION_ART_V938_DMA .*?palette=)0400', r'\g<1>0500', t, count=1))

    def test_missing_exact_native_fifo(self):
        self.reject('actual DMA bound', lambda t: t.replace('queue_match=1', 'queue_match=0', 1))

    def test_missing_burst_picture(self):
        self.reject('all six displayed', lambda t: re.sub(r'^MK2_INFLATION_ART_V938_POSE_SNAPSHOT .*source=0F783480 .*\n', '', t, flags=re.M))

    def test_prior_backpage_picture(self):
        self.reject('native next-field', lambda t: t.replace('queued_frame=3299', 'queued_frame=3300', 1))

    def test_missing_native_color_evidence(self):
        self.reject('hardware palette evidence', lambda t: re.sub(r'^MK2_INFLATION_ART_V938_PALETTE_DUMP .*\n', '', t, count=1, flags=re.M))

    def test_unretired_victim_art(self):
        self.reject('actor/art retirement', lambda t: t.replace('last=3473', 'last=5100', 1))

    def test_corrupt_owned_descriptor(self):
        guests = {case: (proof.ROOT / case / 'guest_maincpu.bin').read_bytes() for case in proof.CASES}
        g = bytearray(guests[proof.CASES[0]])
        g[proof.assets.ROM_DESCRIPTORS] ^= 1
        guests[proof.CASES[0]] = bytes(g)
        report = self.report(guests=guests)
        self.assertFalse(report['passed'])
        self.assertTrue(any('whole guest equals' in e for e in report['errors']))


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
