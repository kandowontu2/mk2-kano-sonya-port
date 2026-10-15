"""Exact original retained CPU RGB, with entire original BGRX digest gate."""
from pathlib import Path

source=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_special_frames_remote.py').read_text()
changes=(("profile in('special','air')", "profile in('cpu','cpu_leg')"),
    ("root=sys.modules['__main__']if profile=='special'else sys.modules['capture_native_selector_square_contact_retained']",
     "root=sys.modules['capture_native_selector_cpu_choke_retained_bound']if profile=='cpu'else sys.modules['capture_native_selector_cpu_leg_children_retained']"),
    ("cases=root.RAM_CASES if profile=='special'else root.CONTACT_CASES", "cases=root.CPU_CASES if profile=='cpu'else root.RAM_CASES"),
    ("handles=root.NATIVE_HANDLES if profile=='special'else root.CONTACT_HANDLES", "handles=root.CPU_HANDLES if profile=='cpu'else root.NATIVE_HANDLES"),
    ("assert held['process'].poll()==0 and report['nativeExit']==0 and report['passed']",
     "assert held['process'].poll()==0 and report['nativeExit']==0 and not report['nativeTerminal']['hostDecodeErrors']and len(report['proofs'])==5\n"
     "        answer['originalCapturePassed']=report['passed'];answer['originalCaptureRejection']=report.get('error')"))
for before,after in changes:
    assert source.count(before)==1
    source=source.replace(before,after,1)
exec(compile(source,'whole_original_BRGX_retained_CPU_viewer','exec'))
