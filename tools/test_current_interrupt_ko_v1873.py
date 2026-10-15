"""Re-run unchanged v825 counterexamples against fresh v1836 physical traces."""
import io
import json
import unittest
import test_current_interrupt_and_ko_v825 as original
import verify_current_interrupt_v1870 as current
import verify_current_ko_v1872 as ko_current
from verify_human_special_phases_v1767 import sha

ROOT=current.ROOT
OUT=ROOT/'audit_v1873_current_interrupt_ko_units'

def interrupt(move='blade',side=1,victim='sonya'):
    return (ROOT/f'audit_v1869_interrupt_{move}_p{side}_{victim}/run.log').read_text(encoding='utf-8-sig')

def ko(move='bicycle',side=1,victim='sonya'):
    return (ROOT/f'audit_v1871_ko_{move}_p{side}_{victim}/run.log').read_text(encoding='utf-8-sig')

# Fixture routing only: every inherited rejection predicate is unchanged.
original.interrupt=interrupt
original.ko=ko

class ExpandedKnockouts(original.Knockouts):
    def test_all_ten_current_ko_round_cases(self):
        for move,side,victim in ko_current.CASES:
            with self.subTest(move=move,side=side,victim=victim):
                proof=self.grade(ko(move,side,victim),move,side,victim)
                self.assertTrue(proof['passed'],proof['errors'])

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    pins={}
    for folder in (current.OUT,ko_current.OUT):
        path=folder/'report.json';report=json.loads(path.read_text())
        assert report['passed'] and report['candidate']==current.NAME
        pins.update(report['inputHashes']);pins[str(path)]=sha(path)
    for file,wanted in pins.items():assert sha(file)==wanted,'Changed verified fixture '+file
    stream=io.StringIO();suite=unittest.TestSuite()
    for cls in (original.Interruptions,ExpandedKnockouts):suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    current.module_pins(pins)
    OUT.mkdir();(OUT/'unit-tests.log').write_text(stream.getvalue())
    (OUT/'report.json').write_text(json.dumps(dict(passed=result.wasSuccessful(),methods=result.testsRun,
        candidate=current.NAME,inputHashes=pins,fullPortAcceptance=False,scope=__doc__),indent=2)+'\n')
    print(stream.getvalue(),flush=True)
    raise SystemExit(0 if result.wasSuccessful()else 1)
