-- Preserve the full CPU-fetch-qualified Tomb/channel/PCM observer. Add only
-- actual ADSP input-latch reads; no injected packets or game/register writes.
dofile('mk2ks_current_tomb_audio_ram_v3664.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,origin,taps=0,nil,{}
taps[#taps+1]=p:install_read_tap(0xff8bdfe0,0xff8bdfef,'native sound delivery origin',function(at)
 if at==0xff8bdfe0 and cpu.PC.value==at+16 and frame>1 and not origin then origin=frame end
end)
local dsp=assert(manager.machine.devices[':dcs:dcs'])
taps[#taps+1]=dsp.spaces.data:install_read_tap(0x3400,0x37ff,'actual original MKII DCS input-latch reads',function(at,value,mask)
 if origin and frame<=origin+650 then
  print(string.format('MK2_TAUDIO_DELIVERY frame=%d seconds=%.12f writes=0 assistance=none at=%04X word=%04X mask=%04X dsp_pc=%04X',
   frame,emu.time(),at,value,mask,dsp.state.PC.value))
 end
end)
emu.register_frame(function()frame=frame+1 end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
