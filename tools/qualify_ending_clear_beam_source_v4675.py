"""Fresh executable preflight after4671 parse-only unmatched-parenthesis error."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
source=(ROOT/'tools/qualify_ending_clear_beam_source_v4671.py').read_text()
try:compile(source,'frozen4671_parse_counterexample','exec')
except SyntaxError as error:
    assert error.lineno==25 and "unmatched ')'"in str(error)
else:raise ValueError('Original parse failure not preserved')
changes=[("'buckets={}')):","'buckets={}'):"),
         ('audit_v4672_ending_clear_beam_source_checked','audit_v4677_ending_clear_beam_source_checked'),
         ('import run_ending_clear_beam_probe_ram_v4670 as capture','import run_ending_clear_beam_probe_ram_v4676 as capture'),
         ('    report=dict(passed=True,inputHashes=',
          "    files.extend([ROOT/'tools/qualify_ending_clear_beam_source_v4671.py',ROOT/'tools/run_ending_clear_beam_probe_ram_v4670.py'])\n    report=dict(passed=True,inputHashes=")]
for before,after in changes:
    assert source.count(before)==1;source=source.replace(before,after)
scope=dict(__name__='qualified_clear_source_4675',__file__=__file__)
exec(compile(source,__file__+'::whole4671_parse_only_correction','exec'),scope)
globals().update({key:value for key,value in scope.items()if not key.startswith('__')})
if __name__=='__main__':main()
