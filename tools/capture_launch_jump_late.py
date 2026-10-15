"""Whole terminal-first RAM capture, later actual Bicycle jump/kick route."""
import argparse,code,json,traceback
import capture_launch_jump_io as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=original.source
for before,after in [('audit_launch_jump_io_','audit_launch_jump_late_'),
 ('Path(__file__),Path(original.__file__)',"Path(__file__),Path(original.__file__),ROOT/'tools/capture_launch_jump_io.py'")]:
 need(source.count(before)==1,'Fresh actual controller leaf and source pins');source=source.replace(before,after,1)
scope=dict(original.scope,__file__=__file__,LUA=ROOT/'mk2ks_launch_jump_late.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_collector_later_real_jump_route','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--delay',type=int,default=1);parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:scope['run']('bicycle',args.side,args.delay)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if args.hold and scope['LAST_CAPTURE']:
  code.interact(banner='Same terminal later native jump/kick; all buffers RAM-only.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
