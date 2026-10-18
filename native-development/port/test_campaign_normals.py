import unittest
from inspect_campaign_normals import inventory,NORMALS

class CampaignNormalInventoryTests(unittest.TestCase):
    def test_only_actual_selected_actor_in_combat_counts(self):
        actions={name:i for i,name in enumerate(NORMALS)}
        def row(mode='2',selected='17',active='17'):
            return dict(mode=mode,p1selected=selected,p1char=active,p1action='0')
        result=inventory([row(),row('4'),row(selected='6'),row(active='18')],17,actions)
        self.assertEqual(result[NORMALS[0]]['sampledFields'],1)
        self.assertTrue(result[NORMALS[0]]['observed'])
        self.assertFalse(result[NORMALS[1]]['observed'])
