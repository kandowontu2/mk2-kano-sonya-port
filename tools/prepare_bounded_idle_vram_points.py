"""Read only queried native VRAM words; no VRAM/framebuffer dump."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_idle_all_draw_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    marker='local idle_points={}';assert lua.count(marker)==1
    lua=lua.replace(marker,r'''
local point_vram=nil
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_local_videoram$')then assert(not point_vram);point_vram=emu.item(index)end
end end
assert(point_vram and point_vram.size==2 and point_vram.count>=512*512)
'''+marker,1)
    marker="   log('IDLE_ALL_DRAW_FINAL',string.format(";assert lua.count(marker)==1
    lua=lua.replace(marker,r'''
   local current=point_vram:read(q.y*512+q.x)&0x7fff
   local rgbword=p:read_u16(0x01800000+current*16)
   local vrgb=(expand((rgbword>>10)&31)<<16)|(expand((rgbword>>5)&31)<<8)|expand(rgbword&31)
   log('IDLE_VRAM_POINT',string.format('source_frame=%d slot=%d id=%d dma_x=%d dma_y=%d predicted=%d source_vram=%d display_vram=%d vram_rgb=%06X actual=%06X source_matches=%d display_matches=%d',
    q.frame,q.slot,q.id,q.x,q.y,index,q.source_vram or -1,current,vrgb,actual,q.source_vram==index and 1 or 0,vrgb==actual and 1 or 0))
'''+marker,1)
    lua+=r'''
emu.register_frame_done(function()
 for _,q in ipairs(idle_points)do
  if q.kind=='shadow' and q.frame==frame then q.source_vram=point_vram:read(q.y*512+q.x)&0x7fff end
 end
end)
'''
    out=root/'audit_bounded_idle_vram_points_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_idle_all_draw_runtime',f'audit_bounded_{fighter}_idle_vram_points_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
