"""Own palette-index-preserving native frozen tints, as readable ASM data."""
import hashlib
import json
from pathlib import Path
import re
from statue_palettes import build as build_statue_palettes

PORT=Path(__file__).resolve().parent
OUT=PORT/'generated_frozen'
assert not OUT.exists()
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
lines=['; Own native frozen/lightning palette DATA; pixel indices unchanged.','        .data']
records={}
for actor in ('kano','sonya'):
    source=PORT/f'generated_packed/{actor.upper()}ART.ASM'
    text=source.read_text().split(f'ks_{actor}_primary_palette\n',1)[1].split(f'ks_{actor}_alternate_palette\n',1)[0]
    words=[]
    for line in text.splitlines():
        if '.word' in line:
            for token in line.split('.word',1)[1].split(','):
                token=token.strip();words.append(int(token[:-1],16) if token.lower().endswith('h') else int(token))
    count=words[0];colors=words[1:]
    assert count==len(colors)==65 and colors[0]==0
    converted=[]
    for value in colors:
        if value==0:converted.append(0);continue
        red,green,blue=value>>10&31,value>>5&31,value&31
        luma=(red*3+green*6+blue)//10
        r=luma*20//31;g=luma*27//31;b=8+luma*23//31
        assert 0<=r<=g<=b<=31
        converted.append((r<<10)|(g<<5)|b)
    label=f'ks_{actor}_frozen_palette'
    lines += [f'        .def {label}',label,f'        .word {count}']
    for start in range(0,count,8):
        lines.append('        .word '+','.join(f'0{value:04x}h' for value in converted[start:start+8]))
    records[actor]=dict(sourceSHA256=sha(source.read_bytes()),colors=count,
        transparentIndexPreserved=True,pixelIndicesChanged=False,formula='RGB15 luma3:6:1 -> blue ramp20:27:23+8')
OUT.mkdir()
data=('\n'.join(lines)+'\n').encode('ascii')
statues,statue_records=build_statue_palettes()
data+=statues
(OUT/'KSICEPAL.ASM').write_bytes(data)
(OUT/'FROZEN_PALETTES.json').write_text(json.dumps(dict(actors=records,statuePalettes=statue_records,sourceSHA256=sha(data),
    runtimeVerified=False,visualTintAccepted=False,releaseReady=False),indent=2)+'\n')
print(json.dumps(dict(actors=list(records),colorsEach=65,visualTintAccepted=False),indent=2))
