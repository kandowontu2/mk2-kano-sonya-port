"""Use latest retained independent models for both-slot real Square contacts.

Distinct physical AIR trials, not replay of the stationary whiff trials.
All original contact/body/shadow/health and24+22+2 fault requirements retained.
Complete initialized windows in each job, exact original handles retained.
"""
import inspect,json,re
from pathlib import Path
from types import FunctionType,SimpleNamespace
import capture_native_selector_special_shadow as current
import capture_native_kano_laser_square_contact as contact

ROOT,need,sha=current.ROOT,current.need,current.sha
BASE=ROOT/'audit_native_selector_square_contact_ram'
OUT=ROOT/'audit_native_selector_square_contact_checked'
CONTACT_CASES={};CONTACT_HANDLES={}


def execute(state):
    need(not BASE.exists()and not OUT.exists()and not current.prior.identity.census(),'Fresh distinct physical airborne contact trials; original16 native jobs terminal')
    previous_path=current.OUT/'report.json';previous=json.loads(previous_path.read_text())
    need(previous['passed']and previous['actualCases']==16 and previous['actualVerifiedSpecialCycles']==32 and
         previous['allEightMovesBothSlotsRepeatRecoverVerified']and
         all(sha(p)==h for p,h in previous['inputHashes'].items())and
         all(sha(p)==h for p,h in previous['outputHashes'].items()),'Actual latest full repeat/body/shadow matrix and unchanged sources')
    factory=inspect.getsource(current.functions)
    before="    exec(compile(source,__file__+'::entire_native_capture_plus_full_current_windows_exact_kernel_identity','exec'),scope)"
    after="    source=replace(source,\"MK2KS_HUMAN_SPECIAL_AIR='0'\",\"MK2KS_HUMAN_SPECIAL_AIR='1'\")\n"+before
    factory=current.replace(factory,before,after)
    namespace=dict(vars(current),BASE=BASE,OUT=OUT,RAM_CASES=CONTACT_CASES,COMPLETED=[],
        NATIVE_HANDLES=CONTACT_HANDLES,WINDOWS=state['WINDOWS'],__file__=__file__)
    exec(compile(factory,__file__+'::whole_latest_capture_original_physical_AIR_branch','exec'),namespace)
    scoped=namespace['functions']();base=SimpleNamespace(**scoped)
    binding=FunctionType(contact.bindings.__code__,dict(contact.bindings.__globals__,base=base),contact.bindings.__name__)
    fault_checks=FunctionType(contact.fault_checks.__code__,dict(contact.fault_checks.__globals__,base=base),contact.fault_checks.__name__)
    guest,gfx,build,gfx32,payload=(state[k]for k in('guest','gfx','build','gfx32','payload'))
    native,human_check,check,decode=binding(guest,build)
    need(native.NAME==current.startup.NAME and state['WINDOWS']['high']==guest,'Same complete latest independent guest models, no repeated initializer')
    pins=dict(previous['inputHashes'])
    for p in (Path(__file__),Path(contact.__file__),Path(current.__file__),previous_path):pins[str(p.resolve())]=sha(p)
    reports=[];faults=[]
    for side in (1,2):
        report=scoped['capture']('square',side,guest,gfx,gfx32,payload,native,check,decode,pins)
        reports.append(report);need(report['passed'],'Actual airborne damage/body/shadow recovery, do not replay on rejection')
        folder,text,images=CONTACT_CASES[f'square_p{side}'];rows=base.defaultdict(list)
        for line in text.splitlines():
            if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):rows[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        actual=dict(move='square',side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,
            streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))
        faults.append(dict(side=side,**fault_checks(actual,guest,payload,gfx32,check)))
    need(not base.identity.census()and all(sha(p)==h for p,h in pins.items()),'Both actual native handles terminal; executed inputs unchanged')
    outputs={str(p.resolve()):sha(p)for p in BASE.rglob('*')if p.is_file()}
    need(all(Path(p).suffix.lower()not in('.png','.wav','.bin','.exe','.zip')for p in outputs),'No raw media/build/ROM copies')
    value=dict(passed=True,candidate=native.NAME,cases=reports,faultChecks=faults,inputHashes=pins,outputHashes=outputs,
        actualPhysicalCases=2,actualAirborneContactCycles=4,actualSquareContactVerified=True,
        everyReadyOwnedBodyShadowFieldSourceBound=True,wholeCurrentInitializedWindowsProvedInEachNativeJob=True,
        fullVisualTimelineAccepted=False,allArenasAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,
        repeatedInitializer=False,publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        goalStatus='active',scope=__doc__)
    OUT.mkdir();current.prior.save(OUT/'report.json',value)
    print(json.dumps(dict(passed=True,actualAirborneContactCycles=4,fullPortAcceptance=False)),flush=True)
    return value
