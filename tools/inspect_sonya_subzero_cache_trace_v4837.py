"""Exact original4830 ROM/native binding on the corrected actual4835 trace."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/inspect_sonya_subzero_cache_trace_v4830.py').read_text()
for before,after in (
 ('run_sonya_subzero_cache_trace_ram_v4826','run_sonya_subzero_cache_trace_ram_v4832'),
 ('audit_v4828_sonya_subzero_cache_trace_ram','audit_v4835_sonya_subzero_cache_trace_ram'),
 ("if __name__=='__main__':print(json.dumps(inspect(),indent=2))",'')):
    assert text.count(before)==1,before
    text=text.replace(before,after,1)
exec(compile(text,__file__+'::whole4830_corrected_actual_trace','exec'),globals())
if __name__=='__main__':
    result=inspect()
    assert not result['sourceOnly']and result['traceRows']>0,'Actual trace required, not transport-only or prepared source'
    assert result['lookups']and result['cacheBegins'],'Actual earlier native input provenance required'
    for key in ('selectedMainStreams','actualOverruns'):
        result[key]=dict(count=len(result[key]))if key=='selectedMainStreams'else result[key][:2]
    print(json.dumps(result,indent=2))
