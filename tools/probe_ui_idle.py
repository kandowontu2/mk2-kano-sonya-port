#!/usr/bin/env python3
"""Locate the native MK3 stance components used by the selector preview."""

from __future__ import annotations

import importlib.util
import pathlib
import struct


root = pathlib.Path(__file__).resolve().parent.parent
module_path = root / "tools" / "build_mk2ks_mk3.py"
spec = importlib.util.spec_from_file_location("mk2ks_builder", module_path)
builder = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(builder)
data = (root / "mk3" / "mk3-maincpu.bin").read_bytes()

sources = {0x120, 0x3F6A, 0x5199B0, 0x51C214}
targets = []
for offset in range(0, len(data) - 18, 2):
    source = struct.unpack_from("<I", data, offset + 8)[0]
    if source in sources and builder.looks_like_frame(data, offset):
        targets.append(
            (
                offset,
                builder.stock_address(offset),
                source,
                [builder.signed(builder.u16(data, offset + index * 2)) for index in range(4)],
                builder.u16(data, offset + 12),
            )
        )

print("targets", targets)
for name, main, special, block in (
    ("kano", builder.KANO_MAIN, builder.KANO_SPECIAL, builder.KANO_BLOCK),
    ("sonya", builder.SONYA_MAIN, builder.SONYA_SPECIAL, builder.SONYA_BLOCK),
):
    spans = builder.sequence_spans(data, main, block, (main, special))
    for animation_id, span in spans.items():
        direct = [value for _, value in builder.frame_references(data, *span)]
        groups = builder.group_references(data, *span, *block)
        grouped = [value for _, _, frames in groups for value in frames]
        if any(address in direct or address in grouped for _, address, _, _, _ in targets):
            print(
                name,
                animation_id,
                tuple(hex(value) for value in span),
                "direct",
                len(direct),
                "groups",
                [(hex(pointer), [hex(frame) for frame in frames]) for _, pointer, frames in groups],
            )
