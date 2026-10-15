"""Full asset comparison and independently observed original-game timing.

These checks deliberately do NOT establish gameplay success for a new port EXE.
Runtime tests must additionally prove the scheduler, collision, rendering and
cleanup in both slots, then repeat through ending/restart transitions.
"""
import hashlib
import json
import re
import struct
import unittest
from pathlib import Path

import build_native_projectile_choreography as choreography
import build_native_projectiles as flight
import build_mk2ks_mk3 as animation
import upgrade_ksui_previews as decoder

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT/'diagnostic_v298_projectile_choreography_payload/roms/mk2ks/mk2ks.mdata'


def bits(data,at,n):
    return sum(((data[(at+i)//8]>>((at+i)%8))&1)<<i for i in range(n))


def original_pixels(gfx,spec):
    cursor,command,w,h,*_ = spec
    pixels = []
    for y in range(h):
        pre = post = 0
        if command&0x80:
            skip = bits(gfx,cursor,8);cursor += 8
            pre = (skip&15)<<((command>>8)&3);post = (skip>>4)<<((command>>10)&3)
        row = [0]*w
        for x in range(pre,max(pre,w-post)):
            pixel = bits(gfx,cursor,6);cursor += 6
            if x<w:row[x] = pixel
        pixels.extend(row)
    return pixels


def records(log,kind):
    result = []
    for line in log.splitlines():
        if line.startswith('MK3_CHOREO_'+kind+' '):
            fields = dict(re.findall(r'(\w+)=([^ ]+)',line))
            for key in fields:
                fields[key] = int(fields[key],16 if key in ('pc','actor','process','group','pose','action','vx','vy','flags') else 10)
            result.append(fields)
    return result


class ChoreographyAssets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.program = (ROOT/'mk3/mk3-maincpu.bin').read_bytes()
        cls.base = (ROOT/'diagnostic_v293_native_projectile_impacts/roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.payload = bytearray(cls.base)
        cls.report = choreography.build(cls.payload,cls.program,ROOT/'mk3')
        cls.gfx = decoder.load_gfx(ROOT/'mk3')

    def test_generated_payload_exact(self):
        self.assertEqual(self.payload,OUTPUT.read_bytes())
        self.assertEqual(self.report['component_count'],12)
        self.assertEqual(self.report['pixel_bytes'],6356)
        self.assertEqual(self.report['payload_sha256'],hashlib.sha256(self.payload).hexdigest())
        self.assertEqual(struct.unpack_from('<4s9I',self.payload,choreography.HEADER),
                         (b'KPJ1',0x1f4000,6356,0x1e60000,0xff610800,0xff610a00,
                          0xff610c00,0xff610f00,12,14))

    def test_preserves_every_unrelated_byte_and_all_impact_data(self):
        allowed = set(range(choreography.HEADER,choreography.META_END))|set(range(choreography.PIXELS,choreography.END))
        allowed.update(at+j for at in self.report['pointer_cells'] for j in range(4))
        self.assertEqual(len(self.report['pointer_cells']),12)
        for i,(old,new) in enumerate(zip(self.base,self.payload)):
            if old != new:self.assertIn(i,allowed)
        self.assertEqual(self.payload[0x1c1000:0x1c2000],self.base[0x1c1000:0x1c2000])
        self.assertEqual(self.payload[0x1e6000:0x1f4000],self.base[0x1e6000:0x1f4000])

    def test_every_intro_component_pixel_palette_and_pivot(self):
        for record in self.report['intro_components']:
            spec = decoder.component_spec(self.program,int(record['source'],16))
            _,_,w,h,xo,yo = spec
            at = (int(record['native'],16)-choreography.BASE)//8
            nw,nh,nxo,nyo,graphic,cmd,palette = struct.unpack_from('<4hIHI',self.payload,at)
            self.assertEqual((nw,nh,nxo,nyo,cmd,palette),(w,h,xo-100,yo-72,0x6000,0xff600800))
            self.assertEqual(graphic&7,0)
            pixel = choreography.PIXELS*8+graphic-choreography.GFX_DEST*8
            actual = [bits(self.payload,pixel+i*6,6) for i in range(w*h)]
            expected = original_pixels(self.gfx,spec)
            self.assertEqual(actual,expected,record['source'])
            self.assertEqual(hashlib.sha256(bytes(actual)).hexdigest(),record['pixel_sha256'])
            self.assertLess(max(actual),24)
        source_palette = animation.stock_file(0xffc96600)
        colors = list(struct.unpack_from('<24H',self.program,source_palette+2));colors[0] = 0
        self.assertEqual(struct.unpack_from('<H64H',self.payload,0x1c0100),(64,*(colors+[0]*40)))

    def test_full_body_and_intro_composites(self):
        for fighter in ('kano','sonya'):
            for phase in ('body','intro'):
                for group in self.report[fighter][phase]:
                    source = animation.frame_group(self.program,int(group['source'],16),0xff800000,0xffffffff)
                    self.assertEqual(len(group['components']),len(source))
                    at = (int(group['native'],16)-choreography.BASE)//8
                    self.assertEqual(struct.unpack_from(f'<{len(source)+1}I',self.payload,at),(*group['components'],0))
        self.assertEqual([len(g['components']) for g in self.report['kano']['intro']],[2,1,2,3,2,2])
        self.assertEqual(self.report['sonya']['intro'],[])
        self.assertEqual(len(self.report['kano']['body']),8)
        self.assertEqual(len(self.report['sonya']['body']),5)

    def test_all_fourteen_existing_travel_frames_match_original_pixels(self):
        for fighter in ('kano','sonya'):
            for group in self.report[fighter]['flight']:
                source = animation.frame_group(self.program,int(group['source'],16),0xff800000,0xffffffff)[0]
                spec = decoder.component_spec(self.program,source)
                at = (group['components'][0]-choreography.BASE)//8
                w,h,xo,yo,graphic,cmd,palette = struct.unpack_from('<4hIHI',self.payload,at)
                self.assertEqual((w,h),spec[2:4])
                self.assertEqual((xo,yo),(spec[4]-100,spec[5]-72) if fighter == 'kano' else spec[4:])
                pixel = flight.PIXELS*8+graphic-flight.GFX_DEST*8
                self.assertEqual([bits(self.payload,pixel+i*6,6) for i in range(w*h)],original_pixels(self.gfx,spec))

    def test_native_sequences_have_full_cycle_and_token_one_loop(self):
        for index,fighter in enumerate(('kano','sonya')):
            info = self.report[fighter]
            body = [int(g['native'],16) for g in info['body']]
            self.assertEqual(struct.unpack_from(f'<{len(body)+1}I',self.payload,choreography.BODY_SEQUENCES[index]),(*body,0))
            intro = [int(g['native'],16) for g in info['intro']]
            travel = [int(g['native'],16) for g in info['flight']]
            expected = [*(intro or [travel[0]]),0,*travel,1,int(info['flight_sequence'],16),0]
            self.assertEqual(struct.unpack_from(f'<{len(expected)}I',self.payload,choreography.CHILD_SEQUENCES[index]),tuple(expected))
            self.assertEqual(len(set(travel)),10 if fighter == 'kano' else 4)
            self.assertFalse(info['bootstrap_is_held'])
            blocks = [animation.HYBRID_FILE_BASES[fighter]]+[b for n,b in animation.HYBRID_VARIANT_BASES.items() if n.startswith(fighter)]
            for block in blocks:
                self.assertEqual(animation.u32(self.payload,block+38*4),int(info['body_sequence'],16))
                self.assertEqual(animation.u32(self.payload,block+39*4),int(info['child_sequence'],16))

    def test_occupied_allocations_and_wrong_predecessor_fail_transactionally(self):
        for at in (choreography.HEADER,choreography.FRAMES,choreography.PIXELS,choreography.END-1):
            payload = bytearray(self.base);payload[at] = 0;snapshot = bytes(payload)
            with self.assertRaisesRegex(ValueError,'occupied'):choreography.build(payload,self.program,ROOT/'mk3')
            self.assertEqual(payload,snapshot)
        payload = bytearray(self.base);payload[123] ^= 1;snapshot = bytes(payload)
        with self.assertRaisesRegex(ValueError,'predecessor'):choreography.build(payload,self.program,ROOT/'mk3')
        self.assertEqual(payload,snapshot)

    def test_changed_original_body_asset_rejected_transactionally(self):
        program = bytearray(self.program);program[animation.stock_file(0xffb165d0)] ^= 1
        payload = bytearray(self.base)
        with self.assertRaisesRegex(ValueError,'body frame'):choreography.build(payload,program,ROOT/'mk3')
        self.assertEqual(payload,self.base)


class OriginalRuntimeChoreography(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.references = {}
        for fighter,kind in (('kano','knife'),('sonya','ring')):
            directory = ROOT/f'audit_v297_original_{kind}_release_full'
            result = json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))
            if result['exit_code'] != 0 or result['scope'] != 'original_MK3_read_only_reference' or not result['choreography']:
                raise AssertionError('not a terminal successful original-game run')
            for path,expected in result['input_hashes'].items():
                if Path(path).suffix.lower() in ('.lua','.ps1'):
                    frozen = directory/'input_sources'/Path(path).name
                    if hashlib.sha256(frozen.read_bytes()).hexdigest().upper() != expected:
                        raise AssertionError('original frozen source hash changed')
            source = (directory/'input_sources/mk3_projectile_choreography_reference.lua').read_text()
            source += (directory/'input_sources/mk3_knife_geometry_reference.lua').read_text()
            if re.search(r'\b(?:p|space):write_(?:u|s)(?:8|16|32|64)\b',source):
                raise AssertionError('original source contains a gameplay write')
            log = (directory/'run.log').read_text(encoding='utf-8-sig')
            cls.references[fighter] = (records(log,'GROUP'),records(log,'HUMAN'),records(log,'FIELD'),log)

    def test_complete_two_original_body_releases_and_recovery(self):
        for fighter,(groups,humans,fields,log) in self.references.items():
            body_groups = choreography.BODY_GROUPS[fighter]
            starts = [r for r in groups if r['body'] and r['group'] == body_groups[0]]
            self.assertEqual(len(starts),2)
            for start in starts:
                age = start['frame'];timing = choreography.TIMING[fighter]
                body = [r for r in groups if r['body'] and age <= r['frame'] < age+60]
                self.assertEqual([r['group'] for r in body],list(body_groups))
                expected_ages = [0]
                for hold in timing['body_holds'][:-1]:expected_ages.append(expected_ages[-1]+hold)
                self.assertEqual([r['frame']-age for r in body],expected_ages)
                human = {r['frame']:r for r in humans if age+1 <= r['frame'] < age+60}
                self.assertEqual(len(human),59)
                release = sum(timing['body_holds'])
                ready = age+release+timing['recovery_fields']+1
                for field in range(age+1,ready):
                    row = human[field]
                    self.assertEqual((row['id'],row['actor'],row['process'],row['writes']),
                                     (0 if fighter == 'kano' else 1,start['actor'],start['process'],0))
                    self.assertEqual((row['x'],row['y'],row['vx'],row['vy']),
                                     (start['x'],start['y'],0,0))
                    self.assertEqual(row['action'],(1 if fighter == 'kano' else 2) if field<=age+release else 0x604)
                    pose = next(g['group'] for g in reversed(body) if g['frame']<field)
                    self.assertEqual(row['pose'],pose)
                self.assertEqual(human[ready]['action'],0x303)
                self.assertEqual(human[ready]['pose'],body_groups[-1])
                self.assertNotEqual(human[ready+1]['pose'],body_groups[-1])

    def test_original_knife_six_intro_poses_then_ten_one_field_rotations(self):
        groups,humans,fields,log = self.references['kano']
        for start in [r for r in groups if r['body'] and r['group'] == 0xff82f400]:
            age = start['frame']
            intro = [r for r in groups if not r['body'] and age<=r['frame']<age+22 and
                     r['process'] != start['process']]
            self.assertEqual([r['group'] for r in intro],list(choreography.INTRO_SOURCE_GROUPS))
            self.assertEqual([r['frame']-age for r in intro],[3,6,9,12,15,18])
            self.assertTrue(all((r['x'],r['y'],r['vx'],r['vy']) == (start['x'],start['y'],0,0) for r in intro))
            flight_rows = [r for r in groups if not r['body'] and age+22<=r['frame']<age+42]
            self.assertEqual(len(flight_rows),20)
            self.assertEqual([r['group'] for r in flight_rows],list(choreography.FLIGHT_SOURCE_GROUPS['kano'])*2)
            for i,row in enumerate(flight_rows):
                self.assertEqual((row['frame']-age,row['x']-start['x'],row['y']-start['y'],row['vx'],row['vy']),
                                 (22+i,88+8*i,32,0x80000,0))
                self.assertEqual(row['actor'],intro[0]['actor'])
                self.assertNotEqual(row['process'],start['process'])

    def test_original_ring_no_stationary_intro_four_three_field_rotations(self):
        groups,humans,fields,log = self.references['sonya']
        for start in [r for r in groups if r['body'] and r['group'] == 0xff83dbe0]:
            age = start['frame']
            self.assertEqual([r for r in groups if not r['body'] and age<=r['frame']<age+16],[])
            travel = [r for r in groups if not r['body'] and age+16<=r['frame']<age+40]
            self.assertEqual([r['group'] for r in travel],list(choreography.FLIGHT_SOURCE_GROUPS['sonya'])*2)
            for i,row in enumerate(travel):
                self.assertEqual((row['frame']-age,row['x']-start['x'],row['y']-start['y'],row['vx'],row['vy']),
                                 (16+i*3,8+24*i,0,0x80000,0))
                self.assertNotEqual(row['actor'],start['actor'])
                self.assertNotEqual(row['process'],start['process'])

    def test_duck_reference_no_health_or_gameplay_write(self):
        for groups,humans,fields,log in self.references.values():
            self.assertNotIn('MK3_KNIFE_HEALTH',log)
            self.assertNotIn('writes=1',log)
            self.assertTrue(all(r['writes'] == 0 for r in groups+humans+fields))

    def test_each_original_held_child_field_and_one_field_handoff(self):
        for fighter,(groups,humans,fields,log) in self.references.items():
            first_body = choreography.BODY_GROUPS[fighter][0]
            for start in [r for r in groups if r['body'] and r['group'] == first_body]:
                age = start['frame']
                native_flight = [r for r in groups if not r['body'] and
                                 age <= r['frame'] < age+60 and
                                 r['group'] in choreography.FLIGHT_SOURCE_GROUPS[fighter]]
                actor = native_flight[0]['actor']
                child = {r['frame']:r for r in fields if not r['body'] and r['actor'] == actor and age<=r['frame']<age+60}
                if fighter == 'kano':
                    for i in range(18):
                        row = child[age+4+i]  # Frame callback precedes the group tap.
                        self.assertEqual((row['pose'],row['x'],row['y'],row['vx'],row['vy']),
                                         (choreography.INTRO_SOURCE_GROUPS[i//3],start['x'],start['y'],0,0))
                    # Original enables velocity while the old intro remains at
                    # the body origin. Position/first-flight rendering switch
                    # on the following field, NOT on the last intro field.
                    row = child[age+22]
                    self.assertEqual((row['pose'],row['x'],row['y'],row['vx'],row['vy']),
                                     (choreography.INTRO_SOURCE_GROUPS[-1],start['x'],start['y'],0x80000,0))
                    first = child[age+23]
                    self.assertEqual((first['pose'],first['x']-start['x'],first['y']-start['y']),
                                     (0xff82ee80,88,32))
                else:
                    for i in range(24):
                        row = child[age+17+i]
                        self.assertEqual((row['pose'],row['x']-start['x'],row['y']-start['y'],row['vx'],row['vy']),
                                         (choreography.FLIGHT_SOURCE_GROUPS['sonya'][(i//3)%4],8+8*i,0,0x80000,0))


if __name__ == '__main__':unittest.main()
