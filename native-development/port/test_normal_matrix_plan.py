import unittest
from qualify_normal_matrix import plan
from qualify_normal_contact import contact_spec

class NormalMatrixPlanTests(unittest.TestCase):
    def test_full_normal_contact_plan_has_all_seventeen_action_types_and_roles(self):
        fixtures=plan();cells=set()
        self.assertEqual(len(fixtures),136)
        for _,args,_ in fixtures:
            side=int(next(a.split('=')[1] for a in args if a.startswith('--normal-attacker=')))
            actor=((18,17) if '--mirror' in args else (17,18))[side-1]
            move=next(a.split('=')[1] for a in args if a.startswith('--normal-case='))
            gap=int(next((a.split('=')[1] for a in args if a.startswith('--normal-gap=')),'70'))
            blocking='--normal-block' in args
            action=contact_spec(move,gap,blocking)[0]
            cells.add((actor,side,action,blocking))
        self.assertEqual(len(cells),136)
        self.assertEqual(len({action for _,_,action,_ in cells}),17)
