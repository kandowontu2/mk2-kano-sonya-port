"""Unchanged original rejection tests routed to actual fresh v2753 captures.
Also require every attempted rejection mutation differs from all real fixtures.
"""
import io, json, unittest
from pathlib import Path
import test_current_interrupt_and_ko_v825 as original
import verify_native_combat_regression_v2854 as current
import verify_current_ko_v1872 as knockout_inventory

ROOT=current.ROOT
OUT=ROOT/'audit_v2857_native_combat_regression_units'
def interrupt(move='blade',side=1,victim='sonya'):
    return (ROOT/f'audit_v2853_interrupt_{move}_p{side}_{victim}/run.log').read_text(encoding='utf-8-sig')
def ko(move='bicycle',side=1,victim='sonya'):
    return (ROOT/f'audit_v2853_ko_{move}_p{side}_{victim}/run.log').read_text(encoding='utf-8-sig')
original.interrupt=interrupt;original.ko=ko
ACTUAL_INTERRUPT={interrupt(m,s,v) for m,s,v in current.interrupt.INT_CASES}
ACTUAL_KO={ko(m,s,v) for m,s,v in knockout_inventory.CASES}

class Interruptions(original.Interruptions):
    def reject(self,log,move='blade',side=1,victim='sonya'):
        self.assertNotIn(log,ACTUAL_INTERRUPT,'Mutation must change the actual evidence')
        super().reject(log,move,side,victim)

class Knockouts(original.Knockouts):
    def reject(self,log,move='bicycle',side=1,victim='sonya'):
        self.assertNotIn(log,ACTUAL_KO,'Mutation must change the actual evidence')
        super().reject(log,move,side,victim)
    def test_all_ten_native_ko_round_cases(self):
        for move,side,victim in knockout_inventory.CASES:
            with self.subTest(move=move,side=side,victim=victim):
                proof=self.grade(ko(move,side,victim),move,side,victim)
                self.assertTrue(proof['passed'],proof['errors'])

if __name__=='__main__':
    current.assembly.need(not OUT.exists(),'Immutable rejection evidence')
    proof_path=current.OUT/'report.json';proof=json.loads(proof_path.read_text())
    current.assembly.need(proof['passed'] and proof['candidate']==current.assembly.NAME and
        proof['originalPerFieldAcceptanceUnchanged'] and len(proof['cases'])==20,'Actual accepted full original combat contracts')
    pins=dict(proof['inputHashes']);pins[str(proof_path)]=current.assembly.sha(proof_path)
    for file,wanted in pins.items():current.assembly.need(current.assembly.sha(file)==wanted,'Actual positive evidence unchanged '+file)
    stream=io.StringIO();suite=unittest.TestSuite()
    for cls in (Interruptions,Knockouts):suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    for file in (Path(__file__),Path(original.__file__),Path(original.old.__file__)):
        pins[str(file.resolve())]=current.assembly.sha(file)
    for file,wanted in pins.items():current.assembly.need(current.assembly.sha(file)==wanted,'Actual captures/source never changed '+file)
    OUT.mkdir();(OUT/'unit-tests.log').write_text(stream.getvalue())
    report=dict(passed=result.wasSuccessful(),methods=result.testsRun,candidate=current.assembly.NAME,
                actualMutationNonVacuityRequired=True,originalRejectionPredicatesUnchanged=True,
                actualCaptureFilesUnmodified=True,inputHashes=pins,fullPortAcceptance=False,scope=__doc__)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(stream.getvalue(),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
