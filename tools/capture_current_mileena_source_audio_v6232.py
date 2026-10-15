"""Entire6230 collector with actual6103 lifecycle references/global refill.

Preserve initial post-native host failures. Source6093 correctly identifies
the original global refill's P2 register context, not winning-actor ownership.
"""
import argparse,inspect,json,traceback
from pathlib import Path
from types import SimpleNamespace
import capture_current_mileena_source_audio_v6230 as prior
import current_mileena_global_refill_v6093 as global_health
import qualify_current_mileena_matrix_v6100 as matrix
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
health=SimpleNamespace(**dict(vars(global_health),original=prior.health.original))

def state(text,fighter,side,guest):
 native=health.gate(health.original.parse(text),fighter,side,guest)
 need(native['passed'],'Entire current native global refill/earned/stream/cleanup state '+repr(native['errors']))
 leaf=next(leaf for f,s,leaf in matrix.CONTEXTS if(f,s)==(fighter,side))
 reference=ROOT/leaf/'run.log'
 rows=lambda value:[s.strip()for s in value.splitlines()if s.startswith(('MK2_MILEENA_V3784_','MK2_CACHE_V3823_'))]
 actual=rows(text);expected=rows(reference.read_text())
 need(actual==expected,'Every actual controller/health/task/cache/cleanup event equals current6103-qualified lifecycle')
 return dict(native,nativeStateRows=len(actual),sourceQualifiedCurrentLifecycle=str(reference))

def run(fighter,side):
 guest=prior.original.current.expected()
 leaf=next(leaf for f,s,leaf in matrix.CONTEXTS if(f,s)==(fighter,side))
 reference=ROOT/leaf/'run.log';need(reference.exists(),'Actual current qualified lifecycle before native boot')
 proofpath=ROOT/'audit_v6103_current_mileena_lifecycle_checked/report.json';proof=json.loads(proofpath.read_text())
 need(proof['passed'],'Complete source-qualified current four-case lifecycle prerequisite')
 state(reference.read_text(),fighter,side,guest)
 code=inspect.getsource(prior.run)
 def replace(before,after):
  nonlocal code
  need(code.count(before)==1,'One complete current lifecycle binding correction')
  code=code.replace(before,after,1)
 replace('audit_v6231_current_mileena_','audit_v6233_current_mileena_')
 replace('Path(health.__file__),Path(health.original.__file__),',
         'Path(prior.__file__),Path(matrix.__file__),proofpath,Path(health.__file__),Path(global_health.prior.__file__),Path(health.original.__file__),')
 replace('LUA=LUA,PARENT=PARENT,state=state,dac_models=dac_models)',
         'LUA=LUA,PARENT=PARENT,state=state,dac_models=dac_models,prior=prior,matrix=matrix,proofpath=proofpath,global_health=global_health)')
 scope=dict(vars(prior),__file__=__file__,prior=prior,health=health,state=state,matrix=matrix,
            proofpath=proofpath,global_health=global_health)
 exec(compile(code,__file__+'::whole6230_source_qualified_current_lifecycle','exec'),scope)
 return scope['run'](fighter,side)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:run(args.fighter,args.side)
 except Exception as error:
  folder=ROOT/f'audit_v6233_current_mileena_{args.fighter}_p{args.side}_native_audio'
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():prior.original.save(folder/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
