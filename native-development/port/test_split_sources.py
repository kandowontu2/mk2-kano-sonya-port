import json
from pathlib import Path
import unittest
from build_arm_rip_assets import read_pgm, sha

PORT=Path(__file__).resolve().parent
SOURCE=PORT/'assets/split_v2'


class SplitSourceTests(unittest.TestCase):
    def setUp(self):
        self.report=json.loads((SOURCE/'SPLIT_SOURCES.json').read_text())

    def test_all_34_editable_components(self):
        self.assertEqual(len(self.report['frames']),34)
        for frame in self.report['frames']:
            path=SOURCE/frame['file']
            self.assertEqual(sha(path.read_bytes()),frame['SHA256'])
            w,h,pixels=read_pgm(path)
            self.assertEqual((w,h),(frame['width'],frame['height']))
            self.assertTrue(any(pixels))

    def test_common_body_scale_and_ground_origin(self):
        for actor,ground in (('kano',131),('sonya',132)):
            frames=[f for f in self.report['frames'] if f['actor']==actor]
            self.assertEqual(len(frames),17)
            self.assertEqual(len({f['sourceScale'] for f in frames}),1)
            first=next(f for f in frames if f['phase']==0)
            self.assertEqual(first['height']-first['yOffset'],ground)
            for f in frames:
                reference=f['referenceGeometryOnly']['unionBounds']
                self.assertEqual(f['height']-f['yOffset'],reference[3]+f['nativeGroundAdaptation'])

    def test_secondary_canonical_orientation_and_matched_lengths(self):
        self.assertEqual(sum(f['nativeSecondaryPixelsReflected'] for f in self.report['frames']),14)
        for actor in ('kano','sonya'):
            for role in ('viewer_left','viewer_right'):
                frames=[f for f in self.report['frames'] if f['actor']==actor and f['role']==role]
                self.assertEqual([f['phase'] for f in frames],list(range(3,10)))
                for f in frames:
                    self.assertEqual(f['xOffset'],f['width']-f['referenceGeometryOnly']['unionBounds'][2])
                    self.assertEqual(f['nativeSecondaryPixelsReflected'],role=='viewer_right')

    def test_only_kano_half_frames_can_change(self):
        previous=json.loads((PORT/'assets/split/SPLIT_SOURCES.json').read_text())
        self.assertEqual(self.report['unchangedOtherFrames'],20)
        preserved=0
        for frame in self.report['frames']:
            old=next(f for f in previous['frames'] if f['file']==frame['file'])
            if frame['actor']!='kano' or frame['role']=='whole':
                self.assertEqual(frame['SHA256'],old['SHA256'])
                preserved+=1
        self.assertEqual(preserved,20)


if __name__=='__main__':unittest.main()
