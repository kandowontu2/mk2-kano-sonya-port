"""Sparse passive ring-child and native-damage linkage; ordinary inputs unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_ring_spacing_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_ring_hit_owner_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='for n,slot in ipairs(slots)do\n'
assert source.count(marker)==1
extra=r'''
local ring_children={}
local ring_entry=0xff800000+0xf8e00*8
taps[#taps+1]=p:install_read_tap(ring_entry,ring_entry+15,'passive native ring child birth',function()
 if p:read_u16(0x01061b30)~=5 then return end
 local main,actor=cpu.A13.value,cpu.A8.value
 if main<0x01000000 or main>=0x01100000 or actor<0x01000000 or actor>=0x01100000 then return end
 ring_children[main]={frame=frame,actor=actor}
 log('RING_CHILD',string.format('main=%08X actor=%08X actor_id=%d owner=%08X link290=%08X link2a0=%08X p1_main=%08X p2_main=%08X',main,actor,p:read_u16(actor+0x1f0),p:read_u32(main+0xc0),p:read_u32(main+0x290),p:read_u32(main+0x2a0),p:read_u32(slots[1].main),p:read_u32(slots[2].main)))
end)
'''
source=source.replace(marker,extra+'\n'+marker)
needle="   log('HEALTH',string.format(";assert source.count(needle)==1
extra=r'''
   if p:read_u16(0x01061b30)==5 and cpu.PC.value==0xff836700 then
    local before,after=p:read_u16(at),data&0xffff
    local child=ring_children[cpu.A13.value]
    if before<=161 and after<before then
     log('HIT_OWNER',string.format('slot=%d before=%d after=%d a8=%08X a13=%08X ring_born=%d ring_actor=%08X p1_actor=%08X p2_actor=%08X',n,before,after,cpu.A8.value,cpu.A13.value,child and child.frame or -1,child and child.actor or 0,p:read_u32(slots[1].actor),p:read_u32(slots[2].actor)))
    end
   end
'''
source=source.replace(needle,extra+needle)
source=source.replace('frame>=24000','frame>=18500').replace('maximum_fields=24000','maximum_fields=18500')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_ring_spacing_runtime','audit_current_sonya_mirror_ring_hit_owner_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared sparse passive ring-child damage linkage;18500 fields/no media')
