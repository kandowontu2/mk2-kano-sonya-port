-- Native loser leaves; observe the winner's actual next CPU match, without inputs.
local file=assert(io.open('mk2ks_native_subzero_shatter_lifecycle_v4943.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'Unique subsequent CPU match anchor')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('if frame-natural==60 then','if false then')
replace('frame-deep>=1200','frame-deep>=2400')
replace("assert(load(source,'@native_shatter_lifecycle_v4943','t',_ENV))()",[==[
replace('end)\n]])', [=[end)
emu.register_frame_done(function()
 if not natural or frame-natural<60 or p:read_u16(0x010601d0)~=2 then return end
 local own=p:read_u32(slots[winner].actor);local enemy=p:read_u32(slots[side].actor)
 local om=p:read_u32(slots[winner].main);local em=p:read_u32(slots[side].main)
 if not valid(own)or not valid(enemy)or not valid(om)or not valid(em)then return end
 if p:read_u32(om+0xc0)~=own or p:read_u32(em+0xc0)~=enemy then return end
 if p:read_u16(own+0x1f0)~=8 or p:read_u16(slots[winner].state)~=1 or p:read_u16(slots[side].state)~=0 then return end
 local op,ep=p:read_u32(own+0x1d0),p:read_u32(enemy+0x1d0)
 if op==0xffd62400 or op==0xffd62480 or op==0xffd62900 or op==0xffd62960 or ep==0xffd62400 or ep==0xffd62480 or ep==0xffd62900 or ep==0xffd62960 then return end
 local raw,width,height=screen:pixels();assert(width==400 and height==254 and #raw==400*254*4)
 print(string.format('MK2_EARNED_SUBZERO_RGB frame=%d width=%d height=%d bytes=%d hex=%s',frame,width,height,#raw,raw:gsub('.',function(c)return string.format('%02x',c:byte())end)))
 log('LIFECYCLE_END',string.format('fracture=%d wrap=%d natural=%d mode=2 winner_state=1 enemy_state=0 winner_actor=%08X enemy_actor=%08X winner_main=%08X enemy_main=%08X winner_owner=%08X enemy_owner=%08X winner_id=%d enemy_id=%d winner_hp=%d enemy_hp=%d winner_pose=%08X enemy_pose=%08X',
  fracture or-1,wrap or-1,natural,own,enemy,om,em,p:read_u32(om+0xc0),p:read_u32(em+0xc0),p:read_u16(own+0x1f0),p:read_u16(enemy+0x1f0),p:read_u16(slots[winner].hp),p:read_u16(slots[side].hp),op,ep))
 manager.machine:exit()
end)
]])]=])
assert(load(source,'@native_shatter_lifecycle_v4943_nextmatch','t',_ENV))()
]==])
assert(load(source,'@actual_native_shatter_next_cpu_match_v4951','t',_ENV))()
