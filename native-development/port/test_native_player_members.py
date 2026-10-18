import unittest
from audit_stock_mame_distribution import player_member


class PlayerMemberTests(unittest.TestCase):
    def test_only_player_inputs_not_developer_dumps_are_selected(self):
        for name in ('PATCH.cmd','PLAY.cmd','MOVELIST_NATIVE.txt','patches/example.ips'):
            self.assertTrue(player_member(name),name)
        for name in ('source/asm/KANO.ASM','FILES.json','roms/mk3.zip','mame.sym','capture.bgra',
                     '../patches/example.ips','patches/../example.ips','patches\\example.ips','patches/.ips'):
            self.assertFalse(player_member(name),name)


if __name__=='__main__':unittest.main()
