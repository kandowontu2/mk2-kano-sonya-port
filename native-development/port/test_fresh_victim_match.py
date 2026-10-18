import unittest
from fresh_victim_match import verify

def sample():
    rows=[dict(frame=str(frame),mode='2',death='0',winner='0',missing='0',p1char='2',p2char='17',
               p1hp='161',p2hp='161' if frame==100 else '137') for frame in range(100,700)]
    palettes=[dict(frame=str(frame),p1source='ff800100',initialP1source='ff800100',p2source='ff800200',initialP2source='ff800200',
                   p1rgbMismatch='0',p2rgbMismatch='0',p1colors='64',p2colors='65') for frame in range(100,700)]
    events=[dict(frame='90',phase='selection'),dict(frame='100',phase='combat')]
    return rows,events,palettes

class FreshVictimMatchTests(unittest.TestCase):
    def test_full_valid_baseline(self):
        self.assertEqual(verify(*sample(),1,2,17)['freshHardwarePaletteColorComparisons'],77400)

    def test_identity_gap_reset_and_palette_corruption_rejected(self):
        for target,change in (('rows',{'p2char':'0'}),('rows',{'frame':'999'}),('rows',{'winner':'1'}),
                              ('palettes',{'p1rgbMismatch':'1'}),('palettes',{'p2source':'ff800300'})):
            rows,events,palettes=sample()
            (rows if target=='rows' else palettes)[10].update(change)
            with self.assertRaises(AssertionError):verify(rows,events,palettes,1,2,17)

    def test_mirror_roles_and_missing_damage_are_not_accepted(self):
        rows,events,palettes=sample()
        with self.assertRaises(AssertionError):verify(rows,events,palettes,2,2,17)
        for row in rows:row['p2hp']='161'
        with self.assertRaises(AssertionError):verify(rows,events,palettes,1,2,17)
