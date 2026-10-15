"""Retain original full native campaign gate and qualify actual choke entries."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_scorpion_close_air_scoped.py').read_text()
source=source.replace('audit_current_kano_p2_scorpion_close_air','audit_current_kano_p2_scorpion_choke')
source=source.replace("'SCORPION_AIR_WRITE')","'SCORPION_AIR_WRITE','SCORPION_UPPER_ENTRY')")
exec(compile(source,__file__+'::same_earned_campaign_gate','exec'))
entries=[r for r in rows.get('SPECIAL',[]) if r['move']=='choke' and r['stage']=='6']
for r in entries:
    assert r['id']==r['roster']=='17' and r['actor']==r['a8'] and r['main']==r['a13'] and r['entry']=='FFF91400'
(out/'native-choke-entry.json').write_text(json.dumps(dict(nativeOwnedEntries=len(entries),entries=entries,fullCampaignAccepted=False),indent=2))
print('Native owned Scorpion choke entries:',len(entries))
