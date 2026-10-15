"""Same true native campaign gate; actual owned ball contacts and entries."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_scorpion_close_air_scoped.py').read_text()
source=source.replace('audit_current_kano_p2_scorpion_close_air','audit_current_kano_p2_scorpion_guarded_ball')
source=source.replace("'SCORPION_AIR_WRITE')","'SCORPION_AIR_WRITE','SCORPION_UPPER_ENTRY')")
source=source.replace("proof['ownedAirKickContacts']","proof['ownedBallContacts']").replace("proof['ownedAirKickDamage']","proof['ownedBallDamage']")
source=source.replace("r['actions'].split(',')[1]=='512'","r['actions'].split(',')[1]=='523'")
exec(compile(source,__file__+'::native_ball_gate','exec'))
entries=[r for r in rows.get('SPECIAL',[]) if r['move']=='ball' and r['stage']=='6']
for r in entries:
    assert r['id']==r['roster']=='17' and r['actor']==r['a8'] and r['main']==r['a13'] and r['entry']=='FFFFDE00'
(out/'native-ball-entry.json').write_text(json.dumps(dict(nativeOwnedEntries=len(entries),entries=entries,fullCampaignAccepted=False),indent=2))
print('Native owned Scorpion ball entries:',len(entries))
