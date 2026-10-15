"""Complete frozen retreat stream, compact aggregates rather than RAM media.

Bind every terminal row by category and whole-stream hashes. Count damage
only at the native HP collision kernel with the same actual attacking actor,
not the many native round/setup stores. No test-policy loss proves a bug.
"""
import collections
import gzip
import hashlib
import json
import re
from pathlib import Path
import run_native_sonya_subzero_retreat_retry_bound_campaign as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
OUT = ROOT / 'audit_native_subzero_retreat_retry_loss_diagnosed'


def run():
    need(not OUT.exists(), 'Fresh complete frozen failed-policy diagnosis')
    paths = [ROOT/'audit_native_sonya_subzero_retreat_retry_policy_preserved/report.json',
             ROOT/'audit_native_sonya_subzero_retreat_retry_policy_retirement/report.json',
             ROOT/'audit_native_subzero_retreat_retry_preceding_campaign_checked/report.json']
    saved, retired, preceding = [json.loads(path.read_text()) for path in paths]
    need(saved['preservationPassed'] and not saved['passed'] and retired['passed'] and
         preceding['passed'] and preceding['accepted']['completedOpponents'] == 11,
         'Actual failed transport retired and complete eleven earlier fights retained')
    pins = {}
    for proof in (saved, retired, preceding):
        need(not proof['fullPortAcceptance'], 'Finite proofs never whole-port acceptance')
        for path, digest in proof['inputHashes'].items():
            need(sha(path) == digest and (path not in pins or pins[path] == digest), 'All frozen sources and outcomes unchanged')
            pins[path] = digest
    counts, decisions, actions, cpu_actions, damage = (collections.Counter() for _ in range(5))
    category_hashes = collections.defaultdict(hashlib.sha256)
    whole = hashlib.sha256()
    wins, losses, examples = [], [], []
    field = decision = physical = None
    frozen_fields = flight_fields = total = 0
    first_freeze = None
    log_path = capture.OUT/'run.log.gz'
    with gzip.open(log_path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            need(line.endswith('\n'), 'Complete original terminal records only')
            need(not line.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ', 'MK2_MILEENA_CAMPAIGN_OVERRUN ')), 'No native cache failure in entire log')
            if not line.startswith('MK2_NAT_CAMPAIGN_'):
                continue
            row = dict(re.findall(r'(\w+)=([^\s]+)', line))
            if int(row.get('frame', '0')) < 304271:
                continue
            tag = line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_')
            need(row['writes'] == '0' and row['assistance'] == 'none', 'Every actual target record unassisted')
            counts[tag] += 1; total += 1
            whole.update(line.encode()); category_hashes[tag].update(line.encode())
            if tag == 'RANGE_FIELD':
                need(row['human_id'] == row['human_roster'] == '18' and
                     row['cpu_id'] == row['cpu_roster'] == '8' and
                     row['human_actor'] == row['human_owner'] and row['cpu_actor'] == row['cpu_owner'],
                     'Every observed actual field has true current Sonya/SubZero ownership')
                field = row
                frozen_fields += row['human_action'] == '1025'
                flight_fields += row['human_action'] in ('776', '512')
                if row['human_action'] == '1025' and first_freeze is None:
                    first_freeze = row
            elif tag == 'RANGE_DECISION':
                decisions[row['reason']] += 1; decision = row
            elif tag == 'INPUT':
                physical = row
            elif tag == 'RANGE_ACTION':
                actions[row['after']] += 1
            elif tag == 'RANGE_CPU_ACTION':
                cpu_actions[row['after']] += 1
            elif tag == 'HEALTH' and field is not None:
                before, after = int(row['before']), int(row['after'])
                actor = field['cpu_actor'] if row['slot'] == '1' else field['human_actor']
                main = field['cpu_main'] if row['slot'] == '1' else field['human_main']
                if (row['frame'] == field['frame'] and row['pc'] == 'FF836700' and
                    row['a8'] == actor and row['a13'] == main and 0 <= after < before <= 161):
                    key = (row['slot'], field['human_action'], field['cpu_action'], before-after)
                    damage[key] += 1
                    if len(examples) < 12:
                        examples.append(dict(store=row, sameActualField=field,
                                             previousDecision=decision, previousPhysicalInput=physical))
            elif tag == 'WIN':
                wins.append(row)
            elif tag == 'LOSS':
                losses.append(row)
    need(counts['RANGE_FIELD'] == counts['RANGE_DECISION'] > 0 and counts['SPECIAL'] == 0,
         'Every physical field/decision retained; no claimed custom move activation')
    need(len(losses) == saved['statistics']['lossesByStage']['11'] >= 30 and
         wins and all(row['slot'] == '2' for row in wins) and
         actions['776'] > 0 and actions['512'] > 0 and first_freeze is not None,
         'Complete actual failed matches and native jump/airkick/freeze events, not button counts')
    for path in (*paths, log_path, Path(__file__).resolve(), Path(capture.__file__)):
        pins[str(path.resolve())] = sha(path)
    report = dict(diagnosisCompleted=True, gameplayAccepted=False, fullPortAcceptance=False,
        completeTargetRows=total, completeTargetSHA256=whole.hexdigest().upper(),
        completeCategorySHA256={tag:digest.hexdigest().upper() for tag,digest in category_hashes.items()},
        counts=dict(counts), decisionCounts=dict(decisions), nativeHumanActionStores=dict(actions),
        nativeCPUActionStores=dict(cpu_actions), actualFrozenFields=frozen_fields,
        actualJumpOrAirKickFields=flight_fields, firstActualFreeze=first_freeze,
        completeOwnedCollisionDamageInventory=[dict(slot=k[0],humanAction=k[1],cpuAction=k[2],damage=k[3],count=v)
                                               for k,v in sorted(damage.items())],
        firstOwnedCollisionDamageExamples=examples, allActualWins=wins, allActualLosses=losses,
        fullOriginalLogRemainsRetained=True, engineDefectNotInferredFromControllerLosses=True,
        inputHashes=pins, originalNaturalIntegrationRequirements=saved['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=saved['originalRemainingWorkGroups'],
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    need(all(sha(path)==digest for path,digest in pins.items()), 'No frozen input changed during full diagnosis')
    OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('completeTargetRows','counts','decisionCounts',
         'nativeHumanActionStores','actualFrozenFields','completeOwnedCollisionDamageInventory')},indent=2),flush=True)
    return report


if __name__ == '__main__':
    run()
