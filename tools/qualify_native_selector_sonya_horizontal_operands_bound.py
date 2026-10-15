"""Preserve rejected import source; repair one Python conditional spacing token.

Whole original operand/replay/source/status model and fourteen faults retained.
Same native42616 data only; no new game to repair a host checker typo.
"""
import json
from pathlib import Path
import capture_native_selector_sonya_horizontal_operands as capture

path=Path(__file__).with_name('qualify_native_selector_sonya_horizontal_operands.py')
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
failure=ROOT/'audit_native_selector_sonya_horizontal_operands_checked/failure.json'
source=path.read_text()
try:compile(source,str(path),'exec')
except SyntaxError as error:
    need(error.msg=="expected 'else' after 'if' expression" and error.lineno==115,
         'Exact original actually rejected checker conditional')
    if not failure.exists():
        failure.parent.mkdir()
        failure.write_text(json.dumps(dict(passed=False,error=repr(error),line=error.lineno,
            sourceSHA256=sha(path),originalSource=str(path),newNativeGames=0,fullPortAcceptance=False),indent=2)+'\n')
else:raise ValueError('Original actual import rejection unexpectedly absent')
for before,after in (
    ('else3191','else 3191'),
    ("OUT=ROOT/'audit_native_selector_sonya_horizontal_operands_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_horizontal_operands_bound_checked'"),
    ('for p in (Path(__file__),path,Path(prior.__file__),Path(geometry.__file__),',
     'for p in (Path(__file__),original_source,original_failure,path,Path(prior.__file__),Path(geometry.__file__),')):
    need(source.count(before)==1,'Only actual host syntax or explicit preservation boundary repaired')
    source=source.replace(before,after,1)
original_source,original_failure=path,failure
exec(compile(source,str(path)+'::whole_original_operand_suite_syntax_bound','exec'))
