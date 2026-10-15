"""Distinct original approach/jump-guard continuation, natural CPU choices.

Full original cold proof, physical controller, body/shadow provenance, native
HP/state,19-channel PCM/DAC/ROM and callback-distinct raster transport. This is
not automatic all-move/art/audio acceptance; actual outcomes are not supplied.
"""
import hashlib
import inspect
import json
import re
import sys
from pathlib import Path
import capture_native_selector_cpu_projectile_pcm as original
import capture_native_selector_sonya_cpu_choices as choices

ROOT,need,sha=original.ROOT,original.need,original.sha
BASE=ROOT/'audit_native_selector_sonya_choice_visual_audio_ram'
OUT=ROOT/'audit_native_selector_sonya_choice_visual_audio_capture_checked'
LUA=ROOT/'mk2ks_native_selector_sonya_choice_visual_audio.lua'
KEY='natural_sonya_original_approach_jump_guard_boot608_confirm264'
PARENT=ROOT/'audit_native_selector_existing_sonya_travel_checkpoint_checked/report.json'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[];AUDIO={};SCOPE=None


def prepare(state):
    scope=dict(vars(original),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
               RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,AUDIO=AUDIO,__file__=__file__)
    exec(compile(inspect.getsource(original.decode_audio),__file__+'::whole_original_sound_transport','exec'),scope)
    source=inspect.getsource(original.functions)
    for before,after in (("MK2KS_TEST_BOOT_FRAME='607'","MK2KS_TEST_BOOT_FRAME='608'"),
                         ("MK2KS_CPU_CONTINUATION_POLICY='guard_hold'","MK2KS_CPU_CONTINUATION_POLICY='jump_guard'")):
        source=choices.current.replace(source,before,after)
    exec(compile(source,__file__+'::whole_original_collector_distinct_actual_inputs','exec'),scope)
    return scope['functions'](state)


def execute(state,preflight=False):
    global SCOPE
    need(not BASE.exists() and not OUT.exists() and not choices.current.prior.identity.census(),
         'Fresh distinct actual input policy, never replay solely an observation timeout')
    parent=json.loads(PARENT.read_text());pins=dict(parent['inputHashes'])
    need(parent['passed'] and all(sha(p)==h for p,h in pins.items()), 'Entire preceding source/evidence checkpoint')
    need(choices.migration.verify()['passed'],'Current canonical/compiled sources independently synchronized')
    sources=[LUA,*(ROOT/name for name in (
        'mk2ks_native_selector_cpu_projectile_pcm_startup_direct.lua','mk2ks_native_selector_cpu_projectile_pcm.lua',
        'mk2ks_current_tomb_winner_mix_observer_v5779.lua','mk2ks_native_selector_sonya_cpu_choices.lua',
        'mk2ks_native_selector_cpu_first_round_projectile.lua','mk2ks_native_selector_cpu_startup_guard.lua',
        'mk2ks_native_selector_cpu_guard_shadow.lua','mk2ks_native_selector_cpu_blade_knife.lua',
        'mk2ks_native_shang_drain_startup.lua','mk2ks_current_cpu_blade_knife_shadow_v6312.lua',
        'mk2ks_current_cpu_blade_allocation_v6340.lua','mk2ks_blade_allocation_v2892.lua',
        'mk2ks_current_kano_cpu_extended_ram_v6290.lua','mk2ks_physical_p2_cpu_continuation_v3300.lua',
        'mk2ks_physical_p2_cpu_round_trace_v1940.lua','mk2ks_physical_p2_cpu_overlap_trace_v1942.lua',
        'mk2ks_physical_p2_cpu_knife_trace_v1955.lua','mk2ks_physical_p2_cpu_choice_trace_v3303.lua',
        'mk2ks_special_shadow_v5131.lua','mk2ks_native_kano_laser_special_shadow.lua'))]
    for path in sources:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)',path.read_text()),
             'All loaded controls/observers have no game/register/state writes')
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):sources.append(Path(file).resolve())
    for path in [Path(__file__),PARENT,*sources]:
        key=str(path.resolve());digest=sha(path)
        need(key not in pins or pins[key]==digest,'Never silently replace historical source pin')
        pins[key]=digest
    expected_rom,_=original.audio_model.expected_region(pins)
    SCOPE=prepare(state)
    guest,gfx,build,gfx32,payload=(state[k] for k in ('guest','gfx','build','gfx32','payload'))
    native,_,_,decode=SCOPE['bindings'](guest,build)
    need(native.NAME==choices.current.startup.NAME and guest==state['WINDOWS']['high'],'Same independent complete current candidate')
    if preflight:return dict(passed=True,preflight=True,inputHashes=pins,newNativeGames=0)
    AUDIO[KEY]=dict(pcmChunks=[],pcmHeaders=[],dacChunks=[],dacHeaders=[],
                   rom={p:bytearray() for p in ('startup','terminal')},expectedROM=expected_rom,audioGuestObserved=False)
    def check(b,guest,payload,gfx32):
        whole=choices.native_state.gate(b['cpuLog'],guest)
        branches=choices.choices_gate(b['cpuLog'],guest,whole['schedule'])
        return dict(wholeNativeStateHealth=whole,actualNaturalSonyaChoices=branches,
                    wholeMoveArtAudioAcceptance=False,fullPortAcceptance=False)
    report=SCOPE['capture']('sonya_choices_visual_audio',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    held=AUDIO[KEY]
    need(NATIVE_HANDLES[KEY]['process'].poll()==report['nativeExit'] and not choices.current.prior.identity.census(),
         'Original native handle genuinely terminal, not a timeout replay')
    OUT.mkdir()
    receipt=dict(passed=report['passed'],originalCaptureError=report.get('error'),
                 actualNativeIdentity=NATIVE_HANDLES[KEY]['identity'],nativeExit=report['nativeExit'],
                 qualification=report.get('sourceBoundBodyShadowSemantics'),inputHashes=pins,
                 PCMCallbacks=len(held['pcmChunks']),DACCallbacks=len(held['dacChunks']),
                 wholeSoundROM=[dict(phase=p,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper())
                                for p,raw in held['rom'].items()],originalRGBCallbacks=len(report['actualScenes']),
                 requirements=parent['requirements'],remainingGroups=parent['remainingGroups'],goalStatus='active',
                 waveformAcceptance=False,allMovesArtAudioAccepted=False,fullPortAcceptance=False,
                 publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    choices.current.prior.save(OUT/('report.json' if report['passed'] else 'failure.json'),receipt)
    return receipt
