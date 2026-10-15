"""Natural CPU P1 Sonya repeated paired contacts on the current private candidate.

Entire original schema9 physical controller, all repeated-pair choreography,
native flags/state/health, every ready body/shadow, passive nineteen channels.
No CPU choice/state/health/position writes and no release or whole-port claim.
"""
import code
import copy
import gzip
import hashlib
import inspect
import json
import os
import re
import struct
import traceback
from pathlib import Path
from types import SimpleNamespace
import capture_native_kano_laser_cpu_choke_shadow as prior
import verify_repeated_sonya_cpu_v1463 as repeated
import verify_current_cpu_choke_health_shadow_v5333 as complete_health

base=prior.base
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
BASE=ROOT/'audit_native_kano_laser_cpu_leg_repeat_ram'
OUT=ROOT/'audit_native_kano_laser_cpu_leg_repeat_checked'
INIT=ROOT/'audit_native_kano_laser_cpu_leg_repeat_initializer_source'
GUARD=ROOT/'audit_native_kano_laser_cpu_leg_repeat_source'
LUA=ROOT/'mk2ks_native_kano_laser_cpu_leg_repeat.lua'
RAM_CASES={}
COMPLETED=[]


def once(source,before,after):
    return prior.replace_once(source,before,after)


def wrapper_expected():
    source=(ROOT/'mk2ks_cpu_choke_shadow_v5328.lua').read_text()
    for before,after in (
        ("local move,side,attempt,air='choke',2,1,false","local move,side,attempt,air='leg',1,1,false"),
        ("local expected={human=='kano'and 17 or 18,17}","local expected={18,human=='kano'and 17 or 18}"),
        ('a.state==1 and b.state==0','a.state==0 and b.state==1')):
        source=once(source,before,after)
    need(source.count('mk2ks_cpu_recovery_probe_v1438.lua')==2,'Only file read/compiler labels')
    return source.replace('mk2ks_cpu_recovery_probe_v1438.lua','mk2ks_cpu_recovery_probe_v1459.lua')


def qualify():
    source=inspect.getsource(prior.qualify)
    source=once(source,"ROOT/'mk2ks_native_kano_laser_cpu_choke_parse.lua'","ROOT/'mk2ks_native_kano_laser_cpu_leg_repeat_parse.lua'")
    need(source.count('mk2ks_cpu_recovery_probe_v1438.lua')==2,'Exact original physical path and whole-source expectation')
    source=source.replace('mk2ks_cpu_recovery_probe_v1438.lua','mk2ks_cpu_recovery_probe_v1459.lua')
    source=once(source,"expanded['wrapper']==(ROOT/'mk2ks_cpu_choke_shadow_v5328.lua').read_text()","expanded['wrapper']==wrapper_expected()")
    scope=dict(vars(prior),GUARD=GUARD,LUA=LUA,__file__=__file__,wrapper_expected=wrapper_expected)
    exec(compile(source,__file__+'::whole_native_parser_and_byte_exact_physical_qualification','exec'),scope)
    guard=scope['qualify']()
    need(guard['passed'],'Actual native parser qualification')
    return guard


def physical_bindings(guest):
    # The modified current helper code must match independently reconstructed
    # current instructions, not a stale stock-ROM image. All other typed gates
    # remain the complete original repeated-contact checker.
    scope=dict(vars(repeated),CURRENT_GUEST=guest)
    source=inspect.getsource(repeated.verify_cpu_flag_ledger)
    source=once(source,"original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()","original=CURRENT_GUEST")
    source=once(source,"'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'",repr(hashlib.sha256(guest).hexdigest().upper()))
    exec(compile(source,__file__+'::entire_repeated_flag_ledger_bound_to_whole_current_guest','exec'),scope)
    for function in (repeated._verify_log,repeated.verify_log):
        exec(compile(inspect.getsource(function),__file__+'::entire_original_repeated_pair_contract','exec'),scope)
    verify=scope['verify_log']

    source=inspect.getsource(complete_health.whole_health)
    source=once(source,'p=prior.cpu.original','p=repeated')
    source=once(source,"assert set(posts)=={(f,s)for f in range(first,last+1)for s in(1,2)},'Both complete draw-time physical slots'", """terminal=p.rows(log,'RESULT')
 assert len(terminal)==1 and terminal[0]['frame']==last and terminal[0]['complete_count']>=2
 assert last==terminal[0]['complete']+30,'Exact schema9 repeated full-pair exit deadline'
 physical_source=(ROOT/'mk2ks_cpu_recovery_probe_v1459.lua').read_text()
 assert 'if complete_count>=2 and frame>=last_complete+30 then manager.machine:exit()end'in physical_source
 assert set(posts)=={(f,s)for f in range(first,last)for s in(1,2)},'All actually executed post fields before original pre-callback exit'
 phase=[s for s in log.splitlines()if s.startswith('MK2_HPHASE_RESULT ')]
 assert len(phase)==1 and int(re.search(r'frame=(\\d+)',phase[0])[1])==last
 assert not any(r['frame']==last for r in stores),'No execution invented in original exit callback'""")
    source=once(source,'for frame in range(first,last+1):','for frame in range(first,last):')
    source=once(source,"((1,'vhp'),(2,'hp'))","((1,'hp'),(2,'vhp'))")
    source=once(source,"(h['cpu_slot'],h['human_slot'])==(2,1)","(h['cpu_slot'],h['human_slot'])==(1,2)")
    source=once(source,"prefix='v'if slot==1 else''","prefix='v'if slot==2 else''")
    source=once(source,"count==len(stores)>4","count==len(stores)>0")
    health_scope=dict(complete_health.whole_health.__globals__,repeated=repeated,re=re)
    exec(compile(source,__file__+'::whole_both_physical_slots_health_replay_exact_repeated_terminal','exec'),health_scope)
    whole_health=health_scope['whole_health']

    def physical(text,human,current_guest):
        need(current_guest==guest,'Whole independently reconstructed matched current guest')
        result=verify(text,human)
        need(result['passed'],str(result['errors']))
        fields=repeated.rows(text,'FIELD')
        need(all(r['id']==18 and r['vid']==repeated.HUMANS[human] and
                 (r['cpu_slot'],r['human_slot'])==(1,2) and
                 r['floor']==r['stage_floor']-135 and
                 r['vfloor']==r['stage_floor']-(134 if human=='kano'else 135)for r in fields),
             'Every native CPU Sonya/human true identity and source-derived floor anchor')
        flags=repeated.flag_rows(text)
        for r in flags:
            offset=(r['pc']-32-0xff800000)//8
            need(0<=offset<=len(guest)-4 and struct.unpack_from('<HH',guest,offset)==(r['op0'],r['op1']),
                 'Every observed store in both physical slots matches whole current code')
            need(r['at']==(r['actor']+0x160 if r['kind']=='body'else r['main']+(0x1f0 if r['kind']=='action'else 0x210)),
                 'Every actual both-slot native store address belongs to correct owner')
        return dict(originalContract=result,allRecordedFields=len(fields),sourceBoundStores=len(flags),
                    floorAnchorsChecked=True,wholeNativeHealthHistory=whole_health(text,guest))
    return physical


def bindings(guest,human):
    physical=physical_bindings(guest)
    scope=dict(vars(prior.cpu_body),cpu=SimpleNamespace(original=repeated,verify_log=physical))
    source=inspect.getsource(prior.cpu_body.bindings)
    source=once(source,"ids={2:17,1:cpu.original.HUMANS[b[\"human\"]]}","ids={1:18,2:cpu.original.HUMANS[b[\"human\"]]}")
    exec(compile(source,__file__+'::whole_original_body_shadow_factory_physical_CPU_Sonya_P1','exec'),scope)
    _,original=scope['bindings'](human)
    return lambda b,g,p,gfx:original(dict(b,human=human),g,p,gfx)


def run():
    global guest,gfx,gfx32,payload,native,pins,check
    need(not BASE.exists() and not OUT.exists() and not base.identity.census(),'Fresh native repeated-pair trial')
    guard=qualify()
    scope=dict(vars(base.ui),INIT=INIT,__file__=__file__)
    exec(compile(inspect.getsource(base.ui.expectation),__file__+'::whole_current_guest_initializer','exec'),scope)
    guest,gfx,build=scope['expectation']()
    native,_,_,decode=base.bindings(guest,build)
    candidate=ROOT/base.audio.NAME
    payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()
    pins=dict(build['input_hashes']);pins.update(guard['inputHashes'])
    for p in (Path(repeated.__file__),Path(complete_health.__file__),Path(prior.__file__),Path(base.__file__),
              Path(base.shadow.__file__),Path(base.graphics.__file__),Path(base.original_transport.__file__),
              GUARD/'report.json',INIT/'report.json',candidate/'roms/mk2ks/mk2ks.mdata'):
        pins[str(p.resolve())]=sha(p)
    gfx32=base.reconstruct(native,pins)
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
        need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==original[(lo-0xff800000)//8:(hi-0xff800000)//8],
             'Entire original native body/shadow kernels unchanged')
    source=inspect.getsource(base.capture)
    source=once(source,"env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM='kitana')",
                "env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='605',MK2KS_CPU_PAIR_APPROACH='guard_until_close',MK2KS_CPU_PAIR_CONFIRM_AGE='264')")
    source=once(source,"s.startswith('MK2_HSPECIAL_RESULT ')","s.startswith('MK2_CPU_PAIR_RESULT ')")
    source=once(source,"need(len(result)==1 and result[0]['completed']==result[0]['attempt']=='2','Both real physical activation/recovery cycles')",
                "need(len(result)==1 and result[0]['schema']=='9' and int(result[0]['complete_count'])>=2 and int(result[0]['complete'])>0,'At least two actual full paired recoveries')")
    source=once(source,"b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams)",
                "b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams,human='kano',cpuLog=text)")
    source=once(source,"key=f'{move}_p{side}'","key='leg_cpu_sonya_p1_human_kano_p2'")
    source=once(source,"victim='kitana'","victim='kano'")
    scope=dict(vars(base),BASE=BASE,LUA=LUA,RAM_CASES=RAM_CASES,COMPLETED=COMPLETED)
    exec(compile(source,__file__+'::whole_RAM_only_native_capture_unchanged_physical_schema9','exec'),scope)
    check=bindings(guest,'kano')
    r=scope['capture']('leg',1,guest,gfx,gfx32,payload,native,check,decode,pins)
    need(r['passed'],'Full repeated-pair/body/shadow/health positive control')
    need(not base.identity.census() and all(sha(p)==h for p,h in pins.items()),'Same native terminal and immutable inputs')
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,candidate=native.NAME,cases=COMPLETED,inputHashes=pins,
        physicalCPUSlot=1,physicalHumanSlot=2,actualCPUChoicePrescribed=False,checkerFaultTestsPending=True,
        fullVisualTimelineAccepted=False,allCPUContextsAccepted=False,allArenasAccepted=False,fullAudioAcceptance=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active'))
    print('Two full original native CPU Sonya pairs/body/shadow/whole health accepted; faults/visual review pending',flush=True)


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve executed failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                        fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    server=base.preview.serve(RAM_CASES)
    code.interact(banner='Same actual CPU Sonya repeated trial retained in RAM; no terminal replay.',
                 local=dict(cases=RAM_CASES,server=server,module=__import__(__name__)))
