import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from refresh_stage_videos import plan,verify_capture

class StageVideoPlanTests(unittest.TestCase):
    def test_six_unique_positive_own_pair_profiles(self):
        fixtures=plan('stage_video_test')
        self.assertEqual({(kind,actor) for _,kind,actor,_ in fixtures},
                         {(kind,actor) for kind in ('deadpool','tomb','pit') for actor in (17,18)})
        self.assertEqual(len({name for name,_,_,_ in fixtures}),6)
        for _,_,_,args in fixtures:
            for flag in ('--game','--own-victim','--audio','--capture-finish','--sound-candidate'):
                self.assertIn(flag,args)
            self.assertNotIn('--mirror',args)
            self.assertNotIn('--deadpool-no-chord',args)
        with self.assertRaises(AssertionError):plan('../outside')

    def test_arena_filter_prevents_earlier_tomb_capture(self):
        for _,kind,_,args in plan('filtered'):
            self.assertIn(f"--capture-background={dict(deadpool=0,tomb=1,pit=6)[kind]}",args)
        fixtures=plan('pit_retry',True)
        self.assertEqual(len(fixtures),2)
        self.assertTrue(all(kind=='pit' for _,kind,_,_ in fixtures))

    def test_pit_capture_rejects_wrong_arena_and_truncated_interval(self):
        with TemporaryDirectory() as directory:
            run=Path(directory)
            (run/'qualification.json').write_text(json.dumps(dict(nativeLaunchToFallFields=148,nativePitActionFields=206)))
            (run/'pit_objects.csv').write_text('frame\n1148\n')
            (run/'finisher_capture.csv').write_text('frame\n'+''.join(f'{f}\n' for f in range(1000,1266)))
            (run/'stage_environment.csv').write_text('frame,background\n'+''.join(f'{f},6\n' for f in range(1000,1266)))
            verify_capture(run,'pit')
            (run/'stage_environment.csv').write_text('frame,background\n'+''.join(f'{f},1\n' for f in range(1000,1266)))
            with self.assertRaisesRegex(AssertionError,'wrong arena'):verify_capture(run,'pit')
            (run/'stage_environment.csv').write_text('frame,background\n'+''.join(f'{f},6\n' for f in range(1000,1266)))
            (run/'finisher_capture.csv').write_text('frame\n'+''.join(f'{f}\n' for f in range(1000,1265)))
            with self.assertRaisesRegex(AssertionError,'Incomplete Pit'):verify_capture(run,'pit')
