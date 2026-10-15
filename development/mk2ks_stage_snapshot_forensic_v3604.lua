-- Actual current scene pixels and shared native palette/reset pass-through.
-- Read-only observer; the preserved v806 controller owns all physical inputs.
dofile('mk2ks_current_stage_provenance_v3595.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local frame,origin,retired,pixels=0,nil,nil,0
local taps={}
local pending_palette,pending_reset=nil,nil
local allocations,resets,matching_allocations,matching_sprites=0,0,0,0
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function registers()
 local values={string.format('%08X',cpu.ST.value),string.format('%08X',cpu.SP.value)}
 for i=0,14 do values[#values+1]=string.format('%08X',cpu['A'..i].value)end
 return table.concat(values,',')
end
local function log(tag,value)
 print(string.format('MK2_STAGE_TRANSFER_%s frame=%d writes=0 assistance=none %s',tag,frame,value or''))
end
local function tap(entry,name,callback)
 taps[#taps+1]=p:install_read_tap(entry,entry+15,name,function(at,data,mask)
  if at==entry and cpu.PC.value==entry+16 and mask==0xffff then callback(data)end
 end)
end
if os.getenv('MK2KS_STAGE_NO_HOOKS')~='1' then
tap(0xff80cf60,'actual palette hook entry',function(data)
 assert(data==0xc080 and not pending_palette)
 allocations=allocations+1
 local request=cpu.A0.value
 if request==0xfecdf710 then matching_allocations=matching_allocations+1 end
 pending_palette={serial=allocations,request=request,state=registers()}
 log('ALLOC_ENTRY',string.format('serial=%d request=%08X regs=%s',allocations,request,pending_palette.state))
end)
tap(0xfffe2e00,'actual preserved palette allocator prologue',function(data)
 assert(data==0x098f and pending_palette)
 local prior=pending_palette;local state=registers()
 -- This non-Friendship scene must take only the untouched stock request path.
 assert(prior.request~=0xfecdf710 and state==prior.state)
 log('ALLOC_RESUME',string.format('serial=%d request=%08X regs=%s exact=1',prior.serial,cpu.A0.value,state))
 pending_palette=nil
end)
tap(0xff83f060,'actual sprite pool reset hook entry',function(data)
 assert(data==0xc080 and not pending_reset)
 resets=resets+1
 local actor=p:read_u32(0x0105d480)
 local seen,count,eligible={},0,0
 while actor~=0 do
  assert(valid(actor)and not seen[actor]and count<512)
  seen[actor]=true;count=count+1
  local pose=p:read_u32(actor+0x1d0)
  if pose>=0xfe9d2610 and pose<=0xfe9d2790 then
   local bank=p:read_u16(actor+0x140)&255
   local cell=0x0105bb30+(bank<<6)
   if p:read_u32(cell)==0xfffe2800 and p:read_i16(cell+0x20)>0 then eligible=eligible+1 end
  end
  actor=p:read_u32(actor)
 end
 matching_sprites=matching_sprites+eligible
 pending_reset={serial=resets,state=registers(),sprites=count,eligible=eligible}
 assert(eligible==0)
 log('RESET_ENTRY',string.format('serial=%d sprites=%d eligible=%d regs=%s',resets,count,eligible,pending_reset.state))
end)
tap(0xfffe33a0,'actual restored original reset prefix',function(data)
 assert(data==0x5600 and pending_reset)
 local prior=pending_reset;local state=registers()
 assert(state==prior.state)
 log('RESET_RESUME',string.format('serial=%d regs=%s exact=1',prior.serial,state))
 pending_reset=nil
end)
end
tap(0xff8bdfe0,'native earned Tomb begin',function()
 if origin then return end
 assert(p:read_u16(0x01061ac0)==1)
 origin=frame
 log('BEGIN',string.format('origin=%d actor=%08X main=%08X id=%d',origin,cpu.A8.value,cpu.A13.value,p:read_u16(cpu.A8.value+0x1f0)))
end)
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()
 if not origin then return end
 if not retired and p:read_u32(0x01060220)==0 and p:read_u32(0x01060df0)==0 then
  retired=frame
  log('RETIRED',string.format('origin=%d retired=%d mode=%d',origin,retired,p:read_u16(0x010601d0)))
 end
 if frame<=origin or retired and frame>retired+30 then return end
 local raw=manager.machine.video:snapshot_pixels()
 assert(screen.width==400 and screen.height==254 and #raw==400*254*4)
 local hex=raw:gsub('....',function(word)return string.format('%08X',string.unpack('<I4',word))end)
 pixels=pixels+1
 io.stdout:write(string.format('MK2_STAGE_TRANSFER_PIXELS frame=%d age=%d width=400 height=254 bytes=%d encoding=u32le_as_hex_numeric writes=0 assistance=none\n',frame,frame-origin,#raw),hex,'\n')
end)
emu.register_stop(function()
 assert(not pending_palette and not pending_reset)
 log('RESULT',string.format('origin=%d retired=%d pixels=%d allocations=%d resets=%d matching_allocations=%d matching_sprites=%d',
  origin or-1,retired or-1,pixels,allocations,resets,matching_allocations,matching_sprites))
 for _,handle in ipairs(taps)do handle:remove()end
end)
