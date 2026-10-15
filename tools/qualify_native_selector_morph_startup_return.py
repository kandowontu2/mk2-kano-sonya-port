"""Real latest-build Shang/Kano late Cannonball and native timed return.

Retain whole native physical/health/ownership/waveform/delivery models. Bind
only the asset file to the actual current build; no old-build runtime transfer.
Finite actual P1 morph context, not all forms/slots, scanout or full-port proof.
"""
import hashlib
import inspect
import json
import re
import sys
import traceback
from pathlib import Path
import capture_native_selector_morph_startup_return as capture
import qualify_morph_startup_return_v3 as physical_model
import check_morph_startup_return_faults as provenance

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
base = physical_model.previous
OUT = ROOT/'audit_native_selector_morph_startup_return_ball_p1_checked'


def events(c, pins, fields):
    source = inspect.getsource(base.events)
    before = "ROOT/original.prior.mirror.old.current.NAME/'samples/mk2ks/kano_ball_launch.wav'"
    need(source.count(before) == 1, 'Only actual source clip location rebinds; no sound equations change')
    source = source.replace(before, "ROOT/'diagnostic_native_selector_layers_long/samples/mk2ks/kano_ball_launch.wav'", 1)
    scope = dict(vars(base), __file__=__file__)
    exec(compile(source, __file__+'::whole_original_form_sound_current_asset_path', 'exec'), scope)
    return scope['events'](c, pins, fields)


def execute(c):
    need(not OUT.exists(), 'Fresh immutable actual current morph qualification')
    terminal = c['terminal']; identity = terminal['actualWindowsIdentity']
    need(c['report']['passed'] and c['process'].poll() == terminal['nativeExit'] == 0 and
         (identity['ProcessId'], identity['ParentProcessId'], identity['createdUnix']) ==
         (46572, 38752, 1791761737.394802) and not c['decodeErrors'] and
         c['move'] == 'ball' and c['side'] == 1 and
         all(bytes(c['coldBuffers'][k]) == v for k, v in capture.SCOPE['WINDOWS'].items()) and
         not capture.original.original.identity.census(),
         'Exact original terminal46572/latest initialized windows/retained Popen; no replay')
    pins = dict(c['pins'])
    need(all(sha(p) == h for p, h in pins.items()), 'Whole captured current source/candidate inventory')
    physical, fields = physical_model.physical(c)
    inputs = provenance.input_provenance(c, fields)
    sources = events(c, pins, fields)
    owners = base.owners(c, sources)
    print('Latest real Shang/Kano form, late Cannonball, native return and ordinary controls PASS', flush=True)
    waveform = base.predict(c, sources, pins)
    OUT.mkdir()
    (OUT/'waveform.json').write_text(json.dumps(waveform, indent=2)+'\n')
    need(waveform['passed'], 'Every actual native mixed sample equals complete unchanged source model')
    dac_gate, dac_faults = base.original.prior.mirror.qualifier.source_audio.dac_models(len(c['pcmHeaders']))
    dac = dict(positive=dac_gate(c['dac'], c['dacHeaders'], c['pcmHeaders']),
        faults=dac_faults(c['dac'], c['dacHeaders'], c['pcmHeaders']))
    rg, rf = base.original.prior.mirror.qualifier.source_audio.host.models.rom_models(c['expectedROM'])
    rom = dict(positive=[rg(bytes(c['rom'][p]), p) for p in c['rom']],
               faults=[v for p in c['rom'] for v in rf(bytes(c['rom'][p]), p)])
    delivery = base.packets(c['text'])
    restored = physical['originalReturnStoreFrame']+1
    formed = physical['originalForwardStoreFrame']+1
    text = c['text']; faults = []
    def reject(label, tag, predicate, key, value, gate, remove=False):
        changed = provenance.mutate.change(text, tag, predicate, key, value, remove=remove)
        try:
            gate(dict(c, text=changed))
        except (ValueError, AssertionError) as error:
            faults.append(dict(fault=label, rejectedBy=str(error)))
        else:
            raise ValueError('Actual morph corruption admitted '+label)
    for key, value in (('id','17'), ('roster','17'), ('actor','01000000'),
                       ('main','01000000'), ('floor','82'), ('hp','160')):
        reject('restored_'+key, 'MK2_KO_FIELD',
            lambda r: r['frame'] == str(restored) and r['slot'] == '1', key, value,
            physical_model.physical)
    reject('form_proxy', 'MK2_KO_FIELD',
        lambda r: r['frame'] == str(formed) and r['slot'] == '1', 'id', '0', physical_model.physical)
    reject('return_pc', 'MK2_HUMAN_SHANG_STORE', lambda r: r['id'] == '6',
           'pc', 'FFA16710', physical_model.physical)
    reject('return_missing', 'MK2_HUMAN_SHANG_STORE', lambda r: r['id'] == '6',
           'pc', None, physical_model.physical, True)
    reject('walk_input', 'MK2_HUMAN_SHANG_INPUT', lambda r: r['age'] == '1100',
           'buttons', 'Down', physical_model.physical)
    for key, value in (('actor','01000000'), ('id','0')):
        reject('input_'+key, 'MK2_HUMAN_SHANG_INPUT', lambda r: r['age'] == '1100',
               key, value, lambda bad: provenance.input_provenance(bad, fields))
    for key, value in (('actor','01000000'), ('main','01000000'), ('id','17'), ('health','161')):
        reject('retired_source_'+key, 'MK2_INTERRUPT_OWNER',
            lambda r: r['frame'] == str(restored) and r['slot'] == '1', key, value,
            lambda bad: base.owners(bad, sources))
    for key in ('loop','paused'):
        reject('channel_'+key, 'MK2_INTERRUPT_CHANNEL',
            lambda r: r['frame'] == str(restored) and r['channel'] == str(sources[0]['channel']),
            key, '1', lambda bad: base.owners(bad, sources))
    need(len(faults) == 18 and physical_model.physical(c)[0] == physical and
         provenance.input_provenance(c, fields) == inputs and base.owners(c, sources) == owners,
         'All eighteen actual morph faults reject and complete whole positives restored')
    for module in tuple(sys.modules.values()):
        name = getattr(module, '__file__', None)
        if name:
            path = Path(name).resolve()
            if path.is_relative_to(ROOT) and path.is_file():
                key = str(path); digest = sha(path)
                need(key not in pins or pins[key] == digest, 'Every executed local source immutable')
                pins[key] = digest
    for path in c['folder'].rglob('*'):
        if path.is_file(): pins[str(path.resolve())] = sha(path)
    pins[str((OUT/'waveform.json').resolve())] = sha(OUT/'waveform.json')
    need(all(sha(p) == h for p, h in pins.items()), 'Whole source/capture inventory after faults')
    parent = json.loads(capture.PARENT.read_text())
    value = dict(passed=True, goalStatus='active', actualNativeIdentity=identity,
        completePhysicalAndHealthInventory=physical, wholeNativeInputProvenance=inputs,
        completeIndependentOwnership=owners, completeSourceWaveform=waveform,
        sourceDAC=dac, wholeSoundROM=rom, completeNativeDCSDelivery=delivery,
        sourceEvents=[{k:v for k,v in e.items() if k not in ('sample','positions')} for e in sources],
        actualMorphFaultsRejected=faults, inputHashes=pins,
        requirements=parent['requirements'], remainingGroups=parent['remainingGroups'],
        actualLatestP1KanoLateSpecialNativeReturnAccepted=True, allMorphContextsAccepted=False,
        fullRasterAcceptance=False, fullPortAcceptance=False, publicPlayableChanged=False,
        newNativeGamesDuringQualification=0, newBuilds=0, newROMCopies=0, newRawMediaFiles=0, newZIPs=0)
    (OUT/'report.json').write_text(json.dumps(value, indent=2)+'\n')
    print('PASS latest actual native morph/special/return/input/ownership/full source sound and18 faults', flush=True)
    return value


def safe_execute(c):
    try:
        return execute(c)
    except Exception as error:
        if not OUT.exists(): OUT.mkdir()
        need(not (OUT/'failure.json').exists(), 'Preserve exact original morph rejection')
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False, error=repr(error),
            traceback=traceback.format_exc(), actualNativeIdentity=c['terminal']['actualWindowsIdentity'],
            goalStatus='active', newNativeGames=0, fullPortAcceptance=False), indent=2)+'\n')
        raise
