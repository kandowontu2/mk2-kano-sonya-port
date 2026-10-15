"""Stage additive native shrinking tables and victim-owned palette routing.

Produces a mechanically encoded source fragment, not an emulator build. Original
source/art/data are pinned and untouched. Native choreography still needs replay.
"""
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'art_native_shang_drain_encoded_v1'
RESERVATION = ROOT / 'audit_native_shang_drain_reservation_native/report.json'
OUT = ROOT / 'source_native_shang_drain_fragment'

TEMPLATE = r'''
    // SHANG_OWNED_DRAIN_BEGIN
    // Give true Kano17/Sonya18 character-owned three-phase victim streams.
    // Keep the original 6-field / wait10 / 8-field grammar and shared final
    // skeleton/finish handoff. The first17 effective words stay byte-identical;
    // secondary rows12..16 are trailing stock colour data, NOT valid palettes.
    // This is additive native data, not an actor-ID alias or renderer cap.
    constexpr unsigned shang_drain_primary=0xb1000, shang_drain_secondary=0xb1060;
    constexpr unsigned shang_drain_descriptors=0xb10c0, shang_drain_groups=0xb1140;
    constexpr unsigned shang_drain_streams[2]={0xb1180,0xb11c0};
    constexpr unsigned shang_drain_palettes[2][2]={{0xb1200,0xb12a0},{0xb1340,0xb13e0}};
    constexpr unsigned shang_drain_original_palettes[2][2]={{0xfda00,0xfdb00},{0xf1500,0xf1600}};
    constexpr unsigned shang_drain_palette_router=0xb1500;
    constexpr uint32_t shang_drain_original_tables[2][17]={
@TABLES@
    };
    constexpr uint16_t shang_drain_original_helper[]={0xa30f,0xb7a8,0x0140,0x0d5f,0x1090,0xff84,0x09af,0x0100,0x0960};
    struct shang_drain_pose { uint16_t width,height; int16_t x,y; uint32_t graphics; };
    constexpr shang_drain_pose shang_drain_poses[6]={
@POSES@
    };
    // Six-bit pixels generated from the pinned transparent atlases. Native
    // DMA owns mirroring, clipping, palette fades and animation rendering.
    static constexpr uint8_t shang_drain_pixels[]={
@PIXELS@
    };
    static_assert(sizeof(shang_drain_pixels)==25632);
    if (memregion("maincpu")->bytes()!=0x100000 || gfx_region->bytes()!=0x2000000)
        fatalerror("MK2KS: unsupported native shrinking storage windows");
    for (unsigned at=0xb1000;at<0xb2000;at++)
        if (rom[at]!=0xff) fatalerror("MK2KS: native shrinking metadata/code storage occupied");
    for (unsigned at=0x1fb0000;at<0x1fc0000;at++)
        if (gfx[at]) fatalerror("MK2KS: native shrinking graphics storage occupied");
    constexpr uint32_t shang_drain_table_sources[2]={0xff9d7770,0xff9d8d70};
    constexpr uint32_t shang_drain_table_opcodes[2]={0xff8cafe0,0xff8cb0e0};
    for (unsigned table=0;table<2;table++)
    {
        unsigned const opcode=rom_offset(shang_drain_table_opcodes[table]);
        if (read16(opcode)!=0x09e0 || read32(opcode+2)!=shang_drain_table_sources[table])
            fatalerror("MK2KS: original shrinking victim lookup instruction changed");
        for (unsigned row=0;row<17;row++)
            if (read32(rom_offset(shang_drain_table_sources[table])+row*4)!=shang_drain_original_tables[table][row])
                fatalerror("MK2KS: original shrinking effective table row changed");
    }
    for (unsigned word=0;word<std::size(shang_drain_original_helper);word++)
        if (read16(rom_offset(0xff8cb410)+word*2)!=shang_drain_original_helper[word])
            fatalerror("MK2KS: complete original shrinking victim palette helper changed");
    for (unsigned costume=0;costume<2;costume++)
        for (unsigned fighter=0;fighter<2;fighter++)
            if (read16(shang_drain_original_palettes[costume][fighter])!=65 ||
                read16(shang_drain_original_palettes[costume][fighter]+2)!=0)
                fatalerror("MK2KS: owned shrinking victim palette layout changed");
    for (unsigned pose=0;pose<6;pose++)
    {
        auto const &p=shang_drain_poses[pose];
        uint64_t const first=p.graphics, last=first+uint64_t(p.width)*p.height*6;
        if (!p.width || p.width>80 || !p.height || p.height>125 ||
            first<0x1fb0000U*8 || last>uint64_t(0x1fb0000+sizeof(shang_drain_pixels))*8)
            fatalerror("MK2KS: typed shrinking bitmap bounds invalid");
    }
    // All original boundary/typed storage checks precede the first write.
    std::copy_n(shang_drain_pixels,sizeof(shang_drain_pixels),gfx+0x1fb0000);
    for (unsigned table=0;table<2;table++)
        std::copy_n(rom+rom_offset(shang_drain_table_sources[table]),68,
                    rom+(table ? shang_drain_secondary : shang_drain_primary));
    for (unsigned costume=0;costume<2;costume++)
        for (unsigned fighter=0;fighter<2;fighter++)
            std::copy_n(rom+shang_drain_original_palettes[costume][fighter],132,
                        rom+shang_drain_palettes[costume][fighter]);
    for (unsigned pose=0;pose<6;pose++)
    {
        auto const &p=shang_drain_poses[pose];
        unsigned const descriptor=shang_drain_descriptors+pose*20;
        write16(descriptor,p.width); write16(descriptor+2,p.height);
        write16(descriptor+4,uint16_t(p.x)); write16(descriptor+6,uint16_t(p.y));
        write32(descriptor+8,p.graphics); write16(descriptor+12,0x6000);
        write32(descriptor+14,native_address(shang_drain_palettes[0][pose/3]));
        write16(descriptor+18,0);
        write32(shang_drain_groups+pose*8,native_address(descriptor));
        write32(shang_drain_groups+pose*8+4,0);
    }
    for (unsigned fighter=0;fighter<2;fighter++)
    {
        uint32_t const a=native_address(shang_drain_groups+fighter*24);
        uint32_t const b=a+64, c=a+128;
        uint32_t const script[]={a,b,c,0,b,a,b,c,0};
        for (unsigned word=0;word<std::size(script);word++)
            write32(shang_drain_streams[fighter]+word*4,script[word]);
        write32(shang_drain_primary+(17+fighter)*4,native_address(shang_drain_streams[fighter]));
        write32(shang_drain_secondary+(17+fighter)*4,native_address(shang_drain_palettes[1][fighter]));
    }
    // Stock caller's1C0 branch observes the PERFORMER, not the victim's own
    // costume. Limit the override to our four unique drain palettes AND true
    // victim17/18, then use that actual victim's flag6. Later shared skeleton
    // palettes and every stock caller retain the exact incoming A0 pointer.
    // Preserve scratch A1 and the original incoming status, replay the complete
    // original helper (real victim A8 / native palette cache / restore / return).
    unsigned shang_drain_cursor=shang_drain_palette_router;
    auto const shang_drain_code=[&](std::initializer_list<uint16_t> words) {
        if (shang_drain_cursor+words.size()*2>0xb1700)
            fatalerror("MK2KS: shrinking palette helper overflow");
        for (uint16_t word:words) { write16(shang_drain_cursor,word); shang_drain_cursor+=2; }
    };
    auto const shang_drain_movi=[&](uint32_t value) {
        shang_drain_code({0x09e0,uint16_t(value),uint16_t(value>>16)});
    };
    auto const shang_drain_branch=[&](uint16_t opcode) {
        unsigned const operand=shang_drain_cursor+2;
        shang_drain_code({opcode,0,0}); return operand;
    };
    shang_drain_code({0xa30f,0xb7a8,0x0140,0x01e0,0x098f,0x4000});
    unsigned shang_drain_matches[4];
    for (unsigned costume=0;costume<2;costume++)
        for (unsigned fighter=0;fighter<2;fighter++)
        {
            uint32_t const compare=~native_address(shang_drain_palettes[costume][fighter]);
            shang_drain_code({0x0b80,uint16_t(compare),uint16_t(compare>>16)});
            shang_drain_matches[costume*2+fighter]=shang_drain_branch(0xca80);
        }
    unsigned const shang_drain_not_ours=shang_drain_branch(0xc080);
    for (unsigned operand:shang_drain_matches) write32(operand,native_address(shang_drain_cursor));
    shang_drain_code({0xb501,0x01f0,0x0b41,0xffee});
    unsigned const shang_drain_kano=shang_drain_branch(0xca80);
    shang_drain_code({0x0b41,0xffed});
    unsigned const shang_drain_not_added=shang_drain_branch(0xcb80);
    shang_drain_movi(native_address(shang_drain_palettes[0][1]));
    shang_drain_code({0xb501,0x0160,0x1f21});
    unsigned const shang_drain_sonya_normal=shang_drain_branch(0xca80);
    shang_drain_movi(native_address(shang_drain_palettes[1][1]));
    unsigned const shang_drain_sonya_done=shang_drain_branch(0xc080);
    write32(shang_drain_kano,native_address(shang_drain_cursor));
    shang_drain_movi(native_address(shang_drain_palettes[0][0]));
    shang_drain_code({0xb501,0x0160,0x1f21});
    unsigned const shang_drain_kano_normal=shang_drain_branch(0xca80);
    shang_drain_movi(native_address(shang_drain_palettes[1][0]));
    for (unsigned operand:{shang_drain_not_ours,shang_drain_not_added,
            shang_drain_sonya_normal,shang_drain_sonya_done,shang_drain_kano_normal})
        write32(operand,native_address(shang_drain_cursor));
    shang_drain_code({0x09af,0x0002,0x01c0,0x0d5f,0x1090,0xff84,0x09af,0x0100,0x0960});
    write32(rom_offset(0xff8caff0),native_address(shang_drain_primary));
    write32(rom_offset(0xff8cb0f0),native_address(shang_drain_secondary));
    write16(rom_offset(0xff8cb410),0xc080);
    write32(rom_offset(0xff8cb420),native_address(shang_drain_palette_router));
    // SHANG_OWNED_DRAIN_END
'''


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def need(value, reason):
    if not value:
        raise ValueError(reason)


def main():
    need(not OUT.exists(), 'Never overwrite staged source evidence')
    assets = json.loads((ASSETS / 'asset-report.json').read_text())
    reservation = json.loads(RESERVATION.read_text())
    need(assets['passed'] and assets['formatRoundTrips'] == 6 and
         reservation['passed'] and reservation['nativeReservationAccepted'] and
         not assets['nativeRepairAccepted'] and not reservation['nativeRepairAccepted'],
         'Exact encoded owned artwork and actual whole native free reservations')
    need(all(sha(p) == h for p, h in assets['inputHashes'].items()) and
         all(sha(p) == h for p, h in assets['outputHashes'].items()) and
         all(sha(p) == h for p, h in reservation['inputHashes'].items()), 'All executed asset/native evidence immutable')
    stock_path = ROOT / 'mk2/mk2-maincpu.bin'
    stock = stock_path.read_bytes()
    tables = [struct.unpack_from('<17I', stock, (address - 0xff800000) // 8)
              for address in (0xff9d7770, 0xff9d8d70)]
    poses = [row for fighter in assets['fighters'] for row in fighter['frames']]
    pixels = (ASSETS / 'drain-six-bit.bin').read_bytes()
    need(len(pixels) == 25632 and sha(ASSETS / 'drain-six-bit.bin') == assets['packedSHA256'], 'Exact six-bit pixel blob')
    snippet = TEMPLATE.replace('@TABLES@', '\n'.join('        {' + ','.join(f'0x{v:08x}' for v in row) + '},' for row in tables))
    snippet = snippet.replace('@POSES@', '\n'.join('        {' + ','.join(str(row[k]) for k in
                              ('width', 'height', 'xOffset', 'yOffset', 'graphicsSourceBits')) + '},' for row in poses))
    snippet = snippet.replace('@PIXELS@', '\n'.join('        ' + ','.join(f'0x{b:02x}' for b in pixels[at:at+24]) + ','
                                                   for at in range(0, len(pixels), 24)))
    need('@TABLES@' not in snippet and '@POSES@' not in snippet and '@PIXELS@' not in snippet, 'All mechanical source fields expanded')
    pins = {str(p.resolve()): sha(p) for p in (Path(__file__), ASSETS / 'asset-report.json',
            ASSETS / 'drain-six-bit.bin', RESERVATION, stock_path,
            ROOT / 'tools/native_shang_owned_reaction.inc', ROOT / 'source_native_paired_stumble_table/midtunit_m.cpp')}
    OUT.mkdir()
    fragment = OUT / 'native_shang_owned_drain.inc'
    fragment.write_text(snippet)
    report = dict(passed=True, sourceGenerationOnly=True, fragmentSHA256=sha(fragment),
                  fragmentBytes=fragment.stat().st_size, pixelBytes=len(pixels),
                  exactNativeFreeReservationsReused=True, original17WordTablesPreserved=True,
                  normalAndAlternateOwnedPalettes=4, trueVictimIDs=[17,18],
                  nativeAnimationScriptWords=9, typedTerminatedComposites=6,
                  stockSkeletonHandoffUnchanged=True, inputHashes=pins,
                  wholeSourceCompilationStillRequired=True, nativeRepairAccepted=False,
                  artworkRuntimeAccepted=False, fullPortAcceptance=False, newEmulatorBuilds=0,
                  newROMCopies=0, newRawMedia=0, newZIPs=0, publicPlayableChanged=False, goalStatus='active')
    (OUT / 'generation-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(passed=True, fragment=str(fragment), bytes=report['fragmentBytes'], nativeRepairAccepted=False)))


if __name__ == '__main__':
    main()
