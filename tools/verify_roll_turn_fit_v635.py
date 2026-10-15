"""Evidence-backed decision for five current native turn contacts, not all matchups."""
import argparse
import json
import re
import struct
from pathlib import Path
from inspect_roll_sprite_planes_v635_v2 import inspect_case
from verify_native_ui_flow_v635 import ROOT,NAME,EXE,PAYLOAD,digest


def need(condition,message):
    if not condition:raise ValueError(message)


def check_fit(cases):
    need(len(cases)==6 and{(c['victim'],c['side'])for c in cases}==
         {(v,s)for v in('kitana','mileena','raiden')for s in(1,2)},'All six current contact/miss controls')
    for case in cases:
        last=case['comparison_sprite_rows'][-1]
        target=case['victim'];side=case['side']
        contact=not(target=='raiden'and side==2)
        overlap=case['native']['lastComparison']
        need((last['attack_top'],last['attack_bottom'])==(106,137),'Current owned high roll plane')
        need((last['roles']['own']['id'],last['roles']['victim']['id'])==
             (17,{'kitana':4,'mileena':5,'raiden':7}[target]),'Real imported/stock identities')
        if contact:
            need(overlap['horizontal']>0 and overlap['vertical']>0,'Positive original comparator, not held-input inference')
            need(last['roles']['victim']['pixels_in_positive_comparator_intersection']==
                 (32 if target=='raiden'else 6 if side==1 else 2),'Real exposed original target pixels inside both rectangles')
            own=last['roles']['own']
            need(own['top']<=last['attack_top']<last['attack_bottom']<=own['bottom']+1 and
                 own['pixels_in_attack_rectangle']==1118,'High box fits actual rolling composite, not shifted above art')
        else:
            need(overlap['horizontal']<0 and last['roles']['victim']['pixels_in_attack_rectangle']==0 and
                 last['roles']['victim']['pixels_in_positive_comparator_intersection']==0,'Independent opposite-side separating/miss control')
    return dict(decision='Retain the current high roll box and original pose-aware CMPXY collision for these five stock crouching-turn contacts',
                reason='Actual opaque head/hat pixels lie inside the authored attack and original native hurtbox at first positive overlap; normal earlier crouches separate. Opposite-side Raiden remains a genuine horizontal miss.',
                observedTurnFitAccepted=True,planeCorrectionNeededForTheseFive=False,
                fullContactFidelityAccepted=False,fullPortAcceptance=False)


def verify():
    code=ROOT/'audit_v649_native_sprite_coordinate_code'
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(digest(ROOT/'mk2/mk2-maincpu.bin')=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Original native sprite code')
    # Verify the observed disassembly words against the original instruction
    # stream, including complete function entry and cache/flip arithmetic.
    observed={}
    for line in(code/'body-context.asm').read_text().splitlines():
        m=re.match(r'([0-9A-F]{8}): ((?:[0-9A-F]{4} )+)',line)
        if not m:continue
        start=int(m[1],16);words=[int(w,16)for w in m[2].split()]
        for index,word in enumerate(words):
            at=start+index*16
            need(struct.unpack_from('<H',original,(at-0xff800000)//8)[0]==word,'Actual observed sprite code is original')
            observed[at]=word
    need(all(at in observed for at in(0xff804000,0xff8041b0,0xff804280,0xff804290,0xff804350,0xff804370,0xff804380,0xff8043f0)),
         'Valid complete native entry/cache SUBXY/XFlip width-minus-one coordinate context')
    compiled=(code/'compiled-roll.bin').read_bytes()
    need(len(compiled)==32 and struct.unpack_from('<9H',compiled)==(57,8,72,31,0x1417,0x1805,0,0,1),'Actual compiled unchanged native roll descriptor')
    cases=[];inputs={}
    for victim in('kitana','mileena','raiden'):
        for side in(1,2):
            case,checked=inspect_case(victim,side);cases.append(case);inputs.update(checked)
    decision=check_fit(cases)
    return dict(candidate=NAME,executable_sha256=EXE,payload_sha256=PAYLOAD,
                scope='Five exposed native stock crouching-turn contacts and opposite Raiden miss; not universal duck immunity, every matchup or original-MK3 target-specific equivalence',
                cases=cases,decision=decision,checked_inputs=inputs,fullPortAcceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();encoded=json.dumps(verify(),indent=2)
    if args.output:args.output.write_text(encoded+'\n',encoding='utf-8')
    else:print(encoded)
