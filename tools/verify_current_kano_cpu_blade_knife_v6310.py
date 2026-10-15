"""Direct original-source adapter: exact blocked shot during round2 handoff.

Preserve the floor/mode and adapter failures. Reuse the entire6304 blade,
knife and fault gate with explicit context only, not nested string escaping.
"""
import ast,json
from pathlib import Path
import verify_current_kano_cpu_blade_knife_v6304 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6311_current_kano_cpu_blade_knife_checked'


def main():
 failures=[ROOT/f'audit_v{n}_current_kano_cpu_blade_knife_checked/failure.json'for n in(6305,6307,6309)]
 need(all(not json.loads(p.read_text())['passed']for p in failures),'All executed host failures preserved')
 source=Path(prior.__file__).read_text();tree=ast.parse(source)
 assignment=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='knife'for t in n.targets))
 changes=ast.literal_eval(assignment.value.args[1])
 changes["native['mode']==(2 if serial==1 else 7)"]="native['mode']==(7)"
 changes["allfields=rows(log,'FIELD');by={(r['frame'],r['slot']):r for r in allfields}"]=\
  "allfields=[r for r in rows(log,'FIELD')if actions[0]['frame']<r['frame']<=max(actions[0]['frame']+50,max(q['frame']for q in overlap.rows(log,'RETIRE')))];by={(r['frame'],r['slot']):r for r in allfields}"
 lines=source.splitlines(keepends=True)
 lines[assignment.lineno-1:assignment.end_lineno]=['knife=model.bind(model.knife.knives,'+repr(changes)+')\n']
 source=''.join(lines)
 adaptations={
  "OUT=ROOT/'audit_v6305_current_kano_cpu_blade_knife_checked'":"OUT=ROOT/'audit_v6311_current_kano_cpu_blade_knife_checked'",
  'shots=knife(text,guest)':"shots=knife(text,guest)\n need(all(r['mode']==2 for r in model.knife.R.rows(text,'FIELD')if 2443<=r['frame']<=2495),'Complete actual knife callbacks mode2 after observed mode7 handoff')",
  'for path in(PARENT,Path(__file__),':"for path in(*failures,*(ROOT/f'tools/verify_current_kano_cpu_blade_knife_v{n}.py'for n in(6304,6306,6308)),PARENT,Path(__file__),",
 }
 for before,after in adaptations.items():
  need(source.count(before)==1,'Single explicit scope/context adaptation');source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__file__=__file__,__name__='direct_current_knife_context',failures=failures)
 exec(compile(source,__file__+'::whole_original_blade_knife_fault_gate','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
