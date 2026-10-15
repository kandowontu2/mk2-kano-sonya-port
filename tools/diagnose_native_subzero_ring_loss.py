"""Read the complete frozen failed Ring trial; never gameplay acceptance.

Distinguish actual native activation, health stores and physical decisions.
Keep every target event, not merely a favorable or first-round sample.
"""
import collections
import gzip
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'audit_native_sonya_subzero_ring_campaign_ram'
OUT = ROOT / 'audit_native_subzero_ring_loss_diagnosed'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def run():
    assert not OUT.exists(), 'Fresh passive diagnosis, never overwrite a frozen report'
    preserved_path = ROOT / 'audit_native_sonya_subzero_ring_policy_preserved/report.json'
    retired_path = ROOT / 'audit_native_sonya_subzero_ring_policy_retirement/report.json'
    preserved, retired = [json.loads(p.read_text()) for p in (preserved_path, retired_path)]
    assert preserved['preservationPassed'] and not preserved['passed'] and retired['passed']
    pins = dict(preserved['inputHashes'])
    pins.update(retired['inputHashes'])
    assert all(sha(p) == h for p, h in pins.items())
    counts, decisions, actions, cpu_actions = (collections.Counter() for _ in range(4))
    samples = collections.defaultdict(list)
    latest_field = latest_decision = latest_input = latest_live = None
    hits, activations, wins, losses = [], [], [], []
    target_hash = hashlib.sha256()
    total_rows = 0
    with gzip.open(FOLDER / 'run.log.gz', 'rt', encoding='utf-8') as stream:
        for line in stream:
            assert line.endswith('\n'), 'Only a complete terminal stream'
            if not line.startswith('MK2_NAT_CAMPAIGN_'):
                continue
            row = dict(re.findall(r'(\w+)=([^\s]+)', line))
            if int(row.get('frame', '0')) < 304271:
                continue
            tag = line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_')
            total_rows += 1
            target_hash.update(line.encode())
            counts[tag] += 1
            if len(samples[tag]) < (12 if tag in ('HEALTH', 'RANGE_ACTION', 'RANGE_CPU_ACTION') else 4):
                samples[tag].append(row)
            if tag == 'LIVE':
                latest_live = row
            elif tag == 'RANGE_FIELD':
                assert row['human_id'] == row['human_roster'] == '18'
                assert row['cpu_id'] == row['cpu_roster'] == '8'
                assert row['human_actor'] == row['human_owner'] and row['cpu_actor'] == row['cpu_owner']
                latest_field = row
            elif tag == 'RANGE_DECISION':
                decisions[row['reason']] += 1
                latest_decision = row
            elif tag == 'INPUT':
                latest_input = row
            elif tag == 'RANGE_ACTION':
                actions[row['after']] += 1
            elif tag == 'RANGE_CPU_ACTION':
                cpu_actions[row['after']] += 1
            elif tag == 'SPECIAL':
                activations.append(row)
            elif tag == 'HEALTH':
                hits.append(dict(store=row, precedingField=latest_field,
                                 precedingDecision=latest_decision, precedingInput=latest_input,
                                 precedingLive=latest_live))
            elif tag == 'WIN':
                wins.append(row)
            elif tag == 'LOSS':
                losses.append(row)
    assert counts['RANGE_FIELD'] == counts['RANGE_DECISION'] > 0
    assert len(losses) == 37 and wins and all(q['slot'] == '2' for q in wins)
    assert activations and all(q['move'] == 'ring' and q['id'] == q['roster'] == '18' for q in activations)
    for p in (preserved_path, retired_path, Path(__file__).resolve(), FOLDER / 'run.log.gz'):
        pins[str(p)] = sha(p)
    report = dict(diagnosisCompleted=True, gameplayAccepted=False, fullPortAcceptance=False,
                  completeTargetRows=total_rows, completeTargetSHA256=target_hash.hexdigest().upper(),
                  counts=dict(counts), decisionCounts=dict(decisions),
                  nativeHumanActionStores=dict(actions), nativeCPUActionStores=dict(cpu_actions),
                  firstActualEvents=dict(samples), allActualNativeRingActivations=activations,
                  allActualHealthStoresWithPrecedingEvidence=hits, allActualWins=wins,
                  allActualLosses=losses, inputHashes=pins,
                  engineDefectNotInferredFromControllerLosses=True,
                  newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                  originalNaturalIntegrationRequirements=preserved['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=preserved['originalRemainingWorkGroups'], goalStatus='active')
    OUT.mkdir()
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('completeTargetRows', 'counts', 'decisionCounts',
                                           'nativeHumanActionStores', 'nativeCPUActionStores', 'firstActualEvents')}, indent=2))


if __name__ == '__main__':
    run()
