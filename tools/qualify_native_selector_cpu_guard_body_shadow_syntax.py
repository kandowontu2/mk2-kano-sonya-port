"""Fix only the pre-import host predicate grouping; preserve its syntax rejection."""
from pathlib import Path
import capture_native_selector_cpu_guard_shadow as actual

ROOT=actual.ROOT
original_path=ROOT/'tools/qualify_native_selector_cpu_guard_body_shadow.py'
syntax_failure=ROOT/'audit_native_selector_cpu_guard_body_shadow_syntax_rejection/report.json'
source=original_path.read_text()
before="""            if a['mode']==c['mode']==2 and a['states']==c['states']=='1,0'and
                    a['valid']==c['valid']==1 and a['id']==c['id']==17 and
                    a['owner']==a['actor']and c['owner']==c['actor']:"""
after=before.replace('if a[','if (a[',1).replace("c['owner']==c['actor']:","c['owner']==c['actor']):",1)
source=actual.prior.current.replace(source,before,after)
source=actual.prior.current.replace(source,
    "OUT=ROOT/'audit_native_selector_cpu_guard_body_shadow_checked'",
    "OUT=ROOT/'audit_native_selector_cpu_guard_body_shadow_syntax_checked'")
source=actual.prior.current.replace(source,
    'for p in(Path(__file__),Path(body.__file__),Path(model.__file__),',
    'for p in(original_path,syntax_failure,Path(__file__),Path(body.__file__),Path(model.__file__),')
scope=dict(__file__=__file__,original_path=original_path,syntax_failure=syntax_failure)
exec(compile(source,__file__+'::whole_original_gate_predicate_grouping_only','exec'),scope)
bindings=scope['bindings']
execute=scope['execute']
safe_execute=scope['safe_execute']
