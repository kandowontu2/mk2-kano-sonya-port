"""Earlier-route equality, actual Shao jump entries, no intended-input success."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_campaign_frontier_observer.py').read_text()
source=source.replace('audit_current_kano_p2_campaign_frontier_observer','audit_current_kano_p2_shao_held_escape')
source=source.replace("prior=root/'audit_current_kano_p2_changed_health_only_runtime'","prior=root/'audit_current_kano_p2_approved_180s_runtime'")
source=source.replace('65763','69698')
exec(compile(source,__file__+'::scoped_controller_trial','exec'))
entries=[r for r in rows.get('BOSS_ACTION',[]) if r['stage']=='16' and r['after'] in ('776','779')]
assert all(r['id']==r['roster']=='17' and r['actor']==r['owner']==r['a8'] and r['main']==r['a13'] for r in entries)
detail=dict(actualOwnedShaoJumpEntries=entries,shaoObserved=any(r['stage']=='16' for r in rows['STAGE']),fullPortAccepted=False)
(out/'jump-entries.json').write_text(json.dumps(detail,indent=2)+'\n');print(json.dumps(detail))
