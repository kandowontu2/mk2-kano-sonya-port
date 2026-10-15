"""Keep native zero ramp rows when the corresponding name row is empty.

Match the actual C++ guard: a nonzero ramp is required only for face pixels.
The original failed reconstruction remains unchanged.
"""
import inspect
from pathlib import Path
import launch_ground_native_names as previous
need,sha,ROOT=previous.need,previous.sha,previous.ROOT
source=inspect.getsource(previous.reconstruct)
old="  need(best!=0,'Actual original native HUD gold ramp');ramp.append(best)"
need(source.count(old)==1,'Exact previously overbroad host-only guard')
source=source.replace(old,'  ramp.append(best)')
old="    pen=ramp[y]if face(x,y)else 2 if x and(face(x-1,y)or(y and face(x-1,y-1)))else 0"
need(source.count(old)==1,'Exact native face guard insertion')
source=source.replace(old,"    need(not face(x,y) or ramp[y]!=0,'Actual native HUD face has gold ramp')\n"+old)
scope=dict(vars(previous));exec(compile(source,__file__+'::exact_native_face_guard','exec'),scope)
reconstruct=scope['reconstruct']
source=inspect.getsource(previous.continue_remaining)
source=source.replace("(Path(__file__),Path(base.__file__),Path(previous.__file__))", "(Path(__file__),Path(base.__file__),Path(previous.__file__),Path(name_adapter.__file__))")
scope.update(__file__=__file__,name_adapter=previous)
exec(compile(source,__file__+'::same_terminal_then_unstarted_cases','exec'),scope)
continue_remaining=scope['continue_remaining']
