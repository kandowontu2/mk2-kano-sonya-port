"""Named Kano extraction phases and actual per-character native victim art."""
import json
import re
import struct
import sys
import zipfile
from collections import defaultdict
import import_character_art as art
from inventory_character_tables import source_tables

HERE=art.HERE

def main():
    output=HERE/'generated_extract'
    assert not output.exists() or '--refresh' in sys.argv
    with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as z:
        files={n.rsplit('/',1)[-1].upper():z.read(n).decode('cp437').replace('\r\n','\n')
               for n in z.namelist() if n.startswith('mk2-rebuild-main/src/') and n.count('/')==2 and n.upper().endswith(('.ASM','.TBL'))}
    tables={};aliases={}
    for file,text in files.items():
        if not file.endswith('.ASM'):continue
        local=source_tables(text)
        labels=re.findall(r'^([A-Za-z_]\w*):?',text,re.M)
        for a,b in zip(labels,labels[1:]):
            if a not in local:aliases[file,a.casefold()]=b
        for label,table in local.items():tables[file,label.casefold()]=(label,table)
    def table(file,label):
        seen=set()
        while (file,label.casefold()) not in tables:
            assert label not in seen,(file,label)
            seen.add(label);label=aliases[file,label.casefold()]
        return tables[file,label.casefold()]
    def longs(file,label):
        return [v for r in table(file,label)[1]['rows'] if r['type']=='long' for v in r['values']]
    frame_labels={n.casefold() for f,t in files.items() if f.endswith('.TBL') for n in re.findall(r'^([A-Za-z_]\w*):',t,re.M)}
    def group(file,label):
        return (file,label.casefold()) in tables and any(v.casefold() in frame_labels for v in longs(file,label))
    roots=longs('MKGUYS.ASM','character_anitabs1')[:17]
    victims={};exports=defaultdict(dict)
    for identity,root in enumerate(roots):
        if identity in (12,13):continue
        owners=[f for f in files if f.endswith('.ASM') and ((f,root.casefold()) in tables or (f,root.casefold()) in aliases)]
        assert len(owners)==1,(identity,root)
        file=owners[0];entries=longs(file,root)
        windup=[v for v in longs(file,entries[0x37]) if group(file,v)]
        fall=[]
        for value in longs(file,entries[0x3c]):
            if group(file,value) and value not in fall:fall.append(value)
        assert len(windup)>=2 and len(fall)>=7,(identity,windup,fall)
        chosen=[windup[1]]+[fall[i] for i in (0,1,3,5,6)]
        chosen=[table(file,v)[0] for v in chosen]
        named=[]
        for pose in chosen:
            # Original modules have local names reused by other actors (notably
            # Shang's NJDECAP names). Export unique aliases, not those locals.
            alias=f'ks_ex_{file[2:-4].lower()}_{pose.lower()}'
            exports[file][pose]=alias;named.append(alias)
        victims[identity]=named
    for identity,groups in [(17,[0xff9b29b0,0xff9b2a30,0xff9b2ab0,0xff9b2b30,0xff9b2b70,0xff9b2bb0]),
                            (18,[0xff9b2d10,0xff9b2db0,0xff9b2e50,0xff9b2ef0,0xff9b2f70,0xff9b2fb0])]:
        victims[identity]=[f'ks_finish_pose_{g:08x}' for g in groups]
    body=[0xff9b24f0,0xff9b2550,0xff9b25b0,0xff9b2610,0xff9b2670,
          0xff9b26d0,0xff9b2730,0xff9b2790,0xff9b2810]
    skeleton=[0xff9b22d0,0xff9b2310,0xff9b2350,0xff9b23d0,0xff9b2430,0xff9b2490]
    refs={p for v in victims.values() for p in v}|{f'ks_finish_pose_{g:08x}' for g in body+skeleton}
    lines=['; Typed extraction phases; real victim art, not a proxy identity.',
           '        .data']+['        .ref '+r for r in sorted(refs)]
    lines+=['        .def ks_extract_intro,ks_extract_body,ks_extract_skeleton,ks_extract_victims',
            'ks_extract_intro']
    lines += [f'        .long ks_finish_pose_{g:08x}' for g in body[:4]]+['        .long 0','ks_extract_body']
    lines += [f'        .long ks_finish_pose_{g:08x}' for g in body]+['ks_extract_skeleton']
    lines += [f'        .long ks_finish_pose_{g:08x}' for g in skeleton]+['        .long 0','ks_extract_victims']
    for identity in range(19):lines.append('        .long '+(f'ks_extract_victim_{identity}' if identity in victims else '0'))
    for identity,poses in sorted(victims.items()):
        lines += [f'ks_extract_victim_{identity}']+['        .long '+pose for pose in poses]
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        d=bytearray(1048576);d[::2]=z.read('mk321u54.bin');d[1::2]=z.read('mk321u63.bin')
    assert art.sha(d)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    at=art.parser.stock_file(0xffc95de0);assert art.parser.u32(d,at)==64
    colors=struct.unpack_from('<64H',d,at+4)
    lines+=['        .def ks_extract_kano_victim_palette','ks_extract_kano_victim_palette','        .word 65,0']
    for i in range(0,64,8):lines.append('        .word '+','.join(art.word(c) for c in colors[i:i+8]))
    output.mkdir(exist_ok=True);source=('\n'.join(lines)+'\n').encode()
    (output/'KSEXANI.ASM').write_bytes(source)
    exports={f:dict(sorted(labels.items())) for f,labels in sorted(exports.items())}
    (output/'SOURCE_EXPORTS.json').write_text(json.dumps(exports,indent=2)+'\n')
    (output/'EXTRACT_DATA.json').write_text(json.dumps(dict(sourceSHA256=art.sha(source),
        victims=victims,excludedVictims=[12,13],body=[hex(g) for g in body],skeleton=[hex(g) for g in skeleton],
        sourceExports=exports,runtimeVerified=False),indent=2)+'\n')
    print(json.dumps(dict(victims=len(victims),exports=exports),indent=2))

if __name__=='__main__':main()
