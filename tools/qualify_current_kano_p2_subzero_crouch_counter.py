"""Qualify bounded physical counter evidence without assuming a campaign clear."""
import copy
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

sync.verify()
folder = sync.ROOT / 'audit_current_kano_p2_subzero_crouch_counter_runtime'
out = sync.ROOT / 'audit_current_kano_p2_subzero_crouch_counter_checked'
assert not out.exists()
terminal = json.loads((folder / 'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode'] == 0 and terminal['limitReason'] is None
assert terminal['peakWorkingSetBytes'] <= 320 * 1024 * 1024
assert terminal['logBytes'] <= 10 * 1024 * 1024
assert not (folder / 'stderr.log').read_text().strip()
rows = chronology.load(folder / 'run.log')
old = chronology.load(sync.ROOT / 'audit_current_kano_p2_sonya_standing_counter_runtime/run.log')
for tag in set(rows) | set(old):
    if tag not in ('KANO_P2_SUBZERO_DAMAGE', 'KANO_P2_SUBZERO_COUNTER'):
        assert [r for r in rows.get(tag, []) if int(r['frame']) < 4681] == [
            r for r in old.get(tag, []) if int(r['frame']) < 4681], tag

def gate(records):
    assert records['RESULT'][0]['frame'] == '20000'
    assert all(r['writes'] == '0' and r['assistance'] == 'none'
               for group in records.values() for r in group)
    assert all(r['human'] == '17:17' for r in records['LIVE'] + records['FIGHT'])
    assert all(r['roster'] == '17' for r in records['SELECT_ID'])
    stages = chronology.check(records, 2, 17, list(range(13)) + [14, 15, 16])
    arrival = next(r for r in records['FIGHT'] if r['stage'] == '1')
    wins = [r for r in records['WIN'] if r['slot'] == '2' and r['stage'] == '0']
    assert [r['frame'] for r in wins] == ['2733', '4168']
    assert all(r['id'] == '17' and r['entry'] == 'FFFEFA20' for r in wins)
    assert arrival['frame'] == '4681' and arrival['cpu'] == '8:8'
    assert not any(int(r['frame']) <= 4681 for r in records.get('LOSS', []))
    damage = records.get('KANO_P2_SUBZERO_DAMAGE', [])
    assert all(r['ids'] == '8,17' and r['p1_actor'] != r['p2_actor']
               and r['p1_main'] != r['p2_main'] for r in damage)
    contacts = [r for r in damage if r['victim_slot'] == '1'
                and r['actions'].split(',')[1] == '263'
                and r['a8'] == r['p2_actor'] and r['a13'] == r['p2_main']]
    return dict(earnedStages=stages, openingMatchRetained=True,
                ownUppercutContacts=len(contacts),
                outgoing=sum(int(r['before']) - int(r['after']) for r in damage if r['victim_slot'] == '1'),
                incoming=sum(int(r['before']) - int(r['after']) for r in damage if r['victim_slot'] == '2'),
                subZeroOwnRoundWins=[r for r in records['WIN'] if r['stage'] == '1' and r['slot'] == '2'],
                paidLosses=len(records.get('LOSS', [])), subZeroMatchCleared=2 in stages)

proof = gate(rows)
bad = copy.deepcopy(rows)
bad['LIVE'][0]['human'] = '17:1'
try:
    gate(bad)
except AssertionError:
    pass
else:
    raise AssertionError('Proxy accepted')
out.mkdir()
report = dict(finiteObservationPassed=True, priorEarnedPrefixUnchangedThrough=4680,
              proof=proof, proxyFaultRejected=True, terminal=terminal,
              logSHA256=sync.sha(folder / 'run.log'),
              fullCampaignAccepted=False, fullPortAccepted=False)
(out / 'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(proof))
