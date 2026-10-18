"""One-time lossless export of authored palette indices into readable sources."""
import json
from pathlib import Path
import hashlib

HERE=Path(__file__).resolve().parent

def sha(raw):return hashlib.sha256(raw).hexdigest().upper()

def main():
    generated=HERE/'generated_pit'
    data=json.loads((generated/'PIT_DATA.json').read_text())
    packed=(generated/'fighter_ui_finish_pit_graphics.bin').read_bytes()
    target=HERE/'assets/pit'
    assert not target.exists(),'Never overwrite authored asset sources'
    target.mkdir(parents=True)
    manifest=dict(format='MK2KS-PIT-PALETTE-INDEX-PGM-1',transparentIndex=0,maxIndex=63,
                  sourceKind=data['sourceKind'],historicalAssetPayloadSHA256=data['sourcePayloadSHA256'],actors={})
    for name,record in data['records'].items():
        frames=[]
        for frame in record['frames']:
            w,h,start=frame['width'],frame['height'],frame['packedByteOffset']
            raw=packed[start:start+(w*h*6+7)//8]
            assert sha(raw)==frame['compressedSHA256']
            indices=bytes((int.from_bytes(raw[(i*6)//8:(i*6)//8+2],'little')>>((i*6)&7))&63 for i in range(w*h))
            filename=f'{name}_{frame["phase"]}.pgm'
            text='P2\n# Authored Pit sprite: palette indices, NOT luminance; zero is transparent.\n'
            text+=f'{w} {h}\n63\n'
            text+='\n'.join(' '.join(str(v) for v in indices[y*w:(y+1)*w]) for y in range(h))+'\n'
            encoded=text.encode('ascii');(target/filename).write_bytes(encoded)
            frames.append(dict(phase=frame['phase'],width=w,height=h,xOffset=frame['xOffset'],yOffset=frame['yOffset'],
                               file=filename,fileSHA256=sha(encoded),indexSHA256=sha(indices),packedSHA256=sha(raw)))
        manifest['actors'][name]=dict(actorID=record['actorID'],coordinate=record['coordinate'],frames=frames)
    (target/'PIT_SOURCE.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(actors=2,sourceImages=12,sourceDirectory=str(target),losslessPaletteIndices=True)))

if __name__=='__main__':main()
