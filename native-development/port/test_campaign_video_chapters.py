import unittest
from campaign_video_chapters import chapter_plan, metadata


class CampaignChapterTests(unittest.TestCase):
    def test_first_encounter_and_later_clear_attempt_are_distinct(self):
        clock = dict(firstGuestFrame=1000, frames=6001, rate=55)
        def row(frame, position, opponent, attempt):
            return dict(frame=str(frame), mode='2', map=str(position), p2selected=str(opponent), attempt=str(attempt))
        rows = [row(1200,0,3,0), row(2000,0,3,2), row(3000,1,9,2),
                row(4000,16,13,3), row(5000,16,13,4)]
        result = chapter_plan(iter(rows), clock, {3:'BARAKA',9:'REPTILE',13:'SHAO KAHN'}, {0:2,1:2,16:4}, 6000)
        self.assertEqual([r['title'] for r in result], ['CHARACTER SELECT','BARAKA','BARAKA - CLEAR ATTEMPT',
            'REPTILE','SHAO KAHN','SHAO KAHN - CLEAR ATTEMPT','ENDING'])
        self.assertTrue(metadata(result).startswith(';FFMETADATA1\n[CHAPTER]'))

    def test_morph_object_does_not_rename_shang_matchup(self):
        rows = [dict(frame='1200',mode='2',map='14',p2selected='6',p2char='17',attempt='0')]
        result = chapter_plan(rows,dict(firstGuestFrame=1000,frames=3000,rate=55),{6:'SHANG TSUNG',17:'KANO'},{14:0},3000)
        self.assertEqual(result[1]['title'],'SHANG TSUNG')

    def test_unrecorded_ending_is_rejected(self):
        with self.assertRaises(AssertionError):
            chapter_plan([],dict(firstGuestFrame=1000,frames=3000,rate=55),{}, {},9000)


if __name__=='__main__':unittest.main()
