"""Current instruction-time roll/crouch sprite rows, not plane-fidelity approval."""
import json
import re
from pathlib import Path
import numpy as np
from inspect_natural_arena_floor_v602 import decoder
from inspect_roll_turn_contacts_v545 import rows,inspect_log,xy
from verify_native_ui_flow_v635 import ROOT,NAME,EXE,PAYLOAD,digest


def check_launch(folder,victim,side):
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    assert (result['exit_code'],result['candidate'],result['executable_sha256'],result['payload_sha256'],
            result['move'],result['side'],result['scenario'],result['victim'],result['assistance'])==\
           (0,NAME,EXE,PAYLOAD,'ball',side,'miss',victim,'none')
    assert before==result['input_hashes']
    for filename,sha in before.items():
        assert digest(filename)==sha,'Matched current launch input'
        if Path(filename).suffix in('.lua','.ps1','.json'):
            assert digest(folder/'input_sources'/Path(filename).name)==sha,'Exact frozen launch source'
    for script in ('mk2ks_cannonball_geometry_probe_v3.lua','mk2ks_human_special_negative_v9.lua'):
        text=(folder/'input_sources'/script).read_text()
        assert not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',text),'No guest state injection'
    return before


def inspect_case(victim,side):
    folder=ROOT/f'audit_v647_roll_art_p{side}_{victim}'
    inputs=check_launch(folder,victim,side)
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    prior=(ROOT/f'audit_v574_roll_pose_p{side}_{victim}/run.log').read_text(encoding='utf-8-sig')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    payload=(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    native=inspect_log(log,prior,side,victim,original,payload)
    buffers={}
    for line in log.splitlines():
        if not line.startswith('MK2_BALL_V3_GFX '):continue
        value=dict(re.findall(r'(\w+)=([^\s]+)',line))
        value['offset']=int(value['offset']);buffers[value['key']]=value
    decode=decoder(buffers)
    geometries=rows(log,'GEOMETRY');actors=rows(log,'ACTOR');parts=rows(log,'PART')
    amap={(a['frame'],a['role']):a for a in actors}
    records=[]
    for g in geometries:
        attack_top,attack_bottom=xy(g['attack_min'])[1],xy(g['attack_max'])[1]
        victims_top,victims_bottom=xy(g['victim_min'])[1],xy(g['victim_max'])[1]
        roles={}
        for role in('own','victim'):
            a=amap[g['frame'],role]
            ys=[];counts={}
            for component in[p for p in parts if p['frame']==g['frame']and p['role']==role]:
                indices=decode(component['source'],component['command']|0x8002,component['width'],component['height'])
                assert component['command']&32==0,'Original no-Y-flip cached component'
                for y,count in enumerate(np.count_nonzero(indices,axis=1)):
                    if count:
                        world_y=a['y']-component['dy']+y
                        ys.append(world_y);counts[world_y]=counts.get(world_y,0)+int(count)
            assert ys,'Actual opaque cached component rows'
            roles[role]=dict(id=a['id'],top=min(ys),bottom=max(ys),
                opaque_pixels=sum(counts.values()),
                pixels_in_attack_vertical_band=sum(count for y,count in counts.items()if attack_top<=y<attack_bottom),
                # A vertical band is not a two-dimensional collision proof.
                rows_in_attack_vertical_band=sorted(y for y in counts if attack_top<=y<attack_bottom))
        records.append(dict(frame=g['frame'],attack_top=attack_top,attack_bottom=attack_bottom,
                            victim_bound_top=victims_top,victim_bound_bottom=victims_bottom,roles=roles))
    return dict(victim=victim,side=side,native=native,comparison_sprite_rows=records,
                scope='Exact original/current comparator, cache/ROM poses and opaque world-Y rows only; no instruction-time rendered screenshot or 2D pixel-contact claim',
                contactFidelityAccepted=False,planeCorrectionClaim=False,fullPortAcceptance=False),inputs


if __name__=='__main__':
    cases=[];inputs={}
    for victim in('kitana','mileena','raiden'):
        for side in(1,2):
            case,checked=inspect_case(victim,side);cases.append(case);inputs.update(checked)
    print(json.dumps(dict(candidate=NAME,cases=cases,checked_inputs=inputs,
                          contactFidelityAccepted=False,planeCorrectionClaim=False,fullPortAcceptance=False),indent=2))
