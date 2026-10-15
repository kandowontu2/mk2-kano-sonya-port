"""Verify actual native projectile physics and a rendered final contact field.

Original-ROM rules are independently checked. This does not replace visual QA,
audio checks, other victims, or whole-game acceptance.
"""
import argparse
import json
import math
import re
from pathlib import Path
from verify_sonya_contact_reference import verify_rom


def verify(log,side):
    errors=[]
    tick_pattern=(r'MK2_SONYA_NATIVE_TICK frame=(\d+) age=(\d+) actor=([0-9A-F]{8}) '
                  r'process=([0-9A-F]{8}) vx=([0-9A-F]{8}) vy=([0-9A-F]{8}) sequence=([0-9A-F]{8}) loop=(\d+)')
    ticks=[dict(frame=int(m[1]),age=int(m[2]),actor=int(m[3],16),
                vx=int(m[5],16),vy=int(m[6],16),sequence=int(m[7],16))
           for m in re.finditer(tick_pattern,log)]
    contact=re.search(r'MK2_SONYA_NATIVE_CONTACT frame=(\d+) age=(\d+) actor=([0-9A-F]{8}) '
                      r'child=([0-9A-F]{8}) x=(-?\d+) y=(-?\d+) target_x=(-?\d+) target_y=(-?\d+) '
                      r'graphic=([0-9A-F]{8}) flags=([0-9A-F]{4})',log)
    rows=[]
    for m in re.finditer(r'MK2_SONYA_CONTACT_FRAME frame=(\d+) action_age=(\d+) side=(\d+) child=([0-9A-F]{8}) '
                         r'present=(true|false) owner_x=(-?\d+) owner_y=(-?\d+) victim_x=(-?\d+) victim_y=(-?\d+) '
                         r'victim_pose=([0-9A-F]{8}) child_x=(-?\d+) child_y=(-?\d+) child_graphic=([0-9A-F]{8}) flags=([0-9A-F]{4})',log):
        rows.append(dict(frame=int(m[1]),side=int(m[3]),child=int(m[4],16),present=m[5]=='true',
                         own_x=int(m[6]),victim_x=int(m[8]),victim_pose=int(m[10],16),
                         x=int(m[11]),y=int(m[12]),graphic=int(m[13],16)))
    if len(ticks)!=59 or [r['age'] for r in ticks]!=list(range(1,60)):
        errors.append('Missing ordered 59 native motion steps')
    if not contact:
        errors.append('Missing native retirement/contact evidence')
    if ticks and contact and len(ticks)==59:
        own=int(contact[3],16)
        direction=1 if side==1 else -1
        table=0xfffb2800 if side==1 else 0xfffb2c00
        for t in ticks:
            age=t['age']
            if age<=5:
                vx,vy=direction*6*65536,0
            elif age<=33:
                vx=direction*(6*65536-(age-6)*32768)
                vy=-7*65536+(age-6)*16384
            elif age<=43:
                n=age-34
                vx=direction*(-8*65536)+sum(range(11-n,11))
                vy=n*32768
            else:
                vx,vy=ticks[43]['vx'],ticks[43]['vy']
            if (t['vx'],t['vy'])!=(vx&0xffffffff,vy&0xffffffff):
                errors.append(f'Wrong pre-integration original velocity at age {age}')
            if t['actor']!=own or t['sequence']!=table or t['frame']!=ticks[0]['frame']+age-1:
                errors.append(f'Wrong ownership, frame table or native clock at age {age}')
        home=next((r for r in rows if r['frame']==ticks[43]['frame'] and r['present']),None)
        if not home:
            errors.append('Missing published homing origin')
        else:
            vx=math.trunc((int(contact[7])-home['x'])*65536/16)&0xffffffff
            vy=math.trunc((int(contact[8])-home['y'])*65536/16)&0xffffffff
            if (ticks[43]['vx'],ticks[43]['vy'])!=(vx,vy):
                errors.append('Homing velocity does not target the current victim over 16 fields')
        if int(contact[2])!=59 or int(contact[1])!=ticks[-1]['frame']+1:
            errors.append('Final point must render for one field before child retirement')
        if abs(int(contact[5])-int(contact[7]))>1 or abs(int(contact[6])-int(contact[8]))>1:
            errors.append('Native final point missed the actual victim/floor target')
        rendered=next((r for r in rows if r['frame']==int(contact[1]) and r['present']),None)
        if not rendered or rendered['child']!=int(contact[4],16) or rendered['x']!=int(contact[5]) or rendered['y']!=int(contact[6]):
            errors.append('Final contact point was never published as a live visible child')
        if rendered and rendered['victim_pose']==0xfe9b0ae0:
            errors.append('Victim started burning before the visible contact point')
        first_burn=next((r for r in rows if r['victim_pose']==0xfe9b0ae0),None)
        if not first_burn or first_burn['frame']<=int(contact[1]) or first_burn['present']:
            errors.append('Missing ordered contact/child retirement/victim burn transition')
        frames=0xfffb1800 if side==1 else 0xfffb2000
        seen={r['graphic'] for r in rows if r['present'] and r['frame']<=ticks[42]['frame']}
        if seen!={frames+i*0x100 for i in range(8)}:
            errors.append('Actual ascent/turn did not publish all eight original frames')
    for marker in ('MK2_RANGE_RESULT pass=true ','MK2KS_EXIT_RESULT pass=true ',
                   'MK2KS_STABILITY stalled_frames=0 trap_frames=0',
                   'MK2KS_DISPLAY_RESULT pass=true ','MK2KS_HUD_SHADOW_RESULT pass=true '):
        if marker not in log:
            errors.append('Missing existing gameplay/identity/display gate: '+marker)
    if re.search(r'\[LUA ERROR\]|fatal error|access violation|MK2_FINISH_POSITION_ASSIST',log,re.I):
        errors.append('Runtime error or forbidden position assistance')
    return dict(passed=not errors,scope='native_physics_and_rendered_contact_not_whole_game_acceptance',
                side=side,motion_steps=len(ticks),errors=errors)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log',type=Path)
    parser.add_argument('--side',type=int,choices=(1,2),required=True)
    args=parser.parse_args()
    verify_rom((Path(__file__).resolve().parents[1]/'mk3/mk3-maincpu.bin').read_bytes())
    result=verify(args.log.read_text(encoding='utf-8-sig'),args.side)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__=='__main__':
    main()
