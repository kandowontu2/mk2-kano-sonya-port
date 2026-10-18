import unittest
from campaign_rounds import split_rounds

def row(frame,stage,round_number,player,cpu,score=0):
    return dict(frame=str(frame),map=str(stage),round=str(round_number),p1hp=str(player),
        p2hp=str(cpu),p2char='3',p1match=str(score))

class CampaignRoundTests(unittest.TestCase):
    def test_healthy_win_small_refill_starts_new_native_round(self):
        result=split_rounds([row(1,0,1,161,161),row(2,0,1,135,0),
            row(3,0,2,161,161),row(4,0,2,71,0)])
        self.assertEqual(len(result),2)
        self.assertEqual([r['minimumPlayerHP'] for r in result],[135,71])
        self.assertEqual([r['minimumCPUHP'] for r in result],[0,0])

    def test_score_update_inside_ko_not_an_extra_round(self):
        result=split_rounds([row(1,0,2,71,0,1),row(2,0,2,71,0,2)])
        self.assertEqual(len(result),1)

    def test_new_map_resets_round_counter(self):
        result=split_rounds([row(1,0,2,71,0),row(2,1,1,161,161)])
        self.assertEqual([r['map'] for r in result],[0,1])
        self.assertEqual([r['nativeRound'] for r in result],[2,1])

    def test_continue_does_not_merge_reused_round_counter(self):
        before=row(1,2,1,0,91)
        after=row(100,2,1,161,161);after['attempt']='1'
        result=split_rounds([before,after])
        self.assertEqual(len(result),2)
        self.assertEqual([r['attempt'] for r in result],[0,1])
        self.assertEqual([r['minimumPlayerHP'] for r in result],[0,161])

if __name__=='__main__':unittest.main()
