"""Native leg-grab phases and explicit per-victim own-art/waist trajectories."""
import hashlib
import json
import re
import struct
import zipfile
from collections import defaultdict
from pathlib import Path
import import_character_art as art
from inventory_character_tables import source_tables

HERE=art.HERE
p=art.parser

def main():
    out=HERE/'generated_leg'
    assert not out.exists()
    out.mkdir()
    files={}
    with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as z:
        for name in z.namelist():
            if name.startswith('mk2-rebuild-main/src/') and name.count('/')==2 and name.upper().endswith(('.ASM','.TBL')):
                files[Path(name).name.upper()]=z.read(name).decode('cp437').replace('\r\n','\n')
    tables={};aliases={}
    for file,text in files.items():
        if not file.endswith('.ASM'):continue
        labels=re.findall(r'^([A-Za-z_]\w*):?',text,re.M)
        local=source_tables(text)
        for a,b in zip(labels,labels[1:]):
            if a not in local:aliases[(file,a.casefold())]=b
        for label,table in local.items():tables[(file,label.casefold())]=(label,table)
    def table(file,label):
        seen=set()
        while (file,label.casefold()) not in tables:
            assert label not in seen,(file,label)
            seen.add(label);label=aliases[(file,label.casefold())]
        return tables[(file,label.casefold())]
    def longs(file,label):
        return [v for r in table(file,label)[1]['rows'] if r['type']=='long' for v in r['values']]
    frame_labels={n.casefold() for file,text in files.items() if file.endswith('.TBL') for n in re.findall(r'^([A-Za-z_]\w*):',text,re.M)}
    def group(file,label):
        key=(file,label.casefold())
        if key not in tables:return False
        return any(v.casefold() in frame_labels for r in tables[key][1]['rows'] for v in r['values'])
    roots=longs('MKGUYS.ASM','character_anitabs1')[:17]
    exports=defaultdict(set);victims={}
    grip=[[(86,-4),(67,-53),(14,-50),(-48,5),(-94,33)],
          [(84,1),(64,-42),(1,-49),(-48,-23),(-92,12)],
          [(85,-8),(59,-33),(4,-50),(-53,-18),(-98,1)],
          [(86,-10),(59,-23),(10,-61),(-68,-26),(-106,16)],
          [(87,-3),(68,-41),(19,-62),(-56,-21),(-96,31)],
          [(87,-3),(68,-41),(19,-62),(-56,-21),(-96,31)],
          [(90,0),(68,-48),(10,-65),(-55,-50),(-99,13)],
          [(91,-8),(66,-50),(2,-77),(-57,-32),(-107,30)],
          [(83,-13),(62,-43),(8,-62),(-64,-41),(-107,16)],
          [(83,-13),(62,-43),(8,-62),(-64,-41),(-107,16)],
          [(83,-13),(62,-43),(8,-62),(-64,-41),(-107,16)],
          [(86,-12),(63,-52),(4,-85),(-52,-35),(-96,25)]]
    for identity,root in enumerate(roots):
        if identity in (12,13):continue
        owners=[f for f in files if f.endswith('.ASM') and ((f,root.casefold()) in tables or (f,root.casefold()) in aliases)]
        assert len(owners)==1,(identity,root,owners)
        file=owners[0];entries=longs(file,root)
        first=[v for v in longs(file,entries[15]) if group(file,v)][0]
        flip=[];phases=0
        for value in longs(file,entries[43]):
            if value=='0':
                phases+=1
                if phases==2:break
            elif group(file,value) and value not in flip:flip.append(value)
        body=identity if identity<12 else (4 if identity==16 else 8)
        extra=body in (4,5,6)
        assert len(flip)>=(5 if extra else 4),(identity,flip)
        poses=[first,flip[0],flip[2 if extra else 1],flip[3 if extra else 2],flip[-1]]
        rows=[]
        for (x,y),pose in zip(grip[body],poses):
            pose=table(file,pose)[0]
            exports[file].add(pose);rows.append((-x,y,pose))
        victims[identity]=dict(kind='own native hurt/throw composites',records=rows)
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        lo=z.read('mk321u54.bin');hi=z.read('mk321u63.bin')
    data=bytearray(len(lo)*2);data[::2]=lo;data[1::2]=hi
    assert art.sha(data)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    refs={pose for v in victims.values() for _,_,pose in v['records']}
    for identity,name,root,block in [(17,'kano',p.KANO_MAIN,p.KANO_BLOCK),(18,'sonya',p.SONYA_MAIN,p.SONYA_BLOCK)]:
        at=p.stock_file(p.u32(data,p.stock_file(root)+54*4))
        rows=[]
        for i in range(5):
            token,xy,pose=struct.unpack_from('<III',data,at+i*12)
            assert token==10 and p.frame_group(data,pose,*block)
            x,y=struct.unpack('<hh',struct.pack('<I',xy))
            label=f'ks_{name}_pose_{pose:08x}'
            assert f'.def {label}\n' in (HERE/'generated_packed'/f'{name.upper()}ART.ASM').read_text()
            refs.add(label);rows.append((x,y,label))
        assert p.u32(data,at+60)==0
        victims[identity]=dict(kind='own donor leg victim',records=rows)
    body=[0xff83bbe0,0xff83bc60,0xff83bce0,0xff83bd40,0xff83bda0,0xff83be00,0xff83be60]
    refs|={f'ks_sonya_pose_{a:08x}' for a in body}
    lines=['; Native leg-grab DATA: own body phases, victim XY and composite symbols.',
           '        .include mainequ.asm','        .data']
    lines+=['        .ref '+r for r in sorted(refs)]
    lines+=['        .def ks_leg_intro,ks_leg_pair,ks_leg_end,ks_leg_victims','ks_leg_intro']
    for i,a in enumerate(body):
        if i<2:lines+=['        .long ani_adjustx','        .word 12']
        if i==2:lines+=['        .long ani_adjustxy','        .word 12,0']
        lines += [f'        .long ks_sonya_pose_{a:08x}']
    lines+=['        .long 0','ks_leg_pair']
    lines += [f'        .long ks_sonya_pose_{a:08x}' for a in reversed(body[2:])]
    lines+=['        .long 0','ks_leg_end',f'        .long ks_sonya_pose_{body[1]:08x},ks_sonya_pose_{body[0]:08x},0','ks_leg_victims']
    for identity in range(19):lines += ['        .long '+(f'ks_leg_victim_{identity}' if identity in victims else '0')]
    for identity,entry in sorted(victims.items()):
        lines += [f'ks_leg_victim_{identity}']
        for x,y,pose in entry['records']:lines += [f'        .word {x},{y}',f'        .long {pose}']
    source=('\n'.join(lines)+'\n').encode()
    (out/'KSLANI.ASM').write_bytes(source)
    exports={f:sorted(labels) for f,labels in sorted(exports.items())}
    (out/'SOURCE_EXPORTS.json').write_text(json.dumps(exports,indent=2)+'\n')
    (out/'LEG_ASSETS.json').write_text(json.dumps(dict(sourceSHA256=hashlib.sha256(source).hexdigest().upper(),
        body=[hex(a) for a in body],victims=victims,bossesExcluded=[12,13],sourceExports=exports,runtimeVerified=False),indent=2)+'\n')
    print(json.dumps(exports,indent=2))
if __name__=='__main__':main()
