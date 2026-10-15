"""Transient RGB point checks; no retained framebuffer or media files."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_twohuman_idle_opaque_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    lua=lua.replace('local sole_gfx=', 'local idle_points={}\nlocal sole_gfx=',1)
    lua=lua.replace('local count,low,high=0,nil,nil','local count,low,high=0,nil,nil\n    local point_x,point_pixel',1)
    lua=lua.replace('if take(bpp)~=0 then','local pixel=take(bpp)\n            if pixel~=0 then',1)
    marker='local yy=command&0x20~=0 and -y or y'
    assert lua.count(marker)==1
    lua=lua.replace(marker,marker+'\n                if not high or yy>high then point_x=command&0x10~=0 and -x or x;point_pixel=pixel end',1)
    lua=lua.replace('bit-mapped\nend','bit-mapped,point_x,point_pixel\nend',1)
    lua=lua.replace('local count,top,bottom,bits=opaque_bounds(src,w,h,c)','local count,top,bottom,bits,px,pixel=opaque_bounds(src,w,h,c)\n idle_points[#idle_points+1]={frame=frame,slot=own.slot,id=own.id,x=(x+px)&1023,y=(y+bottom)&511,index=(reg(8)&0x7f00)|pixel}',1)
    lua+=r'''
emu.register_frame_done(function()
 if #idle_points==0 then return end
 local control=p:read_u16(0xc0000080);local adr=p:read_u16(0xc00001e0)
 local veb,vsb=p:read_u16(0xc0000050),p:read_u16(0xc0000060)
 local effective=(adr+(vsb-veb)*(control&0x3fc))&65535
 local address=control&0x400~=0 and effective or effective~0xfffc
 local row=(address>>4)&511;local column=((((address&0x7c)<<4)|(p:read_u16(0xc00001b0)&0x3fff))*2)&511
 local raw,w,h=screen:pixels();assert(w==400 and h==254 and #raw==406400)
 for _,q in ipairs(idle_points)do
  local xx,yy=q.x-column,q.y-row
  local word=p:read_u16(0x01800000+q.index*16)
  local function expand(v)return (v<<3)|(v>>2)end
  local expected=(expand((word>>10)&31)<<16)|(expand((word>>5)&31)<<8)|expand(word&31)
  local actual=-1
  if xx>=0 and xx<w and yy>=0 and yy<h then actual=string.unpack('<I4',raw,(yy*w+xx)*4+1)&0xffffff end
  log('IDLE_SCANPOINT',string.format('source_frame=%d slot=%d id=%d dma_x=%d dma_y=%d display_x=%d display_y=%d row=%d column=%d effective=%04X dpyadr=%04X control=%04X veb=%d vsb=%d palette_index=%d expected=%06X actual=%06X match=%d',
   q.frame,q.slot,q.id,q.x,q.y,xx,yy,row,column,effective,adr,control,veb,vsb,q.index,expected,actual,actual==expected and 1 or 0))
 end
 idle_points={}
end)
'''
    assert ':write_' not in lua and ':snapshot(' not in lua
    out=root/'audit_bounded_idle_scanout_points_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter,move in (('sonya','ring'),('kano','knife')):
        runner=(old/'run.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace('audit_bounded_twohuman_sonya_kitana_idle_opaque_runtime',f'audit_bounded_{fighter}_idle_scanout_points_runtime')
        runner=runner.replace("MK2KS_HUMAN_SPECIAL_MOVE='ring'",f"MK2KS_HUMAN_SPECIAL_MOVE='{move}'")
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,retainedFramePixels=False,observerSha=sync.sha(target))))
    print('Prepared transient scalar scanout points')

if __name__=='__main__':main()
