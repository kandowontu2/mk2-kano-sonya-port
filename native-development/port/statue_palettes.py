"""Readable own-index cyan-white statue palettes; ordinary ice tint unchanged."""
import hashlib
import json
from pathlib import Path
import sys

PORT=Path(__file__).resolve().parent
sha=lambda data:hashlib.sha256(data).hexdigest().upper()

def build():
    lines=['; Deep-freeze statue palettes: opaque blacks become cyan, index0 stays transparent.']
    records={}
    for actor in ('kano','sonya'):
        path=PORT/f'generated_packed/{actor.upper()}ART.ASM'
        text=path.read_text().split(f'ks_{actor}_primary_palette\n',1)[1].split(f'ks_{actor}_alternate_palette\n',1)[0]
        words=[]
        for line in text.splitlines():
            if '.word' not in line:continue
            for token in line.split('.word',1)[1].split(','):
                token=token.strip();words.append(int(token[:-1],16) if token.lower().endswith('h') else int(token))
        assert words[0]==65 and len(words)==66 and words[1]==0
        colors=[0]
        for color in words[2:]:
            r,g,b=color>>10&31,color>>5&31,color&31
            luma=(3*r+6*g+b)//10
            colors.append(((8+23*luma//31)<<10)|((24+7*luma//31)<<5)|31)
        label=f'ks_{actor}_statue_palette'
        lines.extend((f'        .def {label}',label,'        .word 65'))
        for index in range(0,65,8):lines.append('        .word '+','.join(f'0{color:04x}h' for color in colors[index:index+8]))
        records[actor]=dict(sourceSHA256=sha(path.read_bytes()),colors=65,indexZeroTransparent=True,
            opaqueBlackBecomesCyan=True,formula='RGB15 luma3:6:1 -> (8+23L/31,24+7L/31,31)',
            pixelIndicesChanged=False)
    return ('\n'.join(lines)+'\n').encode('ascii'),records

if __name__=='__main__':
    assert sys.argv[1:]==['--extend-current-generated']
    path=PORT/'generated_frozen/KSICEPAL.ASM'
    manifest=PORT/'generated_frozen/FROZEN_PALETTES.json'
    record=json.loads(manifest.read_text());old=path.read_bytes()
    assert sha(old)==record['sourceSHA256'] and b'_statue_palette' not in old
    block,actors=build();data=old+block
    path.write_bytes(data)
    record.update(sourceSHA256=sha(data),statuePalettes=actors,visualTintAccepted=False,runtimeVerified=False)
    manifest.write_text(json.dumps(record,indent=2)+'\n')
    # Native source module is generated data, not manually authored ASM.
    target=PORT.parent/'baseline/mk2-rebuild-main/srcp/KSICEPAL.ASM'
    assert target.read_bytes()==old
    target.write_bytes(data)
    print(json.dumps(dict(bytesAdded=len(block),statuePalettes=list(actors),visualAcceptance=False)))
