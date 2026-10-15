"""Execute staged C++ initializers and independently check all affected windows.

This is source/data qualification, not a full MAME build or native gameplay.
Full current high1MiB and owned low2MiB conservation is checked. GFX acceptance
is limited explicitly to the actual native-observed64KiB reservation; sentinel
bytes prove this new initializer does not touch the rest of a32MiB GFX region.
"""
import gzip
import hashlib
import inspect
import json
import re
import struct
import subprocess
from pathlib import Path

import capture_native_paired_stumble_campaign as current
import check_native_shang_owned_reaction_source as lead

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_shang_drain_source'
FRAGMENT = ROOT / 'source_native_shang_drain_fragment/native_shang_owned_drain.inc'
GENERATION = FRAGMENT.parent / 'generation-report.json'
ASSETS = ROOT / 'art_native_shang_drain_encoded_v1'
NATIVE = ROOT / 'audit_native_shang_drain_reservation_native'
COMPILER = Path('C:/Strawberry/c/bin/g++.exe')
PAL = ((0xb1200, 0xb12a0), (0xb1340, 0xb13e0))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def digest(data):
    return hashlib.sha256(data).hexdigest().upper()


def need(value, reason):
    if not value:
        raise ValueError(reason)


def addr(at):
    return 0xff800000 + at * 8


def off(address):
    need(0xff800000 <= address < 0x100000000 and address % 8 == 0, 'Typed high-program pointer')
    return (address - 0xff800000) // 8


def u32(data, at):
    return struct.unpack_from('<I', data, at)[0]


def independent_router():
    """Independent symbolic assembler, not a copy/extraction of compiled code."""
    words, labels, fixups = [], {}, []
    def emit(*values):
        words.extend(values)
    def branch(op, name):
        emit(op, 0, 0)
        fixups.append((len(words) - 2, name))
    def movi(value):
        emit(0x09e0, value & 65535, value >> 16)
    emit(0xa30f, 0xb7a8, 0x0140, 0x01e0, 0x098f, 0x4000)
    for value in [addr(at) for row in PAL for at in row]:
        inverse = (~value) & 0xffffffff
        emit(0x0b80, inverse & 65535, inverse >> 16)
        branch(0xca80, 'identity')
    branch(0xc080, 'done')
    labels['identity'] = len(words)
    emit(0xb501, 0x01f0, 0x0b41, 0xffee)
    branch(0xca80, 'kano')
    emit(0x0b41, 0xffed)
    branch(0xcb80, 'done')
    movi(addr(PAL[0][1]))
    emit(0xb501, 0x0160, 0x1f21)
    branch(0xca80, 'done')
    movi(addr(PAL[1][1]))
    branch(0xc080, 'done')
    labels['kano'] = len(words)
    movi(addr(PAL[0][0]))
    emit(0xb501, 0x0160, 0x1f21)
    branch(0xca80, 'done')
    movi(addr(PAL[1][0]))
    labels['done'] = len(words)
    emit(0x09af, 0x0002, 0x01c0, 0x0d5f, 0x1090, 0xff84, 0x09af, 0x0100, 0x0960)
    for at, name in fixups:
        target = addr(0xb1500 + labels[name] * 2)
        words[at:at + 2] = [target & 65535, target >> 16]
    return struct.pack('<' + str(len(words)) + 'H', *words)


def independent_guest(before, asset, pixels):
    after = bytearray(before)
    for table, original in ((0xb1000, 0xff9d7770), (0xb1060, 0xff9d8d70)):
        after[table:table + 68] = before[off(original):off(original) + 68]
    for costume, originals in enumerate(((0xfda00, 0xfdb00), (0xf1500, 0xf1600))):
        for fighter, old in enumerate(originals):
            at = PAL[costume][fighter]
            after[at:at + 132] = before[old:old + 132]
    for fighter, record in enumerate(asset['fighters']):
        groups = []
        for phase, row in enumerate(record['frames']):
            number = fighter * 3 + phase
            descriptor, group = 0xb10c0 + number * 20, 0xb1140 + number * 8
            struct.pack_into('<4hIHIH', after, descriptor, row['width'], row['height'],
                             row['xOffset'], row['yOffset'], row['graphicsSourceBits'],
                             0x6000, addr(PAL[0][fighter]), 0)
            struct.pack_into('<II', after, group, addr(descriptor), 0)
            groups.append(addr(group))
        a, b, c = groups
        stream = (0xb1180, 0xb11c0)[fighter]
        struct.pack_into('<9I', after, stream, a, b, c, 0, b, a, b, c, 0)
        struct.pack_into('<I', after, 0xb1000 + (17 + fighter) * 4, addr(stream))
        struct.pack_into('<I', after, 0xb1060 + (17 + fighter) * 4, addr(PAL[1][fighter]))
    code = independent_router()
    after[0xb1500:0xb1500 + len(code)] = code
    struct.pack_into('<I', after, off(0xff8caff0), addr(0xb1000))
    struct.pack_into('<I', after, off(0xff8cb0f0), addr(0xb1060))
    struct.pack_into('<HI', after, off(0xff8cb410), 0xc080, addr(0xb1500))
    need(len(after) == len(before) and len(pixels) == 25632, 'Whole high-program model size retained')
    return bytes(after), code


def run_router_model(code, incoming, ident, flags, original_status):
    """Bounded instruction model of ACTUAL compiled helper, not native CPU proof.

    The native palette-cache call itself is recorded, never simulated/accepted.
    Both the stock incoming args and true victim owner must reach that one call.
    """
    regs = {0: incoming, 1: 0x12345678, 8: 0x01034230, 13: 0x010757d0}
    victim = 0x01034020
    stack, z, status, pc, calls = [], False, original_status, 0, []
    def field(actor, displacement):
        need(actor == victim, 'Helper reads the actual victim, not performer')
        return {0x01f0: ident, 0x0160: flags}[displacement]
    for _ in range(100):
        op = struct.unpack_from('<H', code, pc)[0]
        if op == 0xa30f:
            stack.append(('a8', regs[8])); pc += 2
        elif op == 0xb7a8:
            need(struct.unpack_from('<H', code, pc + 2)[0] == 0x0140, 'Original real-victim field')
            regs[8] = victim; pc += 4
        elif op == 0x01e0:
            stack.append(('status', status)); pc += 2
        elif op == 0x098f:
            need(struct.unpack_from('<H', code, pc + 2)[0] == 0x4000, 'Save A1 only')
            stack.append(('a1', regs[1])); pc += 4
        elif op == 0x0b80:
            value = (~struct.unpack_from('<I', code, pc + 2)[0]) & 0xffffffff
            z = regs[0] == value; pc += 6
        elif op == 0x0b41:
            value = (~struct.unpack_from('<H', code, pc + 2)[0]) & 65535
            z = regs[1] == value; pc += 4
        elif op in (0xca80, 0xcb80, 0xc080):
            target = struct.unpack_from('<I', code, pc + 2)[0]
            taken = op == 0xc080 or (z if op == 0xca80 else not z)
            pc = off(target) - 0xb1500 if taken else pc + 6
            need(0 <= pc < len(code) and pc % 2 == 0, 'Bounded branch within actual helper')
        elif op == 0xb501:
            displacement = struct.unpack_from('<H', code, pc + 2)[0]
            regs[1] = field(regs[8], displacement); pc += 4
        elif op == 0x09e0:
            regs[0] = struct.unpack_from('<I', code, pc + 2)[0]; pc += 6
        elif op == 0x1f21:
            z = not bool(regs[1] & 64); pc += 2
        elif op == 0x09af:
            mask = struct.unpack_from('<H', code, pc + 2)[0]
            name, value = stack.pop()
            need((mask, name) in ((2, 'a1'), (256, 'a8')), 'Balanced original register restore')
            regs[1 if mask == 2 else 8] = value; pc += 4
        elif op == 0x01c0:
            name, status = stack.pop(); need(name == 'status', 'Balanced status restore'); pc += 2
        elif op == 0x0d5f:
            need(struct.unpack_from('<I', code, pc + 2)[0] == 0xff841090, 'One complete native palette helper, never substitute a cache operation')
            calls.append(dict(palette=regs[0], victim=regs[8], a1=regs[1], status=status)); pc += 6
        elif op == 0x0960:
            need(not stack and regs[8] == 0x01034230 and regs[1] == 0x12345678 and
                 status == original_status and len(calls) == 1, 'Balanced helper stack / performer restore / one native call')
            return calls[0]
        else:
            raise ValueError(f'Unexpected helper opcode {op:04X} at {pc}')
    raise ValueError('Unbounded helper model')


def harness(snippet):
    return r'''
#include <algorithm>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <initializer_list>
#include <iterator>
#include <stdexcept>
#include <vector>
#include <io.h>
#include <fcntl.h>
struct region {
    std::vector<uint8_t> data;
    uint8_t *base() { return data.data(); }
    unsigned bytes() const { return unsigned(data.size()); }
};
region main_region{{std::vector<uint8_t>(0x100000)}};
region low_region{{std::vector<uint8_t>(0x200000)}};
region graphics_region{{std::vector<uint8_t>(0x2000000,0x5a)}};
region *memregion(char const *name) {
    if (!std::strcmp(name,"maincpu")) return &main_region;
    if (!std::strcmp(name,"mk3data")) return &low_region;
    if (!std::strcmp(name,"gfxrom")) return &graphics_region;
    throw std::runtime_error("unexpected region");
}
void fatalerror(char const *reason) { throw std::runtime_error(reason); }
int main() {
    _setmode(_fileno(stdin),_O_BINARY); _setmode(_fileno(stdout),_O_BINARY);
    uint8_t *rom=main_region.base(), *donor=low_region.base(), *gfx=graphics_region.base();
    region *gfx_region=&graphics_region;
    std::cin.read(reinterpret_cast<char *>(rom),0x100000);
    std::cin.read(reinterpret_cast<char *>(donor),0x200000);
    std::cin.read(reinterpret_cast<char *>(gfx+0x1fb0000),0x10000);
    if (!std::cin) return 2;
    auto rom_offset=[](uint32_t value) { return (value-0xff800000U)/8; };
    auto native_address=[](unsigned at) { return 0xff800000U+at*8; };
    auto donor32=[&](unsigned at) { return uint32_t(donor[at])|(uint32_t(donor[at+1])<<8)|
        (uint32_t(donor[at+2])<<16)|(uint32_t(donor[at+3])<<24); };
    auto read16=[&](unsigned at) { return uint16_t(rom[at])|(uint16_t(rom[at+1])<<8); };
    auto read32=[&](unsigned at) { return uint32_t(rom[at])|(uint32_t(rom[at+1])<<8)|
        (uint32_t(rom[at+2])<<16)|(uint32_t(rom[at+3])<<24); };
    auto write16=[&](unsigned at,uint16_t value) { rom[at]=value;rom[at+1]=value>>8; };
    auto write32=[&](unsigned at,uint32_t value) { for (unsigned n=0;n<4;n++) rom[at+n]=value>>(n*8); };
    try {
''' + snippet + r'''
    } catch (std::exception const &error) {
        std::cerr<<error.what();return 5;
    }
    for (unsigned at=0;at<graphics_region.bytes();at++)
        if ((at<0x1fb0000 || at>=0x1fc0000) && gfx[at]!=0x5a) return 6;
    std::cout.write(reinterpret_cast<char *>(rom),0x100000);
    std::cout.write(reinterpret_cast<char *>(donor),0x200000);
    std::cout.write(reinterpret_cast<char *>(gfx+0x1fb0000),0x10000);
    return std::cout ? 0 : 3;
}
'''


def main():
    need(not OUT.exists(), 'Fresh combined source qualification')
    gen = json.loads(GENERATION.read_text())
    asset = json.loads((ASSETS / 'asset-report.json').read_text())
    native = json.loads((NATIVE / 'report.json').read_text())
    previous = json.loads((ROOT / 'audit_native_shang_owned_reaction_source/report.json').read_text())
    need(gen['passed'] and native['passed'] and previous['passed'] and
         sha(FRAGMENT) == gen['fragmentSHA256'] and
         all(sha(p) == h for r in (gen, asset, native, previous) for p, h in r['inputHashes'].items()),
         'All frozen source/format/native-reservation prerequisite hashes intact')
    OUT.mkdir()
    # Execute unchanged full current high-window factory in fresh proof dirs.
    scope = dict(vars(current), __file__=__file__,
                 OLD_INIT=OUT / 'previous_initializer', INIT=OUT / 'current_initializer')
    scope['OLD_INIT'].parent.mkdir(exist_ok=True)
    exec(compile(inspect.getsource(current.expectation), __file__ + '::unchanged_current_full_high_initializer', 'exec'), scope)
    before, limited_gfx, build, _ = scope['expectation']()
    need(len(before) == 0x100000 and digest(before) ==
         '8234D0D3E25480018C3F4A68B5F5C8F24A1839F54E7887C260084D43E6B6C479', 'Entire current high guest retained')
    need(len(limited_gfx) == 18976, 'Old GFX provider remains explicitly only its frozen-body slice')
    low = (ROOT / current.NAME / 'roms/mk2ks/mk2ks.mdata').read_bytes()
    lower, _ = lead.proposed_data(low)
    need(digest(lower) == previous['proposedOwnedWindowSHA256'], 'Exact independently checked eight-cell lead-in repair')
    pixels = (ASSETS / 'drain-six-bit.bin').read_bytes()
    after, code = independent_guest(before, asset, pixels)
    snippet = (ROOT / 'tools/native_shang_owned_reaction.inc').read_text() + '\n' + FRAGMENT.read_text()
    prior = (ROOT / 'source_native_paired_stumble_table/midtunit_m.cpp').read_text()
    anchor = '\t// PAIRED_STUMBLE_TABLE_END\n'
    need(prior.count(anchor) == 1 and 'SHANG_OWNED_DRAIN_BEGIN' not in prior, 'One additive successor source insertion')
    whole = prior.replace(anchor, anchor + snippet, 1)
    need(whole.replace(snippet, '', 1) == prior, 'Entire previous driver conserved outside the two additive fragments')
    cpp = harness(snippet)
    probe = OUT / 'initializer_probe.exe'
    compiled = subprocess.run([str(COMPILER), '-std=c++17', '-O1', '-Wall', '-Wextra', '-Werror',
                               '-x', 'c++', '-', '-o', str(probe)], input=cpp, text=True, capture_output=True)
    (OUT / 'compiler.log').write_text(compiled.stdout + compiled.stderr)
    need(compiled.returncode == 0 and not compiled.stdout and not compiled.stderr, 'Actual complete staged C++ initializer harness compiled warning-free')
    baseline = before + low + bytes(65536)
    result = subprocess.run([str(probe)], input=baseline, capture_output=True)
    need(result.returncode == 0 and not result.stderr and len(result.stdout) == len(baseline), 'Actual staged C++ initialization execution, whole affected windows')
    expected = after + lower + pixels + bytes(65536 - len(pixels))
    need(result.stdout == expected, 'Every high/owned/reservation byte equals independent source/art model')
    faults = []
    mutations = [('program_reservation', 0xb1000), ('last_program_reservation', 0xb1fff),
                 ('graphics_reservation', 0x300000), ('last_graphics_reservation', len(baseline)-1),
                 ('primary_operand', off(0xff8caff0)), ('secondary_operand', off(0xff8cb0f0)),
                 ('primary_opcode', off(0xff8cafe0)), ('secondary_opcode', off(0xff8cb0e0)),
                 ('helper_save', off(0xff8cb410)), ('helper_return', off(0xff8cb490))]
    for table, address in (('primary', 0xff9d7770), ('secondary', 0xff9d8d70)):
        mutations += [(table + '_row_' + str(row), off(address) + row * 4) for row in range(17)]
    mutations += [('palette_' + hex(at), at) for row in ((0xfda00, 0xfdb00), (0xf1500, 0xf1600)) for at in row]
    mutations += [('owned_root_' + str(i), 0x100000 + at + 56 * 4) for i, at in enumerate(lead.ROOTS)]
    for name, at in mutations:
        bad = bytearray(baseline); bad[at] ^= 1
        rejected = subprocess.run([str(probe)], input=bad, capture_output=True)
        need(rejected.returncode == 5 and rejected.stderr, 'Actual C++ must reject fault: ' + name)
        faults.append(name)
    probe.unlink()
    # Scope-limited instruction-level ownership/status/stack model. Stock
    # skeleton and all original playable palettes must bypass the new routing.
    stock = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    stock_palettes = list(struct.unpack_from('<12I', stock, off(0xff9d8d70)))
    skeleton_group = u32(stock, off(0xff9d8cf0))
    skeleton_frame = u32(stock, off(skeleton_group))
    skeleton_palette = u32(stock, off(skeleton_frame) + 14)
    incoming_values = [addr(at) for row in PAL for at in row] + stock_palettes + [skeleton_palette, 0x01234567]
    model_cases = 0
    for incoming in incoming_values:
        for ident in range(19):
            for flags in (0, 1, 63, 64, 65, 65535):
                status = (model_cases * 0x123457) & 0xffffffff
                call = run_router_model(code, incoming, ident, flags, status)
                wanted = addr(PAL[bool(flags & 64)][ident - 17]) if incoming in incoming_values[:4] and ident in (17, 18) else incoming
                need(call == dict(palette=wanted, victim=0x01034020, a1=0x12345678, status=status),
                     'Exact victim/costume routing OR byte-identical stock incoming pointer with balanced ABI')
                model_cases += 1
    # Inspect the actual compiled guest helper with the project's native
    # disassembler; count uses DECIMAL bit count and a small code-only file.
    code_path = OUT / 'palette-router-code.bin'
    code_path.write_bytes(code)
    disasm = subprocess.run([str(ROOT / 'mame-mkp/unidasm.exe'), str(code_path), '-arch', 'tms34010',
                             '-basepc', hex(addr(0xb1500)), '-count', str(len(code) * 8), '-norawbytes'],
                            capture_output=True, text=True)
    need(disasm.returncode == 0 and not disasm.stderr and len(disasm.stdout) < 20000 and
         disasm.stdout.count('PUSHST') == disasm.stdout.count('POPST') == 1 and
         disasm.stdout.count('CALLA  FF841090h') == 1 and 'RETS' in disasm.stdout and
         'ill' not in disasm.stdout.lower(), 'Bounded actual native instruction decode / one original palette call / status save-restore')
    (OUT / 'palette-router.disasm.txt').write_text(disasm.stdout)
    # Check both new primary entries resolve stream -> terminated composite
    # -> bounded6-bit bitmap, never the original composite-as-stream failure.
    rows = []
    for fighter in range(2):
        ident = 17 + fighter
        stream = u32(after, 0xb1000 + ident * 4)
        words = struct.unpack_from('<9I', after, off(stream))
        need(words[3] == words[8] == 0 and words[4:8] == (words[1], words[0], words[1], words[2]), 'Original complete 3-pose / 4-pose stream grammar')
        for phase, group in enumerate(words[:3]):
            descriptor, terminator = struct.unpack_from('<II', after, off(group))
            need(terminator == 0 and descriptor == addr(0xb10c0 + (fighter * 3 + phase) * 20), 'Typed single-bitmap terminated composite')
            w, h, x, y, bits, command, palette, zero = struct.unpack_from('<4hIHIH', after, off(descriptor))
            need(command == 0x6000 and palette == addr(PAL[0][fighter]) and zero == 0 and
                 h - y == (139, 140)[fighter] and 0x1fb0000 * 8 <= bits and
                 bits + w * h * 6 <= (0x1fb0000 + len(pixels)) * 8, 'Own palette and ground-anchored bounded bitmap')
        rows.append(dict(trueIdentity=ident, stream=f'{stream:08X}', scriptWords=[f'{v:08X}' for v in words],
                         secondaryPalette=f'{u32(after, 0xb1060 + ident * 4):08X}'))
    cause = json.loads((ROOT / 'audit_native_shang_actual_cache_cause_checked/report.json').read_text())
    pins = {str(p.resolve()): sha(p) for p in (Path(__file__), FRAGMENT, GENERATION, ASSETS / 'asset-report.json',
            ASSETS / 'drain-six-bit.bin', NATIVE / 'report.json', NATIVE / 'native-output.txt.gz',
            Path(current.__file__), Path(lead.__file__), ROOT / 'tools/native_shang_owned_reaction.inc',
            ROOT / 'audit_native_shang_owned_reaction_source/report.json', ROOT / 'mk2/mk2-maincpu.bin',
            ROOT / current.NAME / 'build-info.json', ROOT / current.NAME / 'roms/mk2ks/mk2ks.mdata',
            ROOT / 'source_native_paired_stumble_table/midtunit_m.cpp', COMPILER,
            ROOT / 'mame-mkp/unidasm.exe', ROOT / 'PLAY_LATEST_KANO_SONYA.cmd')}
    need(all(sha(p) == h for p, h in pins.items()) and not probe.exists(), 'Frozen sources and exact public playable unchanged; probe retired')
    with gzip.open(OUT / 'executed-harness.cpp.gz', 'wt', encoding='utf-8') as target:
        target.write(cpp)
    report = dict(passed=True, sourceOnlyAccepted=True, actualCppInitializerExit=result.returncode,
                  actualCompilerExit=compiled.returncode, actualCppFaultsRejected=faults,
                  helperInstructionModelCases=model_cases, helperInstructionModelNotNativeCPUAcceptance=True,
                  boundedNativeDisassemblerExit=disasm.returncode, paletteRouterBytes=len(code),
                  entireHighGuestConservedOutsideExactModel=True, wholeProposedGuestSHA256=digest(after),
                  wholeProposedOwnedWindowSHA256=digest(lower), proposedGraphicsReservationSHA256=digest(expected[-65536:]),
                  oldHighGuestSHA256=digest(before), changedHighGuestBytes=sum(a != b for a,b in zip(before,after)),
                  changedOwnedBytes=sum(a != b for a,b in zip(low,lower)),
                  fullCurrentGFXNotClaimed=True, outsideNewGFXWritesRejectedBySentinels=True,
                  additiveWholeDriverSHA256=digest(whole.encode()), sourceFragmentsOnly=True,
                  nativeDataRows=rows, viewedAuthoringPreviews=['native-size-preview.png','native-size-preview-3x.png'],
                  originalNaturalIntegrationRequirements=cause['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=cause['originalRemainingWorkGroups'],
                  inputHashes=pins, nativeRepairAccepted=False, artworkRuntimeAccepted=False,
                  fullPortAcceptance=False, originalCampaignStillFailed=True,
                  newEmulatorBuilds=0, newROMCopies=0, newRawGameplayMedia=0, newZIPs=0,
                  publicPlayableChanged=False, previousGoalTurnClassification='no progress: status only',
                  thisGoalTurnClassification='progress: encode all6 shrinking poses, actual native reservation proof, staged typed primary/secondary repair and compiled whole-window conservation/fault qualification',
                  nextAction='Build one complete successor from both fragments, verify BOTH initialized ROM windows and new GFX bytes, then replay the unchanged failing physical campaign and inspect real victim art/audio/choreography/cleanup. Full original14 requirements/six groups remain open.',
                  goalStatus='active')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(passed=True, sourceOnlyAccepted=True, actualCppFaultsRejected=len(faults),
                         helperInstructionModelCases=model_cases, wholeProposedGuestSHA256=digest(after),
                         nativeRepairAccepted=False, fullPortAcceptance=False)))


if __name__ == '__main__':
    main()
