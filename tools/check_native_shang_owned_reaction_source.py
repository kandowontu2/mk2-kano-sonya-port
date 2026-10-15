"""Qualify a staged lead-in repair, NOT the later drain or playable build.

All proposed source/data stays in memory; stdout is the only report output.
No ROM, game state, emulator, artwork, public launcher or release is written.
"""
import hashlib
import json
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAGMENT = ROOT / 'tools/native_shang_owned_reaction.inc'
PRIOR = ROOT / 'source_native_paired_stumble_table'
CAUSE = ROOT / 'audit_native_shang_actual_cache_cause_checked/report.json'
META = ROOT / 'diagnostic_native_paired_stumble_table_ps7/build-info.json'
BASE = 0xfe800000
ROOTS = (0x100000, 0x104000)
SCRIPTS = (0xff00b070, 0xff02b070)
RECOILS = (0xff013300, 0xff033420)
DIZZIES = (0xff011f60, 0xff0320c0)
CELLS = (24, 36, 48, 60)
XY = (0x001afff6, 0xfff80013, 0xffec0008, 0)


def need(value, text):
    if not value:
        raise ValueError(text)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def word(data, at):
    return struct.unpack_from('<I', data, at)[0]


def typed_original(data):
    """Independently model every actual pre-write guard in the C++ fragment."""
    need(len(data) == 0x200000, 'Whole immutable original owned window')
    rows = []
    for fighter, root in enumerate(ROOTS):
        script, dizzy = word(data, root + 56 * 4), word(data, root + 40 * 4)
        need(script == SCRIPTS[fighter] and BASE <= dizzy < 0xff800000 and not dizzy & 15,
             'Actual main56 and aligned owned main40 script roots')
        at = (script - BASE) // 8
        group = word(data, (dizzy - BASE) // 8)
        need(group == DIZZIES[fighter] and word(data, at) == 4 and
             word(data, at + 4) == 0xffedffb8 and word(data, at + 8) == RECOILS[fighter] and
             word(data, at + 12) == 0, 'Complete owned opening recoil and separator')
        for cell, xy in zip(CELLS, XY):
            need(word(data, at + cell - 8) == 4 and word(data, at + cell - 4) == xy and
                 word(data, at + cell) == 0xff9d7cb0, 'Original token4/XY/borrowed composite record')
        parts = []
        for i in range(8):
            frame = word(data, (group - BASE) // 8 + i * 4)
            if not frame:
                break
            need(BASE <= frame < 0xff7fff00 and not frame & 15,
                 'Owned composite contains bitmap descriptors, not a stream or proxy')
            desc = (frame - BASE) // 8
            w, h, x, y, graphics, command = struct.unpack_from('<4hIH', data, desc)
            need(0 < w <= 256 and 0 < h <= 256 and command >> 12 & 7 == 6,
                 'Actual native six-bit bitmap geometry')
            parts.append(dict(descriptor=f'{frame:08X}', width=w, height=h,
                              x=x, y=y, graphics=f'{graphics:08X}', command=f'{command:04X}'))
        else:
            raise ValueError('Composite has no bounded terminator')
        need(parts, 'Composite is not empty')
        rows.append(dict(identity=17 + fighter, root=f'{BASE + root * 8:08X}',
                         main56=f'{script:08X}', openingRecoilUnchanged=f'{RECOILS[fighter]:08X}',
                         ownDizzy=f'{group:08X}', descriptors=parts,
                         repairedCells=[f'{script + cell * 8:08X}' for cell in CELLS]))
    return rows


def proposed_data(original):
    rows = typed_original(original)
    after = bytearray(original)
    for fighter, script in enumerate(SCRIPTS):
        for cell in CELLS:
            struct.pack_into('<I', after, (script - BASE) // 8 + cell, DIZZIES[fighter])
    return bytes(after), rows


def conservation(original, proposed):
    exact, _ = proposed_data(original)
    need(proposed == exact, 'Every other owned-window byte and native command/XY conserved')
    return True


def main():
    cause = json.loads(CAUSE.read_text())
    meta = json.loads(META.read_text(encoding='utf-8-sig'))
    need(cause['passed'] and cause['nativeCauseAccepted'] and
         cause['actualBorrowedLiuVictimPoseBeforeLookup'] and
         cause['entireFailedCampaignRemainsFailed'] and not cause['nativeRepairAccepted'],
         'Actual four borrowed victim poses and later independent corruption remain recorded')
    payload = Path(meta['payload_hardlink_to_immutable_prior'])
    need(sha(payload) == meta['payload_sha256'] ==
         'A9A9DB228D4CF5FEA7E2A659AEF4D4407193FEE3D2F86E217F7F725D0D8E58D3',
         'Exact immutable complete current payload')
    need(meta['expected_guest_sha256'] ==
         '8234D0D3E25480018C3F4A68B5F5C8F24A1839F54E7887C260084D43E6B6C479',
         'Same current whole high-window guest; no implied primary-table fix')
    borrowed = cause['actualBorrowedPoseRecords']
    need(len(borrowed) == 4 and [r['a9'] for r in borrowed] ==
         [f'{SCRIPTS[1] + (cell + 4) * 8:08X}' for cell in CELLS] and
         all(r['a0'] == 'FF9D7CB0' and r['human_id'] == r['human_roster'] == '18'
             and r['cpu_id'] == r['cpu_roster'] == '6' and r['writes'] == '0'
             for r in borrowed), 'All four exact true18 victim cells independently bound')
    original = payload.read_bytes()
    proposed, rows = proposed_data(original)
    conservation(original, proposed)
    changed = [i for i, (a, b) in enumerate(zip(original, proposed)) if a != b]
    cells = [(s - BASE) // 8 + cell for s in SCRIPTS for cell in CELLS]
    need(all(any(at <= i < at + 4 for at in cells) for i in changed),
         'Only eight actual composite-pointer cells change')
    faults = []
    original_faults = [(f'root_{i}', root + 56 * 4) for i, root in enumerate(ROOTS)]
    original_faults += [(f'dizzy_root_{i}', root + 40 * 4) for i, root in enumerate(ROOTS)]
    for i, s in enumerate(SCRIPTS):
        original_faults += [(f'recoil_{i}', (s - BASE) // 8 + 8)]
        for j, c in enumerate(CELLS):
            original_faults += [(f'{kind}_{i}_{j}', (s - BASE) // 8 + c - back)
                                for kind, back in (('token', 8), ('alignment', 4), ('borrowed', 0))]
    for i, g in enumerate(DIZZIES):
        original_faults += [(f'dizzy_group_{i}', (g - BASE) // 8)]
        f = word(original, (g - BASE) // 8)
        original_faults += [(f'bitmap_width_{i}', (f - BASE) // 8)]
    for label, at in original_faults:
        bad = bytearray(original)
        if label.startswith('bitmap_width'):
            struct.pack_into('<H', bad, at, 0)
        else:
            bad[at] ^= 1
        try:
            typed_original(bad)
        except ValueError:
            faults.append(label)
        else:
            raise ValueError('Bad original accepted: ' + label)
    for j, at in enumerate(cells + [0]):
        bad = bytearray(proposed)
        bad[at] ^= 1
        try:
            conservation(original, bad)
        except ValueError:
            faults.append('wrong_proposed_cell_' + str(j))
        else:
            raise ValueError('Bad proposed owned data accepted')
    snippet = FRAGMENT.read_text()
    before = (PRIOR / 'midtunit_m.cpp').read_text()
    anchor = '\t// PAIRED_STUMBLE_TABLE_END\n'
    need(before.count(anchor) == 1 and 'SHANG_OWNED_REACTION_BEGIN' not in before,
         'One additive successor insertion; frozen previous source never edited')
    after = before.replace(anchor, anchor + '\n' + snippet, 1)
    need(after.replace('\n' + snippet, '', 1) == before,
         'Entire prior driver source conserved outside additive lead-in fragment')
    cpp = '''#include <cstdint>
struct region { unsigned bytes(); uint8_t *base(); };
region *memregion(char const *); void fatalerror(char const *);
void source_syntax_check() {
uint8_t const *donor = memregion("mk3data")->base();
auto const donor32 = [donor](unsigned at) {
return uint32_t(donor[at]) | (uint32_t(donor[at+1]) << 8) |
(uint32_t(donor[at+2]) << 16) | (uint32_t(donor[at+3]) << 24); };
''' + snippet + '\n}\n'
    compiler = Path('C:/Strawberry/c/bin/g++.exe')
    syntax = subprocess.run([str(compiler), '-std=c++17', '-Wall', '-Wextra', '-Werror',
                             '-fsyntax-only', '-x', 'c++', '-'], input=cpp,
                            capture_output=True, text=True)
    need(syntax.returncode == 0 and not syntax.stdout and not syntax.stderr,
         'Actual C++ fragment syntax-only compilation')
    paths = [Path(__file__), FRAGMENT, CAUSE, META, payload, compiler,
             *(PRIOR / name for name in ('midtunit.cpp', 'midtunit.h', 'midtunit_m.cpp')),
             ROOT / 'mk2/mk2-maincpu.bin', ROOT / 'mk3/mk3-maincpu.bin',
             ROOT / 'PLAY_LATEST_KANO_SONYA.cmd']
    pins = {str(p.resolve()): sha(p) for p in paths}
    need(len(cause['originalNaturalIntegrationRequirements']) == 14 and
         len(cause['originalRemainingWorkGroups']) == 6, 'Full original scope retained')
    result = dict(passed=True, stagedLeadInSourceAccepted=True,
                  candidate='diagnostic_native_paired_stumble_table_ps7',
                  nativeRepairAccepted=False, fullPortAcceptance=False,
                  primaryShrinkTableStillUnrepaired=True, secondaryPaletteTableStillUnrepaired=True,
                  originalCampaignStillFailed=True, artworkRuntimeAccepted=False,
                  previousGoalTurnClassification='no progress: requested status only',
                  thisGoalTurnClassification='progress: eight borrowed lead-in composite cells repaired in staged additive C++ source; complete source/data conservation and adversarial source tests',
                  actualCppSyntaxOnlyExit=syntax.returncode, sourceOnly=True,
                  repairedCompositeCells=8, changedOwnedDataBytes=len(changed),
                  proposedOwnedWindowSHA256=hashlib.sha256(proposed).hexdigest().upper(),
                  proposedFullDriverSourceSHA256=hashlib.sha256(after.encode()).hexdigest().upper(),
                  initializedHighWindowUnchangedSHA256=meta['expected_guest_sha256'],
                  rows=rows, faultRejections=faults, inputHashes=pins,
                  originalNaturalIntegrationRequirements=cause['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=cause['originalRemainingWorkGroups'],
                  nextAction='Complete character-owned three-phase shrinking artwork and typed native primary/secondary lookup rows; then build one successor and replay original physical inputs. Verify both initialized ROM windows and native rendered alignment, palette, choreography and cleanup.',
                  newEmulatorBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                  publicPlayableChanged=False, goalStatus='active')
    need(all(sha(p) == h for p, h in pins.items()), 'Every original and proposed source remains unchanged')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
