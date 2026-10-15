"""Independent narrow native palette patch assembly; not gameplay acceptance."""
import argparse, hashlib, json, struct, subprocess
from pathlib import Path
import verify_ball_register_source_v1837 as prior

ROOT = prior.ROOT
NAME = 'diagnostic_v2753_native_friendship_palette'
SOURCE = ROOT/'audit_v2752_native_friendship_palette_source/midtunit_m.cpp'
SOURCE_SHA = 'F509CC18D5C9CA4152508E52FEBA23B93A1B6C4085986E498F02C53E5BE7EABA'

def sha(path):
    return hashlib.file_digest(Path(path).open('rb'), 'sha256').hexdigest().upper()

def need(value, message):
    if not value: raise ValueError(message)

def address(offset): return 0xff800000 + offset*8
def offset(addr): return (addr-0xff800000)//8
def packed(*words): return struct.pack('<'+'H'*len(words), *words)

def expected():
    old, _, payload = prior.expected()
    guest = bytearray(old)
    need(old[0xfc500:0xfc800] == b'\xff'*0x300, 'Reserved native palette/router space was actually unused')
    donor = (0xfecdf710-0xfe800000)//8
    record = payload[donor:donor+34]
    need(struct.unpack_from('<H', record)[0] == 16, 'Genuine original sixteen-color palette record')
    guest[0xfc500:0xfc522] = record
    old_tail = packed(0xb541,0x0140,0x0b81,0x00ff,0x0000,0x09e0,0xf720,0xfecd,0x09e2,16,0,0x0d5f,0xc6b0,0xff80,0x0960)
    start = old.find(old_tail,0xf9e00,0xf9e80)
    need(start >= 0 and old.find(old_tail,start+1,0xf9e80) < 0, 'Exactly the redundant untracked bubble color upload')
    guest[start:start+len(old_tail)] = packed(0x0960)+b'\xff'*(len(old_tail)-2)
    cursor = 0
    limit = 0
    ends = {}
    def begin(at, end):
        nonlocal cursor, limit
        cursor, limit = at, end
    def emit(*words):
        nonlocal cursor
        data = packed(*words)
        need(cursor+len(data) <= limit, 'Native assembly fits independently reserved span')
        guest[cursor:cursor+len(data)] = data
        cursor += len(data)
    def movi(reg,value): emit(0x09e0+reg,value&65535,value>>16)
    def jump(op,target):
        operand = cursor+2
        emit(op,target&65535,target>>16)
        return operand
    def resolve(operand,target): struct.pack_into('<I',guest,operand,target)
    def call(target): jump(0x0d5f,target)
    begin(0xfc540,0xfc5c0)
    emit(0x01e0,0x0b60,0x08ef,0x0132)
    stock = jump(0xcb80,0)
    emit(0x01c0,0x098f,0x0400)
    movi(5,0); movi(0,address(0xfc500)); call(address(0xfc5c0))
    emit(0x09af,0x0020,0x0960)
    resolve(stock,address(cursor))
    emit(0x01c0); jump(0xc080,address(0xfc5c0))
    ends['allocatorRouter'] = cursor
    begin(0xfc5c0,0xfc600)
    emit(0x098f,0x7800,0x09c3,0x003c); jump(0xc080,0xff80cfa0)
    ends['originalPrologue'] = cursor
    begin(0xfc600,0xfc800)
    emit(0x01e0,0x098f,0xfffe,0x07a8,0xd480,0x0105)
    loop = address(cursor)
    emit(0x4d08); done = jump(0xca80,0)
    emit(0xb702,0x01d0,0x0b62,0xd9ef,0x0162); low = jump(0xc480,0)
    emit(0x0b62,0xd86f,0x0162); high = jump(0xc780,0)
    emit(0xb500,0x0140,0x0b80,0xff00,0xffff,0x4c01,0x24c1,0x0b21,0xbb30,0x0105,0x8620)
    complement = (~address(0xfc500)) & 0xffffffff
    emit(0x0b60,complement&65535,complement>>16); other = jump(0xcb80,0)
    emit(0xb420,0x0020); empty = jump(0xc680,0)
    emit(0xb500,0x0140); call(0xff80d580)
    for operand in (low,high,other,empty): resolve(operand,address(cursor))
    emit(0x8708); jump(0xc080,loop)
    resolve(done,address(cursor))
    emit(0x09af,0x7fff,0x01c0,0x5600,0x0580,0x19f0,0x0106)
    jump(0xc080,0xff83f0a0)
    ends['paletteRetirement'] = cursor
    for entry, target, original in (
        (0xff80cf60,0xfc540,packed(0x098f,0x7800,0x09c3,0x003c)),
        (0xff83f060,0xfc600,packed(0x5600,0x0580,0x19f0,0x0106))):
        at = offset(entry)
        need(old[at:at+8] == original, 'Exact complete native stolen prologue')
        guest[at:at+8] = packed(0xc080,address(target)&65535,address(target)>>16,0x0300)
    ranges = ((start,start+len(old_tail)),(offset(0xff80cf60),offset(0xff80cf60)+8),
              (offset(0xff83f060),offset(0xff83f060)+8),(0xfc500,0xfc800))
    changed = [i for i,(a,b) in enumerate(zip(old,guest)) if a != b]
    need(all(any(lo<=i<hi for lo,hi in ranges) for i in changed), 'Every other guest byte unchanged')
    return bytes(guest), old, payload, ends, ranges

def source_check():
    need(sha(SOURCE) == SOURCE_SHA, 'Exact independently reviewed unexecuted candidate source')
    oldpath = ROOT/prior.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
    old, new = oldpath.read_text(), SOURCE.read_text()
    original = '''\t// Group-object construction reserves its own palette, but does not load
\t// the MK3 component's optional palette tail. Queue the original 16 pens
\t// into that child's bank, never into Kano's or the opponent's body bank.
\tleg_code({0xb541,0x0140,0x0b81,0x00ff,0x0000});
\tleg_movi(0,0xfecdf720); leg_movi(2,16); leg_call(0xff80c6b0);
'''
    replacement = '''\t// The typed native palette allocation below queues the same original
\t// sixteen pens. No untracked overwrite of a stock palette cache bank.
'''
    first = new.index('\n\n\t// A real donor palette is not imported frame metadata.')
    last = new.index('\n}\n\n\nvoid midtunit_state::init_mk2ks_native_selector()',first)
    restored = (new[:first]+new[last:]).replace(replacement,original)
    need(old.count(original)==new.count(replacement)==1 and restored == old,
         'Entire candidate source is only explicit upload removal and typed native palette routers')
    return {str(oldpath):sha(oldpath),str(SOURCE):sha(SOURCE),str(Path(__file__)):sha(__file__)}

def verify(out):
    need(not out.exists(), 'Never overwrite evidence')
    pins = source_check()
    guest,old,payload,ends,ranges = expected()
    out.mkdir()
    binary = out/'native_patch_space.bin'
    binary.write_bytes(guest[0xfc500:0xfc800])
    listings = {}
    for tag,start in (('allocatorRouter',0xfc540),('originalPrologue',0xfc5c0),('paletteRetirement',0xfc600)):
        result = subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(binary),'-arch','tms34010',
                  '-skip',str(start-0xfc500),'-count',str((ends[tag]-start)*8),'-basepc',f'{address(start):X}'],
                  check=True,capture_output=True,text=True)
        listings[tag] = result.stdout
        (out/(tag+'.txt')).write_text(result.stdout)
    need('PUSHST' in listings['allocatorRouter'] and 'POPST' in listings['allocatorRouter'], 'Correct status-stack instructions')
    need('JALE' in listings['paletteRetirement'] and 'JAHI' not in listings['paletteRetirement'], 'Real disassembler confirms no-reference guard')
    need('ANDI   FFh,A0' in listings['paletteRetirement'], 'Actual low-byte palette index mask')
    need('CALLA  FF80D580h' in listings['paletteRetirement'] and 'A0-A14' in listings['paletteRetirement'], 'Native release with all original caller registers saved')
    pins[str(ROOT/'mame-mkp/unidasm.exe')] = sha(ROOT/'mame-mkp/unidasm.exe')
    report = dict(passed=True,sourceOnly=True,gameplayAcceptance=False,candidate=NAME,
                  sourceDeltaExactlyTwoChanges=True,independentlyAssembledExpectedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
                  paletteAddress=f'{address(0xfc500):08X}',paletteColorsUnchanged=True,
                  assemblyEnds=ends,patchRanges=ranges,inputHashes=pins,fullPortAcceptance=False)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    verify(parser.parse_args().output)
