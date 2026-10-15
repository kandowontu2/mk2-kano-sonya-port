"""Corrected generated passive observer after the original native exit3."""
import argparse,code,json,traceback
import capture_launch_challenger_transition as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=original.source.replace('audit_launch_challenger_transition_','audit_launch_challenger_transition_v2_',1)
source=source.replace('Path(__file__),Path(original.__file__),','Path(__file__),Path(original.__file__),ROOT/\'tools/capture_launch_interruption_v6681.py\',ROOT/\'mk2ks_launch_challenger_transition.lua\',',1)
scope=dict(original.scope,__file__=__file__,original=original,LUA=ROOT/'mk2ks_launch_challenger_transition_v2.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_corrected_delimiter_terminal_first_transport','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=('ball','square'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);a=parser.parse_args()
 try:scope['run'](a.move,a.side,1)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if scope['LAST_CAPTURE']:code.interact(banner='Same-terminal corrected live-startup challenger RAM carrier.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
