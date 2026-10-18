import unittest
from pathlib import Path
from run_lethal_victim_matrix import plan
from qualify_lethal_roster_matrix import validate_coverage


class LethalVictimPlanTests(unittest.TestCase):
    def test_full_plan_covers_four_lethals_fourteen_victims_both_sides(self):
        cases=plan()
        self.assertEqual(len(cases),112)
        self.assertEqual(len({c[0] for c in cases}),112)
        self.assertEqual({c[2] for c in cases},set(range(12))|{17,18})
        self.assertTrue(all('--finisher-rejoin' in c[4] and '--audio' not in c[4] for c in cases))

    def test_pilot_is_exact_subset_without_writes_or_boss_victims(self):
        self.assertEqual(len(plan(True)),8)
        self.assertTrue(all(c in plan() for c in plan(True)))
        for _,kind,victim,side,args in plan():
            self.assertIn('--'+kind,args)
            self.assertIn(f'--finisher-victim={victim}',args)
            self.assertEqual('--mirror' in args,side==2)

    def test_bubble_victim_animation_comes_from_linked_native_table(self):
        source=(Path(__file__).parent/'qualify_bubble.py').read_text()
        self.assertIn("read(symbols['character_anitabs1']+victim*32)",source)
        self.assertNotIn("'ks_kano_anitab1' if victim==17 else 'lk_anitab1'",source)

    def test_acceptance_rejects_partial_and_duplicate_coverage(self):
        cases=[dict(run=n,kind=k,victim=v,side=s) for n,k,v,s,_ in plan(True)]
        validate_coverage(cases,True)
        with self.assertRaises(AssertionError):validate_coverage(cases[:-1],True)
        with self.assertRaises(AssertionError):validate_coverage(cases+cases[:1],True)
        with self.assertRaises(AssertionError):validate_coverage(cases,False)

    def test_completed_family_does_not_count_as_full_matrix(self):
        cases=[dict(run=n,kind=k,victim=v,side=s) for n,k,v,s,_ in plan() if k=='extract']
        validate_coverage(cases,False,'extract')
        with self.assertRaises(AssertionError):validate_coverage(cases)
        with self.assertRaises(AssertionError):validate_coverage(cases,False,'laser')


if __name__=='__main__':unittest.main()
