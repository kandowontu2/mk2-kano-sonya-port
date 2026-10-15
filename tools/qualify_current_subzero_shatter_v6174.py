"""Exact nested source-pin binding repair; no game or predicate changes.

The6172 matrix reached final source pinning after all native/refill/pixel
checks, but its nested exec scope omitted two precursor path variables. Bind
them explicitly and retain every original check, fault and executed source.
"""
from pathlib import Path
previous_harness=Path(__file__).with_name('qualify_current_subzero_shatter_v6172.py')
source=previous_harness.read_text()
source=source.replace('audit_v6173_current_subzero_shatter_checked','audit_v6175_current_subzero_shatter_checked')
before="source=source.replace(before,'prior,repair,Path(__file__),Path(original.__file__),Path(refill_source.__file__)',1)"
after="source=source.replace(before,'prior,repair,previous_harness,Path(__file__),Path(original.__file__),Path(refill_source.__file__)',1)"
assert source.count(before)==1,'All precursor source paths retained'
source=source.replace(before,after,1)
before="scope=dict(globals(),__name__='complete_current_shatter_and_nextmatch')"
after="source=source.replace('scope=dict(original.__dict__,','scope=dict(original.__dict__,prior=prior,repair=repair,previous_harness=previous_harness,',1)\n"+before
assert source.count(before)==1,'Exact complete nested source pin binding'
source=source.replace(before,after,1)
exec(compile(source,__file__+'::complete_native_matrix_pin_scope','exec'),globals())
