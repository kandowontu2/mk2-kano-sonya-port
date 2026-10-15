"""Read actual native boss-victim field/task states; never a tower-clear gate."""
import argparse
import json
import re
from pathlib import Path


def inspect(folder):
    text=(folder/'run.log').read_text(encoding='utf-8-sig')
    rows=[]
    for match in re.finditer(r'^MK2_NAT_CAMPAIGN_BOSS_FIELD (.*)$',text,re.M):
        row=dict(re.findall(r'(\w+)=([^\s]+)',match[1]))
        for key in ('frame','human_slot','age','slot','id','roster','state','hp','x','y','floor'):row[key]=int(row[key])
        for key in ('actor','main','owner','action','flags','pose','vx','vy'):row[key]=int(row[key],16)
        row['task']={int(k,16):int(v,16) for k,v in (part.split(':') for part in row['task'].split(','))}
        rows.append(row)
    own=[r for r in rows if r['slot']==r['human_slot']]
    if not own:return dict(fields=0,error='No actual stomp-victim fields yet')
    first=own[0]
    changes=[];last=None
    for row in own:
        key=(row['flags'],row['action'],row['pose'],row['y'],row['hp'])
        if key!=last:
            code_fields={f'{k:03X}':f'{v:08X}' for k,v in row['task'].items() if 0xff800000<=v<=0xffffffff}
            changes.append({k:row[k] for k in ('age','frame','hp','x','y','floor','action','flags','pose')}|dict(native_code_fields=code_fields))
            last=key
    first_clear=next((r for r in own if r['age']>0 and r['flags']&4==0 and r['y']==r['floor']),None)
    first_move=next((r for r in own if first_clear and r['age']>=first_clear['age'] and r['x']!=first_clear['x']),None)
    return dict(fields=len(own),id=first['id'],human_slot=first['human_slot'],first_hp=first['hp'],
                first_clear_age=first_clear['age'] if first_clear else None,
                first_post_clear_move_age=first_move['age'] if first_move else None,
                changes=changes,scope='Native sampled boss-victim state discovery; not rendered fidelity or unassisted clear')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path)
    args=parser.parse_args();print(json.dumps(inspect(args.folder),indent=2))
