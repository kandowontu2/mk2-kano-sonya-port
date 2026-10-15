"""Full4689 before-boot beam/source/fault checks, actual projector namespace."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/qualify_ending_clear_projection_source_v4689.py').read_text()
changes=[
 ('audit_v4690_ending_clear_projection_source_checked','audit_v4695_ending_clear_projection_source_checked'),
 ('import run_ending_clear_projection_ram_v4687 as capture','import run_ending_clear_projection_ram_v4693 as capture'),
 ('    for p in files:',
  "    files.extend([ROOT/'tools/run_ending_clear_projection_ram_v4687.py',ROOT/'tools/qualify_ending_clear_projection_source_v4689.py'])\n    for p in files:")]
for before,after in changes:
    assert text.count(before)==1;text=text.replace(before,after)
scope=dict(__name__='actual_bound_projection_source4694',__file__=__file__)
exec(compile(text,__file__+'::whole4689_actual_inner_namespace_preflight','exec'),scope)
globals().update({key:value for key,value in scope.items()if not key.startswith('__')})
if __name__=='__main__':main()
