import hashlib
import json
from pathlib import Path
import unittest
from PIL import Image
import numpy as np
from leg_ground_source import OWN_LEG_EXTENT,SPAWN,SHATTER,PALETTE,HELPER,integrate

class DetachedLegGroundingTests(unittest.TestCase):
    def test_only_four_explicit_consumers_and_true_own_ids(self):
        source=(SPAWN+'\n')*3+SHATTER+'\n'+PALETTE
        changed=integrate(source)
        self.assertEqual(changed.count('callr ks_ground_own_legs\n'),4)
        self.assertIn(HELPER,changed)
        self.assertIn('cmpi 17,a0',HELPER)
        self.assertIn('cmpi 18,a0\n\tjrne ks_ground_own_legs_done',HELPER)
        self.assertTrue(HELPER.rstrip().endswith('pull a0\n\trets'))
        with self.assertRaises(AssertionError):integrate(changed)
        with self.assertRaises(AssertionError):integrate(source.replace(SPAWN,'',1))

    def test_extent_matches_opaque_source_pixels_and_signed_pivot(self):
        port=Path(__file__).resolve().parent
        records=json.loads((port/'generated_torso/TORSO_DATA.json').read_text())['records']
        for actor in ('kano','sonya'):
            record=records[actor][6]
            path=port/'assets/torso'/record['file']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest().upper(),record['fileSHA256'])
            with Image.open(path) as image:pixels=np.asarray(image)
            last=int(np.nonzero(pixels)[0].max())
            self.assertEqual(last+1-record['yOffset'],OWN_LEG_EXTENT)
            for ground in (180,220,240):
                self.assertEqual(ground-OWN_LEG_EXTENT+last+1-record['yOffset'],ground)
