"""Independently check original Sonya projectile physics, not port acceptance.

Does not claim full input-gate validation: the existing Kano-only input verdict
is intentionally false for this Sonya discovery capture.
"""
import argparse
import json
import re
import struct
from pathlib import Path


def verify_rom(program):
    def words(address,count):
        return struct.unpack_from('<'+'H'*count,program,(address-0xff800000)//8)
    assert words(0xff9af7c0,5)==(0x09e5,0,6,0x09cb,0x8000), 'Launch velocity/acceleration changed'
    assert words(0xff9af8e0,3)==(0x09e0,0,0xfff9), 'Initial vertical velocity changed'
    assert words(0xff9af9c0,2)==(0x0b00,0x4000), 'Ascent acceleration changed'
    assert words(0xff9afa10,1)==(0x194b,), 'Ten-field turn changed'
    assert words(0xff9afab0,3)==(0x0b20,0x8000,0), 'Turn acceleration changed'
    assert words(0xff9afbb0,2)==(0x0be5,0xffa7), 'Floor-minus-88 homing target changed'
    assert words(0xff9afc50,6)==(0x09c0,16,0x5803,0x5805,0xb268,0x40), 'Sixteen-field homing velocity changed'
    assert words(0xff9afd10,2)==(0x09cb,16), 'Homing duration changed'


def verify(log):
    errors=[]
    selection=re.search(r'MK3_FATALITY_SELECTION frame=\d+ ids=1,0 own=([0-9A-F]{8}) victim=([0-9A-F]{8})',log)
    owners=re.search(r'MK3_FATALITY_FINISH_OWNERS frame=\d+ own=([0-9A-F]{8}) victim=([0-9A-F]{8})',log)
    if not selection or not owners:
        errors.append('Missing current Sonya/Kano human-selection and final-round ownership evidence')
    owner=int(owners[1],16) if owners else None
    code=[]
    for match in re.finditer(r'MK3_SONYA_CONTACT_CODE frame=(\d+) at=([0-9A-F]{8}) a8=([0-9A-F]{8}) a11=([0-9A-F]{8}) owner=([0-9A-F]{8}) child=(none|[0-9A-F]{8})',log):
        code.append(dict(frame=int(match[1]),at=int(match[2],16),actor=int(match[3],16),
                         owner=int(match[5],16),child=int(match[6],16) if match[6]!='none' else None))
    launch=next((r for r in code if r['at']==0xff9af630 and r['actor']==owner and r['owner']==owner),None)
    child=next((r['child'] for r in code if r['at']==0xff9af7a0 and launch and r['frame']==launch['frame']),None)
    if not launch or not child:
        errors.append('Missing original launch and owned child task')
    rows={}
    pattern=(r'MK3_SONYA_CONTACT_FRAME frame=(\d+) launch_age=(\d+) child=([0-9A-F]{8}) '
             r'x=(-?\d+) y=(-?\d+) vx=([0-9A-F]{8}) vy=([0-9A-F]{8}) graphic=([0-9A-F]{8}) '
             r'victim_x=(-?\d+) victim_y=(-?\d+) victim_pose=([0-9A-F]{8}) owner_x=(-?\d+) owner_y=(-?\d+)')
    for m in re.finditer(pattern,log):
        age=int(m[2])
        if age in rows:
            errors.append('Duplicate launch-age sample')
        rows[age]=dict(frame=int(m[1]),child=int(m[3],16),x=int(m[4]),y=int(m[5]),
                       vx=int(m[6],16),vy=int(m[7],16),graphic=int(m[8],16),
                       victim_x=int(m[9]),owner_x=int(m[12]))
    if not all(age in rows for age in range(1,60)):
        errors.append('Missing continuous launch-to-contact samples')
    else:
        direction=1 if rows[1]['victim_x']>rows[1]['owner_x'] else -1
        for age in range(1,60):
            row=rows[age]
            if row['child']!=child or not launch or row['frame']!=launch['frame']+age:
                errors.append(f'Incorrect actor or clock at projectile age {age}')
            if age<=4:
                vx,vy=direction*6*65536,0
            elif age<=33:
                vx=direction*(6*65536-(age-5)*32768)
                vy=-7*65536+(age-5)*16384
            elif age<=42:
                step=age-33
                vx=direction*(-8*65536)+sum(range(11-step,11))
                vy=step*32768
            else:
                vx,vy=rows[43]['vx'],rows[43]['vy']
            if (row['vx'],row['vy'])!=(vx&0xffffffff,vy&0xffffffff):
                errors.append(f'Original physics differs at age {age}')
        observed={rows[age]['graphic'] for age in range(1,43)}
        expected={0xffb263f0+i*0x70 for i in range(8)}
        if observed!=expected:
            errors.append('The eight ascent/turn graphic frames are incomplete')
        if abs(rows[59]['x']-rows[59]['victim_x'])>1:
            errors.append('Projectile did not reach the victim at the end of homing')
        for address,age,actor in ((0xff9afdc0,58,child),(0xff9b0100,59,int(owners[2],16) if owners else None)):
            if not any(r['at']==address and r['actor']==actor and launch and r['frame']==launch['frame']+age for r in code):
                errors.append('Missing ordered projectile retirement/victim burn transition')
    if not re.search(r'MK3_FATALITY_INPUT_RESULT pass=false fighter=sonya round_health_writes=\d+ position_writes=0 auto_cheat=false',log):
        errors.append('Missing explicit no-position-write/no-cheat accounting')
    if re.search(r'\[LUA ERROR\]|fatal error|access violation|MK3_FATALITY_(?:CLOSE_ASSIST|ORIENTATION_ASSIST|AUTO_CHEAT|STAGE_ASSIST)',log,re.I):
        errors.append('Forbidden assistance or runtime error')
    return dict(passed=not errors,scope='original_sonya_projectile_physics_not_port_or_full_input_acceptance',
                original_input_gate_validation_complete=False,samples=len(rows),
                launch_frame=launch['frame'] if launch else None,errors=errors)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log',type=Path)
    args=parser.parse_args()
    verify_rom((Path(__file__).resolve().parents[1]/'mk3/mk3-maincpu.bin').read_bytes())
    result=verify(args.log.read_text(encoding='utf-8-sig'))
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__=='__main__':
    main()
