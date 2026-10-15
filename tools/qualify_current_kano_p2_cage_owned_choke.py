"""Unchanged prefix before Cage; later stages only actual records, not fixed timing."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_campaign_frontier_observer.py').read_text().replace('audit_current_kano_p2_campaign_frontier_observer','audit_current_kano_p2_cage_owned_choke').replace('65763','8509')
exec(compile(source,__file__+'::earlier_route_change','exec'))
chokes=[r for r in rows.get('SPECIAL',[]) if r['move']=='choke' and r['stage']=='2']
assert all(r['id']==r['roster']=='17' and r['actor']==r['a8'] and r['main']==r['a13'] for r in chokes)
detail=dict(actualOwnedCageChokeEntries=chokes,ownCageRounds=[r for r in rows['WIN'] if r['stage']=='2' and r['slot']=='2'],laterFightStages=[r for r in rows['FIGHT'] if int(r['stage'])>2],fullPortAccepted=False)
(out/'cage-context.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
