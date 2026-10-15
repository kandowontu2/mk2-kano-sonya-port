"""Expanded passive window, not a replay of the old missing-marker capture."""
import code,inspect,json,traceback
import capture_launch_challenger_transition_rgb as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
source=previous.source
before='audit_launch_challenger_transition_rgb_';need(source.count(before)==1,'Fresh expanded-observer context')
source=source.replace(before,'audit_launch_challenger_fullcold_',1)
before='Path(__file__),Path(original.__file__),';need(source.count(before)==1,'Pin all generated collector parents')
source=source.replace(before,"Path(__file__),Path(previous.__file__),Path(original.__file__),ROOT/'tools/capture_launch_challenger_transition.py',ROOT/'mk2ks_launch_challenger_transition_v2.lua',",1)
scope=dict(previous.scope,__file__=__file__,previous=previous,LUA=ROOT/'mk2ks_launch_challenger_fullcold.lua',LAST_CAPTURE=None)
exec(compile(source,__file__+'::same_controls_fullcold_terminal_first_RAM_transport','exec'),scope)
if __name__=='__main__':
 try:scope['run']('ball',2,1)
 except Exception as error:print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)),flush=True)
 if scope['LAST_CAPTURE']:code.interact(banner='Same terminal expanded CPU-source observation; original narrower capture retained.',local=dict(capture=scope['LAST_CAPTURE'],module=__import__(__name__)))
