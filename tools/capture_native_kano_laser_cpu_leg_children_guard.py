"""Fresh original guard_wait human route, native CPU/child observers unchanged.

Independent whole current guest/GFX reconstruction; no previous RAM retained,
CPU choice injection, HP edits, ROM copies or emulator rebuild. Keep failed
original uninterrupted-pair acceptance separate from finite mixed contracts.
"""
import code
import inspect
import json
import traceback
from pathlib import Path
import capture_native_kano_laser_cpu_leg_children as prior

ROOT,need,sha,once,base=prior.ROOT,prior.need,prior.sha,prior.once,prior.base
BASE=ROOT/'audit_native_kano_laser_cpu_leg_children_guard_ram'
OUT=ROOT/'audit_native_kano_laser_cpu_leg_children_guard_repeat_checked'
INIT=ROOT/'audit_native_kano_laser_cpu_leg_children_guard_initializer_source'
GUARD=prior.GUARD
LUA=prior.LUA
KEY='leg_cpu_sonya_p2_human_sonya_p1_children_guard_wait'
RAM_CASES={}
COMPLETED=[]


def run():
    global guest,gfx,gfx32,payload,native,pins,check
    review_path=ROOT/'audit_native_kano_laser_cpu_leg_children_review/report.json'
    retired_path=ROOT/'audit_native_kano_laser_cpu_leg_children_retirement/report.json'
    review=json.loads(review_path.read_text());retired=json.loads(retired_path.read_text())
    need(review['passed'] and retired['passed'] and review['finiteMixedRingOwnershipVerified'] and
         review['allNativeHPContextsInThisTraceVerified'] and retired['originalRAMRastersReleased']==21 and
         all(sha(p)==h for p,h in review['inputHashes'].items()),
         'Preserve preceding actual blocked-ring proof and exact terminal retirement')
    source=inspect.getsource(prior.run)
    source=once(source,"MK2KS_CPU_PAIR_APPROACH='original'","MK2KS_CPU_PAIR_APPROACH='guard_wait'")
    source=once(source,"for p in (Path(__file__),Path(prior.__file__),Path(prior.previous.__file__),",
                "for p in (Path(__file__),Path(capture_source_file),review_path,retired_path,Path(prior.__file__),Path(prior.previous.__file__),")
    scope=dict(vars(prior),BASE=BASE,OUT=OUT,INIT=INIT,GUARD=GUARD,LUA=LUA,KEY=KEY,
               RAM_CASES=RAM_CASES,COMPLETED=COMPLETED,__file__=__file__,
               capture_source_file=prior.__file__,review_path=review_path,retired_path=retired_path)
    exec(compile(source,__file__+'::whole_native_capture_only_original_human_guard_strategy_changed','exec'),scope)
    try:scope['run']()
    finally:
        for name in ('guest','gfx','gfx32','payload','native','pins','check'):
            if name in scope:globals()[name]=scope[name]


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve fresh original guard-route failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                        fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    server=base.preview.serve(RAM_CASES)
    code.interact(banner='Same actual child-covered guard_wait trial retained in RAM; no terminal replay.',
                 local=dict(cases=RAM_CASES,server=server,module=__import__(__name__)))
