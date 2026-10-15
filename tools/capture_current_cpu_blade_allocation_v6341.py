"""Repair observer lifetime only; keep original failed mixed trace untouched."""
import inspect,json
from pathlib import Path
import capture_current_cpu_blade_knife_shadow_v6313 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
FOLDER=ROOT/'audit_v6342_current_cpu_blade_allocation_ram'
LUA=ROOT/'mk2ks_current_cpu_blade_allocation_v6340.lua'


def main():
 baseline=ROOT/'audit_v2912_blade_allocation_checked/report.json'
 proof=json.loads(baseline.read_text());observer=ROOT/'mk2ks_blade_allocation_v2892.lua'
 need(proof['passed'] and sha(observer)==proof['inputHashes'][str(observer)],'Entire original source retained')
 failure=ROOT/'audit_v6339_current_cpu_blade_allocation_checked/failure.json'
 need(not json.loads(failure.read_text())['passed'],'Actual failed old observer interpretation preserved')
 need(not prior.terminal.process_tools.census(),'Previous native job naturally terminal, actual census empty')
 previous=ROOT/'audit_v6337_current_cpu_blade_allocation_ram/native_terminal.json'
 terminal=json.loads(previous.read_text());need(terminal['naturalTerminal'] and terminal['exitCode']==0,'Same old job terminal before successor')
 source=inspect.getsource(prior.capture)
 before="for p in (ROOT/'mk2ks_special_shadow_v5131.lua',"
 need(source.count(before)==1,'Additional source/failure pins only, not physical trajectory')
 source=source.replace(before,"for p in (ROOT/'mk2ks_current_cpu_blade_allocation_v6330.lua',ROOT/'tools/capture_current_cpu_blade_allocation_v6331.py',ROOT/'tools/capture_current_cpu_blade_allocation_v6336.py',ROOT/'tools/verify_current_cpu_blade_allocation_v6333.py',ROOT/'tools/verify_current_cpu_blade_allocation_v6338.py',ROOT/'audit_v6335_current_cpu_blade_allocator_prelaunch/failure.json',ROOT/'audit_v6339_current_cpu_blade_allocation_checked/failure.json',ROOT/'audit_v6337_current_cpu_blade_allocation_ram/result.json',ROOT/'audit_v6337_current_cpu_blade_allocation_ram/native_terminal.json',ROOT/'audit_v6337_current_cpu_blade_allocation_ram/run.log.gz',ROOT/'audit_v2912_blade_allocation_checked/report.json',ROOT/'mk2ks_blade_allocation_v2892.lua',ROOT/'tools/capture_current_cpu_blade_knife_shadow_v6313.py',"+before[len('for p in ('):],1)
 scope=dict(prior.__dict__,__file__=__file__,FOLDER=FOLDER,LUA=LUA)
 exec(compile(source,__file__+'::whole_terminal_capture_with_distinct_effect_lifetimes','exec'),scope)
 return scope['capture']()


if __name__=='__main__':main()
