"""Resolve queried shadow points through later real owned body DMA pixels."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_idle_shadow_points_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    lua=lua.replace('local idle_points={}','local idle_points={}\nlocal shadow_queries={}\nlocal coverage_context=nil',1)
    marker='local yy=command&0x20~=0 and -y or y';assert lua.count(marker)==1
    lua=lua.replace(marker,marker+r'''
                if coverage_context then
                 local xx=command&0x10~=0 and -x or x
                 local key=string.format('%d_%d_%d',frame,(coverage_context.x+xx)&1023,(coverage_context.y+yy)&511)
                 for _,q in ipairs(shadow_queries[key]or{})do
                  q.cover_index=coverage_context.bank|pixel;q.cover_id=coverage_context.id;q.cover_slot=coverage_context.slot
                  q.cover_source=source;q.cover_sx=x;q.cover_sy=y;q.cover_pixel=pixel;q.cover_command=command;q.cover_pc=coverage_context.pc
                 end
                end
''',1)
    marker=' local count,top,bottom,bits,px,pixel=opaque_bounds(src,w,h,c)';assert lua.count(marker)==1
    lua=lua.replace(marker," coverage_context={x=x,y=y,bank=reg(8)&0x7f00,id=own.id,slot=own.slot,pc=regs.PC.value}\n"+marker+'\n coverage_context=nil',1)
    marker='  log(\'IDLE_SCANPOINT\',string.format(';assert lua.count(marker)==1
    lua=lua.replace(marker,r'''
  if q.kind=='shadow' then
   local index=q.cover_index or q.index
   local value=p:read_u16(0x01800000+index*16)
   local final=(expand((value>>10)&31)<<16)|(expand((value>>5)&31)<<8)|expand(value&31)
   log('IDLE_SHADOW_COVER',string.format('source_frame=%d slot=%d id=%d dma_x=%d dma_y=%d covered=%d cover_slot=%d cover_id=%d cover_source=%08X cover_sx=%d cover_sy=%d cover_pixel=%d cover_command=%04X cover_pc=%08X index=%d final=%06X actual=%06X match=%d',
    q.frame,q.slot,q.id,q.x,q.y,q.cover_index and 1 or 0,q.cover_slot or 0,q.cover_id or 0,q.cover_source or 0,q.cover_sx or -1,q.cover_sy or -1,q.cover_pixel or 0,q.cover_command or 0,q.cover_pc or 0,index,final,actual,final==actual and 1 or 0))
  end
'''+marker,1)
    lua=lua.replace(' idle_points={}\nend)',' idle_points={}\n shadow_queries={}\nend)',1)
    marker=" if count>0 then idle_points[#idle_points+1]={frame=frame,slot=slot,id=own.id,kind='shadow',x=(x+px)&1023,y=(y+bottom)&511,index=(reg(8)&0x7f00)|(reg(9)&255)}end"
    assert lua.count(marker)==1
    lua=lua.replace(marker,r'''
 if count>0 then
  local q={frame=frame,slot=slot,id=own.id,kind='shadow',x=(x+px)&1023,y=(y+bottom)&511,index=(reg(8)&0x7f00)|(reg(9)&255)}
  idle_points[#idle_points+1]=q
  local key=string.format('%d_%d_%d',frame,q.x,q.y)
  shadow_queries[key]=shadow_queries[key]or{};shadow_queries[key][#shadow_queries[key]+1]=q
 end
''',1)
    out=root/'audit_bounded_idle_shadow_coverage_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_idle_shadow_points_runtime',f'audit_bounded_{fighter}_idle_shadow_coverage_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target),rawMedia='none')))

if __name__=='__main__':main()
