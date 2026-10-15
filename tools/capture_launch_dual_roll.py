"""Entire terminal-first collector, actual two-human Kano mirror rolls."""
import argparse,code,json,traceback
import capture_launch_interruption_v6681 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
import inspect
source=inspect.getsource(original.run)
for before,after in [('audit_v6682_launch_interrupt_','audit_launch_dual_roll_'),
 ("MK2PORT_ACCEPT_VICTIM='sub_zero'","MK2PORT_ACCEPT_VICTIM='kano'"),
 ('Path(__file__),Path(current.__file__)','Path(__file__),Path(original.__file__),Path(current.__file__)')]:
 need(source.count(before)==1,'Fresh mirror route and exact executed source pins');source=source.replace(before,after,1)
scope=dict(vars(original),__file__=__file__,original=original,LUA=ROOT/'mk2ks_launch_dual_roll.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_terminal_collector_actual_dual_roll','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:scope['run']('ball',args.side,1)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if args.hold and scope['LAST_CAPTURE']:
  code.interact(banner='Same terminal two-human rolls; full native transport remains RAM-only.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
