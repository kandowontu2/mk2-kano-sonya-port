"""Complete terminal-first Sonya Square KO/reset transport, held in RAM."""
import argparse,code,inspect,json,traceback
import capture_launch_interruption_v6681 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=inspect.getsource(original.run)
for before,after in [('audit_v6682_launch_interrupt_','audit_sonya_launch_ko_round_'),
 ('Path(__file__),Path(current.__file__)',"Path(__file__),Path(original.__file__),ROOT/'mk2ks_launch_ko_round.lua',ROOT/'mk2ks_launch_interrupt_v6680.lua',ROOT/'mk2ks_launch_precrouch_v6683.lua',ROOT/'mk2ks_launch_jump_interrupt_v6693.lua',Path(current.__file__)")]:
 need(source.count(before)==1,'Exact fresh case and full actual source pins');source=source.replace(before,after,1)
scope=dict(vars(original),__file__=__file__,original=original,LUA=ROOT/'mk2ks_sonya_launch_ko_round.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_terminal_first_Sonya_KO_transport','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:scope['run']('square',args.side,1)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if scope['LAST_CAPTURE']:code.interact(banner='Same terminal Sonya KO/reset native buffers remain RAM-only; no replay.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
