"""Compile preserved torso art to readable indices with costume-safe Kano blood."""
import json
import struct
import sys
from PIL import Image
from generate_head_sources import PORT,sha
import import_character_art as art
SOURCE=PORT/'assets/torso_sources'
OUT=PORT/'assets/torso'
BOUNDS=((-7,-10,47,66),(-14,9,52,66),(-13,4,27,72),(-20,21,49,67),(-4,24,44,80),(-14,52,71,88))
COUNTS=(2,3,1,2,2,2,2)
def crop(image,box):
    cell=image.crop(box)
    bounds=cell.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
    assert bounds and min(bounds[:2])>=2 and bounds[2]<=cell.width-2 and bounds[3]<=cell.height-2
    return cell.crop(bounds),bounds
def rgb(v):return ((v>>10&31)*255//31,(v>>5&31)*255//31,(v&31)*255//31)
def main():
    assert not OUT.exists() or '--refresh-generated' in sys.argv
    OUT.mkdir(exist_ok=True)
    inputs=json.loads((SOURCE/'TORSO_INPUTS.json').read_text())
    for asset in inputs['assets']:assert sha((SOURCE/asset['file']).read_bytes())==asset['SHA256']
    program=(art.ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    lower=Image.open(SOURCE/'lower-stumps.png').convert('RGBA')
    guides=[Image.open(SOURCE/n).convert('RGBA') for n in ('kano-upper-blood-guide.png','lower-blood-guide.png')]
    result=dict(format='MK2KS-TORSO-PALETTE-INDEX-PGM-1',actors={},componentCounts=COUNTS,
                transparentIndex=0,maxIndex=63,visualAcceptance=False,runtimeVerified=False,fullPortVerified=False)
    preview=Image.new('RGBA',(1120,280),(35,35,40,255))
    for row,(actor,normal_at,alternate_at) in enumerate((('kano',0x92bbc,0x92c3e),('sonya',0x92cf2,0x92d74))):
        normal=[(0,0,0)]+[rgb(v) for v in struct.unpack_from('<64H',program,normal_at+4)[:63]]
        alternate=[(0,0,0)]+[rgb(v) for v in struct.unpack_from('<64H',program,alternate_at+4)[:63]]
        atlas=Image.open(SOURCE/f'{actor}-upper-torsos.png').convert('RGBA')
        parts=[crop(atlas,(i%3*512,i//3*512,(i%3+1)*512,(i//3+1)*512)) for i in range(6)]
        parts.append(crop(lower,(row*627,0,(row+1)*627,1254)))
        factor=76/parts[0][0].height
        if actor=='kano':assert all(normal[i]==alternate[i] for i in (48,46,63))
        frames=[];nearest={}
        for phase,(image,box) in enumerate(parts):
            scale=factor if phase<6 else 94/image.height
            w,h=round(image.width*scale),round(image.height*scale)
            assert 0<w<=120 and 0<h<=120
            scaled=image.resize((w,h),Image.Resampling.LANCZOS)
            guide=None
            if actor=='kano':
                cell=guides[0].crop((phase%3*512,phase//3*512,(phase%3+1)*512,(phase//3+1)*512)) if phase<6 else guides[1].crop((0,0,627,1254))
                guide=list(cell.crop(box).resize((w,h),Image.Resampling.LANCZOS).getdata())
            indices=[];blood_count=0
            for i,(r,g,b,a) in enumerate(scaled.getdata()):
                if a<128:indices.append(0);continue
                key=(r,g,b)
                if key not in nearest:
                    nearest[key]=min(range(1,64),key=lambda pen:sum((key[c]-normal[pen][c])**2 for c in range(3)))
                pen=nearest[key]
                if guide:
                    gr,gg,gb,ga=guide[i]
                    blood=(ga>=128 and gg>=gr+20 and gb>=gr+20 and gg*2>=gb and gb*2>=gg and r>max(g,b)*1.2+8)
                    if blood:
                        pen=min((48,46,63),key=lambda p:sum((key[c]-normal[p][c])**2 for c in range(3)))
                        blood_count+=1
                indices.append(pen)
            if actor=='kano':assert blood_count>0
            if phase<6:
                native=BOUNDS[phase];left=round((native[0]+native[2]-w)/2);bottom=native[3]
                if phase==5:bottom=(131 if actor=='kano' else 132)-80
            else:left=round((5-w)/2);bottom=141
            filename=f'{actor}_{phase}.pgm'
            text=f'P2\n# Native palette indices, not grayscale luminance.\n{w} {h}\n63\n'
            text+='\n'.join(' '.join(map(str,indices[y*w:(y+1)*w])) for y in range(h))+'\n'
            (OUT/filename).write_text(text,encoding='ascii')
            frames.append(dict(phase=phase,file=filename,width=w,height=h,xOffset=-left,yOffset=h-bottom,
                componentCount=COUNTS[phase],sourceCrop=box,uniformScale=scale,bloodPixels=blood_count,
                fileSHA256=sha((OUT/filename).read_bytes()),indexSHA256=sha(bytes(indices)),pivotRuntimeCalibrated=False))
            decoded=Image.new('RGBA',(w,h));decoded.putdata([(*normal[p],255) if p else (0,0,0,0) for p in indices])
            preview.alpha_composite(decoded,(phase*160+25,row*140+15))
        result['actors'][actor]=dict(frames=frames)
    (OUT/'TORSO_SOURCE.json').write_text(json.dumps(result,indent=2)+'\n')
    preview.save(OUT/'palette_preview.png')
    print(json.dumps(dict(frames=14,kanoBloodPensCostumeInvariant=True,runtimeVerified=False)))
if __name__=='__main__':main()
