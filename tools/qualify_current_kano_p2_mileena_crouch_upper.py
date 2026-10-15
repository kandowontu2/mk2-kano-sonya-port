"""Reuse actual native chronology gate; measure owned uppercut263 contacts."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_standing.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_standing','audit_current_kano_p2_mileena_crouch_upper')
source=source.replace("=='259'", "=='263'")
source=source.replace('mileenaOwnedHK','mileenaOwnedUpper')
exec(compile(source,__file__+'::native_upper_gate','exec'))
import json
import check_campaign_stage_chronology as chronology
root=Path(__file__).resolve().parents[1]
rows=chronology.load(root/'audit_current_kano_p2_mileena_crouch_upper_runtime/run.log')
throws=rows.get('MILEENA_THROW_START',[])
for r in throws:
    assert r['a8']==r['cpu_actor'] and r['a13']==r['cpu_main']
    assert int(r['at'],16)==int(r['cpu_main'],16)+0x1f0
    assert r['pc']=='FF8B6FA0'
    assert r['cpu_actor']!=r['human_actor'] and r['cpu_main']!=r['human_main']
summary=dict(actualOwnedThrowStarts=len(throws),gaps=[int(r['gap']) for r in throws],
             upperInputFields=len(rows.get('MILEENA_UPPER_INPUT',[])),
             fullCampaignAccepted=False,fullPortAccepted=False)
(root/'audit_current_kano_p2_mileena_crouch_upper_checked/throw-spacing.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
