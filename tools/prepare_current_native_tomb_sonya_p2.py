"""Last basic reciprocal Tomb role, current real actor IDs."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_tomb_sonya_preparation'
out=sync.ROOT/'audit_current_native_tomb_sonya_p2_preparation';assert not out.exists()
runner=(base/'run_sonya_p1.ps1').read_text()
assert runner.count("MK2KS_STAGE_SIDE='1'")==1
runner=runner.replace("MK2KS_STAGE_SIDE='1'","MK2KS_STAGE_SIDE='2'")
runner=runner.replace('audit_current_native_tomb_sonya_p1_runtime','audit_current_native_tomb_sonya_p2_runtime')
out.mkdir();(out/'run_sonya_p2.ps1').write_text(runner)
checker=(sync.ROOT/'tools/qualify_current_native_tomb_sonya.py').read_text()
needle='    replacements={';assert checker.count(needle)==1
checker=checker.replace(needle,needle+'\n        "r[\'side\']==\'1\'":"r[\'side\']==\'2\'",')
checker=checker.replace('audit_current_native_tomb_sonya_p1_runtime','audit_current_native_tomb_sonya_p2_runtime').replace('audit_current_native_tomb_sonya_p1_checked','audit_current_native_tomb_sonya_p2_checked').replace('Current genuine SonyaP1/KanoP2','Current genuine SonyaP2/KanoP1')
checker=checker.replace("path=Path(__file__).with_name('qualify_current_native_tomb_case.py')","path=Path(r'"+str(sync.ROOT/'tools/qualify_current_native_tomb_case.py')+"')")
(out/'qualify.py').write_text(checker)
print('Prepared SonyaP2/KanoP1 native Tomb, same Lua/no media/caps')
