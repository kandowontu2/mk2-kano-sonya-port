"""Run unchanged state/cleanup corruptions on actual current ordinary leg paths."""
import hashlib
import io
import json
import sys
import unittest
from pathlib import Path
import test_current_cpu_pair_state_v836 as prior
import verify_current_cpu_ordinary_leg_v839 as current
v=current.v


class OrdinaryLeg(prior.PairState):
    @classmethod
    def setUpClass(cls):
        cls.logs={name:(v.ROOT/name/'run.log').read_text(encoding='utf-8-sig')for name in current.CASES}
        cls.proofs={name:cls.verify(name,log)for name,log in cls.logs.items()}
        assert all(p['passed']for p in cls.proofs.values()),cls.proofs

    @staticmethod
    def verify(name,log):return v.ordinary.verify_log(log,current.CASES[name][0])

    def test_five_current_native_baselines(self):
        # Override the inherited five-case baseline, keeping all unchanged
        # held-state/opcode/damage/fling/ready mutation methods below it.
        self.assertEqual(len(self.proofs),3)
        for name,proof in self.proofs.items():
            v.matched(v.ROOT/name,{})
            self.assertEqual((proof['target'],proof['held_fields'],proof['damage']),('sonya',46,35))
            self.assertEqual(proof['native_followup']['kind'],'ordinary')
            self.assertFalse(proof['whole_character_integration_complete'])

    def test_ordinary_followup_cannot_replace_signature(self):
        for name,(player,_)in current.CASES.items():
            for move in('square','bicycle'):
                with self.subTest(capture=name,wrong_move=move):
                    self.assertFalse(v.special.verify_log(self.logs[name],player,move)['passed'])


if __name__=='__main__':
    out=v.ROOT/'audit_v840_current_cpu_ordinary_leg_units'
    if out.exists():raise ValueError('Refusing to overwrite evidence')
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(OrdinaryLeg))
    paths=[v.ROOT/name/'run.log'for name in current.CASES]
    paths+=[v.ROOT/name/'result.json'for name in current.CASES]
    for module in tuple(sys.modules.values()):
        value=getattr(module,'__file__',None)
        if value:
            path=Path(value).resolve()
            if path.is_relative_to(v.ROOT/'tools')and path.suffix=='.py':paths.append(path)
    hashes={str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest().upper()for p in paths}
    out.mkdir();(out/'unit-tests.log').write_text(stream.getvalue())
    (out/'verification.json').write_text(json.dumps({'passed':result.wasSuccessful(),'methods':result.testsRun,
        'baseline_cases':3,'inputHashes':hashes,'fullPortAcceptance':False},indent=2)+'\n')
    print(stream.getvalue());sys.exit(0 if result.wasSuccessful()else 1)
