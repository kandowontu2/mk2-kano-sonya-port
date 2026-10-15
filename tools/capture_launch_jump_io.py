"""Reuse the whole RAM-only terminal-first collector with real jump-kick inputs."""
import argparse,code,json,traceback
import capture_launch_ground_io_fixed_v6710 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=original.source
for before,after in [('audit_v6711_launch_ground_io_fixed_','audit_launch_jump_io_'),
 ('Path(__file__),Path(original.__file__)',"Path(__file__),Path(original.__file__),ROOT/'tools/capture_launch_ground_io_fixed_v6710.py',ROOT/'mk2ks_launch_jump_interrupt_v6693.lua'")]:
 need(source.count(before)==1,'Fresh capture leaf and complete actual executed sources');source=source.replace(before,after,1)
scope=dict(original.scope,__file__=__file__,LUA=ROOT/'mk2ks_launch_jump_io.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_collector_correct_jump_input_ports','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=('ball','bicycle'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--delay',type=int,required=True);parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:scope['run'](args.move,args.side,args.delay)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if args.hold and scope['LAST_CAPTURE']:
  code.interact(banner='Same terminal jump/kick test; complete native buffers remain RAM-only.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
