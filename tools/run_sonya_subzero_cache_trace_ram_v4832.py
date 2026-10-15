"""Fresh native readonly trace after actual missing-register observer failure."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/run_sonya_subzero_cache_trace_ram_v4820.py').read_text()
for before,after in (
 ('mk2ks_sonya_subzero_cache_trace_ram_v4819.lua','mk2ks_sonya_subzero_cache_trace_ram_v4831.lua'),
 ('audit_v4822_sonya_subzero_cache_trace_source_checked','audit_v4834_sonya_subzero_cache_trace_source_checked'),
 ('audit_v4823_{fighter}_subzero_cache_trace_ram','audit_v4835_{fighter}_subzero_cache_trace_ram'),
 ('audit_v4823_{args.fighter}_subzero_cache_trace_ram','audit_v4835_{args.fighter}_subzero_cache_trace_ram'),
 ('audit_v4824_{args.fighter}_subzero_cache_trace_observed','audit_v4836_{args.fighter}_subzero_cache_trace_observed'),
 ('qualify_sonya_subzero_cache_trace_source_v4821','qualify_sonya_subzero_cache_trace_source_v4833')):
    assert text.count(before)==1,before
    text=text.replace(before,after,1)
needle="exec(compile(text,__file__+'::whole4772_readonly_defect_probe_only','exec'),globals())"
runtime_before="    meta=json.loads((folder/'result.json').read_text())"
runtime_after=runtime_before+"\n    need('MK2_SUBZERO_CACHE_TRACE frame=' in text and 'first_bad=108255' in text, 'Actual nonempty readonly cache provenance and deterministic bad-write witness required; transport-only success insufficient')"
assert text.count(needle)==1
injection='assert text.count('+repr(runtime_before)+')==1\ntext=text.replace('+repr(runtime_before)+','+repr(runtime_after)+',1)\n'
text=text.replace(needle,injection+needle,1)
exec(compile(text,__file__+'::whole4820_corrected_observer_and_runtime_gate','exec'),globals())
