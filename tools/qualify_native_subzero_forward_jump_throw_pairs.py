"""Source-bound diagnosis of every actually observed native SubZero throw.

Reconstruct the complete current guest in RAM through the original compiled
initializer and entire79-byte model, then bind actual native stores/pairs.
No new game boot, no guest writes, no image/audio/campaign acceptance.
"""
import collections
import gzip
import hashlib
import inspect
import json
import re
import struct
from pathlib import Path
from types import SimpleNamespace
import capture_native_kano_laser_audio as audio
import capture_native_paired_stumble_campaign as model
import run_native_sonya_subzero_forward_jump_bound_campaign as capture
import diagnose_native_subzero_forward_jump_loss as diagnosis

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT / 'audit_native_subzero_forward_jump_native_throws_checked'
BASE = ROOT / 'audit_native_subzero_forward_jump_throw_initializer_probe'
INIT = ROOT / 'audit_native_subzero_forward_jump_throw_source_initializer'
OLD_INIT = ROOT / 'audit_native_subzero_forward_jump_throw_unused_initializer_leaf'


def expectation():
    return baseline_guest, None, baseline_build, None


def kernels(guest, native):
    off = lambda address: (address - 0xff800000) // 8
    for begin, end in ((0xff842710, 0xff8429f0), (0xff8b6e80, 0xff8b6ff0),
                       (0xff831300, 0xff8313e0), (0xff871ed0, 0xff871f50)):
        need(guest[off(begin):off(end)] == native[off(begin):off(end)],
             'Whole native victim capture/throw/jump/airkick kernels unchanged')
    for begin, end, words in ((0xff842870, 0xff8428a0, (0x5600,0xb00d,0x01f0)),
                              (0xff8b6f60, 0xff8b6fa0, (0x09c0,0x0507,0xb00d,0x01f0)),
                              (0xff831320, 0xff831360, (0x09c0,0x0308,0xb00d,0x01f0)),
                              (0xff871f10, 0xff871f50, (0x09c0,0x0200,0xb00d,0x01f0))):
        need(guest[off(begin):off(end)] == struct.pack('<' + 'H'*len(words), *words),
             'Exact native post-fetch clear/throw/jump/airkick instruction signature')
    return True


def pairs(fields, actions, throws):
    need(len(throws) == 344, 'Every actually inventoried native CPU507 store retained')
    owned = []
    for throw in throws:
        field = fields[int(throw['frame'])]
        need(throw['after'] == '1287' and throw['pc'] == 'FF8B6FA0' and
             int(throw['a0'],16)&0xffff == 0x507 and throw['mask'] == 'FFFF' and
             throw['id'] == throw['roster'] == field['cpu_id'] == field['cpu_roster'] == '8' and
             throw['actor'] == throw['owner'] == throw['a8'] == field['cpu_actor'] == field['cpu_owner'] and
             throw['main'] == throw['a13'] == field['cpu_main'] and
             int(throw['at'],16) == int(throw['main'],16)+0x1f0 and
             throw['health'] == field['health'] and all(0<int(h)<=161 for h in throw['health'].split(',')),
             'Actual original throw setter, registers, native stock8 owner and positive-health same-field pair')
        clears = [q for q in actions[int(throw['frame'])] if q['pc'] == 'FF8428A0' and
                  q['actor'] == field['human_actor'] and q['main'] == field['human_main']]
        need(len(clears) == 1, 'Each observed native throw has exactly one actual victim Main clear')
        clear = clears[0]
        need(clear['after'] == '0' and clear['mask'] == 'FFFF' and clear['id'] == clear['roster'] ==
             field['human_id'] == field['human_roster'] == '18' and
             clear['actor'] == clear['owner'] == clear['a8'] == field['human_actor'] == field['human_owner'] and
             clear['main'] == clear['a13'] == field['human_main'] and
             int(clear['at'],16) == int(clear['main'],16)+0x1f0 and clear['health'] == field['health'],
             'Native opponent victim capture is true owned Sonya18, not a name-only actor or port cleanup')
        following = fields.get(int(throw['frame'])+1)
        need(following is not None and following['human_actor'] == field['human_actor'] and
             following['human_main'] == field['human_main'] and following['human_action'] == '0' and
             following['cpu_action'] == '1287' and int(following['flags'],16)&4,
             'Actual next native field retains captured owned Sonya and executing stock throw')
        owned.append(dict(throw=throw, victimClear=clear, sameNativeField=field, followingNativeField=following))
    return owned


def run():
    need(not OUT.exists() and not BASE.exists() and not capture.original.core.base.census.census(),
         'Fresh source/terminal analysis only after actual original native retirement')
    diagnosed_path = diagnosis.OUT / 'report.json'
    diagnosed = json.loads(diagnosed_path.read_text())
    need(diagnosed['diagnosisCompleted'] and not diagnosed['gameplayAccepted'] and
         diagnosed['nativeCPUActionStores']['1287'] == 344 and
         all(sha(p) == h for p,h in diagnosed['inputHashes'].items()), 'Whole original failed trial frozen')
    BASE.mkdir()
    factory = capture.original.previous.once(inspect.getsource(audio.functions),
                                             "return scope['run']", 'return scope')
    scope = dict(vars(audio), __file__=__file__)
    exec(compile(factory, __file__ + '::entire_original_source_initializer_factory', 'exec'), scope)
    baseline_guest, baseline_build = scope['functions']()['expected'](BASE)
    need(not (BASE/'guest_expectation_probe.exe').exists(), 'Tiny initializer probe already removed by original helper')
    carrier = SimpleNamespace(expectation=expectation, baseline_guest=baseline_guest, baseline_build=baseline_build)
    scope = dict(vars(model), __file__=__file__, base=carrier, INIT=INIT, OLD_INIT=OLD_INIT)
    exec(compile(inspect.getsource(model.expectation), __file__ + '::entire_original79_byte_guest_model', 'exec'), scope)
    guest, _, _, _ = scope['expectation']()
    proof = json.loads((capture.OUT/'guest_memory_proof.json').read_text())
    need(proof['everyActualByteComparedInRAM'] and proof['bytes'] == len(guest) == 1048576 and
         proof['sha256'] == hashlib.sha256(guest).hexdigest().upper(), 'Every actual current guest byte bound to full reconstruction')
    native = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(kernels(guest,native), 'Whole original native kernels')
    fields, actions, throws = {}, collections.defaultdict(list), []
    with gzip.open(capture.OUT/'run.log.gz','rt',encoding='utf-8') as stream:
        for line in stream:
            if not line.startswith(('MK2_NAT_CAMPAIGN_RANGE_FIELD ', 'MK2_NAT_CAMPAIGN_RANGE_ACTION ',
                                    'MK2_NAT_CAMPAIGN_RANGE_CPU_ACTION ')): continue
            row = dict(re.findall(r'(\w+)=([^\s]+)',line))
            need(row['stage'] == '11' and row['human_slot'] == '1' and row['fighter'] == 'sonya' and
                 row['writes'] == '0' and row['assistance'] == 'none', 'Every actual observer row remains unassisted target context')
            if line.startswith('MK2_NAT_CAMPAIGN_RANGE_FIELD '): fields[int(row['frame'])] = row
            elif line.startswith('MK2_NAT_CAMPAIGN_RANGE_ACTION '): actions[int(row['frame'])].append(row)
            elif row['after'] == '1287': throws.append(row)
    positive = pairs(fields,actions,throws)
    faults = []
    for key,value in (('pc','FFF00000'),('a0','00000303'),('mask','00FF'),('id','18'),('owner','01000000'),
                      ('main','01000000'),('at','01000000'),('a8','01000000'),('a13','01000000'),('health','0,161')):
        bad = list(throws); bad[0] = dict(bad[0],**{key:value})
        try: pairs(fields,actions,bad)
        except (ValueError,KeyError) as error: faults.append(dict(fault='actualCpuThrow_'+key,rejectedBy=str(error)))
        else: raise ValueError('False native CPU throw admitted')
    clear = positive[0]['victimClear']; frame = int(clear['frame'])
    for key,value in (('after','263'),('mask','00FF'),('id','1'),('owner','01000000'),('a8','01000000'),('a13','01000000')):
        bad = dict(actions); bad[frame] = [dict(q,**{key:value}) if q is clear else q for q in actions[frame]]
        try: pairs(fields,bad,throws)
        except (ValueError,KeyError) as error: faults.append(dict(fault='actualVictimClear_'+key,rejectedBy=str(error)))
        else: raise ValueError('False native victim clear admitted')
    for description,bad in [('missingCpuThrow',throws[1:])]:
        try: pairs(fields,actions,bad)
        except ValueError as error: faults.append(dict(fault=description,rejectedBy=str(error)))
        else: raise ValueError('Missing native throw accepted')
    for address in (0xff842870,0xff8b6f60,0xff831320,0xff871f10):
        bad = bytearray(guest); bad[(address-0xff800000)//8] ^= 1
        try: kernels(bad,native)
        except ValueError as error: faults.append(dict(fault='actualNativeKernel_'+hex(address),rejectedBy=str(error)))
        else: raise ValueError('Changed native kernel admitted')
    need(pairs(fields,actions,throws) == positive and kernels(guest,native), 'Whole positive restored after actual faults')
    pins = dict(diagnosed['inputHashes'])
    for path in (diagnosed_path, Path(__file__).resolve(), Path(audio.__file__), Path(model.__file__),
                 ROOT/'mk2/mk2-maincpu.bin', capture.OUT/'guest_memory_proof.json',
                 *BASE.rglob('*'), *INIT.rglob('*')):
        if path.is_file(): pins[str(path.resolve())] = sha(path)
    need(all(sha(p) == h for p,h in pins.items()), 'All actual native evidence and original source inputs unchanged')
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(dict(passed=True, finiteNativeThrowDiagnosisAccepted=True,
        wholeCurrentGuestSHA256=proof['sha256'], wholeOriginalThrowCaptureJumpAirKickKernelsUnchanged=True,
        actualOwnedNativeCpuThrows=344, actualPairedNativeSonyaVictimClears=344, nativePairs=positive,
        semanticAndKernelFaultsRejected=faults, portCleanupNotInferredFromCapturedHeightOrActionZero=True,
        newEmulatorBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        tinySourceInitializerProbeSelfRemoved=True, inputHashes=pins,
        originalNaturalIntegrationRequirements=diagnosed['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=diagnosed['originalRemainingWorkGroups'],
        gameplayFixRequiredByThisEvidence=False, fullTowerAccepted=False, artAccepted=False,audioAccepted=False,
        fullPortAcceptance=False, goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(passed=True, actualNativeCpuThrows=344, actualOwnedVictimClears=344,
                         faultsRejected=len(faults), newNativeBoots=0, fullPortAcceptance=False)),flush=True)


if __name__ == '__main__':
    run()
