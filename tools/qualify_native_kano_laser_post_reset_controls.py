"""Whole original adaptive control policy at actual native next-round handoff.

Native-compile all eleven full expansions, preserve every passive observer,
qualify unchanged actual response/retry/survival logic. Human buttons only;
compile qualification never claims gameplay/control/render acceptance.
"""
import inspect
import json
import re
from pathlib import Path
import qualify_native_kano_laser_cpu_post_ko as previous

ROOT,need,sha,once,source=previous.ROOT,previous.need,previous.sha,previous.once,previous.source
LUA=ROOT/'mk2ks_native_kano_laser_post_reset_controls.lua'
GUARD=ROOT/'audit_native_kano_laser_post_reset_controls_source'


def slice_source(text,first,last):
    need(text.count(first)==1,'Exact original source slice start '+first)
    a=text.index(first);b=text.index(last,a+len(first));return text[a:b]


def expected():
    wanted=previous.expected()
    wanted['physical']=once(wanted['physical'],
        'if complete_count>=2 and frame>=last_complete+30 then manager.machine:exit()end',
        '-- The actual post-reset adaptive control/recovery deadline owns observation exit.')
    root=previous.LUA.read_text()
    root=once(root,"resumed=frame;log('RESUMED','actual_native_full_health_round')",
        "resumed=frame;MK2_POST_CTRL_READY=frame;log('RESUMED','actual_native_full_health_round')")
    root=once(root,"if resumed and frame>=resumed+60 then terminal=true;log('END','sixty_actual_post_reset_fields');manager.machine:exit()end",
        "if MK2_POST_CTRL_RECOVERED and frame>=MK2_POST_CTRL_RECOVERED+180 then terminal=true;MK2_POST_CTRL_EXIT_PENDING=true;log('END','actual_control_recovery_plus_180_fields');manager.machine:exit()end")
    wanted['root_post']=root
    original=(ROOT/'mk2ks_single_continue_v6567.lua').read_text()
    wrapper=LUA.read_text()
    literals=re.findall(r'prefix=prefix\.\.\[\[(.*?)\]\]',wrapper,re.S)
    need(len(literals)==2,'Both exact declared adaptive bindings/frame wrapper literals')
    first=wrapper.index('prefix=prefix..whole_original_controls..[[')+len('prefix=prefix..whole_original_controls..[[')
    last=wrapper.index(']]',first)
    adaptive=(ROOT/'mk2ks_single_continue_controls_v6579.lua').read_text()
    a=adaptive.index('local after=[[')+len('local after=[[');b=adaptive.index(']]',a)
    controller=once(adaptive[a:b],'if frame-recover>=180 then manager.machine:exit()end',
        '-- Original recovery+180 exit is handled by the shared native post-KO observer.')
    # Lua long brackets discard one initial newline. Account for that exact
    # language rule in each independently source-derived literal.
    literal=lambda s:s[1:]if s.startswith('\n')else s
    wanted['post_controls']=(slice_source(original,'local p=manager.machine.devices','local buttons={}')+
        literal(literals[0])+slice_source(original,'local function valid(a)','local adjacency=')+
        slice_source(original,'local function sample(n)','local function snap(label)')+
        literal(literals[1])+literal(controller)+literal(wrapper[first:last]))
    return wanted


def run():
    wanted=expected()
    text=inspect.getsource(source.qualify)
    text=once(text,"ROOT/'mk2ks_native_kano_laser_cpu_choke_parse.lua'","ROOT/'mk2ks_native_kano_laser_post_reset_controls_parse.lua'")
    text=once(text,'pins={str(p.resolve()):sha(p)for p in paths}',
        "paths.extend([Path(previous.__file__),previous.LUA,previous.previous.GUARD/'report.json',previous.previous.GUARD/'native_stdout.log.gz',ROOT/'mk2ks_native_kano_laser_cpu_leg_children.lua',ROOT/'mk2ks_native_kano_laser_cpu_leg_repeat_p2.lua',ROOT/'mk2ks_physical_p2_cpu_overlap_trace_v1999.lua',ROOT/'mk2ks_physical_p2_cpu_ring_trace_v2013.lua',ROOT/'mk2ks_physical_p2_cpu_round_trace_v1998.lua',ROOT/'mk2ks_single_continue_v6567.lua',ROOT/'mk2ks_single_continue_controls_v6579.lua']);pins={str(p.resolve()):sha(p)for p in paths}")
    text=once(text,'len(rows)==len(expanded)==4','len(rows)==len(expanded)==11')
    a=text.index("    original=(ROOT/'mk2ks_cpu_recovery_probe_v1438.lua').read_text()")
    b=text.index('    need(all(not re.search',a)
    text=once(text,text[a:b],
        "    need(expanded==wanted,'Every entire actual native expansion conserves original observers and adaptive response/retry/survival; only declared reset handoff/deadline differs')\n")
    text=once(text,'wholePhysicalCPUUnchangedExceptSixSinks=True,',
        'wholeOriginalAdaptiveActualResponseLogicConserved=True,wholePassiveChildRoundChannelObserversConserved=True,physicalHumanPolicyHandoffAfterNativeReset=True,')
    scope=dict(vars(source),GUARD=GUARD,LUA=LUA,__file__=__file__,previous=previous,wanted=wanted)
    exec(compile(text,__file__+'::whole_actual_native_eleven_expansion_control_qualification','exec'),scope)
    guard=scope['qualify']()
    print(json.dumps(dict(passed=guard['passed'],actualFullExpansions=11,
                         gameplayAccepted=False,postResetControlsAccepted=False,newBuilds=0)),flush=True)


if __name__=='__main__':run()
