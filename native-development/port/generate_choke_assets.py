"""Typed choke body phases and per-character grip trajectories from donor data."""
import hashlib
import json
import struct
import zipfile
import import_character_art as art

HERE=art.HERE
p=art.parser

def main():
    out=HERE/'generated_choke'
    assert not out.exists()
    out.mkdir()
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        lo=z.read('mk321u54.bin');hi=z.read('mk321u63.bin')
    data=bytearray(len(lo)*2);data[::2]=lo;data[1::2]=hi
    assert art.sha(data)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    donor={}
    refs=set()
    for name,root,block in [('kano',p.KANO_MAIN,p.KANO_BLOCK),('sonya',p.SONYA_MAIN,p.SONYA_BLOCK)]:
        at=p.stock_file(p.u32(data,p.stock_file(root)+56*4))
        assert p.u32(data,at+36)==0 and p.u32(data,at+88)==0
        rows=[]
        for relative in (0,12,24,40,52,64,76):
            token,xy,pose=struct.unpack_from('<III',data,at+relative)
            assert token==10 and p.frame_group(data,pose,*block)
            x,y=struct.unpack('<hh',struct.pack('<I',xy))
            label=f'ks_{name}_pose_{pose:08x}'
            assert f'.def {label}\n' in (HERE/'generated_packed'/f'{name.upper()}ART.ASM').read_text()
            refs.add(label);rows.append((x,y,label))
        donor[name]=rows
    phases={
        'ks_choke_intro':[0xff830420,0xff830480,0xff8304e0],
        'ks_choke_lift':[0xff8304e0,0xff830540,0xff8305a0],
        'ks_choke_cycle':[0xff830600,0xff830660,0xff8306c0,0xff830660],
        'ks_choke_end':[0xff8304e0,0xff830480,0xff830420],
    }
    refs|={f'ks_kano_pose_{a:08x}' for values in phases.values() for a in values}
    lines=['; Choke control/trajectory DATA, not executable opcode arrays.','        .data']
    lines+=['        .ref '+r for r in sorted(refs)]
    for name,poses in phases.items():
        lines += [f'        .def {name}',name]
        lines += [f'        .long ks_kano_pose_{a:08x}' for a in poses]+['        .long 0']
    lines+=['        .def ks_choke_victims','ks_choke_victims']
    for identity in range(19):
        lines.append('        .long 0' if identity in (12,13) else f'        .long ks_choke_victim_{identity}')
    grip=[(-9,50),(-7,44),(-11,48),(-14,47),(-12,47),(-12,47),
          (-19,48),(-7,43),(-9,41),(-9,41),(-9,41),(-6,44)]
    report={}
    for identity in range(19):
        if identity in (12,13):continue
        if identity>=17:
            rows=donor['kano' if identity==17 else 'sonya'];kind='own donor choke victim'
        else:
            # Zero pose is an explicit request for THIS original fighter's
            # native high-hit pose 2, resolved at runtime; never another actor.
            body=identity if identity<12 else (4 if identity==16 else 8)
            rows=[(x-8-grip[body][0],y+54-grip[body][1],'0') for x,y,_ in donor['sonya']]
            kind='own native high-hit pose 2'
        lines += [f'ks_choke_victim_{identity}']
        for x,y,pose in rows:lines += [f'        .word {x},{y}',f'        .long {pose}']
        report[identity]=dict(poseKind=kind,records=rows)
    source=('\n'.join(lines)+'\n').encode()
    (out/'KSCANI.ASM').write_bytes(source)
    (out/'CHOKE_ASSETS.json').write_text(json.dumps(dict(
        sourceSHA256=hashlib.sha256(source).hexdigest().upper(),
        phases={n:[hex(a) for a in g] for n,g in phases.items()},
        victims=report,bossesExcluded=[12,13],runtimeVerified=False),indent=2)+'\n')
    print(out)
if __name__=='__main__':main()
