"""Same full terminal-first collector, real blocked-roll rebound counter."""
import argparse,code,json,traceback
import capture_launch_ground_io_fixed_v6710 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=original.source
for before,after in [('audit_v6711_launch_ground_io_fixed_','audit_v6718_roll_block_counter_'),
 ('Path(__file__),Path(original.__file__)',"Path(__file__),Path(original.__file__),ROOT/'tools/capture_launch_ground_io_fixed_v6710.py'")]:
 need(source.count(before)==1,'Only fresh actual controller leaf or complete executed source pin');source=source.replace(before,after,1)
scope=dict(original.scope,__file__=__file__,LUA=ROOT/'mk2ks_roll_block_counter_v6716.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::entire_collector_actual_stock_block_then_counter','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--delay',type=int,default=24);parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:scope['run']('ball',args.side,args.delay)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if args.hold and scope['LAST_CAPTURE']:
  code.interact(banner='Same terminal stock guard/rebound counter; entire native buffers RAM-only.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
