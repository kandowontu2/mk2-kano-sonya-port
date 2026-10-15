-- Retain every original read-only audio observer and earned physical input.
local file=assert(io.open('mk2ks_scorpion_secondary_audio_ram_v4663.lua','rb'))
local wrapper=file:read('a');file:close()
local marker="assert(load(source,'@entire4210_audio_only_Scorpion_origin_and_4534_controls_4657','t',_ENV))()"
local first,last=assert(wrapper:find(marker,1,true))
assert(not wrapper:find(marker,last+1,true),'Unique original wrapper execution')
local addition=[====[
once("emu.register_frame(function()",[==[
taps[#taps+1]=p:install_read_tap(0xffa13ba0,0xffa13baf,'actual native packet caller stack',function(at)
 if at~=0xffa13ba0 or cpu.PC.value~=at+16 or not active()then return end
 local a,m,sp=cpu.A8.value,cpu.A13.value,cpu.SP.value
 assert(valid(sp),'Actual native packet stack in guest RAM')
 log('PACKET_CALLER',string.format('entry=%08X a1=%08X a3=%08X a4=%08X a8=%08X a13=%08X sp=%08X return_pc=%08X id=%d owner=%08X',
  at,cpu.A1.value,cpu.A3.value,cpu.A4.value,a,m,sp,p:read_u32(sp),
  valid(a)and p:read_u16(a+0x1f0)or-1,valid(m)and p:read_u32(m+0xc0)or 0))
end)
emu.register_frame(function()
]==])
once("assert(#taps==15,'Every audio observer retained')","assert(#taps==16,'Every audio observer retained')")
]====]
wrapper=wrapper:sub(1,first-1)..addition..wrapper:sub(first)
assert(load(wrapper,'@whole4663_plus_readonly_packet_caller_4761','t',_ENV))()
