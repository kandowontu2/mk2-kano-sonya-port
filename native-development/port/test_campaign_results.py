import unittest
from campaign_rounds import native_round_wins,completed_native_matches,sampled_action_tag_episodes


def result(attempt,round_number,counter,frame):
    return dict(map=3,opponent=7,attempt=attempt,nativeRound=round_number,
                playerRoundWins=counter,cpuRoundWins=0,resultFrame=frame)


class NativeResults(unittest.TestCase):
    def test_action_tag_counts_are_opponent_scoped_and_reset_on_new_round(self):
        row=dict(attempt='0',map='3',round='1',p2char='7',p1action='530')
        rows=[row,row,dict(row,round='2'),dict(row,attempt='1',round='1'),
              dict(row,map='4',p2char='4'),dict(row,map='4',p2char='4')]
        self.assertEqual(sampled_action_tag_episodes(rows),{7:{'0212':3},4:{'0212':1}})
        self.assertEqual(sampled_action_tag_episodes([]),{})

    def test_round_wins_on_different_paid_attempts_are_not_a_match(self):
        self.assertEqual(completed_native_matches([result(0,1,1,100),result(1,1,1,200)]),[])

    def test_a_counter_two_without_its_first_round_is_not_full_proof(self):
        self.assertEqual(completed_native_matches([result(0,1,1,100),result(1,2,2,200)]),[])

    def test_successful_attempt_excludes_earlier_failed_attempt_wins(self):
        rows=[result(0,1,1,100),result(1,1,1,200),result(1,3,2,300)]
        matches=completed_native_matches(rows)
        self.assertEqual(len(matches),1)
        self.assertEqual(matches[0]['attempt'],1)
        self.assertEqual(matches[0]['nativeResults'],rows[1:])

    def test_health_minimum_is_not_a_winning_result(self):
        data=[dict(map=3,opponent=7,attempt=0,nativeRound=1,firstFrame=1)]
        row=dict(map='3',round='1',attempt='0',frame='100',mode='2',winner='0',
                 p1hp='100',p2hp='0',p1match='0',p2match='0')
        self.assertEqual(native_round_wins([row],data),[])
        row.update(mode='5',winner='1',p1match='1')
        self.assertEqual(len(native_round_wins([row],data)),1)


if __name__=='__main__':unittest.main()
