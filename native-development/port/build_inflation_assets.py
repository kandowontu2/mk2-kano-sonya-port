"""Stage readable own inflation ASM/pixels, without changing the active link."""
import json
import sys
from pathlib import Path
from build_arm_rip_assets import read_pgm, sha

PORT = Path(__file__).resolve().parent
SOURCE = PORT/'assets/inflation'
OUT = PORT/'generated_inflation'


def pack6(pixels):
    result = bytearray((len(pixels)*6+7)//8)
    for index, value in enumerate(pixels):
        assert 0 <= value < 64
        at, shift = divmod(index*6, 8)
        result[at] |= value << shift & 255
        if shift > 2:
            result[at+1] |= value >> (8-shift)
    return bytes(result)


def unpack6(payload, count):
    # Separate bounded byte-window decoder, no enormous integer conversion.
    result = []
    for index in range(count):
        at, shift = divmod(index*6, 8)
        window = payload[at]
        if at+1 < len(payload):
            window |= payload[at+1] << 8
        result.append(window >> shift & 63)
    return result


def main(prefix_path=None,output=None,source_root=None):
    global SOURCE, OUT
    refresh = sys.argv[1:] == ['--native-facing-refresh']
    repair = sys.argv[1:] == ['--kano-boundary-repair'] or refresh
    assert not sys.argv[1:] or repair
    if repair:
        SOURCE = PORT/'assets/inflation_v3'
        OUT = PORT/'generated_inflation_v3'
    if source_root is not None:SOURCE=Path(source_root)
    if output is not None:OUT=Path(output)
    previous = None
    if refresh:
        previous = json.loads((OUT/'INFLATION_DATA.json').read_text())
        assert not previous.get('nativeFacingNormalized', False), 'Already normalized'
        assert sha((OUT/'KSINFART.ASM').read_bytes()) == previous['assemblySHA256']
        assert sha((OUT/'fighter_ui_finish_inflate_graphics.bin').read_bytes()) == previous['packedSHA256']
        for name, digest in previous['sockets'].items():
            assert sha((OUT/name).read_bytes()) == digest
    else:
        assert not OUT.exists(), 'Never overwrite staged/reviewed art'
    manifest_path = SOURCE/'INFLATION_SOURCES.json'
    manifest = json.loads(manifest_path.read_text())
    if refresh:
        assert sha(manifest_path.read_bytes()) == previous['sourceManifestSHA256']
    if repair:
        assert manifest['boundaryRepairOnly'] and manifest['unchangedOtherFrames'] == 10
        assert not any(f['touchesCellEdge'] for f in manifest['frames'])
    prefix_path = Path(prefix_path) if prefix_path is not None else PORT/'generated_arm_rip/fighter_ui_finish_arm_graphics.bin'
    prefix = prefix_path.read_bytes()
    if refresh:
        assert sha(prefix) == previous['prefixSHA256']
    packed = bytearray(prefix)
    lines = ['; Own inflation DATA: staged only, NOT runtime qualified.',
             '        .include mainequ.asm',
             '        .ref ks_kano_primary_palette,ks_sonya_primary_palette',
             '        .data']
    records = []
    for actor in ('kano', 'sonya'):
        frames = sorted((f for f in manifest['frames'] if f['actor'] == actor),
                        key=lambda f: f['phase'])
        assert [f['phase'] for f in frames] == list(range(6))
        for frame in frames:
            path = SOURCE/frame['file']
            assert sha(path.read_bytes()) == frame['SHA256']
            w, h, pixels = read_pgm(path)
            assert (w, h) == (frame['width'], frame['height'])
            # Authored sprites face left, native reaction expects right-facing
            # source art. Reflect both rows and animation-point X together.
            pixels = [v for y in range(h) for v in pixels[y*w:(y+1)*w][::-1]]
            frame = dict(frame, sourceXOffset=frame['xOffset'],
                         xOffset=w-1-frame['xOffset'])
            payload = pack6(pixels)
            assert unpack6(payload, w*h) == pixels
            offset = len(packed)
            packed.extend(payload)
            label = f'ks_inf_{actor}_img{frame["phase"]}'
            group = f'ks_inf_{actor}_pose{frame["phase"]}'
            lines += [f'        .def {label},{group}', label,
                      f'        .word {w},{h},{frame["xOffset"]},{frame["yOffset"]}',
                      f'        .long 0{(0xc00000+offset)*8:08x}h',
                      '        .word 06000h',
                      f'        .long ks_{actor}_primary_palette', group,
                      f'        .long {label},0']
            records.append(dict(**frame, imageLabel=label, poseLabel=group,
                packedByteOffset=offset, packedBytes=len(payload),
                packedSHA256=sha(payload), sixBitRoundTripVerified=True))
        # Native inflate_pose consumes first group, mframew consumes rest
        # through first zero, do_next_a9_frame then consumes pop group.
        label = f'ks_{actor}_inflated'
        lines += [f'        .def {label}', label]
        lines += [f'        .long ks_inf_{actor}_pose{phase}' for phase in range(5)]
        lines += ['        .long 0', f'        .long ks_inf_{actor}_pose5',
                  '        .long 0']
    assert len(records) == 12 and len(packed) < 0x600000
    assembly = ('\n'.join(lines)+'\n').encode('ascii')
    report = dict(format='MK2KS-INFLATION-TYPED-DATA-1', frames=records,
        sourceManifestSHA256=sha(manifest_path.read_bytes()),
        prefixSHA256=sha(prefix), prefixBytes=len(prefix),
        appendedBytes=len(packed)-len(prefix), packedSHA256=sha(packed),
        assemblySHA256=sha(assembly), prefixPreservedByteIdentical=True,
        sixBitRoundTripVerified=True, socketsEmitted=False,
        artBoundaryIssues=[dict(actor=f['actor'], phase=f['phase']) for f in records
                           if f['touchesCellEdge']],
        nativeLookupIntegration=False, runtimeVerified=False,
        pixelAcceptance=False, activeLinkChanged=False, releaseReady=False)
    report.update(nativeFacingNormalized=True,
                  nativeFacingMethod='row reflection and xOffset=width-1-sourceXOffset')
    if refresh:
        region = packed+bytes(0x600000-len(packed))
        rebuilt = bytearray(len(region))
        sockets = {}
        for bank, size in ((0, 0x100000), (1, 0x80000)):
            for lane in range(4):
                chip = 121-bank*4-lane
                name = f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
                start = bank*0x400000+lane
                data = region[start:start+size*4:4]
                (OUT/name).write_bytes(data)
                sockets[name] = sha(data)
                rebuilt[start:start+size*4:4] = data
        assert rebuilt == region
        report.update(sockets=sockets, socketsEmitted=True,
                      stockSocketRoundTripVerified=True,
                      previousPackedSHA256=previous['packedSHA256'])
    OUT.mkdir(exist_ok=refresh)
    (OUT/'KSINFART.ASM').write_bytes(assembly)
    (OUT/'fighter_ui_finish_inflate_graphics.bin').write_bytes(packed)
    (OUT/'INFLATION_DATA.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'frames'}, indent=2))


if __name__ == '__main__':
    main()
