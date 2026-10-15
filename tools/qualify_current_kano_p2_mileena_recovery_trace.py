"""Same passive-prefix gate, then exact native upper and flag-address evidence."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_kano_p2_mileena_throw_trace.py').read_text()
source=source.replace('audit_current_kano_p2_mileena_throw_trace','audit_current_kano_p2_mileena_recovery_trace')
source=source.replace('audit_current_kano_p2_mileena_retreat_counter_runtime','audit_current_kano_p2_mileena_crouch_spacing_runtime')
source=source.replace("last = max(int(fields['frame']) for _, fields, _ in rows)","last = min(max(int(fields['frame']) for _, fields, _ in rows), max(int(fields['frame']) for _, fields, _ in old))")
source=source.replace("'MILEENA_THROW_START', 'HOST_BOUND', 'RESULT'", "'MILEENA_UPPER_ENTRY', 'MILEENA_RECOVERY_ONSET', 'HOST_BOUND', 'RESULT'")
exec(compile(source,__file__+'::passive_prefix_gate','exec'))
upper=[f for tag,f,_ in rows if tag=='MILEENA_UPPER_ENTRY']
onsets=[f for tag,f,_ in rows if tag=='MILEENA_RECOVERY_ONSET']
for f in upper:
    assert f['a8']==f['actor']==f['owner'] and f['a13']==f['main']
    assert f['pc']=='FF870DD0'
for f in onsets:
    assert int(f['at'],16)==int(f['main'],16)+0x210
    assert int(f['before'],16)&4==0 and int(f['after'],16)&4!=0
    assert f['actor']!=f['cpu_actor'] and f['main']!=f['cpu_main']
detail=dict(actualOwnedUpperEntries=upper,ownBit4Onsets=onsets,
            fullCampaignAccepted=False,fullPortAccepted=False)
(out/'native-entries.json').write_text(json.dumps(detail,indent=2)+'\n')
print(json.dumps(dict(actualOwnedUpperEntries=len(upper),ownBit4Onsets=len(onsets),
                     onsetPCs=sorted({f['pc'] for f in onsets}))))
