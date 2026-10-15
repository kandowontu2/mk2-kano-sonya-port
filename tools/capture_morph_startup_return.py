"""Cold native morph startup/return capture, terminal-first and RAM-only."""
import argparse,code,inspect,json,traceback
import capture_launch_interruption_v6681 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=inspect.getsource(original.run)
changes=[('audit_v6682_launch_interrupt_','audit_morph_startup_return_'),
 ("MK2PORT_ACCEPT_VICTIM='sub_zero',MK2PORT_INTERRUPT_DELAY=str(delay)","MK2PORT_ACCEPT_VICTIM='sub_zero',MK2PORT_INTERRUPT_DELAY=str(delay),MK2KS_HUMAN_SHANG_SIDE=str(side),MK2KS_HUMAN_SHANG_TARGET='kano'if move=='ball'else'sonya',MK2KS_MORPH_ADVERSITY_PHASE='formed',MK2KS_MORPH_ADVERSITY_FORM='added',MK2KS_MORPH_CAPTURE_OUT=str(folder)"),
 ('Path(__file__),Path(current.__file__)',"Path(__file__),Path(original.__file__),ROOT/'mk2ks_morph_adversity_v3215.lua',ROOT/'mk2ks_launch_interrupt_v6680.lua',ROOT/'mk2ks_launch_ko_round.lua',Path(current.__file__)"),
 ("carrier['rgb'].append(head)","carrier['rgb'].append(head);carrier.setdefault('rgbFrames',[]).append(dict(header=dict(head),pixels=raw))")]
for before,after in changes:need(source.count(before)==1,'Whole terminal-first collector with exact morph route binding');source=source.replace(before,after,1)
scope=dict(vars(original),__file__=__file__,original=original,LUA=ROOT/'mk2ks_morph_startup_return.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::whole_native_terminal_first_RAM_transport','exec'),scope)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--move',choices=('ball','square'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:scope['run'](args.move,args.side,1)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if scope['LAST_CAPTURE']:code.interact(banner='Same terminal native morph/startup buffers; no replay.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
