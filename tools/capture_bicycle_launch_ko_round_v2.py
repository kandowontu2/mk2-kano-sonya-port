"""Fresh corrected observer after the first boot's authoritative exit3."""
import argparse,code,json,traceback
import capture_bicycle_launch_ko_round as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=original.source.replace('audit_bicycle_launch_ko_round_','audit_bicycle_launch_ko_round_v2_',1)
source=source.replace('Path(__file__),Path(original.__file__),','Path(__file__),Path(original.__file__),ROOT/\'tools/capture_launch_interruption_v6681.py\',',1)
scope=dict(original.scope,__file__=__file__,original=original,LUA=ROOT/'mk2ks_bicycle_launch_ko_round_v2.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_terminal_first_corrected_Bicycle_KO_transport','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:scope['run']('bicycle',args.side,1)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if scope['LAST_CAPTURE']:code.interact(banner='Same-terminal corrected Bicycle KO/reset RAM carriers.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
