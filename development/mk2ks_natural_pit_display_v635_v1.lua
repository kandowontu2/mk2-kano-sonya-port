-- Unchanged cold real-input campaign; this observer only reads/saves output.
dofile('mk2ks_natural_campaign_probe_v11.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local screen=manager.machine.screens[':screen']
local frame,origin,last_lookup,snapshots=0,nil,nil,0
local taps={}
local table=p:read_u32(0xff85c330)
assert(table==0xff180800 and table==p:read_u32(0xff85c4a0))
local function log(tag,value)
 print(string.format('MK2_PIT_DISPLAY_%s frame=%d writes=0 assistance=none %s',tag,frame,value or''))
end
taps[#taps+1]=p:install_read_tap(table,table+19*32-1,'actual Pit display origin',function(at)
 if cpu.PC.value~=0xff83b850 or(at-table)%32~=0 then return end
 if not origin then origin=frame end
 last_lookup=frame
 log('LOOKUP',string.format('at=%08X id=%d a8=%08X a13=%08X origin=%d',at,(at-table)//32,cpu.A8.value,cpu.A13.value,origin))
end)
taps[#taps+1]=p:install_write_tap(0x01d01020,0x01d0103f,'actual native sound commands',function(at,data,mask)
 if p:read_u16(0x010601d0)~=9 then return end
 log('SOUND',string.format('at=%08X data=%04X mask=%04X pc=%08X a8=%08X a13=%08X',at,data,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
end)
emu.register_frame(function()frame=frame+1 end)
emu.register_frame_done(function()
 if not origin or frame<origin or frame>origin+330 then return end
 local file=string.format('pit_display_%d.png',frame)
 screen:snapshot(file);snapshots=snapshots+1
 log('SNAP',string.format('origin=%d mode=%d start=%04X control=%04X tap=%04X file=%s',origin,p:read_u16(0x010601d0),p:read_u16(0xc0000090),p:read_u16(0xc0000080),p:read_u16(0xc00001b0),file))
end)
emu.register_stop(function()
 log('RESULT',string.format('origin=%d last_lookup=%d snapshots=%d scope=natural_Pit_display_audio_capture_verification_pending',origin or -1,last_lookup or -1,snapshots))
 for _,tap in ipairs(taps)do tap:remove()end
end)
