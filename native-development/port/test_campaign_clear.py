import unittest
from pathlib import Path
from qualify_campaign_clear import earned_clear

def sample(frame,mode,**changes):
    row=dict(frame=str(frame),mode=str(mode),winner='0',p1match='1',p2match='0',
             p1selected='18',p1char='18',p2selected='13',p2char='13',p1hp='17',
             p2hp='0',attempt='24',map='16',round='2')
    row.update(changes)
    return row

def clear_rows():
    return [sample(10,5,winner='1',round='1'),
            sample(20,2,p1hp='161',p2hp='161'),sample(30,2),
            sample(32,11,winner='1',p1match='2'),sample(40,11),sample(50,1)]

class EarnedClear(unittest.TestCase):
    def test_packager_rejects_stale_source_guide_build_identity(self):
        source=(Path(__file__).parent/'package_native_patches.py').read_text()
        self.assertIn("assert sha(program_bytes).encode('ascii') in guide",source)
        self.assertIn("files['source/NATIVE_SOURCE_GUIDE.md']=guide",source)

    def test_native_second_win_can_enter_gameover_directly(self):
        result=earned_clear(clear_rows(),18)
        self.assertEqual(result['finalBossClearFrame'],32)
        self.assertEqual(result['attractReturnFrame'],50)

    def test_other_attempt_cannot_supply_first_win(self):
        rows=clear_rows();rows[0]['attempt']='23'
        with self.assertRaises(AssertionError):earned_clear(rows,18)

    def test_zero_health_without_native_counter_is_not_clear(self):
        rows=clear_rows();rows[3]['p1match']='1'
        with self.assertRaises(AssertionError):earned_clear(rows,18)

    def test_wrong_identity_or_dead_player_is_not_clear(self):
        for change in ({'p1char':'1'},{'p2char':'12'},{'p1hp':'0'},{'winner':'2'}):
            rows=clear_rows();rows[3].update(change)
            with self.assertRaises(AssertionError):earned_clear(rows,18)

    def test_same_round_or_no_fresh_round_is_rejected(self):
        for change in ({'round':'2'},{'p1hp':'17'}):
            rows=clear_rows()
            rows[0 if 'round' in change else 1].update(change)
            with self.assertRaises(AssertionError):earned_clear(rows,18)

    def test_no_attract_or_intervening_selection_is_not_full_flow(self):
        rows=clear_rows()[:-1]
        with self.assertRaises(AssertionError):earned_clear(rows,18)
        rows=clear_rows();rows[4]['mode']='4'
        with self.assertRaises(AssertionError):earned_clear(rows,18)

if __name__=='__main__':unittest.main()
