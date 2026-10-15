"""Sparse cache-owned native floor-shadow DMA during physical campaign play."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_campaign_progress_core_preparation'
out=sync.ROOT/'audit_bounded_campaign_shadows_preparation';assert not out.exists();out.mkdir()
source=(old/'core.lua').read_text()
marker='emu.register_frame(function()\n';assert source.count(marker)==1
extra="""taps[#taps+1]=p:install_write_tap(0x01a80010,0x01a8001f,'campaign native floor shadows',function(at,data)
 if at~=0x01a80010 or frame%120~=0 or p:read_u16(0x010601d0)~=2 or (cpu.PC.value~=0xff8015a0 and cpu.PC.value~=0xff801610)then return end
 local row=cpu.A9.value
 local own,slot,cache
 for n=1,2 do
  local s=sample(n)
  if s and s.owner==s.actor then
   local c=p:read_u32(s.actor+0x1a0)
   if c>=0x01000000 and c<0x01100000 and row>=c and row<c+12*112 and (row-c)%112==0 and p:read_u32(row)~=0 then
    assert(not own,'Unique shadow cache owner');own,slot,cache=s,n,c
   end
  end
 end
 if not own then log('SHADOW_UNOWNED',string.format('row=%08X pc=%08X',row,cpu.PC.value));return end
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 local index=(reg(8)&0x7f00)|(reg(9)&255)
 log('SHADOW',string.format('slot=%d id=%d roster=%d actor=%08X main=%08X owner=%08X stage=%d row=%08X cache=%08X source=%08X graphic=%08X command=%04X palette_index=%04X color=%04X x=%d y=%d width=%d height=%d actor_y=%d floor=%d action=%d pc=%08X',slot,own.id,own.roster,own.actor,own.main,own.owner,p:read_u16(0x01061b30),row,cache,reg(2)|(reg(3)<<16),p:read_u32(row),data&0xffff,index,p:read_u16(0x01800000+index*16),reg(4)&0x3ff,reg(5)&0x1ff,reg(6)&0x3ff,reg(7)&0x3ff,own.y,own.floor,own.action,cpu.PC.value))
end)
"""
source=source.replace(marker,extra+marker)
lua=out/'shadows.lua';lua.write_text(source)
for fighter in ('kano','sonya'):
 for side in (1,2):
  runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
  runner=runner.replace(old.name+'/core.lua',out.name+'/shadows.lua').replace(sync.sha(old/'core.lua'),sync.sha(lua))
  runner=runner.replace(f'audit_bounded_campaign_progress_core_{fighter}_p{side}_runtime',f'audit_bounded_campaign_shadows_{fighter}_p{side}_runtime')
  (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,passiveShadowDMASamplingEveryFields=120,physicalInputsUnchanged=True,rawMedia=False)))
