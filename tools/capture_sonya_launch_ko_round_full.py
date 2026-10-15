"""Fresh cold tests after the previous native jobs are actually terminal.

Original partial observer attempts remain untouched. No observation timeout
triggers a restart; correct only a proven Lua substring-return bug.
"""
import argparse,code,inspect,json,traceback
import capture_sonya_launch_ko_round as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=original.source.replace('audit_sonya_launch_ko_round_','audit_sonya_launch_ko_round_full_',1)
source=source.replace('Path(__file__),Path(original.__file__),','Path(__file__),Path(original.__file__),ROOT/\'tools/capture_launch_interruption_v6681.py\',ROOT/\'mk2ks_sonya_launch_ko_round.lua\',',1)
scope=dict(vars(original.original),__file__=__file__,original=original,LUA=ROOT/'mk2ks_sonya_launch_ko_round_full.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_terminal_collector_complete_observer','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:scope['run']('square',args.side,1)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if scope['LAST_CAPTURE']:code.interact(banner='Full same-terminal Sonya KO/reset carriers in RAM.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
