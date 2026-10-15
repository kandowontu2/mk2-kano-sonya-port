"""Fresh full 52-case native human-state regression, with strict scene diagnostics.

Every physical input/identity/pose/contact/health/recovery event must match the
checked v1836 build. Only palette allocation bank numbers are normalized, as in
the earlier accepted state contract. All endpoint PNGs are compared, not masked.
Scene differences are retained as unresolved gates, never relabeled a pass.
No universal artwork, erasure, CPU, repeated-match or audio acceptance.
"""
import hashlib,json,re,sys
from pathlib import Path
import numpy as np
from PIL import Image
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_human_special_matrix as positive
import verify_human_special_negative_v6 as negative
import run_native_palette_special_regression_v2790 as dispatch

ROOT=assembly.ROOT;NAME=assembly.NAME
OUT=ROOT/'audit_v2792_native_palette_special_state_checked'

def verify():
    pins={};cases=[];screens=[]
    def pin(path,wanted=None):
        path=Path(path)
        if not path.is_absolute():path=ROOT/path
        key=str(path.absolute());actual=assembly.sha(path)
        assembly.need(wanted is None or actual==wanted,'Changed evidence '+key)
        assembly.need(key not in pins or pins[key]==actual,'Consistent pinned file '+key)
        pins[key]=actual
    assembly.source_check()
    for path,wanted in assembly.source_check().items():pin(path,wanted)
    proof_path=ROOT/'audit_v2751_native_friendship_palette_assembly_checked/report.json'
    proof=json.loads(proof_path.read_text());pin(proof_path)
    assembly.need(proof['passed'] and proof['sourceOnly'] and proof['candidate']==NAME,'Independent native patch proof')
    guest,_,payload,_,_=assembly.expected()
    assembly.need(hashlib.sha256(guest).hexdigest().upper()==proof['independentlyAssembledExpectedGuestSHA256'],'Complete independently expected guest')
    build_path=ROOT/NAME/'build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'));pin(build_path)
    assembly.need(build['name']==NAME and hashlib.sha256(payload).hexdigest().upper()==build['payload_sha256'],'Matched independently reconstructed payload')
    pin(ROOT/NAME/'mkport_candidate.exe',build['executable_sha256'])
    pin(ROOT/NAME/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
    for path,wanted in build['input_hashes'].items():pin(path,wanted)
    pin(ROOT/NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp',assembly.SOURCE_SHA)
    prior_path=ROOT/'audit_v1846_ball_register_special_matrix_checked/report.json'
    prior=json.loads(prior_path.read_text());pin(prior_path)
    assembly.need(prior['passed'] and prior['candidate']=='diagnostic_v1836_ball_register_boundary' and prior['current52CaseHumanStateMatrixAccepted'],'Accepted checked-build baseline')
    historical={str((Path(p) if Path(p).is_absolute() else ROOT/p).absolute()):h for p,h in prior['inputHashes'].items()}
    def baseline_pin(path):
        key=str(path.absolute())
        assembly.need(key in historical,'Baseline file bound to accepted historical proof: '+key)
        pin(path,historical[key])
    dispatch_path=dispatch.OUT/'report.json';ran=json.loads(dispatch_path.read_text());pin(dispatch_path)
    assembly.need(ran['candidate']==NAME and ran['allRunnersTerminal'] and ran['allRunnerExitsZero'] and len(ran['cases'])==52,'All 52 actual runners terminal')
    pin(Path(dispatch.__file__),ran['sourceSHA256'])
    pin(dispatch.OUT/Path(dispatch.__file__).name,ran['sourceSHA256'])
    assembly.need(len(dispatch.fixtures)==52 and len(set(dispatch.fixtures))==52,'Exact complete native fixture inventory')
    for move,side,scenario,air in dispatch.fixtures:
        suffix=move+('_air' if air else '_'+scenario if scenario else '')
        folder=ROOT/f'audit_v2791_human_{suffix}_p{side}'
        baseline=ROOT/(f'audit_v1841_human_ball_p{side}_boundary' if move=='ball' and scenario is None else f'audit_v1845_human_{suffix}_p{side}')
        launch=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        assembly.need((launch['exit_code'],launch['candidate'],launch['move'],launch['side'],launch['victim'],launch['cheats_enabled'],launch['assistance'])==(0,NAME,move,side,'sub_zero',False,'none'),'Actual matched physical fixture')
        assembly.need(launch['executable_sha256']==build['executable_sha256'] and launch['payload_sha256']==build['payload_sha256'],'Matched actual executable/payload')
        assembly.need(launch['scenario']==scenario if scenario else launch['air']==air,'Declared defense/air fixture')
        assembly.need(before==launch['input_hashes'] and all(before.get(p)==h for p,h in build['input_hashes'].items()),'Executed source before/after manifest')
        for path,wanted in before.items():
            pin(path,wanted)
            if Path(path).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(path).name,wanted)
        observer='mk2ks_human_special_negative_v9.lua' if scenario else 'mk2ks_human_special_matrix_v3.lua'
        text=(folder/'input_sources'/observer).read_text()
        assembly.need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|dofile\(',text),'Read-only physical input observer')
        runner='run_current_human_negative_v1240.ps1' if scenario else 'run_current_human_special_v820.ps1'
        assembly.need('-nocheat' in (folder/'input_sources'/runner).read_text(),'Cheat-disabled launcher')
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        old=(baseline/'run.log').read_text(encoding='utf-8-sig');baseline_pin(baseline/'run.log')
        assembly.need(not re.search(r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|fatal error|access violation|stack traceback',log,re.I),'No actual runtime errors')
        events=lambda text:[re.sub(r'\bbank=[0-9A-F]+','bank=NATIVE_ALLOCATION',line) for line in text.splitlines() if line.startswith('MK2_HSPECIAL_')]
        assembly.need(events(log)==events(old),'Every native event matches checked build: '+folder.name)
        result=negative.verify_log(log,move,side,scenario) if scenario else positive.verify_log(log,move,side,air)
        if move=='ball':
            if scenario:negative.verify_repel(log,side)
            if scenario=='block' or scenario is None:result.update(negative.verify_rebound(log,side,scenario=='block'))
        result.update(case=folder.name,actualNativeEvents=len(events(log)),allCheckedBuildNativeEventsMatched=True)
        cases.append(result)
        for filename in ('special_before.png','special_recovered.png','special_final.png'):
            path=folder/'snap'/filename;old_path=baseline/'snap'/filename;baseline_pin(old_path)
            actual=np.asarray(Image.open(path).convert('RGB'));previous=np.asarray(Image.open(old_path).convert('RGB'))
            assembly.need(actual.shape==previous.shape==(254,400,3),'Full unscaled original endpoint scenes')
            changed=np.any(actual!=previous,axis=2);y,x=np.where(changed)
            screens.append(dict(case=folder.name,file=filename,exactPNGBytes=path.read_bytes()==old_path.read_bytes(),
                exactRGBPixels=not bool(changed.any()),differentPixels=int(changed.sum()),
                differingBounds=None if not len(x) else [int(x.min()),int(y.min()),int(x.max()),int(y.max())],
                differencesMasked=False,sourceBoundCauseProven=False if len(x) else None))
        for path in folder.rglob('*'):
            if path.is_file():pin(path)
        print(folder.name+' actual command/state/contact/recovery/follow-up passed',flush=True)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file:
            path=Path(file).absolute()
            if path.is_relative_to(ROOT/'tools') and path.suffix=='.py':pin(path)
    assembly.need(len(cases)==52 and len(screens)==156,'Complete independent bounded state and scene inventories')
    failures=[s for s in screens if not s['exactRGBPixels']]
    return dict(passed=True,candidate=NAME,scope=__doc__,cases=cases,positiveCases=18,negativeCases=34,
        pairedFields=sum(c['fields'] for c in cases),nativeEvents=sum(c['actualNativeEvents'] for c in cases),
        current52CaseHumanStateMatrixAccepted=True,everyCheckedBuildNativeEventMatched=True,
        onlyNormalizedField='native palette allocation bank',endpointScenes=screens,
        exactCheckedBuildEndpointScenes=sum(s['exactPNGBytes'] for s in screens),
        allEndpointScenesAccepted=not bool(failures),unresolvedEndpointDifferences=failures,
        endpointDifferencesNotSilentlyAccepted=True,wholeActualGuestCapturedByTheseObservers=False,
        freshFullRasterErasureAcceptance=False,allMoveChoreographyAccepted=False,audioAccepted=False,
        CPUAccepted=False,allArenasAccepted=False,fullPortAccepted=False,inputHashes=pins)

if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable new candidate evidence')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report.get(k) for k in ('passed','error','pairedFields','nativeEvents','current52CaseHumanStateMatrixAccepted','exactCheckedBuildEndpointScenes','allEndpointScenesAccepted','unresolvedEndpointDifferences')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
