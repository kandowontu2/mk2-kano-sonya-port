#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("builder", ROOT / "tools" / "build_mk2ks_mk3.py")
builder = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(builder)

data = (ROOT / "mk3" / "mk3-maincpu.bin").read_bytes()

for fighter, block in (("kano", builder.KANO_BLOCK), ("sonya", builder.SONYA_BLOCK)):
    print(f"[{fighter}]")
    for key, groups in builder.DONOR_SEQUENCE_GROUPS[fighter].items():
        print(f"  {key[0]} {key[1]}")
        for group_address in groups:
            frames = builder.frame_group(data, group_address, block[0], block[1])
            print(f"    group={group_address:08x} frames={len(frames) if frames else 0}")
            for frame_address in frames or ():
                offset = builder.stock_file(frame_address)
                coords = [builder.signed(builder.u16(data, offset + i * 2)) for i in range(4)]
                source = builder.u32(data, offset + 8)
                command = builder.u16(data, offset + 12)
                tail = builder.u32(data, offset + 14) if offset + 18 <= len(data) else 0
                print(
                    f"      frame={frame_address:08x} xywh={coords} "
                    f"source={source:08x} command={command:04x} tail={tail:08x}"
                )
