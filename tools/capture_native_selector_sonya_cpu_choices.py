"""Distinct guard-until-close/neutral continuation; true natural Sonya choices.

Preserve original physical controller and Kano-only choice result. Observe
Sonya in an additional passive tag, never supply CPU/HP/RNG/position/state.
Whole original health/state gates and exact terminal identity are retained.
"""
import inspect
import json
import re
import sys
from pathlib import Path
import capture_native_selector_special_shadow as current
import capture_native_selector_cpu_blade_knife as physical
import qualify_native_selector_natural_state_health_bound as native_state
import verify_current_existing_cpu_leg_choices_v6274 as original_choices
import verify_native_source_sync as migration

ROOT, need, sha = current.ROOT, current.need, current.sha
BASE = ROOT / 'audit_native_selector_sonya_cpu_choices_ram'
OUT = ROOT / 'audit_native_selector_sonya_cpu_choices_checked'
LUA = ROOT / 'mk2ks_native_selector_sonya_cpu_choices.lua'
KEY = 'human_kano_cpu_natural_guard_until_close_neutral_boot608_confirm264'
RAM_CASES, NATIVE_HANDLES, COMPLETED = {}, {}, []
PARENT = ROOT / 'audit_native_selector_natural_state_health_checkpoint_checked/report.json'
SCOPE = None


def choices_gate(text, guest, schedule):
    source = inspect.getsource(original_choices.choice_gate)
    before = "n(r,'schedule')==0xfffa3180"
    need(source.count(before) == 1, 'Only old fixed native schedule context')
    source = source.replace(before, "n(r,'schedule')==schedule", 1)
    scope = dict(original_choices.choice_gate.__globals__, schedule=schedule)
    exec(compile(source, __file__ + '::whole_original_native_choice_gate', 'exec'), scope)
    rows = native_state.rows(text, 'MK2_SONYA_CHOICE_EVENT')
    actual = scope['choice_gate'](rows, guest)
    result = native_state.rows(text, 'MK2_SONYA_CHOICE_RESULT')
    need(len(result) == 1 and int(result[0]['choices']) == len(actual),
         'Every actual native serial accounted, no inferred CPU execution')
    code = native_state.rows(text, 'MK2_SONYA_CHOICE_CODE')
    need(len(code) == 2, 'Whole original router and RNG code checkpoints')
    for row in code:
        lo, hi = (int(row[k], 16) for k in ('start', 'stop'))
        raw = bytes.fromhex(''.join(word[2:] + word[:2] for word in row['words'].split(',')))
        need(raw == guest[(lo-0xff800000)//8:(hi-0xff800000)//8],
             'Every actual router/RNG word independently source-bound')
    return dict(actualNativeChoices=actual, observedMoves=sorted({r['move'] for r in actual}),
                wholeOriginalChoiceLogicRetained=True, fullMoveAcceptance=False)


def prepare(state):
    factory = inspect.getsource(current.functions)
    marker = "    exec(compile(source,__file__+'::entire_native_capture_plus_full_current_windows_exact_kernel_identity','exec'),scope)"
    adaptations = '''
    source=replace(source,"key=f'{move}_p{side}'","key=KEY")
    source=replace(source,"env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM='kitana')",
        "env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='608',MK2KS_CPU_PAIR_CONFIRM_AGE='264',MK2KS_CPU_PAIR_APPROACH='guard_until_close',MK2KS_CPU_CONTINUATION_POLICY='neutral_hold')")
    source=replace(source,'            for line in job.stdout:',
        '            for line in job.stdout:\\n                line=normalize(line)')
    source=replace(source,"name=f'ui_{frame:04d}.png'","name=f'ui_{frame:04d}_{len(scenes):04d}.png'")
    source=replace(source,"scenes.append(dict(stage=h['stage']","scenes.append(dict(imageKey=name,callbackOrdinal=len(scenes),stage=h['stage']")
    source=replace(source,"s.startswith('MK2_HSPECIAL_RESULT ')","s.startswith('MK2_CPU_PAIR_RESULT ')")
    source=replace(source,"need(len(result)==1 and result[0]['completed']==result[0]['attempt']=='2','Both real physical activation/recovery cycles')",
        "need(len(result)==1 and int(result[0]['frame'])>0,'Original physical full-match terminal; completed grab acceptance separate')")
    source=replace(source,"victim='kitana'","victim='kano'")
    source=replace(source,"report['sourceBoundBodyShadowSemantics']=check(b,guest,payload,gfx32)",
        "b['cpuLog']=text\\n        report['sourceBoundBodyShadowSemantics']=check(b,guest,payload,gfx32)")
    scope.update(KEY=KEY,normalize=normalize)
'''
    factory = current.replace(factory, marker, adaptations + '\n' + marker)
    scope = dict(vars(current), BASE=BASE, OUT=OUT, LUA=LUA, KEY=KEY,
                 RAM_CASES=RAM_CASES, NATIVE_HANDLES=NATIVE_HANDLES, COMPLETED=COMPLETED,
                 WINDOWS=state['WINDOWS'], normalize=physical.normalize, __file__=__file__)
    exec(compile(factory, __file__ + '::whole_original_terminal_collector', 'exec'), scope)
    return scope['functions']()


def execute(state, preflight=False):
    global SCOPE
    need(not BASE.exists() and not OUT.exists() and not current.prior.identity.census(),
         'Fresh distinct actual input strategy, not timeout replay')
    parent = json.loads(PARENT.read_text())
    pins = dict(parent['inputHashes'])
    need(parent['passed'] and all(sha(p) == h for p,h in pins.items()),
         'Previous whole state/health/RGB checkpoint inputs unchanged')
    need(migration.verify()['passed'], 'Current canonical/compiled sources independently synchronized')
    sources = [LUA, *(ROOT / name for name in (
        'mk2ks_native_selector_cpu_first_round_projectile.lua',
        'mk2ks_native_selector_cpu_startup_guard.lua', 'mk2ks_native_selector_cpu_guard_shadow.lua',
        'mk2ks_native_selector_cpu_blade_knife.lua', 'mk2ks_native_shang_drain_startup.lua',
        'mk2ks_current_cpu_blade_knife_shadow_v6312.lua', 'mk2ks_current_cpu_blade_allocation_v6340.lua',
        'mk2ks_blade_allocation_v2892.lua', 'mk2ks_current_kano_cpu_extended_ram_v6290.lua',
        'mk2ks_physical_p2_cpu_continuation_v3300.lua', 'mk2ks_physical_p2_cpu_round_trace_v1940.lua',
        'mk2ks_physical_p2_cpu_overlap_trace_v1942.lua', 'mk2ks_physical_p2_cpu_knife_trace_v1955.lua',
        'mk2ks_physical_p2_cpu_choice_trace_v3303.lua', 'mk2ks_special_shadow_v5131.lua',
        'mk2ks_native_kano_laser_special_shadow.lua'))]
    for path in sources:
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)', path.read_text()),
             'Whole loaded physical controller/passive observers have no game/register writes')
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file and Path(file).resolve().is_relative_to(ROOT / 'tools'):
            sources.append(Path(file).resolve())
    for path in [Path(__file__), PARENT, *sources]:
        key = str(path.resolve()); digest = sha(path)
        need(key not in pins or pins[key] == digest, 'Never silently replace historical input pin')
        pins[key] = digest
    SCOPE = prepare(state)
    guest,gfx,build,gfx32,payload = (state[k] for k in ('guest','gfx','build','gfx32','payload'))
    native,_,_,decode = SCOPE['bindings'](guest,build)
    need(native.NAME == current.startup.NAME and guest == state['WINDOWS']['high'],
         'Same complete current independent candidate')
    if preflight:
        return dict(passed=True, preflight=True, inputHashes=pins, newNativeGames=0)
    def check(b, guest, payload, gfx32):
        whole = native_state.gate(b['cpuLog'], guest)
        choices = choices_gate(b['cpuLog'], guest, whole['schedule'])
        return dict(wholeOriginalNativeHealthState=whole, actualNaturalSonyaChoices=choices,
                    fullEffectRasterAudioAcceptance=False, completedGrabAcceptance=False)
    report = SCOPE['capture']('natural_sonya_choices',2,guest,gfx,gfx32,payload,native,check,decode,pins)
    need(NATIVE_HANDLES[KEY]['process'].poll() == report['nativeExit'] and
         not current.prior.identity.census(), 'Original handle really terminal, no replay')
    OUT.mkdir()
    current.prior.save(OUT / ('report.json' if report['passed'] else 'failure.json'), dict(
        passed=report['passed'], originalCaptureError=report.get('error'),
        actualNativeIdentity=NATIVE_HANDLES[KEY]['identity'], nativeExit=report['nativeExit'],
        qualification=report.get('sourceBoundBodyShadowSemantics'), inputHashes=pins,
        originalRGBCallbacks=len(report['actualScenes']), requirements=parent['requirements'],
        remainingGroups=parent['remainingGroups'], goalStatus='active', fullPortAcceptance=False,
        publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0))
    return report
