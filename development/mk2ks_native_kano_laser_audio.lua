-- Same physically earned laser trial; full native PCM/DAC and all19 voices.
-- No gameplay writes or changes to the original physical controller.
dofile('mk2ks_native_kano_laser_burst.lua')
local filename='mk2ks_current_tomb_winner_mix_observer_v5779.lua'
local file=assert(io.open(filename,'r'));local source=file:read('a'):gsub('\r\n','\n');file:close()
local function replace(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('local function active()return origin and frame<=origin+1100 end',
 'local function active()return origin and frame<=origin+750 end')
replace('0xff8bdfe0,0xff8bdfef','0xffd85800,0xffd8580f')
replace('at~=0xff8bdfe0','at~=0xffd85800')
replace("p:read_u16(a+0x1f0)~=assert(({kano=17,sonya=18})[os.getenv('MK2KS_STAGE_WINNER')])",
 'p:read_u16(a+0x1f0)~=17')
-- The physical trial already dumps the entire initialized guest once.
local begin=assert(source:find('  -- Native bit-addressed program reads,',1,true))
local finish=assert(source:find("  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do",begin,true))
source=source:sub(1,begin-1)..source:sub(finish)
-- Conservatively expand every old14-channel loop, without narrowing PCM.
local count;source,count=source:gsub('for n=0,13 do','for n=0,18 do');assert(count==2)
source,count=source:gsub('for channel=0,13 do','for channel=0,18 do');assert(count==2)
replace("assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')",
 "assert(checks==2 and origin and frame==origin+751,'Both complete sound ROM checks and same physical laser terminal')")
assert(load(source,'@'..filename..'::full_native_laser_audio','t',_G))()

local frame,owners,channels,taps=0,{},{},{}
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local function log(tag,s)
 print(string.format('MK2_LAUDIO_%s frame=%d seconds=%.12f writes=0 assistance=none %s',tag,frame,emu.time(),s))
end
local function pool(phase)
 local values={}
 for i=0,4 do values[#values+1]=string.format('%04X,%d',owners.priority:read(i),owners.remaining:read(i))end
 log('POOL',string.format('phase=%s slot=%d actor=%08X main=%08X mode=%d slots=%s',phase,
  owners.slot:read(0),owners.actor:read(0),owners.main:read(0),p:read_u16(0x010601d0),table.concat(values,';')))
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':'].items)do
   local field=name:match('m_mk2ks_finish_audio_(.+)$')
   if field then assert(not owners[field]);owners[field]=emu.item(index)end
  end
  assert(owners.actor and owners.main and owners.slot and owners.priority and owners.remaining)
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then channel=tonumber(channel,16);channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)end
  end
  for n=0,18 do assert(channels[n] and channels[n].source_num and channels[n].source_len and channels[n].pos)end
  taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'passive exact laser audio marker',function(at,data,mask)
   if at==0x01d01030 and mask==0xffff and data>=0x6b40 and data<=0x6b44 then
    log('MARKER',string.format('marker=%04X pc=%08X a8=%08X a13=%08X id=%d',data,cpu.PC.value,cpu.A8.value,cpu.A13.value,p:read_u16(cpu.A8.value+0x1f0)))
    pool('port_before_dispatch')
   end
  end)
 end
 if frame>=2800 then pool('video')end
end)
emu.register_sound_update(function()
 if frame>=2800 then pool('sound')end
end)
emu.register_stop(function()
 pool('terminal')
 for n=0,18 do local c=channels[n];log('CHANNEL_TERMINAL',string.format('channel=%d sample=%d length=%d pos=%.17g',
  n,c.source_num:read(0),c.source_len:read(0),string.unpack('<d',c.pos:read_block(0,8))))end
 for _,tap in ipairs(taps)do tap:remove()end
end)
