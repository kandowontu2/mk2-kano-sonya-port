"""Same current native long-match capture, legitimate human jump/backstep policy.

No move/character/RNG/HP state change. Reuse the complete original observers,
collector and all-mode state/health/native-choice contracts with a fresh leaf.
"""
import inspect
from pathlib import Path
import capture_current_kano_cpu_extended_v6292 as prior
need=prior.need


def capture():
 source=inspect.getsource(prior.capture)
 changes={
  "MK2KS_CPU_CONTINUATION_POLICY='retreat'":"MK2KS_CPU_CONTINUATION_POLICY='jump_guard'",
  'audit_v6293_current_kano_cpu_extended_ram':'audit_v6301_current_kano_cpu_jump_guard_ram',
  'Path(model.__file__).resolve(),':'ROOT/"tools/capture_current_kano_cpu_extended_v6292.py",Path(model.__file__).resolve(),',
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Only current physical policy, fresh evidence path and source pin change')
  source=source.replace(before,after,1)
 namespace=dict(prior.capture.__globals__,__file__=__file__)
 exec(compile(source,__file__+'::whole_current_native_collector_human_jump_guard','exec'),namespace)
 return namespace['capture']()


if __name__=='__main__':capture()
