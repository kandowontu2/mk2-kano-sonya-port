"""Compare existing current Sub-Zero campaign failures without replaying them."""
import collections
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync

sync.verify()
out=sync.ROOT/'audit_current_subzero_campaign_controllers'
assert not out.exists()
cases={}
for name in ('mirror_guard','mirror_subzero_ring'):
 folder=sync.ROOT/f'audit_current_sonya_p2_{name}_runtime'
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None
 rows=chronology.load(folder/'run.log')
 live=[r for r in rows['LIVE'] if r['stage']=='1']
 assert live and all(r['human']=='18:18' and r['cpu']=='8:8' for r in live)
 start=int(rows['STAGE'][1]['frame'])
 health=[r for r in rows['HEALTH'] if int(r['frame'])>=start and r['pc']=='FF836700' and 0<=int(r['after'])<int(r['before'])<=161]
 wins=[r for r in rows['WIN'] if r['stage']=='1']
 actions=[collections.Counter(r['actions'].split(',')[i] for r in live) for i in (0,1)]
 cases[name]={'logSHA256':sync.sha(folder/'run.log'),
  'specials':dict(collections.Counter(r['move'] for r in rows['SPECIAL'] if r['stage']=='1')),
  'nativeDamageToSubZero':sum(int(r['before'])-int(r['after']) for r in health if r['slot']=='1'),
  'nativeDamageToSonya':sum(int(r['before'])-int(r['after']) for r in health if r['slot']=='2'),
  'ownRoundWins':sum(r['slot']=='2' for r in wins),'cpuRoundWins':sum(r['slot']=='1' for r in wins),
  'sparseHumanActions':dict(actions[0]),'sparseCPUActions':dict(actions[1]),
  'sampledCpuThrows':actions[1]['1287']}
out.mkdir()
(out/'report.json').write_text(json.dumps({'cases':cases,'noNewGames':True,
 'exactCollisionAttribution':False,'fullCampaignAccepted':False},indent=2))
print(json.dumps(cases))
