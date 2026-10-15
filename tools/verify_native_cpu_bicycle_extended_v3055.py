"""Original Bicycle miss phase contract retained on a true extended control.

Whole native state/HP ledgers stay independent of the legacy subsequent-pair
contract. No candidate Bicycle/full CPU/art/audio/KO or finished-port claim.
"""
import inspect,json,sys,traceback
from pathlib import Path
import native_cpu_mobility_capture_contract_v3036 as capture
import native_cpu_bicycle_extended_contract_v3054 as phase
import current_sonya_cpu_bicycle_contract_v2006 as original

ROOT=capture.ROOT;OUT=ROOT/'audit_v3056_native_cpu_bicycle_extended_checked';need=capture.need
CASE='audit_v3029_native_cpu_mobility_old_kano_guard_until_close_retreat'

def original_phase_source():
    source=inspect.getsource(original.verify)
    for before,after in (
      ("pair=state.verify_log(log,'kano',guest)","pair=dict(accepted=False,scope='Full raw native state/HP independently checked; no ordinary paired-contact acceptance substituted')"),
      ("codes=overlap(log,'CODE')","codes=overlap(log,'CODE')+native.rows(log,'MK2_MOBILITY_CODE')"),
      ("r['stop']==0xfff9ad00","r['stop']>=0xfff9ad00"),
      ("falls=[r for r in relevant if r['kind']=='fall'];assert len(falls)==1",
       "falls=[r for r in native.rows(log,'MK2_MOBILITY_EVENT')if r['kind']=='native_fall'and r['move']=='bicycle'and r['actor']==actor and r['main']==main and start<=r['frame']<=end];assert len(falls)==1"),
      ('subsequentPairContractUnchanged=pair','originalPairAndOrdinaryAcceptanceNotSubstituted=True,subsequentPairAcceptance=False')):
        need(before in source,'Declared original context adaptation exists');source=source.replace(before,after)
    need(source.rstrip()==inspect.getsource(phase.verify).rstrip(),'Every original61-field Bicycle rise/seek/ceiling/fall/fractional-landing/lock/ready phase check retained exactly')

def verify():
    original_phase_source();capture.metadata_contract_source();pins={}
    log,guest,case=capture.capture(ROOT/CASE,'old','kano','guard_until_close','retreat',pins)
    typed=phase.verify(log,guest)
    path=ROOT/'audit_v3039_native_cpu_mobility_inventory_checked/report.json';proof=json.loads(path.read_text())
    need(proof['passed']and proof['actualControlBicycleMiss'],'Actual unforced first-chance Bicycle inventory')
    native=proof['cases'][CASE]['branches'];need(len(native)==1 and native[0]['move']=='bicycle'and not native[0]['nativeContact']and
         native[0]['firstRandomResult']==174 and native[0]['secondRandomResult']is None and native[0]['actualCollisionChecks']==13,
         'Actual original four-entry first-chance branch and13missed seek checks, no second chance invented')
    need(typed['fields']==61 and typed['damage']==0 and typed['fractionalLandingY']==40960 and
         typed['originalPairAndOrdinaryAcceptanceNotSubstituted']and not typed['subsequentPairAcceptance'],
         'Actual native full missed Bicycle and fractional landing, not substituted ordinary acceptance')
    for file,wanted in proof['inputHashes'].items():
        need(file not in pins or pins[file]==wanted,'Consistent actual Bicycle source evidence');pins[file]=wanted
    pins[str(path)]=capture.assembly.sha(path)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':pins[str(Path(file).resolve())]=capture.assembly.sha(file)
    for file,wanted in pins.items():need(capture.assembly.sha(file)==wanted,'Immutable actual native Bicycle source/capture '+file)
    case.update(case=CASE,player='kano',build='old',phase=typed,nativeChoice=native[0])
    return dict(passed=True,cases={'old_kano':case},actualPhysicalFixtures=1,originalBicycleMissPhaseChecksRetained=True,
      actualControlBicycleMissAccepted=True,candidateBicycleAccepted=False,gameChanged=False,
      allCPUOrHitArtAudioKOAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual extended Bicycle control proof')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
