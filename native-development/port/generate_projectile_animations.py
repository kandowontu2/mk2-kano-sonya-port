"""Typed native scripts/palettes from supplied donor assets, no executable blobs."""
import hashlib
import json
import struct
import zipfile
import import_character_art as art

HERE=art.HERE
p=art.parser

def main():
    out=HERE/'generated_projectiles'
    assert not out.exists()
    out.mkdir()
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        lo=z.read('mk321u54.bin');hi=z.read('mk321u63.bin')
    data=bytearray(len(lo)*2);data[::2]=lo;data[1::2]=hi
    assert art.sha(data)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    scripts={
        'ks_knife_release':('kano',[0xff82f400+i*0x60 for i in range(8)],False),
        'ks_knife_intro':('kano',[0xff82ec40,0xff82eca0,0xff82ece0,0xff82ed40,0xff82edc0,0xff82ee20],False),
        'ks_knife_flight':('kano',list(range(0xff82ee80,0xff82f100,0x40)),True),
        'ks_knife_impact':('kano',[0xff82f100,0xff82f140,0xff82f180,0xff82f1c0,0xff82f200,0xff82f260],False),
        'ks_ring_charge':('sonya',[0xff83dbe0,0xff83dc40,0xff83dca0,0xff83dd00],False),
        'ks_ring_release':('sonya',[0xff83dec0],False),
        'ks_ring_flight':('sonya',list(range(0xff83e100,0xff83e200,0x40)),True),
        'ks_ring_impact':('sonya',[0xff83e200,0xff83e240,0xff83e280,0xff83e340,0xff83e440,0xff83e520,0xff83e5c0],False),
    }
    palettes={'ks_knife_palette':(0xffc96600,24),'ks_ring_charge_palette':(0xffc96fb0,64),'ks_ring_palette':(0xffc973c0,5)}
    refs=set()
    lines=['; Own projectile control data. Original compressed pixels remain in graphics ROM.',
           '        .include mainequ.asm','        .data']
    for name,(fighter,groups,loop) in scripts.items():
        text=(HERE/'generated_packed'/f'{fighter.upper()}ART.ASM').read_text()
        lines += [f'        .def {name}',name]
        for address in groups:
            label=f'ks_{fighter}_pose_{address:08x}'
            assert f'.def {label}\n' in text,label
            refs.add(label);lines.append('        .long '+label)
        lines.append(f'        .long ani_jump,{name}' if loop else '        .long 0')
    for name,(address,count) in palettes.items():
        at=p.stock_file(address)
        assert p.u16(data,at)==count
        colors=list(struct.unpack_from(f'<{count}H',data,at+2))
        colors[0]=0
        colors += [0]*(64-count)
        lines += [f'        .def {name}',name,'        .word 64']
        for i in range(0,64,8):lines.append('        .word '+','.join(art.word(c) for c in colors[i:i+8]))
    lines[2:2]=['        .ref '+label for label in sorted(refs)]
    source=('\n'.join(lines)+'\n').encode()
    (out/'KSPJANI.ASM').write_bytes(source)
    report=dict(sourceSHA256=hashlib.sha256(source).hexdigest().upper(),
                scripts={n:dict(actor=f,groups=[hex(a) for a in g],loop=l) for n,(f,g,l) in scripts.items()},
                palettes={n:dict(source=hex(a),colors=c,transparentPenZero=True) for n,(a,c) in palettes.items()},
                runtimeVerified=False)
    (out/'PROJECTILE_ANIMATIONS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(out)
if __name__=='__main__':main()
