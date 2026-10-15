"""One field: stream every visible opaque body-component pixel, no recording."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_large_rom_cross_throw_preparation'
    out=root/'audit_bounded_complete_throw_footprint_preparation';assert not out.exists()
    lua=(old/'prepared_observer.lua').read_text()
    needle='local idle_points={}';assert lua.count(needle)==1
    lua=lua.replace(needle,needle+'\nlocal footprint_stats={points=0,source_fail=0,display_fail=0,slots={0,0}}')
    needle='local yy=command&0x20~=0 and -y or y';assert lua.count(needle)==1
    lua=lua.replace(needle,needle+r'''
                if coverage_context and frame-ready==128 then
                 assert(command&15==2 and actual_dma[0]==0,'Complete unit-scale opaque copy scope')
                 local xx=command&0x10~=0 and -x or x
                 local dx,dy=(coverage_context.x+xx)&1023,(coverage_context.y+yy)&511
                 if dx<400 and dy<254 and dx>=actual_dma[16] and dx<=actual_dma[17] and dy>=actual_dma[12] and dy<=actual_dma[13] then
                  idle_points[#idle_points+1]={frame=frame,slot=coverage_context.slot,id=coverage_context.id,kind='body',fullbody=true,x=dx,y=dy,index=coverage_context.bank|pixel}
                 end
                end
''')
    needle="  if q.kind=='shadow' or q.kind=='body' then";assert lua.count(needle)==1
    lua=lua.replace(needle,r'''
  if q.fullbody then
   local index=q.all_index or q.cover_index or q.index
   local current=point_vram:read(q.y*512+q.x)&0x7fff
   local value=p:read_u16(0x01800000+index*16)
   local final=(expand((value>>10)&31)<<16)|(expand((value>>5)&31)<<8)|expand(value&31)
   footprint_stats.points=footprint_stats.points+1
   footprint_stats.slots[q.slot]=footprint_stats.slots[q.slot]+1
   if q.source_vram~=index or current~=index then footprint_stats.source_fail=footprint_stats.source_fail+1 end
   if actual~=final then footprint_stats.display_fail=footprint_stats.display_fail+1 end
  else
'''+needle)
    needle=' end\n idle_points={}\n shadow_queries={}';assert lua.count(needle)==1
    lua=lua.replace(needle,r'''
  end -- full footprint bypasses per-pixel logging
 end
 if footprint_stats.points>0 and not footprint_stats.reported then
  footprint_stats.reported=true
  log('COMPLETE_FOOTPRINT',string.format('source_age=128 points=%d slot1=%d slot2=%d source_fail=%d display_fail=%d raw_media=none',footprint_stats.points,footprint_stats.slots[1],footprint_stats.slots[2],footprint_stats.source_fail,footprint_stats.display_fail))
 end
 idle_points={}
 shadow_queries={}''')
    assert ':write_' not in lua
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_large_rom_cross_throw_runtime',
                              f'audit_bounded_{fighter}_complete_throw_footprint_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
