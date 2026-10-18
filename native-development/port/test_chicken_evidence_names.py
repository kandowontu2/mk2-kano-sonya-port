import unittest
from chicken_evidence_names import event_filename

class ChickenEvidenceNameTests(unittest.TestCase):
    def test_legacy_primary_names_preserved(self):
        self.assertEqual(event_filename(),'DCS_CHICKEN_EVENTS.json')
        self.assertEqual(event_filename(mirror=True),'DCS_CHICKEN_MIRROR_EVENTS.json')
        self.assertEqual(event_filename(matched=True),'DCS_CHICKEN_MATCHED_EVENTS.json')

    def test_mirror_never_overwrites_primary_or_other_track(self):
        names=[event_filename(matched=matched,mirror=mirror) for matched in (False,True) for mirror in (False,True)]
        names += [event_filename(matched=True,mirror=mirror,track=track) for track in (1,2,3) for mirror in (False,True)]
        self.assertEqual(len(names),len(set(names)))
        self.assertIn('DCS_CHICKEN_MATCHED_MIRROR_EVENTS.json',names)

    def test_invalid_track_or_unmatched_isolation_rejected(self):
        with self.assertRaises(AssertionError):event_filename(matched=True,track=4)
        with self.assertRaises(AssertionError):event_filename(track=1)
