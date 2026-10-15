-- Read-only native morph drawing, including early identity/palette handoffs.
local side=tonumber(os.getenv('MK2KS_HUMAN_SHANG_SIDE') or '1')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local slot=side==1 and {actor=0x01060220,main=0x01060260,state=0x010601f0} or {actor=0x01060df0,main=0x01060e30,state=0x01060dc0}
local frame,until_frame,collecting,ordinal,phase=0,-1,false,0,'none'
local taps,regs,palettes={},{},{}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function signed(v)return v>=0x8000 and v-0x10000 or v end
local function own()
    return p:read_u16(slot.state)==1 and cpu.A8.value==p:read_u32(slot.actor) and cpu.A13.value==p:read_u32(slot.main)
end
local function log(tag,s)print(string.format('MK2_MORPH_RENDER_%s frame=%d side=%d phase=%s %s writes=0',tag,frame,side,phase,s))end
for _,spec in ipairs({{0xff86e480,'forward'},{0xffa16300,'reverse'}}) do
    taps[#taps+1]=p:install_read_tap(spec[1],spec[1]+15,'morph render window '..spec[2],function()
        if cpu.PC.value==spec[1]+16 and own() then
            phase=spec[2];until_frame=frame+28;log('WINDOW',string.format('actor=%08X main=%08X until_frame=%d',cpu.A8.value,cpu.A13.value,until_frame))
        end
    end)
end
taps[#taps+1]=p:install_read_tap(0xff9075c0,0xff9075cf,'actual morph body palette restore',function()
    if cpu.PC.value==0xff9075d0 and own() and frame<=until_frame then
        log('RESTORE_PALETTE',string.format('actor=%08X main=%08X id=%d flags=%04X body=%04X',cpu.A8.value,cpu.A13.value,p:read_u16(cpu.A8.value+0x1f0),p:read_u16(cpu.A13.value+0x210),p:read_u16(cpu.A8.value+0x160)))
    end
end)
taps[#taps+1]=p:install_write_tap(0x01a80000,0x01a800ff,'morph actual native copy DMA',function(at,data)
    if collecting then return end
    local reg=(at-0x01a80000)//16;regs[reg]=data&0xffff
    if reg~=1 or (data&0x8000)==0 or frame>until_frame then return end
    collecting=true;ordinal=ordinal+1
    local bank=(regs[8] or 0)&0x7f00;local words={}
    for i=0,63 do words[#words+1]=string.format('%04X',p:read_u16(0x01800000+(bank+i)*16))end
    local colors=table.concat(words,',')
    if palettes[bank]~=colors then palettes[bank]=colors;log('PALETTE',string.format('ordinal=%d bank=%04X colors=%s',ordinal,bank,colors))end
    log('DMA',string.format('ordinal=%d pc=%08X graphic=%08X command=%04X x=%d y=%d width=%d height=%d palette=%04X color=%04X scale_x=%04X scale_y=%04X lskip=%04X',ordinal,cpu.PC.value,(regs[2] or 0)|((regs[3] or 0)<<16),data&0xffff,signed(regs[4] or 0),signed(regs[5] or 0),regs[6] or 0,regs[7] or 0,regs[8] or 0,regs[9] or 0,regs[10] or 0,regs[11] or 0,regs[0] or 0))
    collecting=false
end)
emu.register_frame(function()
    collecting=true;frame=frame+1;ordinal=0
    if frame<=until_frame then
        local a,m=p:read_u32(slot.actor),p:read_u32(slot.main)
        if valid(a) and valid(m) then
            local pose,list=p:read_u32(a+0x1d0),p:read_u32(a+0x1a0);local count=0
            if valid(list) and pose>=0xfe800000 then
                for index=0,15 do
                    local descriptor=p:read_u32(pose+index*32)
                    if descriptor==0 then break end
                    local at=list+index*0x70;count=count+1
                    log('COMPONENT',string.format('actor=%08X main=%08X pose=%08X index=%d descriptor=%08X graphic=%08X command=%04X width=%d height=%d dx=%d dy=%d',a,m,pose,index,descriptor,p:read_u32(at),p:read_u16(at+0x40),p:read_u16(at+0x20),p:read_u16(at+0x30),signed(p:read_u16(at+0x50)),signed(p:read_u16(at+0x60))))
                end
                log('BODY',string.format('actor=%08X main=%08X id=%d pose=%08X components=%d flags=%04X x=%d y=%d floor=%d task_flags=%04X body=%04X',a,m,p:read_u16(a+0x1f0),pose,count,p:read_u16(a+0xf0),signed(p:read_u16(a+0x90)),signed(p:read_u16(a+0xb0)),signed(p:read_u16(m+0x200)),p:read_u16(m+0x210),p:read_u16(a+0x160)))
            end
        end
        manager.machine.screens[':screen']:snapshot(string.format('choreo_%d.png',frame))
    end
    collecting=false
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
dofile('mk2ks_human_shang_probe.lua')
