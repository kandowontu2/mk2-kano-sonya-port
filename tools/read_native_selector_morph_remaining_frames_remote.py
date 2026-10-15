"""Whole-pixel original terminal reader with exact remaining-route identity."""
from pathlib import Path
path = Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port\tools\read_native_selector_morph_startup_frames_remote.py')
source = path.read_text()
for before,after in (
    ("request['case'] == 'ball_p1'", "request['case'] in ('square_p1','ball_p2','square_p2')"),
    ("c = root.CASES['ball',1]", "move,label = request['case'].split('_'); side = int(label[1:]); c = root.CASES[move,side]"),
    ("root.ROOT/'audit_native_selector_morph_startup_return_ball_p1_checked/report.json'",
     "root.ROOT/f'audit_native_selector_morph_startup_return_{move}_p{side}_checked/report.json'"),
    ("assert identity == receipt['actualNativeIdentity'] and (identity['ProcessId'],identity['ParentProcessId'],identity['createdUnix']) == (46572,38752,1791761737.394802)",
     "process = json.loads((c['folder']/'process.json').read_text()); assert identity == receipt['actualNativeIdentity'] == process['actualWindowsIdentity'] and identity['ProcessId'] == c['process'].pid and identity['ParentProcessId'] == 38752")):
    assert source.count(before) == 1
    source = source.replace(before,after,1)
exec(compile(source,str(path)+'::whole_original_RGB_remaining_route_identity','exec'))
