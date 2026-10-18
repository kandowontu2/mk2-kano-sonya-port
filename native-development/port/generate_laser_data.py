"""Translate the original Eye Laser's slave controls into named native DATA."""
import json
import struct
import zipfile
import import_character_art as art

HERE=art.HERE

def main():
    out=HERE/'generated_laser'
    assert not out.exists()
    with zipfile.ZipFile(art.ROOT/'mk3.zip') as z:
        data=bytearray(1048576);data[::2]=z.read('mk321u54.bin');data[1::2]=z.read('mk321u63.bin')
    assert art.sha(data)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651'
    p=art.parser
    start=p.u32(data,p.stock_file(p.KANO_SPECIAL)+3*4)
    assert start==0xff830f00
    cursor=p.stock_file(start)
    phases=[[]];pending_beam=0;create=False;first_beam=None
    refs=set()
    def take():
        nonlocal cursor
        v=p.u32(data,cursor);cursor+=4;return v
    def label(value):
        name=f'ks_kano_pose_{value:08x}'
        assert '.def '+name+'\n' in imported
        refs.add(name);return name
    imported=(HERE/'generated_packed/KANOART.ASM').read_text()
    while len(phases)<=3:
        token=take()
        if token==0:
            if len(phases)==3:break
            phases.append([]);continue
        if token==11:
            assert first_beam is None
            first_beam=label(take());create=True;continue
        if token in (12,14):
            pending_beam=label(take())
            if token==12:continue  # Slave changes, then the owner's next pose.
            body=0
        else:
            assert token>=0xff800000,hex(token)
            body=label(token)
        phases[-1].append(dict(body=body,beam=pending_beam,create=create))
        pending_beam=0;create=False
    assert cursor==p.stock_file(0xff831520)
    assert [len(phase) for phase in phases]==[12,4,8]
    assert first_beam=='ks_kano_pose_ff831640'
    palette=0xffccc340;at=p.stock_file(palette)
    assert p.u16(data,at)==16
    colors=list(struct.unpack_from('<16H',data,at+2));colors[0]=0
    victims=json.loads((HERE/'generated_extract/EXTRACT_DATA.json').read_text())['victims']
    victims={int(i):v[0] for i,v in victims.items()}
    victims[17]='ks_kano_pose_ff831b40'
    victims[18]='ks_sonya_pose_ff83ed00'
    assert p.u32(data,p.stock_file(p.KANO_MAIN)+64*4)==0xff831b00
    assert p.u32(data,p.stock_file(p.SONYA_MAIN)+64*4)==0xff83ecc0
    assert p.u32(data,p.stock_file(0xff831b00))==0xff831b40
    assert p.u32(data,p.stock_file(0xff83ecc0))==0xff83ed00
    assert '.def '+victims[18]+'\n' in (HERE/'generated_packed/SONYAART.ASM').read_text()
    refs.update(victims.values())
    lines=['; Native Eye Laser event DATA: body, attached beam, delay and create flag.',
           '        .data']+['        .ref '+name for name in sorted(refs)]
    for number,(phase,delay) in enumerate(zip(phases,[4,6,4])):
        name=f'ks_laser_phase{number}'
        lines+=['        .def '+name,name]
        for event in phase:
            lines+=['        .long '+str(event['body'])+','+str(event['beam']),
                    f'        .word {delay},{int(event["create"])}']
        lines+=['        .long 0,0','        .word 0,0']
    lines+=['        .def ks_laser_beam_start,ks_laser_palette,ks_laser_victims',
            'ks_laser_beam_start','        .long '+first_beam+',0','ks_laser_palette','        .word 16']
    for i in range(0,16,8):lines.append('        .word '+','.join(art.word(c) for c in colors[i:i+8]))
    lines+=['ks_laser_victims']
    lines+=['        .long '+victims.get(i,'0') for i in range(19)]
    source=('\n'.join(lines)+'\n').encode()
    out.mkdir();(out/'KSLAANI.ASM').write_bytes(source)
    report=dict(sourceSHA256=art.sha(source),inputProgramSHA256=art.sha(data),
                sourceSpecialIndex=3,phases=phases,phaseFields=[48,24,32],sustainRepeats=4,totalFields=176,
                firstBeam=first_beam,paletteSource=hex(palette),paletteColors=16,victims=victims,
                originalVictimArt='own native MKII wound reaction; added actors use own original laser victim art',
                additionalGraphicsBytes=0,runtimeVerified=False)
    (out/'LASER_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('phases','victims')},indent=2))

if __name__=='__main__':main()
