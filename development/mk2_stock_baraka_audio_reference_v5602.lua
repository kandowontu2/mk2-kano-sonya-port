-- Genuine original MK2 Cage versus Baraka, not a proxy for either import.
-- Retain whole physical controller and passive native audio observers.
-- Requested guest, sound ROM, DAC and PCM bytes travel only to verifier RAM.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
assert(not manager.machine.devices[':mk2ksvoices'],'Original MK2 has no imported voice device')
local function read(name)
 local f=assert(io.open(root..'/'..name,'rb'))
 local s=f:read('*a');f:close();return s:gsub('\r\n','\n')
end
local function replace(s,before,after)
 local first,last=s:find(before,1,true)
 assert(first and not s:find(before,last+1,true),'One exact whole-source adaptation')
 return s:sub(1,first-1)..after..s:sub(last+1)
end
local function execute(s,name)assert(load(s,'@stock5602_whole_'..name,'t',_ENV))()end
local s=read('mk2ks_stock_head_victim_v921.lua')
s=replace(s,'local identity=assert(({kano=17,sonya=18})[name])',
 'local identity=assert(({cage=2,kitana=4})[name])')
s=replace(s,"screen:snapshot(string.format('stock_head_%d_%03d.png',action_start,frame-action_start))",
 "assert(manager.machine.screens[':screen'],'Requested snapshot omitted; passive display record only')")
execute(s,'921_original_roster_physical_controller_without_snapshot_sink')

s=read('mk2ks_kitana_audio_queue_ram_v3939.lua')
s=replace(s,"dofile('mk2ks_stock_earned_ram_v3918.lua')\n",'')
s=replace(s,'0xff8cc650,0xff8cc65f','0xff8cb4a0,0xff8cb4af')
s=replace(s,'at~=0xff8cc650','at~=0xff8cb4a0')
s=replace(s,'p:read_u16(a+0x1f0)~=4','p:read_u16(a+0x1f0)~=3')
s=replace(s,'a13=%08X id=4','a13=%08X id=3')
s=replace(s,[[  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then channel=tonumber(channel,16);channels[channel]=channels[channel]or{};channels[channel][field]=emu.item(index)end
  end
  for n=0,13 do local c=assert(channels[n]);assert(c.source_len and c.pos and c.source_num and c.loop and c.paused)end]],
 "  assert(not manager.machine.devices[':mk2ksvoices'],'No fabricated imported channel ledger in stock reference')")
s=replace(s,[[ if active()then
  for n=0,13 do
   local c=channels[n]
   log('CHANNEL',string.format('channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d',n,c.source_num:read(0),c.source_len:read(0),
    string.unpack('<d',c.pos:read_block(0,8)),c.loop:read(0),c.paused:read(0)))
  end
 end
]],'')
execute(s,'3939_original_native_audio_routes_and_PCM_without_import_channels')

s=read('mk2ks_current_baraka_priority_ram_v5554.lua')
s=replace(s,[[local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local file=assert(io.open(root..'/mk2ks_current_baraka_audio_ram_v5536.lua','rb'))
local source=file:read('*a');file:close()
assert(load(source,'@whole5536_current_native_physical_raster_and_audio','t',_ENV))()
]],'')
execute(s,'5554_original_fighter_priority_observer_only')
s=read('mk2ks_current_baraka_announcer_ram_v5565.lua')
s=replace(s,"assert(load(source,'@unchanged_whole5554_native_observer','t',_ENV))()\n",'')
execute(s,'5565_original_dual_priority_and_announcer_observers_only')
s=read('mk2ks_current_baraka_packet_origin_v5576.lua')
s=replace(s,[[local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local file=assert(io.open(root..'/mk2ks_current_baraka_announcer_ram_v5565.lua','rb'))
local source=file:read('*a');file:close()
assert(load(source,'@whole5565_qualified_physical_raster_and_dual_dispatcher','t',_ENV))()
]],'')
execute(s,'5576_original_packet_entry_and_return_observers_only')
s=read('mk2ks_current_native_dac_ram_v5592.lua')
s=replace(s,[[local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_current_baraka_packet_origin_v5576.lua','rb'))
local s=f:read('*a');f:close()
assert(load(s,'@entire5576_native_physical_art_packet_audio_observers','t',_ENV))()
]],'')
execute(s,'5592_original_native_DAC_ring_and_serial_controls_only')
s=read('mk2ks_current_dcs_rom_source_v5585.lua')
s=replace(s,[[local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_current_baraka_packet_origin_v5576.lua','rb'))
local source=f:read('*a');f:close()
assert(load(source,'@entire5576_native_physical_art_audio_packet_observers','t',_ENV))()
]],'')
execute(s,'5585_original_complete_loaded_sound_ROM_startup_and_terminal_only')
print('MK2_ORIGINAL_REFERENCE_SETUP driver=mk2 victim=cage victim_id=2 winner=baraka winner_id=3 imported_voice_device=absent writes=0 assistance=none')
