"""Fresh standing-guard physical trial; preceding actual pressure/KO stays rejected.

Reuse the same independently reconstructed RAM inventories and compiled full
observer. Only the original permitted human strategy changes; CPU untouched.
"""
import gzip
import inspect
import json
import traceback
from pathlib import Path
import capture_native_kano_laser_cpu_leg_repeat_p2 as prior

ROOT,need,sha,base=prior.ROOT,prior.need,prior.sha,prior.base
BASE=ROOT/'audit_native_kano_laser_cpu_leg_guard_wait_ram'
OUT=ROOT/'audit_native_kano_laser_cpu_leg_guard_wait_checked'
KEY='leg_cpu_sonya_p2_human_sonya_p1_guard_wait'
RAM_CASES={}
COMPLETED=[]
physical_bindings=prior.physical_bindings


def run(actual):
    global guest,gfx,gfx32,payload,native,pins,check
    need(not BASE.exists() and not OUT.exists() and not base.identity.census(),'Fresh physical guard strategy, original terminal not replayed')
    old_folder,text,images=actual.RAM_CASES[actual.KEY]
    old=json.loads((old_folder/'result.json').read_text())
    need(not old['passed'] and old['nativeExit']==0 and not old['nativeTerminal']['hostDecodeErrors'],
         'Preserve actually terminal earlier CPU Sonya pressure/KO rejection')
    original=prior.previous.repeated
    complete=original.rows(text,'COMPLETE');incomplete=original.rows(text,'INCOMPLETE')
    regains=original.rows(text,'VICTIM_REGAIN')
    need(len(complete)==1 and len(incomplete)==1 and incomplete[0]['cycle']==2 and
         regains[-1]['cycle']==2 and regains[-1]['vhp']<complete[0]['vhp']-35,
         'Prior second actual victim regained after additional native damage, not full uninterrupted pair')
    guest,gfx,gfx32,payload,native,check=(getattr(actual,k)for k in ('guest','gfx','gfx32','payload','native','check'))
    pins=dict(actual.pins)
    for p in (Path(__file__),Path(prior.__file__),old_folder/'result.json',old_folder/'native_terminal.json',
              old_folder/'run.log.gz',actual.OUT/'failure.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Same independently reconstructed current inputs and original source guard')
    source=inspect.getsource(base.capture)
    once=prior.once
    source=once(source,"env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM='kitana')",
                "env.update(MK2KS_TEST_FIGHTER='sonya',MK2KS_TEST_BOOT_FRAME='606',MK2KS_CPU_PAIR_APPROACH='guard_wait',MK2KS_CPU_PAIR_CONFIRM_AGE='264')")
    source=once(source,"s.startswith('MK2_HSPECIAL_RESULT ')","s.startswith('MK2_CPU_PAIR_RESULT ')")
    source=once(source,"need(len(result)==1 and result[0]['completed']==result[0]['attempt']=='2','Both real physical activation/recovery cycles')",
                "need(len(result)==1 and result[0]['schema']=='9' and int(result[0]['complete_count'])>=2 and int(result[0]['complete'])>0,'At least two actual full paired recoveries')")
    source=once(source,"b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams)",
                "b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams,human='sonya',cpuLog=text)")
    source=once(source,"key=f'{move}_p{side}'",'key='+repr(KEY))
    source=once(source,"victim='kitana'","victim='sonya'")
    scope=dict(vars(base),BASE=BASE,LUA=actual.LUA,RAM_CASES=RAM_CASES,COMPLETED=COMPLETED)
    exec(compile(source,__file__+'::whole_native_capture_original_human_guard_wait_option','exec'),scope)
    _,_,_,decode=base.bindings(guest,dict(executable_sha256=native.EXE_SHA,
                                       expected_guest_sha256=native.GUEST_SHA,payload_sha256=native.PAYLOAD_SHA))
    try:
        r=scope['capture']('leg',2,guest,gfx,gfx32,payload,native,check,decode,pins)
        need(r['passed'],'Whole original repeated CPU/body/shadow/health positive')
        need(not base.identity.census() and all(sha(p)==h for p,h in pins.items()),'Actual native terminal and all conserved sources')
        OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,cases=COMPLETED,candidate=native.NAME,inputHashes=pins,
            physicalCPUSlot=2,physicalHumanSlot=1,actualCPUChoicePrescribed=False,checkerFaultTestsPending=True,
            allCPUContextsAccepted=False,allArenasAccepted=False,fullVisualTimelineAccepted=False,fullAudioAcceptance=False,
            fullPortAcceptance=False,publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active'))
    except Exception as error:
        need(not OUT.exists(),'Preserve fresh strategy failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    return COMPLETED
