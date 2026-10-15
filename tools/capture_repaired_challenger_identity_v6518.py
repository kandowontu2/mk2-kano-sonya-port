"""Preserve first new-candidate host identity failure; retain actual census."""
import argparse,inspect
from pathlib import Path
import capture_repaired_challenger_v6510 as prior
ROOT,need=prior.ROOT,prior.need

def capture(fighter,side):
 source=inspect.getsource(prior.capture)
 before='audit_v6511_repaired_challenger_'
 need(source.count(before)==1,'Fresh immutable identity diagnostic')
 source=source.replace(before,'audit_v6519_repaired_challenger_identity_',1)
 # Add a separate full Windows census artifact before the exact old matcher;
 # do not broaden that matcher or synthesize a native process identity.
 before="factory=inspect.getsource(executed.bindings)"
 insertion="""factory=inspect.getsource(executed.bindings)
 factory=factory.replace("source=inspect.getsource(prior.capture)",
  "source=inspect.getsource(prior.capture).replace('jobs=census();matches=', 'jobs=census();(out/\\\"live_census.json\\\").write_text(json.dumps(jobs,indent=2)+chr(10));matches=')",1)
 """
 need(source.count(before)==1,'Actual census addition at terminal-first transport binding')
 source=source.replace(before,insertion,1)
 before='Path(executed.__file__),Path(qualified.__file__),Path(__file__)'
 need(source.count(before)==1,'Pin actually used preceding candidate collector')
 source=source.replace(before,'Path(executed.__file__),Path(qualified.__file__),ROOT/\\\"tools/capture_repaired_challenger_v6510.py\\\",Path(__file__)',1)
 scope=dict(prior.__dict__,__file__=__file__,prior=prior)
 exec(compile(source,__file__+'::whole_original_matcher_plus_actual_census','exec'),scope)
 scope['capture'](fighter,side)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));parser.add_argument('--side',required=True,type=int,choices=(1,2))
 a=parser.parse_args();capture(a.fighter,a.side)
