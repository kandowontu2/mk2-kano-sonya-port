"""Fresh physical CPU Sonya trial with previously native-qualified child taps.

Keep the original two-uninterrupted-pair acceptance gate. Extra child/guard
observations do not turn an interrupted pair into an uninterrupted success.
All guest, graphics and original rasters stay in this parent process's RAM.
"""
import code
import inspect
import json
import traceback
from pathlib import Path
import capture_native_kano_laser_cpu_leg_repeat_p2 as prior

ROOT,need,sha,once,base=prior.ROOT,prior.need,prior.sha,prior.once,prior.base
BASE=ROOT/'audit_native_kano_laser_cpu_leg_children_ram'
OUT=ROOT/'audit_native_kano_laser_cpu_leg_children_repeat_checked'
INIT=ROOT/'audit_native_kano_laser_cpu_leg_children_initializer_source'
GUARD=ROOT/'audit_native_kano_laser_cpu_leg_children_source'
LUA=ROOT/'mk2ks_native_kano_laser_cpu_leg_children.lua'
KEY='leg_cpu_sonya_p2_human_sonya_p1_children'
RAM_CASES={}
COMPLETED=[]


def run():
    global guest,gfx,gfx32,payload,native,pins,check
    need(not BASE.exists() and not OUT.exists() and not base.identity.census(),
         'Fresh actual native child trial; no earlier gameplay replay')
    guard=json.loads((GUARD/'report.json').read_text())
    need(guard['passed'] and guard['actualNativeParserAccepted'] and
         guard['wholePassiveChildGuardObserversConserved'] and
         guard['wholePhysicalInputLogicConservedFiveObservationChangesSixRAMSinks'] and
         not guard['gameplayAccepted'] and not guard['childGameplayAccepted'] and
         all(sha(p)==h for p,h in guard['inputHashes'].items()),
         'All seven actual-native-compiled whole observers remain unchanged')
    scope=dict(vars(base.ui),INIT=INIT,__file__=__file__)
    exec(compile(inspect.getsource(base.ui.expectation),
                 __file__+'::whole_current_independent_initializer','exec'),scope)
    guest,gfx,build=scope['expectation']()
    native,_,_,decode=base.bindings(guest,build)
    candidate=ROOT/base.audio.NAME
    payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()
    pins=dict(build['input_hashes']);pins.update(guard['inputHashes'])
    for p in (Path(__file__),Path(prior.__file__),Path(prior.previous.__file__),
              Path(base.__file__),Path(base.shadow.__file__),Path(base.graphics.__file__),
              Path(base.original_transport.__file__),Path(base.identity.__file__),LUA,
              GUARD/'report.json',INIT/'report.json',candidate/'mkport_candidate.exe',
              candidate/'roms/mk2ks/mk2ks.mdata',ROOT/'PLAY_LATEST_KANO_SONYA.cmd'):
        pins[str(p.resolve())]=sha(p)
    gfx32=base.reconstruct(native,pins)
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
        need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==
             original[(lo-0xff800000)//8:(hi-0xff800000)//8],
             'Entire original native body/shadow kernels unchanged')
    source=inspect.getsource(base.capture)
    source=once(source,
        "env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM='kitana')",
        "env.update(MK2KS_TEST_FIGHTER='sonya',MK2KS_TEST_BOOT_FRAME='606',MK2KS_CPU_PAIR_APPROACH='original',MK2KS_CPU_PAIR_CONFIRM_AGE='264')")
    source=once(source,"s.startswith('MK2_HSPECIAL_RESULT ')","s.startswith('MK2_CPU_PAIR_RESULT ')")
    source=once(source,
        "need(len(result)==1 and result[0]['completed']==result[0]['attempt']=='2','Both real physical activation/recovery cycles')",
        "need(len(result)==1 and result[0]['schema']=='9' and int(result[0]['complete_count'])>=2 and int(result[0]['complete'])>0,'At least two actual full paired recoveries')")
    source=once(source,
        "b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams)",
        "b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams,human='sonya',cpuLog=text)")
    source=once(source,"key=f'{move}_p{side}'",'key='+repr(KEY))
    source=once(source,"victim='kitana'","victim='sonya'")
    scope=dict(vars(base),BASE=BASE,LUA=LUA,RAM_CASES=RAM_CASES,COMPLETED=COMPLETED)
    exec(compile(source,__file__+'::whole_RAM_capture_extra_passive_children_original_acceptance','exec'),scope)
    check=prior.bindings(guest,'sonya')
    result=scope['capture']('leg',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    need(result['passed'],'Original full repeated-pair/body/shadow/health acceptance retained')


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve fresh actual acceptance failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                        fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    server=base.preview.serve(RAM_CASES)
    code.interact(banner='Same actual child-covered CPU Sonya trial retained in RAM; no terminal replay.',
                 local=dict(cases=RAM_CASES,server=server,module=__import__(__name__)))
