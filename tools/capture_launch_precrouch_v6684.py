"""Same entire terminal-first collector; physical pre-crouch is a new input route.

Earlier four actual terminal attempts remain unexercised for interruption.
This is not a restart of those handles or a forced state/health/position hit.
"""
import argparse,code,inspect,json,traceback
from pathlib import Path
import capture_launch_interruption_v6681 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=inspect.getsource(original.run)
before='audit_v6682_launch_interrupt_'
need(source.count(before)==1,'Fresh distinct physical-input capture leaf')
source=source.replace(before,'audit_v6685_launch_precrouch_',1)
before='Path(__file__),Path(current.__file__)'
need(source.count(before)==1,'Both complete observer/controller and original capture source pinned')
source=source.replace(before,"Path(__file__),Path(original.__file__),ROOT/'mk2ks_launch_interrupt_v6680.lua',Path(current.__file__)",1)
scope=dict(original.__dict__,__file__=__file__,original=original,LUA=ROOT/'mk2ks_launch_precrouch_v6683.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_collector_new_actual_precrouch_inputs','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=('ball','square','bicycle'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--delay',type=int,default=1);parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:scope['run'](args.move,args.side,args.delay)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if args.hold and scope['LAST_CAPTURE']:
  code.interact(banner='Same actual terminal pre-crouch attempt; entire native buffers remain RAM-only. No replay.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
