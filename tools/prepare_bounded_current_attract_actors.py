"""Continuous sparse actor pairs in genuine added-character CPU demo windows."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_attract_long_preparation'
out=sync.ROOT/'audit_bounded_current_attract_actors_preparation';assert not out.exists()
source=(old/'attract.lua').read_text()
source+='''
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
 {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
emu.register_frame_done(function()
 if p:read_u16(0x010601d0)~=1 then return end
 local r1,r2=p:read_u16(slots[1].roster),p:read_u16(slots[2].roster)
 if r1~=17 and r1~=18 and r2~=17 and r2~=18 then return end
 for n,s in ipairs(slots)do
  local a,m=p:read_u32(s.actor),p:read_u32(s.main)
  if valid(a)and valid(m)then
   log('DEMO_ACTOR',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d pose=%08X y=%d floor=%d',
    n,a,m,p:read_u32(m+0xc0),p:read_u16(a+0x1f0),p:read_u16(s.roster),p:read_u16(s.state),p:read_u16(s.hp),p:read_u32(a+0x1d0),p:read_i16(a+0xb0),p:read_i16(m+0x200)))
  else log('DEMO_MISSING',string.format('slot=%d actor=%08X main=%08X roster=%d',n,a,m,p:read_u16(s.roster)))end
 end
end)
'''
out.mkdir();lua=out/'attract.lua';lua.write_text(source)
runner=(old/'run.ps1').read_text()
runner=runner.replace(old.name+'/attract.lua',out.name+'/attract.lua').replace(sync.sha(old/'attract.lua'),sync.sha(lua))
runner=runner.replace('audit_bounded_current_attract_long_runtime','audit_bounded_current_attract_actors_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared natural24000field attract actor trace, unchanged resource limits; no media')
