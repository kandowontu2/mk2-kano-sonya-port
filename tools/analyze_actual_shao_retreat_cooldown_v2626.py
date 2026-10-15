"""Read-only actual damage and grounded eligibility during retreat cooldown.
This identifies physical test-policy opportunities, not a game defect or proof
that a changed policy will win. Native state and captured bytes stay unchanged.
"""
import argparse, json
from collections import defaultdict
from pathlib import Path
import verify_current_shao_walking_retreat_boss_ledger_v2614 as ledger
from analyze_current_shao_opening_damage_states_v2408 import own_damage
ROOT = ledger.ROOT
launch = ledger.launch

def need(ok, label):
    if not ok:
        raise ValueError(label)

def verify():
    pins = {}
    cases = {}
    for fighter in ('kano', 'sonya'):
        def accept(path):
            report = json.loads(path.read_text())
            need(report['passed'] and not report['fullPortAcceptance'], 'Accepted bounded actual evidence')
            for file, wanted in report['inputHashes'].items():
                if file in pins:
                    need(pins[file] == wanted, 'Consistent actual dependency ' + file)
                else:
                    need(launch.sha(file) == wanted, 'Unchanged actual dependency ' + file)
                    pins[file] = wanted
            pins[str(path)] = launch.sha(path)
            return report
        proof = accept(ROOT / f'audit_v2612_current_{fighter}_p1_shao_walking_retreat_checked/report.json')
        book = accept(ROOT / f'audit_v2616_current_{fighter}_shao_walking_retreat_boss_ledger_checked/report.json')
        jump = accept(ROOT / f'audit_v2625_current_{fighter}_walking_retreat_jump_correspondence_checked/report.json')
        rows = ledger.native.parse((ROOT / f'audit_v2611_current_{fighter}_p1_shao_walking_retreat_campaign/run.log').read_text(encoding='utf-8-sig'), 1, fighter)
        ledger.check(rows, 17 if fighter == 'kano' else 18, 1)
        fields = {r['frame']: r for r in rows if r['tag'] == 'BOSS_FIELD' and r['stage'] == 16}
        plans = {r['frame']: r for r in rows if r['tag'] == 'BOSS_PLAN' and r['stage'] == 16}
        last = -1000
        ages = {}
        opportunities = []
        for frame, f in sorted(fields.items()):
            if frame - 1 not in fields:
                last = -1000
            if frame in plans:
                last = frame
            ages[frame] = frame - last
            if (48 <= frame - last < 60 and f['height'] == 0 and
                not f['flags'] & 0x1c and not f['body'] & 0x0c and
                f['human_action'] in (0, 0x303, 0x304) and f['gap'] < 220 and f['cpu_height'] < 20):
                opportunities.append(frame)
        opportunity_set = set(opportunities)
        groups = defaultdict(lambda: dict(stores=0, damage=0))
        incoming = own_damage(rows, 1)
        for hit in incoming:
            if hit['actionAtOwnDamage'] != 0:
                continue
            frame = hit['frame']
            f = fields[frame]
            age = ages[frame]
            group = ('cooldown48to59' if 48 <= age < 60 else
                     'before48' if 0 <= age < 48 else 'ready60plus')
            group += '_gap' + ('under220' if f['gap'] < 220 else 'over220')
            g = groups[group]
            g['stores'] += 1
            g['damage'] += hit['damage']
        cases[fighter] = dict(actualShaoRoundWins=sum(r['tag'] == 'WIN' and r['slot'] == 1 and r['stage'] == 16 for r in rows),
                              actualIncomingDamage=sum(r['damage'] for r in incoming),
                              actualWalk0DamageGroups=dict(groups),
                              measuredGrounded48to59OpportunityFields=len(opportunities),
                              actualDamageDuringThoseOpportunityFields=sum(r['damage'] for r in incoming if r['frame'] in opportunity_set),
                              actualDamageStoresDuringThoseOpportunityFields=sum(r['frame'] in opportunity_set for r in incoming),
                              actualNativeJumpAssignments=jump['actualOriginal308Assignments'],
                              firstMeasuredOpportunityFrames=opportunities[:12],
                              completeCurrentInputReplayPassed=proof['bounded_campaign_evidence_proven'],
                              orderedNativeAdjacentPairs=book['positiveHealthAdjacentBossFieldPairs'],
                              improvementNotAssumed=True)
    pins[str(Path(__file__).resolve())] = launch.sha(__file__)
    launch.module_pins(pins)
    return dict(passed=True, cases=cases, inputHashes=pins, gameChanged=False,
                fullPortAcceptance=False, scope=__doc__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    need(not args.output.exists(), 'Immutable actual damage diagnostic')
    report = verify()
    args.output.mkdir()
    (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'inputHashes'}, indent=2), flush=True)
