-- Read-only source inspection of the genuine donor. Never supplies game state.
local d=assert(manager.machine.debugger)
local cpu=manager.machine.devices[':maincpu'];d.visible_cpu=cpu
local p=cpu.spaces.program;local words={}
for at=0xff800000,0xfffffff0,16 do words[#words+1]=string.pack('<I2',p:read_u16(at))end
local raw=table.concat(words)
print('MK3_BALL_DONOR_ROM bytes='..#raw..' hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
local prefix='audit_v6623_donor_ball_startup_source/'
d:command('dasm '..prefix..'cannonball.asm,FF9E6300,1000')
d.execution_state='run'
local fields=0
mk3_startup_source_subscription=emu.add_machine_frame_notifier(function()
 fields=fields+1
 if fields>=30 then print('MK3_BALL_DONOR_SOURCE_TERMINAL fields='..fields..' writes=0');manager.machine:exit()end
end)
