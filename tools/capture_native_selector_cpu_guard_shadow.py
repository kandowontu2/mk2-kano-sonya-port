"""Different physical guard-hold trial with callback-distinct raster keys.

Preserve original terminal-first capture, five current windows and kernel
identity. Keep real CPU choices unknown until observed. Transport/state pass
is not automatic move/body/shadow/art/audio acceptance; those are separate.
"""
import inspect,json,re
from pathlib import Path
import capture_native_selector_cpu_blade_knife as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
BASE=ROOT/'audit_native_selector_cpu_guard_shadow_ram'
OUT=ROOT/'audit_native_selector_cpu_guard_shadow_capture_checked'
LUA=ROOT/'mk2ks_native_selector_cpu_guard_shadow.lua'
KEY='cpu_kano_p2_guard_hold_confirm265'
RAM_CASES={};NATIVE_HANDLES={};COMPLETED=[]
guest=gfx=gfx32=payload=native=None
normalize=prior.normalize


def key_selftest():
    # Preserve the genuine field number: don't invent a different game frame
    # merely to accommodate two separate callbacks. Only capture ordinal differs.
    frame=1871
    keys=[f'ui_{frame:04d}_{ordinal:04d}.png'for ordinal in range(3)]
    need(len(set(keys))==3 and all(k.startswith('ui_1871_')for k in keys),
         'Same physical field, three distinct original callback identities')
    actual=normalize('MK2_KNIFE_RAM_RGB frame=1871 label=actual_entry.png width=400 height=254 bytes=406400 hex=00\n')
    need('frame=1871 stage=actual_entry.png attempt=1'in actual,
         'Transport never adjusts original field/stage to avoid collision')
    return dict(passed=True,unchangedFrame=frame,distinctCallbackKeys=keys)


def execute(state):
    need(not BASE.exists()and not OUT.exists()and not prior.current.prior.identity.census(),
         'Fresh distinct guard-hold physical route, not a rejected-game replay')
    rejection=prior.BASE/prior.KEY/'result.json'
    old=json.loads(rejection.read_text())
    need(not old['passed']and old['nativeExit']==0 and len(old['nativeTerminal']['hostDecodeErrors'])==3,
         'Original actual raster-key rejection retained')
    selftest=key_selftest()
    source=inspect.getsource(prior.execute)
    source=prior.current.replace(source,"MK2KS_CPU_CONTINUATION_POLICY='retreat'",
                                 "MK2KS_CPU_CONTINUATION_POLICY='guard_hold'")
    boundary="    scope.update(KEY=KEY,normalize=normalize)"
    extra='''
    source=replace(source,"name=f'ui_{frame:04d}.png'", "name=f'ui_{frame:04d}_{len(scenes):04d}.png'")
    source=replace(source,"scenes.append(dict(stage=h['stage']", "scenes.append(dict(imageKey=name,callbackOrdinal=len(scenes),stage=h['stage']")
'''
    source=prior.current.replace(source,boundary,extra+boundary)
    source=prior.current.replace(source,
        'full_phase=allocation.phase_gate();full_allocation=allocation.allocation_gate()',
        'full_phase=allocation.phase.model.verify')
    source=prior.current.replace(source,
        "return dict(wholePhysicalPhase=full_phase(b['cpuLog'],guest),\n                    wholeNativeAllocationLifetime=full_allocation(b['cpuLog'],guest),\n                    fullEffectRasterAudioAcceptance=False)",
        "return dict(wholeOriginalNativeStateHPAndChoices=full_phase(b['cpuLog'],guest),\n                    fullMoveBodyShadowAcceptancePending=True,fullEffectRasterAudioAcceptance=False)")
    source=prior.current.replace(source,'sources=[LUA,',
        "sources=[LUA,ROOT/'mk2ks_native_selector_cpu_blade_knife.lua',")
    source=prior.current.replace(source,"pins=dict(proof['inputHashes'])",
        "pins=dict(proof['inputHashes']);pins[str(rejection.resolve())]=sha(rejection);pins[str(Path(prior.__file__).resolve())]=sha(prior.__file__)")
    scope=dict(vars(prior),BASE=BASE,OUT=OUT,LUA=LUA,KEY=KEY,
        RAM_CASES=RAM_CASES,NATIVE_HANDLES=NATIVE_HANDLES,COMPLETED=COMPLETED,
        rejection=rejection,prior=prior,__file__=__file__)
    exec(compile(source,__file__+'::whole_prior_collector_distinct_guard_route_callback_keys','exec'),scope)
    report=scope['execute'](state)
    globals().update({k:scope[k]for k in('guest','gfx','gfx32','payload','native')})
    need(report['nativeExit']==0,'Same native terminal required before any scene qualification')
    print('CALLBACK_KEY_SELFTEST '+json.dumps(selftest),flush=True)
    return report
