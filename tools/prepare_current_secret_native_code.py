"""Bounded current loaded secret-code comparison; never force a secret encounter."""
import json
import struct
import verify_native_source_sync as sync

sync.verify()
base = sync.ROOT / 'audit_current_ending_asset_tables_preparation'
out = sync.ROOT / 'audit_current_secret_native_code_preparation'
assert not out.exists()
stock_path = sync.ROOT / 'mk2/mk2-maincpu.bin'
stock = stock_path.read_bytes()
intervals = [(0xffa19fd0, 0xffa1a610), (0xffa1bda0, 0xffa1c5f0),
             (0xffa0ba10, 0xffa0baf0), (0xff836650, 0xff836750),
             (0xff8258b0, 0xff8259a0), (0xff9decb0, 0xff9defa0),
             (0xff9037c0, 0xff9037f0), (0xff904ee0, 0xff905020)]
source = (base / 'attract.lua').read_text()
source += '\nemu.register_frame_done(function()\n if frame~=600 then return end\n'
expected = []
for lo, hi in intervals:
    raw = stock[(lo - 0xff800000)//8:(hi - 0xff800000)//8]
    words = struct.unpack('<' + 'H' * (len(raw)//2), raw)
    source += (' do local at=0x%08x;local words={%s}\n' %
               (lo, ','.join('0x%04x' % w for w in words)))
    source += ''' local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches))
 assert(mismatches==0)
 end
'''
    expected.append(dict(at=f'{lo:08X}', words=str(len(words)), mismatches='0'))
predicates = []
for i, (site, reg, female, male) in enumerate([
        (0xff829c10, 3, 0xff829c40, 0xff829c70),
        (0xff8d9580, 2, 0xff8d95b0, 0xff8d95e0),
        (0xffa122a0, 2, 0xffa123b0, 0xffa122d0)]):
    target = 0xff800000 + (0xfe000 + i*0x20)*8
    words = [0x0b40+reg, 0xffef, 0xca06, 0x0b40+reg, 0xffed, 0xca03,
             0xc080, male & 0xffff, male >> 16, 0xc080, female & 0xffff, female >> 16]
    source += ''' do
 local site=0x%08x;local target=0x%08x
 assert(p:read_u16(site)==0xc080 and p:read_u32(site+16)==target)
 local words={%s};local mismatches=0
 for i,w in ipairs(words)do if p:read_u16(target+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('SECRET_PREDICATE',string.format('site=%%08X target=%%08X words=%%d mismatches=%%d',site,target,#words,mismatches))
 assert(mismatches==0)
 end
''' % (site, target, ','.join('0x%04x' % w for w in words))
    predicates.append(dict(site=f'{site:08X}', target=f'{target:08X}', words='12', mismatches='0'))
source += 'end)\n'
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir()
lua = out / 'attract.lua'
lua.write_text(source)
runner = (base / 'run.ps1').read_text().replace(base.name+'/attract.lua', out.name+'/attract.lua').replace(
    sync.sha(base / 'attract.lua'), sync.sha(lua)).replace(
    'audit_current_ending_asset_tables_runtime', 'audit_current_secret_native_code_runtime')
(out / 'run.ps1').write_text(runner)
(out / 'expected.json').write_text(json.dumps(dict(stockSHA256=sync.sha(stock_path),
    stockIntervals=expected, predicates=predicates), indent=2))
print('Prepared700fields; eight original intervals/three loaded predicates; no media or encounter forcing')
