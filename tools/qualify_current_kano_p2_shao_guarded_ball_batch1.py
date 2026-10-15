"""Prefix evidence and actual owned ball entries; no planned-input acceptance."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_shao_held_escape.py').read_text()
source=source.replace('audit_current_kano_p2_shao_held_escape','audit_current_kano_p2_shao_guarded_ball_batch1')
exec(compile(source,__file__+'::batch1','exec'))
balls=[r for r in rows.get('SPECIAL',[]) if r['stage']=='16' and r['move']=='ball']
assert all(r['id']==r['roster']=='17' and r['actor']==r['a8'] and r['main']==r['a13'] for r in balls)
detail=dict(actualOwnedBallEntries=balls,ownedShaoRounds=[r for r in rows['WIN'] if r['stage']=='16' and r['slot']=='2'],fullPortAccepted=False)
(out/'ball-entries.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
