#!/usr/bin/env python3
"""Read-only native MKII victim composites, retaining ROM art and palettes."""
import argparse
import json
from pathlib import Path
from PIL import Image,ImageDraw

import build_mk2ks_mk3 as b
import upgrade_ksui_previews as ui
from audit_leg_victims import NAMES,stock_gfx, stock_palette, write_sheet


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace",type=Path)
    parser.add_argument("output",type=Path)
    parser.add_argument("--native-reactions",action="store_true",
                        help="Review complete native head-removal scripts, not ordinary attacks")
    parser.add_argument("--descriptor-palettes",action="store_true",
                        help="Inspect long-frame palettes (not proof of runtime palette switching)")
    parser.add_argument("--native-death-palette",action="store_true",
                        help="Use FF90C800's actual per-ID primary palette for main-60 bodies")
    parser.add_argument("--headless-only",action="store_true",
                        help="Review paired windup and five headless collapse phases")
    parser.add_argument("--alternate",action="store_true",
                        help="Inspect native alternate costume death palettes")
    parser.add_argument("--fighter",choices=NAMES[:12],default="jax")
    args=parser.parse_args()
    if args.output.exists():
        raise SystemExit("Refusing to overwrite existing evidence")
    args.output.mkdir(parents=True)
    program=(args.workspace/"mk2/mk2-maincpu.bin").read_bytes()
    graphics=stock_gfx(args.workspace)
    fighter_id=NAMES.index(args.fighter)
    if args.fighter!="jax" and not args.native_reactions:
        raise SystemExit("Other fighters require --native-reactions")
    groups=[0xff991810,0xff9918b0,0xff991950,0xff9919f0,0xff991a50,0xff991ad0,
            0xff997980,0xff9979e0,0xff997a40,0xff997aa0,
            0xff997180,0xff997200,0xff997260,
            0xff995e40,0xff995ee0,0xff995f80,0xff996000,
            0xff995a00,0xff995a80,0xff995b00,0xff995b80,0xff995c20,0xff995ca0]
    labels=[f"candidate {index}" for index in range(len(groups))]
    if args.native_reactions:
        roots=[b.u32(program,b.MK2_MAIN_TABLE+i*4) for i in range(17)]
        root=roots[fighter_id]
        special=b.u32(program,b.MK2_SPECIAL_TABLE+fighter_id*4)
        end=min(value for value in set(roots)|{0xff9a0000} if value>root)
        spans=b.sequence_spans(program,root,(root,end),(root,special))
        groups=[]
        labels=[]
        for index in ((55,60) if args.headless_only else (55,57,59,60,63)):
            unique=dict((ptr,frames) for _,ptr,frames in
                        b.group_references(program,*spans[index],root,end))
            selected=(2,) if index==55 else (0,1,3,5,6)
            for pose,ptr in enumerate(unique):
                if args.headless_only and pose not in selected:
                    continue
                groups.append(ptr)
                labels.append(f"main {index} / pose {pose}")
    metadata=write_sheet(program,graphics,stock_palette(program,fighter_id),
                         list(zip(labels,groups)),
                         f"MKII {args.fighter} (unaccepted)",
                         args.output/f"{args.fighter}_native_bodies.png",grid=True)
    for row,ptr in zip(metadata,groups):
        row["components"]=[{"frame":f"{frame:08X}",
                            "spec":ui.component_spec(program,frame),
                            "tail_u32":f"{b.u32(program,b.stock_file(frame)+14):08X}"}
                           for frame in b.frame_group(program,ptr,b.TMS_ROM_BASE,0xffffffff)]
    if args.descriptor_palettes:
        sheet=Image.new("RGB",(1100,235*((len(groups)+4)//5)),(40,42,48))
        draw=ImageDraw.Draw(sheet)
        active_palette=stock_palette(program,fighter_id)
        previous_sequence=None
        for index,row in enumerate(metadata):
            x,y=(index%5)*220,(index//5)*235
            draw.text((x+4,y+4),row["label"],fill="white")
            draw.text((x+4,y+17),row["group"],fill="yellow")
            sequence=row["label"].split(" / ")[0]
            if sequence!=previous_sequence:
                active_palette=stock_palette(program,fighter_id)
                if args.native_death_palette and sequence=="main 60":
                    palette_ptr=b.u32(program,b.stock_file(0xff90c900)+fighter_id*8+
                                      (4 if args.alternate else 0))
                    at=b.stock_file(palette_ptr)
                    size=b.u16(program,at)
                    if not 1<=size<=256:
                        raise ValueError(f"Native death palette {palette_ptr:08X}: {size}")
                    active_palette=[(0,0,0,0)]+[(*ui.xrgb555(b.u16(program,at+2+i*2)),255)
                                             for i in range(1,size)]
                    active_palette +=[(255,0,255,255)]*(256-len(active_palette))
                    print(f"native_death_palette fighter={args.fighter} pointer={palette_ptr:08X} colors={size}")
                previous_sequence=sequence
            for component in row["components"]:
                ptr=int(component["tail_u32"],16)
                if 0xff800000<=ptr<0xffff0000 and ptr&15==0 and not (
                    args.native_death_palette and sequence=="main 60"):
                    at=b.stock_file(ptr)
                    count=b.u16(program,at)
                    if not 1<=count<=256:
                        raise ValueError(f"Invalid long-frame palette {ptr:08X}: {count}")
                    active_palette=[(0,0,0,0)]+[(*ui.xrgb555(b.u16(program,at+2+i*2)),255)
                                             for i in range(1,count)]
                    active_palette +=[(255,0,255,255)]*(256-len(active_palette))
                    component["palette_override"]=f"{ptr:08X}"
                source,command,width,height,xo,yo=component["spec"]
                part=ui.decode_component(graphics,active_palette,source,command,width,height)
                sheet.paste(part,(x+95-xo,y+52-yo),part)
        sheet.save(args.output/f"{args.fighter}_descriptor_palettes.png")
    (args.output/f"{args.fighter}_native_bodies.json").write_text(json.dumps(metadata,indent=2)+"\n")
    print(args.output/f"{args.fighter}_native_bodies.png")


if __name__=="__main__":
    main()
