"""Corrupt saved genuine native evidence; never inject game state or inputs."""
import argparse
import copy
import io
import json
import re
import unittest
from unittest.mock import patch
from pathlib import Path
import verify_native_torso_art_v967 as proof

ROOT = proof.ROOT
CASES = tuple(f'audit_v963_cage_{name}_p{side}_owned_torso' for name in ('kano', 'sonya') for side in (1, 2))


class NativeTorsoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texts = {case: (ROOT / case / 'run.log').read_text(encoding='utf-8-sig') for case in CASES}
        # Actual FFT/pixel inspection is independently persisted by v966
        # and the full v967 baseline. Cache only that expensive unchanged
        # image analysis while corrupting text evidence, not native gameplay.
        cls.pictures = json.loads((ROOT / 'audit_v966_actual_presented_torso_pixels_checked/pixel-matches.json').read_text())['cases']

    def report(self, texts=None, pictures=None):
        images = self.pictures if pictures is None else pictures
        with patch.object(proof.pictures, 'check_case', side_effect=lambda case, *args: images[case]):
            return proof.verify(self.texts if texts is None else texts, check_files=False)

    def reject(self, label, edit):
        texts = dict(self.texts)
        texts[CASES[0]] = edit(texts[CASES[0]])
        self.assertNotEqual(texts[CASES[0]], self.texts[CASES[0]])
        report = self.report(texts)
        self.assertFalse(report['passed'])
        self.assertTrue(any(label in error for error in report['errors']), report['errors'])

    def test_true_normal_runtime_is_not_full_port_or_alt_acceptance(self):
        report = self.report()
        self.assertTrue(report['passed'], report['errors'])
        self.assertEqual(sum(r['sectionDMAs'] for r in report['cases'].values()), 8944)
        self.assertTrue(report['normalDeadPoolCageSectionNativeRuntimeAcceptance'])
        for flag in ('fullPortAcceptance', 'alternateCostumeAcceptance', 'allArenasAcceptance', 'unusedNativePose4RuntimeAcceptance'):
            self.assertFalse(report[flag])
        self.assertTrue(report['knownAlternateKanoBlueBlood'])

    def test_missing_physical_case(self):
        texts = dict(self.texts)
        texts.pop(CASES[0])
        report = self.report(texts)
        self.assertFalse(report['passed'])
        self.assertIn('Both true-ID victims in both physical slots', report['errors'])

    def test_proxy_identity(self):
        self.reject('actual Cage and added victim', lambda t: t.replace('ids=2,17', 'ids=2,1', 1))

    def test_illegal_health_writer(self):
        self.reject('original health writer', lambda t: t.replace('pc=FF836700', 'pc=FF838860', 1))

    def test_missing_collision(self):
        self.reject('two real KOs', lambda t: re.sub(r'^MK2_STOCK_HEAD_V921_HEALTH .*pc=FF836700\n', '', t, count=1, flags=re.M))

    def test_wrong_physical_button(self):
        self.reject('real Down Down Forward Forward LP', lambda t: t.replace('button=Low_Punch', 'button=High_Punch'))

    def test_missing_completion(self):
        self.reject('one complete native action', lambda t: re.sub(r'^MK2_STOCK_HEAD_V921_WRAP .*\n', '', t, flags=re.M))

    def test_wrong_completion_age(self):
        self.reject('unchanged original completion', lambda t: t.replace('age=185', 'age=186', 1))

    def test_cache_overrun(self):
        self.reject('no cache overrun', lambda t: t + '\nMK2_STOCK_HEAD_V921_CACHE_OVERWRITE frame=3500 victim=kano side=1 killer=cage writes=0 assistance=none at=01060220\n')

    def test_native_reset(self):
        self.reject('no cache overrun', lambda t: t + '\nMK2_STOCK_HEAD_V921_MODE frame=3500 victim=kano side=1 killer=cage writes=0 assistance=none mode=0 states=0,0\n')

    def test_no_continue_screen(self):
        self.reject('real continue screen', lambda t: t.replace('mode=3 states=', 'mode=6 states='))

    def test_proxy_owned_art_actor(self):
        self.reject('genuine section owner and ID', lambda t: re.sub(r'(^MK2_CAGE_TORSO_V963_QUEUE .*source=0F9.*? id=)17', r'\g<1>1', t, count=1, flags=re.M))

    def test_foreign_art_owner(self):
        self.reject('genuine section owner and ID', lambda t: re.sub(r'(^MK2_CAGE_TORSO_V963_QUEUE .*source=0F9.*? owner=)[0-9A-F]+', r'\g<1>01000000', t, count=1, flags=re.M))

    def test_aliased_stump_is_not_separate_actor(self):
        self.reject('separate native stump', lambda t: re.sub(r'(^MK2_CAGE_TORSO_V963_QUEUE .*source=0F929C40 actor=)[0-9A-F]+', r'\g<1>01034E90', t, count=1, flags=re.M))

    def test_missing_owned_dma(self):
        self.reject('actual section DMA', lambda t: re.sub(r'^MK2_CAGE_TORSO_V963_DMA .*source=0F9.*\n', '', t, count=1, flags=re.M))

    def test_floating_stump(self):
        self.reject('native raster floor', lambda t: re.sub(r'(^MK2_CAGE_TORSO_V963_DMA .*source=0F929C40 .*? y=)135', r'\g<1>134', t, count=1, flags=re.M))

    def test_wrong_palette_bank(self):
        self.reject('native geometry/command/palette bank', lambda t: re.sub(r'(^MK2_CAGE_TORSO_V963_DMA .*source=0F9.*? palette=)0200', r'\g<1>0300', t, count=1, flags=re.M))

    def test_bad_dimensions(self):
        self.reject('native geometry/command/palette bank', lambda t: re.sub(r'(^MK2_CAGE_TORSO_V963_DMA .*source=0F9.*? width=)\d+', r'\g<1>999', t, count=1, flags=re.M))

    def test_bad_fifo_binding(self):
        self.reject('exact current-field FIFO', lambda t: re.sub(r'(^MK2_CAGE_TORSO_V963_DMA .*source=0F9.*? queue_match=)1', r'\g<1>0', t, count=1, flags=re.M))

    def test_prior_page_snapshot(self):
        self.reject('next-field section pictures', lambda t: re.sub(r'(^MK2_CAGE_TORSO_V963_POSE_SNAPSHOT frame=3161 .*queued_frame=)3160', r'\g<1>3161', t, count=1, flags=re.M))

    def test_missing_palette_dump(self):
        self.reject('hardware palette evidence', lambda t: re.sub(r'^MK2_CAGE_TORSO_V963_PALETTE_DUMP .*\n', '', t, count=1, flags=re.M))

    def test_actual_prior_pose_pixels_rejected(self):
        images = copy.deepcopy(self.pictures)
        images[CASES[0]][0]['score'] = 0.0167
        report = self.report(pictures=images)
        self.assertFalse(report['passed'])
        self.assertTrue(any('presented PNG matches actual encoded' in r for r in report['errors']))

    def test_whole_guest_descriptor_corruption(self):
        original = proof.expected_guest
        def changed(payload):
            data = bytearray(original(payload))
            data[proof.assets.ROM_DESCRIPTORS] ^= 1
            return bytes(data)
        with patch.object(proof, 'expected_guest', side_effect=changed):
            report = self.report()
        self.assertFalse(report['passed'])
        self.assertTrue(any('whole guest only private' in r for r in report['errors']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Preserve unit evidence')
    log = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(NativeTorsoTests)
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    args.output.mkdir()
    (args.output / 'unit-tests.log').write_text(log.getvalue())
    report = dict(passed=result.wasSuccessful(), testsRun=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                  fullPortAcceptance=False, alternateCostumeAcceptance=False)
    (args.output / 'unit-results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))
    if not result.wasSuccessful():
        print(log.getvalue())
    raise SystemExit(0 if result.wasSuccessful() else 1)
