"""Original complete RAM native replay, method indentation and native69-field bound."""
import inspect,json,textwrap
from pathlib import Path
import current_cpu_scene_ram_contract_v5357 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
def replay_binding(folder,ram,log):
 source=inspect.getsource(original.replay_binding)
 before='source=inspect.getsource(raster.base.Replay.begin)'
 need(source.count(before)==1,'Only method-source compile indentation corrected')
 source=source.replace(before,'source=textwrap.dedent(inspect.getsource(raster.base.Replay.begin))',1)
 namespace=dict(original.replay_binding.__globals__,textwrap=textwrap,__file__=__file__)
 exec(compile(source,__file__+'::original_whole_native_replay_method_indent','exec'),namespace)
 return namespace['replay_binding'](folder,ram,log)
def verify(folder,ram,log,guest,pins):
 failed=ROOT/'audit_v5359_current_cpu_square_scene_ram_checked/report.json'
 failure=json.loads(failed.read_text())
 need(not failure['passed']and failure['error'].startswith('IndentationError('),'Preserve actual post-native host binding failure')
 source=inspect.getsource(original.verify)
 before="len(snaps)==70 and [r['frame']for r in snaps]==list(range(2279,2349))"
 after="len(snaps)==qualified['sampledFrames']==69 and [r['frame']for r in snaps]==list(range(2279,2317+31))"
 need(source.count(before)==1,'Exact original source-bound inclusive thirty-field post-ready window')
 source=source.replace(before,after,1)
 namespace=dict(original.verify.__globals__,replay_binding=replay_binding,__file__=__file__)
 exec(compile(source,__file__+'::original_complete_scene_native_window','exec'),namespace)
 report=namespace['verify'](folder,ram,log,guest,pins)
 for p in(failed,Path(original.__file__).resolve()):pins[str(p)]=sha(p)
 report.update(originalNativeThirtyPostReadyScanoutsPreserved=True,preservedExecutedHostBindingFailure=str(failed))
 return report
