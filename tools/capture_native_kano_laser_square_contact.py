"""Two physical airborne Square Wave contacts per player slot, current candidate.

Preserves the entire original physical controller and body/shadow checks.
Only the already-present AIR option and explicitly audited contact expectations
change; no guest writes, forced actor states, or replay of terminal processes.
"""
import code
import copy
import inspect
import json
import os
import traceback
from pathlib import Path
from types import SimpleNamespace
import capture_native_kano_laser_special_shadow as base

ROOT, need, sha = base.ROOT, base.need, base.sha
BASE = ROOT / 'audit_native_kano_laser_square_contact_ram'
OUT = ROOT / 'audit_native_kano_laser_square_contact_checked'
INIT = ROOT / 'audit_native_kano_laser_square_contact_initializer_source'
RAM_CASES = {}


def replace_once(source, before, after):
    need(source.count(before) == 1, 'Exact unique original expectation adaptation')
    return source.replace(before, after)


def bindings(guest, build):
    native, _, _, decode = base.bindings(guest, build)
    source = inspect.getsource(base.human.check)
    source = replace_once(source, '  schedule=[]',
                          "  schedule=[(c+age,3-side,'Up')for age in range(3)]")
    source = replace_once(source,
        "need((victim_damage==0)if move=='square'else(victim_damage>0),'Observed stationary square whiff distinguished from genuine damaging moves')",
        "need(move=='square'and victim_damage>0,'Both physical airborne Square Wave cycles genuinely damage the opponent')")
    source = replace_once(source, "actualSquareContactVerified=False if move=='square'else None",
                          "actualSquareContactVerified=True")
    scope = dict(vars(base.human), native=native)
    exec(compile(source, __file__ + '::whole_original_semantics_airborne_expectations', 'exec'), scope)
    original_air = scope['check']

    def human_check(b, guest, payload):
        rows = b['rows']
        need(b['move'] == 'square' and all(t['air'] == '1' for tag, records in rows.items()
             if tag.startswith('MK2_HSPECIAL_') for t in records), 'Actual original AIR controller branch')
        result = original_air(b, guest, payload)
        before = {(int(t['frame']), int(t['slot'])): t for t in rows['MK2_HSPECIAL_FIELD']}
        for cycle in result['cycles']:
            contacts = [t for t in rows['MK2_HSPECIAL_HEALTH']
                        if cycle['entry'] <= int(t['frame']) < cycle['recovered'] and
                        int(t['slot']) == 3-b['side'] and int(t['after']) < int(t['before'])]
            need(contacts and any(int(before[int(t['frame']), 3-b['side']]['y']) <
                                  int(before[int(t['frame']), 3-b['side']]['floor']) for t in contacts),
                 'Each cycle has a genuine native damage write while the physical opponent is airborne')
            cycle['nativeAirborneDamageFrames'] = [int(t['frame']) for t in contacts]
        return result

    scope = dict(vars(base.shadow), human=SimpleNamespace(SPECS=base.human.SPECS, check=human_check))
    exec(compile(inspect.getsource(base.shadow.check), __file__ + '::whole_original_body_shadow_check', 'exec'), scope)
    return native, human_check, scope['check'], decode


def fault_checks(b, guest, payload, gfx32, check):
    faults = base.shadow_faults(b, guest, payload, gfx32, check)
    # Entire original twelve Square Wave semantic mutations. The command
    # mutation targets the selected actor, not the newly explicit victim jump.
    source = inspect.getsource(base.human.main)
    first = source.index('   tests=[]')
    last = source.index('   print(', first)
    block = source[first:last]
    block = '\n'.join(line[3:] if line.startswith('   ') else line for line in block.splitlines())
    block = replace_once(block,
        "if int(t['frame'])==int(b['rows']['MK2_HSPECIAL_COMMAND'][0]['frame'])",
        "if int(t['frame'])==int(b['rows']['MK2_HSPECIAL_COMMAND'][0]['frame'])and int(t['slot'])==side")
    wrapper = 'def original_faults(b,guest,payload,side,move):\n    faults=[]\n' + \
              '\n'.join('    '+line for line in block.splitlines()) + '\n    return faults\n'
    scope = dict(vars(base.human), check=lambda actual, g, p: check(actual, g, p, gfx32))
    exec(compile(wrapper, __file__+'::entire_original_square_semantic_faults', 'exec'), scope)
    semantic = scope['original_faults'](b, guest, payload, b['side'], 'square')
    need(len(semantic) == 12, 'All twelve original semantic faults retained')
    # An opponent jump is mandatory in the positive contact trial.
    changed = copy.deepcopy(b)
    index = next(i for i,t in enumerate(changed['rows']['MK2_HSPECIAL_INPUT'])
                 if t['button'] == 'Up' and int(t['slot']) == 3-b['side'])
    changed['rows']['MK2_HSPECIAL_INPUT'].pop(index)
    try:
        check(changed, guest, payload, gfx32)
    except ValueError as error:
        semantic.append(dict(move='square', side=b['side'], fault='missing_physical_victim_jump', rejectedBy=str(error)))
    else:
        raise ValueError('Missing physical victim jump accepted')
    return dict(originalShadowFaults=faults, originalSemanticFaultsAndVictimJump=semantic)


def run():
    need(not BASE.exists() and not OUT.exists() and not base.identity.census(), 'Fresh airborne-contact leaves')
    previous_path = ROOT / 'audit_native_kano_laser_special_shadow_checked/report.json'
    previous = json.loads(previous_path.read_text())
    guard = json.loads(base.GUARD.read_text())
    need(previous['passed'] and guard['passed'] and guard['actualNativeParserAccepted'] and
         guard['wholePhysicalSpecialShadowByteIdentical'] and not guard['gameplayAccepted'] and
         all(sha(p) == h for p,h in guard['inputHashes'].items()),
         'Already native-compiled entire unchanged physical controller, including original AIR branch')
    scope = dict(vars(base.ui), INIT=INIT, __file__=__file__)
    exec(compile(inspect.getsource(base.ui.expectation), __file__+'::whole_current_initializer', 'exec'), scope)
    guest, gfx, build = scope['expectation']()
    native, human_check, check, decode = bindings(guest, build)
    candidate = ROOT / base.audio.NAME
    payload = (candidate / 'roms/mk2ks/mk2ks.mdata').read_bytes()
    pins = dict(previous['inputHashes'])
    need(all(sha(p) == h for p,h in pins.items()), 'Same current executed candidate and physical sources')
    for p in (Path(__file__), previous_path, INIT/'report.json'):
        pins[str(p.resolve())] = sha(p)
    gfx32 = base.reconstruct(native, pins)
    original = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in ((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
        need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8] ==
             original[(lo-0xff800000)//8:(hi-0xff800000)//8], 'Entire original body/shadow kernels unchanged')
    capture_source = replace_once(inspect.getsource(base.capture),
                                  "MK2KS_HUMAN_SPECIAL_AIR='0'", "MK2KS_HUMAN_SPECIAL_AIR='1'")
    scope = dict(vars(base), BASE=BASE, RAM_CASES=RAM_CASES, COMPLETED=[])
    exec(compile(capture_source, __file__+'::whole_original_capture_original_air_option', 'exec'), scope)
    reports, faults = [], []
    for side in (1,2):
        report = scope['capture']('square',side,guest,gfx,gfx32,payload,native,check,decode,pins)
        reports.append(report)
        need(report['passed'], 'Actual full airborne contact gate; never replay after host or native rejection')
        folder,text,images = RAM_CASES[f'square_p{side}']
        rows = base.defaultdict(list)
        for line in text.splitlines():
            if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):
                rows[line.split()[0]].append(dict(base.re.findall(r'(\w+)=([^\s]+)',line)))
        b = dict(move='square', side=side, folder=folder, report_path=folder/'result.json',
                 report=report, rows=rows, streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))
        faults.append(dict(side=side, **fault_checks(b,guest,payload,gfx32,check)))
    need(not base.identity.census() and all(sha(p)==h for p,h in pins.items()), 'Same actual terminals and stable inputs')
    outputs = {str(p.resolve()):sha(p) for p in BASE.rglob('*') if p.is_file()}
    need(all(Path(p).suffix.lower() not in ('.png','.wav','.bin','.exe','.zip') for p in outputs), 'No raw media or duplicate build')
    value = dict(passed=True,candidate=native.NAME,cases=reports,faultChecks=faults,inputHashes=pins,outputHashes=outputs,
                 actualPhysicalCases=2, actualAirborneContactCycles=4, actualSquareContactVerified=True,
                 everyReadyOwnedBodyShadowFieldSourceBound=True, fullVisualTimelineAccepted=False,
                 allArenasAccepted=False, fullAudioAcceptance=False, fullPortAcceptance=False,
                 publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active',scope=__doc__)
    OUT.mkdir()
    base.save(OUT/'report.json',value)
    print(json.dumps(dict(passed=True,actualAirborneContactCycles=4,fullPortAcceptance=False)),flush=True)


if __name__ == '__main__':
    try:
        run()
    except Exception as error:
        need(not OUT.exists(), 'Preserve immutable failure')
        OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                       fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    server=base.preview.serve(RAM_CASES)
    code.interact(banner='Same actual airborne contact trials retained in RAM, no replay.',
                  local=dict(cases=RAM_CASES,server=server,module=__import__(__name__)))
