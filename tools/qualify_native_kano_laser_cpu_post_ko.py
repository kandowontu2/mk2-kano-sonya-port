"""Native compile qualification of observation beyond the genuine KO boundary.

Keep all seven prior full expansions; only replace the declared body observer
exit at real KO/noncombat. Add the entire original read-only all-mode/HP-reset
observer and an event-based post-reset observation deadline. No game writes.
"""
import gzip
import inspect
import json
from pathlib import Path
import qualify_native_kano_laser_cpu_leg_children as previous

ROOT,need,sha,once=previous.ROOT,previous.need,previous.sha,previous.once
source=previous.source
GUARD=ROOT/'audit_native_kano_laser_cpu_post_ko_source'
LUA=ROOT/'mk2ks_native_kano_laser_cpu_post_ko.lua'


def expected():
    old=json.loads((previous.GUARD/'report.json').read_text())
    need(old['passed'] and old['actualNativeParserAccepted'] and
         all(sha(p)==h for p,h in old['inputHashes'].items()),
         'Entire original seven actual-native-compiled expansions and their sources conserved')
    with gzip.open(previous.GUARD/'native_stdout.log.gz','rt')as file:text=file.read()
    rows=[dict(source.re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_CS_PARSE_SOURCE ')]
    expanded={r['kind']:bytes.fromhex(r['hex']).decode()for r in rows}
    need(len(rows)==len(expanded)==7,'All original exact whole compiled sources, no truncation')
    root=LUA.read_text()
    marker='source=once(source,"if not pair_live(a,b)then'
    start=root.index(marker)
    before="if not pair_live(a,b)then log('FAILED','reason=lost_owned_pair_at_field_done');manager.machine:exit();return end"
    first=root.index('[[',start)+2;last=root.index(']])',first)
    expanded['body_shadow']=once(expanded['body_shadow'],before,root[first:last])
    expanded['root_children']=(ROOT/'mk2ks_native_kano_laser_cpu_leg_children.lua').read_text()
    expanded['round_observer']=once((ROOT/'mk2ks_physical_p2_cpu_round_trace_v1998.lua').read_text(),
        "dofile('mk2ks_physical_p2_cpu_continuation_v1997.lua')",'-- Existing full physical root already loaded; no second controller.')
    return expanded


def run():
    wanted=expected()
    text=inspect.getsource(source.qualify)
    text=once(text,"ROOT/'mk2ks_native_kano_laser_cpu_choke_parse.lua'","ROOT/'mk2ks_native_kano_laser_cpu_post_ko_parse.lua'")
    text=once(text,'pins={str(p.resolve()):sha(p)for p in paths}',
        "paths.extend([Path(previous.__file__),previous.GUARD/'report.json',previous.GUARD/'native_stdout.log.gz',ROOT/'mk2ks_native_kano_laser_cpu_leg_children.lua',ROOT/'mk2ks_native_kano_laser_cpu_leg_repeat_p2.lua',ROOT/'mk2ks_physical_p2_cpu_overlap_trace_v1999.lua',ROOT/'mk2ks_physical_p2_cpu_ring_trace_v2013.lua',ROOT/'mk2ks_physical_p2_cpu_round_trace_v1998.lua']);pins={str(p.resolve()):sha(p)for p in paths}")
    text=once(text,'len(rows)==len(expanded)==4','len(rows)==len(expanded)==9')
    first=text.index("    original=(ROOT/'mk2ks_cpu_recovery_probe_v1438.lua').read_text()")
    last=text.index("    need(all(not re.search",first)
    text=once(text,text[first:last],
        "    need(expanded==wanted,'Every whole actual-native-compiled expansion equals its exact conserved source plus the one KO boundary adaptation and original passive round observer')\n")
    text=once(text,'wholePhysicalCPUUnchangedExceptSixSinks=True,',
        'wholePhysicalInputLogicConservedFiveObservationChangesSixRAMSinks=True,wholePriorChildAndChannelObserversConserved=True,oneNativeKOBodyObserverBoundaryAdapted=True,wholeOriginalAllModeRoundObserverConserved=True,')
    scope=dict(vars(source),GUARD=GUARD,LUA=LUA,__file__=__file__,previous=previous,wanted=wanted)
    exec(compile(text,__file__+'::entire_actual_native_compiler_nine_complete_observer_expansions','exec'),scope)
    guard=scope['qualify']()
    print(json.dumps(dict(passed=guard['passed'],actualFullNativeExpansions=9,
                         gameplayAccepted=False,postKOAccepted=False,newBuilds=0)),flush=True)


if __name__=='__main__':run()
