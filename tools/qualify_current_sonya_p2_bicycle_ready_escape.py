"""Native identity/contact gates and finite physical recovery observations."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_sonya_p2_kunglao_midrange_bicycle.py').read_text().replace('audit_current_sonya_p2_kunglao_midrange_bicycle','audit_current_sonya_p2_bicycle_ready_escape')
exec(compile(source,__file__+'::native_context','exec'))
escapes=rows.get('BICYCLE_READY_ESCAPE',[])
assert all(int(r['flags'],16)&0x1c==0 and int(r['action']) in (0,771,772,770,1792,1793,3) for r in escapes)
fields=[r for r in rows['LIVE'] if r['stage']=='3']
air=[r for r in fields if int(r['hfloor'])-int(r['hpos'].split(',')[1])>8]
(out/'recovery-observations.json').write_text(json.dumps(dict(passed=True,readyEscapePlans=len(escapes),sampledAirborneFields=len(air),sampledOwnAirActions=sorted(set(int(r['actions'].split(',')[0]) for r in air)),kungLaoMatchCleared=4 in stages,fullCampaignAccepted=False,fullPortAccepted=False),indent=2)+'\n')
print('Ready escape plans: '+str(len(escapes))+'; sampled airborne fields: '+str(len(air)))
