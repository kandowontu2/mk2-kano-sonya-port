"""Re-run the reported-failure counterexamples against actual current captures."""
import io,json,unittest
from pathlib import Path
import numpy as np
from PIL import Image
import test_current_native_ui_v817 as prior
import verify_native_palette_ui_v2789 as current
v=current.model;ROOT=current.ROOT;OUT=ROOT/'audit_v2793_native_palette_ui_units'

class CurrentNativeUI(prior.NativeUI):
    @classmethod
    def setUpClass(cls):
        path=current.OUT/'report.json';report=json.loads(path.read_text())
        assert report['passed'] and report['candidate']==current.NAME
        for file,wanted in report['inputHashes'].items():assert current.sha(file)==wanted
        cls.proof=report;cls.logs=[]
        for fighter,side in prior.CASES:
            folder=ROOT/f'audit_v2788_ui_{fighter}_p{side}'
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            assert v.verify_log(log,fighter,side)['passed'];cls.logs.append(log)
        cls.folder=ROOT/'audit_v2788_ui_kano_p1';cls.snapshots=v.records(cls.logs[0],'SNAP')
        cls.images={r['file']:np.asarray(Image.open(cls.folder/'snap'/r['file']).convert('RGB'))for r in cls.snapshots}
        cls.ui=(ROOT/'roms/mk2ks/mk2ks.ui').read_bytes()

    def test_four_actual_current_native_cases(self):
        for i,(fighter,side) in enumerate(prior.CASES):
            proof=v.verify_log(self.logs[i],fighter,side)
            rendered=v.render(ROOT/f'audit_v2788_ui_{fighter}_p{side}',self.logs[i],fighter,side)
            self.assertTrue(proof['passed']);self.assertFalse(proof['whole_character_integration_complete'])
            self.assertEqual(proof['first_match_participant_fields'],362)
            self.assertGreaterEqual(rendered['native_name_shadow_checks'],4)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve evidence'
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CurrentNativeUI))
    OUT.mkdir();(OUT/'unit-tests.log').write_text(stream.getvalue())
    pins={str(path):current.sha(path)for path in (Path(__file__),Path(prior.__file__),Path(v.__file__),current.OUT/'report.json')}
    (OUT/'report.json').write_text(json.dumps(dict(passed=result.wasSuccessful(),candidate=current.NAME,methods=result.testsRun,
        scope='Fresh four-slot baseline and actual state/pixel corruptions for reported CSS/ladder/name failures; immutable artifacts unchanged',
        inputHashes=pins,fullPortAccepted=False),indent=2)+'\n')
    print(stream.getvalue());raise SystemExit(0 if result.wasSuccessful()else 1)
