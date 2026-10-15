"""Fresh retained-host collector preparation, without replaying old games.

Use recovered independent windows and the full original collector. Avoid
historical import-time live-handle guards, which cannot describe an exited
host. Corrected IN2 controls remain unchanged; native execution is separate.
"""
import inspect
import json
import traceback
from pathlib import Path
from types import FunctionType

import verify_native_source_sync as sync

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'audit_native_selector_lowkick_after_host_exit_preflight'
BASE = ROOT / 'audit_native_selector_lowkick_after_host_exit_ram'
LUA = ROOT / 'mk2ks_native_selector_sonya_cpu_lowkick_owners_bound.lua'
KEY = 'fresh_host_Kano_actual_IN2_lowkick_natural_Sonya_CPU_saved_owners'
RAM_CASES, NATIVE_HANDLES, COMPLETED, AUDIO = {}, {}, [], {}
STATE, SCOPE, DISPLAY = {}, None, None


def prepare(windows):
    global SCOPE, DISPLAY
    sync.need(not OUT.exists() and not BASE.exists(), 'Fresh successor preflight, no overwritten evidence')
    OUT.mkdir()
    try:
        provenance = sync.verify()
        import capture_native_selector_sonya_cpu_air_approach as air
        sync.need(not air.sync.REPORTS == {}, 'Full source provenance verifier present')
        DISPLAY = dict(buffers=air.snapshot.RAMBuffers(), headers={}, gfx={}, rgb={}, rgbHeaders={})
        f = air.snapshot.transport.normalize
        normalize = FunctionType(f.__code__, dict(f.__globals__, DISPLAY=DISPLAY), f.__name__, f.__defaults__)
        source = inspect.getsource(air.prepare)
        old = 'inspect.getsource(previous.prepare)'
        sync.need(source.count(old) == 1, 'Retrieve the preserved actual defining factory, not generated line metadata')
        source = source.replace(old, 'inspect.getsource(previous.original.prepare)', 1)
        namespace = dict(vars(air), BASE=BASE, OUT=OUT, LUA=LUA, KEY=KEY, RAM_CASES=RAM_CASES,
                         NATIVE_HANDLES=NATIVE_HANDLES, COMPLETED=COMPLETED, AUDIO=AUDIO,
                         DISPLAY=DISPLAY, normalize=normalize, __file__=__file__)
        exec(compile(source, __file__ + '::unchanged_full_collector_fresh_namespace', 'exec'), namespace)
        import capture_native_selector_special_shadow as current
        build = json.loads((ROOT / current.startup.NAME / 'build-info.json').read_text(encoding='utf-8-sig'))
        cold = json.loads((current.startup.OUT / 'report.json').read_text())
        sync.need({k: current.startup.initial.digest(v) for k, v in windows.items()} == cold['actualWindowHashes'],
                  'All recovered independent models equal current full initialized window contracts')
        gfx = current.models.prior.native_base.ui.graphics.expected_gfx()
        STATE.update(guest=windows['high'], gfx=gfx, build=build, WINDOWS=windows,
                     payload=(ROOT / current.startup.NAME / 'roms/mk2ks/mk2ks.mdata').read_bytes())
        SCOPE = namespace['prepare'](STATE)
        native, _, _, decode = SCOPE['bindings'](STATE['guest'], build)
        pins = {str(Path(__file__).resolve()): sync.sha(__file__), str(LUA): sync.sha(LUA)}
        STATE['gfx32'] = SCOPE['reconstruct'](native, pins)
        expected_rom, _ = air.previous.base.original.audio_model.expected_region(pins)
        STATE.update(native=native, decode=decode, pins=pins, expectedROM=expected_rom)
        lua = LUA.read_text()
        sync.need("manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']" in lua,
                  'Prepared original correction binds real IN2 Low Kick')
        report = dict(passed=True, preflightOnly=True, nativeRuntimeAccepted=False,
                      fullPortAcceptance=False, goalStatus='active', currentSourceSync=provenance,
                      newNativeGames=0, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                      independentModelBytes={k: len(v) for k, v in windows.items()},
                      graphicsBytes=len(STATE['gfx32']), soundROMBytes=len(expected_rom),
                      inputHashes=pins, correctedControllerExecuted=False,
                      reason='Old host and terminal confirmed gone; prepare one genuinely required corrected-control capture, not completed-case replay')
        (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(dict(passed=True, preflightOnly=True, newNativeGames=0,
                              graphicsBytes=report['graphicsBytes'], soundROMBytes=report['soundROMBytes'])), flush=True)
        return report
    except Exception as error:
        (OUT / 'failure.json').write_text(json.dumps(dict(passed=False, error=repr(error),
            traceback=traceback.format_exc(), newNativeGames=0, nativeRuntimeAccepted=False,
            fullPortAcceptance=False), indent=2) + '\n')
        print(json.dumps(dict(passed=False, error=repr(error), traceback=traceback.format_exc())), flush=True)
        return None
