"""Add actual native pool/attachment/retirement taps, not another build.

Entire terminal-first6313 collector and qualified physical blade/knife gate.
Original2892 observer reused unchanged after its old driver preamble only.
Natural terminal and complete old chronology required before qualification.
"""
import inspect,json
from pathlib import Path
import capture_current_cpu_blade_knife_shadow_v6313 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
FOLDER=ROOT/'audit_v6332_current_cpu_blade_allocation_ram'
LUA=ROOT/'mk2ks_current_cpu_blade_allocation_v6330.lua'


def main():
 baseline=ROOT/'audit_v2912_blade_allocation_checked/report.json'
 proof=json.loads(baseline.read_text());observer=ROOT/'mk2ks_blade_allocation_v2892.lua'
 need(proof['passed'] and sha(observer)==proof['inputHashes'][str(observer)],
      'Whole original actual allocator observer unchanged and previously qualified')
 need(not prior.terminal.process_tools.census(),'Actual native census empty before new cold run')
 source=inspect.getsource(prior.capture)
 before="for p in (ROOT/'mk2ks_special_shadow_v5131.lua',"
 need(source.count(before)==1,'Explicit additional pins; whole terminal collector unchanged')
 source=source.replace(before,"for p in (baseline,observer,ROOT/'tools/capture_current_cpu_blade_knife_shadow_v6313.py',"+before[len('for p in ('):],1)
 scope=dict(prior.__dict__,__file__=__file__,FOLDER=FOLDER,LUA=LUA,baseline=baseline,observer=observer)
 exec(compile(source,__file__+'::whole_terminal_first_native_allocator_transport','exec'),scope)
 return scope['capture']()


if __name__=='__main__':main()
