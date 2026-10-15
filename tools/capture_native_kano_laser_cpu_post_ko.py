"""Fresh physical match through earned KO and real next-round observation.

Reuse only the live parent's independently reconstructed current inventories,
not previous runtime acceptance. Entire passive round/HP observer is compiled
and source-qualified. Original failed repeated fixture remains unchanged.
"""
import inspect
import json
import traceback
from pathlib import Path
import capture_native_kano_laser_cpu_leg_children_guard as previous
import qualify_native_kano_laser_cpu_post_ko as qualifier

ROOT,need,sha,once,base=previous.ROOT,previous.need,previous.sha,previous.once,previous.base
BASE=ROOT/'audit_native_kano_laser_cpu_post_ko_ram'
OUT=ROOT/'audit_native_kano_laser_cpu_post_ko_checked'
LUA=qualifier.LUA
KEY='cpu_sonya_guard_wait_earned_ko_next_round'
RAM_CASES={}
COMPLETED=[]


def run(actual):
    global guest,gfx,gfx32,payload,native,pins
    need(not BASE.exists() and not OUT.exists() and not base.identity.census(),'Fresh actual physical post-KO trial')
    guard=json.loads((qualifier.GUARD/'report.json').read_text())
    need(guard['passed'] and guard['actualNativeParserAccepted'] and
         guard['wholeOriginalAllModeRoundObserverConserved'] and
         guard['oneNativeKOBodyObserverBoundaryAdapted'] and not guard['gameplayAccepted'] and
         all(sha(p)==h for p,h in guard['inputHashes'].items()),'Whole nine native expansions conserved')
    guest,gfx,gfx32,payload,native=(getattr(actual,k)for k in ('guest','gfx','gfx32','payload','native'))
    pins=dict(actual.pins);pins.update(guard['inputHashes'])
    for p in (Path(__file__),Path(qualifier.__file__),qualifier.GUARD/'report.json',
              actual.BASE/actual.KEY/'native_terminal.json',ROOT/'audit_native_kano_laser_cpu_leg_children_guard_review/report.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Same independently derived current RAM inventories and all executed inputs')
    from verify_native_kano_laser_cpu_post_ko_ledger import check
    checker_file=ROOT/'tools/verify_native_kano_laser_cpu_post_ko_ledger.py'
    pins[str(checker_file.resolve())]=sha(checker_file)
    source=inspect.getsource(base.capture)
    source=once(source,
        "env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM='kitana')",
        "env.update(MK2KS_TEST_FIGHTER='sonya',MK2KS_TEST_BOOT_FRAME='606',MK2KS_CPU_PAIR_APPROACH='guard_wait',MK2KS_CPU_PAIR_CONFIRM_AGE='264')")
    source=once(source,"s.startswith('MK2_HSPECIAL_RESULT ')","s.startswith('MK2_POST_KO_RESULT ')")
    source=once(source,
        "need(len(result)==1 and result[0]['completed']==result[0]['attempt']=='2','Both real physical activation/recovery cycles')",
        "need(len(result)==1 and int(result[0]['earned_ko'])>0 and int(result[0]['resumed'])>int(result[0]['earned_ko']) and result[0]['reason']=='declared_observation_exit','Actual event-declared native KO and next-round observation, not timeout or another exit')")
    source=once(source,
        "b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams)",
        "b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams,human='sonya',cpuLog=text)")
    source=once(source,"key=f'{move}_p{side}'",'key='+repr(KEY))
    source=once(source,"victim='kitana'","victim='sonya'")
    scope=dict(vars(base),BASE=BASE,LUA=LUA,RAM_CASES=RAM_CASES,COMPLETED=COMPLETED)
    exec(compile(source,__file__+'::whole_RAM_capture_event_declared_actual_post_KO','exec'),scope)
    _,_,_,decode=base.bindings(guest,dict(executable_sha256=native.EXE_SHA,expected_guest_sha256=native.GUEST_SHA,payload_sha256=native.PAYLOAD_SHA))
    result=scope['capture']('leg',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    if not result['passed']:
        OUT.mkdir();base.save(OUT/'failure.json',dict(passed=False,captureFailure=result['error'],
                                                    fullPortAcceptance=False,goalStatus='active'))
    return result
