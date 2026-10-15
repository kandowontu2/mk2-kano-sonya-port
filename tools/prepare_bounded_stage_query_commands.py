"""Observe exact seven saved stage-gap coordinates before/after native draws."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_aerial_all_query_preparation'
    report=json.loads((root/'audit_bounded_aerial_all_query_checked/report.json').read_text())
    lua=(old/'prepared_observer.lua').read_text()
    targets={k:[(int(r['source_frame']),int(r['dma_x']),int(r['dma_y'])) for r in v['unresolvedStageDrawPredictions']] for k,v in report['results'].items()}
    rows='\n'.join(" ['"+name+"']={"+','.join('{'+','.join(map(str,p))+'}' for p in values)+'},' for name,values in targets.items())
    lua+=r'''
local stage_targets={
'''+rows+r'''
}
local stage_name=spec[1]==17 and 'kano' or 'sonya'
local stage_dma_item=nil
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_dma_register$')then assert(not stage_dma_item);stage_dma_item=emu.item(index)end
end end
assert(stage_dma_item and stage_dma_item.size==2)
local stage_pending={}
local function complete_stage_pending()
 for _,r in ipairs(stage_pending)do
  local after=point_vram:read(r.y*512+r.x)&32767
  if r.candidate or r.before~=after then
   log('STAGE_QUERY_COMMAND',string.format('query_frame=%d x=%d y=%d before=%d after=%d changed=%d candidate=%d pc=%08X source=%08X raw_data=%04X mask=%04X merged_command=%04X origin_x=%d origin_y=%d width=%d height=%d scaleX=%d scaleY=%d palette=%04X color=%04X skip=%04X top=%d bottom=%d left=%d right=%d',
    r.frame,r.x,r.y,r.before,after,r.before~=after and 1 or 0,r.candidate and 1 or 0,r.pc,r.source,r.data,r.mask,r.command,r.dx,r.dy,r.w,r.h,r.scaleX,r.scaleY,r.palette,r.color,r.skip,r.top,r.bottom,r.left,r.right))
  end
 end
 stage_pending={}
end
local stage_query_tap=p:install_write_tap(0x01a80010,0x01a8001f,'native stage seven-point command effects',function(at,data,mask)
 if at~=0x01a80010 then return end
 complete_stage_pending()
 local old=stage_dma_item:read(1);local c=(old&(~mask&65535))|(data&mask&65535)
 if c&0x8000==0 then return end
 local function reg(n)return stage_dma_item:read(n)end
 local src=reg(2)|(reg(3)<<16);local dx,dy=reg(4)&1023,reg(5)&511;local w,h=reg(6)&1023,reg(7)&1023
 for _,q in ipairs(stage_targets[stage_name])do
  if q[1]==frame then
   local x,y=q[2],q[3]
   local sx=c&16~=0 and((dx-x)&1023)or((x-dx)&1023)
   local sy=c&32~=0 and((dy-y)&511)or((y-dy)&511)
   stage_pending[#stage_pending+1]={frame=frame,x=x,y=y,before=point_vram:read(y*512+x)&32767,candidate=sx<w and sy<h,
    source=src,pc=regs.PC.value,data=data&65535,mask=mask&65535,command=c,dx=dx,dy=dy,w=w,h=h,
    scaleX=reg(10),scaleY=reg(11),palette=reg(8),color=reg(9),skip=reg(0),top=reg(12)&511,bottom=reg(13)&511,left=reg(16)&1023,right=reg(17)&1023}
  end
 end
end)
emu.register_frame_done(complete_stage_pending)
emu.register_stop(function()assert(stage_query_tap)end)
'''
    out=root/'audit_bounded_stage_query_commands_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_aerial_all_query_runtime',f'audit_bounded_{fighter}_stage_query_commands_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,passiveCoordinates=targets,observerSha=sync.sha(target))))

if __name__=='__main__':main()
