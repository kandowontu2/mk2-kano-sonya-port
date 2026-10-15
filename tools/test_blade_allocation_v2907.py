"""Reject actual blade pool/attachment/retirement/reuse corruptions.

Both original and candidate raw captures remain unchanged. Every mutation
changes a real record and is checked with the independently assembled guest.
No broad visual, audio, CPU, RNG or full-port acceptance is implied.
"""
import json
import sys
import traceback
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import verify_blade_allocation_v2905 as model
from test_current_cpu_overlap_v1912 import mutate

ROOT = model.ROOT
OUT = ROOT / 'audit_v2908_blade_allocation_units'


def verify():
    path = model.OUT/'report.json'
    proof = json.loads(path.read_text())
    model.need(proof['passed'] and proof['actualFixtures'] == 14 and proof['allSevenChangedBladeAddressesSourceBound'] and
               proof['noAddressNormalization'] and proof['originalNativeChronologyExactForEveryFixture'], 'Actual full original allocation proofs')
    pins = dict(proof['inputHashes'])
    pins[str(path)] = model.assembly.sha(path)
    new, old, _, _, _ = model.assembly.expected()
    logs = {(ROOT/r[b]['case']/'run.log').read_text(encoding='utf-8-sig') for r in proof['cases'].values() for b in ('new', 'old')}
    rejected = []
    for key, pair in proof['cases'].items():
        kind = key.split('_')[0]
        context = pair['actualAddressDifferences'][0]['context']
        for build in ('new', 'old'):
            case = pair[build]
            folder = ROOT/case['case']
            meta = json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            log = (folder/'run.log').read_text(encoding='utf-8-sig')
            guest = new if build == 'new' else old
            positive = model.verify_log(log, guest, kind, meta['side'], meta['victim'])
            ctx = next(r for r in positive['contexts'] if r['context'] == context)
            n, start, end, obj, main = (ctx[k] for k in ('context', 'start', 'detached', 'object', 'main'))
            other = f'{obj + 0x210:08X}'
            P = 'MK2_BLADE_ALLOC_'
            tests = [
                ('missing actual sprite pop', 'HEAD_STORE', {'sequence': str(ctx['nativePopSequence'])}, None, None),
                ('wrong native next link', 'HEAD_STORE', {'sequence': str(ctx['nativePopSequence'])}, 'targetNext', 'FFFFFFFF'),
                ('wrong original pop target register', 'HEAD_STORE', {'sequence': str(ctx['nativePopSequence'])}, 'a0', other),
                ('forged original pop opcode', 'HEAD_STORE', {'sequence': str(ctx['nativePopSequence'])}, 'op0', '0000'),
                ('missing high-word allocation transaction', 'HEAD_STORE', {'sequence': str(ctx['nativePopFinalSequence'])}, None, None),
                ('wrong allocation upper word', 'HEAD_STORE', {'sequence': str(ctx['nativePopFinalSequence'])}, 'data', '0000'),
                ('constructor steals a different sprite', 'CREATE', {'context': str(n)}, 'freeHead', other),
                ('attachment uses wrong Main', 'TRAIL_STORE', {'context': str(n), 'frame': str(start), 'at': f'{main+0x190:08X}'}, 'a13', '0106FFFF'),
                ('forged attachment instruction', 'TRAIL_STORE', {'context': str(n), 'frame': str(start), 'at': f'{main+0x190:08X}'}, 'op0', '0000'),
                ('wrong actual attached object register', 'TRAIL_STORE', {'context': str(n), 'frame': str(start), 'at': f'{main+0x1a0:08X}'}, 'a10', other),
                ('substituted child address', 'FIELD', {'context': str(n), 'frame': str(start+1)}, 'object', other),
                ('stale parent attachment after cleanup', 'FIELD', {'context': str(n), 'frame': str(end+1)}, 'trail', f'{obj:08X}'),
                ('wrong source blade descriptor', 'FIELD', {'context': str(n), 'frame': str(start+1)}, 'descriptor', 'FE82AAA0'),
                ('missing active phase callback', 'FIELD', {'context': str(n), 'frame': str(start+10)}, None, None),
                ('simultaneously free and rendered sprite', 'FIELD', {'context': str(n), 'frame': str(start+1)}, 'free', '1'),
                ('forged previous free head at retirement', 'HEAD_STORE', {'sequence': str(ctx['nativePushSequence'])}, 'before', '0105B950'),
                ('retirement targets a different object', 'RETIRE', {'context': str(n)}, 'a0', other),
                ('missing actual original retirement', 'RETIRE', {'context': str(n)}, None, None),
                ('cleanup executes under wrong Main', 'CLEANUP', {'context': str(n)}, 'a13', '0106FFFF'),
                ('false final zero detach', 'TRAIL_STORE', {'context': str(n), 'frame': str(end), 'at': f'{main+0x1a0:08X}'}, 'merged', f'{obj:08X}'),
                ('missing detached continuation callback', 'FIELD', {'context': str(n), 'frame': str(end+2)}, None, None),
                ('false actual detach time', 'CONTEXT_RESULT', {'context': str(n)}, 'detached', str(end+1)),
            ]
            for reuse_ctx in positive['contexts']:
                reuse = reuse_ctx['postRetirementNativeReuse']
                if not reuse:
                    continue
                sequence = str(reuse[0]['nativeReuseSequence'])
                tests += [('reoccupied address without a new actual allocation', 'HEAD_STORE', {'sequence': sequence}, None, None),
                          ('new allocation still under old blade Main', 'HEAD_STORE', {'sequence': sequence}, 'a13', f"{reuse_ctx['main']:08X}")]
                break
            for label, tag, criteria, field, value in tests:
                damaged = mutate(log, P+tag, criteria, field, value)
                model.need(damaged not in logs, 'Actual corruption must differ from every genuine fixture')
                try:
                    model.verify_log(damaged, guest, kind, meta['side'], meta['victim'])
                except (AssertionError, ValueError, KeyError, IndexError) as error:
                    rejected.append(dict(case=case['case'], name=label, error=repr(error)))
                else:
                    raise AssertionError('Accepted actual allocation corruption: '+case['case']+' '+label)
            print(case['case']+': rejected '+str(len(tests))+' actual lifetime corruptions', flush=True)
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file:
            file = Path(file).absolute()
            if file.is_relative_to(ROOT/'tools') and file.suffix == '.py':
                pins[str(file)] = model.assembly.sha(file)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for (file, wanted), actual in zip(pins.items(), pool.map(model.assembly.sha, pins)):
            model.need(actual == wanted, 'Actual source and capture unchanged '+file)
    return dict(passed=True, actualFixturesTested=14, candidate=model.assembly.NAME, control=model.assembly.prior.NAME,
                actualCounterexamplesRejected=len(rejected), counterexamples=rejected, mutationNonVacuityRequired=True,
                actualCapturesUnmodified=True, originalCombatContractsUnchanged=True, gameBytesChanged=False,
                fullPortAcceptance=False, inputHashes=pins, scope=__doc__)


if __name__ == '__main__':
    model.need(not OUT.exists(), 'Immutable actual allocation rejection proof')
    try:
        report = verify()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), fullPortAcceptance=False)
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','counterexamples')}, indent=2), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
