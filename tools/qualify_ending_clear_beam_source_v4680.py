"""Executable full4671 gates: parse fix and actual current guest-provider binding."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
source=(ROOT/'tools/qualify_ending_clear_beam_source_v4671.py').read_text()
try:compile(source,'frozen4671_parse_counterexample','exec')
except SyntaxError as error:assert error.lineno==25 and "unmatched ')'"in str(error)
else:raise ValueError('Original parse failure not preserved')
changes=[("'buckets={}')):","'buckets={}'):"),
 ('audit_v4672_ending_clear_beam_source_checked','audit_v4682_ending_clear_beam_source_checked'),
 ('import run_ending_clear_beam_probe_ram_v4670 as capture','import run_ending_clear_beam_probe_ram_v4681 as capture'),
 ('guest=old.original.expected();rom=',"import run_kintaro_pressure_guard_long_campaign_v4439 as guest_source\n    guest=guest_source.expected();rom="),
 ('    report=dict(passed=True,inputHashes=',
  "    need(not hasattr(old.original,'expected'),'Original wrong guest-provider attribute failure preserved')\n    files.extend([ROOT/'tools/qualify_ending_clear_beam_source_v4671.py',ROOT/'tools/run_ending_clear_beam_probe_ram_v4670.py',ROOT/'tools/qualify_ending_clear_beam_source_v4675.py',ROOT/'tools/run_ending_clear_beam_probe_ram_v4676.py',ROOT/'tools/run_kintaro_pressure_guard_long_campaign_v4439.py'])\n    report=dict(passed=True,priorParseFailurePreserved=True,originalWrongExpectedModuleFailurePreserved=True,inputHashes=")]
for before,after in changes:
    assert source.count(before)==1;source=source.replace(before,after)
scope=dict(__name__='qualified_clear_source_4680',__file__=__file__)
exec(compile(source,__file__+'::whole4671_actual_guest_provider','exec'),scope)
globals().update({key:value for key,value in scope.items()if not key.startswith('__')})
if __name__=='__main__':main()
