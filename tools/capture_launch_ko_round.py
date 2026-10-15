"""Same terminal-first collector for actual collision-earned KO/round reset."""
import argparse,code,inspect,json,traceback
import capture_launch_interruption_v6681 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=inspect.getsource(original.run)
for before,after in [('audit_v6682_launch_interrupt_','audit_launch_ko_round_'),
 ("MK2PORT_ACCEPT_VICTIM='sub_zero'","MK2PORT_ACCEPT_VICTIM='kano'"),
 ('Path(__file__),Path(current.__file__)','Path(__file__),Path(original.__file__),ROOT/\'mk2ks_launch_dual_roll.lua\',ROOT/\'mk2ks_launch_interrupt_v6680.lua\',Path(current.__file__)')]:
 need(source.count(before)==1,'Exact new physical task and full source pins');source=source.replace(before,after,1)
scope=dict(vars(original),__file__=__file__,original=original,LUA=ROOT/'mk2ks_launch_ko_round.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_actual_terminal_collector_KO_round','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:scope['run']('ball',args.side,1)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if scope['LAST_CAPTURE']:
  code.interact(banner='Same actual KO/reset terminal carriers in RAM; no replay.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
