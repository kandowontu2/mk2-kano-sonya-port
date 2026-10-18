"""Compile own ingestion PGM sources into typed ASM and stock Wolf sockets."""
import json
from pathlib import Path
from build_arm_rip_assets import read_pgm, sha
from build_inflation_assets import pack6, unpack6

PORT = Path(__file__).resolve().parent
SOURCE = PORT/'assets/ingestion'
OUT = PORT/'generated_ingestion'


def main(prefix_path=None,output=None,emit_sockets=True):
    global OUT
    if output is not None:OUT=Path(output)
    assert not OUT.exists(), 'Never overwrite reviewed/generated art'
    source_path = SOURCE/'INGESTION_SOURCES.json'
    manifest = json.loads(source_path.read_text())
    assert manifest['allCellsHaveTransparentMargins']
    prefix_path=Path(prefix_path) if prefix_path is not None else PORT/'generated_inflation_v3/fighter_ui_finish_inflate_graphics.bin'
    prefix = prefix_path.read_bytes()
    packed = bytearray(prefix)
    lines = ['; Own ingestion DATA, runtime acceptance tracked separately.',
             '        .include mainequ.asm',
             '        .ref ks_kano_primary_palette,ks_sonya_primary_palette',
             '        .data']
    frames = []
    for actor in ('kano','sonya'):
        selected = sorted((f for f in manifest['frames'] if f['actor']==actor), key=lambda f:f['phase'])
        assert [f['phase'] for f in selected] == list(range(8))
        for frame in selected:
            path = SOURCE/frame['file']
            assert sha(path.read_bytes()) == frame['SHA256']
            w,h,pixels = read_pgm(path)
            assert (w,h) == (frame['width'],frame['height'])
            payload = pack6(pixels)
            assert unpack6(payload,w*h) == pixels
            offset = len(packed)
            packed.extend(payload)
            label = f'ks_ing_{actor}_img{frame["phase"]}'
            group = f'ks_ing_{actor}_pose{frame["phase"]}'
            lines += [f'        .def {label},{group}',label,
                      f'        .word {w},{h},{frame["xOffset"]},{frame["yOffset"]}',
                      f'        .long 0{(0xc00000+offset)*8:08x}h',
                      '        .word 06000h',f'        .long ks_{actor}_primary_palette',
                      group,f'        .long {label},0']
            frames.append(dict(**frame,imageLabel=label,poseLabel=group,
                packedByteOffset=offset,packedBytes=len(payload),packedSHA256=sha(payload),
                sixBitRoundTripVerified=True))
        label = f'ks_{actor}_ingested'
        lines += [f'        .def {label}',label]
        lines += [f'        .long ks_ing_{actor}_pose{i}' for i in range(8)]
        lines += ['        .long 0']
    assert len(frames)==16 and len(packed)<0x600000
    assembly = ('\n'.join(lines)+'\n').encode('ascii')
    region = packed+bytes(0x600000-len(packed))
    rebuilt = bytearray(len(region))
    sockets = {}
    socket_data = {}
    for bank,size in ((0,0x100000),(1,0x80000)):
        for lane in range(4):
            chip = 121-bank*4-lane
            name = f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
            start = bank*0x400000+lane
            data = region[start:start+size*4:4]
            assert len(data)==size
            sockets[name] = sha(data)
            socket_data[name] = data
            rebuilt[start:start+size*4:4] = data
    assert rebuilt==region and packed.startswith(prefix)
    report = dict(format='MK2KS-INGESTION-TYPED-DATA-1',frames=frames,
        sourceManifestSHA256=sha(source_path.read_bytes()),prefixSHA256=sha(prefix),
        prefixBytes=len(prefix),appendedBytes=len(packed)-len(prefix),
        packedSHA256=sha(packed),assemblySHA256=sha(assembly),sockets=sockets,
        socketsEmitted=emit_sockets,stockSocketRoundTripVerified=True,prefixPreservedByteIdentical=True,
        sixBitRoundTripVerified=True,runtimeVerified=False,visualAcceptance=False,releaseReady=False)
    OUT.mkdir()
    (OUT/'KSINART.ASM').write_bytes(assembly)
    (OUT/'fighter_ui_finish_ingest_graphics.bin').write_bytes(packed)
    if emit_sockets:
        for name,data in socket_data.items():(OUT/name).write_bytes(data)
    (OUT/'INGESTION_DATA.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(frames=len(frames),appendedBytes=report['appendedBytes'],
                         sockets=len(sockets),runtimeVerified=False)))


if __name__=='__main__':main()
