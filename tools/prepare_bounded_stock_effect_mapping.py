"""Contemporaneous all-actor FIFO and stock-source DMA mapping."""
import json
import verify_native_source_sync as sync
from prepare_bounded_stock_head_effect_census import TAIL

DMA=r'''
local mapping_dma=p:install_write_tap(0x01a80010,0x01a8001f,'stock effect mapping actual DMA',function(at,data)
 if not ready or frame-ready<59 or frame-ready>174 or at~=0x01a80010 then return end
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 local source=reg(2)|(reg(3)<<16)
 if not stock_effect_sources[source]then return end
 print(string.format('MK2_EFFECT_MAPPING_DMA frame=%d source=%08X width=%d height=%d x=%d y=%d command=%04X pc=%08X writes=0 assistance=none',frame,source,reg(6)&1023,reg(7)&1023,reg(4)&1023,reg(5)&511,data&65535,regs.PC.value))
end)
emu.register_stop(function()assert(mapping_dma)end)
'''

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_head_stock_effect_pixels_preparation'
    out=sync.ROOT/'audit_bounded_stock_effect_mapping_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()+TAIL+DMA
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    runner=(old/'run_sonya.ps1').read_text().replace(old.name,out.name)
    runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
    runner=runner.replace('audit_bounded_sonya_stock_head_stock_effect_pixels_runtime','audit_bounded_sonya_stock_effect_mapping_runtime')
    (out/'run_sonya.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
