#!/usr/bin/env python3
"""Build the MKII Kano/Sonya port prototype from MK3 revision 2.1.

MK3 kept MKII's 14/18-byte animation-frame layout.  The donor program data
is exposed in a separate two-MiB ROM window; only the two character animation
blocks and their referenced frame descriptors are relocated.  MK3 graphics
are appended after MKII's 12 MiB and frame source addresses are rebased.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path


TMS_ROM_BASE = 0xFF800000
DONOR_TMS_BASE = 0xFE800000
DONOR_SIZE = 0x200000
GFX_REBASE = 0x10000000

MK2_MAIN_TABLE = 0x020C2A
MK2_SPECIAL_TABLE = 0x020C6E
MK2_FIGHTER_COUNT = 0x11
NEW_MAIN_TABLE = 0x0FC800
NEW_SPECIAL_TABLE = 0x0FC880
SPECIAL_TABLE_IMMEDIATE = 0x020C0C
MAIN_TABLE_IMMEDIATE = 0x020C14

# MK3 2.1 character animation roots.  The second root is exactly 0x820 bits
# after the first and contains the special-animation dispatch table.
KANO_MAIN = 0xFF823CA0
KANO_SPECIAL = 0xFF8244C0
KANO_BLOCK = (0xFF823CA0, 0xFF831B80)
SONYA_MAIN = 0xFF831B80
SONYA_SPECIAL = 0xFF8323A0
SONYA_BLOCK = (0xFF831B80, 0xFF8408C0)

# Liu Kang is the MKII gameplay donor.  We clone his complete character block
# (rather than executing MK3 animation scripts) and replace only references to
# frame descriptors.  Every timing token, loop, shared routine and collision
# transition therefore remains native MKII data.
LIU_MAIN = 0xFF91FC60
LIU_SPECIAL = 0xFF9204A0
LIU_BLOCK = (0xFF91FC60, 0xFF92D710)
HYBRID_FILE_BASES = {
    "kano": 0x100000,
    "sonya": 0x104000,
}
HYBRID_VARIANT_BASES = {
    "kano_grab": 0x108000,
    "sonya_bicycle": 0x10C000,
    "kano_effect": 0x110000,
    "sonya_effect": 0x114000,
}
# The main table has 65 cells. The much shorter special table is deliberately
# scanned through the same address span because its following bytes contain
# pose/component lists that also need repainting. Post-table cells are not
# independent special-move dispatch entries.
ANIMATION_ENTRIES = 65

# Main animation IDs were reordered between MKII and MK3.  These translations
# are based on the actual composite pose lists (tools/audit_animation_poses.py),
# not equal numeric IDs.  For example, MKII 15 is a knockdown, whereas MK3 15 is
# a low punch; mapping them numerically left defeated fighters standing up.
STANDARD_ANIMATION_TRANSLATIONS = {
    0: (0, "stance"),
    1: (1, "walk forward"),
    2: (1, "short forward walk"),
    3: (2, "walk backward"),
    4: (2, "short backward walk"),
    5: (4, "crouch"),
    6: (22, "vertical jump"),
    7: (26, "forward somersault"),
    8: (27, "backward somersault"),
    9: (3, "turn"),
    10: (5, "crouching turn"),
    11: (12, "standing block"),
    12: (6, "crouching block"),
    13: (17, "high kick"),
    14: (18, "low kick"),
    15: (30, "knockdown"),
    16: (28, "high hit"),
    17: (29, "low hit"),
    18: (33, "backward-fall recovery"),
    19: (14, "high punch"),
    20: (15, "low punch"),
    21: (20, "sweep"),
    22: (31, "sweep fall"),
    23: (34, "sweep recovery"),
    24: (8, "crouching punch"),
    25: (9, "crouching high kick"),
    26: (9, "crouching low kick"),
    27: (7, "crouching hit"),
    28: (11, "uppercut"),
    29: (23, "jump kick"),
    31: (24, "jump punch"),
    32: (21, "roundhouse"),
    33: (19, "close knee"),
    34: (16, "close elbow"),
    35: (32, "stumble"),
    36: (35, "forward fall"),
    37: (32, "short stumble"),
    40: (37, "dizzy"),
    41: (13, "victory"),
}

# Explicit move translations discovered by tracing the original MKII and MK3
# state machines.  The first tuple names the safe Liu Kang gameplay state that
# MKII will continue to execute; the second names the MK3 pose list that should
# be painted over it.  This is deliberately semantic rather than numeric: the
# same table index means different things in the two games.
DONOR_ANIMATION_OVERRIDES = {
    "kano": {
        ("main", 38): ("main", 36),  # high fireball -> knife throw pose
        ("main", 39): ("main", 55),  # projectile follow-up -> detached knife
        ("special", 0): ("special", 1),  # low fireball -> blade swipe
        ("special", 1): ("main", 55),  # detached low projectile, never a body pose
        ("main", 30): ("main", 26),  # flying kick -> cannonball
        ("special", 6): ("special", 2),  # held LK -> grab/shake
    },
    "sonya": {
        ("main", 38): ("main", 36),  # high fireball -> actual ring release
        ("main", 39): ("main", 55),  # projectile follow-up -> energy ring
        ("special", 0): ("special", 0),  # low fireball -> leg grab
        ("special", 1): ("main", 55),  # low-fireball effect -> energy ring
        ("main", 30): ("special", 3),  # flying kick -> square-wave punch
        ("special", 6): ("special", 1),  # held LK -> bicycle kick
    },
}

# Detached projectile assets are now converted into ordinary MKII DMA data.
PRESERVE_NATIVE_STOCK_ANIMATIONS = set()

PRESERVE_NATIVE_BY_FIGHTER = {
    "kano": set(),
    "sonya": set(),
}

# The two MK3 dispatch tables are interleaved in the fighter blocks.  A span
# inferred from only one table can therefore run straight through an unrelated
# move from the other table.  These traced boundaries stop the signature moves
# at their real control/list boundary before frame extraction.
DONOR_SPAN_OVERRIDES = {
    "kano": {
        ("main", 36): (0xFF82F2C0, 0xFF82F700),
        ("special", 2): (0xFF830280, 0xFF830940),
    },
    "sonya": {
        ("main", 55): (0xFF83DF20, 0xFF83E620),
        ("special", 0): (0xFF83B920, 0xFF83C0E0),
        ("special", 1): (0xFF83E620, 0xFF83ED00),
    },
}

# Some MK3 control records point at pose lists outside their own script span,
# and the next move's lists can sit immediately after them.  These are the
# exact pose-list address ranges observed in native MK3 DMA traces.  Filtering
# by the list address (after following the script pointers) prevents a grab or
# bicycle kick from accidentally inheriting the following fighter animation.
DONOR_GROUP_RANGES = {
    "kano": {
        ("main", 36): ((0xFF82F400, 0xFF82F700),),
        ("main", 55): ((0xFF82EC40, 0xFF82F2C0),),
        ("special", 1): ((0xFF82FC40, 0xFF830280),),
        ("special", 2): ((0xFF830420, 0xFF830700),),
        ("main", 26): ((0xFF828BE0, 0xFF828E00),),
    },
    "sonya": {
        ("main", 36): ((0xFF83DBE0, 0xFF83DF20),),
        ("main", 55): ((0xFF83E100, 0xFF83E620),),
        ("special", 0): ((0xFF83BBE0, 0xFF83BEC0),),
        ("special", 3): (
            (0xFF836160, 0xFF8361E0),
            (0xFF840880, 0xFF8408C0),
        ),
        ("special", 1): ((0xFF83EA40, 0xFF83ECA0),),
    },
}

# Signature animations get their native pose order rather than being reduced
# to the number of keyframe slots in the MKII host animation.  Complex MK3
# moves often interleave body and effect-object lists; these explicit lists
# include only the pose groups that belong on the fighter/projectile object.
DONOR_SEQUENCE_GROUPS = {
    "kano": {
        ("main", 36): (
            0xFF82F400, 0xFF82F460, 0xFF82F4C0, 0xFF82F520,
            0xFF82F580, 0xFF82F5E0, 0xFF82F640,
        ),
        ("main", 55): (
            # Flight only. Intro sparks and impact bursts belong to separate
            # processes in MK3, not to MKII's travelling projectile object.
            0xFF82EE80, 0xFF82EEC0, 0xFF82EF00, 0xFF82EF40,
            0xFF82EF80, 0xFF82EFC0, 0xFF82F000, 0xFF82F040,
            0xFF82F080, 0xFF82F0C0,
        ),
        ("special", 1): (
            0xFF82FC40, 0xFF82FCA0, 0xFF82FD00, 0xFF82FD60,
            0xFF82FDC0, 0xFF82FE20, 0xFF82FE80, 0xFF82FEE0,
            0xFF82FF40, 0xFF82FFA0,
        ),
        ("special", 2): (
            0xFF830420, 0xFF830480, 0xFF8304E0, 0xFF8304E0,
            0xFF830540, 0xFF8305A0, 0xFF830600, 0xFF830660,
            0xFF8306C0, 0xFF830660,
        ),
        ("main", 26): (
            0xFF828BE0, 0xFF828C40, 0xFF828C80, 0xFF828CC0,
            0xFF828D00, 0xFF828D40, 0xFF828D80, 0xFF828DC0,
        ),
    },
    "sonya": {
        ("main", 4): (0xFF8332C0, 0xFF833320, 0xFF833380),
        ("main", 55): (0xFF83E100, 0xFF83E140, 0xFF83E180, 0xFF83E1C0),
        ("special", 0): (
            0xFF83BBE0, 0xFF83BC60, 0xFF83BCE0, 0xFF83BD40,
            0xFF83BDA0, 0xFF83BE00, 0xFF83BE60, 0xFF83BE60,
            0xFF83BE00, 0xFF83BDA0, 0xFF83BD40, 0xFF83BCE0,
            0xFF83BC60, 0xFF83BBE0,
        ),
        ("special", 3): (0xFF836160, 0xFF8361A0, 0xFF840880),
        ("special", 1): (
            0xFF83EA40, 0xFF83EA80, 0xFF83EAE0, 0xFF83EB40,
            0xFF83EB80, 0xFF83EBC0, 0xFF83EC00, 0xFF83EC40,
            0xFF83EC80, 0xFF83EC40, 0xFF83EC00, 0xFF83EBC0,
            0xFF83EB80, 0xFF83EAE0, 0xFF83EA80, 0xFF83EA40,
        ),
    },
}

# Reserved for any donor move that is proven to use frame descriptors outside
# its fighter block.  Native read taps showed Kano's knife is fully contained
# in main animation 55, so it deliberately has no external-frame override.
DONOR_TARGET_FRAME_SEQUENCES = {
    "kano": {},
    "sonya": {},
}


def u16(data: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def u32(data: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def put_u32(data: bytearray, offset: int, value: int) -> None:
    struct.pack_into("<I", data, offset, value)


def stock_file(address: int) -> int:
    if not TMS_ROM_BASE <= address <= 0xFFFFFFFF or address & 0x0F:
        raise ValueError(f"not an aligned MK3 ROM pointer: 0x{address:08x}")
    return (address - TMS_ROM_BASE) // 8


def stock_address(file_offset: int) -> int:
    return TMS_ROM_BASE + file_offset * 8


def donor_address(file_offset: int) -> int:
    return DONOR_TMS_BASE + file_offset * 8


def relocate_pointer(value: int) -> int:
    if TMS_ROM_BASE <= value <= 0xFFFFFFFF and not value & 0x0F:
        return value - (TMS_ROM_BASE - DONOR_TMS_BASE)
    return value


def _paired_victim_operands(
    source: bytes, fighter: str, animation: int, phases: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    """Parse the typed XY records and terminators of a paired victim script.

    A negative X following token 10 overlaps a pointer-shaped DWORD at the
    preceding halfword. It is data, not a pointer, and must not be rebased.
    """
    roots = {"kano": (KANO_MAIN, KANO_BLOCK), "sonya": (SONYA_MAIN, SONYA_BLOCK)}
    if fighter not in roots:
        raise ValueError(f"unknown paired-victim fighter: {fighter}")
    root, block = roots[fighter]
    cursor = stock_file(u32(source, stock_file(root) + animation * 4))
    start, end = map(stock_file, block)
    operands = []
    for count in phases:
        if cursor < start or cursor + count * 12 + 4 > min(end, len(source)):
            raise ValueError(f"{fighter}: paired victim animation {animation} outside fighter block")
        for _ in range(count):
            if u32(source, cursor) != 10:
                raise ValueError(f"{fighter}: unexpected paired victim animation {animation} record")
            group = stock_file(u32(source, cursor + 8))
            if not start <= group < end:
                raise ValueError(f"{fighter}: paired victim pose outside fighter block")
            operands.append((cursor + 4, cursor + 8))
            cursor += 12
        if u32(source, cursor):
            raise ValueError(f"{fighter}: missing paired victim animation {animation} terminator")
        cursor += 4
    return tuple(operands)


def leg_victim_operands(source: bytes, fighter: str) -> tuple[tuple[int, int], ...]:
    return _paired_victim_operands(source, fighter, 54, (5,))


def choke_victim_operands(source: bytes, fighter: str) -> tuple[tuple[int, int], ...]:
    # Three lift poses, then a separately terminated four-pose squeeze loop.
    return _paired_victim_operands(source, fighter, 56, (3, 4))


def paired_victim_operands(source: bytes, fighter: str) -> tuple[tuple[int, int], ...]:
    return leg_victim_operands(source, fighter) + choke_victim_operands(source, fighter)


def relocate_pointer_words(
    data: bytearray, start: int, end: int,
    protected_ranges: tuple[tuple[int, int], ...] = (),
) -> int:
    """Relocate pointer-shaped words in pointer/list data, not packed frames."""
    snapshot = bytes(data)
    # A null group terminator followed by a frame whose low word is FF90h
    # also looks like FF900000h at the intervening halfword. Prefer fields
    # independently validated against actual frame descriptors, not that
    # overlapping byte pattern (Sonya's FF8369C0 stumble exposed this).
    frame_fields = {offset for offset, _ in frame_references(
        snapshot, stock_address(start), stock_address(end))}
    changes: list[tuple[int, int]] = []
    for offset in range(start, end - 3, 2):
        if any(offset < last and offset + 4 > first for first, last in protected_ranges):
            continue
        if offset not in frame_fields and (offset - 2 in frame_fields or offset + 2 in frame_fields):
            continue
        value = u32(snapshot, offset)
        replacement = relocate_pointer(value)
        if replacement != value:
            changes.append((offset, replacement))
    # A real pointer field cannot overlap another real pointer by 16 bits.
    # Frame fields above have priority; keep non-overlapping remaining words.
    accepted: list[tuple[int, int]] = []
    for item in changes:
        if accepted and item[0] < accepted[-1][0] + 4:
            continue
        accepted.append(item)
    for offset, replacement in accepted:
        put_u32(data, offset, replacement)
    return len(accepted)


def signed(value: int) -> int:
    return value - 0x10000 if value & 0x8000 else value


def looks_like_frame(data: bytes, offset: int) -> bool:
    if offset < 0 or offset + 14 > len(data):
        return False
    coords = [signed(u16(data, offset + index * 2)) for index in range(4)]
    if any(value < -0x400 or value > 0x400 for value in coords):
        return False
    source = u32(data, offset + 8)
    command = u16(data, offset + 12)
    # MK3 composites mix skip-form (...80) and full-copy (...00) records; the
    # latter are especially common in projectiles and small effect layers.
    # Both keep the low seven command bits clear.  Rejecting full-copy records
    # leaves their source offsets unrebased and makes MKII draw unrelated art.
    return (
        source < 0x0A000000
        and not (command & 0x007F)
        and 3 <= ((command >> 12) & 7) <= 7
    )


def collect_frame_pointers(donor: bytes) -> set[int]:
    result: set[int] = set()
    for start_address, end_address in (KANO_BLOCK, SONYA_BLOCK):
        start, end = stock_file(start_address), stock_file(end_address)
        for offset in range(start, end - 3, 2):
            value = u32(donor, offset)
            if not (TMS_ROM_BASE <= value <= 0xFFFFFFFF) or value & 0x0F:
                continue
            target = stock_file(value)
            if looks_like_frame(donor, target):
                result.add(value)
    return result


def relocate_frame_descriptors(data: bytearray, pointers: set[int]) -> dict[str, int]:
    short_records = 0
    long_records = 0
    for pointer in sorted(pointers):
        offset = stock_file(pointer)
        if not looks_like_frame(data, offset):
            raise SystemExit(f"frame validation changed at 0x{pointer:08x}")
        source = u32(data, offset + 8)
        put_u32(data, offset + 8, source + GFX_REBASE)

        # Long records have a donor program/palette pointer after the command;
        # short records end at 14 bytes and the next frame begins immediately.
        tail = u32(data, offset + 14) if offset + 18 <= len(data) else 0
        if TMS_ROM_BASE <= tail <= 0xFFFFFFFF and not tail & 0x0F:
            put_u32(data, offset + 14, relocate_pointer(tail))
            long_records += 1
        else:
            short_records += 1
    return {"records": len(pointers), "short": short_records, "long": long_records}


def sequence_spans(
    data: bytes,
    root_address: int,
    block: tuple[int, int],
    boundary_roots: tuple[int, ...] = (),
) -> dict[int, tuple[int, int]]:
    """Return animation ID -> byte-address span for an interleaved block.

    MKII and MK3 place the main and special dispatch targets between one
    another.  The next pointer in only one table is therefore not a safe end
    boundary: it can run through several scripts owned by the other table.
    Include both roots when identifying the next sequence address.
    """
    start_address, end_address = block
    root = stock_file(root_address)
    pointers = [u32(data, root + index * 4) for index in range(ANIMATION_ENTRIES)]
    boundary_values = list(pointers)
    for boundary_root in boundary_roots:
        boundary = stock_file(boundary_root)
        boundary_values.extend(
            u32(data, boundary + index * 4) for index in range(ANIMATION_ENTRIES)
        )
    valid = sorted(
        {value for value in boundary_values if start_address <= value < end_address}
    )
    result: dict[int, tuple[int, int]] = {}
    for index, value in enumerate(pointers):
        if value not in valid:
            continue
        position = valid.index(value)
        result[index] = (value, valid[position + 1] if position + 1 < len(valid) else end_address)
    return result


def frame_references(data: bytes, start_address: int, end_address: int) -> list[tuple[int, int]]:
    """Find non-overlapping (file location, frame pointer) references in a span."""
    start, end = stock_file(start_address), stock_file(end_address)
    candidates: list[tuple[int, int]] = []
    for offset in range(start, end - 3, 2):
        value = u32(data, offset)
        if not (TMS_ROM_BASE <= value <= 0xFFFFFFFF) or value & 0x0F:
            continue
        if looks_like_frame(data, stock_file(value)):
            candidates.append((offset, value))
    accepted: list[tuple[int, int]] = []
    for item in candidates:
        if accepted and item[0] < accepted[-1][0] + 4:
            continue
        accepted.append(item)
    return accepted


def frame_group(
    data: bytes, address: int, span_start: int, span_end: int
) -> list[int] | None:
    """Return a local zero-terminated composite-pose frame list."""
    if not (span_start <= address < span_end) or address & 0x0F:
        return None
    offset = stock_file(address)
    frames: list[int] = []
    for _ in range(16):
        value = u32(data, offset)
        if value == 0:
            return frames or None
        if not (TMS_ROM_BASE <= value <= 0xFFFFFFFF) or value & 0x0F:
            return None
        if not looks_like_frame(data, stock_file(value)):
            return None
        frames.append(value)
        offset += 4
    return None


def group_references(
    data: bytes,
    start_address: int,
    end_address: int,
    group_start: int | None = None,
    group_end: int | None = None,
) -> list[tuple[int, int, list[int]]]:
    """Return (file location, group pointer, component frames) in display order."""
    start, end = stock_file(start_address), stock_file(end_address)
    group_start = start_address if group_start is None else group_start
    group_end = end_address if group_end is None else group_end
    result: list[tuple[int, int, list[int]]] = []
    for offset in range(start, end - 3, 2):
        value = u32(data, offset)
        group = frame_group(data, value, group_start, group_end)
        if group is not None:
            if result and offset < result[-1][0] + 4:
                continue
            result.append((offset, value, group))
    return result


def ordered_unique(values: list[int]) -> list[int]:
    result: list[int] = []
    seen: set[int] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def map_by_position(values: list[int], index: int, count: int) -> int:
    if len(values) == 1 or count <= 1:
        return values[0]
    return values[round(index * (len(values) - 1) / (count - 1))]


def native_vertical_jump(source: bytes, fighter: str) -> tuple[int, ...]:
    """Express MK3's airborne/landing pose order in MKII's two-phase format.

    MK3 FF983B10 skips pose zero on takeoff, then plays poses one and two.
    Its landing at FF983DA0/FF983E40 plays pose one then pose zero. A generic
    unique-pose substitution put pose two only in MKII's landing phase,
    leaving an extended-leg airborne silhouette and the wrong hurt bounds.
    """
    root, block = {
        "kano": (KANO_MAIN, KANO_BLOCK),
        "sonya": (SONYA_MAIN, SONYA_BLOCK),
    }[fighter]
    at = stock_file(u32(source, stock_file(root) + 22 * 4))
    poses = tuple(u32(source, at + index * 4) for index in range(3))
    if u32(source, at + 12) or any(frame_group(source, pose, *block) is None for pose in poses):
        raise ValueError(f"{fighter}: unexpected original vertical-jump layout")
    first, middle, tucked = map(relocate_pointer, poses)
    return middle, tucked, 0, middle, first, 0


def build_hybrid_block(
    output: bytearray,
    mk2: bytes,
    mk3_source: bytes,
    fighter: str,
    donor_block: tuple[int, int],
    donor_main: int,
    donor_special: int,
    destination: int | None = None,
    override_updates: dict[tuple[str, int], tuple[str, int]] | None = None,
) -> dict[str, int]:
    """Clone Liu's MKII scripts while substituting MK3 fighter frames."""
    source_start, source_end = map(stock_file, LIU_BLOCK)
    destination = HYBRID_FILE_BASES[fighter] if destination is None else destination
    script_bytes = source_end - source_start
    block = bytearray(b"\xFF" * 0x4000)
    block[:script_bytes] = mk2[source_start:source_end]
    source_address = LIU_BLOCK[0]
    destination_address = donor_address(destination)

    # First relocate every internal Liu pointer so the cloned control graph is
    # self-contained.  Calls and data pointers outside the fighter block remain
    # aimed at MKII, which is exactly what keeps the state machine safe.
    snapshot = bytes(block[:script_bytes])
    internal_changes: list[tuple[int, int]] = []
    for offset in range(0, script_bytes - 3, 2):
        value = u32(snapshot, offset)
        if LIU_BLOCK[0] <= value < LIU_BLOCK[1] and not value & 0x0F:
            internal_changes.append((offset, destination_address + value - source_address))
    accepted_internal: list[tuple[int, int]] = []
    for item in internal_changes:
        if accepted_internal and item[0] < accepted_internal[-1][0] + 4:
            continue
        accepted_internal.append(item)
    for offset, value in accepted_internal:
        put_u32(block, offset, value)
    control_template = bytes(block[:script_bytes])

    substitutions = 0
    mapped_animations = 0
    missing_donor_frames = 0
    missing_donor_cases: list[dict[str, str | int]] = []
    stock_special_slots = (u32(mk2, stock_file(LIU_MAIN)) - LIU_SPECIAL) // 32
    frame_count_mismatches = 0
    composite_groups = 0
    composite_components = 0
    auxiliary_cursor = (script_bytes + 3) & ~3
    mapped_stock_sequences: set[int] = set()

    donor_tables = {
        "main": sequence_spans(
            mk3_source, donor_main, donor_block, (donor_main, donor_special)
        ),
        "special": sequence_spans(
            mk3_source, donor_special, donor_block, (donor_main, donor_special)
        ),
    }
    donor_roots = {"main": donor_main, "special": donor_special}
    overrides = {
        ("main", native): ("main", donor)
        for native, (donor, _) in STANDARD_ANIMATION_TRANSLATIONS.items()
    }
    overrides.update(DONOR_ANIMATION_OVERRIDES[fighter])
    if override_updates:
        overrides.update(override_updates)
    target_frame_sequences = DONOR_TARGET_FRAME_SEQUENCES[fighter]

    for stock_kind, stock_root in (("main", LIU_MAIN), ("special", LIU_SPECIAL)):
        stock_spans = sequence_spans(
            mk2, stock_root, LIU_BLOCK, (LIU_MAIN, LIU_SPECIAL)
        )
        for animation_id, (stock_start, stock_end) in stock_spans.items():
            if ((stock_kind, animation_id) in PRESERVE_NATIVE_STOCK_ANIMATIONS or
                    (stock_kind, animation_id) in PRESERVE_NATIVE_BY_FIGHTER[fighter]):
                root_location = stock_file(stock_root) - source_start + animation_id * 4
                original_pointer = u32(
                    mk2, stock_file(stock_root) + animation_id * 4
                )
                put_u32(block, root_location, original_pointer)
                continue

            # MKII deliberately points many unused/fallback table entries at a
            # shared script (stance is the most visible example).  Repainting
            # that same cloned script once per table entry means a later dummy
            # entry silently replaces the correct core animation.  Main-table
            # entries are visited first, followed by specials, so retaining the
            # first mapping gives the shared script its real gameplay meaning.
            is_override = ((stock_kind, animation_id) in overrides or
                           (stock_kind, animation_id) in target_frame_sequences)
            sequence_was_mapped = stock_start in mapped_stock_sequences
            if sequence_was_mapped and not is_override:
                continue
            if not sequence_was_mapped:
                mapped_stock_sequences.add(stock_start)

            # A few real Liu moves share their control script with a fallback
            # table entry.  Keeping the first paint fixes stance and ordinary
            # movement, but an explicit Kano/Sonya override must still get a
            # private copy or it inherits that earlier entry's body frames.
            # Clone only the overridden occurrence and point its dispatch cell
            # at the copy; all timing, engine calls and collision tokens remain
            # byte-for-byte MKII code.
            patch_delta = 0
            if sequence_was_mapped:
                stock_block_start = stock_file(stock_start) - source_start
                stock_block_end = stock_file(stock_end) - source_start
                clone_size = stock_block_end - stock_block_start
                clone_cursor = (auxiliary_cursor + 3) & ~3
                if clone_size <= 0 or clone_cursor + clone_size > len(block):
                    raise SystemExit(f"{fighter} hybrid override clones exceed reserved block")
                clone = bytearray(control_template[stock_block_start:stock_block_end])
                original_sequence = destination_address + stock_start - source_address
                original_sequence_end = original_sequence + clone_size * 8
                cloned_sequence = donor_address(destination + clone_cursor)
                pointer_changes: list[tuple[int, int]] = []
                for offset in range(0, clone_size - 3, 2):
                    value = u32(clone, offset)
                    if original_sequence <= value < original_sequence_end and not value & 0x0F:
                        pointer_changes.append(
                            (offset, cloned_sequence + value - original_sequence)
                        )
                accepted_changes: list[tuple[int, int]] = []
                for item in pointer_changes:
                    if accepted_changes and item[0] < accepted_changes[-1][0] + 4:
                        continue
                    accepted_changes.append(item)
                for offset, value in accepted_changes:
                    put_u32(clone, offset, value)
                block[clone_cursor : clone_cursor + clone_size] = clone
                auxiliary_cursor = clone_cursor + clone_size
                root_location = (
                    stock_file(stock_root) - source_start + animation_id * 4
                )
                put_u32(block, root_location, cloned_sequence)
                patch_delta = clone_cursor - stock_block_start
            donor_kind, donor_animation_id = overrides.get(
                (stock_kind, animation_id), (stock_kind, animation_id)
            )
            donor_spans = donor_tables[donor_kind]
            donor_root = donor_roots[donor_kind]
            fallback_span = donor_spans.get(0) or next(iter(donor_spans.values()))
            donor_span = DONOR_SPAN_OVERRIDES[fighter].get(
                (donor_kind, donor_animation_id),
                donor_spans.get(donor_animation_id, fallback_span),
            )
            if donor_animation_id not in donor_spans:
                missing_donor_frames += 1
                role = ("component data" if stock_kind == "special" and
                        animation_id >= stock_special_slots else "dispatch")
                missing_donor_cases.append({
                    "stock_kind": stock_kind,
                    "stock_id": animation_id,
                    "donor_kind": donor_kind,
                    "donor_id": donor_animation_id,
                    "table_role": role,
                    "reason": "donor component data absent" if role == "component data"
                              else "donor animation absent",
                })
            stock_groups = group_references(mk2, stock_start, stock_end, LIU_BLOCK[0], LIU_BLOCK[1])
            explicit_frames = target_frame_sequences.get((stock_kind, animation_id), ())
            # The control script and its composite pose lists are separate
            # allocations in MK3.  In particular, standing, walking and both
            # projectile transitions keep every pose list immediately outside
            # the script span.  Validate targets against the fighter block so
            # these complete two/three-layer poses are retained; restricting
            # targets to donor_span silently produced mixed Liu/MK3 fragments.
            donor_group_bounds = donor_block
            donor_groups = group_references(
                mk3_source,
                donor_span[0],
                donor_span[1],
                donor_group_bounds[0],
                donor_group_bounds[1],
            )
            signature_groups = set(
                DONOR_SEQUENCE_GROUPS[fighter].get(
                    (donor_kind, donor_animation_id), ()
                )
            )
            group_ranges = DONOR_GROUP_RANGES[fighter].get(
                (donor_kind, donor_animation_id)
            )
            if signature_groups:
                # Keep MKII's native timing/control script, but feed its pose
                # slots only the exact body/projectile groups observed in the
                # donor move.  Broad address ranges also contain adjacent
                # effect and UI art, which can turn a projectile into a giant
                # portrait or a full-screen DMA fill.
                donor_groups = [
                    item for item in donor_groups if item[1] in signature_groups
                ]
            elif group_ranges:
                donor_groups = [
                    item
                    for item in donor_groups
                    if any(start <= item[1] < end for start, end in group_ranges)
                ]

            if not donor_groups and donor_span != fallback_span:
                donor_groups = group_references(
                    mk3_source, fallback_span[0], fallback_span[1]
                )
            mapped = False
            if stock_groups and explicit_frames:
                # Do this per script occurrence, not per unique original
                # group.  Liu's sequence intentionally revisits one pose, but
                # the shared MK3 effect advances through flight and impact.
                for index, (location, _, _) in enumerate(stock_groups):
                    frame = map_by_position(explicit_frames, index, len(stock_groups))
                    if auxiliary_cursor + 8 > len(block):
                        raise SystemExit(f"{fighter} hybrid composite lists exceed reserved block")
                    group = donor_address(destination + auxiliary_cursor)
                    put_u32(block, auxiliary_cursor, relocate_pointer(frame))
                    put_u32(block, auxiliary_cursor + 4, 0)
                    auxiliary_cursor += 8
                    put_u32(block, location - source_start + patch_delta, group)
                    substitutions += 1
                    composite_groups += 1
                    composite_components += 1
                mapped = True
            else:
                stock_group_values = ordered_unique([value for _, value, _ in stock_groups])
                donor_group_values = ordered_unique([value for _, value, _ in donor_groups])
            if not explicit_frames and stock_group_values and donor_group_values:
                donor_group_frames = {
                    value: frames for _, value, frames in donor_groups
                }
                group_for_stock: dict[int, int] = {}
                for index, stock_group in enumerate(stock_group_values):
                    donor_group = map_by_position(
                        donor_group_values, index, len(stock_group_values)
                    )
                    frames = donor_group_frames[donor_group]
                    bytes_needed = (len(frames) + 1) * 4
                    if auxiliary_cursor + bytes_needed > len(block):
                        raise SystemExit(f"{fighter} hybrid composite lists exceed reserved block")
                    group_for_stock[stock_group] = donor_address(destination + auxiliary_cursor)
                    for frame_index, frame in enumerate(frames):
                        put_u32(
                            block,
                            auxiliary_cursor + frame_index * 4,
                            relocate_pointer(frame),
                        )
                    put_u32(block, auxiliary_cursor + len(frames) * 4, 0)
                    auxiliary_cursor += bytes_needed
                    composite_groups += 1
                    composite_components += len(frames)

                for location, value, _ in stock_groups:
                    put_u32(
                        block,
                        location - source_start + patch_delta,
                        group_for_stock[value],
                    )
                    substitutions += 1
                if len(stock_group_values) != len(donor_group_values):
                    frame_count_mismatches += 1
                mapped = True

            stock_refs = frame_references(mk2, stock_start, stock_end)
            stock_group_locations = {location for location, _, _ in stock_groups}
            stock_group_ranges = [
                (
                    stock_file(group),
                    stock_file(group) + (len(frames) + 1) * 4,
                )
                for _, group, frames in stock_groups
            ]
            # References inside original composite lists become unreachable
            # after their parent pointers are redirected.  Replace only direct
            # frame references elsewhere in the script so no Liu component can
            # leak into a donor pose.
            stock_refs = [
                item
                for item in stock_refs
                if item[0] not in stock_group_locations
                and not any(start <= item[0] < end for start, end in stock_group_ranges)
            ]
            donor_refs = (
                []
                if explicit_frames
                else frame_references(mk3_source, donor_span[0], donor_span[1])
            )
            if signature_groups and donor_groups:
                signature_frames = {
                    frame
                    for _, _, frames in donor_groups
                    for frame in frames
                }
                donor_refs = [
                    item for item in donor_refs if item[1] in signature_frames
                ]
            if not explicit_frames and not donor_refs and donor_span != fallback_span:
                donor_refs = frame_references(
                    mk3_source, fallback_span[0], fallback_span[1]
                )
            stock_values = ordered_unique([value for _, value in stock_refs])
            donor_values = ordered_unique([value for _, value in donor_refs])
            if stock_values and donor_values:
                if len(stock_values) != len(donor_values):
                    frame_count_mismatches += 1

                donor_for_stock = {
                    value: relocate_pointer(
                        map_by_position(donor_values, index, len(stock_values))
                    )
                    for index, value in enumerate(stock_values)
                }
                for location, value in stock_refs:
                    block_location = location - source_start + patch_delta
                    put_u32(block, block_location, donor_for_stock[value])
                    substitutions += 1
                mapped = True
            elif stock_values:
                if donor_animation_id in donor_spans:
                    missing_donor_frames += 1
                    role = ("component data" if stock_kind == "special" and
                            animation_id >= stock_special_slots else "dispatch")
                    missing_donor_cases.append({
                        "stock_kind": stock_kind,
                        "stock_id": animation_id,
                        "donor_kind": donor_kind,
                        "donor_id": donor_animation_id,
                        "table_role": role,
                        "reason": "donor animation has no direct frames",
                    })
            if mapped:
                mapped_animations += 1

    # Own jump script with the original airborne and landing phase semantics.
    # All users retain MKII's native jump scheduler, gravity and input handling.
    jump = native_vertical_jump(mk3_source, fighter)
    jump_cursor = (auxiliary_cursor + 3) & ~3
    if jump_cursor + len(jump) * 4 > len(block):
        raise ValueError(f"{fighter}: native jump script exceeds reserved block")
    for index, value in enumerate(jump):
        put_u32(block, jump_cursor + index * 4, value)
    put_u32(block, 6 * 4, donor_address(destination + jump_cursor))
    auxiliary_cursor = jump_cursor + len(jump) * 4
    output[destination : destination + len(block)] = block
    return {
        "script_bytes": script_bytes,
        "allocated_bytes": auxiliary_cursor,
        "internal_pointers": len(accepted_internal),
        "mapped_animations": mapped_animations,
        "frame_substitutions": substitutions,
        "composite_groups": composite_groups,
        "composite_components": composite_components,
        "missing_donor_frames": missing_donor_frames,
        "missing_dispatch_mappings": sum(
            case["table_role"] == "dispatch" for case in missing_donor_cases
        ),
        "missing_component_mappings": sum(
            case["table_role"] == "component data" for case in missing_donor_cases
        ),
        "missing_donor_cases": missing_donor_cases,
        "frame_count_mismatches": frame_count_mismatches,
    }


def digest_bytes(data: bytes) -> dict[str, str | int]:
    return {
        "size": len(data),
        "crc32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def write_outputs(output_dir: Path, program: bytes, donor: bytes) -> dict[str, dict[str, str | int]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "mk2ks-maincpu.bin": program,
        "mk2ks.uj12": program[0::2],
        "mk2ks.ug12": program[1::2],
        "mk2ks.mdata": donor,
    }
    report: dict[str, dict[str, str | int]] = {}
    for name, contents in files.items():
        (output_dir / name).write_bytes(contents)
        report[name] = digest_bytes(contents)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mk2_program", type=Path)
    parser.add_argument("mk3_program", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--prototype",
        choices=("kano", "sonya", "none"),
        default="none",
        help="temporarily skin MKII fighter ID 1 for visual/combat testing",
    )
    args = parser.parse_args()

    mk2 = bytearray(args.mk2_program.read_bytes())
    mk3_source = args.mk3_program.read_bytes()
    if len(mk2) != 0x100000 or len(mk3_source) != 0x100000:
        raise SystemExit("Both combined program images must be exactly 1 MiB")

    donor = bytearray(b"\xFF" * DONOR_SIZE)
    donor[: len(mk3_source)] = mk3_source

    pointer_relocations: dict[str, int] = {}
    for name, (start_address, end_address) in {
        "kano": KANO_BLOCK,
        "sonya": SONYA_BLOCK,
    }.items():
        pointer_relocations[name] = relocate_pointer_words(
            donor, stock_file(start_address), stock_file(end_address),
            protected_ranges=paired_victim_operands(mk3_source, name),
        )

    frame_pointers = collect_frame_pointers(mk3_source)
    frame_pointers.update(
        frame
        for fighter_sequences in DONOR_TARGET_FRAME_SEQUENCES.values()
        for frames in fighter_sequences.values()
        for frame in frames
    )
    frame_report = relocate_frame_descriptors(donor, frame_pointers)

    hybrid_report = {
        "kano": build_hybrid_block(
            donor, mk2, mk3_source, "kano", KANO_BLOCK, KANO_MAIN, KANO_SPECIAL
        ),
        "sonya": build_hybrid_block(
            donor, mk2, mk3_source, "sonya", SONYA_BLOCK, SONYA_MAIN, SONYA_SPECIAL
        ),
        "kano_grab": build_hybrid_block(
            donor,
            mk2,
            mk3_source,
            "kano",
            KANO_BLOCK,
            KANO_MAIN,
            KANO_SPECIAL,
            destination=HYBRID_VARIANT_BASES["kano_grab"],
            override_updates={("main", 30): ("special", 2)},
        ),
        "sonya_bicycle": build_hybrid_block(
            donor,
            mk2,
            mk3_source,
            "sonya",
            SONYA_BLOCK,
            SONYA_MAIN,
            SONYA_SPECIAL,
            destination=HYBRID_VARIANT_BASES["sonya_bicycle"],
            override_updates={("main", 30): ("special", 1)},
        ),
        "kano_effect": build_hybrid_block(
            donor,
            mk2,
            mk3_source,
            "kano",
            KANO_BLOCK,
            KANO_MAIN,
            KANO_SPECIAL,
            destination=HYBRID_VARIANT_BASES["kano_effect"],
            # Retain this alternate release block for the existing low-state
            # experiments. The normal projectile now uses standing main 38/39.
            override_updates={("special", 0): ("main", 36)},
        ),
        "sonya_effect": build_hybrid_block(
            donor,
            mk2,
            mk3_source,
            "sonya",
            SONYA_BLOCK,
            SONYA_MAIN,
            SONYA_SPECIAL,
            destination=HYBRID_VARIANT_BASES["sonya_effect"],
            # Alternate low-state release; detached effects in both roots are
            # converted to native records by build_native_projectiles below.
            override_updates={("special", 0): ("main", 36)},
        ),
    }

    stock_main = [u32(mk2, MK2_MAIN_TABLE + index * 4) for index in range(MK2_FIGHTER_COUNT)]
    stock_special = [u32(mk2, MK2_SPECIAL_TABLE + index * 4) for index in range(MK2_FIGHTER_COUNT)]
    hybrid_special_offset = stock_file(LIU_SPECIAL) - stock_file(LIU_MAIN)
    kano_main = donor_address(HYBRID_FILE_BASES["kano"])
    kano_special = donor_address(HYBRID_FILE_BASES["kano"] + hybrid_special_offset)
    sonya_main = donor_address(HYBRID_FILE_BASES["sonya"])
    sonya_special = donor_address(HYBRID_FILE_BASES["sonya"] + hybrid_special_offset)
    kano_grab_main = donor_address(HYBRID_VARIANT_BASES["kano_grab"])
    kano_grab_special = donor_address(HYBRID_VARIANT_BASES["kano_grab"] + hybrid_special_offset)
    sonya_bicycle_main = donor_address(HYBRID_VARIANT_BASES["sonya_bicycle"])
    sonya_bicycle_special = donor_address(HYBRID_VARIANT_BASES["sonya_bicycle"] + hybrid_special_offset)
    kano_effect_main = donor_address(HYBRID_VARIANT_BASES["kano_effect"])
    kano_effect_special = donor_address(HYBRID_VARIANT_BASES["kano_effect"] + hybrid_special_offset)
    sonya_effect_main = donor_address(HYBRID_VARIANT_BASES["sonya_effect"])
    sonya_effect_special = donor_address(HYBRID_VARIANT_BASES["sonya_effect"] + hybrid_special_offset)

    if args.prototype == "kano":
        stock_main[1], stock_special[1] = kano_main, kano_special
    elif args.prototype == "sonya":
        stock_main[1], stock_special[1] = sonya_main, sonya_special

    main_table = stock_main + [kano_main, sonya_main]
    special_table = stock_special + [kano_special, sonya_special]
    for start, values in ((NEW_MAIN_TABLE, main_table), (NEW_SPECIAL_TABLE, special_table)):
        for index, value in enumerate(values):
            put_u32(mk2, start + index * 4, value)
    put_u32(mk2, MAIN_TABLE_IMMEDIATE, stock_address(NEW_MAIN_TABLE))
    put_u32(mk2, SPECIAL_TABLE_IMMEDIATE, stock_address(NEW_SPECIAL_TABLE))

    import build_native_projectiles
    projectile_report = build_native_projectiles.build(donor, mk3_source, args.mk3_program.parent)
    import build_native_blade
    blade_report = build_native_blade.build(donor, mk3_source, args.mk3_program.parent)
    import build_native_fatality_art
    fatality_art_report = build_native_fatality_art.build(donor, mk3_source)
    import build_native_kiss
    kiss_report = build_native_kiss.build(donor, mk3_source, args.mk3_program.parent, include_arc_frame=True)
    files = write_outputs(args.output_dir, bytes(mk2), bytes(donor))
    report = {
        "prototype": args.prototype,
        "fighter_ids": {"kano": "0x11", "sonya": "0x12"},
        "selector": "dedicated roster IDs 0x11/0x12",
        "donor_window": "0xFE800000-0xFF7FFFFF",
        "pointer_relocations": pointer_relocations,
        "frames": frame_report,
        "hybrid_blocks": {
            "kano_main": f"0x{kano_main:08x}",
            "kano_special": f"0x{kano_special:08x}",
            "sonya_main": f"0x{sonya_main:08x}",
            "sonya_special": f"0x{sonya_special:08x}",
            "kano_grab_main": f"0x{kano_grab_main:08x}",
            "kano_grab_special": f"0x{kano_grab_special:08x}",
            "sonya_bicycle_main": f"0x{sonya_bicycle_main:08x}",
            "sonya_bicycle_special": f"0x{sonya_bicycle_special:08x}",
            "kano_effect_main": f"0x{kano_effect_main:08x}",
            "kano_effect_special": f"0x{kano_effect_special:08x}",
            "sonya_effect_main": f"0x{sonya_effect_main:08x}",
            "sonya_effect_special": f"0x{sonya_effect_special:08x}",
        },
        "hybrid_report": hybrid_report,
        "native_projectiles": projectile_report,
        "native_blade": blade_report,
        "native_fatality_art": fatality_art_report,
        "native_kiss": kiss_report,
        "files": files,
    }
    (args.output_dir / "mk2ks-build-report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
