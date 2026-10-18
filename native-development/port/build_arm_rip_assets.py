"""Encode own indexed arm-rip assets as staged typed ASM and packed pixels."""
import hashlib
import json
from pathlib import Path
import sys
from arm_rip_origins import origin

PORT=Path(__file__).resolve().parent;SOURCE=PORT/'assets/arm_rip';OUT=PORT/'generated_arm_rip'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()

def read_pgm(path):
    tokens=' '.join(line.split('#',1)[0] for line in path.read_text().splitlines()).split()
    assert tokens[0]=='P2'
    w,h,maximum=map(int,tokens[1:4]);pixels=list(map(int,tokens[4:]))
    assert maximum==63 and len(pixels)==w*h and all(0<=value<=63 for value in pixels)
    return w,h,pixels

def main(prefix_path=None,output=None):
    global OUT
    if output is not None:OUT=Path(output)
    grip_refresh=sys.argv[1:]==['--refresh-grip-pixels']
    refresh=sys.argv[1:]==['--refresh-header-origins'] or grip_refresh
    assert not sys.argv[1:] or refresh
    previous=None
    if OUT.exists():
        assert refresh,'Never overwrite staged art under review'
        previous=json.loads((OUT/'ARM_RIP_DATA.json').read_text())
        assert sha((OUT/'KSARART.ASM').read_bytes())==previous['assemblySHA256']
        assert sha((OUT/'fighter_ui_finish_arm_graphics.bin').read_bytes())==previous['packedSHA256']
    source_manifest=SOURCE/'ARM_RIP_SOURCES.json'
    manifest=json.loads(source_manifest.read_text())
    if previous is not None:
        if grip_refresh:
            assert manifest['gripRevision']['priorManifestSHA256']==previous['sourceManifestSHA256']
            for frame in manifest['frames']:
                old=next(item for item in previous['frames'] if all(item[k]==frame[k] for k in ('actor','role','phase')))
                if frame['role']=='body' and frame['phase']==0:assert frame['priorFrame']['SHA256']==old['SHA256']
                else:assert frame['SHA256']==old['SHA256']
        else:assert sha(source_manifest.read_bytes())==previous['sourceManifestSHA256']
    prefix_path=Path(prefix_path) if prefix_path is not None else PORT/'generated_impale/fighter_ui_finish_impale_graphics.bin'
    prefix=prefix_path.read_bytes();packed=bytearray(prefix)
    lines=['; Own arm-rip victim and detached-arm DATA. Staged, not active gameplay.',
        '        .include mainequ.asm','        .ref ks_kano_primary_palette,ks_sonya_primary_palette','        .data']
    records=[]
    for frame in manifest['frames']:
        path=SOURCE/frame['file'];assert sha(path.read_bytes())==frame['SHA256']
        w,h,pixels=read_pgm(path);assert (w,h)==(frame['width'],frame['height'])
        if frame['role']=='arm':
            xo,yo=origin(frame['actor'],frame['phase'],w,h)
            frame=dict(frame,seedXOffset=frame['xOffset'],seedYOffset=frame['yOffset'],xOffset=xo,yOffset=yo)
        assert 0<w<=160 and 0<h<=160
        payload=bytearray((len(pixels)*6+7)//8)
        for index,value in enumerate(pixels):
            at,shift=divmod(index*6,8);payload[at]|=value<<shift&255
            if shift>2:payload[at+1]|=value>>(8-shift)
        # Independent scalar decoder verifies every original palette index.
        scalar=int.from_bytes(payload,'little')
        assert bytes((scalar>>(index*6))&63 for index in range(w*h))==bytes(pixels)
        actor,role,phase=frame['actor'],frame['role'],frame['phase']
        label=f'ks_ar_{actor}_{role}_frame{phase}';pose=f'ks_ar_{actor}_body_pose{phase}'
        offset=len(packed);packed.extend(payload)
        lines.extend((f'        .def {label}',label,
            f"        .word {w},{h},{frame['xOffset']},{frame['yOffset']}",
            f'        .long 0{(0xc00000+offset)*8:08x}h','        .word 06000h',
            f'        .long ks_{actor}_primary_palette'))
        if role=='body':lines.extend((f'        .def {pose}',pose,f'        .long {label},0'))
        records.append(dict(**frame,imageLabel=label,poseLabel=pose if role=='body' else None,
            packedByteOffset=offset,packedBytes=len(payload),packedSHA256=sha(payload),
            indexSHA256=sha(bytes(pixels)),independentSixBitRoundTripVerified=True))
    for actor in ('kano','sonya'):
        lines.extend((f'        .def ks_{actor}_arms_ripped',f'ks_{actor}_arms_ripped'))
        lines.extend(f'        .long ks_ar_{actor}_body_pose{phase}' for phase in range(5))
        lines.append('        .long 0')
        lines.extend((f'        .def ks_{actor}_arm_fly',f'ks_{actor}_arm_fly'))
        lines.extend(f'        .long ks_ar_{actor}_arm_frame{phase}' for phase in range(5))
        lines.append('        .long 0')
    assert len(records)==20 and packed[:len(prefix)]==prefix and len(packed)<0x600000
    if previous is not None and not grip_refresh:assert sha(packed)==previous['packedSHA256'],'Origin-only refresh changed pixels'
    data=('\n'.join(lines)+'\n').encode('ascii');OUT.mkdir(exist_ok=refresh)
    (OUT/'KSARART.ASM').write_bytes(data)
    (OUT/'fighter_ui_finish_arm_graphics.bin').write_bytes(packed)
    report=dict(format='MK2KS-ARM-RIP-TYPED-DATA-1',frames=records,
        sourceManifestSHA256=sha(source_manifest.read_bytes()),prefixSHA256=sha(prefix),prefixBytes=len(prefix),
        appendedBytes=len(packed)-len(prefix),packedSHA256=sha(packed),assemblySHA256=sha(data),
        bodyFormat='multipart group pointers',detachedArmFormat='single image descriptor pointers',
        independentSixBitRoundTripVerified=True,prefixPreservedByteIdentical=True,
        socketsEmitted=False,currentGraphicsChanged=grip_refresh,activeNativeLinkChanged=False,
        runtimeVerified=False,fullVisualAcceptance=False,releaseReady=False,fullPortVerified=False)
    if previous is not None and previous['socketsEmitted']:
        for name,digest in previous['sockets'].items():assert sha((OUT/name).read_bytes())==digest
        sockets=previous['sockets']
        if grip_refresh:
            region=packed+bytes(0x600000-len(packed));rebuilt=bytearray(len(region));sockets={}
            for bank,size in ((0,0x100000),(1,0x80000)):
                for lane in range(4):
                    name=f'l1_mortal_kombat_3_u{121-bank*4-lane}_game_rom.u{121-bank*4-lane}'
                    start=bank*0x400000+lane;data=region[start:start+size*4:4]
                    (OUT/name).write_bytes(data);sockets[name]=sha(data)
                    rebuilt[start:start+size*4:4]=data
            assert rebuilt==region
        report.update(socketsEmitted=True,sockets=sockets,stockSocketRoundTripVerified=True)
    report.update(originMethod='Native phase center/bottom trajectory adapted to own component dimensions',
        headerOnlyRefresh=refresh and not grip_refresh,graphicsPixelsUnchangedByOriginRefresh=refresh and not grip_refresh,
        gripPixelRefresh=grip_refresh)
    (OUT/'ARM_RIP_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='frames'},indent=2))

if __name__=='__main__':main()
