-- Read-only whole initialized guest; original normal-input and drawing drivers.
local p=manager.machine.devices[':maincpu'].spaces.program
local dumped=false
local output=assert(os.getenv('MK2KS_MORPH_CAPTURE_OUT'))
emu.register_frame(function()
 if dumped then return end
 dumped=true
 local words={}
 for address=0xff800000,0xfffffff0,16 do
  words[#words+1]=string.pack('<I2',p:read_u16(address))
 end
 local raw=table.concat(words)
 assert(#raw==0x100000,'Whole one-megabyte initialized guest required')
 local file=assert(io.open(output..'/guest_maincpu.bin','wb'))
 file:write(raw);file:close()
 print('MK2_MORPH_GUEST frame=1 bytes='..#raw..' start=FF800000 stop=100000000 writes=0')
end)
if os.getenv('MK2KS_MORPH_CAPTURE_RENDER')=='1' then
 dofile('mk2ks_morph_render_probe.lua')
else
 dofile('mk2ks_human_shang_probe.lua')
end

