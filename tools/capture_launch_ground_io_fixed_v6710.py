"""Retain actual6708 terminal3, correct only the Lua concatenation operator."""
import argparse,code,json,traceback
import capture_launch_ground_io_v6707 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=original.source
for before,after in [('audit_v6708_launch_ground_io_','audit_v6711_launch_ground_io_fixed_'),
 ('Path(__file__),Path(original.__file__)',"Path(__file__),Path(original.__file__),ROOT/'tools/capture_launch_ground_io_v6707.py',ROOT/'mk2ks_launch_ground_io_v6706.lua'")]:
 need(source.count(before)==1,'Only fresh capture leaf and full executed source pins');source=source.replace(before,after,1)
scope=dict(original.scope,__file__=__file__,LUA=ROOT/'mk2ks_launch_ground_io_fixed_v6709.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_collector_lexical_Lua_correction','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=('ball','bicycle'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--delay',type=int,required=True);parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:scope['run'](args.move,args.side,args.delay)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if args.hold and scope['LAST_CAPTURE']:
  code.interact(banner='Same terminal grounded attempt; complete buffers and actual IN0/IN2 retained RAM-only.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
