"""Unstarted cases retain their actual full-screen bytes in RAM, never files."""
import argparse,code,json,traceback
import capture_launch_challenger_transition_v2 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
source=previous.source.replace('audit_launch_challenger_transition_v2_','audit_launch_challenger_transition_rgb_',1)
before="carrier['rgb'].append(head)";need(source.count(before)==1,'Whole actual RGB admission hook')
source=source.replace(before,"carrier['rgb'].append(head);carrier.setdefault('rgbFrames',[]).append(dict(header=dict(head),pixels=raw))",1)
source=source.replace('Path(__file__),Path(original.__file__),','Path(__file__),Path(original.__file__),ROOT/\'tools/capture_launch_challenger_transition_v2.py\',',1)
scope=dict(previous.scope,__file__=__file__,original=previous.original,LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_native_transport_plus_RAM_screen_retention','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=('ball','square'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);a=parser.parse_args()
 try:scope['run'](a.move,a.side,1)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if scope['LAST_CAPTURE']:code.interact(banner='Same-terminal live-startup transition with full actual RGB held in RAM.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
