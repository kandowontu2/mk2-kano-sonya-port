"""Same full terminal-first RAM capture, real original low-fireball input."""
import argparse,code,json,traceback
import capture_launch_fireball_counter as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=original.source
for before,after in [('audit_launch_fireball_counter_','audit_launch_low_fireball_counter_'),
 ('Path(__file__),Path(original.__file__)',"Path(__file__),Path(original.__file__),ROOT/'tools/capture_launch_fireball_counter.py',ROOT/'mk2ks_launch_fireball_counter.lua'")]:
 need(source.count(before)==1,'Only fresh real controller leaf and complete source pins');source=source.replace(before,after,1)
scope=dict(original.scope,__file__=__file__,LUA=ROOT/'mk2ks_launch_low_fireball_counter.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_collector_actual_low_fireball','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--delay',type=int,default=16);parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:scope['run']('ball',args.side,args.delay)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if args.hold and scope['LAST_CAPTURE']:
  code.interact(banner='Same terminal native low-fireball counter; all buffers RAM-only.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
