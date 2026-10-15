-- Exact accepted cold controls; observe the previously failed switch only.
dofile('mk2ks_kano_current_p2_campaign_ram_v4472.lua')
local h=assert(io.open('mk2ks_native_tomb_ram_v3624.lua','r'))
local ram=h:read('a');h:close()
local cut=assert(ram:find('local handle=assert(io.open',1,true))
assert(load(ram:sub(1,cut-1),'@original3624_RAM_transport_only_4599','t',_ENV))()
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local palette=manager.machine.palettes[':palette']
local frame,origin,ko,wins,seen=0,nil,nil,0,false
local taps={};local vram
for _,device in pairs(manager.machine.devices)do for name,index in pairs(device.items)do
 if name:match('m_local_videoram$')then assert(not vram);vram=emu.item(index)end
end end
assert(vram and vram.size==2 and vram.count>=512*512)
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function clock()
 return string.format('start=%04X dpyadr=%04X control=%04X tap=%04X vcount=%d vsblnk=%d veblnk=%d seconds=%.9f',
  p:read_u16(0xc0000090),p:read_u16(0xc00001e0),p:read_u16(0xc0000080),p:read_u16(0xc00001b0),
  p:read_u16(0xc00001d0),p:read_u16(0xc0000060),p:read_u16(0xc0000050),manager.machine.time:as_double())
end
local function log(tag,value)
 print(string.format('MK2_ENDING_PROBE_%s frame=%d identity=17 side=2 writes=0 assistance=none %s',tag,frame,value))
end
taps[#taps+1]=p:install_read_tap(0xfffefa20,0xfffefa2f,'actual own first final-stage winner',function(at,data,mask)
 if at~=0xfffefa20 or cpu.PC.value~=0xff8296b0 or p:read_u16(0x01061b30)~=16 or
  p:read_u16(0x01061b00)~=2 or p:read_u16(0x01060e50)~=17 or
  p:read_u16(0x010602f0)~=0 or p:read_u16(0x01060ec0)<=0 then return end
 wins=wins+1;log('WIN',string.format('entry=%08X pc=%08X mask=%04X value=%04X',at,cpu.PC.value,mask,data))
end)
taps[#taps+1]=p:install_write_tap(0x010602f0,0x010602ff,'actual own final collision KO',function(at,data,mask)
 if ko or at~=0x010602f0 or data~=0 or mask~=0xffff or p:read_u16(at)<=0 or
  cpu.PC.value~=0xff836700 or not seen or wins~=1 or p:read_u16(0x01061b30)~=16 or
  p:read_u16(0x01060e50)~=17 or p:read_u16(0x01060ec0)<=0 then return end
 ko=frame;log('KO',string.format('at=%08X before=%d pc=%08X mask=%04X',at,p:read_u16(at),cpu.PC.value,mask))
end)
taps[#taps+1]=p:install_write_tap(0xc0000090,0xc000009f,'actual DPYSTRT request before native commit',function(at,data,mask)
 if at~=0xc0000090 or not origin or frame-origin<1095 or frame-origin>1145 then return end
 log('START_WRITE',string.format('age=%d before=%04X value=%04X mask=%04X pc=%08X %s',frame-origin,p:read_u16(at),data,mask,cpu.PC.value,clock()))
end)
emu.register_frame(function()
 frame=frame+1;assert(#taps==3)
 local mode=p:read_u16(0x010601d0);local roster=p:read_u16(0x01060e50)
 if mode==4 then wins=0 end
 if p:read_u16(0x01060dc0)==1 and roster==17 and valid(p:read_u32(0x01060df0))and p:read_u16(0x01060ec0)>0 then seen=true end
 if not origin and ko and seen and wins==1 and mode==11 and p:read_u16(0x01061b30)==16 and
  p:read_u16(0x01061b00)==2 and roster==17 and p:read_u16(0x010602f0)==0 and
  p:read_u16(0x01060ec0)>0 and p:read_u32(0x01060220)==0 and p:read_u32(0x01060df0)==0 then
  origin=frame;log('BEGIN',string.format('origin=%d final_ko=%d own_wins=%d %s',origin,ko,wins,clock()))
 end
 if origin and frame-origin>=1095 and frame-origin<=1145 then log('FRAME',string.format('age=%d %s',frame-origin,clock()))end
end)
emu.register_frame_done(function()
 if not origin or frame-origin<1100 or frame-origin>1140 then return end
 local raw=vram:read_block(0,512*512*2)
 MK2KS_TOMB_RAM_SAVE(string.format('display_vram_%d.bin',frame),raw)
 local colors={};for pen=0,32767 do colors[#colors+1]=string.pack('<I4',palette:pen_color(pen)&0xffffff)end
 MK2KS_TOMB_RAM_SAVE(string.format('display_palette_%d.bin',frame),table.concat(colors))
 MK2KS_TOMB_RAM_PIXELS(string.format('display_%d.png',frame))
 log('SAMPLE',string.format('age=%d origin=%d %s',frame-origin,origin,clock()))
end)
emu.register_stop(function()
 log('RESULT',string.format('origin=%d final_ko=%d scope=read_only_failed_switch_diagnosis_not_video_acceptance',origin or-1,ko or-1))
 for _,tap in ipairs(taps)do tap:remove()end
end)
