"""Retain the actual successful native run and old2-proof-count rejection.

Require EXACTLY both original memory proofs PLUS all three full current
initialized windows. All original18 state/raster faults, extra pixels and
nine real-response controls remain intact. No native replay or weaker gate.
"""
import inspect,json
from pathlib import Path
import capture_native_kano_laser_cross_continue as prior
import verify_native_selector_layers_startup as startup

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
PREFIX='audit_native_selector_continue_extra_windows'


def upgrade(state,windows):
    need(state and set(windows)=={'high','owned','graphics'},'Original retained current collector and full independent window models')
    expected={
        'guest':dict(bytes=len(state['guest']),sha256=startup.initial.digest(state['guest']),everyActualByteComparedInRAM=True),
        'gfx':dict(bytes=len(state['gfx']),sha256=startup.initial.digest(state['gfx']),everyActualByteComparedInRAM=True)}
    expected.update({'cold_'+kind:dict(bytes=len(raw),sha256=startup.initial.digest(raw),everyActualByteComparedInRAM=True)for kind,raw in windows.items()})
    cold=json.loads((startup.OUT/'report.json').read_text())
    need({kind:expected['cold_'+kind]['sha256']for kind in windows}==cold['actualWindowHashes']and
         expected['guest']['sha256']==state['build']['expected_guest_sha256']and expected['gfx']['bytes']==18976,
         'All five exact independent expectations, limited original graphics slice remains limited')
    source=inspect.getsource(prior.qualification)
    before='    source=qualified.source'
    after="    source=replace(qualified.source,\"len(old['actualGuestGFXProofs'])==2\",\"old['actualGuestGFXProofs']==fullCurrentProofs\")"
    source=prior.replace(source,before,after)
    before='    scope=dict(qualified.scope,__file__=__file__,contract=contract)'
    source=prior.replace(source,before,'    scope=dict(qualified.scope,__file__=__file__,contract=contract,fullCurrentProofs=FULL_CURRENT_PROOFS)')
    scope=dict(vars(prior),PREFIX=PREFIX,FULL_CURRENT_PROOFS=expected,__file__=__file__)
    exec(compile(source,__file__+'::all_original_predicates_plus_exact_five_window_proofs','exec'),scope)
    state['qualify'],state['pixel_check'],state['control_check']=scope['qualification'](state['contract'])
    path=ROOT/(PREFIX+'_source');need(not path.exists(),'Fresh source successor, preserve earlier rejection');path.mkdir()
    report=dict(passed=True,sourceOnlyAccepted=True,earlierTwoProofCountRejectionPreserved=True,
        fullExactRequiredMemoryProofs=expected,wholeQualificationFactorySHA256=startup.initial.digest(source.encode()),
        allOriginalStateRasterControlPredicatesRetained=True,
        inputHashes={str(p.resolve()):sha(p)for p in (Path(__file__),Path(prior.__file__),ROOT/'tools/capture_native_selector_continue.py',
            ROOT/'audit_native_selector_continue_failure/report.json',ROOT/'audit_native_selector_continue_initializer/report.json')},
        newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,fullPortAcceptance=False)
    (path/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return expected


def qualify_retained(state,cases,fighter,side):
    target='sonya'if fighter=='kano'else'kano';key=f'{fighter}_p{side}_to_{target}'
    folder,text,images,report=cases[key]
    qualified=state['qualify'](folder,text,images,report,fighter,side,target)
    pixels=state['pixel_check'](folder,text,images,fighter,side,target)
    controls=state['control_check'](folder,text,fighter,side,target)
    state['COMPLETED'].append(key)
    print(json.dumps(dict(passed=True,key=key,originalUIStateRasterFaults=len(qualified['actualFaultsRejected']),
        originalActualControlFaults=len(controls['actualControlFaultsRejected']),
        additionalPixelFaults=len(pixels['additionalActualImageFaultsRejected']),nativeFramesInRAM=len(images),
        originalNativeReplayed=False,fullPortAcceptance=False)),flush=True)
    return qualified,pixels,controls
