"""Exact original pixel reader; independently qualified tower5, rejection intact."""
from pathlib import Path
source=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_cpu_guard_frames_remote.py').read_text()
before='capture_native_selector_cpu_guard_shadow'
assert source.count(before)==1
source=source.replace(before,'capture_native_selector_cpu_sonya_confirm264',1)
marker="exec(compile(source,'whole_original_BGRX_callback_distinct_guard_viewer','exec'))"
assert source.count(marker)==1
adapter='''
before="        assert held['process'].poll()==0 and report['nativeExit']==0 and report['passed']"
after="""        assert held['process'].poll()==0 and report['nativeExit']==0 and not report['passed']
        assert report['error']==\"ValueError('Actual original-derived Sonya stage-zero tower and unchanged true roster')\"
        qualified=json.loads((root.ROOT/'audit_native_selector_cpu_sonya_round_order_checked/report.json').read_text())
        assert qualified['passed'] and qualified['sameOriginalTerminalNativePID']==held['process'].pid==14472
        assert qualified['actualNativeIdentity']==held['identity']
        assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()==h for p,h in qualified['inputHashes'].items())
"""
assert source.count(before)==1
source=source.replace(before,after,1)
'''
source=source.replace(marker,adapter+'\n'+marker,1)
exec(compile(source,'whole_original_BGRX_Sonya_tower5_reader_independent_current_qualification','exec'))
