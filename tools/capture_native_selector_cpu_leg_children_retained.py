"""Latest native Sonya CPU guard-wait route, full child and current byte proofs.

Preserve entire original repeated gate and any KO rejection. Retain all original
native evidence for complete mixed lifecycle qualification without game replay.
"""
import inspect,json,re,traceback
from pathlib import Path
import capture_native_selector_special_shadow as current
import capture_native_kano_laser_cpu_leg_children as previous

ROOT,need,sha=current.ROOT,current.need,current.sha
BASE=ROOT/'audit_native_selector_cpu_leg_children_ram'
OUT=ROOT/'audit_native_selector_cpu_leg_children_repeat_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_leg_children.lua'
KEY='leg_cpu_sonya_p2_human_sonya_p1_children_guard_wait'
RAM_CASES={};COMPLETED=[];NATIVE_HANDLES={}
guest=gfx=gfx32=payload=native=None


def execute(state):
    global guest,gfx,gfx32,payload,native
    need(not BASE.exists()and not OUT.exists()and not current.prior.identity.census(),
         'Fresh latest child-covered Sonya case; previous Kano native terminal')
    proof_path=ROOT/'audit_native_selector_special_visuals_combined_checked/report.json'
    proof=json.loads(proof_path.read_text())
    need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),
         'Whole latest models/build/original human verification sources unchanged')
    original=inspect.getsource(previous.run)
    first=original.index('    source=inspect.getsource(base.capture)')
    last=original.index('    scope=dict(vars(base),BASE=BASE',first)
    adapters='\n'.join(original[first:last].splitlines()[1:])
    adapters=current.replace(adapters,"MK2KS_CPU_PAIR_APPROACH='original'", "MK2KS_CPU_PAIR_APPROACH='guard_wait'")
    factory=inspect.getsource(current.functions)
    boundary="    exec(compile(source,__file__+'::entire_native_capture_plus_full_current_windows_exact_kernel_identity','exec'),scope)"
    factory=current.replace(factory,boundary,adapters+'\n'+boundary)
    scope=dict(vars(current),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,RAM_CASES=RAM_CASES,
        COMPLETED=COMPLETED,NATIVE_HANDLES=NATIVE_HANDLES,WINDOWS=state['WINDOWS'],
        once=current.replace,__file__=__file__)
    exec(compile(factory,__file__+'::whole_latest_collector_whole_child_physical_guard_route','exec'),scope)
    functions=scope['functions']()
    guest,gfx,build,gfx32,payload=(state[k]for k in('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=functions['bindings'](guest,build)
    functions['capture'].__globals__['KEY']=KEY
    need(native.NAME==current.startup.NAME and guest==state['WINDOWS']['high'],
         'Entire current independent models reused; no repeated initializer')
    pins=dict(proof['inputHashes'])
    for p in(Path(__file__),Path(previous.__file__),Path(previous.prior.__file__),
             Path(previous.prior.previous.__file__),proof_path,LUA,
             ROOT/'mk2ks_native_kano_laser_cpu_leg_children.lua',
             ROOT/'mk2ks_native_kano_laser_cpu_leg_repeat_p2.lua',
             ROOT/'mk2ks_cpu_choke_shadow_v5328.lua',ROOT/'mk2ks_cpu_recovery_probe_v1438.lua',
             ROOT/'mk2ks_physical_p2_cpu_overlap_trace_v1999.lua',
             ROOT/'mk2ks_physical_p2_cpu_ring_trace_v2013.lua'):
        pins[str(p.resolve())]=sha(p)
        if p.suffix=='.lua':
            need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)',p.read_text()),
                 'Each loaded physical/passive observer forbids guest/state/register writes')
    check=previous.prior.bindings(guest,'sonya')
    report=functions['capture']('leg',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    need(not current.prior.identity.census()and all(sha(p)==h for p,h in pins.items()),
         'Exact original native terminal and immutable executed sources')
    need(all(p.suffix.lower()not in('.png','.wav','.bin','.exe','.zip')for p in BASE.rglob('*')if p.is_file()),
         'No raw media/build/ROM copies')
    OUT.mkdir()
    current.prior.save(OUT/'report.json'if report['passed']else OUT/'failure.json',dict(
        passed=report['passed'],candidate=native.NAME,key=KEY,originalRepeatedGatePreserved=True,
        nativeExit=report['nativeExit'],originalCaptureError=report.get('error'),
        originalNativeRetainedForWholeLifecycleQualification=True,inputHashes=pins,
        fullPortAcceptance=False,fullAudioAcceptance=False,newBuilds=0,newROMCopies=0,newRawMedia=0,
        publicPlayableChanged=False,goalStatus='active'))
    return report
