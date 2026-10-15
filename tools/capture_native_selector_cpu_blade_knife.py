"""Distinct latest CPU projectile trial with full original allocation/phase gates.

Original physical continuation, complete cold proofs and exact kernel identity.
Keep original failures and handles; rasters stay in the existing retained host.
No old runtime pass or old trajectory equality substitutes current acceptance.
"""
import inspect,json,re,sys
from pathlib import Path
import capture_native_selector_special_shadow as current
import verify_current_cpu_blade_allocation_v6333 as allocation

ROOT,need,sha=current.ROOT,current.need,current.sha
BASE=ROOT/'audit_native_selector_cpu_blade_knife_ram'
OUT=ROOT/'audit_native_selector_cpu_blade_knife_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_blade_knife.lua'
KEY='cpu_blade_knife_p2_retreat_confirm265'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[]
guest=gfx=gfx32=payload=native=None


def normalize(line):
    if line.startswith('MK2_KNIFE_RAM_GUEST '):
        return line.replace('MK2_KNIFE_RAM_GUEST ','MK2_HPHASE_GUEST ',1)
    if line.startswith('MK2_KNIFE_RAM_RGB '):
        fields=dict(re.findall(r'(\w+)=([^\s]+)',line))
        need(set(fields)=={'frame','label','width','height','bytes','hex'},
             'Entire original native RGB transport metadata')
        return ('MK2_HPHASE_RGB frame='+fields['frame']+' stage='+fields['label']+
                ' attempt=1 width='+fields['width']+' height='+fields['height']+
                ' bytes='+fields['bytes']+' hex='+fields['hex']+'\n')
    return line


def execute(state):
    global guest,gfx,gfx32,payload,native
    need(not BASE.exists()and not OUT.exists()and not current.prior.identity.census(),
         'Fresh distinct latest physical projectile route, no timeout replay')
    parent=ROOT/'audit_native_selector_special_visuals_combined_checked/report.json'
    proof=json.loads(parent.read_text())
    need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),
         'Whole current independent models/build/human sources unchanged')
    factory=inspect.getsource(current.functions)
    boundary="    exec(compile(source,__file__+'::entire_native_capture_plus_full_current_windows_exact_kernel_identity','exec'),scope)"
    adapters='''
    source=replace(source,"key=f'{move}_p{side}'","key=KEY")
    source=replace(source,"env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM='kitana')",
        "env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='605',MK2KS_CPU_PAIR_CONFIRM_AGE='265',MK2KS_CPU_PAIR_APPROACH='guard_until_close',MK2KS_CPU_CONTINUATION_POLICY='retreat')")
    source=replace(source,'            for line in job.stdout:',
        '            for line in job.stdout:\\n                line=normalize(line)')
    source=replace(source,"s.startswith('MK2_HSPECIAL_RESULT ')","s.startswith('MK2_CPU_PAIR_RESULT ')")
    source=replace(source,"need(len(result)==1 and result[0]['completed']==result[0]['attempt']=='2','Both real physical activation/recovery cycles')",
        "need(len(result)==1 and int(result[0]['frame'])>0,'Original native stop receipt; full gameplay acceptance requires independent entire phase/allocation gates below')")
    source=replace(source,"victim='kitana'","victim='kano'")
    source=replace(source,"report['sourceBoundBodyShadowSemantics']=check(b,guest,payload,gfx32)",
        "b['cpuLog']=text\\n        report['sourceBoundBodyShadowSemantics']=check(b,guest,payload,gfx32)")
    scope.update(KEY=KEY,normalize=normalize)
'''
    factory=current.replace(factory,boundary,adapters+'\n'+boundary)
    scope=dict(vars(current),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,
        WINDOWS=state['WINDOWS'],normalize=normalize,__file__=__file__)
    exec(compile(factory,__file__+'::entire_latest_native_collector_whole_projectile_route','exec'),scope)
    functions=scope['functions']()
    guest,gfx,build,gfx32,payload=(state[k]for k in('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=functions['bindings'](guest,build)
    need(native.NAME==current.startup.NAME and guest==state['WINDOWS']['high'],
         'Retained whole current independent models, no new initializer')
    full_phase=allocation.phase_gate();full_allocation=allocation.allocation_gate()
    def check(b,guest,payload,gfx32):
        return dict(wholePhysicalPhase=full_phase(b['cpuLog'],guest),
                    wholeNativeAllocationLifetime=full_allocation(b['cpuLog'],guest),
                    fullEffectRasterAudioAcceptance=False)
    pins=dict(proof['inputHashes'])
    sources=[LUA,ROOT/'mk2ks_native_shang_drain_startup.lua',
        ROOT/'mk2ks_current_cpu_blade_knife_shadow_v6312.lua',
        ROOT/'mk2ks_current_cpu_blade_allocation_v6340.lua',
        ROOT/'mk2ks_blade_allocation_v2892.lua',
        ROOT/'mk2ks_current_kano_cpu_extended_ram_v6290.lua',
        ROOT/'mk2ks_physical_p2_cpu_continuation_v3300.lua',
        ROOT/'mk2ks_physical_p2_cpu_round_trace_v1940.lua',
        ROOT/'mk2ks_physical_p2_cpu_overlap_trace_v1942.lua',
        ROOT/'mk2ks_physical_p2_cpu_knife_trace_v1955.lua',
        ROOT/'mk2ks_physical_p2_cpu_choice_trace_v3303.lua',
        ROOT/'mk2ks_special_shadow_v5131.lua',
        ROOT/'mk2ks_native_kano_laser_special_shadow.lua']
    for path in sources:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)',path.read_text()),
             'Whole original loaded driver/observer forbids game/register/state writes')
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):
            sources.append(Path(file).resolve())
    for path in [Path(__file__),parent,*sources]:pins[str(path.resolve())]=sha(path)
    report=functions['capture']('blade_knife',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    need(not current.prior.identity.census()and all(sha(p)==h for p,h in pins.items()),
         'Same native terminal and immutable complete executed input inventory')
    OUT.mkdir()
    current.prior.save(OUT/('report.json'if report['passed']else'failure.json'),dict(
        passed=report['passed'],candidate=native.NAME,key=KEY,nativeExit=report['nativeExit'],
        originalCaptureError=report.get('error'),inputHashes=pins,
        completeCurrentColdWindows=True,originalPhysicalControllerPreserved=True,
        actualNativeHandlesAndRastersRetained=True,newBuilds=0,newROMCopies=0,
        newRawMedia=0,newZIPs=0,publicPlayableChanged=False,
        fullEffectRasterAudioAcceptance=False,fullPortAcceptance=False,goalStatus='active'))
    return report
