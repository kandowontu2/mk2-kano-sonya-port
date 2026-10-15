"""Native choices and complete whole source/state/HP after normal human holds."""
import json,sys,traceback
from pathlib import Path
import native_cpu_human_close_capture_contract_v3124 as capture
import verify_native_cpu_mobility_inventory_v3038 as choices
import run_native_cpu_human_close_dispatch_v3121 as dispatch
ROOT=capture.ROOT;OUT=ROOT/'audit_v3126_native_cpu_human_close_inventory_checked';need=capture.need
def verify():
    capture.input_source();pins={};cases={}
    for player,approach,policy in dispatch.CASES:
        folder=ROOT/dispatch.name((player,approach,policy))
        log,guest,case=capture.capture(folder,'new',player,approach,policy,pins)
        native=choices.native_choices(log,guest,player)
        case.update(case=folder.name,branches=native,policy=policy,
          actualBicycleEntries=sum(r['move']=='bicycle'for r in native),fullContactPhaseOrArtAudioAccepted=False)
        cases[policy]=case
        print(policy+': '+str([(r['move'],r['start'],r['nativeContact'])for r in native]),flush=True)
    path=dispatch.OUT/'report.json';runner=json.loads(path.read_text())
    need(runner['allRunnersTerminal']and runner['allRunnerExitsZero'],'Both real games terminal zero')
    pins[str(path)]=capture.assembly.sha(path);pins[str(Path(dispatch.__file__).resolve())]=runner['sourceSHA256']
    pins[str(dispatch.OUT/Path(dispatch.__file__).name)]=runner['sourceSHA256']
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':pins[str(Path(file).resolve())]=capture.assembly.sha(file)
    for file,wanted in pins.items():need(capture.assembly.sha(file)==wanted,'Immutable genuine human hold evidence '+file)
    return dict(passed=True,cases=cases,actualPhysicalFixtures=2,wholeNativeStateHealthSourceAndChoicesAccepted=True,
      originalNativeObserverBodiesUnchanged=True,onlyPhysicalHumanButtonsChanged=True,
      CPUIdentityOrMoveOrRNGPrescribed=False,gameChanged=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual native human hold inventory')
    try:value=verify()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in('cases','inputHashes','scope')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
