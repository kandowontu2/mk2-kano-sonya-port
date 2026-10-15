"""Actual compiler qualification of the missing child/guard observer coverage.

Entire original passive allocation, every child field, damage, tested victim
guard and native retirement, without another controller or any guest write.
Compilation alone is explicitly NOT gameplay or child ownership acceptance.
"""
import inspect
import json
from pathlib import Path
import capture_native_kano_laser_cpu_choke_shadow as source
import capture_native_kano_laser_cpu_leg_repeat_p2 as physical

ROOT,need,sha,once=physical.ROOT,physical.need,physical.sha,physical.once
GUARD=ROOT/'audit_native_kano_laser_cpu_leg_children_source'
LUA=ROOT/'mk2ks_native_kano_laser_cpu_leg_children.lua'


def child_expected(name):
    text=(ROOT/name).read_text()
    if name=='mk2ks_physical_p2_cpu_overlap_trace_v1999.lua':
        text=once(text,"dofile('mk2ks_physical_p2_cpu_round_trace_v1998.lua')",'-- Existing physical/body/channel root already loaded; no second controller.')
        text=once(text,"if cycle==2 and frame%10==0 then manager.machine.screens[':screen']:snapshot('overlap_'..frame..'.png')end",'-- Original native scenes remain in the existing RAM-only observer; no legacy files.')
    else:
        text=once(text,"dofile('mk2ks_physical_p2_cpu_overlap_trace_v1999.lua')",'-- Complete original passive child observer already loaded above.')
    return text


def run():
    text=inspect.getsource(source.qualify)
    text=once(text,"ROOT/'mk2ks_native_kano_laser_cpu_choke_parse.lua'","ROOT/'mk2ks_native_kano_laser_cpu_leg_children_parse.lua'")
    text=once(text,"pins={str(p.resolve()):sha(p)for p in paths}",
              "paths.extend([ROOT/'mk2ks_native_kano_laser_cpu_leg_repeat_p2.lua',ROOT/'mk2ks_physical_p2_cpu_overlap_trace_v1999.lua',ROOT/'mk2ks_physical_p2_cpu_ring_trace_v2013.lua',Path(physical.__file__),Path(source_module_file)]);pins={str(p.resolve()):sha(p)for p in paths}")
    text=once(text,'len(rows)==len(expanded)==4','len(rows)==len(expanded)==7')
    text=once(text,"original=(ROOT/'mk2ks_cpu_recovery_probe_v1438.lua').read_text()","original=physical.repeat_expected()")
    text=once(text,"expanded['wrapper']==(ROOT/'mk2ks_cpu_choke_shadow_v5328.lua').read_text()","expanded['wrapper']==physical.wrapper_expected()")
    before="need(all(not re.search(r':write_|write_[ui]\\d+|load_?state|\\.value\\s*=(?!=)',s)for s in expanded.values()),'No guest/item/register/state writes')"
    after="""need(expanded['root_p2']==(ROOT/'mk2ks_native_kano_laser_cpu_leg_repeat_p2.lua').read_text(),'Entire existing P2 CPU physical/body/channel root')
    need(expanded['child_overlap']==child_expected('mk2ks_physical_p2_cpu_overlap_trace_v1999.lua') and expanded['child_guard']==child_expected('mk2ks_physical_p2_cpu_ring_trace_v2013.lua'),'Both entire actual passive child/guard observers, only two loader hooks and one no-file snapshot')
    need(all(not re.search(r':write_|write_[ui]\\d+|load_?state|\\.value\\s*=(?!=)',s)for s in expanded.values()),'No guest/item/register/state writes')"""
    text=once(text,before,after)
    text=once(text,'wholePhysicalCPUUnchangedExceptSixSinks=True,',
              'wholePhysicalInputLogicConservedFiveObservationChangesSixRAMSinks=True,wholePassiveChildGuardObserversConserved=True,childGameplayAccepted=False,')
    scope=dict(vars(source),GUARD=GUARD,LUA=LUA,__file__=__file__,physical=physical,
               child_expected=child_expected,source_module_file=source.__file__)
    exec(compile(text,__file__+'::entire_native_compiler_all_seven_full_actual_expansions','exec'),scope)
    guard=scope['qualify']()
    print(json.dumps(dict(passed=guard['passed'],actualNativeParserAccepted=True,fullActualExpansions=7,
                         gameplayAccepted=False,childGameplayAccepted=False,newBuilds=0,publicPlayableChanged=False)),flush=True)


if __name__=='__main__':run()
