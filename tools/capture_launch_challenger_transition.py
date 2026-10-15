"""Whole current terminal-first live-startup challenger transition in RAM."""
import argparse,code,inspect,json,traceback
import capture_launch_interruption_v6681 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=inspect.getsource(original.run)
for before,after in (
 ('audit_v6682_launch_interrupt_','audit_launch_challenger_transition_'),
 ("MK2PORT_ACCEPT_VICTIM='sub_zero',MK2PORT_INTERRUPT_DELAY=str(delay)",
  "MK2PORT_ACCEPT_VICTIM='sub_zero',MK2PORT_INTERRUPT_DELAY=str(delay),MK2PORT_CONTINUE_FIGHTER='kano'if move=='ball'else'sonya',MK2PORT_CONTINUE_SIDE=str(side)"),
 ('Path(__file__),Path(current.__file__)',
  "Path(__file__),Path(original.__file__),ROOT/'mk2ks_current_challenger_v6486.lua',ROOT/'mk2ks_launch_interrupt_v6680.lua',ROOT/'mk2ks_launch_ko_round.lua',Path(current.__file__)")
):
 need(source.count(before)==1,'Exact new challenger route and all executed source pins');source=source.replace(before,after,1)
scope=dict(vars(original),__file__=__file__,original=original,LUA=ROOT/'mk2ks_launch_challenger_transition.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_terminal_first_live_startup_challenger_transport','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=('ball','square'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:scope['run'](args.move,args.side,1)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if scope['LAST_CAPTURE']:code.interact(banner='Same-terminal actual launch/challenger transition RAM buffers.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
