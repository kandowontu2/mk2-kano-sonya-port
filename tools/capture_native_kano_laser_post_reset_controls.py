"""One fresh current native reset/control job, full native rasters in RAM only.

Use the qualified whole adaptive controller. No old runtime pass, modified
guest state, emulator rebuild, duplicate ROM or disk image/audio transport.
"""
import code
import inspect
import json
import traceback
from pathlib import Path
import capture_native_kano_laser_cpu_leg_children as previous
import qualify_native_kano_laser_post_reset_controls as qualifier
import native_kano_laser_post_reset_controls_contract as contract

ROOT,need,sha,once,base=previous.ROOT,previous.need,previous.sha,previous.once,previous.base
BASE=ROOT/'audit_native_kano_laser_post_reset_controls_ram'
OUT=ROOT/'audit_native_kano_laser_post_reset_controls_checked'
INIT=ROOT/'audit_native_kano_laser_post_reset_controls_initializer_source'
KEY='sonya_p1_cpu_sonya_earned_reset_actual_controls'
LUA=qualifier.LUA
RAM_CASES={}
COMPLETED=[]


def run():
    global guest,gfx,gfx32,payload,native,pins
    need(not BASE.exists() and not OUT.exists() and not base.identity.census(),'Fresh actual native reset/control test')
    guard=json.loads((qualifier.GUARD/'report.json').read_text())
    need(guard['passed'] and guard['actualNativeParserAccepted'] and
         guard['wholeOriginalAdaptiveActualResponseLogicConserved'] and not guard['gameplayAccepted'] and
         all(sha(p)==h for p,h in guard['inputHashes'].items()),'All eleven whole actual native expansions remain unchanged')
    scope=dict(vars(base.ui),INIT=INIT,__file__=__file__)
    exec(compile(inspect.getsource(base.ui.expectation),__file__+'::whole_independent_current_guest','exec'),scope)
    guest,gfx,build=scope['expectation']()
    native,_,_,decode=base.bindings(guest,build)
    payload=(ROOT/base.audio.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    pins=dict(build['input_hashes']);pins.update(guard['inputHashes'])
    for p in (Path(__file__),Path(qualifier.__file__),Path(contract.__file__),Path(contract.original_controls.__file__),
              Path(contract.ground.__file__),Path(contract.ground.prior.__file__),Path(base.__file__),
              Path(base.shadow.__file__),Path(base.graphics.__file__),Path(base.original_transport.__file__),
              qualifier.GUARD/'report.json',INIT/'report.json',LUA,ROOT/'PLAY_LATEST_KANO_SONYA.cmd'):
        pins[str(p.resolve())]=sha(p)
    gfx32=base.reconstruct(native,pins)
    source=inspect.getsource(base.capture)
    source=once(source,
        "env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM='kitana')",
        "env.update(MK2KS_TEST_FIGHTER='sonya',MK2KS_TEST_BOOT_FRAME='606',MK2KS_CPU_PAIR_APPROACH='guard_wait',MK2KS_CPU_PAIR_CONFIRM_AGE='264')")
    source=once(source,"elif tag=='MK2_HPHASE_RGB':","elif tag in('MK2_HPHASE_RGB','MK2_POST_CTRL_RGB'):")
    source=once(source,"name=f'ui_{frame:04d}.png'", "name=(f'control_{frame:04d}.png'if tag=='MK2_POST_CTRL_RGB'else f'ui_{frame:04d}.png')")
    source=once(source,"scenes.append(dict(stage=h['stage'],attempt=int(h['attempt']),frame=frame,",
        "scenes.append(dict(stage=h['stage'],attempt=int(h['attempt']),frame=frame,nativeRasterFrame=int(h.get('native_frame',h['frame'])),transportTag=tag,")
    source=once(source,"s.startswith('MK2_HSPECIAL_RESULT ')","s.startswith('MK2_POST_CTRL_RESULT ')")
    source=once(source,
        "need(len(result)==1 and result[0]['completed']==result[0]['attempt']=='2','Both real physical activation/recovery cycles')",
        "need(len(result)==1 and int(result[0]['recover'])>0 and int(result[0]['frame'])==int(result[0]['recover'])+180,'Actual control recovery then180 native survival fields')")
    source=once(source,
        "b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams)",
        "b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams,human='sonya',cpuLog=text)")
    source=once(source,"key=f'{move}_p{side}'",'key='+repr(KEY))
    source=once(source,"victim='kitana'","victim='sonya'")
    scope=dict(vars(base),BASE=BASE,LUA=LUA,RAM_CASES=RAM_CASES,COMPLETED=COMPLETED)
    exec(compile(source,__file__+'::whole_native_RAM_transport_actual_post_reset_controls','exec'),scope)
    result=scope['capture']('leg',2,guest,gfx,gfx32,payload,native,contract.check,decode,pins)
    need(result['passed'],'Full actual control/round/health/ground positive; preserve failure')
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,candidate=native.NAME,case=COMPLETED[0],inputHashes=pins,
        semanticFaultTestsPending=True,bodyShadowFaultsPending=True,fullVisualTimelineAccepted=False,
        fullAudioAcceptance=False,allCPUContextsAccepted=False,fullPortAcceptance=False,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active'))


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual reset/control rejection');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                        fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    server=base.preview.serve(RAM_CASES)
    code.interact(banner='Same actual native post-reset control/RGB trial retained in RAM; no terminal replay.',
        local=dict(cases=RAM_CASES,server=server,module=__import__(__name__)))
