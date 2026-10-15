"""Fresh capture only after rechecking the previous external game is gone.

The6313 attempt stopped before launch because ordinary v1250 was running.
Never terminate/restart that game; preserve its actual prelaunch rejection.
"""
import inspect,json
from pathlib import Path
import capture_current_cpu_blade_knife_shadow_v6313 as prior
ROOT,need=prior.ROOT,prior.need


def main():
 failure=ROOT/'audit_v6315_current_cpu_shadow_prelaunch_wait/failure.json'
 need(not json.loads(failure.read_text())['startedNativeProcess'],'Original attempt did not launch an emulator')
 need(not prior.terminal.process_tools.census(),'Actual native census empty now, not an assumed terminal')
 source=inspect.getsource(prior.capture)
 before='ROOT/\'mk2ks_special_shadow_v5131.lua\',ROOT/'
 need(source.count(before)==1,'Pin executed original collector and actual prelaunch rejection')
 source=source.replace(before,"ROOT/'tools/capture_current_cpu_blade_knife_shadow_v6313.py',ROOT/'audit_v6315_current_cpu_shadow_prelaunch_wait/failure.json',"+before,1)
 scope=dict(prior.capture.__globals__,__file__=__file__,FOLDER=ROOT/'audit_v6317_current_cpu_blade_knife_shadow_ram')
 exec(compile(source,__file__+'::unchanged_native_shadow_transport_after_actual_census','exec'),scope)
 return scope['capture']()


if __name__=='__main__':main()
