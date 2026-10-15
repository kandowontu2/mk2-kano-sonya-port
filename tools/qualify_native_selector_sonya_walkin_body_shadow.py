"""Whole native fighter body/ROM/shadow drawing for actual walk-in27520.

Retain the original native geometry equations and all eleven original faults.
The independently captured all-mode fields determine drawing chronology,
owners, true IDs and fixed Main floors; no old throw-floor timeline transfers.
Scope is this actual repeated-choke/missed-Knife sequence, not all arenas,
projectile pixels, artistic scanout, waveform or full-port acceptance.
"""
import copy
import json
import re
import sys
import traceback
from collections import defaultdict
from pathlib import Path
import capture_native_selector_sonya_walkin_kano_cpu as capture
import qualify_native_selector_sonya_walkin_pairs as paired
import qualify_native_selector_opposite_roles_geometry as original

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT/'audit_native_selector_sonya_walkin_body_shadow_checked'
PARENT = paired.OUT/'report.json'
body, current = original.body, original.current


def execute(state):
    need(not OUT.exists(), 'New immutable actual walk-in body/shadow proof')
    parent = json.loads(PARENT.read_text())
    pins = dict(parent['inputHashes'])
    folder, text, images = capture.RAM_CASES[capture.KEY]
    held = capture.NATIVE_HANDLES[capture.KEY]
    meta = json.loads((folder/'result.json').read_text())
    identity = held['identity']
    need(parent['passed'] and meta['passed'] and
         held['process'].poll() == meta['nativeExit'] == 0 and
         identity == parent['actualNativeIdentity'] == meta['nativeTerminal']['actualWindowsIdentity'] and
         (identity['ProcessId'], identity['ParentProcessId'], identity['createdUnix']) ==
         (27520, 38752, 1791760361.8604069) and
         not current.prior.identity.census() and
         all(sha(p) == h for p, h in pins.items()),
         'Same original terminal27520 and complete immutable pair/source inventory')
    rows = defaultdict(list)
    for line in text.splitlines():
        if line.startswith('MK2_HPHASE_'):
            values = re.findall(r'(\w+)=([^\s]+)', line)
            need(len(values) == len(dict(values)), 'Unambiguous complete native drawing record')
            rows[line.split()[0]].append(dict(values))
    bundle = dict(move='knife', side=2, folder=folder, report_path=folder/'result.json',
        report=meta, cpuLog=text, rows=rows,
        streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))
    stock = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for start, end in ((0xff801070, 0xff8017b0), (0xff804160, 0xff804430)):
        lo, hi = (start-0xff800000)//8, (end-0xff800000)//8
        need(state['guest'][lo:hi] == stock[lo:hi],
             'Entire original native body and direct floor-shadow kernels unchanged')
    # This binding changes only the original guard template's actual roles:
    # P1 Sonya18/floor81, P2 Kano17/floor82, and the whole native state ledger.
    # Exact unmodified geometry, packed-ROM row decoding and DMA checks follow.
    check = original.bindings(state['guest'])
    positive = check(bundle, state['guest'], state['payload'], state['gfx32'])
    need(positive['state']['wholeNativeStateHPAndChoices'] == parent['wholeNativeStateHealthChoices'],
         'Independent whole physical/state/HP/choice proof equals actual paired checkpoint')
    need(positive['actualContiguousActorFields'] == 3034 and
         len(positive['state']['expectedNativeDrawingFrames']) == 1517 and
         positive['actualRoutineEntryFrames'] == [2035, 2163, 2256, 3117],
         'Entire independently expected drawing scope, both caught chokes, actual Knife, uncaught third attempt')
    print('Whole actual walk-in fighter body/packed-ROM/shadow positive PASS', flush=True)
    faults = current.prior.shadow_faults(
        dict(bundle, report=dict(meta, sourceBoundBodyShadowSemantics=positive)),
        state['guest'], state['payload'], state['gfx32'], check)
    trials = [
        ('first_held_Sonya_body', 'MK2_HPHASE_CANDIDATE', 'source', '00000000', 2068, 1),
        ('second_held_Sonya_body', 'MK2_HPHASE_CANDIDATE', 'source', '00000000', 2217, 1),
        ('Knife_Kano_body', 'MK2_HPHASE_CANDIDATE', 'source', '00000000', 2272, 2),
        ('Knife_overlap_Sonya_shadow_owner', 'MK2_HPHASE_SHADOW_BEGIN', 'owner', '010350A0', 2272, 1),
        ('Knife_overlap_Kano_shadow_floor', 'MK2_HPHASE_PROJECTION', 'floor', '81', 2272, 2),
        ('second_recovery_Sonya_floor', 'MK2_HPHASE_POST_FIELD', 'floor', '82', 2316, 1),
        ('second_recovery_Sonya_proxy', 'MK2_HPHASE_POST_FIELD', 'id', '1', 2316, 1),
        ('actual_Knife_entry_opcode', 'MK2_HPHASE_CPU_NATIVE_ENTRY', 'opcode', '574B', 2256, 2),
    ]
    extra = []
    for label, tag, key, value, frame, slot in trials:
        changed = dict(bundle, rows=copy.copy(rows))
        changed['rows'][tag] = copy.deepcopy(rows[tag])
        record = next(r for r in changed['rows'][tag] if int(r['frame']) == frame and
                      (tag == 'MK2_HPHASE_CPU_NATIVE_ENTRY' or int(r['slot']) == slot))
        need(record[key] != value, 'Effective actual phase/role corruption, never a no-op')
        record[key] = value
        try:
            check(changed, state['guest'], state['payload'], state['gfx32'])
        except (ValueError, AssertionError) as error:
            extra.append(dict(fault=label, frame=frame, slot=slot, rejectedBy=str(error)))
        else:
            raise ValueError('Actual phase/role geometry corruption admitted '+label)
    need(len(faults) == 11 and len(extra) == 8 and
         check(bundle, state['guest'], state['payload'], state['gfx32']) == positive,
         'All nineteen effective actual geometry faults reject; entire exact positive restored')
    sources = {Path(__file__).resolve(), PARENT.resolve(), (ROOT/'mk2/mk2-maincpu.bin').resolve()}
    for module in tuple(sys.modules.values()):
        name = getattr(module, '__file__', None)
        if name:
            path = Path(name).resolve()
            if path.is_relative_to(ROOT) and path.is_file():
                sources.add(path)
    for path in sources:
        key = str(path); digest = sha(path)
        need(key not in pins or pins[key] == digest, 'No executed or historical source replaced')
        pins[key] = digest
    need(all(sha(p) == h for p, h in pins.items()), 'Whole source/evidence inventory after all faults')
    value = dict(passed=True, goalStatus='active', actualNativeIdentity=identity,
        wholeNativeFighterBodyROMShadow=positive, originalGeometryFaultsRejected=faults,
        actualPairKnifePhaseFaultsRejected=extra, inputHashes=pins,
        requirements=parent['requirements'], remainingGroups=parent['remainingGroups'],
        finiteActualPairKnifeFighterGeometryAccepted=True, allArenaCPUContextsAccepted=False,
        projectilePixelGeometryAccepted=False, finalScanoutArtisticAcceptance=False,
        sourceMixedWaveformAccepted=False, fullPortAcceptance=False, publicPlayableChanged=False,
        newNativeGames=0, newBuilds=0, newROMCopies=0, newRawMediaFiles=0, newZIPs=0)
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(value, indent=2)+'\n')
    print('PASS1517 full native drawing fields, complete fighter bodies/shadows and19 faults', flush=True)
    return value


def safe_execute(state):
    try:
        return execute(state)
    except Exception as error:
        need(not OUT.exists(), 'Preserve original exact qualification failure')
        OUT.mkdir()
        (OUT/'failure.json').write_text(json.dumps(dict(passed=False, error=repr(error),
            traceback=traceback.format_exc(), goalStatus='active', newNativeGames=0,
            fullPortAcceptance=False), indent=2)+'\n')
        raise
