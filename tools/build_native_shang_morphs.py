"""Original Kano/Sonya morph art in MKII's native Shang animation grammar.

Asset-only preparation: native selection, transformation, combat and restore
must still be proved in a matching executable. Never modify the source payload.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path

import build_mk2ks_mk3 as animation
import build_native_projectile_impacts as pixels
import upgrade_ksui_previews as decoder

BASE=animation.DONOR_TMS_BASE
HEADER,META_END=0x118000,0x119000
PALETTES=(0x118100,0x118200)
SEQUENCES=(0x118300,0x118340)
FRAMES,GROUPS=0x118400,0x118800
PIXELS,END=0x119000,0x124000
GFX_DEST,GFX_END=0x1e70000,0x1e7b000
SOURCE_SHA='51bd733de93015db71faa7e5172d68d90832622173d776d1725aeabf27e33e82'
SOURCE_GROUPS={'kano':(0xff8e9750,0xff8e97b0,0xff8e9810),
               'sonya':(0xff8e9ab0,0xff8e9b10,0xff8e9b70)}


def address(at):return BASE+at*8


def build(payload,program,gfx_directory):
    original=bytes(payload)
    if len(payload)!=0x200000 or hashlib.sha256(payload).hexdigest()!=SOURCE_SHA:
        raise ValueError('Use exact complete v300 choreography payload')
    if any(v!=255 for v in payload[HEADER:END]):
        raise ValueError('Morph allocation occupied')
    gfx=decoder.load_gfx(gfx_directory)
    output=bytearray(payload)
    frame_at,group_at,pixel_at=FRAMES,GROUPS,PIXELS
    reports={}
    for index,fighter in enumerate(('kano','sonya')):
        first=animation.frame_group(program,SOURCE_GROUPS[fighter][0],0xff800000,0xffffffff)
        if not first:raise ValueError('Original complete morph group missing')
        palette_source=animation.u32(program,animation.stock_file(first[0])+14)
        palette_at=animation.stock_file(palette_source)
        count=animation.u16(program,palette_at)
        if count!=(64 if fighter=='kano' else 63):raise ValueError('Original morph palette header changed')
        # Morph palettes already use the native 16-bit count, unlike ordinary
        # MK3 body palettes. Preserve every opaque index, with transparent zero.
        palette=list(struct.unpack_from(f'<{count}H',program,palette_at+2))
        palette[0]=0
        struct.pack_into('<H64H',output,PALETTES[index],64,*(palette+[0]*(64-count)))
        groups,components=[],[]
        for source_group in SOURCE_GROUPS[fighter]:
            frames=animation.frame_group(program,source_group,0xff800000,0xffffffff)
            if not frames or len(frames)!=2:raise ValueError('Original two-part morph composite changed')
            native_group=address(group_at)
            native_frames=[]
            for source_frame in frames:
                spec=decoder.component_spec(program,source_frame)
                indices=pixels.decode_indices(gfx,spec)
                if max(indices)>=count:raise ValueError('Morph component exceeds original palette')
                packed=pixels.pack_indices(indices)
                if frame_at+20>GROUPS or pixel_at+len(packed)>END or GFX_DEST+pixel_at-PIXELS+len(packed)>GFX_END:
                    raise ValueError('Morph storage overflow')
                source_bits=(GFX_DEST+pixel_at-PIXELS)*8
                native=address(frame_at)
                struct.pack_into('<4hIHI',output,frame_at,*spec[2:],source_bits,0x6000,address(PALETTES[index]))
                output[pixel_at:pixel_at+len(packed)]=packed
                components.append(dict(source=f'{source_frame:08X}',native=f'{native:08X}',width=spec[2],height=spec[3],
                    x_offset=spec[4],y_offset=spec[5],original_command=f'{spec[1]:04X}',source_bits=source_bits,
                    pixel_sha256=hashlib.sha256(indices).hexdigest()))
                native_frames.append(native);frame_at+=20;pixel_at=(pixel_at+len(packed)+3)&~3
            if group_at+12>META_END:raise ValueError('Morph group storage overflow')
            struct.pack_into('<3I',output,group_at,*native_frames,0);group_at+=12
            groups.append(dict(source=f'{source_group:08X}',native=f'{native_group:08X}',components=native_frames))
        block=animation.HYBRID_FILE_BASES[fighter]
        stance=animation.u32(original,block)
        stance_group=animation.u32(original,(stance-BASE)//8)
        if not BASE<=stance_group<BASE+len(original)*8:raise ValueError('Own native target stance missing')
        # Stock prefix, stock palette callback, three original target composites,
        # stock last-pose token and the OWN canonical stance. No donor code call.
        sequence=(0xff959cb0,6,0xff9645e0,*(int(g['native'],16) for g in groups),5,stance_group,0)
        struct.pack_into('<9I',output,SEQUENCES[index],*sequence)
        reports[fighter]=dict(groups=groups,components=components,palette_source=f'{palette_source:08X}',palette_colors=count,
            palette=f'{address(PALETTES[index]):08X}',sequence=f'{address(SEQUENCES[index]):08X}',sequence_words=sequence,
            target_stance=f'{stance_group:08X}',target_id=17+index)
    struct.pack_into('<4s6I',output,HEADER,b'KSM1',PIXELS,pixel_at-PIXELS,GFX_DEST,
                     address(SEQUENCES[0]),address(SEQUENCES[1]),12)
    if output[:HEADER]!=original[:HEADER] or output[END:]!=original[END:]:
        raise ValueError('Morph upgrade changed unrelated payload data')
    payload[:]=output
    return dict(scope='original_morph_assets_only_native_runtime_not_yet_verified',source_sha256=SOURCE_SHA,
                payload_sha256=hashlib.sha256(output).hexdigest(),pixel_bytes=pixel_at-PIXELS,component_count=12,
                header=HEADER,gfx_destination=GFX_DEST,fighters=reports)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    report_path=a.output.with_suffix('.morph.json')
    if a.output.exists() or report_path.exists():raise SystemExit('Refusing to overwrite payload/evidence')
    root=Path(__file__).resolve().parents[1]
    payload=bytearray(a.source.read_bytes());report=build(payload,(root/'mk3/mk3-maincpu.bin').read_bytes(),root/'mk3')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(payload)
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
