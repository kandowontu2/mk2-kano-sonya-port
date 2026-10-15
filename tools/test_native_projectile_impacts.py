"""Full-component conversion, allocation and original runtime-reference tests."""
import re
import struct
import unittest
from pathlib import Path

import build_native_projectile_impacts as impact
import build_mk2ks_mk3 as animation
import upgrade_ksui_previews as decoder

ROOT=Path(__file__).resolve().parents[1]


class ImpactAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.program=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
        cls.base=(ROOT/'diagnostic_v291_native_projectile_core/roms/mk2ks/mk2ks.mdata').read_bytes()
        cls.payload=bytearray(cls.base)
        cls.report=impact.build(cls.payload,cls.program,ROOT/'mk3')
        cls.gfx=decoder.load_gfx(ROOT/'mk3')

    def test_exact_current_payload(self):
        self.assertEqual(self.payload,(ROOT/'diagnostic_v292_projectile_impact_payload/roms/mk2ks/mk2ks.mdata').read_bytes())
        self.assertEqual(self.report['component_count'],34)
        self.assertEqual(self.report['pixel_bytes'],56796)

    def test_only_reserved_space_and_own_dispatch_changes(self):
        allowed=set(range(impact.HEADER,impact.META_END))|set(range(impact.PIXELS,impact.END))
        allowed.update(i+j for i in self.report['pointer_cells'] for j in range(4))
        self.assertEqual(len(self.report['pointer_cells']),6)
        for i,(old,new) in enumerate(zip(self.base,self.payload)):
            if old!=new:self.assertIn(i,allowed)

    def test_all_donor_components_pixels_pivots_and_palettes(self):
        # Independent bit reader and raster decoder handle both skip-encoded
        # frames and raw tiny particles (the preview decoder assumes skips).
        def bits(data,at,n):return sum(((data[(at+i)//8]>>((at+i)%8))&1)<<i for i in range(n))
        for fighter in ('kano','sonya'):
            count=self.report[fighter]['palette_colors']
            for record in self.report[fighter]['components']:
                frame=int(record['source'],16);spec=decoder.component_spec(self.program,frame)
                source,command,w,h,xo,yo=spec
                at=(int(record['native'],16)-impact.BASE)//8
                nw,nh,nxo,nyo,pixels,dma,palette=struct.unpack_from('<4hIHI',self.payload,at)
                self.assertEqual((nw,nh,nxo,nyo,dma),(w,h,xo,yo,0x6000))
                cursor=source;expected=[]
                for y in range(h):
                    pre=post=0
                    if command&0x80:
                        skip=bits(self.gfx,cursor,8);cursor+=8
                        pre=(skip&15)<<((command>>8)&3);post=(skip>>4)<<((command>>10)&3)
                    row=[0]*w
                    for x in range(pre,max(pre,w-post)):
                        value=bits(self.gfx,cursor,6);cursor+=6
                        if x<w:row[x]=value
                    expected.extend(row)
                start=impact.PIXELS*8+pixels-impact.GFX_DEST*8
                actual=[bits(self.payload,start+i*6,6) for i in range(w*h)]
                self.assertEqual(actual,expected,record['source'])
                self.assertLess(max(actual),count)
                pal_at=(palette-impact.BASE)//8
                source_pal=animation.stock_file(0xffc96600 if fighter=='kano' else 0xffc973c0)
                colors=list(struct.unpack_from(f'<{count}H',self.program,source_pal+2));colors[0]=0
                self.assertEqual(struct.unpack_from('<H64H',self.payload,pal_at),(64,*(colors+[0]*(64-count))))

    def test_composites_and_sequences_complete(self):
        for index,fighter in enumerate(('kano','sonya')):
            info=self.report[fighter];groups=info['groups']
            self.assertEqual(len(groups),6+index)
            self.assertEqual(struct.unpack_from(f'<{len(groups)+1}I',self.payload,impact.SEQUENCES[index]),
                             (*(int(g['native'],16) for g in groups),0))
            for group in groups:
                original=animation.frame_group(self.program,int(group['source'],16),0xff800000,0xffffffff)
                self.assertEqual(len(group['components']),len(original))
                at=(int(group['native'],16)-impact.BASE)//8
                self.assertEqual(struct.unpack_from(f'<{len(original)+1}I',self.payload,at),(*group['components'],0))
            for cell in self.report['pointer_cells']:
                if ((cell-0x100000)//0x4000)%2==index:
                    self.assertEqual(animation.u32(self.payload,cell),int(info['sequence'],16))

    def test_original_input_only_pose_cadence_and_drift(self):
        for fighter,scenario in ((f,s) for f in ('kano','sonya') for s in ('hit','block')):
            kind='knife' if fighter=='kano' else 'ring'
            version=292 if scenario=='hit' else 295
            log=(ROOT/f'audit_v{version}_original_{kind}_impact_{scenario}/run.log').read_text(encoding='utf-8-sig')
            matches=re.findall(r'MK3_IMPACT_FIELD frame=(\d+) actor=([0-9A-F]+).*?x=(\d+) y=(\d+) pose=([0-9A-F]+)',log)
            first=next(r for r in matches if int(r[4],16)==impact.SOURCE_GROUPS[fighter][0])
            start=int(first[0]);actor=first[1]
            rows=[r for r in matches if r[1]==actor and start<=int(r[0])<start+4*len(impact.SOURCE_GROUPS[fighter])]
            self.assertEqual(len(rows),4*len(impact.SOURCE_GROUPS[fighter]))
            for i,row in enumerate(rows):
                self.assertEqual(int(row[4],16),impact.SOURCE_GROUPS[fighter][i//4])
                self.assertEqual(int(row[2]),int(first[2])+i*(2 if fighter=='sonya' else 0))
                self.assertEqual(row[3],first[3])
            self.assertIn('before=166 after='+('147' if scenario=='hit' else '163'),log)
            self.assertNotIn('writes=1',log)

    def test_occupied_allocations_fail_without_mutation(self):
        for offset in (impact.HEADER,impact.FRAMES,impact.PIXELS,impact.END-1):
            payload=bytearray(self.base);payload[offset]=0;snapshot=bytes(payload)
            with self.assertRaisesRegex(ValueError,'occupied'):impact.build(payload,self.program,ROOT/'mk3')
            self.assertEqual(payload,snapshot)

    def test_wrong_prior_dispatch_fails_without_mutation(self):
        payload=bytearray(self.base);struct.pack_into('<I',payload,self.report['pointer_cells'][0],0)
        snapshot=bytes(payload)
        with self.assertRaisesRegex(ValueError,'dispatch'):impact.build(payload,self.program,ROOT/'mk3')
        self.assertEqual(payload,snapshot)


if __name__=='__main__':unittest.main()
