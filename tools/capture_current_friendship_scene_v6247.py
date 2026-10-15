"""Keep full6245 capture; correct exact original parser RAM spelling only.

The original parser uses path.read_text, not Path(path).read_text. Preserve
the executed6245 source/attempt; existing complete frames require no rerun.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_friendship_scene_v6245 as prior
ROOT,need=prior.ROOT,prior.need

def run(fighter,side):
 source=inspect.getsource(prior.run)
 before='before="Path(path).read_text(encoding=\'utf-8-sig\')"'
 after='before="path.read_text(encoding=\'utf-8-sig\')"'
 need(source.count(before)==1,'Exactly original parser RAM-routing spelling corrected')
 source=source.replace(before,after,1)
 before='audit_v6246_current_';need(source.count(before)==1,'Fresh successor output only')
 source=source.replace(before,'audit_v6248_current_',1)
 before='files=[LUA,Path(__file__).resolve(),Path(current.__file__),'
 need(source.count(before)==1,'Preserve full executed original capture source as input')
 source=source.replace(before,'files=[LUA,Path(__file__).resolve(),Path(prior.__file__),Path(current.__file__),',1)
 namespace=dict(vars(prior),__file__=__file__,prior=prior)
 exec(compile(source,__file__+'::whole6245_original_parser_RAM_correction','exec'),namespace)
 return namespace['run'](fighter,side)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:run(args.fighter,args.side)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  folder=ROOT/f'audit_v6248_current_{args.fighter}_friendship_scene_p{args.side}'
  if folder.exists():prior.save(folder/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
