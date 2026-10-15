"""Native jump/kick writers, ownership and exact replay observer neutrality."""
import json
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_p2_scorpion_air_writers_runtime'
out=sync.ROOT/'audit_current_kano_p2_scorpion_air_writers_checked'
assert not out.exists()
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_kano_p2_scorpion_air_writers_preparation/campaign.lua')
assert not (case/'stderr.log').read_text().strip()
rows=chronology.load(case/'run.log');old=chronology.load(sync.ROOT/'audit_current_kano_p2_scorpion_event_jump_runtime/run.log')
for tag in set(rows)|set(old):
    if tag!='SCORPION_AIR_WRITE':assert rows.get(tag,[])==old.get(tag,[]),tag
events=rows['SCORPION_AIR_WRITE'];assert events
for r in events:
    assert r['actor']==r['owner']==r['a8'] and r['main']==r['a13']
    assert int(r['at'],16)==int(r['main'],16)+0x1f0
    assert (r['after'],r['pc']) in [('776','FF831360'),('512','FF871F50')]
kicks=[r for r in events if r['after']=='512'];jumps=[r for r in events if r['after']=='776']
assert kicks and jumps
out.mkdir()
report=dict(passiveObserverNeutral=True,nativeJumpWriters=len(jumps),nativeAirKickWriters=len(kicks),
    kickGeometry=[dict(frame=int(r['frame']),gap=int(r['gap']),height=int(r['height'])) for r in kicks],
    correction='Action512 is native air kick, not merely forward jump; 270 is a separate native air attack. Prior absence-of-kicks inference is superseded.',
    terminal=terminal,fullCampaignAccepted=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
