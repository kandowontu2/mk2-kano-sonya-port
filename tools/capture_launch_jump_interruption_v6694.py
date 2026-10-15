"""Entire existing terminal-first RAM collector, distinct physical jump inputs."""
import argparse,code,inspect,json,traceback
from pathlib import Path
import capture_launch_interruption_v6681 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=inspect.getsource(original.run)
for before,after in [('audit_v6682_launch_interrupt_','audit_v6695_launch_jump_interrupt_'),
 ('Path(__file__),Path(current.__file__)',"Path(__file__),Path(original.__file__),ROOT/'mk2ks_launch_interrupt_v6680.lua',ROOT/'mk2ks_launch_precrouch_v6683.lua',Path(current.__file__)")]:
 need(source.count(before)==1,'Exact fresh collector leaf or executed-source pin');source=source.replace(before,after,1)
scope=dict(original.__dict__,__file__=__file__,original=original,LUA=ROOT/'mk2ks_launch_jump_interrupt_v6693.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::entire_terminal_collector_actual_jump_inputs','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=('ball','square','bicycle'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--delay',type=int,default=1);parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:scope['run'](args.move,args.side,args.delay)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if args.hold and scope['LAST_CAPTURE']:
  code.interact(banner='Same terminal physical jump attempt; complete native buffers remain RAM-only.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
