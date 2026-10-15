"""Fresh bounded readonly native probe after corrected source preflight4825.

Exact original4820 collector; only fresh source/result leaves change.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/run_sonya_subzero_cache_trace_ram_v4820.py').read_text()
for before,after in (
 ('audit_v4822_sonya_subzero_cache_trace_source_checked','audit_v4827_sonya_subzero_cache_trace_source_checked'),
 ('audit_v4823_{fighter}_subzero_cache_trace_ram','audit_v4828_{fighter}_subzero_cache_trace_ram'),
 ('audit_v4823_{args.fighter}_subzero_cache_trace_ram','audit_v4828_{args.fighter}_subzero_cache_trace_ram'),
 ('audit_v4824_{args.fighter}_subzero_cache_trace_observed','audit_v4829_{args.fighter}_subzero_cache_trace_observed'),
 ('qualify_sonya_subzero_cache_trace_source_v4821','qualify_sonya_subzero_cache_trace_source_v4825')):
    assert text.count(before)==1,before
    text=text.replace(before,after,1)
exec(compile(text,__file__+'::whole4820_fresh_leaves_only','exec'),globals())
