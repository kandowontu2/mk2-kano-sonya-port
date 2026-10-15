"""Sparse actual FIFO/DMA opaque bounds in the neutral two-human control."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_twohuman_idle_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    decoder=(root/'tools/prepare_bounded_native_stance_bounds_probe.py').read_text()
    decoder=decoder[decoder.index('local sole_gfx='):decoder.index('emu.register_frame_done(function()',decoder.index('local sole_gfx='))]
    marker='local idle_fifo= p:install_read_tap'
    assert lua.count(marker)==1
    lua=lua.replace(marker,decoder+'\nlocal idle_owned={}\n'+marker)
    marker="   log('IDLE_FIFO',string.format("
    assert lua.count(marker)==1
    lua=lua.replace(marker,r'''
   local size,xy,c=regs.A9.value,regs.A10.value,(regs.A12.value>>16)&0xffff
   local key=string.format('%d_%08X_%d_%d_%04X_%d_%d',frame,regs.A11.value,size&0x3ff,(size>>16)&0x3ff,c,xy&0x3ff,(xy>>16)&0x1ff)
   assert(not idle_owned[key]);idle_owned[key]={slot=slot,id=a.id,pose=a.pose}
'''+marker)
    lua+=r'''
local idle_dma=p:install_write_tap(0x01a80010,0x01a8001f,'actual idle body opaque bounds',function(at,data)
 if not ready or at~=0x01a80010 then return end
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 local src=reg(2)|(reg(3)<<16);local w,h=reg(6)&0x3ff,reg(7)&0x3ff
 local c,x,y=data&0xffff,reg(4)&0x3ff,reg(5)&0x1ff
 local key=string.format('%d_%08X_%d_%d_%04X_%d_%d',frame,src,w,h,c,x,y)
 local own=idle_owned[key];if not own then return end
 local count,top,bottom,bits=opaque_bounds(src,w,h,c)
 log('IDLE_OPAQUE',string.format('slot=%d id=%d pose=%08X source=%08X width=%d height=%d command=%04X x=%d y=%d opaque=%d top=%d bottom=%d endpoint=%d bits=%d scaleX=%d scaleY=%d clip12=%d clip13=%d config=%04X skip=%04X',
  own.slot,own.id,own.pose,src,w,h,c,x,y,count,top,bottom,(y+bottom)&511,bits,reg(10),reg(11),reg(12),reg(13),reg(15),reg(0)))
 idle_owned[key]=nil
end)
emu.register_stop(function()assert(idle_dma);local pending=0;for _ in pairs(idle_owned)do pending=pending+1 end;log('IDLE_OPAQUE_STOP','pending='..pending)end)
'''
    assert ':write_' not in lua and ':pixels(' not in lua
    out=root/'audit_bounded_twohuman_idle_opaque_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    runner=(old/'run.ps1').read_text().replace('audit_bounded_twohuman_sonya_kitana_idle_runtime','audit_bounded_twohuman_sonya_kitana_idle_opaque_runtime')
    runner=runner.replace(old.name,out.name).replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))
    print('Prepared sparse neutral opaque observer')

if __name__=='__main__':main()
