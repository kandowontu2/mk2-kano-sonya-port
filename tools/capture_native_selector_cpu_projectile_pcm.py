"""Current candidate, distinct physical boot607 route, full RAM PCM/DAC/ROM.

Keep entire original terminal-first transport, five current cold windows,
exact kernel identity, native controls/CPU/state/HP and callback-distinct RGB.
Sound transport is NOT waveform/source/ear acceptance. No raw files or replay.
"""
import hashlib,inspect,json,re,sys
from pathlib import Path
import capture_native_selector_special_shadow as current
import capture_native_selector_cpu_blade_knife as physical
import current_tomb_winner_mix_fault_model_v5789 as audio_model

ROOT,need,sha=current.ROOT,current.need,current.sha
BASE=ROOT/'audit_native_selector_cpu_projectile_pcm_ram'
OUT=ROOT/'audit_native_selector_cpu_projectile_pcm_capture_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_projectile_pcm.lua'
KEY='cpu_kano_p2_projectile_pcm_boot607_confirm264'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={}
guest=gfx=gfx32=payload=native=None


def decode_audio(tag,h,raw,expected_guest):
    held=AUDIO[KEY]
    if tag=='MK2_BBAUDIO_PCM':
        need(len(raw)==3840,'Every whole stereo960-frame48kHz sound callback')
        held['pcmChunks'].append(raw);held['pcmHeaders'].append(dict(h))
    elif tag=='MK2_NATIVE_DAC_RAM':
        held['dacChunks'].append(raw);held['dacHeaders'].append(dict(h))
    elif tag=='MK2_NATIVE_DCS_ROM':
        phase=h['phase'];need(phase in held['rom'],'Actual startup/terminal sound ROM phase')
        block=held['rom'][phase];at=int(h['offset'])
        need(at==len(block)and h['size']=='12582912'and h['bytes']=='65536'and
             h['bytewidth']=='2'and h['bitwidth']=='16'and h['writes']=='0'and h['assistance']=='none'and
             raw==held['expectedROM'][at:at+len(raw)],'Every ordered actual sound ROM byte equals independent source')
        block.extend(raw)
    elif tag=='MK2_MAUDIO_GUEST':
        need(not held['audioGuestObserved']and raw==expected_guest,'Entire actual initialized audio guest equals current model')
        held['audioGuestObserved']=True
    else:raise ValueError('Unknown audio transport '+tag)


def functions(state):
    factory=inspect.getsource(current.functions)
    marker="    exec(compile(source,__file__+'::entire_native_capture_plus_full_current_windows_exact_kernel_identity','exec'),scope)"
    adaptations='''
    source=replace(source,"key=f'{move}_p{side}'","key=KEY")
    source=replace(source,"env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM='kitana')",
        "env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='607',MK2KS_CPU_PAIR_CONFIRM_AGE='264',MK2KS_CPU_PAIR_APPROACH='original',MK2KS_CPU_CONTINUATION_POLICY='guard_hold')")
    source=replace(source,'            for line in job.stdout:',
        '            for line in job.stdout:\\n                line=normalize(line)')
    source=replace(source,"name=f'ui_{frame:04d}.png'","name=f'ui_{frame:04d}_{len(scenes):04d}.png'")
    source=replace(source,"scenes.append(dict(stage=h['stage']","scenes.append(dict(imageKey=name,callbackOrdinal=len(scenes),stage=h['stage']")
    before="                        if tag=='MK2_DRAIN_STARTUP':"
    after="""                        if tag in('MK2_BBAUDIO_PCM','MK2_NATIVE_DAC_RAM','MK2_NATIVE_DCS_ROM','MK2_MAUDIO_GUEST'):
                            decode_audio(tag,h,raw,guest)
                        elif tag=='MK2_DRAIN_STARTUP':"""
    source=replace(source,before,after)
    source=replace(source,"s.startswith('MK2_HSPECIAL_RESULT ')","s.startswith('MK2_CPU_PAIR_RESULT ')")
    source=replace(source,"need(len(result)==1 and result[0]['completed']==result[0]['attempt']=='2','Both real physical activation/recovery cycles')",
        "need(len(result)==1 and int(result[0]['frame'])>0,'One original native terminal; sound acceptance remains separate')")
    source=replace(source,"victim='kitana'","victim='kano'")
    source=replace(source,"report['sourceBoundBodyShadowSemantics']=check(b,guest,payload,gfx32)",
        "b['cpuLog']=text\\n        report['sourceBoundBodyShadowSemantics']=check(b,guest,payload,gfx32)")
    scope.update(KEY=KEY,normalize=normalize,decode_audio=decode_audio)
'''
    factory=current.replace(factory,marker,adaptations+'\n'+marker)
    scope=dict(vars(current),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,
        WINDOWS=state['WINDOWS'],normalize=physical.normalize,decode_audio=decode_audio,__file__=__file__)
    exec(compile(factory,__file__+'::whole_terminal_first_current_PCM_collector','exec'),scope)
    return scope['functions']()


def execute(state,preflight=False):
    global guest,gfx,gfx32,payload,native
    need(not BASE.exists()and not OUT.exists()and not current.prior.identity.census(),'Fresh distinct real physical route; no observation-timeout replay')
    parent=ROOT/'audit_native_selector_cpu_first_round_checkpoint_checked/report.json'
    proof=json.loads(parent.read_text())
    need(proof['passed']and all(sha(p)==h for p,h in proof['inputHashes'].items()),'Whole current first-round checkpoint unchanged')
    sources=[LUA,ROOT/'mk2ks_current_tomb_winner_mix_observer_v5779.lua',
        ROOT/'mk2ks_native_selector_cpu_first_round_projectile.lua',ROOT/'mk2ks_native_selector_cpu_startup_guard.lua',
        ROOT/'mk2ks_native_selector_cpu_guard_shadow.lua',ROOT/'mk2ks_native_selector_cpu_blade_knife.lua',
        ROOT/'mk2ks_native_shang_drain_startup.lua',ROOT/'mk2ks_current_cpu_blade_knife_shadow_v6312.lua',
        ROOT/'mk2ks_current_cpu_blade_allocation_v6340.lua',ROOT/'mk2ks_blade_allocation_v2892.lua',
        ROOT/'mk2ks_current_kano_cpu_extended_ram_v6290.lua',ROOT/'mk2ks_physical_p2_cpu_continuation_v3300.lua',
        ROOT/'mk2ks_physical_p2_cpu_round_trace_v1940.lua',ROOT/'mk2ks_physical_p2_cpu_overlap_trace_v1942.lua',
        ROOT/'mk2ks_physical_p2_cpu_knife_trace_v1955.lua',ROOT/'mk2ks_physical_p2_cpu_choice_trace_v3303.lua',
        ROOT/'mk2ks_special_shadow_v5131.lua',ROOT/'mk2ks_native_kano_laser_special_shadow.lua']
    for path in sources:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)',path.read_text()),'Entire original controller/observers have no game-state writes')
    collector=functions(state)
    guest,gfx,build,gfx32,payload=(state[k]for k in('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=collector['bindings'](guest,build)
    need(native.NAME==current.startup.NAME and guest==state['WINDOWS']['high'],'Exact retained independent current candidate')
    pins=dict(proof['inputHashes'])
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(file).resolve())]=sha(file)
    for path in(Path(__file__),parent,*sources):pins[str(path.resolve())]=sha(path)
    expected_rom,_=audio_model.expected_region(pins)
    if preflight:
        return dict(preflightPassed=True,entireCollectorCompiled=True,soundROMBytes=len(expected_rom),
            exactCandidate=native.NAME,newNativeGames=0,inputHashes=pins)
    AUDIO[KEY]=dict(pcmChunks=[],pcmHeaders=[],dacChunks=[],dacHeaders=[],
        rom={p:bytearray()for p in('startup','terminal')},expectedROM=expected_rom,audioGuestObserved=False)
    full_state=physical.allocation.phase.model.verify
    def check(b,guest,payload,gfx32):
        return dict(wholeOriginalNativeStateHPAndChoices=full_state(b['cpuLog'],guest),
            PCMSourceWaveformAcceptancePending=True,fullEffectRasterAudioAcceptance=False)
    report=collector['capture']('projectile_pcm',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    held=AUDIO[KEY]
    need(not current.prior.identity.census()and all(sha(p)==h for p,h in pins.items()),'Same native terminal and complete immutable inventory')
    need(report['passed']and held['audioGuestObserved']and len(held['pcmChunks'])==len(held['dacChunks'])>1000 and
         all(len(raw)==len(expected_rom)for raw in held['rom'].values()),'Whole original current PCM/DAC and both complete actual sound ROM checks retained in RAM')
    OUT.mkdir();receipt=dict(passed=True,goalStatus='active',candidate=native.NAME,key=KEY,
        actualNativeIdentity=NATIVE_HANDLES[KEY]['identity'],nativeExit=report['nativeExit'],
        PCMCallbacks=len(held['pcmChunks']),DACCallbacks=len(held['dacChunks']),
        PCMBytes=sum(map(len,held['pcmChunks'])),DACBytes=sum(map(len,held['dacChunks'])),
        wholeSoundROM=[dict(phase=phase,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),
            everyActualByteSourceCompared=True)for phase,raw in held['rom'].items()],
        PCMSourceWaveformAcceptance=False,PCMArtisticAcceptance=False,fullPortAcceptance=False,
        requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],inputHashes=pins,
        publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    current.prior.save(OUT/'report.json',receipt)
    print('PASS current full-match PCM/DAC transport; source waveform qualification still pending',flush=True)
    return receipt
