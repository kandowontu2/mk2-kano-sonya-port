"""Current native candidate, full original four-route paid-continue contracts.

No older runtime pass transfers. Whole original physical Lua and every
state/UI/source-raster/actual-response condition retained. Native executable
is launched directly and declared as such; public CMD remains untouched.
All full original rasters/guest/GFX remain RAM-only; no gameplay writes.
"""
import argparse
import code
import inspect
import json
import traceback
from pathlib import Path
from types import SimpleNamespace
import capture_cross_continue_adaptive as original
import cross_continue_adaptive_contract as adaptive
import qualify_cross_continue_adaptive_v2 as qualified
import check_cross_continue_adaptive_pixels as pixels
import check_cross_continue_controls as controls
import capture_native_kano_laser_special_shadow as native_base
import review_launch_challenger_ram_frames as preview

ROOT,need,sha=native_base.ROOT,native_base.need,native_base.sha
INIT=ROOT/'audit_native_kano_laser_cross_continue_initializer_source'
PREFIX='audit_native_kano_laser_cross_continue'
RAM_CASES={}
COMPLETED=[]
once=native_base.ui.audio.qualified.need


def replace(source,before,after):
    need(source.count(before)==1,'Exact whole retained-source adaptation: '+before)
    return source.replace(before,after,1)


def expectation():
    scope=dict(vars(native_base.ui),INIT=INIT,__file__=__file__)
    exec(compile(inspect.getsource(native_base.ui.expectation),__file__+'::whole_current_independent_initializer','exec'),scope)
    guest,gfx,build=scope['expectation']()
    current=SimpleNamespace(ROOT=ROOT,NAME=native_base.audio.NAME,EXE_SHA=build['executable_sha256'],
        GUEST_SHA=build['expected_guest_sha256'],PAYLOAD_SHA=build['payload_sha256'],expected=lambda:guest,expected_gfx=lambda:gfx)
    return guest,gfx,build,current


def contracts(current):
    viewport_scope=dict(adaptive.previous.viewport.__globals__,context=current)
    exec(compile(inspect.getsource(adaptive.original.viewport),__file__+'::whole_current_source_ladder_viewport','exec'),viewport_scope)
    render_scope=dict(vars(adaptive.model),viewport=viewport_scope['viewport'])
    exec(compile(adaptive.original.source,__file__+'::whole_original_native_UI_raster_gate_current_guest','exec'),render_scope)
    gate_scope=dict(vars(adaptive),current=current)
    source=replace(inspect.getsource(adaptive.gate),'current v6640','current native Kano laser/audio candidate')
    exec(compile(source,__file__+'::whole_original_cross_continue_actual_response_gate','exec'),gate_scope)
    dependencies=[*adaptive.DEPENDENCIES,Path(__file__),Path(original.__file__),Path(qualified.__file__),
        Path(pixels.__file__),Path(controls.__file__),Path(native_base.__file__),Path(native_base.ui.__file__),
        Path(native_base.audio.__file__),INIT/'report.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
    return SimpleNamespace(**(dict(vars(adaptive))|dict(current=current,gate=gate_scope['gate'],
        viewport=viewport_scope['viewport'],render=render_scope['render'],DEPENDENCIES=dependencies)))


def collector(current,contract):
    source=original.source
    source=replace(source,'audit_cross_continue_adaptive_',PREFIX+'_')
    source=replace(source,
        "command=[os.environ['ComSpec'],'/d','/c',str(ROOT/'TEST_KANO_BALL_LAUNCH_V6640.cmd'),'-video'",
        "command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(build/'samples')+';'+str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-skip_gameinfo','-nocheat','-wavwrite','NUL','-video'")
    source=replace(source,"'-str','250'","'-str','400'")
    source=replace(source,'j[\'ParentProcessId\']==process.pid',"j['ProcessId']==process.pid and j['ParentProcessId']==os.getpid()")
    source=replace(source,"actual checked CMD pid={process.pid}","actual current native pid={process.pid}")
    source=replace(source,"  process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace')",
        "  process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)")
    source=replace(source,"cmdPID=process.pid,startedUnix=started","nativeProducerPID=process.pid,startedUnix=started")
    source=replace(source,"terminal=dict(cmdPID=process.pid,","terminal=dict(nativeProducerPID=process.pid,")
    source=replace(source,"  except(ValueError,AssertionError,KeyError)as e:","  except(ValueError,AssertionError)as e:")
    source=replace(source,'        newBuilds=0,newROMCopies=0,newRawMedia=0,fullPortAcceptance=False)',
        '        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,canonicalCMDUsed=False,publicPlayableChanged=False,fullPortAcceptance=False)')
    source=replace(source," if hold:code.interact(banner='Same terminal native process; full actual display buffers remain in RAM, no replay.',local=dict(images=images,text=text,report=r,guest=guest,folder=out))",
        " RAM_CASES[f'{fighter}_p{side}_to_{target}']=(out,text,images,r)")
    scope=dict(original.scope,__file__=__file__,current=current,contract=contract,gate=contract.gate,
               DEPENDENCIES=contract.DEPENDENCIES,RAM_CASES=RAM_CASES)
    exec(compile(source,__file__+'::whole_original_native_capture_actual_current_direct_PID','exec'),scope)
    return scope['capture']


def qualification(contract):
    source=qualified.source
    source=replace(source,'audit_cross_continue_adaptive_checked_',PREFIX+'_checked_')
    source=replace(source,'except(ValueError,AssertionError,KeyError,IndexError)as e:',
                   'except(ValueError,AssertionError)as e:')
    source=replace(source,"print(json.dumps(dict(passed=True,case=f'{fighter} P{side} to {target}',faults=len(faults),pixels=pixels)),flush=True)",
                   "print(json.dumps(dict(passed=True,case=f'{fighter} P{side} to {target}',faults=len(faults),nativeNameShadowChecks=pixels['native_name_shadow_checks'])),flush=True)")
    scope=dict(qualified.scope,__file__=__file__,contract=contract)
    exec(compile(source,__file__+'::whole_original_eighteen_state_raster_faults_current_candidate','exec'),scope)
    qualify=scope['qualify']
    source=pixels.source
    source=replace(source,'audit_cross_continue_adaptive_checked_',PREFIX+'_checked_')
    source=replace(source,'audit_cross_continue_adaptive_pixels_',PREFIX+'_pixels_')
    source=replace(source,'except(ValueError,AssertionError,KeyError)as e:',
                   'except(ValueError,AssertionError)as e:')
    scope=dict(pixels.scope,__file__=__file__,contract=contract)
    exec(compile(source,__file__+'::whole_original_own_icon_and_extra_raster_faults','exec'),scope)
    pixel_check=scope['check']
    source=inspect.getsource(controls.check)
    source=replace(source,'audit_cross_continue_adaptive_control_faults_',PREFIX+'_control_faults_')
    source=replace(source,'audit_cross_continue_adaptive_checked_',PREFIX+'_checked_')
    source=replace(source,'except(ValueError,KeyError,IndexError)as error:',
                   'except(ValueError,AssertionError)as error:')
    scope=dict(vars(controls),__file__=__file__,contract=contract)
    exec(compile(source,__file__+'::whole_original_nine_actual_control_response_faults','exec'),scope)
    return qualify,pixel_check,scope['check']


def run(fighter,side):
    global guest,gfx,build,current,contract,capture,qualify,pixel_check,control_check
    need(not native_base.identity.census(),'No native game replay or overlapping producer')
    guest,gfx,build,current=expectation();contract=contracts(current)
    capture=collector(current,contract);qualify,pixel_check,control_check=qualification(contract)
    next_case(fighter,side)


def next_case(fighter,side):
    target='sonya'if fighter=='kano'else'kano';key=f'{fighter}_p{side}_to_{target}'
    capture(fighter,side,target,False)
    folder,text,images,report=RAM_CASES[key]
    qualified_report=qualify(folder,text,images,report,fighter,side,target)
    pixel_report=pixel_check(folder,text,images,fighter,side,target)
    control_report=control_check(folder,text,fighter,side,target)
    COMPLETED.append(key)
    print(json.dumps(dict(passed=True,key=key,originalUIStateRasterFaults=len(qualified_report['actualFaultsRejected']),
        originalActualControlFaults=len(control_report['actualControlFaultsRejected']),
        additionalPixelFaults=len(pixel_report['additionalActualImageFaultsRejected']),nativeFramesInRAM=len(images),
        fullPortAcceptance=False)),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
    parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    try:run(args.fighter,args.side)
    except Exception as error:
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                              fullPortAcceptance=False)),flush=True)
    code.interact(banner='Same current native paid-continue buffers retained; do not replay completed captures.',
                  local=dict(cases=RAM_CASES,module=__import__(__name__)))
