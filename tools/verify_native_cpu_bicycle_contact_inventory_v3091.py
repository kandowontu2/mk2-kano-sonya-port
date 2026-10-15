"""Actual native mobility outcomes after physical selection-timing variation.

Whole source/state/health/native choices, not full hit/render/audio acceptance.
Every fixture must really select CPU Sonya through normal cold UI; misses are
not reclassified as hits and no next-move criterion is forced into gameplay.
"""
import json,sys,traceback
from pathlib import Path
import native_cpu_mobility_timing_capture_contract_v3090 as capture
import verify_native_cpu_mobility_inventory_v3038 as choices
import run_native_cpu_bicycle_contact_dispatch_v3087 as dispatch
ROOT=capture.ROOT;OUT=ROOT/'audit_v3092_native_cpu_bicycle_contact_inventory_checked';need=capture.need
def verify():
    capture.metadata_contract_source();pins={};cases={}
    path=dispatch.OUT/'report.json';runner=json.loads(path.read_text())
    need(runner['allRunnersTerminal']and runner['allRunnerExitsZero']and len(runner['cases'])==2,'Both original-input matches terminal zero')
    for setup in dispatch.CASES:
        build,player,approach,policy,boot,age=setup;folder=ROOT/dispatch.name(setup)
        log,guest,case=capture.capture(folder,build,player,approach,policy,pins,boot,age)
        native=choices.native_choices(log,guest,player)
        case.update(case=folder.name,boot=boot,confirmAge=age,branches=native,
          actualBicycleEntries=sum(r['move']=='bicycle'for r in native),
          actualSquareEntries=sum(r['move']=='square'for r in native),
          noBicycleScenario=not any(r['move']=='bicycle'for r in native),
          fullMobilityPhaseArtAudioAccepted=False)
        cases[str(age)]=case
        print(folder.name+': actual branches '+str([(r['move'],r['start'],r['nativeContact'])for r in native]),flush=True)
    pins[str(path)]=capture.assembly.sha(path)
    pins[str(Path(dispatch.__file__).resolve())]=runner['sourceSHA256']
    pins[str(dispatch.OUT/Path(dispatch.__file__).name)]=runner['sourceSHA256']
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':pins[str(Path(file).resolve())]=capture.assembly.sha(file)
    for file,wanted in pins.items():need(capture.assembly.sha(file)==wanted,'Immutable genuine timing/whole-state evidence '+file)
    return dict(passed=True,cases=cases,actualPhysicalFixtures=2,wholeNativeStateHealthSourceAndChoicesAccepted=True,
      actualBicycleEntries=sum(c['actualBicycleEntries']for c in cases.values()),
      actualSquareEntries=sum(c['actualSquareEntries']for c in cases.values()),
      originalPhysicalDriverUnchanged=True,guestStateAIHealthStageRNGChanged=False,
      fullContactPhaseOrArtAudioOrPortAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
    need(not OUT.exists(),'Immutable genuine contact discovery verification')
    try:value=verify()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('cases','inputHashes','scope')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
