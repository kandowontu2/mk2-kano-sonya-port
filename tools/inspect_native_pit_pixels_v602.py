"""Read-only diagnostic: actual Pit raster versus its native packed body pens.

No image resizing, painting, generated-asset editing or guest state changes.
Phase association/acceptance is deliberately left to an independent verifier.
"""
import argparse
import json
import struct
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def poses(fighter):
    payload=(ROOT/'diagnostic_v602_native_pit_position/roms/mk2ks/mk2ks.mdata').read_bytes()
    program=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    number=0 if fighter=='kano' else 1
    palette_at=((0x92BBC,0x92C3E),(0x92CF2,0x92D74))[number]
    palettes=[]
    for at in palette_at:
        if struct.unpack_from('<I',program,at)[0]!=64:raise ValueError('Original palette header')
        colors=[(0,0,0)]
        for color in struct.unpack_from('<64H',program,at+4):
            channels=[(color>>shift)&31 for shift in (10,5,0)]
            colors.append(tuple((c<<3)|(c>>2)for c in channels))
        palettes.append(np.array(colors,dtype=np.uint8))
    result=[]
    for phase in range(6):
        at=0x130800+(number*6+phase)*16
        width,height,xo,yo,bits,command=struct.unpack_from('<4hIH',payload,at)
        if command!=0x6000:raise ValueError('Full-copy native six-bit descriptor')
        source=0x134000+bits//8-0x1E80000
        count=(width*height*6+7)//8
        raw=payload[source:source+count]
        indices=np.empty(width*height,dtype=np.uint8)
        for pixel in range(width*height):
            bit=pixel*6
            indices[pixel]=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&63
        indices=indices.reshape(height,width)
        result.append(dict(phase=phase,left=192-xo,top=64-yo,indices=indices,
                           normal=palettes[0][indices],alternate=palettes[1][indices]))
    return result


def inspect(folder,fighter):
    body=poses(fighter);report=[]
    for path in sorted((Path(folder)/'snap').glob('campaign_pit_*.png')):
        if 'exit' in path.stem:continue
        image=np.asarray(Image.open(path).convert('RGB'))
        best=None
        for pose in body:
            mask=pose['indices']!=0
            h,w=mask.shape;x,y=pose['left'],pose['top']
            actual=image[y:y+h,x:x+w]
            if actual.shape!=(h,w,3):raise ValueError('Expected actor outside raster')
            for variant in ('normal','alternate'):
                matches=int(np.count_nonzero(np.all(actual==pose[variant],axis=2)&mask))
                count=int(np.count_nonzero(mask))
                candidate=dict(file=path.name,phase=pose['phase'],variant=variant,
                               matches=matches,opaque=count,ratio=matches/count)
                if best is None or candidate['ratio']>best['ratio']:best=candidate
        report.append(best)
    return dict(scope='pixel_diagnostic_not_independent_phase_or_palette_acceptance',fighter=fighter,frames=report)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path);parser.add_argument('fighter',choices=('kano','sonya'))
    args=parser.parse_args();print(json.dumps(inspect(args.folder,args.fighter),indent=2))
