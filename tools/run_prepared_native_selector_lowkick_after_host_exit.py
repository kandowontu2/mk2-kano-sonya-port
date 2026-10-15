"""One required corrected physical-input capture after confirmed host loss.

Use the full prepared original collector and independent recovered models.
Never rerun completed matrices, alter guest state, or prescribe CPU outcomes.
Raw display/audio remain in RAM; terminal transport is not full acceptance.
"""
import json
import sys
import traceback
from pathlib import Path

import verify_native_source_sync as sync

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'audit_native_selector_lowkick_after_host_exit_capture_checked'
REPORT = None


def execute(prepared):
    global REPORT
    sync.need(not OUT.exists(), 'Fresh current successor capture evidence')
    state, scope = prepared.STATE, prepared.SCOPE
    sync.need(scope is not None and state, 'Actual successful retained collector preflight')
    import capture_native_selector_sonya_cpu_air_approach as air
    sync.need(not air.sync.FIXED == {} and not air.previous.base.choices.current.prior.identity.census(),
              'No live native game is restarted')
    sync.verify()
    parent = ROOT / 'audit_native_selector_sonya_voice_owner_eof_sealed.json'
    previous = json.loads(parent.read_text())
    sync.need(previous['passed'], 'Preserved previous finite owner receipt, not replayed')
    pins = dict(state['pins'])
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file and Path(file).resolve().is_relative_to(ROOT / 'tools'):
            pins[str(Path(file).resolve())] = sync.sha(file)
    for file in (Path(__file__), parent, prepared.OUT / 'report.json', prepared.LUA,
                 ROOT / 'audit_native_selector_models_after_host_exit_pin_routes/report.json'):
        pins[str(file.resolve())] = sync.sha(file)
    # Original loaded Lua inventory is conserved. Current generated wrapper
    # adds only physical IN2 binding/release and read-only saved owner fields.
    for file, expected in previous['inputHashes'].items():
        if Path(file).suffix == '.lua':
            sync.need(sync.sha(file) == expected, 'Unchanged actually loaded controller/observer source')
            pins[file] = expected
    key = prepared.KEY
    prepared.AUDIO[key] = dict(pcmChunks=[], pcmHeaders=[], dacChunks=[], dacHeaders=[],
                              rom={p: bytearray() for p in ('startup', 'terminal')},
                              expectedROM=state['expectedROM'], audioGuestObserved=False)
    ledger = air.previous.base.choices
    def check(bundle, guest, payload, gfx32):
        whole = ledger.native_state.gate(bundle['cpuLog'], guest)
        choices = ledger.choices_gate(bundle['cpuLog'], guest, whole['schedule'])
        return dict(wholeNativeHealthState=whole, allActuallyObservedChoices=choices,
                    interruptionQualificationPending=True, fullPortAcceptance=False)
    report = scope['capture']('fresh_actual_IN2_lowkick_saved_owners', 2,
                             state['guest'], state['gfx'], state['gfx32'], state['payload'],
                             state['native'], check, state['decode'], pins)
    handle = prepared.NATIVE_HANDLES[key]
    sync.need(handle['process'].poll() == report['nativeExit'], 'Same actual handle genuinely terminal')
    folder, text, images = prepared.RAM_CASES[key]
    errors = (folder / 'stderr.log').read_text()
    sync.need('[LUA ERROR]' not in errors, 'Every actual controller/observer callback completed without Lua error')
    if report['passed']:
        sync.need('MK2_CPU_PAIR_LOWKICK_INPUT ' in text and 'MK2_LOWKICK_BIND count=1' in text,
                  'Corrected one real Low Kick controller actually loaded and observed')
        rows = ledger.native_state.rows
        items = rows(text, 'MK2_VOICE_OWNER_ITEM')
        owners = rows(text, 'MK2_VOICE_OWNER')
        sync.need(len(items) == 5 and {r['field'] for r in items} == {'actor','main','health','id','mode'}
                  and {r['phase'] for r in owners} == {'frame','sound','stop'},
                  'Actual saved layouts and complete observation phases captured')
        sync.need(len(prepared.DISPLAY['rgb']) == 1800 and
                  [int(h['frame']) for h in prepared.DISPLAY['rgbHeaders'].values()] == list(range(1818,3618)),
                  'Whole original dense current display transport retained in RAM')
    for file in folder.rglob('*'):
        if file.is_file():
            pins[str(file.resolve())] = sync.sha(file)
    sync.need(all(sync.sha(p) == h for p, h in pins.items()), 'Whole original/current/new input inventory unchanged')
    REPORT = dict(passed=report['passed'], originalCapture=report,
                  actualNativeIdentity=handle['identity'], nativeExit=report['nativeExit'],
                  inputHashes=pins, goalStatus='active', fullPortAcceptance=False,
                  wholeDisplayedPixelsAccepted=False, wholeSourceAudioAccepted=False,
                  privateOwnerInterruptionAccepted=False, correctedControllerExecuted=True,
                  actualDenseDisplayCallbacks=len(prepared.DISPLAY['rgb']),
                  actualPCMCallbacks=len(prepared.AUDIO[key]['pcmHeaders']),
                  newNativeGames=1, newBuilds=0, newROMCopies=0, newRawMediaFiles=0,
                  newZIPs=0, publicPlayableChanged=False,
                  originalScopeReceipt=str(parent),
                  limitations=['Actual transport/state/choice evidence only; full interruption/display/audio analysis remains.',
                               'Earlier raw RAM was lost with the old host; saved historical proofs are preserved, not represented as recoverable raw buffers.'])
    OUT.mkdir()
    (OUT / ('report.json' if report['passed'] else 'failure.json')).write_text(json.dumps(REPORT, indent=2) + '\n')
    print(json.dumps(dict(passed=report['passed'], actualNativeIdentity=handle['identity'],
                          nativeExit=report['nativeExit'], correctedControllerExecuted=True,
                          denseDisplayCallbacks=REPORT['actualDenseDisplayCallbacks'],
                          fullPortAcceptance=False)), flush=True)
    return REPORT


def safe_execute(prepared):
    try:
        return execute(prepared)
    except Exception as error:
        if not OUT.exists():
            OUT.mkdir()
            (OUT / 'failure.json').write_text(json.dumps(dict(passed=False, error=repr(error),
                traceback=traceback.format_exc(), fullPortAcceptance=False, goalStatus='active'), indent=2) + '\n')
        print(json.dumps(dict(passed=False, error=repr(error), traceback=traceback.format_exc())), flush=True)
        return None
