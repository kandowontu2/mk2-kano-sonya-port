import unittest
from qualify_choke import stock_victim_pose


class ChokeVictimPose(unittest.TestCase):
    def test_each_actor_uses_its_own_table_and_second_high_hit_pose(self):
        memory={1000+1*32:2000,1000+8*32:3000,
                2000+16*32:4000,3000+16*32:5000,
                4000+32:0xff111111,5000+32:0xff888888}
        self.assertEqual(stock_victim_pose(memory.__getitem__,1000,1),0xff111111)
        self.assertEqual(stock_victim_pose(memory.__getitem__,1000,8),0xff888888)

    def test_missing_victim_does_not_fall_back_to_liu(self):
        memory={1032:2000,2512:4000,4032:0xff111111}
        with self.assertRaises(KeyError):stock_victim_pose(memory.__getitem__,1000,8)

    def test_added_actors_and_bosses_are_not_original_grip_records(self):
        for victim in (12,13,17,18):
            with self.assertRaises(AssertionError):stock_victim_pose(lambda address:0,1000,victim)


if __name__=='__main__':unittest.main()
