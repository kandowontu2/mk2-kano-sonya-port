"""Keep prelaunch6331 rejection; use literal pins in collector namespace."""
import inspect,json
from pathlib import Path
import capture_current_cpu_blade_allocation_v6331 as prior
ROOT,need=prior.ROOT,prior.need


def main():
 failure=ROOT/'audit_v6335_current_cpu_blade_allocator_prelaunch/failure.json'
 need(not json.loads(failure.read_text())['startedNativeProcess'] and not prior.FOLDER.exists(),
      'Original namespace failure occurred before any native launch or capture folder')
 source=inspect.getsource(prior.main)
 before='"for p in (baseline,observer,ROOT/\'tools/capture_current_cpu_blade_knife_shadow_v6313.py\','
 after='"for p in (ROOT/\'audit_v6335_current_cpu_blade_allocator_prelaunch/failure.json\',ROOT/\'tools/capture_current_cpu_blade_allocation_v6331.py\',ROOT/\'audit_v2912_blade_allocation_checked/report.json\',ROOT/\'mk2ks_blade_allocation_v2892.lua\',ROOT/\'tools/capture_current_cpu_blade_knife_shadow_v6313.py\','
 need(source.count(before)==1,'Exactly one additional-pin namespace repair')
 source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__file__=__file__,FOLDER=ROOT/'audit_v6337_current_cpu_blade_allocation_ram')
 exec(compile(source,__file__+'::unchanged_terminal_capture_with_resolved_pins','exec'),scope)
 return scope['main']()


if __name__=='__main__':main()
