"""Latest selector candidate: all eight specials, both slots, twice each.

Preserve full original physical controls, contiguous native body/shadow
provenance, all194 special and176 shadow faults. Add complete initialized
HIGH/OWNED/reservedGFX proofs in EACH native job and retain exact handles.
Finite Prison/Kitana trials, not CPU/blocked/KO/arena/audio/full-port acceptance.
"""
import code,hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
from types import SimpleNamespace
import capture_native_kano_laser_special_shadow as prior
import capture_native_selector_continue as models
import verify_native_selector_layers_startup as startup

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
BASE=ROOT/'audit_native_selector_special_shadow_ram'
OUT=ROOT/'audit_native_selector_special_shadow_checked'
MATRIX=ROOT/'audit_native_selector_special_matrix_checked'
INIT=ROOT/'audit_native_selector_special_initializer_source'
LUA=ROOT/'mk2ks_native_selector_special_shadow.lua'
RAM_CASES={};COMPLETED=[];NATIVE_HANDLES={};WINDOWS={}
state=None


def replace(source,before,after):
    need(source.count(before)==1,'Exact entire original special boundary: '+before)
    return source.replace(before,after,1)


def expectation():
    source=inspect.getsource(models.expectation)
    source=replace(source,"ROOT/'tools/capture_native_selector_continue.py'", "Path(__file__)")if "ROOT/'tools/capture_native_selector_continue.py'"in source else source
    scope=dict(vars(models),INIT=INIT,WINDOWS=WINDOWS,LUA=LUA,__file__=__file__)
    exec(compile(source,__file__+'::independent_complete_current_initialized_models','exec'),scope)
    guest,gfx,build,current=scope['expectation']()
    return guest,gfx,build


def functions():
    audio=SimpleNamespace(**(vars(prior.audio)|dict(NAME=startup.NAME)))
    scope=dict(vars(prior),audio=audio,BASE=BASE,OUT=OUT,MATRIX=MATRIX,INIT=INIT,LUA=LUA,
        RAM_CASES=RAM_CASES,COMPLETED=COMPLETED,NATIVE_HANDLES=NATIVE_HANDLES,WINDOWS=WINDOWS,
        expectation=expectation,__file__=__file__)
    for name in ('bindings','reconstruct','channels_gate','load','shadow_faults'):
        exec(compile(inspect.getsource(getattr(prior,name)),__file__+'::whole_original_'+name,'exec'),scope)
    source=inspect.getsource(prior.capture)
    changes=(
        ('images={};scenes=[];streams=[];proofs={};errors=[]',
         'images={};scenes=[];streams=[];proofs={};errors=[];cold_buffers={k:bytearray()for k in WINDOWS}'),
        ('        actual=None',
         '        NATIVE_HANDLES[key]=dict(process=job,command=command,folder=folder)\n        actual=None'),
        ("actual['createdUnix']>=born-1", "actual['createdUnix']>=born"),
        ("str(folder)in actual['CommandLine']", "actual['CommandLine']==subprocess.list2cmdline(command)"),
        ("        save(folder/'process.json'", "        NATIVE_HANDLES[key]['identity']=actual\n        save(folder/'process.json'"),
        ("                        if tag in('MK2_HPHASE_GUEST','MK2_HPHASE_GFX'):",
         "                        if tag=='MK2_DRAIN_STARTUP':\n"
         "                            kind=h['kind'];need(kind in cold_buffers and int(h['offset'])==len(cold_buffers[kind])and h['writes']=='0'and h['assistance']=='none'and int(h['start'],16)==(0x1fb0000 if kind=='graphics'else 0),'Every complete actual initialized chunk, ordered and unassisted')\n"
         "                            cold_buffers[kind].extend(raw);need(len(cold_buffers[kind])<=len(WINDOWS[kind]),'No duplicate or overflow initialized window')\n"
         "                            if len(cold_buffers[kind])==len(WINDOWS[kind]):\n"
         "                                need(bytes(cold_buffers[kind])==WINDOWS[kind],'Entire actual current '+kind+' equals independent model in THIS special job')\n"
         "                                proofs['cold_'+kind]=dict(bytes=len(cold_buffers[kind]),sha256=digest_window(cold_buffers[kind]),everyActualByteComparedInRAM=True)\n"
         "                        elif tag in('MK2_HPHASE_GUEST','MK2_HPHASE_GFX'):"),
        ('len(proofs)==2','len(proofs)==5'),
        ("        result=[dict(re.findall", "        need(text.count('MK2_DRAIN_STARTUP_COMPLETE writes=0 assistance=none')==1,'Exactly one full current startup completion')\n        result=[dict(re.findall"),
        ('        fullPortAcceptance=False,fullArtAcceptance=False,fullAudioAcceptance=False)',
         '        fullPortAcceptance=False,fullArtAcceptance=False,fullAudioAcceptance=False,limitedUIGFXBytes=18976,fullGFXRegionAccepted=False,fullCurrentHIGHOWNEDReservedGFXAccepted=True)'))
    for before,after in changes:source=replace(source,before,after)
    scope['digest_window']=lambda raw:hashlib.sha256(raw).hexdigest().upper()
    exec(compile(source,__file__+'::entire_native_capture_plus_full_current_windows_exact_kernel_identity','exec'),scope)
    source=inspect.getsource(prior.run)
    before="    scope=dict(vars(ui),INIT=INIT,__file__=__file__)\n    exec(compile(inspect.getsource(ui.expectation),__file__+'::whole_independent_current_guest_initializer','exec'),scope)\n    guest,gfx,build=scope['expectation']()"
    source=replace(source,before,'    guest,gfx,build=expectation()\n    globals().update(guest=guest,gfx=gfx,build=build)')
    source=replace(source,'    native,human_check,check,decode_part=bindings(guest,build)',
        '    native,human_check,check,decode_part=bindings(guest,build)\n    globals().update(native=native,human_check=human_check,check=check,decode_part=decode_part)')
    source=replace(source,"    gfx32=reconstruct(native,pins)","    gfx32=reconstruct(native,pins)\n    globals().update(gfx32=gfx32,payload=payload,pins=pins)")
    source=replace(source,'for p in(Path(__file__),LUA,GUARD,',
        "for p in(Path(__file__),Path(prior.__file__),Path(models.__file__),Path(startup.__file__),startup.OUT/'report.json',ROOT/'mk2ks_native_shang_drain_startup.lua',ROOT/'mk2ks_native_kano_laser_special_shadow.lua',ROOT/'audit_native_selector_continue_combined_checked/report.json',LUA,GUARD,")
    source=replace(source,"        inputHashes=pins,outputHashes=outputs,scope=__doc__,allEightMovesBothSlotsRepeatRecoverVerified=True,",
        "        inputHashes=pins,outputHashes=outputs,scope=__doc__,allEightMovesBothSlotsRepeatRecoverVerified=True,wholeCurrentInitializedWindowsProvedInEachNativeJob=True,limitedUIGFXBytes=18976,fullGFXRegionAccepted=False,")
    scope.update(prior=prior,models=models,startup=startup)
    exec(compile(source,__file__+'::entire16case_32cycle_194special_176shadow_fault_matrix','exec'),scope)
    return scope


if __name__=='__main__':
    try:state=functions();accepted=state['run']()
    except Exception as error:
        failure=ROOT/'audit_native_selector_special_shadow_failure'
        need(not failure.exists(),'Never overwrite actual preflight/native rejection');failure.mkdir()
        prior.save(failure/'report.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
            completedCases=COMPLETED,inputHashes={str(Path(__file__).resolve()):sha(__file__)},fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
    server=prior.preview.serve(RAM_CASES)
    code.interact(banner='Original current special/shadow native handles and RGB retained; never timeout-replay.',
        local=dict(cases=RAM_CASES,handles=NATIVE_HANDLES,state=state,server=server))
