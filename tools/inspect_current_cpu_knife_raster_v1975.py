"""Exact v1231 replay plus the unchanged source-bound v1716 scaling routine.

The underlying unit-scale decoder, CPU writes, latches and body/shadow masks
are unmodified. Only real non-unit DMA commands use the original integer
source iterator, which has independent fixed-point and compressed-row tests.
"""
import json
from pathlib import Path
import inspect_secondary_display_v1231 as base
import inspect_native_scaled_arena_v1716 as scaling
import verify_current_interrupt_v1870 as launch

HEX=base.HEX;data=base.data
class Replay(base.Replay):
    def __init__(self,folder,groups,buffers,owners):
        super().__init__(folder,groups,buffers,owners);self.buffers=buffers
    scaled_dma=scaling.Replay.scaled_dma
    def dma(self,d):
        if d['width']and d['height']and(d['scaleX']not in(0,256)or d['scaleY']not in(0,256)):
            return self.scaled_dma(d)
        return super().dma(d)

def source(pins):
    path=launch.ROOT/'audit_v1718_scaled_raster_units_checked/report.json'
    proof=json.loads(path.read_text());assert proof['passed']and proof['independentScaleModeFlipCases']==108 and proof['exactCompressedUnitScaleRegressions']==16
    for file,wanted in proof['inputHashes'].items():assert launch.sha(file)==wanted;pins[file]=wanted
    build=json.loads((launch.ROOT/launch.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    wanted=[h for file,h in build['input_hashes'].items()if Path(file).name=='midtunit_v.cpp']
    assert len(wanted)==1 and launch.sha(launch.ROOT/'mame-mkp/src/mame/midway/midtunit_v.cpp')==wanted[0]
    pins[str(path)]=launch.sha(path)

# Extend the actual replay used by both complete-scene and continuous-erase
# functions. There is no fixture substitution, dropped command or scale bypass.
base.Replay=Replay
inspect=base.inspect
