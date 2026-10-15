"""Existing native chronology/contact gate, plus actual passive throw ownership."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_retreat_counter.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_retreat_counter','audit_current_kano_p2_mileena_gap90')
exec(compile(source,__file__+'::native_gate','exec'))
import json
root=Path(__file__).resolve().parents[1]
import check_campaign_stage_chronology as chronology
rows=chronology.load(root/'audit_current_kano_p2_mileena_gap90_runtime/run.log')
throws=rows.get('MILEENA_THROW_START',[])
for r in throws:
    assert r['a8']==r['cpu_actor'] and r['a13']==r['cpu_main']
    assert int(r['at'],16)==int(r['cpu_main'],16)+0x1f0
    assert r['pc']=='FF8B6FA0'
    assert r['cpu_actor']!=r['human_actor'] and r['cpu_main']!=r['human_main']
path=root/'audit_current_kano_p2_mileena_gap90_checked/throw-spacing.json'
path.write_text(json.dumps(dict(actualOwnedThrowStarts=len(throws),gaps=[int(r['gap']) for r in throws],
    fullCampaignAccepted=False,fullPortAccepted=False),indent=2)+'\n')
print(path.read_text())
