"""Fresh correction of the executed4821 equality/assignment false positive.

The observer, original controls, guest/RAM sinks and native failure stay exact.
Preserve4821 and replay its actual failure; do not claim a native fix.
"""
from pathlib import Path
import re
import qualify_sonya_subzero_cache_trace_source_v4821 as failed_checker

ROOT=Path(__file__).resolve().parent.parent
try:
    failed_checker.source_boundary()
except ValueError as error:
    original_failure=repr(error)
    assert str(error)=='No memory, register, health, AI, RNG, roster, palette, task or input mutations in observer'
else:
    raise ValueError('Executed4821 false positive no longer reproduces')

def observer_readonly(wrapper):
    if 'p:write_' in wrapper or re.search(r'\.value\s*=(?!=)',wrapper) or ':set_value(' in wrapper:
        raise ValueError('No native memory or register assignment in readonly observer')

observer_readonly('if cpu.PC.value==address+16 then end')
for assignment in ('cpu.A0.value=0','cpu.A0.value = 0','p:write_u16(0x010601F0,1)', 'cpu.A0:set_value(0)'):
    try: observer_readonly(assignment)
    except ValueError: pass
    else: raise ValueError('Assignment-check counterexample admitted')

text=(ROOT/'tools/qualify_sonya_subzero_cache_trace_source_v4821.py').read_text()
changes=[
 ('import run_sonya_subzero_cache_trace_ram_v4820 as capture','import run_sonya_subzero_cache_trace_ram_v4826 as capture'),
 ('audit_v4822_sonya_subzero_cache_trace_source_checked','audit_v4827_sonya_subzero_cache_trace_source_checked'),
 ('audit_v4823_{fighter}_subzero_cache_trace_ram','audit_v4828_{fighter}_subzero_cache_trace_ram'),
 ('    need(hashlib.sha256(wrapper.encode()).hexdigest().upper()==EXPECTED_SHA,',
  '    observer_readonly(wrapper)\n    need(hashlib.sha256(wrapper.encode()).hexdigest().upper()==EXPECTED_SHA,'),
 ("'.value=' not in wrapper", "not re.search(r'\\.value\\s*=(?!=)',wrapper)"),
 ('*(ROOT/p for p in TRANSITIVE_LUA)]:pins[str(p.resolve())]=sha(p)',
  "*(ROOT/p for p in TRANSITIVE_LUA),ROOT/'tools/qualify_sonya_subzero_cache_trace_source_v4821.py',ROOT/'tools/run_sonya_subzero_cache_trace_ram_v4820.py']:pins[str(p.resolve())]=sha(p)"),
 ('report=dict(positive,inputHashes=pins,originalSourceFaultsRetained=27,actualSourceFaultsRejected=faults)',
  'report=dict(positive,inputHashes=pins,originalSourceFaultsRetained=27,actualSourceFaultsRejected=faults,executed4821FailureReproduced=original_failure,equalityAcceptedAssignmentRejected=True)')]
for before,after in changes:
    assert text.count(before)==1,before
    text=text.replace(before,after,1)
exec(compile(text,__file__+'::whole4821_corrected_assignment_check','exec'),globals())
