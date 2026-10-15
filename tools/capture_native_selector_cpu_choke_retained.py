"""Actual latest natural CPU Kano mirror: full health/body/shadow and faults.

Reuse retained independent models, not older runtime passes. Whole original
physical close-approach controller; no CPU/HP/position/RNG/state writes.
Current initialized windows and exact native kernel identity in the new job.
"""
import inspect,json,re
from pathlib import Path
from types import FunctionType,SimpleNamespace
import capture_native_selector_special_shadow as current
import capture_native_kano_laser_cpu_choke_shadow as cpu

ROOT,need,sha=current.ROOT,current.need,current.sha
BASE=ROOT/'audit_native_selector_cpu_choke_ram'
OUT=ROOT/'audit_native_selector_cpu_choke_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_choke_shadow.lua'
CPU_CASES={};CPU_HANDLES={}


def execute(state):
    need(not BASE.exists()and not OUT.exists()and not current.prior.identity.census(),'Fresh distinct natural CPU case; all earlier native jobs terminal')
    proof_path=ROOT/'audit_native_selector_special_visuals_combined_checked/report.json';proof=json.loads(proof_path.read_text())
    need(proof['passed']and proof['actualOriginalNativeJobs']==18 and
         all(sha(p)==h for p,h in proof['inputHashes'].items()),'Actual latest full human matrix/source/visual evidence intact')
    # Generate the entire latest collector with original natural CPU adapters.
    cpu_source=inspect.getsource(cpu.run)
    first=cpu_source.index('    source=inspect.getsource(base.capture)');last=cpu_source.index('    reports=[]',first)
    adapters=cpu_source[first:last].splitlines()[1:]
    adapters='\n'.join(adapters)
    need(adapters.count('line.startswith(')==2,'Preserve explicit correction of both original adapter source spellings')
    adapters=adapters.replace('line.startswith(','s.startswith(')
    adapters=current.replace(adapters,"MK2KS_CPU_PAIR_APPROACH='guard_until_close'","MK2KS_CPU_PAIR_APPROACH='original'")
    factory=inspect.getsource(current.functions)
    before="    exec(compile(source,__file__+'::entire_native_capture_plus_full_current_windows_exact_kernel_identity','exec'),scope)"
    factory=current.replace(factory,before,adapters+'\n'+before)
    namespace=dict(vars(current),BASE=BASE,OUT=OUT,LUA=LUA,RAM_CASES=CPU_CASES,COMPLETED=[],NATIVE_HANDLES=CPU_HANDLES,
        WINDOWS=state['WINDOWS'],replace_once=current.replace,human='kano',__file__=__file__)
    exec(compile(factory,__file__+'::entire_latest_native_collector_original_natural_CPU_inputs','exec'),namespace)
    scoped=namespace['functions']();scoped['capture'].__globals__['human']='kano'
    base=SimpleNamespace(**scoped)
    bindings=FunctionType(cpu.bindings.__code__,dict(cpu.bindings.__globals__,base=base),cpu.bindings.__name__)
    guest,gfx,build,gfx32,payload=(state[k]for k in('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=base.bindings(guest,build);check=bindings('kano')
    need(native.NAME==current.startup.NAME and guest==state['WINDOWS']['high'],'Actual retained whole current models, no reinitializer')
    pins=dict(proof['inputHashes'])
    for p in(Path(__file__),Path(cpu.__file__),Path(current.__file__),Path(cpu.cpu_body.__file__),Path(cpu.health.__file__),
        proof_path,LUA,ROOT/'mk2ks_native_kano_laser_cpu_choke_shadow.lua',ROOT/'mk2ks_cpu_choke_shadow_v5328.lua',
        ROOT/'mk2ks_cpu_recovery_probe_v1438.lua'):
        pins[str(p.resolve())]=sha(p)
        if p.suffix=='.lua':need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)',p.read_text()),'Actual loaded CPU controller/passive observer forbids guest/state/register writes')
    report=scoped['capture']('choke',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    need(report['passed'],'Actual latest CPU native pair/health/body/shadow/recovery; never replay rejected game')
    folder,text,images=CPU_CASES['choke_cpu_kano_human_kano'];rows=base.defaultdict(list)
    for line in text.splitlines():
        if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):rows[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    b=dict(move='choke',side=2,human='kano',cpuLog=text,folder=folder,report_path=folder/'result.json',report=report,rows=rows,
        streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))
    positive=check(b,guest,payload,gfx32)
    need(json.loads(json.dumps(positive))==report['sourceBoundBodyShadowSemantics'],'Exact whole original CPU positive after JSON key canonicalization')
    original_source=inspect.getsource(cpu.cpu_body.run);first=original_source.index(' faults=[]');last=original_source.index(' for p,h in b',first)
    block='\n'.join(line[1:]if line.startswith(' ')else line for line in original_source[first:last].splitlines())
    wrapper='def original_faults(b,guest,payload,gfx,case,human):\n'+'\n'.join('    '+line for line in block.splitlines())+'\n    return faults,physical_faults\n'
    closure=dict(zip(check.__code__.co_freevars,(cell.cell_contents for cell in check.__closure__)))
    physical=closure['original_check'].__globals__['cpu'];fault_scope=dict(vars(cpu.cpu_body),check=check,cpu=physical)
    exec(compile(wrapper,__file__+'::entire_original11shadow4physical_CPU_faults','exec'),fault_scope)
    shadows,physical_faults=fault_scope['original_faults'](b,guest,payload,gfx32,positive,'kano')
    need(len(shadows)==11 and len(physical_faults)==4 and check(b,guest,payload,gfx32)==positive,'All15 original actual-row faults; whole positive restored')
    need(not base.identity.census()and all(sha(p)==h for p,h in pins.items()),'Actual native terminal; executed source hashes unchanged')
    outputs={str(p.resolve()):sha(p)for p in BASE.rglob('*')if p.is_file()}
    need(all(Path(p).suffix.lower()not in('.png','.wav','.bin','.exe','.zip')for p in outputs),'No raw media/ROM/build copies')
    value=dict(passed=True,candidate=native.NAME,cases=[report],actualPhysicalCPUChokeCases=1,actualCPUKanoMirrorOnly=True,
        actualBodyShadowFaultsRejected=shadows,actualPhysicalFaultsRejected=physical_faults,inputHashes=pins,outputHashes=outputs,
        wholeNativeHealthHistoryVerified=True,everyReadyOwnedBodyShadowFieldSourceBound=True,
        wholeCurrentInitializedWindowsProvedInNativeJob=True,actualCPUChoicesPrescribed=False,
        allCPUContextsAccepted=False,allArenasAccepted=False,fullVisualTimelineAccepted=False,fullAudioAcceptance=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    OUT.mkdir();base.save(OUT/'report.json',value)
    print(json.dumps(dict(passed=True,actualPhysicalCPUChokeCases=1,actualFaults=15,fullPortAcceptance=False)),flush=True)
    return value
