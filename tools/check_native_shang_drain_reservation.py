"""Reconstruct current initialized guest/GFX before reserving new victim data.

Runs the unchanged frozen initializer providers, not an emulator or campaign.
Only small proof files and their temporary, retired compiler probe are created.
No ROM image, game state, executable candidate or public launcher is written.
"""
import hashlib
import inspect
import json
import struct
from pathlib import Path

import capture_native_paired_stumble_campaign as current

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_shang_drain_reservation'
OLD_INIT = ROOT / 'audit_native_shang_drain_reservation_previous_initializer'
INIT = ROOT / 'audit_native_shang_drain_reservation_current_initializer'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def need(value, reason):
    if not value:
        raise ValueError(reason)


def initialized():
    scope = dict(vars(current), __file__=__file__, OLD_INIT=OLD_INIT, INIT=INIT)
    source = inspect.getsource(current.expectation)
    exec(compile(source, __file__ + '::unchanged_complete_current_initializer', 'exec'), scope)
    return scope['expectation']()


def main():
    need(not OUT.exists() and not OLD_INIT.exists() and not INIT.exists(), 'Fresh reservation proof')
    guest, gfx, build, _ = initialized()
    need(len(guest) == 0x100000 and len(gfx) == 0x2000000, 'Entire current high guest and graphics windows')
    guest_hash = hashlib.sha256(guest).hexdigest().upper()
    need(guest_hash == '8234D0D3E25480018C3F4A68B5F5C8F24A1839F54E7887C260084D43E6B6C479',
         'Actual current paired-stumble initializer, not merely original ROM')
    need(guest[0xb1000:0xb2000] == b'\xff' * 0x1000, 'Whole proposed metadata/code reservation free')
    need(gfx[0x1fb0000:0x1fc0000] == bytes(0x10000), 'Whole proposed native six-bit graphics reservation free')
    original = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    tables = []
    for address in (0xff9d7770, 0xff9d8d70):
        at = (address - 0xff800000) // 8
        need(guest[at:at + 68] == original[at:at + 68], 'All17 effective original table words still intact')
        tables.append(dict(address=f'{address:08X}', words=[f'{w:08X}' for w in
                          struct.unpack_from('<17I', guest, at)]))
    for at in (0xfda00, 0xfdb00, 0xf1500, 0xf1600):
        need(struct.unpack_from('<HH', guest, at) == (65, 0), 'Owned native palette count/transparent entry')
    for opcode, pointer in ((0xff8cafe0, 0xff9d7770), (0xff8cb0e0, 0xff9d8d70)):
        at = (opcode - 0xff800000) // 8
        need(struct.unpack_from('<HI', guest, at) == (0x09e0, pointer), 'Exact original victim table MOVI boundary')
    helper = (0xff8cb410 - 0xff800000) // 8
    need(guest[helper:helper + 18] == bytes.fromhex('0fa3a8b740015f0d901084ffaf0900016009'),
         'Complete original victim palette helper, including save/restore/return')
    pins = dict(build['input_hashes'])
    for p in (Path(__file__), Path(current.__file__), Path(current.base.__file__),
              ROOT / current.NAME / 'build-info.json',
              ROOT / 'art_native_shang_drain_encoded_v1/asset-report.json',
              ROOT / 'art_native_shang_drain_encoded_v1/drain-six-bit.bin',
              ROOT / 'tools/native_shang_owned_reaction.inc'):
        pins[str(p.resolve())] = sha(p)
    need(all(sha(p) == h for p, h in pins.items()), 'Whole immutable initializer and asset inputs retained')
    OUT.mkdir()
    report = dict(passed=True, sourceOnlyAccepted=True, scope=__doc__,
                  currentGuestSHA256=guest_hash,
                  currentGFXSHA256=hashlib.sha256(gfx).hexdigest().upper(),
                  wholeGuestBytes=len(guest), wholeGFXBytes=len(gfx),
                  programReservation=[0xb1000, 0xb2000], graphicsReservation=[0x1fb0000, 0x1fc0000],
                  entireReservationActuallyFree=True, original17WordTables=tables,
                  secondaryValidOriginalPlayableRows=12,
                  originalSecondaryTrailingWordsPreservedWithoutCallingThemPalettes=True,
                  inputHashes=pins, nativeRepairAccepted=False, fullPortAcceptance=False,
                  gameWrites=0, newEmulatorBuilds=0, newROMCopies=0, newRawMedia=0,
                  newZIPs=0, publicPlayableChanged=False, goalStatus='active')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(passed=True, sourceOnlyAccepted=True, currentGuestSHA256=guest_hash,
                         entireReservationActuallyFree=True, nativeRepairAccepted=False)))


if __name__ == '__main__':
    main()
