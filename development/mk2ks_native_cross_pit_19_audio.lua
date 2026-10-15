-- Same earned opposite-character Pit; expand only passive channel coverage.
dofile('mk2ks_current_cross_tomb_provenance_v5834.lua')
local file=assert(io.open('mk2ks_current_tomb_winner_mix_observer_v5779.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local count
source,count=source:gsub('for n=0,13 do','for n=0,18 do');assert(count==2)
source,count=source:gsub('for channel=0,13 do','for channel=0,18 do');assert(count==2)
local function replace(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
replace("0xff8bdfe0,0xff8bdfef,'actual native Tomb mirror audio origin'",
 "0xff8bdde0,0xff8bddef,'actual native Pit audio origin'")
replace('at~=0xff8bdfe0','at~=0xff8bdde0')
assert(load(source,'@complete5779_cross_tomb_all19_channels','t',_ENV))()

-- Observe added finish-audio ownership and actual terminal channel retirement.
local frame,owners,channels=0,{},{}
emu.register_frame(function()
 frame=frame+1
 if frame~=1 then return end
 for name,index in pairs(manager.machine.devices[':'].items)do
  local field=name:match('m_mk2ks_finish_audio_(.+)$')
  if field then assert(not owners[field]);owners[field]=emu.item(index)end
 end
 assert(owners.actor and owners.main and owners.slot and owners.priority and owners.remaining)
 for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
  local channel,field=name:match('^(%x+)/chan%.(.+)$')
  if channel then
   channel=tonumber(channel,16);channels[channel]=channels[channel]or{}
   channels[channel][field]=emu.item(index)
  end
 end
 for n=0,18 do assert(channels[n]and channels[n].source_num and channels[n].source_len and channels[n].pos)end
end)
emu.register_stop(function()
 local slots={}
 for n=0,4 do slots[#slots+1]=string.format('%04X,%d',owners.priority:read(n),owners.remaining:read(n))end
 print(string.format('MK2_CROSS_TOMB_AUDIO_POOL frame=%d writes=0 assistance=none slot=%d actor=%08X main=%08X slots=%s',
  frame,owners.slot:read(0),owners.actor:read(0),owners.main:read(0),table.concat(slots,';')))
 for n=0,18 do
  local c=channels[n]
  print(string.format('MK2_CROSS_TOMB_AUDIO_TERMINAL frame=%d writes=0 assistance=none channel=%d sample=%d length=%d pos=%.17g',
   frame,n,c.source_num:read(0),c.source_len:read(0),string.unpack('<d',c.pos:read_block(0,8))))
 end
end)

-- Preserve the original failure-only deadline and complete 1101-field scene.
emu.register_frame_done(function()
 if emu.time()>=890 then
  print(string.format('MK2_TOMB_SOURCE_HOST_DEADLINE frame=%d writes=0 assistance=none',frame))
  manager.machine:exit()
 end
end)
