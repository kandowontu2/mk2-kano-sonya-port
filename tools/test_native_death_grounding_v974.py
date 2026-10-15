"""Corrupt real native death-art evidence; no simulated game acceptance."""
import argparse
import io
import json
import re
import unittest
from pathlib import Path
import verify_native_death_grounding_v971 as proof


class NativeDeathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {case: (proof.ROOT / case / 'run.log').read_text(encoding='utf-8-sig') for case in proof.CASES}

    def report(self, texts=None):
        return proof.verify(self.texts if texts is None else texts, check_files=False)

    def reject(self, label, edit):
        texts = dict(self.texts)
        case = proof.CASES[0]
        texts[case] = edit(texts[case])
        self.assertNotEqual(texts[case], self.texts[case])
        report = self.report(texts)
        self.assertFalse(report['passed'])
        self.assertTrue(any(label in message for message in report['errors']), report['errors'])

    def test_baseline_is_four_native_cases_not_whole_port(self):
        report = self.report()
        self.assertTrue(report['passed'], report['errors'])
        self.assertTrue(report['ownedHeadAndHeadlessBodyNativeRuntimeAcceptance'])
        self.assertTrue(report['reptileVictimDeadPoolGroundingAcceptance'])
        self.assertFalse(report['fullPortAcceptance'])
        self.assertFalse(report['fullNativeDeathArtAcceptance'])
        self.assertFalse(report['alternatePaletteRuntimeAcceptance'])
        self.assertFalse(report['allFinisherAllArenaGroundingAcceptance'])
        self.assertEqual(sum(case['nativeArtDMAs'] for case in report['cases'].values()), 2054)

    def test_proxy_identity(self):
        self.reject('actual Reptile and true victim', lambda t: t.replace('ids=9,17', 'ids=9,1', 1))

    def test_illegal_health_writer(self):
        self.reject('original physical health writers', lambda t: t.replace('pc=FF836700', 'pc=FF838860', 1))

    def test_missing_action(self):
        self.reject('one complete original fatality', lambda t: re.sub(r'^MK2_REPTILE_V879_ACTION .*\n', '', t, flags=re.M))

    def test_missing_wrap(self):
        self.reject('one complete original fatality', lambda t: re.sub(r'^MK2_REPTILE_V879_WRAP .*\n', '', t, flags=re.M))

    def test_unearned_damage(self):
        self.reject('observed 322 damage', lambda t: re.sub(r'^MK2_REPTILE_V879_HEALTH .*before=161 after=121 pc=FF836700\n', '', t, count=1, flags=re.M))

    def test_missing_actual_command(self):
        self.reject('real Back Back Down LP', lambda t: re.sub(r'^MK2_REPTILE_V879_INPUT .*button=Low_Punch\n', '', t, flags=re.M))

    def test_wrong_row_offset(self):
        self.reject('exact original four-field', lambda t: t.replace('data=FFFD mask=FFFF pc=FF8C8AB0', 'data=0000 mask=FFFF pc=FF8C8AB0', 1))

    def test_wrong_row_consumer(self):
        self.reject('exact original four-field', lambda t: t.replace('pc=FF8C8AB0', 'pc=FFA59F10', 1))

    def test_wrong_palette(self):
        self.reject('real independent normal palette', lambda t: t.replace('pointer=FFFED000', 'pointer=FFADD0D0', 1))

    def test_wrong_head(self):
        self.reject('own native head descriptor', lambda t: t.replace('descriptor=FFFD5460', 'descriptor=FFB4A4B0', 1))

    def test_body_floor_mismatch(self):
        self.reject('headless physical actor retains its own native floor', lambda t: t.replace('y=82 floor=82', 'y=85 floor=82', 1))

    def test_body_has_foreign_owner(self):
        self.reject('physical true-ID art owner', lambda t: re.sub(r'(^MK2_DEATH_ART_V897_QUEUE .*?owner=)[0-9A-F]+', r'\g<1>01000000', t, count=1, flags=re.M))

    def test_missing_collapse_pose(self):
        self.reject('all seven body poses', lambda t: re.sub(r'^MK2_DEATH_ART_V897_QUEUE .*pose=FF013A20 .*\n', '', t, flags=re.M))

    def test_no_original_fifo_binding(self):
        self.reject('actual DMA bound to original native FIFO', lambda t: t.replace('queue_match=1', 'queue_match=0', 1))

    def test_wrong_native_dimensions(self):
        self.reject('actual native dimensions', lambda t: re.sub(r'(^MK2_DEATH_ART_V897_DMA .*?width=)47', r'\g<1>48', t, count=1, flags=re.M))

    def test_wrong_raster_ground(self):
        def edit(text):
            return re.sub(r'(^MK2_DEATH_ART_V897_DMA .*? y=)(\d+)', lambda m: m[1] + str(int(m[2]) + 1), text, count=1, flags=re.M)
        self.reject('every collapse pose contacts the native raster ground row', edit)

    def test_native_art_cannot_linger(self):
        self.reject('native art retires well before terminal', lambda t: re.sub(r'(^MK2_DEATH_ART_V897_RESULT .*?last=)\d+', r'\g<1>5197', t, count=1, flags=re.M))

    def test_wrong_native_camera(self):
        self.reject('every collapse pose contacts the native raster ground row', lambda t: re.sub(r'(^MK2_DEATH_ART_V897_QUEUE .*?displayY=)(-?\d+)', lambda m: m[1] + str(int(m[2]) + 1), t, count=1, flags=re.M))

    def test_wrong_stage_floor(self):
        self.reject('original stage-relative owned floor anchor', lambda t: re.sub(r'(^MK2_DEATH_ART_V897_QUEUE .*?stageY=)(-?\d+)', lambda m: m[1] + str(int(m[2]) + 1), t, count=1, flags=re.M))

    def test_missing_same_frame_queue(self):
        self.reject('exact current-frame ground projection queue', lambda t: re.sub(r'(^MK2_DEATH_ART_V897_QUEUE frame=)\d+', r'\g<1>1', t, count=1, flags=re.M))

    def test_wrong_native_wrap_age(self):
        self.reject('native completion 90 fields', lambda t: t.replace('age=187 pc=FF8C9690', 'age=188 pc=FF8C9690', 1))

    def test_cache_overrun_cannot_be_waived(self):
        self.reject('no body-cache overrun', lambda t: t + '\nMK2_REPTILE_V879_CACHE_OVERWRITE frame=3265 victim=kano side=1 writes=0 assistance=none at=01060130 data=7E7F mask=FFFF\n')

    def test_boot_picture_is_not_finisher(self):
        self.reject('actual full finisher snapshot chronology', lambda t: t.replace('DISPLAY frame=3135', 'DISPLAY frame=1', 1))

    def test_both_slots_required(self):
        texts = dict(self.texts)
        del texts[proof.CASES[1]]
        report = self.report(texts)
        self.assertFalse(report['passed'])
        self.assertIn('Both true victims in both physical slots', report['errors'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Preserve unit-test evidence')
    args.output.mkdir()
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NativeDeathTests))
    (args.output / 'run.log').write_text(stream.getvalue())
    report = {'passed': result.wasSuccessful(), 'methods': result.testsRun,
              'failures': len(result.failures), 'errors': len(result.errors),
              'scope': 'four native Reptile victim art/grounding cases; not full-port acceptance'}
    (args.output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))
    raise SystemExit(0 if result.wasSuccessful() else 1)
