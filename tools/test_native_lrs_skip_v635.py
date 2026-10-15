"""Native scenery LRSKIP source/destination contract using observed arena data."""
import re
import unittest
from pathlib import Path
import numpy as np
from inspect_natural_arena_floor_v635_v3 import Replay
from verify_native_ui_flow_v635 import ROOT


class NativeColumnSkip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.buffer=None
        with (ROOT/'audit_v643_native_floor_kano_p2/run.log').open(encoding='utf-8-sig')as stream:
            for line in stream:
                if 'FLOOR_GFX 'in line and 'key=046B4F3B_E042_98_61 'in line:
                    cls.buffer=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    cls.buffer['offset']=int(cls.buffer['offset'])
                    break
        assert cls.buffer is not None,'Actual native scenery source is required'

    def compare(self,skip,flip=False):
        command=0xe042|(16 if flip else 0)
        key=f'046B4F3B_{command:04X}_98_61'
        replay=Replay(Path('.'),{'FLOOR_BASE':[]}, {key:self.buffer},{})
        replay.words=np.full((512,512),0xaabb,dtype=np.uint16)
        replay.body=np.zeros((512,512),dtype=np.uint8)
        replay.shadow=np.zeros((512,512),dtype=bool)
        d=dict(source=0x046b4f3b,command=command,width=98,height=61,skip=skip,
               x=180,y=314,scaleX=256,scaleY=256,left=0,right=511,top=256,bottom=509,
               palette=0x400,color=0,slot=0)
        replay.dma(d)
        raw=bytes.fromhex(self.buffer['data'])
        bit=self.buffer['offset']%8
        expected=np.full((512,512),0xaabb,dtype=np.uint16)
        start,end=skip&255,skip>>8
        for y in range(61):
            destx=180
            for x in range(98):
                at=bit+(y*98+x)*6
                pen=(int.from_bytes(raw[at//8:at//8+2],'little')>>(at%8))&63
                if start<=x<98-end:
                    if pen:expected[314+y,destx]=0x400|pen
                    destx+=-1 if flip else 1
        self.assertTrue(np.array_equal(expected,replay.words))

    def test_native_startskip88_rebases_only_source(self):self.compare(88)
    def test_native_endskip74(self):self.compare(74<<8)
    def test_native_both_skips(self):self.compare((42<<8)|23)
    def test_native_startskip_xflip(self):self.compare(88,True)
    def test_native_both_skips_xflip(self):self.compare((42<<8)|23,True)


if __name__=='__main__':unittest.main()
