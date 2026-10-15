-- Same failed physical case and error ancestry. Capture bounded SP and
-- cooperative stacks and the actual task list; all taps return nil.
dofile('mk2ks_current_challenger_ancestry_v6496.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame=0
local taps,counts={},{}
local function words(address,count)
 if address<0x01000000 or address>=0x01100000 then return 'outside_ram' end
 count=math.min(count,(0x01100000-address)//32)
 local out={};for i=0,count-1 do out[#out+1]=string.format('%08X',p:read_u32(address+i*32))end
 return table.concat(out,',')
end
for _,entry in ipairs({0xff80e0e0,0xffa1d860,0xff83f520,0xff83a4c0,0xff83a4e0,0xff8b6820,0xff8affb0,0xff8b5d20,0xff8b6450})do
 counts[entry]=0
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'challenger cleanup stacks '..entry,function(at)
  if frame<2000 or counts[entry]>=16 then return end
  counts[entry]=counts[entry]+1
  print(string.format('MK2_JC_ENTRY frame=%d at=%08X pc=%08X ordinal=%d a0=%08X a8=%08X a13=%08X sp=%08X stack=%s coop=%s actor=%s mode=%d writes=0 assistance=none',frame,at,cpu.PC.value,counts[entry],cpu.A0.value,cpu.A8.value,cpu.A13.value,cpu.SP.value,words(cpu.SP.value,24),words(cpu.A12.value,24),words(cpu.A8.value,24),p:read_u16(0x010601d0)))
  local cursor=p:read_u32(0x01068e30);local seen={}
  for i=1,128 do
   if cursor==0 or seen[cursor] or cursor<0x01000000 or cursor>=0x01100000 then break end
   seen[cursor]=true
   print(string.format('MK2_JC_TASK frame=%d entry=%08X ordinal=%d listIndex=%d task=%08X words=%s writes=0 assistance=none',frame,at,counts[entry],i,cursor,words(cursor,24)))
   cursor=p:read_u32(cursor)
  end
 end)
end
emu.register_frame_done(function()frame=frame+1 end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
