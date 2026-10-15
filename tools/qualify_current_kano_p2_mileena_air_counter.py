"""Native chronology and actual owned airborne state stores, not input intent."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_crouch_upper.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_crouch_upper','audit_current_kano_p2_mileena_air_counter')
source=source.replace("=='263'", "=='512'").replace('mileenaOwnedUpper','mileenaOwnedAirKick')
exec(compile(source,__file__+'::native_air_gate','exec'))
air=rows.get('MILEENA_AIR_WRITE',[])
for r in air:
    assert r['actor']==r['owner']==r['a8'] and r['main']==r['a13']
    assert int(r['at'],16)==int(r['main'],16)+0x1f0
    assert (r['pc'],r['after']) in [('FF831360','776'),('FF871F50','512')]
summary=dict(actualOwnedNativeAirWrites=air,fullCampaignAccepted=False,fullPortAccepted=False)
(root/'audit_current_kano_p2_mileena_air_counter_checked/native-air.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(dict(nativeJumps=sum(r['after']=='776' for r in air),nativeAirKicks=sum(r['after']=='512' for r in air))))
