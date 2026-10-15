"""Timed falling-body raster regression, not full artistic/impact acceptance.

Uses the observer's fixed 3-field snapshot cadence and native draw chronology.
Never searches for a best pose, position, costume or RGB tolerance. The first
white-flash snapshot is excluded explicitly; native impact/shake/foreground
frames are outside this bounded falling-body contract.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image
from inspect_native_pit_pixels_v602 import poses
from verify_native_pit_scene_v602_v4 import need


def check_frame(image,pose):
    need(image.shape==(254,400,3),'Exact retained native raster dimensions')
    mask=pose['indices']!=0
    h,w=mask.shape;x,y=pose['left'],pose['top']
    actual=image[y:y+h,x:x+w]
    need(actual.shape==pose['normal'].shape,'Actual centered body inside native raster')
    matches=int(np.count_nonzero(np.all(actual==pose['normal'],axis=2)&mask))
    opaque=int(np.count_nonzero(mask))
    need(matches==opaque,'Every opaque native body pixel at fixed phase/origin/normal palette')
    return opaque


def verify(folder,fighter,episodes):
    body=poses(fighter);frames=[]
    for episode in episodes:
        start=episode['pit_enter']
        # Snapshot reads the retained front buffer, not the just-enqueued
        # native copier's current-field output. This is the fixed observed
        # cadence of this observer, identical in P1/P2/mirror captures.
        first=((start+6)//3)*3
        for index in range(19):
            frame=first+index*3;phase=index%5
            path=Path(folder)/'snap'/f'campaign_pit_{frame}.png'
            need(path.is_file(),'Each timed falling raster retained')
            image=np.asarray(Image.open(path).convert('RGB'))
            opaque=check_frame(image,body[phase])
            frames.append(dict(file=path.name,episode=episode.get('episode',1),phase=phase,opaque_pixels=opaque))
    return dict(passed=True,fighter=fighter,frames=frames,checked_frames=len(frames),
                opaque_pixels=sum(r['opaque_pixels']for r in frames),fullPortAcceptance=False,
                scope='Timed native falling-body pixels only: fixed phase, centered origin and exact normal palette. Not white flash, impact/shake/foreground, whole artistic/audio or campaign acceptance.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path);parser.add_argument('fighter',choices=('kano','sonya'))
    parser.add_argument('scene_proof',type=Path);args=parser.parse_args()
    proof=json.loads(args.scene_proof.read_text(encoding='utf-8-sig'))
    need(proof.get('passed')and proof.get('fighter')==args.fighter,'Actual matched scene proof required')
    episodes=proof['episodes']if 'episodes'in proof else [proof]
    print(json.dumps(verify(args.folder,args.fighter,episodes),indent=2))
