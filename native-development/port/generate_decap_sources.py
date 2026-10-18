"""Prepare authored headless-body rasters; no retired runtime payload consumed."""
import json
import struct
import sys
from PIL import Image
from generate_head_sources import PORT, components, sha
import import_character_art as art

OUT=PORT/'assets/decap'
SOURCES={
    'kano-first':('kano-bodies-first-five.png','EF72EDCBF572B9D460B4372C95F32F43EAAD4F2C7B3F090C6F93920BE4435A13'),
    'kano-last':('kano-bodies-last-two.png','91AC4E2E7AECC9F9EFD9FF083FD46CEE4C6A88EF04C6EF1858D02668FB51CC5E'),
    'sonya':('sonya-bodies.png','805F6A9E244D0CEECB0706B6C2CE5BB7744AF6DEB26C0850A1C1E5215D28C674')}

def main():
    assert not OUT.exists() or '--refresh-generated' in sys.argv
    OUT.mkdir(exist_ok=True)
    parts={};provenance={}
    for key,(name,expected) in SOURCES.items():
        raw=(art.ROOT/'art_native_death_v893'/name).read_bytes()
        assert sha(raw)==expected
        (OUT/name).write_bytes(raw)
        with Image.open(OUT/name) as image:
            parts[key]=components(image.convert('RGBA'))
        provenance[key]=dict(file=name,SHA256=expected,components=len(parts[key]))
    assert [len(parts[k]) for k in SOURCES]==[6,2,7]
    # The first Kano sheet's final pair is connected: use its first five
    # components, then the separately authored two final collapse frames.
    actors={'kano':parts['kano-first'][:5]+parts['kano-last'],'sonya':parts['sonya']}
    program=(art.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    report=dict(format='MK2KS-DECAP-PALETTE-INDEX-PGM-1',sources=provenance,
                actors={},transparentIndex=0,maxIndex=63,visualAcceptance=False,
                runtimeVerified=False,fullPortVerified=False)
    preview=Image.new('RGBA',(1120,340),(35,35,40,255))
    for row,(actor,offset) in enumerate((('kano',0x92bbc),('sonya',0x92cf2))):
        colors=struct.unpack_from('<64H',program,offset+4)
        palette=[(0,0,0)]+[((v>>10&31)*255//31,(v>>5&31)*255//31,(v&31)*255//31) for v in colors[:63]]
        upright=(110 if actor=='kano' else 105)/actors[actor][0][1].height
        prone=(130 if actor=='kano' else 125)/actors[actor][6][1].width
        frames=[];nearest={}
        for phase,(box,image,area) in enumerate(actors[actor]):
            scale=upright if phase<5 else prone
            w,h=max(1,round(image.width*scale)),max(1,round(image.height*scale))
            image=image.resize((w,h),Image.Resampling.LANCZOS)
            indices=[]
            for r,g,b,a in image.getdata():
                if a<128:
                    indices.append(0);continue
                key=(r,g,b)
                if key not in nearest:
                    nearest[key]=min(range(1,64),key=lambda i:sum((key[c]-palette[i][c])**2 for c in range(3)))
                indices.append(nearest[key])
            filename=f'{actor}_{phase}.pgm'
            text=f'P2\n# Native palette indices, not grayscale luminance.\n{w} {h}\n63\n'
            text+='\n'.join(' '.join(map(str,indices[y*w:(y+1)*w])) for y in range(h))+'\n'
            (OUT/filename).write_text(text,encoding='ascii')
            # Own ordinary-body ground plane, not inherited Liu sprite pivots.
            bottom=131 if actor=='kano' else 132
            frames.append(dict(phase=phase,file=filename,width=w,height=h,
                xOffset=(14,20,14,13,15,10,15)[phase],yOffset=h-bottom,
                fileSHA256=sha((OUT/filename).read_bytes()),indexSHA256=sha(bytes(indices)),
                sourceBox=box,uniformScale=scale,pivotRuntimeCalibrated=False))
            decoded=Image.new('RGBA',(w,h))
            decoded.putdata([(*palette[i],255) if i else (0,0,0,0) for i in indices])
            preview.alpha_composite(decoded,(phase*160+5,row*170+140-h))
        report['actors'][actor]=dict(frames=frames)
    (OUT/'DECAP_SOURCE.json').write_text(json.dumps(report,indent=2)+'\n')
    preview.save(OUT/'palette_preview.png')
    print(json.dumps(dict(frames=14,visualAcceptance=False,runtimeVerified=False)))

if __name__=='__main__':main()
