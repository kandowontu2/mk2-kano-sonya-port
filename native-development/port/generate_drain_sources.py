"""Recover authored soul-drain art as readable native palette-index sources.

Encoding only. Legacy executable payloads and custom emulator hooks are unused.
"""
import json
import struct
import sys
from PIL import Image
from generate_head_sources import PORT, sha
import import_character_art as art

OUT=PORT/'assets/drain'
ASSETS=(('kano','911755BFFE92E49E620DBEAC1ED3E821B7107DFB48C96FB59ACBAC5801971152',0x92bbc),
        ('sonya','E159587A7FE975097C2DF7F0F4628C020AD5DCE91C3AF5F2C1D20F4A0E7A9376',0x92cf2))

def main():
    assert not OUT.exists() or '--refresh-generated' in sys.argv
    OUT.mkdir(exist_ok=True)
    program=(art.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    assert sha(program)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    report=dict(format='MK2KS-DRAIN-PALETTE-INDEX-PGM-1',actors={},
                transparentIndex=0,maxIndex=63,alphaThreshold=128,
                visualAcceptance=False,runtimeVerified=False,fullPortVerified=False)
    preview=Image.new('RGBA',(480,300),(35,35,40,255))
    for row,(actor,expected,offset) in enumerate(ASSETS):
        name=actor+'-drain-draft-v1.png'
        raw=(art.ROOT/'art_native_shang_drain'/name).read_bytes()
        assert sha(raw)==expected
        (OUT/name).write_bytes(raw)
        colors=struct.unpack_from('<64H',program,offset+4)
        palette=[(0,0,0)]+[((v>>10&31)*255//31,(v>>5&31)*255//31,(v&31)*255//31) for v in colors[:63]]
        nearest={};frames=[]
        with Image.open(OUT/name) as image:
            assert image.mode=='RGBA' and image.size==(1536,1024)
            for phase,height in enumerate((125,119,113)):
                cell=image.crop((phase*512,0,(phase+1)*512,1024))
                box=cell.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
                assert box and 0<box[0]<box[2]<512 and 0<box[1]<box[3]<1024
                scale=height/(box[3]-box[1])
                width=round((box[2]-box[0])*scale)
                assert 20<=width<=80
                scaled=cell.crop(box).resize((width,height),Image.Resampling.LANCZOS)
                indices=[]
                for r,g,b,a in scaled.getdata():
                    if a<128:
                        indices.append(0);continue
                    key=(r,g,b)
                    if key not in nearest:
                        nearest[key]=min(range(1,64),key=lambda i:sum((key[c]-palette[i][c])**2 for c in range(3)))
                    indices.append(nearest[key])
                feet=[i%width for i in range((height-3)*width,height*width) if indices[i]]
                assert len(feet)>3
                # These are deliberately lifted sprites, not standing bodies.
                # Match native SOULSUCKHO1/2/3 origins at the identical heights;
                # the shared CORPSE handoff uses that same coordinate system.
                xoffset=(-2,-2,-3)[phase]
                yoffset=(5,3,1)[phase]
                filename=f'{actor}_{phase}.pgm'
                text=f'P2\n# Native palette indices, not grayscale luminance.\n{width} {height}\n63\n'
                text+='\n'.join(' '.join(map(str,indices[y*width:(y+1)*width])) for y in range(height))+'\n'
                (OUT/filename).write_text(text,encoding='ascii')
                frames.append(dict(phase=phase,file=filename,width=width,height=height,
                    xOffset=xoffset,yOffset=yoffset,sourceCellBox=box,uniformScale=scale,
                    fileSHA256=sha((OUT/filename).read_bytes()),indexSHA256=sha(bytes(indices)),
                    pivotBasis='Native MKFX SOULSUCKHO1/2/3 descriptor origins at identical raster heights',
                    pivotRuntimeCalibrated=False))
                decoded=Image.new('RGBA',(width,height))
                decoded.putdata([(*palette[i],255) if i else (0,0,0,0) for i in indices])
                preview.alpha_composite(decoded,(phase*160+40,row*150+140-height))
        report['actors'][actor]=dict(sourceFile=name,sourceSHA256=expected,frames=frames)
    (OUT/'DRAIN_SOURCE.json').write_text(json.dumps(report,indent=2)+'\n')
    preview.resize((960,600),Image.Resampling.NEAREST).save(OUT/'palette_preview.png')
    print(json.dumps(dict(frames=6,visualAcceptance=False,runtimeVerified=False)))

if __name__=='__main__':main()
