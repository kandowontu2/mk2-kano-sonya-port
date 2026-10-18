"""Explicit own throw victim descriptors; no numeric actor-animation alias."""
import json
from pathlib import Path
PORT=Path(__file__).resolve().parent
OUT=PORT/'generated_throw'
out=OUT/'KSTHVIC.ASM'
assert not out.exists()
leg=json.loads((PORT/'generated_leg/LEG_ASSETS.json').read_text())['victims']
own=json.loads((OUT/'THROW_DATA.json').read_text())['actors']
lines=['; Authored throw victim descriptors. Original-roster XY needs visual QA.',
       '        .include mainequ.asm','        .data']
refs=set();report={}
for owner in ('kano','sonya'):
    table=f'ks_throw_{owner}_victims'
    lines.extend([f'        .def {table}',table])
    for identity in range(19):lines.append('        .long '+('0' if identity in (12,13) else f'ks_tv_{owner}_{identity}'))
    report[owner]={}
    for key,entry in leg.items():
        identity=int(key)
        poses=[record[2] for record in entry['records']]
        if identity in (17,18):
            actor='kano' if identity==17 else 'sonya'
            records=own[actor]['asVictim'][owner]['records']
            paired=f'ks_th_{owner}_v_{actor}'
            flight=paired+'_flight'
            grab=records[0][2]
            refs.update((paired,flight,grab))
            provenance='original own MK3 throw XY and pose records'
        else:
            # Explicit named composites from this victim, never another actor.
            xy=[(-57,-16),(-35,-54),(66,-71)] if owner=='kano' else [(-36,0),(-22,1),(30,-26),(93,-31),(129,-35)]
            selected=poses[1:4] if owner=='kano' else poses[1:]+[poses[-1]]
            records=[[x,y,pose] for (x,y),pose in zip(xy,selected)]
            paired=f'ks_tp_{owner}_{identity}'
            flight=f'ks_tf_{owner}_{identity}'
            grab=poses[1]
            refs.update(poses)
            provenance='own native composites; authored XY adaptation awaiting visual qualification'
        lines.extend([f'ks_tv_{owner}_{identity}',f'        .long {grab},{paired},{flight}'])
        if identity not in (17,18):
            lines.append(paired)
            for x,y,pose in records:lines.extend([f'        .word {x},{y}',f'        .long {pose}'])
            lines.extend([flight,'        .long '+','.join(poses[3:]+['0'])])
        report[owner][key]={'records':records,'provenance':provenance,'runtimeVerified':False}
lines[3:3]=['        .ref '+name for name in sorted(refs)]
out.write_text('\n'.join(lines)+'\n')
(OUT/'THROW_VICTIMS.json').write_text(json.dumps({'owners':report,'bossesExcluded':[12,13],'fullPortVerified':False},indent=2)+'\n')
print('Generated explicit descriptors for17 non-boss victims per thrower.')
