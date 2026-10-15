"""Same original native campaign gate, exact handler entries and damage."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_scorpion_upper.py').read_text()
source=source.replace('audit_current_kano_p2_scorpion_upper','audit_current_kano_p2_scorpion_close_upper')
source=source.replace("'SCORPION_AIR_WRITE')","'SCORPION_AIR_WRITE','SCORPION_READY','SCORPION_UPPER_ENTRY')")
exec(compile(source,__file__+'::native_upper_gate','exec'))
entries=rows.get('SCORPION_UPPER_ENTRY',[])
for r in entries:
    assert r['actor']==r['owner']==r['a8'] and r['main']==r['a13']
    assert int(r['height'])==0
(out/'native-upper-entry.json').write_text(json.dumps(dict(nativeOwnedEntries=len(entries),entries=entries,fullCampaignAccepted=False),indent=2))
print('Actual native owned upper handler entries:',len(entries))
