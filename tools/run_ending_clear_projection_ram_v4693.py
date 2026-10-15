"""Fresh projection capture: bind projector in the actual generated collector."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/run_ending_clear_projection_ram_v4687.py').read_text()
before='    text=inspect.getsource(previous.collector)'
after="""    text=inspect.getsource(previous.collector)
    binding='namespace=dict(vars(original),__file__=__file__,source=source,LUA=source.LUA,model=model,comparison=comparison)'
    need(text.count(binding)==1,'Actual inner full4439 capture namespace, not just outer factory')
    text=text.replace(binding,binding[:-1]+',projection=projection)')"""
changes=[(before,after),
 ('qualify_ending_clear_projection_source_v4689','qualify_ending_clear_projection_source_v4694'),
 ('audit_v4690_ending_clear_projection_source_checked','audit_v4695_ending_clear_projection_source_checked'),
 ('audit_v4691_{fighter}_ending_clear_projection_ram','audit_v4696_{fighter}_ending_clear_projection_ram'),
 ('audit_v4692_kano_ending_clear_projection_observed','audit_v4697_kano_ending_clear_projection_observed')]
for before,after in changes:
    assert text.count(before)==1;text=text.replace(before,after)
scope=dict(__name__='actual_bound_projection_capture4693',__file__=__file__)
exec(compile(text,__file__+'::whole4687_actual_inner_namespace_binding','exec'),scope)
globals().update({key:value for key,value in scope.items()if not key.startswith('__')})
if __name__=='__main__':main()
