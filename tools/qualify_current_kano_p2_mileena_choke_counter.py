"""True IDs/native chronology and actual choke dispatch, not planned intent."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_ready_escape.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_ready_escape','audit_current_kano_p2_mileena_choke_counter')
exec(compile(source,__file__+'::native_choke_counter_gate','exec'))
chokes=[r for r in rows.get('SPECIAL',[]) if r['stage']=='10' and r['move']=='choke']
for r in chokes:
    assert r['id']==r['roster']=='17' and r['actor']==r['a8'] and r['main']==r['a13']
summary=dict(actualOwnedNativeChokeEntries=len(chokes),
             actualLPInputFields=len(rows.get('MILEENA_CHOKE_LP_INPUT',[])),
             fullCampaignAccepted=False,fullPortAccepted=False)
(root/'audit_current_kano_p2_mileena_choke_counter_checked/native-choke.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
