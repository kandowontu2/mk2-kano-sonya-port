"""Same earned true-ID campaign/ball gate plus actual low-health knife entries."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_scorpion_guarded_ball.py').read_text()
source=source.replace('audit_current_kano_p2_scorpion_guarded_ball','audit_current_kano_p2_scorpion_ball_knife')
exec(compile(source,__file__+'::same_native_ball_gate','exec'))
entries=[r for r in rows.get('SPECIAL',[]) if r['move']=='knife' and r['stage']=='6']
for r in entries:
    assert r['id']==r['roster']=='17' and r['actor']==r['a8'] and r['main']==r['a13'] and r['entry']=='FFFFB000'
(out/'native-knife-entry.json').write_text(json.dumps(dict(nativeOwnedEntries=len(entries),entries=entries,fullCampaignAccepted=False),indent=2))
print('Native owned low-health Scorpion knife entries:',len(entries))
